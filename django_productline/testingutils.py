from __future__ import unicode_literals
from django.test import TestCase as DjangoTestCase


def get_fixture(package_name, name):
    """
    Returns the full path of <file> within <package_name> to be used
    in Django testcase's fixtures class variable
    :param package_name:
    :param name:
    :return:
    """
    import os
    import inspect
    import importlib
    package = importlib.import_module(package_name)
    return os.path.join(os.path.dirname(inspect.getfile(package)), 'fixtures', name)


class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"

class NoMigrationsTestCase(DjangoTestCase):
    """
    Extend your test cases from this class an migrations will be disabled.
    """

    def __init__(self, *args, **kw):
        from django.conf import settings
        settings.MIGRATION_MODULES = DisableMigrations()
        super(DjangoTestCase, self).__init__(*args, **kw)




