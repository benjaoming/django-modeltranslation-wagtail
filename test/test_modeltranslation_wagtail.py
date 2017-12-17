"""
Tests for `modeltranslation_wagtail` module.
"""
from django.conf import settings
from django.test.testcases import TestCase
from django.utils import translation
from wagtail.wagtailcore.models import Page
from django.http.response import HttpResponseRedirect

from .transapp import models


class TestModeltranslation_wagtail(TestCase):

    @classmethod
    def setup_class(cls):
        pass

    def test_modeltranslation_setup(self):
        self.assertTrue(hasattr(models.Test, 'title_en'))

    def test_default_language(self):
        root = Page.get_first_root_node()
        translation.activate(settings.LANGUAGE_CODE)
        title_en = "The English Title"
        _created = models.Test(
            title=title_en,
            slug="test",
            url_path='/kiks/',
        )
        _created = root.add_child(instance=_created)
        test_object = models.Test.objects.get(id=_created.id)
        self.assertEqual(test_object.title, title_en)
        
        root_get = self.client.get("/")
        self.assertTrue(isinstance(root_get, HttpResponseRedirect))
        
        

    def test_url_routing(self):
        pass
