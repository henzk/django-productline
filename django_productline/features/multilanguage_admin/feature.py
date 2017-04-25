# coding: utf-8
from __future__ import unicode_literals


def select(composer):
    from . import settings
    import django_productline.settings
    composer.compose(settings, django_productline.settings)

    from . import admin_urls_refinement
    import django_productline.features.djpladmin.admin_urls
    composer.compose(admin_urls_refinement, django_productline.features.djpladmin.admin_urls)
