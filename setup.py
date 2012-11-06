
from setuptools import setup

setup(
    name='posthook',
    version='0.1',
    description='Postfix asynchronous smtphooks',
    author='Anthony Johnson',
    author_email='aj@ohess.org',
    packages=['posthook'],
    install_requires=[
        'gevent'
    ],
    setup_requires=[
        'nose',
        'mock'
    ],
    test_suite='posthook.tests'
)

