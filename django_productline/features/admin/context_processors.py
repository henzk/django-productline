from django.conf import settings



def django_admin(request):
    '''
    Adds the variable boolean django_admin to context indicating whether the current 
    page is part of the django admin or not.
    '''
    
    if settings.ADMIN_URL.endswith('/'):
        admin_url = ''.join(settings.ADMIN_URL[:-1])
    if not settings.ADMIN_URL.startswith('/'):
        admin_url = '/' + settings.ADMIN_URL
    
    print admin_url, request.META['PATH_INFO']
    if request.META['PATH_INFO'].startswith(admin_url):
        return {'django_admin': True}
    else:
        return {'django_admin': False}
