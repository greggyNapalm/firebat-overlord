#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

if not hasattr(sys, 'version_info') or sys.version_info < (2, 7, 0, 'final'):
    raise SystemExit("Firebat-manager requires Python 2.7 or later.")

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

#from firemanager import __version__

install_requirements = [
    'Flask==0.9',
    'Flask-SQLAlchemy',
    'SQLAlchemy',
    'psycopg2',
    'celery==3.0.5',
    'requests',
    'validictory',
    'PyYAML',
    'jinja2',
    'simplejson',
]

with open("README.rst") as f:
    README = f.read()

#with open("docs/changelog.rst") as f:
#    CHANGES = f.read()
CHANGES = ''

setup(
    name='firebat-overlord',
    version='0.0.1',
    author='Gregory Komissarov',
    author_email='gregory.komissarov@gmail.com',
    description='REST application to manage load tests,' +
        ' store and display results.',
    long_description=README + '\n' + CHANGES,
    license='BSD',
    url='https://github.com/greggyNapalm/firebat-overlord',
    keywords=['phantom', 'firebat'],
    #scripts=[
    #    "bin/fire",
    #    "bin/daemon_fire",
    #    "bin/fire-chart",
    #],
    packages=[
        'fireoverlord',
        'fireoverlord.test',
    ],
    package_data={
        'docs': [
            'changelog.rst',
        ],
    },
    zip_safe=False,
    install_requires=install_requirements,
    tests_require=['nose'],
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        "Topic :: Software Development :: Testing :: Traffic Generation",
    ],
)
