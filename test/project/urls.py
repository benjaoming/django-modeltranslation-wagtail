from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns

from wagtail.wagtailcore import urls as wagtail_urls


urlpatterns = i18n_patterns(
    url("", include(wagtail_urls)),
)
