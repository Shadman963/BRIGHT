from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Scholarship(models.Model):
    """Scholarships available for students in China and abroad."""
    SCHOLARSHIP_TYPES = [
        ('csc_type_a', 'Chinese Government Scholarship (CSC Type A - Bilateral)'),
        ('csc_type_b', 'Chinese Government Scholarship (CSC Type B - University High-Level)'),
        ('belt_road', 'Belt and Road / Silk Road Scholarship'),
        ('provincial', 'Provincial Government Scholarship (Zhejiang, Jiangsu, etc.)'),
        ('municipal', 'Municipal Mayor Scholarship (Shanghai, Beijing, etc.)'),
        ('university', 'University Presidential Full/Partial Scholarship'),
        ('enterprise', 'Corporate / Enterprise Sponsored Scholarship'),
    ]

    name = models.CharField(max_length=200)
    scholarship_type = models.CharField(max_length=50, choices=SCHOLARSHIP_TYPES)
    coverage = models.CharField(
        max_length=250,
        help_text="e.g. 100% Tuition Waiver + Free Campus Accommodation + Monthly Stipend"
    )
    monthly_stipend = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. 2,500 RMB (Bachelor), 3,000 RMB (Master), 3,500 RMB (PhD)"
    )
    eligibility = models.TextField(blank=True)
    description = models.TextField(blank=True)
    badge_color = models.CharField(
        max_length=50,
        default="bg-emerald-100 text-emerald-800 border-emerald-300",
        help_text="CSS badge classes"
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_scholarship_type_display()})"


class University(models.Model):
    """Universities represented or partnered with Bright Edu Consultancy."""
    name = models.CharField(max_length=200, unique=True, verbose_name="University Name")
    chinese_name = models.CharField(max_length=200, blank=True, verbose_name="Chinese Name (Hanzi)")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="China")
    ranking_national = models.PositiveIntegerField(null=True, blank=True, verbose_name="National Rank")
    ranking_world = models.PositiveIntegerField(null=True, blank=True, verbose_name="QS/THE World Rank")
    logo = models.ImageField(upload_to='universities/logos/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='universities/covers/', blank=True, null=True)
    cover_image_url = models.URLField(blank=True, help_text="Fallback external image URL if no file uploaded")
    website = models.URLField(blank=True)
    description = models.TextField()
    campus_highlights = models.TextField(blank=True, help_text="List key campus facilities, labs, dorms")
    has_csc_scholarship = models.BooleanField(default=True, verbose_name="CSC Scholarship Eligible")
    has_provincial_scholarship = models.BooleanField(default=True, verbose_name="Provincial Scholarship Eligible")
    is_featured = models.BooleanField(default=False, verbose_name="Feature on Home Page")
    established_year = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ranking_national', 'name']
        verbose_name_plural = "Universities"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('universities:university_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    @property
    def display_cover(self):
        if self.cover_image:
            return self.cover_image.url
        if self.cover_image_url:
            return self.cover_image_url
        return 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=1000&auto=format&fit=crop&q=80'


class Program(models.Model):
    """Academic programs offered at partner universities."""
    DEGREE_LEVELS = [
        ('Bachelor', 'Bachelor Degree (Undergraduate)'),
        ('Master', 'Master Degree (Postgraduate)'),
        ('PhD', 'Doctoral Degree (PhD)'),
        ('Language', 'Non-Degree / Chinese Language Program'),
    ]

    DISCIPLINES = [
        ('Medicine', 'Medicine & MBBS (English Taught)'),
        ('Computer Science', 'Computer Science, AI & Software Engineering'),
        ('Engineering', 'Civil, Mechanical & Electrical Engineering'),
        ('Business', 'International Business, Trade & Finance'),
        ('Science', 'Natural Sciences & Biotechnology'),
        ('Chinese Language', 'Chinese Language & Cultural Studies'),
        ('Arts & Design', 'Arts, Architecture & Media'),
        ('Other', 'Other Academic Fields'),
    ]

    LANGUAGES = [
        ('English', 'English Taught'),
        ('Chinese', 'Chinese Taught (HSK required)'),
        ('Bilingual', 'Bilingual (English & Chinese)'),
    ]

    INTAKE_CHOICES = [
        ('September', 'Autumn Intake (September)'),
        ('March', 'Spring Intake (March)'),
        ('Both', 'Both Spring & Autumn Intakes'),
    ]

    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='programs')
    title = models.CharField(max_length=200, verbose_name="Program Name")
    slug = models.SlugField(max_length=250, blank=True)
    degree_level = models.CharField(max_length=50, choices=DEGREE_LEVELS, default='Bachelor')
    discipline = models.CharField(max_length=50, choices=DISCIPLINES, default='Engineering')
    language_of_instruction = models.CharField(max_length=50, choices=LANGUAGES, default='English')
    duration_years = models.DecimalField(max_digits=3, decimal_places=1, default=4.0, help_text="e.g. 4.0 years for Bachelor, 2.5 for Master")
    annual_tuition_cny = models.PositiveIntegerField(verbose_name="Tuition Fee (CNY/Year)", help_text="Annual tuition in RMB")
    intake = models.CharField(max_length=50, choices=INTAKE_CHOICES, default='September')
    application_deadline = models.CharField(max_length=100, default="June 30 / Rolling", help_text="e.g. May 30, 2026")
    scholarships = models.ManyToManyField(Scholarship, blank=True, related_name='programs')
    requirements = models.TextField(blank=True, help_text="Minimum GPA, age limit, language proficiency (IELTS/Duolingo or English MOI)")
    curriculum_overview = models.TextField(blank=True, help_text="Core course modules and career pathways")
    is_popular = models.BooleanField(default=False, verbose_name="Mark as Popular Program")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['degree_level', 'title']
        unique_together = ('university', 'slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.degree_level}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('universities:program_detail', kwargs={'university_slug': self.university.slug, 'program_slug': self.slug})

    def __str__(self):
        return f"{self.title} ({self.get_degree_level_display()}) - {self.university.name}"

    @property
    def formatted_tuition(self):
        return f"¥{self.annual_tuition_cny:,} CNY"
