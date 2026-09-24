from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import (
    StudentProfile,
    StudentApplication,
    ApplicationDocument,
    ApplicationTimeline
)
from universities.models import University, Program

INPUT_CLASSES = "w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none transition text-slate-800"
SELECT_CLASSES = "w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none transition bg-white text-slate-800"
FILE_CLASSES = "w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer"


class StudentRegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Email address (used for login)'})
    )
    phone = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': '+880 1712 345678 (WhatsApp)'})
    )
    nationality = forms.CharField(
        max_length=100,
        initial="Bangladesh",
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Nationality'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Create secure password (min 6 characters)'})
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email address already exists. Please login.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")
        return cleaned_data


class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Email address or username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Password'})
    )


class OnlineApplicationForm(forms.ModelForm):
    # Additional initial document upload fields (optional during first submission, can also upload later)
    passport_file = forms.FileField(
        required=False,
        label="Passport Bio Page (PDF/JPG)",
        widget=forms.FileInput(attrs={'class': FILE_CLASSES, 'accept': '.pdf,.jpg,.jpeg,.png'})
    )
    photo_file = forms.FileField(
        required=False,
        label="Recent White Background Photo (JPG/PNG)",
        widget=forms.FileInput(attrs={'class': FILE_CLASSES, 'accept': '.jpg,.jpeg,.png'})
    )
    certificate_file = forms.FileField(
        required=False,
        label="Highest Certificate / Diploma (PDF/JPG)",
        widget=forms.FileInput(attrs={'class': FILE_CLASSES, 'accept': '.pdf,.jpg,.jpeg,.png'})
    )
    transcript_file = forms.FileField(
        required=False,
        label="Academic Transcript / Marksheet (PDF)",
        widget=forms.FileInput(attrs={'class': FILE_CLASSES, 'accept': '.pdf,.jpg,.jpeg,.png'})
    )
    cv_file = forms.FileField(
        required=False,
        label="Curriculum Vitae / Resume (PDF)",
        widget=forms.FileInput(attrs={'class': FILE_CLASSES, 'accept': '.pdf,.docx'})
    )
    study_plan_file = forms.FileField(
        required=False,
        label="Study Plan / Statement of Purpose (PDF/DOC)",
        widget=forms.FileInput(attrs={'class': FILE_CLASSES, 'accept': '.pdf,.docx'})
    )

    class Meta:
        model = StudentApplication
        fields = [
            'target_degree',
            'preferred_university',
            'preferred_university_name',
            'preferred_program',
            'preferred_program_name',
            'target_intake',
            'scholarship_preference',
            'highest_qualification',
            'institute_name',
            'graduation_year',
            'cgpa_or_percentage',
            'english_proficiency',
        ]
        widgets = {
            'target_degree': forms.Select(attrs={'class': SELECT_CLASSES}),
            'preferred_university': forms.Select(attrs={'class': SELECT_CLASSES}),
            'preferred_university_name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'If university is not in dropdown'}),
            'preferred_program': forms.Select(attrs={'class': SELECT_CLASSES}),
            'preferred_program_name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g. Computer Science, MBBS, International Trade'}),
            'target_intake': forms.Select(attrs={'class': SELECT_CLASSES}),
            'scholarship_preference': forms.Select(attrs={'class': SELECT_CLASSES}),
            'highest_qualification': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g. HSC / High School / Bachelor in Science'}),
            'institute_name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g. Dhaka College / University of Dhaka'}),
            'graduation_year': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g. 2024'}),
            'cgpa_or_percentage': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g. 4.90 / 5.00 or 85%'}),
            'english_proficiency': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g. English Medium / IELTS 6.5 / Duolingo'}),
        }


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = ApplicationDocument
        fields = ['doc_type', 'title', 'file']
        widgets = {
            'doc_type': forms.Select(attrs={'class': SELECT_CLASSES}),
            'title': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Document title / description (e.g. Official Transcript 2024)'}),
            'file': forms.FileInput(attrs={'class': FILE_CLASSES, 'required': True}),
        }


class ReplaceDocumentForm(forms.ModelForm):
    class Meta:
        model = ApplicationDocument
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'class': FILE_CLASSES, 'required': True}),
        }


class AdminStatusUpdateForm(forms.ModelForm):
    timeline_note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 2, 'placeholder': 'Reason or milestone detail for status change log...'})
    )

    class Meta:
        model = StudentApplication
        fields = [
            'status',
            'status_note',
            'has_missing_documents',
            'missing_documents_note',
            'internal_counselor_notes',
        ]
        widgets = {
            'status': forms.Select(attrs={'class': SELECT_CLASSES}),
            'status_note': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 3}),
            'has_missing_documents': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-blue-600 rounded border-slate-300 focus:ring-blue-500'}),
            'missing_documents_note': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 3, 'placeholder': 'Specific instruction for student re-upload...'}),
            'internal_counselor_notes': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 3, 'placeholder': 'Private internal notes...'}),
        }


class AdminDocumentReviewForm(forms.ModelForm):
    class Meta:
        model = ApplicationDocument
        fields = ['status', 'counselor_feedback']
        widgets = {
            'status': forms.Select(attrs={'class': SELECT_CLASSES}),
            'counselor_feedback': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 2, 'placeholder': 'Feedback if document needs adjustment or re-upload'}),
        }
