# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ctf-usb-keyboard-GUI',
    version='0.1.0',
    description='Usb Keyboard Parser GUI',
    long_description=readme,
    author='Capiaghi Ludovico',
    author_email='f63capia#gmail.com',
    url='https://github.com/Ludof63/CTF-USB-KEYBOARD-GUI',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

