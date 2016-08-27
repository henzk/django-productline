########################################
django-productline Feature Documentation
########################################

``django-productline`` should be used as a base feature.

It provides the basis to create feature-oriented django product lines:

- it defines the product generation process
- it provides hooks for other features to refine to add/adapt the functionality


.. _refinements_by_example:

**********************
Refinements by example
**********************

This section shows some use cases and patterns to develop features for a django product line.

Refining the django settings
============================

Many features require adaptations to the settings module used by django. ``django-productline`` always uses ``django_productline.settings`` as the django settings module.
Features can apply refinements to it, to add/adapt settings to support the features functionality.
Common cases are the refinement of ``INSTALLED_APPS`` to register one or more additional django apps and the refinement of ``MIDDLEWARE_CLASSES`` to add django middlewares.

As a simple example, we are going to create a feature called ``https_only``,
that is implemented by integrating and configuring `django-secure <http://django-secure.readthedocs.org/>`_.

First, we need to create the python package ``https_only`` by creating a folder with that name that contains an empty ``__init__.py``.
As the feature needs to refine ``django_productline.settings``, we also create a ``settings`` module within the package::

    https_only/
        __init__.py
        settings.py

Let's use the following settings refinement::

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

This adds ``djangosecure`` to the list of installed apps and adds the middleware it depends on.
Also, it introduces some security related settings.

.. warning::

    Before using this in production, please consult the `django-secure documentation <http://django-secure.readthedocs.org/>`_.

Now, we need to make sure the settings refinement is applied, when feature ``https_only`` is bound:

To use ``https_only`` as a feature, we need to add a module called ``feature`` to it.
Let's create ``feature.py`` with the following content::

    #https_only/feature.py

    def select(composer):
        '''bind feature https_only'''
        #import settings refinement (https_only.settings)
        from . import settings
        #import project settings
        import django_productline.settings
        #apply the refinement to the project settings
        composer.compose(settings, django_productline.settings)

This applies our settings refinement, when the feature is bound.
We can now add the functionality to products by selecting the ``https_only`` feature.

