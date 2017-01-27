# -*- coding: utf-8 -*-
from __future__ import absolute_import

import imp
import os

import django
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase, TransactionTestCase
from django.test.utils import override_settings
from django.utils.translation import get_language, trans_real
try:
    from django.apps import apps as django_apps
    NEW_APP_CACHE = True
except ImportError:
    from django.db.models.loading import AppCache
    NEW_APP_CACHE = False

from . import settings as mt_settings, translator
from .tests.test_settings import TEST_SETTINGS

MIGRATE_CMD = django.VERSION >= (1, 8)
MIGRATIONS = MIGRATE_CMD and "django.contrib.auth" in TEST_SETTINGS[
    'INSTALLED_APPS']
NEW_DEFERRED_API = django.VERSION >= (1, 10)


models = translation = None

# None of the following tests really depend on the content of the request,
# so we'll just pass in None.
request = None

# How many models are registered for tests.
TEST_MODELS = 50 + (1 if MIGRATIONS else 0)


class reload_override_settings(override_settings):
    """Context manager that not only override settings, but also reload modeltranslation conf."""

    def __enter__(self):
        super(reload_override_settings, self).__enter__()
        imp.reload(mt_settings)

    def __exit__(self, exc_type, exc_value, traceback):
        super(reload_override_settings, self).__exit__(
            exc_type, exc_value, traceback)
        imp.reload(mt_settings)


# In this test suite fallback language is turned off. This context manager
# temporarily turns it on.
def default_fallback():
    return reload_override_settings(
        MODELTRANSLATION_FALLBACK_LANGUAGES=(mt_settings.DEFAULT_LANGUAGE,))


class dummy_context_mgr():

    def __enter__(self):
        return None

    def __exit__(self, _type, value, traceback):
        return False


def get_field_names(model):
    if django.VERSION < (1, 9):
        return model._meta.get_all_field_names()
    names = set()
    fields = model._meta.get_fields()
    for field in fields:
        if field.is_relation and field.many_to_one and field.related_model is None:
            continue
        if field.model != model and field.model._meta.concrete_model == model._meta.concrete_model:
            continue

        names.add(field.name)
        if hasattr(field, 'attname'):
            names.add(field.attname)
    return names


