from modeltranslation.translator import register
from modeltranslation_wagtail.translator import TranslationOptions

from .models import Test


@register(Test)
class TestTR(TranslationOptions):
    fields = ()
