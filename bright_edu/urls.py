"""
URL configuration for Bright Edu Consultancy project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('universities/', include('universities.urls', namespace='universities')),
    path('portal/', include('portal.urls', namespace='portal')),
]

# Serve media and static files
# WhiteNoise handles static files automatically in production.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
elif getattr(settings, 'SERVE_MEDIA_FILES', False):
    # Safe media serving fallback for standalone containers / VPS deployments
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

# Custom Admin Site Branding
admin.site.site_header = 'Bright Edu Consultancy - Administration'
admin.site.site_title = 'Bright Edu Portal'
admin.site.index_title = 'Welcome to Bright Edu Management Dashboard'

# Custom HTTP Error Handlers
handler400 = 'core.views.custom_400_view'
handler403 = 'core.views.custom_403_view'
handler404 = 'core.views.custom_404_view'
handler500 = 'core.views.custom_500_view'
