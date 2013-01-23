from ape import tasks

@tasks.register
def manage(*args):
    """
    call django management tasks
    the product will be bound before the task is executed
    """
    from django_productline import startup
    from django.core.management import execute_from_command_line
    startup.select_product()
    execute_from_command_line(['ape manage'] + list(args))
