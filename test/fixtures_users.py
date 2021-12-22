import pytest

from django.contrib.auth.models import User

SINGLE_USER_USERNAME = "single_user"
SINGLE_USER_PASSWORD = "lalalalalalalala"
SINGLE_ADMIN_USERNAME = "single_admin"
SINGLE_ADMIN_PASSWORD = "lalalalalalalala"

@pytest.fixture
def single_user(db):
    user = User.objects.create_user(SINGLE_USER_USERNAME, email="user@example.org", password=SINGLE_USER_PASSWORD)
    return user


@pytest.fixture
def single_admin(db):
    user = User.objects.create_superuser(SINGLE_ADMIN_USERNAME, email="admin@example.org", password=SINGLE_ADMIN_PASSWORD)
    return user
