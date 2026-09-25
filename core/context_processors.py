from django.conf import settings
from datetime import datetime

def site_settings(request):
    """Context processor providing global consultancy contact information and settings."""
    site_info = getattr(settings, 'CONSULTANCY_INFO', {
        'NAME': 'Bright Edu Consultancy',
        'TAGLINE': 'Your Gateway to Global Education & China Scholarships',
        'PHONE': '+880 1712 345678',
        'WHATSAPP': '+8801712345678',
        'WHATSAPP_DISPLAY': '+880 1712-345678',
        'WECHAT_ID': 'BrightEdu_China',
        'EMAIL': 'info@brighteduconsultancy.com',
        'ADMISSIONS_EMAIL': 'admissions@brighteduconsultancy.com',
        'MAIN_OFFICE': 'Suite 701, Green Horizon Tower, Panthapath, Dhaka-1205',
        'CHINA_OFFICE': 'Building 4, Science Park, Pudong New Area, Shanghai, China',
        'OFFICE_HOURS': 'Sat - Thu: 9:30 AM - 6:30 PM',
        'FACEBOOK_URL': 'https://facebook.com',
        'INSTAGRAM_URL': 'https://instagram.com',
        'LINKEDIN_URL': 'https://linkedin.com',
    })

    user_application = None
    if hasattr(request, 'user') and request.user.is_authenticated and not request.user.is_staff:
        # Check if student has an existing application
        try:
            from portal.models import StudentApplication
            user_application = StudentApplication.objects.filter(student=request.user).first()
        except Exception:
            user_application = None

    return {
        'site_info': site_info,
        'current_year': datetime.now().year,
        'user_application': user_application,
    }
