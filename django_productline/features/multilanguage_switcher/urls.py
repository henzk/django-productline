from __future__ import unicode_literals


def refine_get_urls(original):
    def get_urls():
        from django.conf.urls import url
        from .views import ChangeLangView

        urlpatterns = [
            url(r'^activate_language', ChangeLangView.as_view(), name='activate_language')
        ]
        return urlpatterns + original()

    return get_urls
