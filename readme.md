# Email Campaign Studio 🚀

An open-source, non-tech friendly email automation and cold outreach tool built by **[@techsavvymohan](https://github.com/techsavvymohan)**. Schedule, personalize, test, and send cold email campaigns with automated follow-ups!

[![Developed by @techsavvymohan](https://img.shields.io/badge/Developer-%40techsavvymohan-black?style=for-the-badge&logo=github)](https://github.com/techsavvymohan)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/techsavvymohan)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.0+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Windows](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)

---

> *"Not to be dramatic, but this might save you 10 hours this week."*  
> Effortless cold email campaigns with automated follow-ups, built for creators, founders, and marketers.

---

## ⚡ Installation & Quick Start (Windows)

Choose any of the 3 easy methods below to run the bot on your computer:

---

### Method 1: 1-Click Launch (Easiest) 🖱️

Just **double-click [`run.bat`](run.bat)** in the project folder!  
It automatically:
1. Creates the `venv` virtual environment if not already present.
2. Installs all required packages from `requirements.txt`.
3. Applies database migrations.
4. Boots the server at **`http://127.0.0.1:8080/`**.

---

### Method 2: Single Command (One-Liner) ⚡

Open **Command Prompt (CMD)** or **PowerShell** inside the project directory and run this single command:

```cmd
python -m venv venv && .\venv\Scripts\activate && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver 127.0.0.1:8080
```

---

### Method 3: Step-by-Step Commands 📋

If you prefer executing each step manually, run these commands in Command Prompt or PowerShell:

#### Step 1: Clone the Repository
```cmd
git clone https://github.com/techsavvymohan/Email_Campaign_Bot.git
cd Email_Campaign_Bot
```

#### Step 2: Create a Virtual Environment
```cmd
python -m venv venv
```

#### Step 3: Activate the Virtual Environment
```cmd
.\venv\Scripts\activate
```

#### Step 4: Upgrade Pip & Install Dependencies
```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 5: Apply Database Migrations
```cmd
python manage.py migrate
```

#### Step 6: Start the Application Server
```cmd
python manage.py runserver 127.0.0.1:8080
```

#### Step 7: Access the Dashboard
Open your browser and navigate to:  
👉 **[http://127.0.0.1:8080/](http://127.0.0.1:8080/)**  
*(Auto-login is enabled — no signup, login forms, or passwords required!)*

---

## ✨ Key Features

- **⚡ Zero-Config Gmail (SMTP) Connection:** Connect your `@gmail.com` address in 1 minute using a 16-character Google App Password. No complex host or port settings required.
- **💼 Professional Work Email (SMTP):** Connect any custom domain email (`you@company.com`) using standard SMTP and IMAP settings.
- **🧪 Test Campaign on 2+ Emails:** Live test your campaign on at least two email addresses before launching to verify spam deliverability, formatting, and personalization tags.
- **⏰ Native IST (Indian Standard Time) Scheduling:** Accurate scheduling in `Asia/Kolkata` (IST) with automated background execution via Celery & Celery Beat.
- **🎨 Dynamic Email Templates:** Create rich templates with Jinja2 personalization variables (`{{name}}`, `{{company}}`, `{{from_signature}}`) and conditional logic (`{% if ... %}`).
- **🔄 Smart Automated Follow-ups:** Automatically schedule follow-up emails based on whether the recipient responded or not (via IMAP reply detection).
- **📊 Spreadsheet Recipient Import:** Upload your audience list directly via Excel (`.xlsx`, `.xls`) or CSV (`.csv`) with automatic duplicate detection.
- **🛡️ Built-in Privacy & Encryption:** Sender passwords and mailbox credentials are fully encrypted at rest using AES cryptography (`django-encrypted-model-fields`).

---

## 🛠️ How It Works

```
┌───────────────────────────┐      ┌───────────────────────────┐      ┌───────────────────────────┐
│ 1. Connect Email (SMTP)   │ ───► │ 2. Create Email Template  │ ───► │ 3. Test & Launch Campaign │
│ Gmail or Work Domain      │      │ Dynamic Jinja2 Variables  │      │ Test on 2 Mails & Send    │
└───────────────────────────┘      └───────────────────────────┘      └───────────────────────────┘
```

1. **Connect Sender Email:** Choose **Gmail (SMTP)** or **Professional Email (SMTP)** from your dashboard.
2. **Create Template:** Compose your message using variables like `{{name}}` and `{{company}}`.
3. **Upload Recipients:** Upload a CSV/Excel file with your contact list.
4. **Test Campaign:** Send a live test to at least 2 email addresses to inspect live delivery and formatting.
5. **Schedule & Send:** Choose your send date & time in IST, set follow-up rules, and launch!

---

## 📝 Example Template

### Subject:
```
Quick question regarding {{company}}
```

### Body:
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

### Rendered Output:
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

---

## 👨‍💻 Developer & Maintainer

Developed and maintained with ❤️ by **[@techsavvymohan](https://github.com/techsavvymohan)**.

- **GitHub:** [@techsavvymohan](https://github.com/techsavvymohan)
- **LinkedIn:** [Mohan Singh (@techsavvymohan)](https://www.linkedin.com/in/techsavvymohan)
- **Repository:** [https://github.com/techsavvymohan/Email_Campaign_Bot](https://github.com/techsavvymohan/Email_Campaign_Bot)

---

## 📄 License & Disclaimer

This project is licensed under the MIT License.

> **Disclaimer:** This tool is designed for legitimate business inquiries, outreach, and automated communications. Please comply with CAN-SPAM, GDPR, and email deliverability guidelines. Do not send unsolicited spam.
