"""Setuptools configuration for chattools."""

from setuptools import setup
from setuptools import find_packages


with open('README.rst', 'r') as readmefile:

    README = readmefile.read()

setup(
    name='chattools',
    version='0.1.0',
    url='https://github.com/kevinconway/chattools',
    description='Demo tools for extracting metadata from chat lines.',
    author="Kevin Conway",
    author_email="kevinjacobconway@gmail.com",
    long_description=README,
    license='MIT',
    packages=find_packages(exclude=['tests', 'build', 'dist', 'docs']),
    install_requires=[
        'six',
        'requests',
        'defusedxml',
    ],
    entry_points={
        'console_scripts': [

        ],
    },
    include_package_data=True,
)
