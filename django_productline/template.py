"""
This module encapsulate the logic to build django template settings from DJANGO_TEMPLATE_* keys
which are thanks to this module refineable as usual, because they get introduced late in select_product
after the composition process.
"""
import django
from django_productline import compare_version

def bind_settings():
    """
    Put DJANGO_TEMPLATE_* under the right settings.* name according to django-version
    :return:
    """
    from django_productline import settings

    if settings.TEMPLATE_LOADER_CACHED_ENABLED:
        loaders = [
            ['django.template.loaders.cached.Loader', settings.DJANGO_TEMPLATE_LOADERS]
        ]
    else:
        loaders = settings.DJANGO_TEMPLATE_LOADERS

    if compare_version(django.get_version(), '1.9') >= 0:

        TEMPLATES = [
            {
                'BACKEND': settings.DJANGO_TEMPLATE_BACKEND,
                'DIRS': settings.DJANGO_TEMPLATE_DIRS,
                'OPTIONS': {
                    'builtins': settings.DJANGO_TEMPLATE_BUILTINS,
                    'context_processors': settings.DJANGO_TEMPLATE_CONTEXT_PROCESSORS,
                    'loaders': loaders,
                    'debug': settings.DJANGO_TEMPLATE_DEBUG
                },
            },
        ]

        setattr(settings, 'TEMPLATES', TEMPLATES)

    else:
        setattr(settings, 'TEMPLATE_DEBUG', settings.DJANGO_TEMPLATE_DEBUG)
        setattr(settings, 'TEMPLATE_DIRS', settings.DJANGO_TEMPLATE_DIRS)
        setattr(settings, 'TEMPLATE_CONTEXT_PROCESSORS', settings.DJANGO_TEMPLATE_CONTEXT_PROCESSORS)
        setattr(settings, 'TEMPLATE_LOADERS', loaders)
