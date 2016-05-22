import io
import os.path
import re
from setuptools import setup


# https://packaging.python.org/en/latest/single_source_version
def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


with open('README.rst') as f:
    long_description = f.read()


setup(
    name='pynote',
    version=find_version('note'),
    description='Manage notes on the commandline',
    long_description=long_description,
    author='Stefan Tatschner',
    author_email='rumpelsepp@sevenbyte.org',
    url='https://github.com/rumpelsepp/pynote',
    license='MIT',
    install_requires=['plaintable', 'arrow', 'pyxdg'],
    scripts=['note'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
)
