<div align="center">

# 🚀 Email Campaign Studio & Bot
### *The #1 Open-Source Cold Email Campaign, Outreach Automation & Follow-Up Engine*

<p align="center">
  <b>Launch unlimited cold email campaigns with automated multi-stage follow-ups, zero-config Gmail SMTP, live deliverability testing, and dynamic Jinja2 personalization — 100% Free & Self-Hosted.</b>
</p>

[![Developer](https://img.shields.io/badge/Developer-%40techsavvymohan-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/techsavvymohan)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/techsavvymohan)
[![Stars](https://img.shields.io/github/stars/techsavvymohan/Email_Campaign_Bot?style=for-the-badge&color=ffd700&label=%E2%AD%90%20Stars)](https://github.com/techsavvymohan/Email_Campaign_Bot/stargazers)
[![Forks](https://img.shields.io/github/forks/techsavvymohan/Email_Campaign_Bot?style=for-the-badge&color=blue&label=%F0%9F%94%80%20Forks)](https://github.com/techsavvymohan/Email_Campaign_Bot/network/members)
[![Issues](https://img.shields.io/github/issues/techsavvymohan/Email_Campaign_Bot?style=for-the-badge&color=success&label=%E2%9C%94%EF%B8%8F%20Issues)](https://github.com/techsavvymohan/Email_Campaign_Bot/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](License.txt)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django 4.0+](https://img.shields.io/badge/Django-4.0+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Windows Compatible](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)

<br/>

[**⚡ Quick Start (1-Click)**](#-quick-start-windows) •
[**✨ Key Features**](#-key-features) •
[**📊 Comparison with Paid Tools**](#-why-choose-email-campaign-studio-vs-paid-tools) •
[**🛠️ How It Works**](#%EF%B8%8F-how-an-email-campaign-works) •
[**🧪 Live Campaign Testing**](#-live-campaign-testing-on-2-emails) •
[**👨‍💻 Developer**](#-developer--maintainer)

<br/>

---

> 💡 **Why pay $50–$100/month for Instantly or Lemlist?**  
> **Email Campaign Studio** gives you complete control over your cold email campaigns, sender accounts, contact lists, and scheduled follow-ups with zero monthly subscription fees and 100% data privacy.

---

</div>

<br/>

## ⚡ Quick Start (Windows)

Choose either of the two easy ways below to launch your email campaign bot in seconds:

### Method 1: 1-Click Launch (Easiest) 🖱️

Just **double-click [`run.bat`](run.bat)** in the project directory!  
It automatically:
1. Creates the `venv` virtual environment if not already present.
2. Installs all required dependencies from `requirements.txt`.
3. Applies database migrations.
4. Starts the email campaign dashboard at **`http://127.0.0.1:8080/`**.

---

### Method 2: Single Command (One-Liner) ⚡

Open **Command Prompt (CMD)** or **PowerShell** in the project folder and paste:

```cmd
python -m venv venv && .\venv\Scripts\activate && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver 127.0.0.1:8080
```

---

### Method 3: Step-by-Step Installation 📋

```cmd
# 1. Clone the Email Campaign Bot repository
git clone https://github.com/techsavvymohan/Email_Campaign_Bot.git
cd Email_Campaign_Bot

# 2. Create and activate Python virtual environment
python -m venv venv
.\venv\Scripts\activate

# 3. Upgrade pip and install all campaign dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Start the Email Campaign application
python manage.py runserver 127.0.0.1:8080
```

🌐 **Access the App:** Open **[http://127.0.0.1:8080/](http://127.0.0.1:8080/)** in your browser.  
*(Local auto-login is active — no passwords or signup required!)*

<br/>

---

## 📊 Why Choose Email Campaign Studio vs. Paid Tools?

| Feature | **Email Campaign Studio** 🚀 | **Instantly.ai** 💸 | **Lemlist** 💸 | **Mailchimp** 💸 |
| :--- | :---: | :---: | :---: | :---: |
| **Monthly Cost** | **$0 / Free Forever** | $37 - $97 / mo | $59 - $99 / mo | $20 - $350 / mo |
| **Email Campaign Volume** | **Unlimited** | Tier Restricted | Tier Restricted | Tier Restricted |
| **Connected Sender Accounts** | **Unlimited** | Limited by Plan | Limited by Plan | 1 Domain |
| **Live 2-Email Pre-Send Testing** | **Built-in & Free** | Limited | Add-on | Extra Fee |
| **Data Privacy & Storage** | **100% Local / Self-Hosted** | Stored on 3rd Party | Stored on 3rd Party | Stored on 3rd Party |
| **Credential Encryption** | **AES-256 at Rest** | Proprietary | Proprietary | Proprietary |
| **Automated Follow-ups** | **Yes (Smart Reply Detection)** | Yes | Yes | Limited |
| **Spreadsheet Upload (CSV/XLSX)** | **Unlimited Contacts** | Capped | Capped | Capped |

<br/>

---

## ✨ Key Features for High-Converting Email Campaigns

- **⚡ Zero-Config Gmail (SMTP) Connection:** Connect any `@gmail.com` address in under 60 seconds with a 16-character Google App Password. No complex ports, SSL/TLS toggles, or server hostnames needed.
- **💼 Professional Custom Domain Email (SMTP/IMAP):** Connect unlimited business emails (`you@company.com`) through standard SMTP and IMAP protocols.
- **🧪 Live Email Campaign Testing (2+ Recipients):** Test email formatting, dynamic personalization tags, and spam score across 2 test inboxes before launching to your full contact list.
- **⏰ Native IST (Indian Standard Time) Scheduling:** Accurate time picker configured for `Asia/Kolkata` (IST) with background Celery & Celery Beat scheduling.
- **🎨 Dynamic Jinja2 Email Templates:** Personalize every email with variables (`{{name}}`, `{{company}}`, `{{from_signature}}`) and conditional logic (`{% if role %}...{% endif %}`).
- **🔄 Smart Automated Follow-up Sequences:** Automatically send follow-ups based on recipient actions (e.g., send follow-up only if no reply was received within 3 days).
- **📊 Spreadsheet Audience Import:** Import thousands of leads instantly using `.xlsx`, `.xls`, or `.csv` files with automatic duplicate email detection.
- **🛡️ AES Credential Encryption:** Passwords and SMTP credentials are encrypted at rest using industry-standard cryptography (`django-encrypted-model-fields`).

<br/>

---

## 🛠️ How an Email Campaign Works

```
┌───────────────────────────┐      ┌───────────────────────────┐      ┌───────────────────────────┐
│ 1. Connect Email (SMTP)   │ ───► │ 2. Build Campaign Content │ ───► │ 3. Test & Launch Campaign │
│ Gmail or Work Domain      │      │ Jinja2 Dynamic Variables  │      │ Live Test on 2 Mails      │
└───────────────────────────┘      └───────────────────────────┘      └───────────────────────────┘
```

1. **Connect Sender Email:** Add your Gmail or professional custom domain mailbox via the dashboard.
2. **Draft Email Template:** Write high-converting copy with dynamic tags (`{{name}}`, `{{company}}`).
3. **Upload Leads:** Import your target audience spreadsheet.
4. **Test Before Launch:** Send a live preview test to at least 2 test email addresses.
5. **Schedule & Send:** Choose your launch time in IST and let the automation handle delivery and follow-ups.

<br/>

---

## 🧪 Live Campaign Testing (on 2+ Emails)

Never send an email campaign with broken tags or bad formatting again!

Before launching any campaign, you can enter **two test email addresses** directly in the campaign builder. The bot will:
1. Render your Jinja2 template with sample lead data.
2. Deliver the rendered email live to both test inboxes via your connected SMTP server.
3. Allow you to verify deliverability, mobile layout, subject line display, and unsubscribe tags in real-time.

<br/>

---

## 📝 Example High-Converting Cold Email Template

### Subject Line:
```
Quick question regarding {{company}}
```

### Template Body:
```html
Hello {{name}},

Hope you are having a productive week! I am {{from_name}} reaching out to explore potential collaboration opportunities with {{company}}.

{% if role %}
I noticed your impressive work as {{role}} and wanted to share how our platform can help you scale your outreach.
{% else %}
I wanted to share how our platform can help your team scale cold outreach effortlessly.
{% endif %}

Looking forward to connecting!

{{from_signature}}
```

### Live Rendered Output:
> **Hello Alex,**  
>  
> Hope you are having a productive week! I am Mohan reaching out to explore potential collaboration opportunities with Acme Corp.  
>  
> I noticed your impressive work as Head of Growth and wanted to share how our platform can help you scale your outreach.  
>  
> Looking forward to connecting!  
>  
> *Best regards,*  
> **Mohan Singh**  
> *Founder & Developer*

<br/>

---

## 🔍 Recommended GitHub Topics (SEO Tags)

To maximize discoverability and help users find this project on GitHub and Google, add these topics in your GitHub repository settings:

```
email-campaign, cold-email, email-automation, email-campaign-bot, cold-outreach, 
email-marketing, gmail-smtp, email-sequencer, cold-email-software, email-deliverability, 
drip-campaign, mail-merge, django-email, lead-generation, outreach-tool
```

<br/>

---

## 👨‍💻 Developer & Maintainer

Developed and maintained with ❤️ by **[@techsavvymohan](https://github.com/techsavvymohan)**.

* **GitHub:** [@techsavvymohan](https://github.com/techsavvymohan)
* **LinkedIn:** [Mohan Singh (@techsavvymohan)](https://www.linkedin.com/in/techsavvymohan)
* **Repository:** [https://github.com/techsavvymohan/Email_Campaign_Bot](https://github.com/techsavvymohan/Email_Campaign_Bot)

⭐ **If you find this project helpful, please give it a star on GitHub!** It helps more creators and founders discover open-source email outreach tools.

<br/>

---

## 📄 License & Disclaimer

This project is licensed under the **MIT License**.

> **Disclaimer:** This software is intended for legitimate business inquiries, client outreach, and authorized transactional communications. Please respect CAN-SPAM, GDPR, and anti-spam regulations. Always include an opt-out mechanism and maintain sender reputation.
