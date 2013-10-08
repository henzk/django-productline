from ape import tasks
from decorator import decorator
import os
import importlib
from featuremonkey.composer import get_features_from_equation_file
import json

@tasks.register_helper
@decorator#preserves signature of wrappee
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
@tasks.requires_product_environment
def select_features():
    """
    call when product.equation changes
    """
    pass


@tasks.register
def prepare_db():
    """
    create the database
    """
    #the base feature assumes sqlite
    #or that the database is managed manually
    #other features can easily add support for
    #a specific database server and creation mechanism
    #by refining this task
    pass


@tasks.register
def prepare_db_schema():
    """
    create the database schema
    """
    tasks.manage('syncdb', '--noinput')
    tasks.manage('migrate')


@tasks.register
@tasks.requires_product_environment
def prepare():
    """
    prepare product for deployment

    does stuff like:
    -setting up the db and schema
    -generate webserver config
    ... everything to get the web application setup

    must be rerun after feature selection and/or the
    product context is changed
    """
    tasks.create_data_dir()


@tasks.register
def dev():
    """
    run the development server
    """
    tasks.manage('runserver')


@tasks.register
def deploy():
    """
    deploy application
    """
    #other features may add support for mod_wsgi, uwsgi, gunicorn,...
    #by _replacing_ this method
    tasks.generate_context()
    tasks.prepare()


@tasks.register_helper
def get_context_template():
    '''
    Features which require configuration parameters in the product context need to refine
    this method and update the context with their own data.
    '''
    import random
    return {
        'SITE_ID':  1,
        'SECRET_KEY': ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)]),
        'DATA_DIR': os.path.join(os.environ['PRODUCT_DIR'], '__data__'),
    }


@tasks.register
@tasks.requires_product_environment
def create_data_dir():
    '''
    Creates the DATA_DIR.
    '''
    from django_productline.context import PRODUCT_CONTEXT
    if not os.path.exists(PRODUCT_CONTEXT.DATA_DIR):
        os.mkdir(PRODUCT_CONTEXT.DATA_DIR)
        print '*** Created DATA_DIR in %s' % settings.DATA_DIR
    else:
        print '... skipping. DATA_DIR already exists.'


@tasks.register
def generate_context(force_overwrite=False, drop_secret_key=False):
    '''
    Generates context.json
    '''

    print '... generating context'
    context_fp = '%s/context.json' % os.environ['PRODUCT_DIR']
    context = {}

    if os.path.isfile(context_fp):
        print '... augment existing context.json'

        with open(context_fp, 'r') as context_f:
            content = context_f.read().strip() or '{}'
            try:
                context = json.loads(content)
            except ValueError:
                print 'ERROR: not valid json in your existing context.json!!!'  
                return

        if force_overwrite:
            print '... overwriting existing context.json'
            if drop_secret_key:
                print '... generating new SECRET_KEY'
                context = {}
            else:
                print '... using existing SECRET_KEY from existing context.json'
                context = {'SECRET_KEY': context['SECRET_KEY']}

    with open(context_fp, 'w') as context_f:
        new_context = tasks.get_context_template()

        new_context.update(context)
        context_f.write(json.dumps(new_context, indent=4))
    print 
    print '*** Successfully generated context.json'

