import json
import pytz
import jinja2

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from django.forms import model_to_dict
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.serializers.json import DjangoJSONEncoder, Serializer
from django.db.models import Q, F, BooleanField, Case, When, Value, Count, OuterRef, Subquery

from django_ratelimit.decorators import ratelimit

from .forms import (EmailTemplateForm, AttachmentForm, EmailConfigurationForm, 
                        EmailCampaignForm, EmailForm)
from .models import (EmailTemplate, EmailCampaign, EmailTemplateAttachment, 
                        EmailConfiguration, EmailCampaignTemplate, EMAIL_SEND_RULES)

from django.core.mail.backends.smtp import EmailBackend
from django.core.files.storage import default_storage
from utils.tasks import send_attachment_mail_celery
from utils.common import get_file_size, get_plain_text_from_html, is_valid_mail
from utils.mailing import test_email_credentials, send_email_with_attachments
from utils.decorators import login_required_for_post, login_required_rest_api


jinja_env = jinja2.Environment()


@login_required_for_post
@require_http_methods(['GET', 'POST'])
def email_template_create(request):

    edit = request.GET.get('edit')

    if request.method == 'GET':
        
        copy = request.GET.get('copy')

        context = {
            'subject': '',
            'body': '',
            'template_name': '',
            'variables': '',
            'attachements': [],
            'edit': edit
        }

        if edit:

            if not request.user.is_authenticated:
                return redirect('login')

            try:
                int(edit)
                template = EmailTemplate.objects.get(id=edit)
            except (ValueError, EmailTemplate.DoesNotExist):
                return render(request, '404.html') 

            if template.user == request.user:
                
                context = {
                    'template': template,
                    'edit': edit
                }

            elif template.public == True:
                
                kwargs = model_to_dict(template, exclude=['id', 'user', 'name', 'public'])

                temp = EmailTemplate.objects.create(id=None, user=request.user, name=f'{template.name} (copy)', public=False, **kwargs)
                modified_url = reverse('email-template-create') + f'?edit={temp.id}'

                return redirect(modified_url)

            else:
                return render(request, '404.html')


        if copy:

            if not request.user.is_authenticated:
                return redirect('login')

            try:
                int(copy)
            except ValueError:
                return render(request, '404.html') 


            template = EmailTemplate.objects.filter(id=copy)

            if not template.exists():
                return render(request, '404.html')

            dup_temp = template.last()
            dup_temp.copy_count += 1
            dup_temp.save()

            kwargs = model_to_dict(dup_temp, exclude=['id', 'user', 'name', 'public', 'copy_count'])

            temp = EmailTemplate.objects.create(id=None, user=request.user, name=f'{dup_temp.name} (copy)', public=False, **kwargs)
            # TODO: copy the attachments
            modified_url = reverse('email-template-create') + f'?edit={temp.id}'

            return redirect(modified_url)

        return render(request, 'email-template-create.html', context=context)
    
    if request.method == 'POST':
       
        if edit:
            try:
                int(edit)

            except ValueError:
                return render(request, '404.html') 

            email_template = EmailTemplate.objects.filter(id=edit)

            if not email_template.exists() or (email_template.last().public == False and email_template.last().user != request.user):
                return render(request, '404.html') 

        instance = None

        if edit:
            instance = EmailTemplate.objects.get(id=edit)
        
        template_form = EmailTemplateForm(request.POST or None, instance=instance)


        if template_form.is_valid():

            file_form = AttachmentForm(request.POST, request.FILES)
            template = template_form.save(commit=False)

            if edit:
                attachment_ids = request.POST.get('existing-attachments') or []
                attachments = EmailTemplateAttachment.objects.filter(template=template).exclude(id__in=attachment_ids).delete()

            if request.FILES:
                # if there are attachment check if the form is valid before
                if file_form.is_valid():
        
                    template.user = request.user
                    template.save()

                    EmailTemplateAttachment.objects.filter(template=template).delete()

                    for f in request.FILES.getlist('attachment'):
                        EmailTemplateAttachment.objects.create(template=template, attachment=f)

                else:
                    error = file_form.errors.as_data()
                    errors = [f'{list(error[x][0])[0]}' for x in error]

                    # print("error2: ", error)
                    return render(request, 
                                    'email-template-create.html', 
                                    {'error': ['error with file'], 
                                     'template': request.POST,
                                     'edit': edit
                                    })
            
            else:
                
                if edit:
                    template = EmailTemplate.objects.filter(id=edit).update(**template_form.cleaned_data)
                    EmailTemplateAttachment.objects.filter(template=template).delete()

                else:
                    template = template_form.save(commit=False)
                    template.user = request.user
                    template.save()

            return redirect('email-templates')

        else:
            error = template_form.errors.as_data()
            # print("error2: ", error)
            errors = [f'{list(error[x][0])[0]}' for x in error]
            return render(request, 'email-template-create.html', {'error': errors, 'template': request.POST})

    return render(request, 'email-template-create.html')


