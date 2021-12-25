from django.db import models
from wagtail.core.models import Page


class ModelWithoutMigrations(Page):
    """
    This model is translated but there are no migrations.
    
    During testing, we create the migrations and verify that they are okay.
    """
    
    field_that_is_translated = models.CharField(max_length=255, null=True, blank=True)
    field_that_is_not_translated = models.CharField(max_length=255, null=True, blank=True)
