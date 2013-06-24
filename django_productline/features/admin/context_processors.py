from django.conf import settings


def django_admin(request):
    '''
    Adds additional information to the context:

    ``django_admin`` - boolean variable indicating whether the current
    page is part of the django admin or not.
    ``ADMIN_URL`` - normalized version of settings.ADMIN_URL; starts with a slash, ends without a slash

    NOTE: do not set ADMIN_URL='/' in case your application provides functionality
    outside of django admin as all incoming urls are interpreted as admin urls.
    '''
    # ensure that adminurl always starts with a '/' but never ends with a '/'
    if settings.ADMIN_URL.endswith('/'):
        admin_url = settings.ADMIN_URL[:-1]
    if not settings.ADMIN_URL.startswith('/'):
        admin_url = '/' + settings.ADMIN_URL

    # add ADMIN_URL and django_admin to context
    data = {
        'ADMIN_URL': admin_url,
        'django_admin': request.META['PATH_INFO'].startswith(admin_url)
    }

    return data
