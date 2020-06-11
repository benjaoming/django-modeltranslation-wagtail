DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

DEBUG = True

SITE_ID = 1

USE_I18N = True

LANGUAGE_CODE = 'da'
LANGUAGES = [
    ('da', 'Dansk'),
    ('en', 'English'),
    ('en_AU', 'Aussie'),
    ('de', 'German'),
    ('nb', 'Norsk Bokmål'),
]

MODELTRANSLATION_FALLBACK_LANGUAGES = {
    'default': ('en', 'de',),
    'en_AU': ('en',),
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
    'taggit',    
    'test.transapp',
]
MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
USE_TZ = True
SECRET_KEY = 'kiks'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    },
]
