# coding: utf-8
from __future__ import unicode_literals


def refine_get_admin_urls(original):

    def new_impl():
        from django.contrib import admin
        from django.conf import settings
        from django.conf.urls.i18n import i18n_patterns
        admin.autodiscover()
        if settings.MULTILANGUAGE_ADMIN:
            return i18n_patterns(*original())
        else:
            return original()

    return new_impl
