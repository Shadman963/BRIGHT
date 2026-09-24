from django.db import models
from django.utils import timezone

class ContactMessage(models.Model):
    """Stores inquiries submitted from the website contact forms."""
    DEGREE_CHOICES = [
        ('Bachelor', 'Bachelor Degree'),
        ('Master', 'Master Degree'),
        ('PhD', 'PhD / Doctoral'),
        ('Language', 'Chinese Language Program'),
        ('Other', 'Other Programs'),
    ]

    name = models.CharField(max_length=150, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=30, verbose_name="Phone / WhatsApp Number")
    desired_degree = models.CharField(max_length=50, choices=DEGREE_CHOICES, blank=True, verbose_name="Desired Degree")
    subject = models.CharField(max_length=200, verbose_name="Subject")
    message = models.TextField(verbose_name="Inquiry Message")
    is_read = models.BooleanField(default=False, verbose_name="Marked as Read")
    replied = models.BooleanField(default=False, verbose_name="Replied")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Submission Date")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"


class Testimonial(models.Model):
    """Stores student testimonials and success stories."""
    DEGREE_CHOICES = [
        ('Bachelor', 'Bachelor Degree'),
        ('Master', 'Master Degree'),
        ('PhD', 'PhD Degree'),
        ('Language', 'Language & Cultural Studies'),
    ]

    student_name = models.CharField(max_length=150, verbose_name="Student Name")
    home_country = models.CharField(max_length=100, default="Bangladesh", verbose_name="Home Country")
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True, verbose_name="Student Photo")
    university_admitted = models.CharField(max_length=200, verbose_name="University Admitted")
    program_name = models.CharField(max_length=200, verbose_name="Program / Major")
    degree_level = models.CharField(max_length=50, choices=DEGREE_CHOICES, default='Bachelor')
    scholarship_received = models.CharField(
        max_length=200,
        default="Chinese Government Scholarship (CSC) Full Fund",
        verbose_name="Scholarship Received"
    )
    quote = models.TextField(verbose_name="Student Review / Testimonial")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="Rating (1-5)")
    intake_year = models.CharField(max_length=20, default="2025/2026", verbose_name="Intake Year")
    is_featured = models.BooleanField(default=True, verbose_name="Show on Home Page")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = "Student Testimonial"
        verbose_name_plural = "Student Testimonials"

    def __str__(self):
        return f"{self.student_name} - {self.university_admitted}"


class FAQ(models.Model):
    """Frequently asked questions."""
    CATEGORY_CHOICES = [
        ('china', 'Study in China & CSC'),
        ('application', 'Application & Documents'),
        ('visa', 'Visa & Travel Guidance'),
        ('scholarships', 'Scholarship Types & Eligibility'),
        ('general', 'General Consultancy Services'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='china')
    question = models.CharField(max_length=300)
    answer = models.TextField()
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'display_order', 'id']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class NewsletterSubscriber(models.Model):
    """Newsletter subscription list."""
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email
