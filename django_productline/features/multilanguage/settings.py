# coding: utf-8
from __future__ import unicode_literals


def refine_INSTALLED_APPS(original):
    return ['django_productline.features.multilanguage'] + list(original)

# Just make sure that the default djpl settings weren't overridden
refine_USE_I18N = True

refine_USE_L10N = True


def refine_MIDDLEWARE_CLASSES(original):
    """
    Django docs say that the LocaleMiddleware should come after the SessionMiddleware.
    Here, we make sure that the SessionMiddleware is enabled and then place the
    LocaleMiddleware at the correct position.
    Be careful with the order when refining the MiddlewareClasses with following features.
    :param original:
    :return:
    """
    try:
        session_middleware_index = original.index('django.contrib.sessions.middleware.SessionMiddleware')
        original.insert(session_middleware_index + 1, 'django.middleware.locale.LocaleMiddleware')
        return original
    except ValueError:
        raise LookupError('SessionMiddleware not found! Please make sure you have enabled the \
         SessionMiddleware in your settings (django.contrib.sessions.middleware.SessionMiddleware).')


introduce_PREFIX_DEFAULT_LANGUAGE = True
