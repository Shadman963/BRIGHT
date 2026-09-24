from django.contrib import admin
from .models import University, Program, Scholarship

class ProgramInline(admin.TabularInline):
    model = Program
    extra = 1
    fields = ('title', 'degree_level', 'discipline', 'language_of_instruction', 'annual_tuition_cny', 'is_popular')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('name', 'scholarship_type', 'coverage', 'monthly_stipend')
    list_filter = ('scholarship_type',)
    search_fields = ('name', 'coverage', 'description')


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'chinese_name', 'city', 'province', 'ranking_national', 'ranking_world', 'has_csc_scholarship', 'is_featured')
    list_filter = ('province', 'has_csc_scholarship', 'has_provincial_scholarship', 'is_featured')
    search_fields = ('name', 'chinese_name', 'city', 'province', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProgramInline]


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'university', 'degree_level', 'discipline', 'language_of_instruction', 'annual_tuition_cny', 'intake', 'is_popular')
    list_filter = ('degree_level', 'discipline', 'language_of_instruction', 'intake', 'is_popular', 'university__city')
    search_fields = ('title', 'university__name', 'requirements')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('scholarships',)