@login_required
@require_http_methods(['POST'])
def email_template_delete(request, id):

    try:
        EmailTemplate.objects.get(user=request.user, id=id).delete()

    except EmailTemplate.DoesNotExist:
        return render(request, '404.html')

    return redirect('email-templates')


@require_http_methods(['GET'])
def email_templates(request):

    public = request.GET.get('public')
    search_query = request.GET.get("search")
    page_number = request.GET.get("page", 1)

    private_templates = EmailTemplate.objects.filter(user__id=request.user.id)

    public_templates = EmailTemplate.objects.filter(public=True).order_by('copy_count')

    if public and search_query:
        public_templates = public_templates.filter(Q(subject__icontains=search_query)|Q(name__istartswith=search_query))

    if public == 'True':

        paginator = Paginator(public_templates, per_page=30)
        templates = paginator.get_page(page_number)

        return render(request, 'public-templates.html', context={'templates': templates})

    return render(request, 'email-templates.html', context={'private_templates': private_templates,
                                                            'public_templates': public_templates
                                                            })


def convert_local(user_time, user_timezone):
    local_timezone = pytz.timezone(user_timezone)

    # Convert the UTC datetime to the user's local timezone
    local_datetime = user_time.astimezone(local_timezone)

    return local_datetime.astimezone(pytz.UTC)


@login_required_for_post
def campaign_create_view(request):

    templates = EmailTemplate.objects.filter(user__id=request.user.id)
    emails = EmailConfiguration.objects.filter(user__id=request.user.id)
    rules  = EMAIL_SEND_RULES.choices

    user_timezone = request.COOKIES.get('user_timezone', 'Asia/Kolkata')

    context = {
            'templates': list(templates.values('name', 'id')),
            'emails': list(emails.values('id', 'email')),
            'rules': rules,
            **request.POST
        }

    edit = request.GET.get('edit')

    if edit:
        try:
            campaign = EmailCampaign.objects.get(id=edit, user=request.user.id)

            context['campaign'] = campaign

        except EmailCampaign.DoesNotExist:
            return render(request, '404.html')
        
    if request.method == 'POST':

        template = request.POST.get('template')
        email_from = request.POST.get('from_email')
        schedule = request.POST.get('schedule')
        scheduled = request.POST.get('scheduled')

        instance = None

        if edit:
            try:
                instance = EmailCampaign.objects.get(id=edit, user=request.user)

            except (EmailCampaign.DoesNotExist):
                return render(request, '404.html')

        campaign_form = EmailCampaignForm(request.POST or None, request.FILES or None, 
                                            instance=instance)

        followups = json.loads(request.POST.get('followups'))
       
        if campaign_form.is_valid():

            campaign = campaign_form.save(commit=False)
            campaign.user = request.user
            campaign.save()

            # If this is an edit request, update the existing campaign
            if edit:
                EmailCampaignTemplate.objects.filter(campaign=campaign).delete()

            email_form = EmailForm({
                                    'campaign': campaign.id, 
                                    'template': template, 
                                    'email': email_from,
                                    'email_send_rule': EMAIL_SEND_RULES.ALL,
                                    'schedule': schedule,
                                    'scheduled': True if scheduled else False,
                                    'followup': None,
                                    'user_timezone': user_timezone
                                    })

            if email_form.is_valid():

                main_email = email_form.save(commit=True)

                for i, x in enumerate(followups):
                    follow_up_form = EmailForm({
                                    'campaign': campaign, 
                                    'template': x['followup-template'], 
                                    'email': email_from,
                                    'email_send_rule': x['rule'],
                                    'schedule': x['followup-schedule'],
                                    'scheduled': True if x['followup-scheduled'] != "" else False,
                                    'followup': main_email,
                                    'user_timezone': user_timezone
                                    })
                    
                    if follow_up_form.is_valid():
                        follow_up_form.save(commit=True)
                    
                    else:
                        campaign.delete()
                        error = follow_up_form.errors.as_data()
                        errors = [f'{list(error[x][0])[0]}' for x in error] 
                        context['errors'] = errors
                        break
                
                return redirect('email-campaigns')

            else:
                campaign.delete()
                error = email_form.errors.as_data()
                errors = [f'{list(error[x][0])[0]}' for x in error] 
                context['errors'] = errors

        else:
            error = campaign_form.errors.as_data()
            errors = [f'{list(error[x][0])[0]}' for x in error] 
            context['errors'] = errors

    context['edit'] = edit
            
    return render(request, 'email-campaign-create.html', context)


