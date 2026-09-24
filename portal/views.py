from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q, Count
from django.utils import timezone

from .models import (
    StudentProfile,
    StudentApplication,
    ApplicationDocument,
    ApplicationTimeline
)
from .forms import (
    StudentRegisterForm,
    StudentLoginForm,
    OnlineApplicationForm,
    DocumentUploadForm,
    ReplaceDocumentForm,
    AdminStatusUpdateForm,
    AdminDocumentReviewForm
)
from universities.models import University, Program


def register_view(request):
    """Student registration view."""
    if request.user.is_authenticated:
        return redirect('portal:dashboard')

    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            nationality = form.cleaned_data['nationality']

            # Use email as username
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create Student Profile
            StudentProfile.objects.create(
                user=user,
                phone=phone,
                nationality=nationality
            )

            # Auto login
            login(request, user)

            messages.success(request, f"Welcome to Bright Edu Consultancy, {first_name}! Your account has been created. Please complete your application.")
            return redirect('portal:apply')
    else:
        form = StudentRegisterForm()

    return render(request, 'portal/register.html', {'form': form})


def login_view(request):
    """Student and staff login view."""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('portal:staff_dashboard')
        return redirect('portal:dashboard')

    if request.method == 'POST':
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            
            # Direct staff to staff portal, students to student dashboard
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            if user.is_staff:
                return redirect('portal:staff_dashboard')
            return redirect('portal:dashboard')
        else:
            messages.error(request, "Invalid email/username or password. Please try again.")
    else:
        form = StudentLoginForm()

    return render(request, 'portal/login.html', {'form': form})


def logout_view(request):
    """Log out user."""
    logout(request)
    messages.info(request, "You have been securely logged out.")
    return redirect('core:home')


@login_required
def dashboard(request):
    """Student main portal dashboard with visual 7-step tracker and alerts."""
    if request.user.is_staff:
        # If staff lands here, give them quick switch option or redirect
        pass

    applications = StudentApplication.objects.filter(student=request.user).order_by('-created_at')
    current_application = applications.first()

    documents = []
    timeline = []
    if current_application:
        documents = current_application.documents.all()
        timeline = current_application.timeline.all()[:10]

    context = {
        'applications': applications,
        'app': current_application,
        'documents': documents,
        'timeline': timeline,
        'statuses': StudentApplication.ORDERED_STATUSES,
    }
    return render(request, 'portal/dashboard.html', context)


@login_required
def apply_view(request):
    """Online application form with initial document upload and unique ID generation."""
    # Check if student already has an active application
    existing_app = StudentApplication.objects.filter(student=request.user).first()
    
    # Pre-select university or program if passed in query string
    initial_data = {}
    uni_id = request.GET.get('university')
    prog_id = request.GET.get('program')
    if uni_id:
        try:
            initial_data['preferred_university'] = University.objects.get(id=uni_id)
        except University.DoesNotExist:
            pass
    if prog_id:
        try:
            prog = Program.objects.get(id=prog_id)
            initial_data['preferred_program'] = prog
            initial_data['preferred_university'] = prog.university
            initial_data['target_degree'] = prog.degree_level
        except Program.DoesNotExist:
            pass

    if request.method == 'POST':
        form = OnlineApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.status = 'Submitted'
            application.status_note = 'Application dossier received. Our senior counselor will begin document verification within 24 hours.'
            application.save()

            # Create initial timeline log
            ApplicationTimeline.objects.create(
                application=application,
                status='Submitted',
                title='Application Submitted Successfully',
                note=f'Student submitted initial dossier for {application.target_degree} ({application.display_program}) at {application.display_university}. Unique ID: {application.application_id}',
                performed_by=request.user
            )

            # Process attached initial files
            file_mappings = [
                ('passport_file', 'passport', 'Passport Bio Page'),
                ('photo_file', 'photo', 'Recent Passport-size Photo'),
                ('certificate_file', 'certificate', 'Highest Degree Certificate'),
                ('transcript_file', 'transcript', 'Official Academic Transcript'),
                ('cv_file', 'cv', 'Curriculum Vitae (CV)'),
                ('study_plan_file', 'study_plan', 'Study Plan / SOP'),
            ]

            for file_field, doc_type, doc_title in file_mappings:
                uploaded_file = request.FILES.get(file_field)
                if uploaded_file:
                    ApplicationDocument.objects.create(
                        application=application,
                        doc_type=doc_type,
                        title=doc_title,
                        file=uploaded_file,
                        status='pending'
                    )

            # Send confirmation email
            try:
                subject = f"Application Received: {application.application_id} - Bright Edu Consultancy"
                body = (
                    f"Dear {request.user.first_name},\n\n"
                    f"Thank you for submitting your study abroad application with Bright Edu Consultancy.\n"
                    f"Your Unique Application ID is: {application.application_id}\n\n"
                    f"Target Program: {application.display_program}\n"
                    f"Target University: {application.display_university}\n"
                    f"Status: Submitted (Stage 1 of 7)\n\n"
                    f"You can log into your Student Portal at any time to monitor your real-time application progress and manage your documents.\n\n"
                    f"Warm regards,\nBright Edu Consultancy Team"
                )
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                    fail_silently=True
                )
            except Exception:
                pass

            messages.success(
                request,
                f"Congratulations! Your application has been submitted successfully with Unique Application ID: {application.application_id}"
            )
            return redirect('portal:dashboard')
        else:
            messages.error(request, "Please review the form errors below.")
    else:
        form = OnlineApplicationForm(initial=initial_data)

    return render(request, 'portal/apply.html', {
        'form': form,
        'existing_app': existing_app,
    })


