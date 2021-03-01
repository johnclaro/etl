#!/usr/bin/env python3

from setuptools import setup, find_packages


def get_requirements():
    with open('requirements.txt') as reqs:
        return reqs.read().splitlines()


setup(
    name='covid',
    version='1.0',
    packages=find_packages(exclude=['tests', 'tests.py']),
    install_requires=get_requirements(),
    author='John Claro',
    author_email='jkrclaro@gmail.com',
    description='ETL for Covid datasets',
    keywords='covid covid',
    url='https://github.com/johnclaro/covid.git'
)


