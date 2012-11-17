
from setuptools import setup

setup(
    name='posthook',
    version='0.1',
    description='SMTP hooks via SMTPServer and Postfix policy server',
    author='Anthony Johnson',
    author_email='aj@ohess.org',
    packages=['posthook', 'posthook.provider', 'posthook.tests'],
    install_requires=[
        'gevent'
    ],
    setup_requires=[
        'nose',
        'mock'
    ],
    test_suite='posthook.tests'
)