# @login_required
@require_http_methods(['GET'])
def campaigns_view(request):

    view = request.GET.get('view')

    current_datetime = timezone.now()

    first_template_data = EmailCampaign.objects.filter(id=OuterRef('id')  # Correlate with the outer EmailCampaign
                                                                ).order_by('emailcampaigntemplate__schedule').values('emailcampaigntemplate__schedule',  'emailcampaigntemplate__template__subject')[:1]


    campaigns = EmailCampaign.objects.filter(user=request.user.id).annotate(
                                                                        total_templates=Count('emailcampaigntemplate'),
                                                                        completed_templates=Count(
                                                                            'emailcampaigntemplate',
                                                                            filter=Q(emailcampaigntemplate__completed=True)
                                                                        ),
                                                                        all_done=Case(
                                                                            When(
                                                                                total_templates=F('completed_templates'),
                                                                                then=Value(True)
                                                                            ),
                                                                            default=Value(False),
                                                                            output_field=BooleanField()
                                                                        ),
                                                                        first_template_schedule=Subquery(first_template_data.values('emailcampaigntemplate__schedule')),
                                                                        started=Case(
                                                                            When(first_template_schedule__gt=current_datetime, then=Value(True)),
                                                                            default=Value(False),
                                                                            output_field=models.BooleanField()
                                                                        ),
                                                                        subject=Subquery(first_template_data.values('emailcampaigntemplate__template__subject'))
                                                                )

    if view:
        try:
            campaign = campaigns.get(id=view)
          
            return render(request, 'campaign-details.html', context={'campaign': campaign})

        except (EmailCampaign.DoesNotExist):
            return render(request, '404.html')


    return render(request, 'email-campaigns.html', context={
                                                                'campaigns': campaigns,

                                                            })


@login_required
def delete_campaign_view(request, id):
    
    try:
        EmailCampaign.objects.get(user=request.user.id, id=id).delete()
    
    except (EmailCampaign.DoesNotExist):
        return render(request, "404.html")

    return redirect('email-campaigns')



