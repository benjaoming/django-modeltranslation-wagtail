from django.apps.config import AppConfig


class TransAppConfig(AppConfig):
    name = 'modeltranslation_wagtail'
    verbose_name = "Translated Wagtail Models"

    def ready(self):
        """
        Lifted from the great minds in the infoportugal/wagtail-modeltranslation
        community.
        """
        from django.conf import settings
        from modeltranslation import settings as mt_settings

        # Add Wagtail defined fields as modeltranslation custom fields
        wagtail_fields = (
            'StreamField',
            'RichTextField',
        )

        # update both the standard settings and the modeltranslation settings,
        # as we cannot guarantee the load order, and so django_modeltranslation
        # may bootstrap itself either before, or after, our ready() gets called.
        custom_fields = getattr(settings, 'MODELTRANSLATION_CUSTOM_FIELDS', tuple())
        setattr(settings, 'MODELTRANSLATION_CUSTOM_FIELDS', tuple(set(custom_fields + wagtail_fields)))

        mt_custom_fields = getattr(mt_settings, 'CUSTOM_FIELDS', tuple())
        setattr(mt_settings, 'CUSTOM_FIELDS', tuple(set(mt_custom_fields + wagtail_fields)))
