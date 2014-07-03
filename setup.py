from setuptools import setup
import pynote

with open('README.rst') as f:
    long_description = f.read()


setup(name='pynote',
      version=pynote.__version__,
      description='Manage notes on the commandline',
      long_description=long_description,
      author='Stefan Tatschner',
      author_email='stefan@sevenbyte.org',
      url='https://github.com/rumpelsepp/pynote',
      license=pynote.__license__,
      packages=['pynote'],
      scripts=['note'],
      install_requires=['plaintable', 'babel', 'click', 'pycrypto'],
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Natural Language :: English',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.4',
      ]
)