@login_required
def application_detail(request, app_id):
    """Detailed view of a student's application dossier and documents."""
    if request.user.is_staff:
        application = get_object_or_404(StudentApplication, application_id=app_id)
    else:
        application = get_object_or_404(StudentApplication, application_id=app_id, student=request.user)

    documents = application.documents.all()
    timeline = application.timeline.all()

    return render(request, 'portal/application_detail.html', {
        'app': application,
        'documents': documents,
        'timeline': timeline,
        'statuses': StudentApplication.ORDERED_STATUSES,
    })


@login_required
def documents_view(request, app_id=None):
    """Document center: shows all uploaded documents, re-upload requests, and upload form."""
    if app_id:
        if request.user.is_staff:
            application = get_object_or_404(StudentApplication, application_id=app_id)
        else:
            application = get_object_or_404(StudentApplication, application_id=app_id, student=request.user)
    else:
        application = StudentApplication.objects.filter(student=request.user).first()
        if not application:
            messages.warning(request, "Please submit an application before managing documents.")
            return redirect('portal:apply')

    if request.method == 'POST':
        upload_form = DocumentUploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            doc = upload_form.save(commit=False)
            doc.application = application
            doc.status = 'pending'
            doc.save()

            # Timeline note
            ApplicationTimeline.objects.create(
                application=application,
                status=application.status,
                title=f"Document Uploaded: {doc.title}",
                note=f"Student uploaded new file for {doc.get_doc_type_display()}",
                performed_by=request.user
            )

            messages.success(request, f"Document '{doc.title}' has been uploaded successfully.")
            return redirect('portal:documents_app', app_id=application.application_id)
    else:
        upload_form = DocumentUploadForm()

    documents = application.documents.all()
    has_action_required = documents.filter(status='action_required').exists()

    return render(request, 'portal/documents.html', {
        'app': application,
        'documents': documents,
        'upload_form': upload_form,
        'has_action_required': has_action_required,
    })


@login_required
def replace_document(request, doc_id):
    """Replace an existing document when re-upload is requested by counselors."""
    doc = get_object_or_404(ApplicationDocument, id=doc_id)
    
    # Permission check: must be owner or staff
    if not request.user.is_staff and doc.application.student != request.user:
        messages.error(request, "Access denied.")
        return redirect('portal:dashboard')

    if request.method == 'POST':
        form = ReplaceDocumentForm(request.POST, request.FILES, instance=doc)
        if form.is_valid():
            updated_doc = form.save(commit=False)
            updated_doc.status = 'pending'
            updated_doc.counselor_feedback = ''
            updated_doc.save()

            # Log to timeline
            ApplicationTimeline.objects.create(
                application=doc.application,
                status=doc.application.status,
                title=f"Document Re-uploaded: {doc.title}",
                note=f"Updated document file uploaded for verification.",
                performed_by=request.user
            )

            # Check if all re-upload requests for this application are now resolved
            remaining_action = doc.application.documents.filter(status='action_required').count()
            if remaining_action == 0:
                doc.application.has_missing_documents = False
                doc.application.missing_documents_note = ''
                doc.application.save()

            messages.success(request, f"New version of '{doc.title}' has been uploaded and queued for review.")
            return redirect('portal:documents_app', app_id=doc.application.application_id)
    else:
        form = ReplaceDocumentForm(instance=doc)

    return render(request, 'portal/replace_document.html', {
        'doc': doc,
        'form': form,
        'app': doc.application,
    })


# ---------------- STAFF & COUNSELOR ADMIN VIEWS ---------------- #

