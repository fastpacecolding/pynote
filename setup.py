#!/usr/bin/env python

from distutils.core import setup

setup(name='pynote',
      version='0.1',
      description='Python Distribution Utilities',
      author='Stefan Tatschner',
      author_email='stefan@sevenbyte.org',
      url='',
      license='MIT',
      py_modules=['note',],
      scripts=['notes'],
      data_files=[('config', ['notesrc'])])
