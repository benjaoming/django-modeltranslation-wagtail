from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page


class HomePage(Page):
    """
    This mimics a typical Wagtail model
    """
    
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
        ],
        verbose_name="body",
        blank=True,
        help_text="The main contents of the page",
    )