def is_staff_user(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_staff_user)
def staff_dashboard(request):
    """Consultancy management dashboard for counselors to manage applications and documents."""
    status_filter = request.GET.get('status', '').strip()
    query = request.GET.get('q', '').strip()

    applications = StudentApplication.objects.select_related('student', 'preferred_university', 'preferred_program').all()

    if status_filter:
        applications = applications.filter(status=status_filter)

    if query:
        applications = applications.filter(
            Q(application_id__icontains=query) |
            Q(student__first_name__icontains=query) |
            Q(student__last_name__icontains=query) |
            Q(student__email__icontains=query) |
            Q(preferred_university_name__icontains=query)
        )

    # Metrics
    total_apps = StudentApplication.objects.count()
    submitted_count = StudentApplication.objects.filter(status='Submitted').count()
    doc_checking_count = StudentApplication.objects.filter(status='Document Checking').count()
    applied_count = StudentApplication.objects.filter(status='Applied').count()
    under_review_count = StudentApplication.objects.filter(status='Under Review').count()
    admission_count = StudentApplication.objects.filter(status='Admission').count()
    visa_count = StudentApplication.objects.filter(status='Visa').count()
    completed_count = StudentApplication.objects.filter(status='Completed').count()
    missing_docs_count = StudentApplication.objects.filter(has_missing_documents=True).count()

    context = {
        'applications': applications,
        'total_apps': total_apps,
        'submitted_count': submitted_count,
        'doc_checking_count': doc_checking_count,
        'applied_count': applied_count,
        'under_review_count': under_review_count,
        'admission_count': admission_count,
        'visa_count': visa_count,
        'completed_count': completed_count,
        'missing_docs_count': missing_docs_count,
        'status_choices': StudentApplication.ORDERED_STATUSES,
        'selected_status': status_filter,
        'selected_q': query,
    }
    return render(request, 'portal/staff_dashboard.html', context)


@login_required
@user_passes_test(is_staff_user)
def staff_application_detail(request, app_id):
    """Full counselor view to review documents, update status, and request document corrections."""
    application = get_object_or_404(StudentApplication, application_id=app_id)
    documents = application.documents.all()
    timeline = application.timeline.all()

    if request.method == 'POST':
        action = request.POST.get('action_type')

        if action == 'update_status':
            status_form = AdminStatusUpdateForm(request.POST, instance=application)
            if status_form.is_valid():
                old_status = application.status
                updated_app = status_form.save()
                new_status = updated_app.status
                note = status_form.cleaned_data.get('timeline_note') or f"Status changed from {old_status} to {new_status}"

                # Create timeline entry
                ApplicationTimeline.objects.create(
                    application=application,
                    status=new_status,
                    title=f"Status Updated: {new_status}",
                    note=note,
                    performed_by=request.user
                )

                # Send email notification to student about status change
                try:
                    subject = f"Application Status Update: {new_status} - {application.application_id}"
                    body = (
                        f"Dear {application.student.first_name},\n\n"
                        f"Your application (ID: {application.application_id}) status has been updated to:\n"
                        f"👉 {new_status}\n\n"
                        f"Counselor Note: {application.status_note}\n\n"
                        f"Log in to your student dashboard to review details:\n"
                        f"Bright Edu Consultancy Admissions Team"
                    )
                    send_mail(
                        subject,
                        body,
                        settings.DEFAULT_FROM_EMAIL,
                        [application.student.email],
                        fail_silently=True
                    )
                except Exception:
                    pass

                messages.success(request, f"Application status updated to '{new_status}' successfully.")
                return redirect('portal:staff_app_detail', app_id=app_id)

        elif action == 'request_document':
            # Fast action to flag missing or incorrect document
            doc_id = request.POST.get('document_id')
            counselor_feedback = request.POST.get('feedback', '').strip()
            
            if doc_id:
                target_doc = get_object_or_404(ApplicationDocument, id=doc_id, application=application)
                target_doc.status = 'action_required'
                target_doc.counselor_feedback = counselor_feedback or "Please re-upload a clear, original colored scan in PDF format."
                target_doc.save()

                application.has_missing_documents = True
                application.missing_documents_note = f"Action needed on {target_doc.title}: {target_doc.counselor_feedback}"
                application.save()

                ApplicationTimeline.objects.create(
                    application=application,
                    status=application.status,
                    title=f"Document Correction Requested: {target_doc.title}",
                    note=target_doc.counselor_feedback,
                    performed_by=request.user
                )

                messages.warning(request, f"Re-upload request sent to student for '{target_doc.title}'.")
                return redirect('portal:staff_app_detail', app_id=app_id)

        elif action == 'verify_document':
            doc_id = request.POST.get('document_id')
            if doc_id:
                target_doc = get_object_or_404(ApplicationDocument, id=doc_id, application=application)
                target_doc.status = 'verified'
                target_doc.counselor_feedback = 'Document verified and approved.'
                target_doc.save()

                ApplicationTimeline.objects.create(
                    application=application,
                    status=application.status,
                    title=f"Document Approved: {target_doc.title}",
                    note="Verified by counselor.",
                    performed_by=request.user
                )

                messages.success(request, f"'{target_doc.title}' marked as Verified & Approved.")
                return redirect('portal:staff_app_detail', app_id=app_id)

    status_form = AdminStatusUpdateForm(instance=application)

    return render(request, 'portal/staff_application_detail.html', {
        'app': application,
        'documents': documents,
        'timeline': timeline,
        'status_form': status_form,
        'statuses': StudentApplication.ORDERED_STATUSES,
    })
