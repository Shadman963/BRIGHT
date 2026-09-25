"""
Django settings for Bright Edu Consultancy project.
Configured for production readiness and seamless deployment.
"""

from pathlib import Path
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    pass


def get_bool_env(name: str, default: bool = False) -> bool:
    """Helper to safely parse boolean environment variables."""
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in ('true', '1', 't', 'yes', 'on')


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-bright-edu-consultancy-2026-portal-top-secret-key-92847193'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool_env('DEBUG', default=False)

# Warn if running in production with default insecure key
if not DEBUG and SECRET_KEY.startswith('django-insecure-'):
    import warnings
    warnings.warn(
        "SECURITY WARNING: SECRET_KEY is using an insecure default value. "
        "Please set SECRET_KEY in your production environment variables or .env file!",
        RuntimeWarning
    )

# Allowed Hosts configuration
allowed_hosts_env = os.environ.get('ALLOWED_HOSTS')
if allowed_hosts_env:
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',') if host.strip()]
elif DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Render environment support
render_external_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_external_hostname:
    ALLOWED_HOSTS.extend([render_external_hostname, '.onrender.com'])

# CSRF Trusted Origins (required for Django 4.0+ with HTTPS)
csrf_origins_env = os.environ.get('CSRF_TRUSTED_ORIGINS')
CSRF_TRUSTED_ORIGINS = (
    [origin.strip() for origin in csrf_origins_env.split(',') if origin.strip()]
    if csrf_origins_env else []
)
if render_external_hostname:
    CSRF_TRUSTED_ORIGINS.extend([
        f'https://{render_external_hostname}',
        'https://*.onrender.com',
    ])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Local consultancy apps
    'core.apps.CoreConfig',
    'universities.apps.UniversitiesConfig',
    'portal.apps.PortalConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bright_edu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'bright_edu.wsgi.application'
ASGI_APPLICATION = 'bright_edu.asgi.application'

# Database configuration
# Supports DATABASE_URL (PostgreSQL, MySQL, SQLite) via dj-database-url
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.config(
                default=DATABASE_URL,
                conn_max_age=600,
                conn_health_checks=True,
            )
        }
    except ImportError:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise storage for high performance static assets in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_USE_FINDERS = True

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Media files (User uploads: documents, certificates, photos)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
SERVE_MEDIA_FILES = get_bool_env('SERVE_MEDIA_FILES', default=True)

# File upload limits (max 10MB per document)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication URLs
LOGIN_URL = 'portal:login'
LOGIN_REDIRECT_URL = 'portal:dashboard'
LOGOUT_REDIRECT_URL = 'core:home'

# Email backend configuration
EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend'
)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = get_bool_env('EMAIL_USE_TLS', default=True)
EMAIL_USE_SSL = get_bool_env('EMAIL_USE_SSL', default=False)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get(
    'DEFAULT_FROM_EMAIL',
    'Bright Edu Consultancy <admissions@brighteduconsultancy.com>'
)

# Production Security & SSL Settings
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    SECURE_SSL_REDIRECT = get_bool_env('SECURE_SSL_REDIRECT', default=False)
    SESSION_COOKIE_SECURE = get_bool_env('SESSION_COOKIE_SECURE', default=True)
    CSRF_COOKIE_SECURE = get_bool_env('CSRF_COOKIE_SECURE', default=True)
    
    hsts_seconds = int(os.environ.get('SECURE_HSTS_SECONDS', '31536000'))
    if hsts_seconds > 0:
        SECURE_HSTS_SECONDS = hsts_seconds
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True
        SECURE_HSTS_PRELOAD = True

# Production Structured Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} {module}:{lineno} - {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# Consultancy contact settings (overridable via environment variables)
CONSULTANCY_INFO = {
    'NAME': os.environ.get('CONSULTANCY_NAME', 'Bright Edu Consultancy'),
    'TAGLINE': os.environ.get('CONSULTANCY_TAGLINE', 'Your Gateway to Global Education & China Scholarships'),
    'PHONE': os.environ.get('CONSULTANCY_PHONE', '+880 1712 345678'),
    'WHATSAPP': os.environ.get('CONSULTANCY_WHATSAPP', '+8801712345678'),
    'WHATSAPP_DISPLAY': os.environ.get('CONSULTANCY_WHATSAPP_DISPLAY', '+880 1712-345678'),
    'WECHAT_ID': os.environ.get('CONSULTANCY_WECHAT', 'BrightEdu_China'),
    'EMAIL': os.environ.get('CONSULTANCY_EMAIL', 'info@brighteduconsultancy.com'),
    'ADMISSIONS_EMAIL': os.environ.get('CONSULTANCY_ADMISSIONS_EMAIL', 'admissions@brighteduconsultancy.com'),
    'MAIN_OFFICE': os.environ.get('CONSULTANCY_MAIN_OFFICE', 'Suite 701, Green Horizon Tower, Panthapath, Dhaka-1205'),
    'CHINA_OFFICE': os.environ.get('CONSULTANCY_CHINA_OFFICE', 'Building 4, Science Park, Pudong New Area, Shanghai, China'),
    'OFFICE_HOURS': os.environ.get('CONSULTANCY_OFFICE_HOURS', 'Sat - Thu: 9:30 AM - 6:30 PM (Friday Closed)'),
    'FACEBOOK_URL': os.environ.get('CONSULTANCY_FACEBOOK_URL', 'https://facebook.com/brighteduconsultancy'),
    'INSTAGRAM_URL': os.environ.get('CONSULTANCY_INSTAGRAM_URL', 'https://instagram.com/brighteduconsultancy'),
    'LINKEDIN_URL': os.environ.get('CONSULTANCY_LINKEDIN_URL', 'https://linkedin.com/company/bright-edu-consultancy'),
}
