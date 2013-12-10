#!/usr/bin/env python

from distutils.core import setup
import pynote


with open('README.rst') as f:
    long_description = f.read()

setup(name='pynote',
      version=pynote.__version__,
      description='Manage notes on the commandline.',
      long_description=long_description,
      author='Stefan Tatschner',
      author_email='stefan@sevenbyte.org',
      url='http://redmine.sevenbyte.org/projects/pynote',
      license='MIT',
      packages=['pynote'],
      scripts=['note', 'note-init'],
      requires=['prettytable'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 3.3'])
