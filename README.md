# Bright Edu Consultancy - Educational Consultancy & Student Application Tracking System

A modern, responsive, and secure web application built with **Django 4.2+** and **Tailwind CSS** for **Bright Edu Consultancy**, specializing in higher education in China, Chinese Government Scholarships (CSC), and international university admissions.

---

## 🌟 Key Features

### 1. Main Public Pages
* **Home Page**: Modern hero section with dynamic statistics counter, quick university/program finder widget, value propositions, featured Chinese universities (Tsinghua, Peking, Zhejiang, Fudan, etc.), popular degree offerings, 7-step admissions stepper, student reviews, and direct call-to-actions.
* **About Us**: Consultancy pedigree, mission, vision, core pillars (Integrity, Real-time Tracking, Ground Presence in Shanghai & Dhaka), and leadership information.
* **Services**: Comprehensive breakdown of 6 core consultancy services:
  1. Free Profile Evaluation & Academic Counseling
  2. University & Major Selection (English & Chinese medium)
  3. CSC & Provincial Government Scholarship Assistance
  4. Statement of Purpose (SOP) & Study Plan Drafting
  5. JW202 / DQ Visa Application & Embassy Preparation
  6. Pre-Departure Orientation, Air Ticketing, Airport Reception in China & Dormitory Setup.
* **Study in China (Dedicated Guide)**:
  - In-depth guide to studying in China.
  - CSC Scholarships (Type A & Type B) coverage: 100% Tuition Waiver, Free Campus Accommodation, Comprehensive Medical Insurance, and Monthly Living Allowances (2,500 - 3,500 RMB).
  - Provincial & University Presidential Grants.
  - Document checklist for international students.
  - China study FAQs and direct apply links.
* **Universities & Programs Database**:
  - Searchable and filterable by Degree Level (Bachelor, Master, PhD, Language), Discipline/Major (Medicine/MBBS, Computer Science & AI, Engineering, Business), City, and Scholarship eligibility.
  - Detailed university profile pages with national rank, campus highlights, available programs, and direct "Apply with this University" button.
  - Program detail pages with curriculum overview, tuition fee in CNY, intake terms, requirements, and scholarship linkages.
* **Student Success / Testimonials**:
  - Filterable reviews by degree level (Bachelor, Master, PhD, Language).
  - Quotes, admitted university, scholarship type, home country, and rating.
* **Contact Us**:
  - Interactive contact inquiry form with database storage and email notifications.
  - Office locations in Dhaka and Shanghai.
  - Direct WhatsApp chat integration.
  - Interactive WeChat QR code popup modal with one-click WeChat ID clipboard copy.

---

### 2. Apply Now / Student Portal & Tracking System
* **Student Registration & Authentication**: Clean sign-up and log-in system supporting email-based authentication.
* **Unique Application ID**: Automatically generates a unique, human-readable identifier (e.g. `BEC-2026-89201`).
* **Online Application Form**:
  - Multi-section form capturing study preferences, target degree, preferred university/major, and academic background.
  - Integrated initial document uploads (Passport bio page, Photo, Degree Certificate, Transcript, CV, Study Plan).
* **Interactive Student Dashboard**:
  - Live 7-Stage Status Stepper:
    1. **Submitted**: Dossier received.
    2. **Document Checking**: Counselors verifying notarizations & compliance.
    3. **Applied**: Formally lodged in Chinese university admissions portal.
    4. **Under Review**: University faculty and scholarship committee evaluation.
    5. **Admission**: Admission letter and JW201/JW202/DQ visa notice issued.
    6. **Visa**: Chinese Embassy visa submission in progress.
    7. **Completed**: Visa granted, student ready for departure!
  - Progress percentage meter and visual node highlights.
  - Public status note explaining current progress.
  - **Action Required / Re-upload Alert**: Prominent alert banner if counselor flags an illegible or missing document.
  - Milestone history audit log.
* **Document Management Center**:
  - View all uploaded files, upload dates, file types, and status (`Pending Verification`, `Verified & Approved`, `Action Required / Re-upload Requested`).
  - Allows students to upload additional documents or replace flagged documents.
* **Application Dossier View**: Clean, printable summary (`window.print()` formatted) of student application details.

---

### 3. Counselor & Admin Management Panel
* Dedicated staff portal (`/portal/staff/`):
  - Overview metrics: Total applications, count per stage (1 to 7), and count of files needing document correction.
  - Search applications by student name, Application ID, email, or passport.
  - Filter by stage.
