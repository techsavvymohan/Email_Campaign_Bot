import jwt
import json

from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods

from .models import User
from .forms import CustomUserCreationForm
from utils.token_generator import send_token

def login_view(request):
    return redirect('home')


def logout_view(request):
    return redirect('home')

@require_http_methods(["GET", "POST"])
def signup_view(request):
    return redirect('home')


def verification_alert(request):
    """
        alert that the user has to verify their email
    """
    email = request.GET.get('email') or ''
    return render(request, 'verification-alert.html', context={'from_email': settings.EMAIL_HOST,
                                                                'to_email': email   
                                                            })


@require_http_methods(["GET", "POST"])
def verification_resend(request):
    """
        resend the confirmation email
    """

    if request.method == "POST":

        email = request.POST.get('email')

        user = User.objects.filter(email=email)

        if not user.exists():

            return render(request, 'resend-confirmation.html', {'error': f'The email {email} is not registered'})

        if user.filter(is_active=True):
            return render(request, 'resend-confirmation.html', {'error': f'The email {email} is already active'})

        send_token(email)
        url = reverse('verification-alert') + f'?email={email}'
        return redirect(url)

    return render(request, 'resend-confirmation.html')


def verify_email(request):
    token = request.GET.get('token')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        email = payload['email']

        user = get_user_model().objects.get(email=email)
        user.is_active = True
        user.save()

        send_token(email)

        return redirect('login')  # Redirect to a success page

    except jwt.ExpiredSignatureError:
        return render(request, 'email-verification.html', context={'error': 'Token expired, request another'})

    except (jwt.DecodeError, Exception):
        return render(request, 'email-verification.html', context={'error': 'Unknown error occurred, request a new token'})