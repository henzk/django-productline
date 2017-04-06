# coding: utf-8
from __future__ import unicode_literals

"""
django-productline i18n root urlconf

urlpatterns are constructed by refining django_productline.urls.get_urls.

Here, get_urls and get_i18n_patterns is called to get the (composed) urlpatterns.
The i18n_patterns must be defined in the root_urlconf, therefore this refinement is necessary.

When refining get_urls using includes like this
    urlpatterns = original() + url(r'^', include('app.urls'))
and receive errors you might want to access the url_patterns attribute of the include directly
as i18n_patterns() expects a list of url() instances and include returns a Resolver instance.

Like this:

    def refine_get_urls(original):

        def get_urls():
            from django.conf.urls import url, include
            # we need the url_patterns attr as this returns a list of url() instances
            urlpatterns = original() + url(r'^', include('app.urls')).url_patterns
            return urlpatterns

        return get_urls
"""

from django.conf.urls.i18n import i18n_patterns
from django_productline import urls

urlpatterns = i18n_patterns(*urls.get_urls(), prefix_default_language=True)
