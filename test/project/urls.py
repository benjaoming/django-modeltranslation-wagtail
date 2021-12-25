from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls

urlpatterns = []

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("wagtail/", include(wagtailadmin_urls)),
    path("", include(wagtail_urls)),
)