@login_required_for_post
@require_http_methods(['GET', 'POST'])
def configuration_create_view(request):

    """
        used to configure the server
    """
    if request.method == 'GET':
        edit = request.GET.get('edit')
        email_type = request.GET.get('type', 'gmail')

        context = {'email_type': email_type}

        if edit:
            try:
                int(edit)
                configuration = EmailConfiguration.objects.get(id=edit, user=request.user)
                context['configuration'] = configuration
                if configuration.host and 'gmail' in configuration.host.lower():
                    context['email_type'] = 'gmail'
                else:
                    context['email_type'] = 'professional'

            except (ValueError, EmailConfiguration.DoesNotExist):
                return render(request, '404.html')
            
        return render(request, 'configure-server.html', context)

    else:
        edit = request.GET.get('edit')
        email_type = request.POST.get('email_type', request.GET.get('type', 'gmail'))

        post_data = request.POST.copy()
        # For Gmail, automatically supply host, port, and imap_host if omitted or empty
        if email_type == 'gmail':
            if not post_data.get('host'):
                post_data['host'] = 'smtp.gmail.com'
            if not post_data.get('port'):
                post_data['port'] = '587'
            if not post_data.get('imap_host'):
                post_data['imap_host'] = 'imap.gmail.com'

        form = EmailConfigurationForm(post_data)
        
        if form.is_valid():

            credentials = form.cleaned_data
            credentials_valid, error = test_email_credentials(email=credentials['email'], password=credentials['password'],
                                    host=credentials['host'], port=credentials['port'], imap_host=credentials['imap_host'])
            
            if credentials_valid != True:
                return render(request, 'configure-server.html', context={'errors': [error], 'configuration': credentials, 'email_type': email_type})

            if edit:
                try:
                    int(edit)
                    configuration = EmailConfiguration.objects.get(id=edit, user=request.user)
            
                except (ValueError, EmailConfiguration.DoesNotExist):
                    return render(request, '404.html')

                EmailConfiguration.objects.filter(id=edit, user=request.user).update(**form.cleaned_data)      

            else:
                # If this email is already connected for this user, update it with the new credentials
                user_configs = EmailConfiguration.objects.filter(user=request.user)
                existing_config = None
                for c in user_configs:
                    if c.email and c.email.lower() == form.cleaned_data['email'].lower():
                        existing_config = c
                        break

                if existing_config:
                    for key, value in form.cleaned_data.items():
                        setattr(existing_config, key, value)
                    existing_config.save()
                else:
                    configuration = form.save(commit=False)
                    configuration.user = request.user
                    configuration.save()

                return redirect('configurations')
        
        else:
            error = form.errors.as_data()
            errors = [f'{list(error[x][0])[0]}' for x in error] 

            return render(request, 'configure-server.html', context={'errors': errors, 'email_type': email_type})


def configurations_view(request):

    cofigurations = EmailConfiguration.objects.filter(user__id=request.user.id)

    return render(request, 'configurations.html', context={'configurations': cofigurations})


@login_required
def delete_configuration_view(request, id):

    try:
        EmailConfiguration.objects.get(id=id, user=request.user).delete()
        return redirect('configurations')   
    
    except (EmailConfiguration.DoesNotExist):
        return render(request, '404.html')



# @csrf_exempt
@login_required_rest_api
@require_http_methods(['POST'])
@ratelimit(key='ip', rate='2/min', method=ratelimit.ALL, block=True)
def send_test_mail_view(request):

    # data = json.loads(request.body.decode("utf-8"))

    variables = request.POST.get('variables') or '{}'
    subject = request.POST.get('subject') or ''
    body = request.POST.get('body') or ''
    files = request.FILES.getlist("attachments")

    try:
        variables = json.loads(variables)
    
    except json.JSONDecodeError:
        return JsonResponse({'json': 'invalid variable structure'}, status=400)

    file_size = 0

    for f in files:
        file_size += get_file_size(f)

    if file_size > 10:
        return JsonResponse({'file': 'file attachments size greater than 10 MB'})

    variables['from_name'] = settings.EMAIL_FROM_NAME
    variables['from_signature'] = settings.EMAIL_FROM_SIGNATURE
    variables['from_email'] = settings.EMAIL_FROM

    try:
        
        template = jinja_env.from_string(subject)
        template.render(variables)
    
        template = jinja_env.from_string(body)
        template.render(variables)

    except jinja2.TemplateSyntaxError as e:
        return JsonResponse({'template': f'template syntax error {e}'}, status=400)
    
    try:
        send_email_with_attachments(subject, get_plain_text_from_html(body), body, variables, recipient_list=[request.user.email], attachments=files)

    except Exception as e:
        # print("exceptioin: ", e)
        return JsonResponse({'error': 'something went wrong'}, status=400)

    return JsonResponse({'success': 'the email has been sent'}, status=200)


