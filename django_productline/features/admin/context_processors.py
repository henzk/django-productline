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
    
    data = {
        'ADMIN_URL': admin_url
    }
    
    if request.META['PATH_INFO'].startswith(admin_url):
        data['django_admin'] = True
    else:
        data['django_admin'] = False
        
    return data
