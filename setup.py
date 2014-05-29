import os
import re
from setuptools import setup


# https://packaging.python.org/en/latest/tutorial.html#version
def find_version(*file_paths):
    here = os.path.abspath(os.path.dirname(__file__))
    version_file = open(os.path.join(here, *file_paths), 'r').read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]'",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


with open('README.rst') as f:
    long_description = f.read()


setup(name='pynote',
    version=find_version('pynote', '__init__.py'),
    description='Manage notes on the commandline',
    long_description=long_description,
    author='Stefan Tatschner',
    author_email='stefan@sevenbyte.org',
    url='https://github.com/rumpelsepp/pynote',
    license='MIT',
    packages=['pynote'],
    scripts=['note'],
    data_files=[('share/man/man5', ['doc/man/noterc.5'])],
    install_requires=['plaintable', 'pygments'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Console',
                 'License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Natural Language :: German',
                 'Programming Language :: Python :: 3.4'])
