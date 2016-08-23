############
Installation
############

Here, setting up ``django-productline`` in `ape's container mode <http://ape.readthedocs.org/en/latest/modes.html#container-mode>`_
is described. This way, you can testdrive or develop multiple product lines isolated from the rest of your system.

If all you need is to deploy a *single* product, you can also use ``ape`` in standalone mode, as described
`here <http://ape.readthedocs.org/en/latest/install.html#installing-ape-globally>`_.

First, make sure ``virtualenv`` is installed. On Debian/Ubuntu you can install it like so::

    $ sudo apt-get install python-virtualenv

Then, create a new ``ape`` container environment and install django-productline and all dependencies::

    $ wget -O - https://raw.github.com/henzk/django-productline/master/bin/install.py | python - webapps
    
For the development version, use::

    $ wget -O - https://raw.github.com/henzk/django-productline/master/bin/install.py | python - --dev webapps


This will create a new folder called ``webapps`` with the following structure::

    webapps/
        _ape/
            venv/
            activape

.. note::

    this is a completely self contained installation. To get rid of everything or to start over, simply delete the ``webapps`` folder.


Congratulations, the installation is now complete!

SPL (software product line) containers can now be placed into the ``webapps`` directory.
Folder ``venv`` contains a ``virtualenv`` that is isolated from the system (created with the ``--no-site-packages`` option).
``ape`` and its dependencies have been installed there. If you want to use system packages, either recreate the virtualenv without the ``--no-site-packages`` option and install ``ape`` into it or
put the system packages back on ``sys.path`` using softlinks, ``.pth`` files, or path hacking.

.. note::

    ``--no-site-packages`` is the default in newer versions of ``virtualenv``. To use system packages the flag ``--system-site-packages`` needs to be specified.  


To activate container mode, change into the ``webapps`` directory and issue the following commands::

    $ . _ape/activape

Under the hood, this takes care of setting some environment variables and activating the virtualenv.



