###############################################################
Installation
###############################################################

Here, setting up ``django-productline`` in `ape's container mode <http://ape.readthedocs.org/en/latest/modes.html#container-mode>`_
is described. This way, you can testdrive or develop multiple product lines isolated from the rest of your system.

If all you need is to deploy a *single* product, you can also use ``ape`` in standalone mode, as described
`here <http://ape.readthedocs.org/en/latest/install.html#installing-ape-globally>`_.

First of all, we need to create a new ``ape`` container environment::

    $ wget -O - https://raw.github.com/henzk/ape/master/bin/bootstrape | python - webapps

This will create a new folder called ``webapps`` with the following structure::

    webapps/
        _ape/
            venv/
            activape

SPL (software product line) containers can now be placed into the ``webapps`` directory.
Folder ``venv`` contains a ``virtualenv`` that is isolated from the system (created with the ``--no-site-packages`` option).
``ape`` and its dependencies have been installed there. If you want to use system packages, either recreate the virtualenv without the ``--no-site-packages`` option and install ``ape`` into it or
put the system packages back on ``sys.path`` using softlinks, ``.pth`` files, or path hacking.

.. note::

    this is a completely self contained installation. To get rid of everything or to start over, simply delete the ``webapps`` folder.


To activate container mode, issue the following command::

    $ . _ape/activape

Under the hood, this takes care of setting some environment variables and activating the virtualenv.

Now, let`s install ``django-productline`` into the virtualenv::

    $ pip install django-productline

This will also install necessary dependencies including ``Django`` and ``South``.

Congratulations, the installation is now complete!