@override_settings(**TEST_SETTINGS)
class ModeltranslationTransactionTestBase(TransactionTestCase):
    cache = django_apps if NEW_APP_CACHE else AppCache()
    synced = False

    @classmethod
    def setUpClass(cls):
        """
        Prepare database:
        * Call syncdb to create tables for tests.models (since during
        default testrunner's db creation wagtail_modeltranslation.tests was 
        not in INSTALLED_APPS
        """
        super(ModeltranslationTransactionTestBase, cls).setUpClass()
        if not ModeltranslationTransactionTestBase.synced:
            # In order to perform only one syncdb
            ModeltranslationTransactionTestBase.synced = True
            mgr = (
                override_settings(**TEST_SETTINGS) if django.VERSION < (1, 8)
                else dummy_context_mgr())
            with mgr:
                from django.db import connections, DEFAULT_DB_ALIAS
                if MIGRATIONS:
                    call_command(
                        'makemigrations', 'auth', verbosity=2,
                        interactive=False,
                        database=connections[DEFAULT_DB_ALIAS].alias
                    )

                # 1. Reload translation in case USE_I18N was False
                from django.utils import translation as dj_trans
                imp.reload(dj_trans)

                # 2. Reload MT because LANGUAGES likely changed.
                imp.reload(mt_settings)
                imp.reload(translator)

                # reload the translation module to register the Page model
                from . import translation as wag_trans
                imp.reload(wag_trans)

                # Reload the patching class to update the imported translator
                # in order to include the newly registered models
                from . import patch_wagtailadmin
                imp.reload(patch_wagtailadmin)

                # 3. Reset test models (because autodiscover have already run,
                # those models have translation fields, but for languages
                # previously defined. We want to be sure that 'de' and 'en' are
                # available)
                if not NEW_APP_CACHE:
                    cls.cache.load_app('modeltranslation_wagtail.tests')
                else:
                    del cls.cache.all_models['tests']
                    if MIGRATIONS:
                        del cls.cache.all_models['auth']
                    import sys
                    sys.modules.pop(
                        'modeltranslation_wagtail.tests.models', None)
                    sys.modules.pop(
                        'modeltranslation_wagtail.tests.translation', None)
                    if MIGRATIONS:
                        sys.modules.pop('django.contrib.auth.models', None)
                    cls.cache.get_app_config('tests').import_models(
                        cls.cache.all_models['tests'])
                    if MIGRATIONS:
                        cls.cache.get_app_config('auth').import_models(
                            cls.cache.all_models['auth'])

                # 4. Autodiscover
                from .models import handle_translation_registrations
                handle_translation_registrations()

                # 5. makemigrations (``migrate=False`` in case of south)
                if MIGRATIONS:
                    call_command(
                        'makemigrations', 'auth', verbosity=2,
                        interactive=False,
                        database=connections[DEFAULT_DB_ALIAS].alias
                    )

                # 6. Syncdb (``migrate=False`` in case of south)
                cmd = 'migrate' if MIGRATE_CMD else 'syncdb'
                call_command(
                    cmd, verbosity=0, migrate=False,
                    interactive=False, run_syncdb=True,
                    database=connections[DEFAULT_DB_ALIAS].alias,
                    load_initial_data=False
                )

                # 7. clean migrations
                if MIGRATIONS:
                    import glob
                    dir = os.path.join(os.path.dirname(
                        os.path.abspath(__file__)),
                        "auth_migrations")
                    for f in glob.glob(dir + "/000?_*.py*"):
                        os.unlink(f)

                # A rather dirty trick to import models into module namespace,
                # but not before tests app has been added into INSTALLED_APPS
                # and loaded (that's why this is not imported in normal import
                # section)
                global models, translation
                from .tests import models as t_models, \
                    translation as t_translation
                models = t_models
                translation = t_translation

                from django.db import connections, DEFAULT_DB_ALIAS
                # 6. Syncdb
                call_command('migrate', verbosity=0, migrate=False, interactive=False, run_syncdb=True,
                             database=connections[DEFAULT_DB_ALIAS].alias, load_initial_data=False)

    def setUp(self):
        self._old_language = get_language()
        trans_real.activate('de')

    def tearDown(self):
        trans_real.activate(self._old_language)


