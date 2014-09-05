"""
product initialization stuff
"""
import os, re
import featuremonkey
from .composer import get_composer

_product_selected = False


def cmp_version(version1, version2):
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
    return cmp(normalize(version1), normalize(version2))

def select_product():
    """
    binds the frozen context the selected features

    should be called only once - calls after the first call have
    no effect
    """
    global _product_selected
    if _product_selected:
        #tss already bound ... ignore
        return

    _product_selected = True
    from django_productline import context

    featuremonkey.add_import_guard('django.conf')
    featuremonkey.add_import_guard('django.db')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_productline.settings'
    contextfile = os.environ['PRODUCT_CONTEXT_FILENAME']
    equationfile = os.environ['PRODUCT_EQUATION_FILENAME']
    #bind context and compose features
    context.bind_context(contextfile)
    get_composer().select_equation(equationfile)
    featuremonkey.remove_import_guard('django.conf')
    featuremonkey.remove_import_guard('django.db')

    import django
    if cmp_version(django.get_version(), '1.7') >= 0:
        django.setup()
    #force import of settings and urls
    #better fail during initialization than on the first request
    from django.conf import settings
    from django.core.urlresolvers import get_resolver
    #eager creation of URLResolver
    get_resolver(None)

    #make sure overextends tag is registered
    from django.template.loader import get_template
    from overextends import models
    

def get_wsgi_application():
    """
    returns the wsgi application for the selected product

    this function is called by featuredjango.wsgi to get the wsgi
    application object

    if you need to refine the wsgi application object e.g. to add
    wsgi middleware please refine django.core.wsgi.get_wsgi_application directly.
    """
    #make sure the product is selected before importing and constructing wsgi app
    select_product()
    #return (possibly refined) wsgi application
    from django.core.wsgi import get_wsgi_application
    return get_wsgi_application()
