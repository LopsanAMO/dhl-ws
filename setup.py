#!/usr/bin/env python
import setuptools
from dhl.version import Version


setuptools.setup(name='dhl-ws',
                 version=Version('1.0.0').number,
                 description='This module provides a Python client for the DHL XML Services.',  # NOQA
                 long_description=open('README.md').read().strip(),
                 author='Jonatan Rodriguez',
                 author_email='jrperdomoz@gmail.com',
                 url='https://github.com/jrperdomoz/dhl-ws',
                 py_modules=['dhl'],
                 license='MIT License',
                 zip_safe=False,
                 keywords='dhl xml webservices quote',
                 install_requires=['requests', 'jxmlease'],
                 classifiers=['Customer Service'])
