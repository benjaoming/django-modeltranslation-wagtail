#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()

setup(
    name='django-modeltranslation-wagtail',
    version='0.4',
    description='The glue between django-modeltranslation and wagtail',
    long_description=readme,
    author='Benjamin Bach',
    author_email='benjamin@overtag.dk',
    url='https://github.com/benjaoming/django-modeltranslation-wagtail',
    packages=[
        'modeltranslation_wagtail',
    ],
    package_dir={'modeltranslation_wagtail': 'modeltranslation_wagtail'},
    include_package_data=True,
    install_requires=[
        'wagtail>=2.0',
        'django-modeltranslation>=0.12',
    ],
    license='MIT',
    zip_safe=False,
    keywords='modeltranslation_wagtail',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Django',
        'Topic :: Software Development :: Internationalization',
    ],
)
