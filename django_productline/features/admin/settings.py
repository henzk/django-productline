#refinement for django_productline.settings

def refine_INSTALLED_APPS(original):
    return original + ['django.contrib.admin']
