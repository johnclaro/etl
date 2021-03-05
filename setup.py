#!/usr/bin/env python3

from setuptools import setup, find_packages


def get_requirements():
    with open('requirements.txt') as reqs:
        return reqs.read().splitlines()


setup(
    name='beetle',
    version='1.0',
    author='John Claro',
    author_email='jkrclaro@gmail.com',
    description='ETL for Covid data',
    keywords='etl covid',
    url='https://github.com/johnclaro/beetle.git',
    packages=find_packages(exclude=['tests', 'tests.py']),
    install_requires=get_requirements(),
    entry_points={
        'console_scripts': [
            'beetle=cli:parse'
        ]
    }
)
