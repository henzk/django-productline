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
    The feature equation is given as text-file containing one feature per line.

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


********************************
Template composition
********************************

********************************
Javascript Composition
********************************

********************************
CSS Composition
********************************

********************************
Task Composition
********************************


