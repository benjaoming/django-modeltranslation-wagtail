from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from test.anotherapp.models import HomePage


class AnotherTest(Page):
    """
    This model is entirely NOT translated.
    
    This could be normal for some kind of page that's individual to every
    language.
    """
   
    field_that_is_not_translated = models.CharField(max_length=255, null=True, blank=True)
    content_panels = [
        FieldPanel("field_that_is_not_translated"),
        StreamFieldPanel("body"),
    ]
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        verbose_name="body",
        blank=True,
        help_text="The main contents of the page",
    )

    def get_context(self, request):
        context = super().get_context(request)
        context['test'] = self.get_children().live()
        return context


class Test(Page):
    """
    This model is translated
    """
    
    field_that_is_translated = models.CharField(max_length=255, null=True, blank=True)
    field_that_is_not_translated = models.CharField(max_length=255, null=True, blank=True)


class InheritsFromHomePageTranslated(HomePage):
    """
    This model is translated but inherits from a non-translated parent.
    
    This could be normal for some kind of page that's individual to every
    language.
    """
    
    field_that_is_translated = models.CharField(max_length=255, null=True, blank=True)
    field_that_is_not_translated = models.CharField(max_length=255, null=True, blank=True)


class InheritsFromPageTranslated(Page):
    """
    This model is translated but inherits from a non-translated parent.
    
    This could be normal for some kind of page that's individual to every
    language.
    """
    
    field_that_is_translated = models.CharField(max_length=255, null=True, blank=True)
    field_that_is_not_translated = models.CharField(max_length=255, null=True, blank=True)
