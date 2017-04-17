import django
import os
import sys


sys.path.append(
    os.path.dirname(__file__)
)

os.environ['DJANGO_SETTINGS_MODULE'] = "project.settings"

django.setup()