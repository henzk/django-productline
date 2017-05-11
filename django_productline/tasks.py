from __future__ import unicode_literals, print_function, division
from ape import tasks
from decorator import decorator
import os
import featuremonkey
import json
import zipfile
import shutil


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
def prepare():
    """
    Prepare filesystem(create_data_dir), database(migrate), services and data (may load fixture)
    :return:
    """
    tasks.prepare_fs()
    tasks.prepare_db()
    tasks.prepare_services()
    tasks.prepare_data()


@tasks.register_helper
def prepare_fs():
    """
    Creates data dir etc.
    :return:
    """
    tasks.create_data_dir()


@tasks.register_helper
def prepare_db():
    """
    Set up database, e.g. migrate
    :return:
    """
    tasks.manage("migrate")


@tasks.register_helper
def prepare_services():
    """
    Set up services
    :return:
    """
    pass


@tasks.register_helper
def prepare_data():
    """
    May install fixture, needs to decide if this shall happen
    :return:
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
    tasks.djpl_compilemessages()


@tasks.register
@tasks.requires_product_environment
def djpl_compilemessages():
    """
    Compile messages hook for django_productline, this task checks for the activated languages
    in settings.LANGUAGES. It runs the standard django compilemessages management command with the -l parameter.
    Example language setting:
        LANGUAGES = [
            ('en', 'English'),
            ('de', 'Deutsch')
        ]
    Remarks:
        - Each argument for the management command MUST be a single list item, e.g. ['compilemessages', '--locale', 'en']
        - The compilemessages command MUST be executed in the projects root dir, so the CWD is adjusted before running this command.
    :return:
    """
    from django.conf import settings
    if hasattr(settings, 'LANGUAGES') and len(settings.LANGUAGES) > 0:
        # changing cwd to project root
        os.chdir(os.path.join(os.environ['APE_ROOT_DIR'], os.environ['CONTAINER_NAME']))
        languages = list()
        # collect the language abbreviations
        for language in settings.LANGUAGES:
            languages.append(language[0])
        args = ['compilemessages']
        # extend the arg list by the -locale argument for each language
        for lang in languages:
            args.extend(['--locale', str(lang)])
        tasks.manage(*args)


@tasks.register
@tasks.requires_product_environment
def export_data(target_path):
    """
    Exports the data of an application - media files plus database,
    :param: target_path:
    :return: a zip archive
    """
    tasks.export_data_dir(target_path)
    tasks.export_database(target_path)
    tasks.export_context(target_path)
    return target_path

@tasks.register
@tasks.requires_product_environment
def import_data(target_zip):
    """
    Import data from given zip-arc, this means database + __data__
    :param target_zip:
    :param backup_zip_path:
    :return:
    """
    from django_productline.context import PRODUCT_CONTEXT
    tasks.import_data_dir(target_zip)
    # product context is not reloaded if context file is changed
    tasks.import_database(target_zip, PRODUCT_CONTEXT.DB_NAME, PRODUCT_CONTEXT.DB_USER)


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


@tasks.register
@tasks.requires_product_environment
def import_data_dir(target_zip):
    """
    Remove whole old data dir, use __data__ from target_zip
    :param target_zip:
    :return:
    """
    from django_productline.context import PRODUCT_CONTEXT
    shutil.rmtree(PRODUCT_CONTEXT.DATA_DIR)
    z = zipfile.ZipFile(target_zip)

    def filter_func(x):
        return x.startswith('__data__/')

    z.extractall(os.path.dirname(PRODUCT_CONTEXT.DATA_DIR), filter(filter_func, z.namelist()))


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
    from django_productline import utils
    context_file = tasks.get_context_path()
    return utils.create_or_append_to_zip(context_file, target_zip, 'context.json')


@tasks.register_helper
def import_context(target_zip):
    """
    Overwrite old context.json, use context.json from target_zip
    :param target_zip:
    :return:
    """
    context_path = tasks.get_context_path()
    with zipfile.ZipFile(target_zip) as unzipped_data:
        with open(context_path, 'w') as context:
            context.write(unzipped_data.read('context.json'))


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
def import_database(target_path, db_name, db_owner):
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
def inject_context(context):
    """
    Updates context.json with data from JSON-string given as param.
    :param context:
    :return:
    """
    context_path = tasks.get_context_path()
    try:
        new_context = json.loads(context)
    except ValueError:
        print('Couldn\'t load context parameter')
        return
    with open(context_path) as jsonfile:
        try:
            jsondata = json.loads(jsonfile.read())
            jsondata.update(new_context)
        except ValueError:
            print('Couldn\'t read context.json')
            return
    with open(context_path, 'w') as jsoncontent:
        json.dump(jsondata, jsoncontent, indent=4)


@tasks.register
@tasks.requires_product_environment
def write_composer_operation_log(filename):
    """
    Writes the composed operation log from featuremonkey's Composer to a json file.
    :param filename:
    :return:
    """
    from featuremonkey.composer import OPERATION_LOG
    fop_data = json.dumps(OPERATION_LOG, indent=4)
    with open(filename, 'w+') as meta_file:
        meta_file.write(fop_data)


@tasks.register
@tasks.requires_product_environment
def run_product_tests(*args):
    """
    Runs tests for the features that are activated in the product equation.
    Example: $ ape runfeaturetests -r -v=2
    """
    features = featuremonkey.get_features_from_equation_file(os.environ['PRODUCT_EQUATION_FILENAME'])
    base_args = ['test'] + features
    args = base_args + list(args)
    tasks.manage(*args)
