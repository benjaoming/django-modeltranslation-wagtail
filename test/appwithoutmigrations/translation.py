from modeltranslation.translator import register
from modeltranslation_wagtail.translator import TranslationOptions

from .models import ModelWithoutMigrations


@register(ModelWithoutMigrations)
class ModelWithoutMigrationsTR(TranslationOptions):
    fields = ("field_that_is_translated",)
