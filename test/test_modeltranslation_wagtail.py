"""
Tests for `modeltranslation_wagtail` module.
"""
import pytest


from project.transapp import models
from django.conf import settings
from django.test.testcases import TestCase
from django.utils import translation

class TestModeltranslation_wagtail(TestCase):

    @classmethod
    def setup_class(cls):
        pass

    def test_modeltranslation_setup(self):
        self.assertTrue(hasattr(models.Test, 'slug_en'))

    def test_default_language(self):
        translation.activate(settings.LANGUAGE_CODE)
        title_en = "The English Title"
        _created = models.Test.objects.create(
            title=title_en
        )
        test_object = models.Test.objects.get(id=_created.id)
        self.assertEqual(test_object.title, title_en)

    def test_url_routing(self):
        pass
