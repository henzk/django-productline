
def refine_get_urls(original):
    """
    serve static files
    
    in production the webserver should serve requested
    static files itself and never let requests to /static/*
    get to the django application.
    """
    
    from django.conf import settings
    
    if settings.DEBUG:
        def get_urls():
            from django.contrib.staticfiles.urls import staticfiles_urlpatterns
            return original() + staticfiles_urlpatterns()
        return get_urls
    else:
        return original
