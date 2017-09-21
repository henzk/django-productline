from __future__ import unicode_literals


def get_admin_urls():
    from django.conf.urls import include, url
    from django.contrib import admin
    from django.conf import settings
    return [url(r'^%s' % settings.ADMIN_URL, include(admin.site.urls))]
