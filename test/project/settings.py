DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

DEBUG = True

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True


LANGUAGE_CODE = 'da'
LANGUAGES = [
    ('da', 'Dansk'),
    ('en', 'English'),
    ('en-UK', 'English UK'),
    ('de', 'German'),
    ('nb', 'Norsk Bokmål'),
]

MODELTRANSLATION_FALLBACK_LANGUAGES = {
    'default': ('en', 'de',),
    'en-UK': ('en',),
    'da': ('nb',)
}

ROOT_URLCONF = 'project.urls'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.messages',
    'modeltranslation',
    'modeltranslation_wagtail',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.contrib.sitemaps',
    'wagtail.contrib.styleguide',
    "wagtail.contrib.simple_translation",
    "modelcluster",
    'taggit',
    'test.transapp',
    'test.anotherapp',  # Tests cross-app integration
    'test.appwithoutmigrations',
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

SECRET_KEY = 'kiks'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
            ],
        },
    },
]



STATIC_URL = "/static/"
MEDIA_URL = "/static/"

WAGTAIL_SITE_NAME = "Test"

# This enables calls to user_perms.for_page(translation).can_add_subpage()
# which calls instance.refresh_from_db => translator.get_options_for_model(model)
# and this generates exceptions like the model "HomePage" is not registered for
# translation because the wrong QuerySet is used.
WAGTAIL_I18N_ENABLED = True

WAGTAIL_CONTENT_LANGUAGES = LANGUAGES

# Search
# https://docs.wagtail.io/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}
