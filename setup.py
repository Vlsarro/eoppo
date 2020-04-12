#!/usr/bin/env python

import eoppo
import os.path
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='eoppo',
    version=eoppo.__version__,
    description='The Python micro library for building embeddable object operators as wrapper classes',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Vlsarro',
    url='https://github.com/Vlsarro/eoppo',
    packages=find_packages(),
    python_requires='>=3.6',
    extras_require={
        'examples': ['torch==1.4.0', 'torchvision==0.5.0', 'numpy==1.18.2', 'Pillow==7.0.0']
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
