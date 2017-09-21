from __future__ import unicode_literals


def refine_get_urls(original):
    """
    serve static files (and media files also)

    in production the webserver should serve requested
    static files itself and never let requests to /static/*
    and /media/* get to the django application.
    """

    def get_urls():
        from django.conf.urls import url
        from django.conf import settings
        from django.contrib.staticfiles.urls import staticfiles_urlpatterns
        from django.views.static import serve
        if settings.DEBUG:
            return staticfiles_urlpatterns() + [
                url(r'^media/(?P<path>.*)$', serve, {
                    'document_root': settings.MEDIA_ROOT,
                }),
            ] + original()
        else:
            return original()
    return get_urls
