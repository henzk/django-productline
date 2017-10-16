from __future__ import unicode_literals


# refinement for django_productline.settings
def refine_INSTALLED_APPS(original):
    return ['django.contrib.staticfiles'] + list(original)


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
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
]


