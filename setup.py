#! /usr/bin/env python
import os
import django_productline
from setuptools import setup, find_packages

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name='django-productline',
    version='0.3',
    description='an approach to feature-oriented software development(FOSD) of web application product lines based on django',
    long_description=read('README.rst'),
    license='The MIT License',
    keywords='django, FOSD, FOP, feature-oriented-programming, product-line, web-application',
    author='Hendrik Speidel',
    author_email='hendrik@schnapptack.de',
    url="https://github.com/henzk/django-productline",
    packages=find_packages(),
    package_dir={'django_productline': 'django_productline'},
    package_data={'django_productline': []},
    include_package_data=True,
    scripts=[],
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
    ],
    install_requires=[
        'Django',
        'decorator',
        'django-overextends',
        'south',
        'featuremonkey>=0.2.2',
        'ape>=0.2.0'
    ]
)
