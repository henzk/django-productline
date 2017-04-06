# coding: utf-8
from __future__ import unicode_literals


def refine_INSTALLED_APPS(original):
    return ['django_productline.features.djpli18n'] + list(original)


def refine_TEMPLATES(original):
    OPTIONS = original[0]['OPTIONS']
    OPTIONS['context_processors'] += [
        "django.template.context_processors.i18n",
    ]

    return original


introduce_LANGUAGES = [
    ('en', 'English')
]

refine_USE_I18N = True

refine_USE_L10N = True


def refine_MIDDLEWARE_CLASSES(original):
    original.insert(2, 'django.middleware.locale.LocaleMiddleware')
    return original


refine_ROOT_URLCONF = 'django_productline.features.djpli18n.root_urlconf'
