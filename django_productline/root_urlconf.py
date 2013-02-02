"""
django-productline root urlconf

urlpatterns are constructed by refining django_productline.urls.get_urls.

Here, get_urls is called to get the (composed) urlpatterns.
Django uses these to construct the root RegexUrlResolver.
"""
from django_productline import urls

urlpatterns = urls.get_urls()
