# coding: utf-8
from __future__ import unicode_literals


def refine_get_admin_urls(original):

    def new_impl():
        from django.contrib import admin
        from django.conf.urls.i18n import i18n_patterns
        admin.autodiscover()
        return i18n_patterns(*original())

    return new_impl
