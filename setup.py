from setuptools import setup
import pynote

with open('README.rst') as f:
    long_description = f.read()


setup(name='pynote',
      # TODO: Fix version thing!
      version=pynote.__version__,
      description='Manage notes on the commandline',
      long_description=long_description,
      author='Stefan Tatschner',
      author_email='stefan@sevenbyte.org',
      url='https://github.com/rumpelsepp/pynote',
      license='MIT',
      packages=['pynote'],
      scripts=['note'],
      install_requires=['plaintable', 'pygments', 'babel'],
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Natural Language :: German',
                   'Programming Language :: Python :: 3.4'])
