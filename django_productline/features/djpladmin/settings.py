import django
from django_productline import compare_version


def refine_INSTALLED_APPS(original):
    return ['django_productline.features.djpladmin', 'django.contrib.admin', ] + list(original)


introduce_ADMIN_URL = 'admin/'

if (compare_version(django.get_version(), '1.9') >= 0):
    # WE use the TEMPLATES variable not prior to 1.9
    def refine_TEMPLATES(original):
        OPTIONS = original[0]['OPTIONS']
        OPTIONS['context_processors'] += [
            'django_productline.features.djpladmin.context_processors.django_admin'
        ]
        return original
else:

    def refine_TEMPLATE_CONTEXT_PROCESSORS(original):
        return list(original) + ['django_productline.features.djpladmin.context_processors.django_admin']





introduce_AUTH_GROUPS = {
    #{
    #    'name': 'Operator',
    #    'permissions': [
    #        ('add_mymodel', 'myapp'),
    #        ('change_my_model', 'myapp')
    #    ]
    #}
}
