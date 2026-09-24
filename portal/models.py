import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from universities.models import University, Program

def generate_application_id():
    """Generates unique application ID, e.g. BEC-2026-84920"""
    year = timezone.now().year
    digits = ''.join(random.choices(string.digits, k=5))
    return f"BEC-{year}-{digits}"


class StudentProfile(models.Model):
    """Extended profile information for registered students."""
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    phone = models.CharField(max_length=30, verbose_name="WhatsApp / Phone Number")
    nationality = models.CharField(max_length=100, default="Bangladesh")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='male')
    passport_number = models.CharField(max_length=50, blank=True, verbose_name="Passport Number")
    passport_expiry = models.DateField(null=True, blank=True, verbose_name="Passport Expiry Date")
    current_address = models.TextField(blank=True, verbose_name="Present Address")
    emergency_contact = models.CharField(max_length=100, blank=True, verbose_name="Emergency Contact Person & Phone")
    avatar = models.ImageField(upload_to='student_avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.phone})"


class StudentApplication(models.Model):
    """The central student application for university admission and scholarship."""
    
    # Required 7 Stages from Prompt:
    # 1. Submitted -> 2. Document Checking -> 3. Applied -> 4. Under Review -> 5. Admission -> 6. Visa -> 7. Completed
    STATUS_CHOICES = [
        ('Submitted', '1. Submitted'),
        ('Document Checking', '2. Document Checking'),
        ('Applied', '3. Applied to University'),
        ('Under Review', '4. Under Review'),
        ('Admission', '5. Admission / JW202 Issued'),
        ('Visa', '6. Visa In Progress'),
        ('Completed', '7. Completed / Ready for Departure'),
    ]

    ORDERED_STATUSES = [
        'Submitted',
        'Document Checking',
        'Applied',
        'Under Review',
        'Admission',
        'Visa',
        'Completed',
    ]

    DEGREE_CHOICES = [
        ('Bachelor', 'Bachelor Degree'),
        ('Master', 'Master Degree'),
        ('PhD', 'Doctoral Degree (PhD)'),
        ('Language', 'Chinese Language Program'),
    ]

    SCHOLARSHIP_CHOICES = [
        ('CSC Type A', 'Chinese Government Scholarship (CSC Type A - Embassy)'),
        ('CSC Type B', 'Chinese Government Scholarship (CSC Type B - University High-Level)'),
        ('Belt and Road', 'Belt & Road / Silk Road Scholarship'),
        ('Provincial', 'Provincial Government Full / Partial Scholarship'),
        ('University President', 'University Presidential Scholarship'),
        ('Self Funded', 'Self-Funded (Tuition Discount)'),
    ]

    INTAKE_CHOICES = [
        ('Autumn 2026', 'Autumn Intake 2026 (September)'),
        ('Spring 2026', 'Spring Intake 2026 (March)'),
        ('Autumn 2027', 'Autumn Intake 2027 (September)'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    application_id = models.CharField(
        max_length=30,
        unique=True,
        default=generate_application_id,
        editable=False,
        verbose_name="Unique Application ID"
    )

    # University & Program Selection
    target_degree = models.CharField(max_length=50, choices=DEGREE_CHOICES, default='Bachelor')
    preferred_university = models.ForeignKey(
        University,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications'
    )
    preferred_university_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="If university not in system list"
    )
    preferred_program = models.ForeignKey(
        Program,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications'
    )
    preferred_program_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="e.g. MBBS, Computer Science & AI, International Trade"
    )
    target_intake = models.CharField(max_length=50, choices=INTAKE_CHOICES, default='Autumn 2026')
    scholarship_preference = models.CharField(max_length=50, choices=SCHOLARSHIP_CHOICES, default='CSC Type B')

    # Academic Background
    highest_qualification = models.CharField(max_length=150, help_text="e.g. Higher Secondary Certificate (HSC) / Bachelor of Science")
    institute_name = models.CharField(max_length=200, help_text="Name of your college/university")
    graduation_year = models.PositiveIntegerField(help_text="Year of completion, e.g. 2024")
    cgpa_or_percentage = models.CharField(max_length=50, help_text="e.g. 3.80 / 4.00 or 85%")
    english_proficiency = models.CharField(
        max_length=150,
        default="English Medium of Instruction (MOI)",
        help_text="e.g. IELTS 6.5, Duolingo 110, or English Medium Certificate"
    )

    # Status tracking
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Submitted')
    status_note = models.TextField(
        blank=True,
        default="Your application dossier has been received and queued for document verification by our counselor team.",
        verbose_name="Public Status Note (Visible to Student)"
    )
    has_missing_documents = models.BooleanField(
        default=False,
        verbose_name="Missing / Re-upload Required Alert"
    )
    missing_documents_note = models.TextField(
        blank=True,
        verbose_name="Specific Document Re-upload Instructions"
    )
    internal_counselor_notes = models.TextField(
        blank=True,
        verbose_name="Internal Counselor Notes (Private)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.application_id} - {self.student.get_full_name() or self.student.username} ({self.status})"

    def get_absolute_url(self):
        return reverse('portal:application_detail', kwargs={'app_id': self.application_id})

    @property
    def display_university(self):
        if self.preferred_university:
            return self.preferred_university.name
        return self.preferred_university_name or "To be decided with counselor"

    @property
    def display_program(self):
        if self.preferred_program:
            return self.preferred_program.title
        return self.preferred_program_name or "General Major Consultation"

    @property
    def stage_index(self):
        """Returns 1-based index (1 to 7) of current status stage."""
        try:
            return self.ORDERED_STATUSES.index(self.status) + 1
        except ValueError:
            return 1

    @property
    def progress_percentage(self):
        """Calculates progress percentage from 14% to 100%."""
        idx = self.stage_index
        return int((idx / len(self.ORDERED_STATUSES)) * 100)

    def is_stage_completed(self, stage_name):
        """Returns whether a given stage has been reached or surpassed."""
        try:
            current_idx = self.ORDERED_STATUSES.index(self.status)
            target_idx = self.ORDERED_STATUSES.index(stage_name)
            return current_idx >= target_idx
        except ValueError:
            return False

    def is_current_stage(self, stage_name):
        return self.status == stage_name


class ApplicationDocument(models.Model):
    """Documents uploaded by students for their application."""
    DOCUMENT_TYPES = [
        ('passport', 'Passport Bio Page'),
        ('photo', 'Passport-size White Background Photo'),
        ('certificate', 'Highest Degree Certificate / Graduation Certificate'),
        ('transcript', 'Official Academic Transcript / Marksheet'),
        ('cv', 'Curriculum Vitae (CV / Resume)'),
        ('study_plan', 'Study Plan / Statement of Purpose (SOP)'),
        ('rec_letter_1', 'Academic Recommendation Letter 1 (Professor)'),
        ('rec_letter_2', 'Academic Recommendation Letter 2 (Associate Professor)'),
        ('physical_exam', 'Foreigner Physical Examination Form (Medical Report)'),
        ('police_clearance', 'Non-Criminal Record Certificate (Police Clearance)'),
        ('english_cert', 'English Proficiency Certificate / MOI'),
        ('other', 'Other Supplementary Documents / Awards / Portfolio'),
    ]

    DOCUMENT_STATUS = [
        ('pending', 'Pending Verification'),
        ('verified', 'Verified & Approved'),
        ('action_required', 'Action Required / Re-upload Requested'),
    ]

    application = models.ForeignKey(StudentApplication, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=150)
    file = models.FileField(upload_to='student_documents/%Y/%m/')
    status = models.CharField(max_length=30, choices=DOCUMENT_STATUS, default='pending')
    counselor_feedback = models.TextField(
        blank=True,
        help_text="Feedback if document needs to be replaced or re-scanned"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return f"{self.application.application_id} - {self.get_doc_type_display()} ({self.get_status_display()})"

    @property
    def file_extension(self):
        if self.file:
            name = self.file.name
            return name.split('.')[-1].upper() if '.' in name else 'FILE'
        return ''


class ApplicationTimeline(models.Model):
    """History of status changes, remarks, and admissions milestones."""
    application = models.ForeignKey(StudentApplication, on_delete=models.CASCADE, related_name='timeline')
    status = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    note = models.TextField(blank=True)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.application.application_id} - {self.status} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
