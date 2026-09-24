from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import University, Program, Scholarship

def university_list(request):
    """List of all universities with multi-parameter search and filters."""
    query = request.GET.get('q', '').strip()
    city_filter = request.GET.get('city', '').strip()
    scholarship_filter = request.GET.get('scholarship', '').strip()
    degree_filter = request.GET.get('degree', '').strip()

    universities = University.objects.prefetch_related('programs').all()

    if query:
        universities = universities.filter(
            Q(name__icontains=query) |
            Q(chinese_name__icontains=query) |
            Q(city__icontains=query) |
            Q(province__icontains=query) |
            Q(description__icontains=query)
        )

    if city_filter:
        universities = universities.filter(city__iexact=city_filter)

    if scholarship_filter == 'csc':
        universities = universities.filter(has_csc_scholarship=True)
    elif scholarship_filter == 'provincial':
        universities = universities.filter(has_provincial_scholarship=True)

    if degree_filter:
        universities = universities.filter(programs__degree_level=degree_filter).distinct()

    # Get distinct cities for filter dropdown
    cities = University.objects.values_list('city', flat=True).distinct().order_by('city')

    context = {
        'universities': universities,
        'cities': cities,
        'selected_q': query,
        'selected_city': city_filter,
        'selected_scholarship': scholarship_filter,
        'selected_degree': degree_filter,
        'total_count': universities.count(),
    }
    return render(request, 'universities/university_list.html', context)


def university_detail(request, slug):
    """Detailed profile of a specific university, its programs, scholarships and campus."""
    university = get_object_or_404(University.objects.prefetch_related('programs__scholarships'), slug=slug)
    programs = university.programs.all()

    # Group programs by degree level for clear presentation
    bachelor_programs = programs.filter(degree_level='Bachelor')
    master_programs = programs.filter(degree_level='Master')
    phd_programs = programs.filter(degree_level='PhD')
    language_programs = programs.filter(degree_level='Language')

    # Available scholarships at this university
    scholarships = Scholarship.objects.filter(programs__university=university).distinct()

    context = {
        'university': university,
        'programs': programs,
        'bachelor_programs': bachelor_programs,
        'master_programs': master_programs,
        'phd_programs': phd_programs,
        'language_programs': language_programs,
        'scholarships': scholarships,
    }
    return render(request, 'universities/university_detail.html', context)


def program_list(request):
    """Search and browse all academic programs across universities."""
    query = request.GET.get('q', '').strip()
    discipline_filter = request.GET.get('discipline', '').strip()
    degree_filter = request.GET.get('degree', '').strip()
    language_filter = request.GET.get('language', '').strip()

    programs = Program.objects.select_related('university').prefetch_related('scholarships').all()

    if query:
        programs = programs.filter(
            Q(title__icontains=query) |
            Q(university__name__icontains=query) |
            Q(university__city__icontains=query) |
            Q(requirements__icontains=query)
        )

    if discipline_filter:
        programs = programs.filter(discipline=discipline_filter)

    if degree_filter:
        programs = programs.filter(degree_level=degree_filter)

    if language_filter:
        programs = programs.filter(language_of_instruction=language_filter)

    context = {
        'programs': programs,
        'disciplines': Program.DISCIPLINES,
        'degree_levels': Program.DEGREE_LEVELS,
        'languages': Program.LANGUAGES,
        'selected_q': query,
        'selected_discipline': discipline_filter,
        'selected_degree': degree_filter,
        'selected_language': language_filter,
        'total_count': programs.count(),
    }
    return render(request, 'universities/program_list.html', context)


def program_detail(request, university_slug, program_slug):
    """Detailed page for an individual program with requirements, tuition, and apply CTA."""
    program = get_object_or_404(
        Program.objects.select_related('university').prefetch_related('scholarships'),
        university__slug=university_slug,
        slug=program_slug
    )

    related_programs = Program.objects.filter(
        university=program.university
    ).exclude(id=program.id)[:4]

    context = {
        'program': program,
        'university': program.university,
        'scholarships': program.scholarships.all(),
        'related_programs': related_programs,
    }
    return render(request, 'universities/program_detail.html', context)
