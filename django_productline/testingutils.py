import os
import inspect
import importlib



def get_fixture(package_name, name):
    """
    Returns the full path of <file> within <package_name> to be used
    in Django testcase's fixtures class variable
    :param package_name:
    :param name:
    :return:
    """
    package = importlib.import_module(package_name)
    return os.path.join(os.path.dirname(inspect.getfile(package)), 'fixtures', name)


