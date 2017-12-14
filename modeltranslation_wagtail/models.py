from modeltranslation import settings as mt_settings
from modeltranslation.utils import build_localized_fieldname
from wagtail.wagtailcore.models import Page


class TranslatedPage(Page):

    def set_url_path(self, parent):
        """
        Work in progress for setting the paths of parent Page objects.
        """

        for language in mt_settings.AVAILABLE_LANGUAGES:

            localized_slug_field = build_localized_fieldname('slug', language)

            default_localized_slug_field = build_localized_fieldname(
                'slug',
                mt_settings.DEFAULT_LANGUAGE
            )

            localized_url_path_field = build_localized_fieldname(
                'url_path',
                language
            )

            default_localized_url_path_field = build_localized_fieldname(
                'url_path',
                mt_settings.DEFAULT_LANGUAGE
            )

            if parent:
                parent = parent.specific

                # Emulate the default behavior of django-modeltranslation to
                # get the slug and url path for the current language. If the
                # value for the current language is invalid we get the one
                # for the default fallback language
                slug = (
                    getattr(self, localized_slug_field, None) or
                    getattr(self, default_localized_slug_field, self.slug)
                )
                parent_url_path = (
                    getattr(parent, localized_url_path_field, None) or
                    getattr(parent, default_localized_url_path_field, None) or
                    parent.url_path
                )

                setattr(
                    self,
                    localized_url_path_field,
                    parent_url_path + slug + '/'
                )

            else:
                # a page without a parent is the tree root,
                # which always has a url_path of '/'
                setattr(self, localized_url_path_field, '/')

        # update url_path for children pages
        for child in self.get_children().specific():
            child.set_url_path(self.specific)
            child.save()

        return self.url_path

    class Meta:
        proxy = True
