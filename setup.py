#!/usr/bin/env python
"""
Install django-externalfiles using setuptools
"""

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='django-externalfiles',
    version="0.1.0",
    description='Serve files from outside the Django MEDIA_ROOT in a secure manner',
    author='Ionata Web Solutions',
    author_email='webmaster@ionata.com.au',
    url='https://bitbucket.org/ionata/django-externalfiles',

    install_requires=['Django>=1.4'],
    zip_safe=False,

    packages=find_packages(),

    include_package_data=True,
    package_data={ },

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
