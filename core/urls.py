from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('study-in-china/', views.study_in_china, name='study_in_china'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq_view, name='faq'),
    path('newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
