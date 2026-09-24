"""
ASGI config for Bright Edu Consultancy project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bright_edu.settings')
application = get_asgi_application()
