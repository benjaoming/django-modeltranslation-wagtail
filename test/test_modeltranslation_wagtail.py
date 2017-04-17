"""
Tests for `modeltranslation_wagtail` module.
"""
import pytest

from project.transapp import models
from django.test.testcases import TestCase


class TestModeltranslation_wagtail(TestCase):

    @classmethod
    def setup_class(cls):
        pass

    def test_modeltranslation_setup(self):
        self.assertTrue(hasattr(models.Test, 'slug_en'))
