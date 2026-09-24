from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Student Portal
    path('dashboard/', views.dashboard, name='dashboard'),
    path('apply/', views.apply_view, name='apply'),
    path('application/<str:app_id>/', views.application_detail, name='application_detail'),
    path('documents/', views.documents_view, name='documents'),
    path('documents/<str:app_id>/', views.documents_view, name='documents_app'),
    path('documents/replace/<int:doc_id>/', views.replace_document, name='replace_document'),

    # Counselor / Staff Management Portal
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/application/<str:app_id>/', views.staff_application_detail, name='staff_app_detail'),
]
