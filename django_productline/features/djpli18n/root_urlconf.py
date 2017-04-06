# coding: utf-8
from __future__ import unicode_literals

"""
django-productline i18n root urlconf

urlpatterns are constructed by refining django_productline.urls.get_urls.

Here, get_urls and get_i18n_patterns is called to get the (composed) urlpatterns.
The i18n_patterns must be defined in the root_urlconf, therefore this refinement is necessary.
"""

from django.conf.urls.i18n import i18n_patterns
from django_productline import urls

urlpatterns = i18n_patterns(*urls.get_urls(), prefix_default_language=True)
