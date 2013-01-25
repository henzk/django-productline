###############################################################
django-productline Feature Documentation
###############################################################

``django-productline`` should be used as a base feature.

It provides the basis to create feature oriented django product lines:

- it defines the product generation process
- it provides hooks for other features to refine to add/adapt the functionality


***********************************
Hooks provided for other features
***********************************

Refining the django settings
=============================

Many features require adaptations to the settings module used by django. ``django-productline`` always uses ``django_productline.settings`` as the django settings module.
Features can apply refinements to it, to add/adapt settings to support the features functionality.
Common cases are the refinement of ``INSTALLED_APPS`` to register one or more additional django apps and the refinement of ``MIDDLEWARE_CLASSES`` to add django middlewares.

As a simple example, we are going to create a feature called ``https_only``,
that is implemented by integrating and configuring `django-secure <http://django-secure.readthedocs.org/>`_.

First, we need to create the python package ``https_only`` by creating a folder by that name that contains an empty ``__init__.py``.
To use that package as a feature, we need to add a module called ``feature`` to it(by creating a file named ``feature.py``).
As the feature needs to refine the settings module, we also create a ``settings`` module within our package and will use the following implementation for our ``feature`` module::

    #https_only/feature.py

    def select():
        '''called if feature https_only is selected'''
        #import our settings refinement (https_only.settings)
        from . import settings
        #import the base settings
        import django_productline.settings
        #apply the refinement to the base settings
        featuremonkey.compose(settings, django_productline.settings)


The settings refinement of our feature now could look like this::

    #https_only/settings.py
    
    #add djangosecure to the end of the INSTALLED_APPS list
    def refine_INSTALLED_APPS(original):
        return original + ['djangosecure']

    #add SecurityMiddleware to the end of the MIDDLEWARE_CLASSES list
    def refine_MIDDLEWARE_CLASSES(original):
        return original + ['djangosecure.middleware.SecurityMiddleware']

    #introduce some new settings into django_productline.settings
    introduce_SESSION_COOKIE_SECURE = True
    introduce_SESSION_COOKIE_HTTPONLY = True
    introduce_SECURE_SSL_REDIRECT = True



That's it. We can now add this functionality to our products by selecting the ``https_only`` feature.

Since this feature refines INSTALLED_APPS and MIDDLEWARE_CLASSES, the composition order needs to be chosen carefully as
the web application`s behaviour is dependent on the order of their entries.

.. warning::

    Please do not simply copy the settings presented here --- consult the `django-secure documentation <http://django-secure.readthedocs.org/>`_.


Registering urlpatterns
=========================

.. automodule:: django_productline.urls


Adding WSGI Middleware
========================

If you are using special WSGI-Middleware with your django project and would like to continue to do so using ``django-productline``,
you can directly refine ``django.core.wsgi`` to acheive that.
So if your feature is called ``mywsgifeature``, you can do it as presented in the following example:

First, create a module called ``wsgi`` in ``mywsgifeature`` containing and define a refinement for ``get_wsgi_application``::

    #mywsgifeature/wsgi.py
    
    def refine_get_wsgi_application(original):
        def get_wsgi_application():
            application = original()
            from dozer import Dozer
            return Dozer(application)
        return get_wsgi_application

This refinement will add the `Dozer <http://pypi.python.org/pypi/Dozer>`_ WSGI middleware that can be used to track down memory leaks.

To use this for all products that contain ``mywsgifeature``, we need to apply the refinement in ``mywsgifeature.feature.select``::

    #mywsgifeature/feature.py

    def select():
        from . import wsgi #import our refinement
        import django.core.wsgi #import base module
        #apply refinement
        featuremonkey.compose(wsgi, django.core.wsgi)

        #apply other necessary refinements of mywsgifeature


.. note::

    If multiple features of your product line add WSGI middlewares to your application, the order in which the middlewares are applied is defined by the composition order of the selected features.


***********************************
Available tasks
***********************************


``manage``
=============

The ``manage`` task takes care of product generation and then simply forwards to django management commands.

So, just use::

    ape manage syncdb

where you used to do::

    python manage.py syncdb


***********************************
Required context data
***********************************

``django_productline`` requires the following keys in the product context:

**DATABASES**
    database configuration in the form required by `django.conf.settings.DATABASES <https://docs.djangoproject.com/en/dev/ref/settings/#databases>`_.

**SITE_ID**
    ``site_id`` to be used by django. See `django.conf.settings.SITE_ID <https://docs.djangoproject.com/en/dev/ref/settings/#site-id>`_

**DATA_DIR**
    absolute path to directory where application data will be stored.
    This directory needs to be writable by the application user.
    Data is placed in the following subfolders:
    
    - ``uploads/`` --- content uploaded by users is stored here (see `django.conf.settings.MEDIA_ROOT <https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-MEDIA_ROOT>`_)
    - ``generated_static/`` --- static files created by ``manage collectstatic`` are placed here (see `django.conf.settings.STATIC_ROOT <https://docs.djangoproject.com/en/dev/ref/settings/#static-root>`_)

**SECRET_KEY**
    see `django.conf.settings.SECRET_KEY <https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY>`_


