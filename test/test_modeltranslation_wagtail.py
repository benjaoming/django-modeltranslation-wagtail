"""
Tests for `modeltranslation_wagtail` module.
"""
import pytest

from django.conf import settings
from django.test.testcases import TestCase
from django.utils import translation
from wagtail.core.models import Page, Site
from django.http.response import HttpResponseRedirect

from .anotherapp.models import HomePage
from .transapp import models

from .fixtures_users import single_admin  # noqa
from .fixtures_users import SINGLE_ADMIN_USERNAME
from .fixtures_users import SINGLE_ADMIN_PASSWORD


def get_root():
    return Site.objects.get(is_default_site=True).root_page


class TestModeltranslation_wagtail(TestCase):

    @classmethod
    def setup_class(cls):
        pass

    def test_modeltranslation_setup(self):
        self.assertTrue(hasattr(models.Test, 'title_en'))

    def test_default_language(self):
        root = get_root()

        translation.activate("en")
        title_en = "The English Title"
        _created = models.Test(
            title=title_en,
            slug="test",
            url_path='/test/',
            field_that_is_translated="test a translation",
        )
        
        _created = root.add_child(instance=_created)
        
        test_object = models.Test.objects.get(id=_created.id)
        test_object.save()
        self.assertEqual(test_object.title, title_en)
        self.assertEqual(test_object.field_that_is_translated, test_object.field_that_is_translated_en)
        
        root_get = self.client.get("/")
        self.assertTrue(isinstance(root_get, HttpResponseRedirect))
        
    def test_not_translated(self):
        root = get_root()
        _created = models.AnotherTest(
            title="Test",
            slug="test-untranslated",
            url_path='/test-untranslated/',
        )
        
        _created = root.add_child(instance=_created)
        
        test_object = models.AnotherTest.objects.get(id=_created.id)
        self.assertEqual(test_object.title, "Test")


@pytest.mark.django_db(serialized_rollback=True)
def test_wagtail_transapp_anothertest_admin_view(client, single_admin):
    """
    Tests that we can render the creation page of "AnotherTest"
    """
    client.login(username=SINGLE_ADMIN_USERNAME, password=SINGLE_ADMIN_PASSWORD)
    response = client.get("/en/wagtail/pages/add/transapp/anothertest/3/")
    assert response.status_code == 200


@pytest.mark.django_db(serialized_rollback=True)
def test_wagtail_anotherapp_admin_view(client, single_admin):
    """
    Tests that we can render the creation page of our HomePage model
    """
    client.login(username=SINGLE_ADMIN_USERNAME, password=SINGLE_ADMIN_PASSWORD)
    response = client.get("/en/wagtail/pages/add/anotherapp/homepage/3/")
    assert response.status_code == 200


@pytest.mark.django_db(serialized_rollback=True)
def test_wagtail_transapp_inheritsfromhomepagetranslated_admin_view(client, single_admin):
    """
    Tests that we can render the creation page of "AnotherTestTranslated"
    """
    client.login(username=SINGLE_ADMIN_USERNAME, password=SINGLE_ADMIN_PASSWORD)
    response = client.get("/en/wagtail/pages/add/transapp/inheritsfromhomepagetranslated/3/")
    assert response.status_code == 200


@pytest.mark.django_db(serialized_rollback=True)
def test_wagtail_transapp_inheritsfrompagetranslated_admin_view(client, single_admin):
    """
    Tests that we can render the creation page of "AnotherTestTranslated"
    """
    client.login(username=SINGLE_ADMIN_USERNAME, password=SINGLE_ADMIN_PASSWORD)
    response = client.get("/en/wagtail/pages/add/transapp/inheritsfrompagetranslated/3/")
    assert response.status_code == 200



@pytest.mark.django_db(serialized_rollback=True)
def test_parent_page():
    """
    Tests that we can render the creation page of "AnotherTestTranslated"
    """
    home_page = HomePage.objects.get(id=3)
    home_page.get_translations().only('id', 'locale').select_related('locale')
