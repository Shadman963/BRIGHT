from django.urls import path
from . import views

app_name = 'universities'

urlpatterns = [
    path('', views.university_list, name='university_list'),
    path('programs/', views.program_list, name='program_list'),
    path('<slug:slug>/', views.university_detail, name='university_detail'),
    path('<slug:university_slug>/program/<slug:program_slug>/', views.program_detail, name='program_detail'),
]
