#!/usr/bin/env python

import eippm
import os.path
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='eippm',
    version=eippm.__version__,
    description='Library for creation of reusable and embeddable image processing python modules',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Vlsarro',
    url='https://github.com/Vlsarro/eippm',
    packages=find_packages(),
    python_requires='>=3.6',
    extras_require={
        'examples': ['torch==1.4.0', 'torchvision==0.5.0', 'numpy==1.18.2', 'Pillow==7.0.0']
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
