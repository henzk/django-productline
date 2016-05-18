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
def select_features():
    """
    call when product.equation changes
    """
    print '... executing select features'
    tasks.install_dependencies()
    tasks.generate_context()


@tasks.register
def install_dependencies():
    '''
    Refine this task to install feature-level dependencies. E.g. djpl-postgres
    refines this task to link psycopg2.
    '''
    pass


@tasks.register
@tasks.requires_product_environment
def deploy():
    '''
    '''
    print '... processing deploy tasks'
    tasks.create_data_dir()
    
    
@tasks.register
@tasks.requires_product_environment
def install_fixtures():
    '''
    Refines this method to enable your feature to load fixtures, either via
    ape manage loaddata or by creating objects programmatically
    '''
    pass

    

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
        print '*** Created DATA_DIR in %s' % PRODUCT_CONTEXT.DATA_DIR
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

