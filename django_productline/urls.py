from __future__ import unicode_literals

"""

``django_productline.urls`` exports the function ``get_urls``.
It is called through ``django_productline.root_urlconf`` which is registered as django`s ``ROOT_URLCONF``.

To introduce new urlpatterns, features may refine ``get_urls``.
The convention is to specify the refinement in a module called ``urls`` within the feature module.

Example::

    #in myfeature.feature.select()
    from . import urls #import the refinement definition
    import featuredjango.urls #import the base module
    #apply the refinement to the base module
    featuremonkey.compose(urls, featuredjango.urls)

    #in myfeature.urls
    def refine_get_urls(original):
        def get_urls():
            '''
            introduce myfeature`s views
            '''
            from django.urls import patterns
            return original() + patterns('',
                (r'^foo/$', 'myfeature.views.foo'),
                (r'^bar/(\d{4})/$', 'myfeature.views.bar'),
            )

        return get_urls

"""


def get_urls():
    """
    refine this to add urlpatterns
    """
    return []


def get_fallback_urls():
    """
    refine this to add special fallback urlpatterns.
    These urls will be appended to the end of the url patterns list (after 'get_urls()' in root_urlconf).
    E.g.:

        url(r'^foo/$', views.foo),
        url(r'^bar/(\d{4})/$', views.bar),
        # This url 'catches' all other requests which don't match the previous patterns.
        url(r'^.*', views.catch_all),

    """
    return []


handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