* **Student Dossier Management (`/portal/staff/application/<app_id>/`)**:
  - One-click file inspection and download.
  - Fast inline document verification ("✓ Approve / Verify").
  - Fast inline "Request Re-upload" with specific counselor instruction message sent directly to student portal.
  - Status updater: Update status across all 7 stages with public note and timeline audit log.
  - Private internal notes for staff eyes only.
* **Standard Django Admin (`/admin/`)**:
  - Fully registered models with search, filters, and tabular inlines for universities, programs, scholarships, contact inquiries, testimonials, and student files.

---

### 4. Communication & Integrations
* **WhatsApp**: Floating button and click-to-chat links with pre-filled inquiry text.
* **WeChat**: Interactive modal with custom QR code SVG, counselor WeChat ID, and one-click copy button.
* **Email Notifications**: Integrated with Django email framework for application confirmations and status change alerts (uses console backend by default in development).
* **Security & Best Practices**:
  - CSRF protection on all forms.
  - Secure file validation and upload storage.
  - Role-based permissions separating regular students from consultancy staff.

---

## 🚀 Quick Start Guide

### Option 1: One-Click Launch (Windows)
Double click `run_project.bat` or run:
```bat
run_project.bat
```

### Option 2: PowerShell
Run:
```powershell
.\setup.ps1
```

### Option 3: Manual Command Line Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations**:
   ```bash
   python manage.py makemigrations core universities portal
   python manage.py migrate
   ```

3. **Populate initial data (Universities, Programs, Demo Accounts)**:
   ```bash
   python manage.py seed_data
   ```

4. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

5. Open your web browser and navigate to:
   - **Website & Portal**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - **Counselor Panel**: [http://127.0.0.1:8000/portal/staff/](http://127.0.0.1:8000/portal/staff/)
   - **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🔑 Demo Login Accounts

| Role | Username / Email | Password | Access URL |
| :--- | :--- | :--- | :--- |
| **Superuser / Admin** | `admin` | `admin123` | `/admin/` or `/portal/staff/` |
| **Counselor Staff** | `counselor` | `counselor123` | `/portal/staff/` |
| **Demo Student** | `student@brightedu.com` | `student123` | `/portal/dashboard/` |

---

## 📁 Project Architecture

```
F:\BRIGHT\
├── manage.py                     # Django administrative entrypoint
├── requirements.txt              # Project dependencies (Django, Pillow, python-dotenv)
├── run_project.bat               # Windows one-click launcher
├── setup.ps1                     # PowerShell automation script
├── bright_edu/
│   ├── settings.py               # Django configuration, templates, media, static
│   ├── urls.py                   # Central URL dispatching
│   ├── wsgi.py                   # WSGI deployment configuration
│   └── asgi.py                   # ASGI deployment configuration
├── core/                         # Public marketing pages & inquiries
│   ├── models.py                 # ContactMessage, Testimonial, FAQ, NewsletterSubscriber
│   ├── views.py                  # Home, About, Services, Study in China, Contact, etc.
│   ├── forms.py                  # ContactForm, NewsletterForm
│   ├── context_processors.py     # Global consultancy settings & branding
│   └── urls.py
├── universities/                 # Academic catalog & search
│   ├── models.py                 # University, Program, Scholarship
│   ├── views.py                  # University & Program listings, filters & details
│   └── urls.py
├── portal/                       # Student admissions & counselor management
│   ├── models.py                 # StudentProfile, StudentApplication, ApplicationDocument, Timeline
│   ├── views.py                  # Register, Login, Apply, Dashboard, Documents, Staff Dashboard
│   ├── forms.py                  # StudentRegisterForm, OnlineApplicationForm, AdminStatusUpdateForm
│   ├── management/commands/
│   │   └── seed_data.py          # Database population script
│   └── urls.py
├── templates/                    # Responsive HTML templates with Tailwind CSS & FontAwesome
│   ├── base.html                 # Master layout with SEO meta & schema.org
│   ├── includes/                 # Reusable components: navbar, footer, floating contact, alerts
│   ├── core/                     # Public page templates
│   ├── universities/             # University and Program catalog templates
│   └── portal/                   # Student & Counselor portal templates
├── static/
│   ├── css/custom.css            # Custom typography, animations & glassmorphism
│   ├── js/main.js                # Mobile navigation, WeChat QR modal, copy ID
│   └── images/                   # SVG brand logo, WeChat QR code, illustrations
└── media/                        # User uploaded student documents and avatars
```

---

## 🛡️ License & Standards
Developed for **Bright Edu Consultancy**. Fully customizable for international student recruitment agencies and academic consultancies.
