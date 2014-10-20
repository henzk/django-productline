from ape import tasks
from operator import __or__ as OR



@tasks.register
@tasks.requires_product_environment
def sync_auth_groups():
    '''
    Syncs auth groups according to settings.AUTH_GROUPS
    '''
    from django.conf import settings
    from django.contrib.auth.models import Group, Permission
    from django.db.models import Q
    
    for data in settings.AUTH_GROUPS:
        g1 = Group.objects.get_or_create(name=data['name'])[0]
        g1.permissions.clear()
        g1.save()
        args = []        
        print '*** Created group %s' % g1.name  
        for perm in data['permissions']:
            print perm
            args.append(Q(codename=perm[0], content_type__app_label=perm[1]))            
            print '   *** Created permission %s' % perm[0]

        g1.permissions.add(*list(Permission.objects.filter(
            reduce(OR, args)
        )))
              
