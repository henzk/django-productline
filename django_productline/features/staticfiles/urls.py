
def refine_get_urls(original):
    """
    serve static files
    
    in production the webserver should serve requested
    static files itself and never let requests to /static/*
    get to the django application.
    """
    
    
    
    def get_urls():
        from django.conf import settings
        from django.contrib.staticfiles.urls import staticfiles_urlpatterns
        if settings.DEBUG:
            return original() + staticfiles_urlpatterns()
        else:
            return original()
    return get_urls
