
def refine_get_urls(original):
    def get_urls():
        from django.conf.urls import patterns, include
        from django.contrib import admin

        admin.autodiscover()

        return original() + patterns('',
            (r'^admin/', include(admin.site.urls)),
        )
    return get_urls
