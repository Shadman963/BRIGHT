"""
URL configuration for Bright Edu Consultancy project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('universities/', include('universities.urls', namespace='universities')),
    path('portal/', include('portal.urls', namespace='portal')),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom Admin Site Headers
admin.site.site_header = 'Bright Edu Consultancy - Administration'
admin.site.site_title = 'Bright Edu Portal'
admin.site.index_title = 'Welcome to Bright Edu Management Dashboard'
