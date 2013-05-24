from django.conf import settings



def django_admin(request):
    '''
    Adds the variable boolean django_admin to context indicating whether the current 
    page is part of the django admin or not.
    
    REMEMBER: do not set ADMIN_URL='/' in case your application features functionality
    outside of django admin; otherwise all incoming urls are interpreted as admin urls.
    '''
    # ensure that adminurl always starts with a '/' but never ends with a '/'
    if settings.ADMIN_URL.endswith('/'):
        admin_url = ''.join(settings.ADMIN_URL[:-1])
    if not settings.ADMIN_URL.startswith('/'):
        admin_url = '/' + settings.ADMIN_URL
    
    # add ADMIN_URL to context
    data = {'ADMIN_URL': admin_url}
       
    if request.META['PATH_INFO'].startswith(admin_url):
        # only set django_admin in case the user is staff and the
        # current url starts with the admin url.
        data['django_admin'] = True
    else:
        data['django_admin'] = False
            
    print data
    return data
