#refinement for django_productline.settings

def refine_INSTALLED_APPS(original):
    return ['django_productline.features.admin', 'django.contrib.admin', ] + list(original)
