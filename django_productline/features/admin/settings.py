#refinement for django_productline.settings

def refine_INSTALLED_APPS(original):
    return ['django_productline.features.admin', 'django.contrib.admin', ] + list(original)
    
    
introduce_ADMIN_URL = 'admin/'



def refine_TEMPLATE_CONTEXT_PROCESSORS(original):
    return list(original) + ['django_productline.features.admin.context_processors.django_admin']

