from setuptools import setup

setup(
    name='ipodify-api',
    version='1.0',
    packages=['ipodify_api'],
    install_requires=[line for line in open('requirements.txt')]
)