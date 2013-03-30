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
