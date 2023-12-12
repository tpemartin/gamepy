from setuptools import setup, find_packages

setup(
    name='gamepy',
    version='1.0.0',
    description='Description of your package',
    author='Your Name',
    packages=find_packages(),
    install_requires=['google_auth_oauthlib', 'googleapiclient'],
)
