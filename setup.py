#!/usr/bin/env python

from distutils.core import setup
from pynote import version


with open('README.rst') as f:
    long_description = f.read()

setup(name='pynote',
      version=version,
      description='Manage notes on the commandline.',
      long_description=long_description,
      author='Stefan Tatschner',
      author_email='stefan@sevenbyte.org',
      url='http://redmine.sevenbyte.org/projects/pynote',
      license='MIT',
      packages=['pynote'],
      scripts=['note', 'note-init'],
      requires=['prettytable'],
      classifiers=['Development Status :: 1 - Planning',
                   'Environment :: Console',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3.3'])
