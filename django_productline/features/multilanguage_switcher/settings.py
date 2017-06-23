from __future__ import unicode_literals


def refine_INSTALLED_APPS(original):
    return ['django_productline.features.multilanguage_switcher'] + list(original)
