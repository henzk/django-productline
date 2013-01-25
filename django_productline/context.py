"""
the product context captures environment and configuration settings
that are specific to each product, e.g. each product requires a different
database configuration.

Use the context only for very specific stuff that NEEDS to 
be configured on a product basis.

The context is loaded from a file in json format.

"""
import json

PRODUCT_CONTEXT = None

class ContextAccessor(object):
    """
    provides nice interface to access the product context
    
    only reading is allowed! Don`t write to the context, please!
    """

    def __init__(self, data):
        """
        :param: data dict to wrap
        """
        self._data = data

    def __getattr__(self, name):
        """
        makes uppercase keys of wrapped dict available using
        dot notation
        """
        if name.isupper():
            try:
                return self._data[name]
            except KeyError:
                pass

        raise AttributeError


def bind_context(context_filename):
    """
    loads context from file and binds to it
    
    :param: context_filename absolute path of the context file
    
    called by featuredjango.startup.select_product
    prior to selecting the individual features
    """
    global PRODUCT_CONTEXT
    if PRODUCT_CONTEXT is None:
        with open(context_filename) as contextfile:
            context = json.loads(contextfile.read())
            context['PRODUCT_CONTEXT_FILENAME'] = context_filename
            PRODUCT_CONTEXT = ContextAccessor(context)
    else:
        #bind_context called but context already bound
        #harmless rebind (with same file) is ignored
        #otherwise this is a serious error
        if PRODUCT_CONTEXT.PRODUCT_CONTEXT_FILENAME != context_filename:
            raise Exception('product context bound multiple times using different data!')
