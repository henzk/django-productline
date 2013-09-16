

def select(composer):
    from . import settings
    import django_productline.settings
    composer.compose(settings, django_productline.settings)
    
    from . import urls
    import django_productline.urls
    composer.compose(urls, django_productline.urls)
