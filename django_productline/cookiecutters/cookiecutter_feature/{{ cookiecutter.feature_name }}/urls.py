


def refine_get_urls(original):

    def get_urls():
        from django.conf.urls.defaults import url, patterns, include
        urlpatterns = patterns('',
            # place your feature's urls here
        )
        return urlpatterns + original()
    return get_urls
