#!/usr/bin/env python
from reqponse import __VERSION__

long_description = ""

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    pass

sdict = {
    'name': 'reqponse',
    'version': __VERSION__,
    'packages': ['reqponse',
                 'reqponse.adapters'],
    'zip_safe': False,
    'install_requires': ['six', 'requests'],
    'author': 'Lichun',
    'long_description': long_description,
    'url': 'https://github.com/socrateslee/reqponse',
    'classifiers': [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python']
}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if __name__ == '__main__':
    setup(**sdict)
