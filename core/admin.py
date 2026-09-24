from django.contrib import admin
from .models import ContactMessage, Testimonial, FAQ, NewsletterSubscriber

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'desired_degree', 'subject', 'created_at', 'is_read', 'replied')
    list_filter = ('is_read', 'replied', 'desired_degree', 'created_at')
    search_fields = ('name', 'email', 'phone', 'subject', 'message')
    readonly_fields = ('created_at',)
    actions = ['mark_as_read', 'mark_as_replied']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected inquiries as Read"

    def mark_as_replied(self, request, queryset):
        queryset.update(replied=True, is_read=True)
    mark_as_replied.short_description = "Mark selected inquiries as Replied"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'university_admitted', 'program_name', 'degree_level', 'scholarship_received', 'rating', 'is_featured', 'display_order')
    list_filter = ('degree_level', 'is_featured', 'rating')
    search_fields = ('student_name', 'university_admitted', 'program_name', 'quote')
    list_editable = ('is_featured', 'display_order')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'display_order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('question', 'answer')
    list_editable = ('display_order', 'is_active')


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
