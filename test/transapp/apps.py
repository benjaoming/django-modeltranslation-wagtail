# -*- coding: utf-8 -*-
from django.apps.config import AppConfig

app_label = "transapp"

class TransappConfig(AppConfig):
    name = 'test.transapp'
    verbose_name = "Kiks"
    default_auto_field = 'django.db.models.BigAutoField'
