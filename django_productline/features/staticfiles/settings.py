#refinement for django_productline.settings

def refine_INSTALLED_APPS(original):
    return ['django.contrib.staticfiles'] + list(original)

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
from django_productline.context import PRODUCT_CONTEXT
introduce_STATIC_ROOT = PRODUCT_CONTEXT.DATA_DIR + '/generated_static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
introduce_STATIC_URL = '/static/'

# Additional locations of static files
introduce_STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
]

# List of finder classes that know how to find static files in
# various locations.
introduce_STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
]