@require_http_methods(['GET'])
@ratelimit(key='ip', rate='30/min', method=ratelimit.ALL, block=True)
def detailed_template_view(request, id):

    template = EmailTemplate.objects.filter(id=id)

    if not template.exists():
        return JsonResponse({'error': 'does not exist'}, status=404)

    if not template.filter(user=request.user.id).exists():

        if template.filter(public=False):
            return JsonResponse({'error': 'unauthorized'}, status=400)

    email_template = model_to_dict(template.last(), exclude=['copy_count', 'datetime', 'user'])
    
    email_template['edit_url'] = reverse('email-template-create') + f"?edit={id}"

    return JsonResponse(email_template, status=200)


@require_http_methods(['POST'])
def send_campaign_test_view(request):
    """
    Sends live test emails to at least two test email addresses
    using the chosen sender account and template.
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    from_email_id = data.get('from_email')
    template_id = data.get('template')
    test_emails = data.get('test_emails') or []
    
    if isinstance(test_emails, str):
        test_emails = [e.strip() for e in test_emails.replace('\n', ',').split(',') if e.strip()]

    # Validate that at least two valid emails are provided
    valid_test_emails = []
    for e in test_emails:
        cleaned = is_valid_mail(e.strip())
        if cleaned and cleaned not in valid_test_emails:
            valid_test_emails.append(cleaned)

    if len(valid_test_emails) < 2:
        return JsonResponse({
            'success': False, 
            'error': f'Please provide at least 2 valid email addresses to test the campaign (currently provided: {len(valid_test_emails)}).'
        }, status=400)

    if not from_email_id:
        return JsonResponse({'success': False, 'error': 'Please select a "Send From Account" in Step 3 first.'}, status=400)

    if not template_id:
        return JsonResponse({'success': False, 'error': 'Please select an "Email Template" in Step 3 first.'}, status=400)

    try:
        email_config = EmailConfiguration.objects.get(id=from_email_id, user=request.user)
    except EmailConfiguration.DoesNotExist:
        email_config = EmailConfiguration.objects.filter(id=from_email_id).first()
        if not email_config:
            return JsonResponse({'success': False, 'error': 'Selected sender account not found.'}, status=404)

    try:
        template = EmailTemplate.objects.get(id=template_id)
    except EmailTemplate.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Selected email template not found.'}, status=404)

    smtp_settings = {
        'host': email_config.host,
        'port': email_config.port,
        'use_ssl': True if email_config.port == 465 else False,
        'use_tls': True if email_config.port == 587 else False,
        'username': email_config.email,
        'password': email_config.password,
    }

    attachments = []
    attachment_names = EmailTemplateAttachment.objects.filter(template=template).values_list('attachment', flat=True)
    for attachment_name in attachment_names:
        try:
            att = default_storage.open(attachment_name)
            attachments.append(att)
        except Exception:
            pass

    subject = template.subject or 'Test Campaign Email'
    body = template.body or ''
    plain_body = get_plain_text_from_html(body)

    sent_emails = []
    failed_emails = []

    try:
        connection = EmailBackend(fail_silently=False, timeout=30.0, **smtp_settings)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Could not connect to SMTP server: {str(e)}'}, status=500)

    for email_addr in valid_test_emails:
        html_context = {
            'from_name': email_config.name or email_config.email,
            'from_email': email_config.email,
            'from_signature': email_config.signature or '',
            'email': email_addr,
            'Email': email_addr,
            'name': email_addr.split('@')[0].replace('.', ' ').title(),
            'Name': email_addr.split('@')[0].replace('.', ' ').title(),
            'company': 'Demo Company Inc.',
            'Company': 'Demo Company Inc.',
        }
        try:
            send_email_with_attachments(
                subject=subject,
                text_message=plain_body,
                html_message=body,
                html_context=html_context,
                from_email=email_config.email,
                recipient_list=[email_addr],
                attachments=attachments,
                connection=connection
            )
            sent_emails.append(email_addr)
        except Exception as e:
            failed_emails.append(f"{email_addr}: {str(e)}")

    if not sent_emails:
        return JsonResponse({
            'success': False, 
            'error': f'Failed to send to all test recipients: {"; ".join(failed_emails)}'
        }, status=500)

    result_msg = f"Live test emails successfully sent to {', '.join(sent_emails)}!"
    if failed_emails:
        result_msg += f" (Failed for: {', '.join(failed_emails)})"

    return JsonResponse({
        'success': True,
        'message': result_msg,
        'sent_emails': sent_emails
    })