#!/usr/bin/env python3

from setuptools import setup, find_packages


def get_requirements():
    with open('requirements.txt') as reqs:
        return reqs.read().splitlines()


setup(
    name='etl',
    version='1.0',
    author='John Claro',
    author_email='jkrclaro@gmail.com',
    description='ETL for Covid',
    keywords='etl covid',
    url='https://github.com/johnclaro/etl.git',
    packages=find_packages(include=['etl', 'etl.*']),
    install_requires=get_requirements(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'etl=etl.cli:parse'
        ]
    }
)
