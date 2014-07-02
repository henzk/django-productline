
def refine_get_urls(original):
    def get_urls():
        from django.conf.urls import patterns, include
        from django.contrib import admin
        from django.conf import settings
        admin.autodiscover()
        
        # ensure that a non empty admin url has always an ending slash
        if len(settings.ADMIN_URL):
            if not settings.ADMIN_URL.endswith('/'):
                settings.ADMIN_URL += '/'
        
        return original() + patterns('',
            (r'^%s' % settings.ADMIN_URL, include(admin.site.urls)),
        )
    return get_urls