class WagtailModeltranslationTest(TestCase,
                                  ModeltranslationTransactionTestBase):
    """
    Test of the modeltranslation features with Wagtail models (Page and
    Snippet)
    """

    @classmethod
    def setUpClass(cls):
        super(WagtailModeltranslationTest, cls).setUpClass()

        # Delete the default wagtail pages from db
        from wagtail.wagtailcore.models import Page
        Page.objects.delete()

    def test_page_fields(self):
        fields = dir(models.PatchTestPage())

        # Check if Page fields are being created
        self.assertIn('title_en', fields)
        self.assertIn('title_de', fields)
        self.assertIn('slug_en', fields)
        self.assertIn('slug_de', fields)
        self.assertIn('seo_title_en', fields)
        self.assertIn('seo_title_de', fields)
        self.assertIn('search_description_en', fields)
        self.assertIn('search_description_de', fields)
        self.assertIn('url_path_en', fields)
        self.assertIn('url_path_de', fields)

        # Check if subclass fields are being created
        self.assertIn('description_en', fields)
        self.assertIn('description_de', fields)

    def test_snippet_fields(self):
        fields = dir(models.PatchTestSnippet())

        self.assertIn('name', fields)
        self.assertIn('name_en', fields)
        self.assertIn('name_de', fields)

    def check_fieldpanel_patching(self, panels, name='name'):
        # Check if there is one panel per language
        self.assertEquals(len(panels), 2)

        # Validate if the created panels are instances of FieldPanel
        from wagtail.wagtailadmin.edit_handlers import FieldPanel
        self.assertIsInstance(panels[0], FieldPanel)
        self.assertIsInstance(panels[1], FieldPanel)

        # Check if both field names were correctly created
        fields = [panel.field_name for panel in panels]
        self.assertListEqual([name + '_de', name + '_en'], fields)

    def check_imagechooserpanel_patching(self, panels, name='image'):
        # Check if there is one panel per language
        self.assertEquals(len(panels), 2)

        from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
        self.assertIsInstance(panels[0], ImageChooserPanel)
        self.assertIsInstance(panels[1], ImageChooserPanel)

        # Check if both field names were correctly created
        fields = [panel.field_name for panel in panels]
        self.assertListEqual([name + '_de', name + '_en'], fields)

    def check_fieldrowpanel_patching(self, panels, child_name='other_name'):
        # Check if the fieldrowpanel still exists
        self.assertEqual(len(panels), 1)

        from wagtail.wagtailadmin.edit_handlers import FieldRowPanel
        self.assertIsInstance(panels[0], FieldRowPanel)

        # Check if the children were correctly patched using the fieldpanel
        # test
        children_panels = panels[0].children

        self.check_fieldpanel_patching(panels=children_panels, name=child_name)

    def check_streamfieldpanel_patching(self, panels):
        # Check if there is one panel per language
        self.assertEquals(len(panels), 2)

        from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
        self.assertIsInstance(panels[0], StreamFieldPanel)
        self.assertIsInstance(panels[1], StreamFieldPanel)

        # Check if both field names were correctly created
        fields = [panel.field_name for panel in panels]
        self.assertListEqual(['body_de', 'body_en'], fields)

        # Fetch one of the streamfield panels to see if the block was correctly
        # created
        child_block = models.StreamFieldPanelPage.body_en.field.stream_block.child_blocks.items()

        self.assertEquals(len(child_block), 1)

        from wagtail.wagtailcore.blocks import CharBlock
        self.assertEquals(child_block[0][0], 'text')
        self.assertIsInstance(child_block[0][1], CharBlock)

    def check_multipanel_patching(self, panels):
        # There are three multifield panels, one for each of the available
        # children panels
        self.assertEquals(len(panels), 3)

        from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel
        self.assertIsInstance(panels[0], MultiFieldPanel)
        self.assertIsInstance(panels[1], MultiFieldPanel)
        self.assertIsInstance(panels[2], MultiFieldPanel)

        fieldpanel = panels[0].children
        imagechooser = panels[1].children
        fieldrow = panels[2].children

        self.check_fieldpanel_patching(panels=fieldpanel)
        self.check_imagechooserpanel_patching(panels=imagechooser)
        self.check_fieldrowpanel_patching(panels=fieldrow)

    def check_inlinepanel_patching(self, panels):
        # The inline panel has all the available combination of children panels
        # making a grand total of 8 panels
        self.assertEqual(len(panels), 8)

        # The first 2 panels are fieldpanels, the following 2 are
        # imagechooserpanels, next is a fieldrowpanel and finally there are 3
        # multifieldpanels
        self.check_fieldpanel_patching(panels=panels[0:2], name='field_name')
        self.check_imagechooserpanel_patching(
            panels=panels[2:4], name='image_chooser')
        self.check_fieldrowpanel_patching(
            panels=panels[4:5], child_name='fieldrow_name')
        self.check_multipanel_patching(panels=panels[5:8])

    def test_page_patching(self):
        self.check_fieldpanel_patching(
            panels=models.FieldPanelPage.content_panels)
        self.check_imagechooserpanel_patching(
            panels=models.ImageChooserPanelPage.content_panels)
        self.check_fieldrowpanel_patching(
            panels=models.FieldRowPanelPage.content_panels)
        self.check_streamfieldpanel_patching(
            panels=models.StreamFieldPanelPage.content_panels)
        self.check_multipanel_patching(
            panels=models.MultiFieldPanelPage.content_panels)

        # In spite of the model being the InlinePanelPage the panels are patch
        # on the related model which is the PageInlineModel
        self.check_inlinepanel_patching(panels=models.PageInlineModel.panels)

    def test_snippet_patching(self):
        self.check_fieldpanel_patching(panels=models.FieldPanelSnippet.panels)
        self.check_imagechooserpanel_patching(
            panels=models.ImageChooserPanelSnippet.panels)
        self.check_fieldrowpanel_patching(
            panels=models.FieldRowPanelSnippet.panels)
        self.check_streamfieldpanel_patching(
            panels=models.StreamFieldPanelSnippet.panels)
        self.check_multipanel_patching(
            panels=models.MultiFieldPanelSnippet.panels)

        # In spite of the model being the InlinePanelSnippet the panels are
        # patch on the related model which is the SnippetInlineModel
        self.check_inlinepanel_patching(
            panels=models.SnippetInlineModel.panels)

    def test_page_form(self):
        """
        In this test we use the InlinePanelPage model because it has all the
        possible "patchable" fields so if the created form has all fields the
        form was correctly patched
        """
        try:
            from wagtail.wagtailadmin.views.pages import get_page_edit_handler, \
                PAGE_EDIT_HANDLERS
        except ImportError:
            pass

        if hasattr(models.InlinePanelPage, 'get_edit_handler'):
            page_edit_handler = models.InlinePanelPage.get_edit_handler()
        else:
            page_edit_handler = get_page_edit_handler(models.InlinePanelPage)
        form = page_edit_handler.get_form_class(models.InlinePanelPage)

        page_base_fields = [
            'slug_de', 'slug_en', 'seo_title_de', 'seo_title_en',
            'search_description_de', 'search_description_en',
            u'show_in_menus', u'go_live_at', u'expire_at'
        ]

        self.assertItemsEqual(page_base_fields, form.base_fields.keys())

        inline_model_fields = [
            'field_name_de', 'field_name_en', 'image_chooser_de',
            'image_chooser_en', 'fieldrow_name_de', 'fieldrow_name_en',
            'name_de', 'name_en', 'image_de', 'image_en', 'other_name_de',
            'other_name_en'
        ]

        related_formset_form = form.formsets['related_page_model'].form

        self.assertItemsEqual(inline_model_fields,
                              related_formset_form.base_fields.keys())

    def test_snippet_form(self):
        """
        In this test we use the InlinePanelSnippet model because it has all
        the possible "patchable" fields so if the created form has all fields
        the the form was correctly patched
        """
        from wagtail.wagtailsnippets.views.snippets import \
            get_snippet_edit_handler
        snippet_edit_handler = get_snippet_edit_handler(
            models.InlinePanelSnippet)

        form = snippet_edit_handler.get_form_class(models.InlinePanelSnippet)

        inline_model_fields = [
            'field_name_de', 'field_name_en', 'image_chooser_de',
            'image_chooser_en', 'fieldrow_name_de', 'fieldrow_name_en',
            'name_de', 'name_en', 'image_de', 'image_en', 'other_name_de',
            'other_name_en'
        ]

        related_formset_form = form.formsets['related_snippet_model'].form

        self.assertItemsEqual(inline_model_fields,
                              related_formset_form.base_fields.keys())

    def test_duplicate_slug(self):
        from wagtail.wagtailcore.models import Site
        # Create a test Site with a root page
        root = models.TestRootPage(
            title='title', depth=1, path='0001', slug_en='slug_en',
            slug_de='slug_de'
        )
        root.save()

        site = Site(root_page=root)
        site.save()

        # Add children to the root
        child = root.add_child(
            instance=models.TestSlugPage1(
                title='child1', slug_de='child', slug_en='child-en', depth=2,
                path='00010001')
        )

        child2 = root.add_child(
            instance=models.TestSlugPage2(
                title='child2', slug_de='child-2', slug_en='child2-en',
                depth=2, path='00010002')
        )

        # Clean should work fine as the two slugs are different
        child2.clean()

        # Make the slug equal to test if the duplicate is detected
        child2.slug_de = 'child'

        self.assertRaises(ValidationError, child2.clean)

    def test_searchfield_patching(self):
        # Check if the search fields have the original field plus the
        # translated ones
        expected_fields = ['title', 'title_de', 'title_en',
                           'description', 'description_de', 'description_en']

        model_search_fields = [
            searchfield.field_name
            for searchfield in models.PatchTestPage.search_fields]

        self.assertItemsEqual(expected_fields, model_search_fields)
