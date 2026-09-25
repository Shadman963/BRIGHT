from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Testimonial, FAQ, ContactMessage, NewsletterSubscriber
from .forms import ContactForm, NewsletterForm

def home(request):
    """Home landing page with interactive search, featured universities, and scholarship guide."""
    # Lazy import to avoid circular dependency
    try:
        from universities.models import University, Program
        featured_unis = University.objects.filter(is_featured=True)[:6]
        popular_programs = Program.objects.select_related('university').filter(is_popular=True)[:6]
    except Exception:
        featured_unis = []
        popular_programs = []

    featured_testimonials = Testimonial.objects.filter(is_featured=True)[:4]
    general_faqs = FAQ.objects.filter(is_active=True)[:5]
    contact_form = ContactForm()

    context = {
        'featured_unis': featured_unis,
        'popular_programs': popular_programs,
        'testimonials': featured_testimonials,
        'faqs': general_faqs,
        'contact_form': contact_form,
    }
    return render(request, 'core/home.html', context)


def about(request):
    """About Bright Edu Consultancy, history, mission, vision, and team."""
    return render(request, 'core/about.html')


def services(request):
    """Consultancy services provided to prospective international students."""
    return render(request, 'core/services.html')


def study_in_china(request):
    """Comprehensive guide to studying in China, CSC scholarships, intakes, costs & visas."""
    faqs = FAQ.objects.filter(category='china', is_active=True)
    return render(request, 'core/study_in_china.html', {'faqs': faqs})


def testimonials(request):
    """Student success stories and reviews."""
    degree_filter = request.GET.get('degree', '')
    testimonials_list = Testimonial.objects.all()

    if degree_filter:
        testimonials_list = testimonials_list.filter(degree_level=degree_filter)

    return render(request, 'core/testimonials.html', {
        'testimonials': testimonials_list,
        'selected_degree': degree_filter,
    })


def contact(request):
    """Contact page with interactive form, office locations, WeChat QR and WhatsApp."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()
            # Send notification email if configured
            try:
                subject = f"[Bright Edu Inquiry] New message from {contact_msg.name}"
                body = (
                    f"Name: {contact_msg.name}\n"
                    f"Email: {contact_msg.email}\n"
                    f"Phone/WhatsApp: {contact_msg.phone}\n"
                    f"Desired Degree: {contact_msg.desired_degree}\n"
                    f"Subject: {contact_msg.subject}\n\n"
                    f"Message:\n{contact_msg.message}\n"
                )
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONSULTANCY_INFO['ADMISSIONS_EMAIL']],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(
                request,
                f"Thank you, {contact_msg.name}! Your inquiry has been received. Our senior counselor will contact you via WhatsApp/Email within 24 hours."
            )
            return redirect('core:contact')
        else:
            messages.error(request, "Please correct the errors in the form below.")
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})


def faq_view(request):
    """Categorized FAQs list."""
    faqs = FAQ.objects.filter(is_active=True)
    categories = FAQ.CATEGORY_CHOICES
    return render(request, 'core/faq.html', {
        'faqs': faqs,
        'categories': categories,
    })


def newsletter_subscribe(request):
    """Handle newsletter subscriptions."""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, "Congratulations! You have subscribed to China Scholarship alerts.")
            else:
                messages.info(request, "You are already subscribed to our scholarship newsletter.")
        else:
            messages.error(request, "Please provide a valid email address.")
    return redirect(request.META.get('HTTP_REFERER', 'core:home'))


# ---------------- PRODUCTION HTTP ERROR HANDLERS ---------------- #

def custom_400_view(request, exception=None):
    """Custom 400 Bad Request error page."""
    return render(request, '400.html', status=400)


def custom_403_view(request, exception=None):
    """Custom 403 Permission Denied error page."""
    return render(request, '403.html', status=403)


def custom_404_view(request, exception=None):
    """Custom 404 Page Not Found error page."""
    return render(request, '404.html', status=404)


def custom_500_view(request):
    """Custom 500 Internal Server Error page."""
    return render(request, '500.html', status=500)