Since this feature refines INSTALLED_APPS and MIDDLEWARE_CLASSES,
the composition order needs to be chosen carefully as
the web application`s behaviour is dependent on the order of their entries.


Registering urlpatterns
=======================

.. automodule:: django_productline.urls


Django Model composition
========================

Django already provides an excellent database modularisation mechanism using apps.
An app may contain multiple models, i.e. ORM-managed database tables.
However, there is no easy way to introduce fields into existing models.

``featuremonkey`` introductions will not work because of the custom metaclass used by django models, that takes
care of additional book-keeping during construction of the model class.
As introductions are applied after the class has been constructed, the book-keeping code
is not executed in this case.

Fortunately, django provides a mechanism that takes care of the book-keeping even for
attributes that are added after the class is constructed: model fields and managers provide a ``contribute_to_class``
method.

To make use of that, ``django_productline`` extends the composer to also support another operation called ``contribute``.
It can be used just like ``introduce`` except that it does not support callable introductions.
Under the hood, it calls ``contribute_to_class`` instead of ``setattr`` which enables the introduction of fields to models.

Field Introduction Example
--------------------------

Let's look at an example. Suppose you are working on a todo list application.
Then, some clients want an additional description field for their todo items, but others don't.
So, you decide to create a feature to add that field conditionally.

Suppose the todo item model lives in ``todo.models`` and looks like this::

    # todo/models.py
    from django.db import models

    class TodoItem(models.Model):
        name=models.CharField(max_length=100)
        done=models.BooleanField()


Now, let's create a feature called ``todo_description``::

    todo_description/
        __init__.py
        feature.py
        todo_models.py

Let's write a refinement for the ``todo.models`` module and place it in ``todo_models.py``::

    #todo_description/todo_models.py
    #refines todo/models.py
    from django.db import models

    class child_TodoItem(object):
        contribute_description = models.TextField

Please note, that we are using ``contribute`` instead of ``introduce`` to let django do its model magic.

Next, let's apply the refinement in the feature binding function::

    #todo_description/feature.py

    def select(composer):
        compose_later(
            'todo_description.todo_models',
            'todo.models'
        )

That was it. The description field can now be added by selecting feature ``todo_description``.
Obviously, since there is a database involved, the schema needs to be created or modified if it exists already.

If the database table for todo items does not exist already, the field is automatically created in the database upon ``syncdb``

If the table exists already, because the product has been run before selecting feature ``todo_description``,
we can use south to do a ``schemamigration``::

    $ ape manage schemamigration todo --auto
    $ ape manage migrate todo


To compose models, we need to use ``compose_later`` as importing ``django.db.models`` starts up all the django initialization machinery as a side effect.
At this point, this could result in references to partially composed objects and hard to debug problems.

To prevent you from importing these parts of django by accident, ``django_productline`` uses import guards for specific modules during composition.
After all features are bound, those guards are dropped again and importing the modules is possible again.

The guarded packages/modules currently are:

- ``django.conf``
- ``django.db``



Adding WSGI Middleware
======================

If you are using special WSGI-Middleware with your django project and would like to continue to do so using ``django-productline``,
you can directly refine ``django.core.wsgi`` to achieve that.
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

    def select(composer):
        from . import wsgi #import our refinement
        import django.core.wsgi #import base module
        #apply refinement
        composer.compose(wsgi, django.core.wsgi)

        #apply other necessary refinements of mywsgifeature


.. note::

    If multiple features of your product line add WSGI middlewares to your application, the order in which the middlewares are applied is defined by the composition order of the selected features.


.. _available_tasks:

***************
Available tasks
***************

(All of these commands are issued by entering ``ape`` + commandname )


Product-Lifecycle tasks
=======================

``install_container <containername>``    
    install a container into the development environment.


``select_features``
    selects and activates the features that are listed in the product equation if run. This needs to be called on every first startup of the environment.

``deploy``
    deploy the selected application to the server

From this point forward you can use the ``ape manage`` commands which are similar to the ``python manage.py``
commands from pythons virtualenv.


Container selection tasks
=========================

``cd <target directory>``
    change into target directory

``zap``
    This changes the focus on the previously installed container. The first argument is the name of the container
    itself, the second one is the context in which the container is setup. In detail this changes some things
    in the product equation, e.g. to provide different setups for productive or development setups. Usually
    these products are ``website_dev`` respectively ``website_prod``. They can be looked up by taking the
    directory names from ``/dev``


``zap <containername>:<product>``
    alias for "teleport". Use this the following way:
    ``ape zap <containername>:<product>`` like:
    ``ape zap slimcontent:sample_dev`` or similar

``switch <target>``
    switch the context to the specified target.

``teleport <dir target>``
    change the directory and switch to the target inside this directory



Further available ape commands
==============================

``dev()``
    starts up the development server. This is equal to ``ape manage runserver``.
    Runserver optionally accepts an IP- Adress as an argument to run the dev server on a
    custom IP- Adress. If the server is started under ``0.0.0.0:<PORT>`` it exposes ``<PORT>`` to the
    LAN under ``<IP- Adress of devmachine>:<PORT>``.
    This is useful for sharing development states amongst diferrent machines e.g. for mobile
    development similar tasks.

``help(task)``
    prints details about available tasks

``info()``
    prints information about the development environment

``manage <...args>``
    calls django-specific management tasks. This is equal to django's default
    ``python manage.py`` - command.

``prepare``
    prepares a product for deployment. This is a combo command that runs the following
    three comands prefixed with ``prepare_`` in order of appearance here.
    Under the hood this runs tasks such as:
        - setting up the database and database schema
        - generating the webserver configuration
        - basically everything that's necessary for the server to run your app

    **must be executed every time after feature selection and/or changes of the product context**

``prepare_db``
    Creates the database, prepares it for sync. By default this does nothing but can be refined by certain features to accomplish specific database creation tasks

``prepare_db_schema``
    This is a combo command that runs ``syncdb`` and applies database migrations afterwards

``prepare_fs``
    Prepares the filesystem for deployment. If you use the base implementation this creates the data dir.

``requires_product_environment``
    Task decorator that checks if the product environment of django-productline is activated which is necessary for the environment to run. Specifically it checks whether:
    - context is bound
    - features have been composed

``manage``
    Calls fundamental Django management tasks

``deploy``
    the base implementation delegates to the ``dev`` task.Features may refine this to add support for mod_wsgi,uwsgi,gunicorn,...


*********************
Required context data
*********************

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
