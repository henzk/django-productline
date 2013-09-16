from ape import tasks
from decorator import decorator
import os

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
def prepare_fs():
    """
    prepare filesystem for deployment
    """
    from django_productline.context import PRODUCT_CONTEXT
    if not os.path.isdir(PRODUCT_CONTEXT.DATA_DIR):
        os.mkdir(PRODUCT_CONTEXT.DATA_DIR)


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
    tasks.prepare_fs()
    tasks.prepare_db()
    tasks.prepare_db_schema()

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
    tasks.dev()
    

def get_cookiecutter_template_dir(template_name):
    import django_productline
    if not template_name.startswith('cookiecutter'):
        print 'ERRROR: template names must start with "cookiecutter"'
        return
    
    return '%s/cookiecutters/%s' % (
        os.path.dirname(django_productline.__file__),
        template_name
    )
    

def get_location(doi):
    parts = doi.split(':')
    if len(parts) == 1:
        container_name, product_name = parts[0], None
    elif len(parts) == 2:
        container_name, product_name = parts[0], parts[1]
    else:
        print 'unable to parse context - format: <container_name>:<product_name>'
        sys.exit(1)
    
    return (container_name, product_name)
    
    
@tasks.register
def create_product(poi):
    '''
    Create a product <product_name> in <container_name>. The argument <poi> is in the form
    container_name:product_name
    '''    
    container_name, product_name = get_location(poi)
    from cookiecutter.generate import generate_files
    import uuid
    template_dir = get_cookiecutter_template_dir('cookiecutter_product')
    webapps = os.environ['APE_ROOT_DIR']
    container_dir = '%s/%s' % (webapps, container_name)
    
    if not os.path.isdir(container_dir):
        print 'ERROR: %s is not a valid container as it does not exist.' % container_dir
        return
    
    products_dir = container_dir + '/products'
    if not os.path.isdir(products_dir):
        print 'ERROR: %s must contain a "products" directory.' % container_dir
        return

    product_dir = products_dir + '/' + product_name
    if os.path.isdir(product_dir):
        print 'ERROR: the product "%s:%s" already exists. Choose another product name or delete this product and try again.' % (container_name, product_name)
        return

    generate_files(
        template_dir, 
        context=dict(
            cookiecutter={
                'product_name': product_name,
                'product_dir': product_dir,
                'secret_key': str(uuid.uuid1())
            }
        ), 
        output_dir=products_dir
    )
    print '*** Created product %s:%s' % (container_name, product_name)
    
    
@tasks.register
def create_container(container_name):
    '''
    Create a container <container_name>.
    '''
    from cookiecutter.generate import generate_files
    template_dir = get_cookiecutter_template_dir('cookiecutter_container')
    webapps = os.environ['APE_ROOT_DIR']
    container_dir = '%s/%s' % (webapps, container_name)

    if os.path.isdir(container_dir):
        print 'ERROR: %s already exists.' % container_dir
        return
    
    generate_files(
        template_dir, 
        context=dict(
            cookiecutter={
                'container_name': container_name,
            }
        ), 
        output_dir=webapps
    )
    print '*** Created container %s' % (container_name)


@tasks.register
@tasks.requires_product_environment
def create_feature(feature_name, feature_pool=None):
    '''
    Create a feature <feature_name> in the active cointainer's <feature_pool> directory.
    '''
    from cookiecutter.generate import generate_files
    from django_productline.context import PRODUCT_CONTEXT
    template_dir = get_cookiecutter_template_dir('cookiecutter_feature')
    container_dir = PRODUCT_CONTEXT.CONTAINER_DIR
    
    if feature_pool is None and 'features_incubator' in os.listdir(container_dir):
        print '*** Detected incubator pool. Will create feature there.'
        feature_pool = 'feature_incubator'
    else:
        feature_pool = 'features'
    
    pool_dir = '%s/%s' % (container_dir, feature_pool)
    if not os.path.isdir(pool_dir):
        print 'ERROR: %s does not exist' % pool_dir
        return

    feature_dir = pool_dir + '/' + feature_name
    if os.path.isdir(feature_dir):
        print 'ERROR: %s already exists.' % feature_dir
        return
    
    generate_files(
        template_dir, 
        context=dict(
            cookiecutter={
                'feature_name': feature_name,
            }
        ), 
        output_dir=pool_dir
    )
    print '*** Created feature %s in %s' % (feature_name, pool_dir)
