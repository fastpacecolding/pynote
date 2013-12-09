#!/usr/bin/env python

from distutils.core import setup
from misc.version import version

setup(name='pynote',
      version=version,
      description='Manage notes on the commandline.',
      author='Stefan Tatschner',
      author_email='stefan@sevenbyte.org',
      url='http://redmine.sevenbyte.org/projects/pynote',
      license='MIT',
      packages=['misc'],
      py_modules=['note'],
      scripts=['note', 'note-init'],
      classifiers=['Development Status :: 1 - Planning',
                   'Environment :: Console',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux,',
                   'Programming Language :: Python :: 3.3'])
