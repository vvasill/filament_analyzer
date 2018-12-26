#!/usr/bin/env python3

from filamentyzer import __version__
from setuptools import setup, find_packages
import sys

packagename = 'filamentyzer'

with open('README.md') as fh:
	long_description = fh.read()

with open(os.path.join(here, 'requirements.txt')) as f:
    install_requires = f.read().splitlines()

setup(
    name = packagename,
    version = __version__,
    license = 'MIT',
    author = 'Vasilii Pushkarev',
    author_email='pushkarev.vv14@physics.msu.ru',
    description = 'A simple analyzer for filamentation images',
	long_description = long_description,
    packages = find_packages(),
    scripts = ['bin/test.py'],
    data_files = [
        ('doc',  ['doc/filament_analyzer.filamentyzer.html']),
     ],
     install_requires = install_requires,
     test_suite = 'test',
     keywords = 'science, filament, analyzer',
)

if __name__ == '__main__':
    setup_package()
    del builtins.__NUMPY_SETUP__
