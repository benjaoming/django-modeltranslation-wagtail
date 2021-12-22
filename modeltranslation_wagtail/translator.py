from modeltranslation.translator import TranslationOptions as TranslationOptionsOrig  # noqa
from modeltranslation.translator import AlreadyRegistered
from modeltranslation import translator

from wagtail.core.models import Page


# Ensure that the Page model is registered for translation when this module is
# imported.
# try:
#     translator.translator.register(Page)
# except AlreadyRegistered:
#     pass


# We register the Page model as a translated model so that modeltranslation
# does not fail -- but we don't actually register any fields. This is because
# we don't want MultilingualManager as it will be inherited onto models that
# are NOT being translated.
if not Page in translator.translator._registry:
    opts = TranslationOptionsOrig(Page)
    opts.registered = True
    translator.translator._registry[Page] = opts


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
