################################
Product Generation Process
################################

Basically, product generation is a two step process (focusing on the Python side of things for now):

.. graphviz::
    :caption: Figure: High-Level overview of the product generation process

    digraph foo {
        graph [bgcolor="#F8F8F8"];
        node [fontsize=10, shape=box3d];
        
        "Product Context" [shape=note];
        "Feature Equation" [shape=note];
        "Django web application" [shape=ellipse];
        
        "Product Context" -> "Context Binding";
        "Context Binding" -> "Feature Composition";
        "Feature Equation" -> "Feature Composition";
        "Feature Composition" -> "Django web application";
    }


Product Context
    The product context contains the specific configuration of the product e.g. the database configuration and the hostname the product will be serving requests from.
    The product context is given in JSON format. Features may provide a wishlist of necessary configuration values.

Context Binding
    the product context is loaded from file and made available as ``django_productline.context.PRODUCT_CONTEXT``.
    The product context is considered to be read only --- so it may not be written to.

Feature Equation
    The list of features selected for the product in the order of composition.
    The feature equation is given as text file containing one feature per line.

Feature Composition
    After the product context has been bound, ``featuremonkey`` is used to compose the selected features.
    This results in a running django web application where introductions and refinements given by the selected features
    have been patched in.

********************************
The product context
********************************

.. automodule:: django_productline.context

********************************
Composition of application code
********************************

``featuremonkey`` is used to compose Python code.
It allows introductions of new structures and refinements of existing ones.

For some use cases in the context of ``django-productline``, see :ref:`refinements_by_example`.

Also, see the `featuremonkey documentation <http://featuremonkey.readthedocs.org>`_.


********************************
Template composition
********************************

You can use `django-overextends <https://github.com/stephenmcd/django-overextends>`_ for feature-oriented template
development. It is automatically installed as a dependency of ``django-productline``.

Now, think about it this way:

- Django apps are the *template features*
- Composition order is given in ``INSTALLED_APPS``


Example
========

Consider, we have a template called ``mytemplate.html`` in the template directory
of a django app called ``myfeature``::

    myfeature/
        templates/
            mytemplate.html
            ...
        ...


Suppose ``mytemplate.html`` looks like this::

    <html>
        <head>
            <title>{% block title %}Hello{% endblock %}</title>
        </head>
        <body>
            {% block body %}
            <h1>Hello</h1>
            {% endblock %}
        </body>
    </html>

Django templates already provide blocks, that are used for `template inheritance
<https://docs.djangoproject.com/en/dev/topics/templates/#template-inheritance>`_

``django-overextends`` provides template superimposition using the ``overextends`` tag:
To refine ``mytemplate.html``, all we need to do is to create another template with that name in
a django app that is placed before ``myfeature`` in ``INSTALLED_APPS``::

    {% overextends "mytemplate.html" %}

    {% block title %}Replacement{% endblock %}

    {% block body %}
    {{ block.super }}
    Refinements are also possible!
    {% endblock %}


Block tags are used to annotate FST-Nodes. Since blocks can be nested, we
can build feature structure trees. Nodes with the same name are superimposed, when the template
is rendered. ``{{ block.super }}`` provides access to the original implementation.

Rendering the above example, would result roughly in the following HTML document::

    <html>
        <head>
            <title>Replacement</title>
        </head>
        <body>
            <h1>Hello</h1>
            Refinements are also possible!
        </body>
    </html>


********************************
Javascript Composition
********************************

If necessary, JavaScript can be composed using ``featuremonkey.js``.
Essentially, it works the same way as ``featuremonkey``.

Have a look at the `example product line <http://featuremonkey_js.schnapptack.de/latest/example_spl/>`_
and feel free to snoop around by viewing the source in your browser.


********************************
CSS Composition
********************************

feature oriented CSS is easy:
concatenation is a pretty good composition mechanism for it.


********************************
Task Composition
********************************

``django-productline`` relies on ``ape tasks``.
Features may introduce new tasks and refine existing ones by providing a ``tasks`` module.

Please see the `ape tasks documentation <http://ape.readthedocs.org/en/latest/tasks.html>`_ for details.

Tasks contributed by ``django-productline`` are listed in :ref:`available_tasks`.
