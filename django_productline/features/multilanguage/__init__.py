"""
django-productline multilanguage

urlpatterns are constructed by refining django_productline.urls.get_urls.

Here, get_urls and get_multilang_urls is called to get the (composed) urlpatterns.

The i18n_patterns must be defined in the root_urlconf, therefore this refinement is necessary.
This function is later called in the get_urls() of django-productline.

To make your projects urls multilanguage, you need to modify your url refinements::

    def refine_get_multilang_urls(original):

        def get_multilang_urls():
            from django.conf.urls import url
            urlpatterns = [
                url(r'foo/$', views.FooView.as_view(), name='foo'),
                url(r'bar/$', views.BarView.as_view(), name='bar')
            ]
            return original() + urlpatterns

        return get_multilang_urls


If your projects has e.g. 'en' as default language and you don't want it to
appear in the url, then set PREFIX_DEFAULT_LANGUAGE to False.

When refining get_urls using includes like this (in case you use standard django apps for example)::

    urlpatterns = original() + url(r'^', include('app.urls'))

and receive errors, you might want to access the url_patterns attribute of the include directly
as i18n_patterns() expects a list of url() instances and include returns a Resolver instance.

Like this::

    def refine_get_multilang_urls(original):

        def get_multilang_urls():
            from django.conf.urls import url, include
            # we need the url_patterns attr as this returns a list of url() instances
            urlpatterns = original() + url(r'^', include('app.urls')).url_patterns
            return urlpatterns

        return get_multilang_urls


"""
