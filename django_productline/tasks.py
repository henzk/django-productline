from __future__ import unicode_literals, print_function, division
from ape import tasks
from decorator import decorator
import os
import json


@tasks.register_helper
@decorator # preserves signature of wrapper
def requires_product_environment(func, *args, **kws):
    """
    task decorator that makes sure that the product environment
    of django_productline is activated:
    -context is bound
    -features have been composed
    """
    from django_productline import startup
    startup.select_product()
    return func(*args, **kws)


@tasks.register
@tasks.requires_product_environment
def manage(*args):
    """
    call django management tasks
    """
    from django.core.management import execute_from_command_line
    execute_from_command_line(['ape manage'] + list(args))


@tasks.register
def select_features():
    """
    call when product.equation changes
    """
    print('... executing select features')
    tasks.install_dependencies()
    tasks.generate_context()


@tasks.register
def install_dependencies():
    """
    Refine this task to install feature-level dependencies. E.g. djpl-postgres
    refines this task to link psycopg2.
    """
    pass


@tasks.register
@tasks.requires_product_environment
def deploy():
    """
    The deploy hook.
    :return:
    """
    print('... processing deploy tasks')
    tasks.create_data_dir()


@tasks.register
@tasks.requires_product_environment
def install_fixtures():
    """
    Refines this method to enable your feature to load fixtures, either via
    ape manage loaddata or by creating objects programatically
    """
    pass


@tasks.register
@tasks.requires_product_environment
def export_data(target_path):
    """
    Exports the data of an application - media files plus database,
    :return: a zip archive
    """
    tasks.export_data_dir(target_path)
    tasks.export_database(target_path)
    tasks.export_context(target_path)
    return target_path


@tasks.register
@tasks.requires_product_environment
def export_data_dir(target_path):
    """
    Exports the media files of the application and bundles a zip archive
    :return: the target path of the zip archive
    """
    from django_productline import utils
    from django.conf import settings

    utils.zipdir(settings.PRODUCT_CONTEXT.DATA_DIR, target_path, wrapdir='__data__')
    print('... wrote {target_path}'.format(target_path=target_path))
    return target_path


@tasks.register_helper
@tasks.requires_product_environment
def get_context_path():
    """
    Get path to context.json
    :return: string - path to context.json
    """
    from django_productline.context import PRODUCT_CONTEXT
    return PRODUCT_CONTEXT.PRODUCT_CONTEXT_FILENAME


@tasks.register
def export_context(target_zip):
    """
    Append context.json to target_zip
    """
    context_file = tasks.get_context_path()
    return tasks.create_or_append_to_zip(context_file, target_zip, 'context.json')


@tasks.register_helper
def create_or_append_to_zip(file_handle, zip_path, arc_name=None):
    """
    Append file_handle to given zip_path with name arc_name if given, else file_handle. zip_path will be created.
    :param file_handle: path to file or file-like object
    :param zip_path: path to zip archive
    :param arc_name: optional filename in archive
    """
    import zipfile
    with zipfile.ZipFile(zip_path, 'a') as my_zip:
        if arc_name:
            my_zip.write(file_handle, arc_name)
        else:
            my_zip.write(file_handle)


@tasks.register
@tasks.requires_product_environment
def export_database(target_path):
    """
    Exports the database. Refine this task in your feature representing your database.
    :return:
    """
    pass


@tasks.register
@tasks.requires_product_environment
def import_database(target_path, db_name=None, db_owner=None):
    """
    Imports the database. Refine this task in your feature representing your database.
    :return:
    """
    pass


@tasks.register_helper
def get_context_template():
    """
    Features which require configuration parameters in the product context need to refine
    this method and update the context with their own data.
    """
    import random
    return {
        'SITE_ID':  1,
        'SECRET_KEY': ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)]),
        'DATA_DIR': os.path.join(os.environ['PRODUCT_DIR'], '__data__'),
    }


@tasks.register
@tasks.requires_product_environment
def create_data_dir():
    """
    Creates the DATA_DIR.
    :return:
    """
    from django_productline.context import PRODUCT_CONTEXT
    if not os.path.exists(PRODUCT_CONTEXT.DATA_DIR):
        os.mkdir(PRODUCT_CONTEXT.DATA_DIR)
        print('*** Created DATA_DIR in %s' % PRODUCT_CONTEXT.DATA_DIR)
    else:
        print('...DATA_DIR already exists.')


@tasks.register
def generate_context(force_overwrite=False, drop_secret_key=False):
    """
    Generates context.json
    """

    print('... generating context')
    context_fp = '%s/context.json' % os.environ['PRODUCT_DIR']
    context = {}

    if os.path.isfile(context_fp):
        print('... augment existing context.json')

        with open(context_fp, 'r') as context_f:
            content = context_f.read().strip() or '{}'
            try:
                context = json.loads(content)
            except ValueError:
                print('ERROR: not valid json in your existing context.json!!!')
                return

        if force_overwrite:
            print('... overwriting existing context.json')
            if drop_secret_key:
                print('... generating new SECRET_KEY')
                context = {}
            else:
                print('... using existing SECRET_KEY from existing context.json')
                context = {'SECRET_KEY': context['SECRET_KEY']}

    with open(context_fp, 'w') as context_f:
        new_context = tasks.get_context_template()

        new_context.update(context)
        context_f.write(json.dumps(new_context, indent=4))
    print()
    print('*** Successfully generated context.json')


@tasks.register
@tasks.requires_product_environment
def clear_tables_for_loaddata(confirm=None):
    """
    Clears al tables in order to loaddata properly.
    :param string:
    :return:
    """
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Permission
    from django.contrib.sites.models import Site

    if confirm != 'yes':
        print('Please enter "yes" to confirm that your want to clear ContentTypes, Sites, Permissions')
    else:
        Site.objects.all().delete()
        Permission.objects.all().delete()
        ContentType.objects.all().delete()


@tasks.register
@tasks.requires_product_environment
def inject_context(context):
    """
    Updates context.json with data from JSON-string given as param.
    :param string:
    :return:
    """
    from django_productline.context import PRODUCT_CONTEXT
    try:
        new_context = json.loads(context)
    except ValueError:
        print('Couldn\'t load context parameter')
        return
    with open(PRODUCT_CONTEXT._data['PRODUCT_CONTEXT_FILENAME']) as jsonfile:
        try:
            jsondata = json.loads(jsonfile.read())
            jsondata.update(new_context)
        except ValueError:
            print('Couldn\'t read context.json')
            return
    with open(PRODUCT_CONTEXT._data['PRODUCT_CONTEXT_FILENAME'], 'w') as jsoncontent:
        json.dump(jsondata, jsoncontent, indent=4)
