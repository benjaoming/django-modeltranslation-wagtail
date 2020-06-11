from modeltranslation.translator import TranslationOptions as TranslationOptionsOrig  # noqa
from modeltranslation.translator import AlreadyRegistered
from modeltranslation.translator import translator

from wagtail.core.models import Page


# Ensure that the Page model is registered for translation when this module is
# imported.
try:
    translator.register(Page)
except AlreadyRegistered:
    pass


class TranslationOptions(TranslationOptionsOrig):

    def __init__(self, *args, **kwargs):
        """
        Create fields dicts without any translation fields.
        """
        # Extend local fields, this ensures that Wagtail Page models are always
        # extend on the local application, not on Wagtail itself (which would
        # cause us to need migrations on wagtailcore!)
        self.fields = list(self.fields)
        self.fields += [
            'search_description',
            'seo_title',
            'title',
        ]
        super(TranslationOptions, self).__init__(*args, **kwargs)
