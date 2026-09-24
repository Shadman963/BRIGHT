from django.contrib import admin
from .models import (
    StudentProfile,
    StudentApplication,
    ApplicationDocument,
    ApplicationTimeline
)

class ApplicationDocumentInline(admin.TabularInline):
    model = ApplicationDocument
    extra = 0
    fields = ('doc_type', 'title', 'file', 'status', 'counselor_feedback', 'uploaded_at')
    readonly_fields = ('uploaded_at',)


class ApplicationTimelineInline(admin.TabularInline):
    model = ApplicationTimeline
    extra = 0
    fields = ('status', 'title', 'note', 'created_at', 'performed_by')
    readonly_fields = ('created_at',)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'nationality', 'passport_number', 'date_of_birth', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'phone', 'passport_number')


@admin.register(StudentApplication)
class StudentApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'application_id',
        'student',
        'target_degree',
        'display_program',
        'display_university',
        'status',
        'has_missing_documents',
        'created_at'
    )
    list_filter = ('status', 'target_degree', 'has_missing_documents', 'target_intake', 'scholarship_preference')
    search_fields = (
        'application_id',
        'student__username',
        'student__first_name',
        'student__last_name',
        'student__email',
        'preferred_university_name',
        'preferred_program_name'
    )
    readonly_fields = ('application_id', 'created_at', 'updated_at')
    inlines = [ApplicationDocumentInline, ApplicationTimelineInline]


@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):
    list_display = ('application', 'doc_type', 'title', 'status', 'uploaded_at')
    list_filter = ('status', 'doc_type', 'uploaded_at')
    search_fields = ('title', 'application__application_id', 'application__student__email')


@admin.register(ApplicationTimeline)
class ApplicationTimelineAdmin(admin.ModelAdmin):
    list_display = ('application', 'status', 'title', 'created_at', 'performed_by')
    list_filter = ('status', 'created_at')
    search_fields = ('application__application_id', 'title', 'note')
