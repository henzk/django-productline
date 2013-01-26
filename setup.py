#! /usr/bin/env python
import os
import django_productline

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name='django-productline',
    version=django_productline.__version__,
    description='an approach to feature-oriented software development(FOSD) of web application product lines based on django',
    long_description=read('README.rst'),
    license='The MIT License',
    keywords='django, FOSD, FOP, feature-oriented-programming, product-line, web-application',
    author='Hendrik Speidel',
    author_email='hendrik@schnapptack.de',
    url="https://github.com/henzk/django-productline",
    packages=['django_productline', 
    ],
    package_dir={'django_productline': 'django_productline'},
    package_data={'django_productline': []},
    include_package_data=True,
    scripts=[],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
    ],
)
