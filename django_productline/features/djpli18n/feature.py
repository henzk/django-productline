# coding: utf-8
from __future__ import unicode_literals


def select(composer):
    from . import settings
    import django_productline.settings
    composer.compose(settings, django_productline.settings)
