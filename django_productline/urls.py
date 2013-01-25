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
