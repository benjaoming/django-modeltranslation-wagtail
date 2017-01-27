# -*- coding: utf-8 -*-
from django.apps import AppConfig


class ModeltranslationWagtailConfig(AppConfig):
    name = 'modeltranslation_wagtail'
    verbose_name = 'Modeltranslation Wagtail'

    def ready(self):
        from modeltranslation_wagtail.models import handle_translation_registrations
        handle_translation_registrations()
