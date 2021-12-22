from modeltranslation.translator import register
from modeltranslation_wagtail.translator import TranslationOptions

from .models import Test, InheritsFromHomePageTranslated, InheritsFromPageTranslated


@register(Test)
class TestTR(TranslationOptions):
    fields = ("field_that_is_translated",)


@register(InheritsFromHomePageTranslated)
class AnotherTestTranslatedTR(TranslationOptions):
    fields = ("field_that_is_translated",)


@register(InheritsFromPageTranslated)
class AnotherTestTranslatedTR(TranslationOptions):
    fields = ("field_that_is_translated",)
