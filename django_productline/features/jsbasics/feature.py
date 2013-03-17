
from __future__ import absolute_import

def select(composer):
    #compose settings
    import django_productline.settings
    from . import settings
    composer.compose(settings, django_productline.settings)

