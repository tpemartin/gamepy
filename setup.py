from setuptools import setup, find_packages

setup(
    name='gamepy',
    version='1.0.12',
    description='Description of your package',
    author='Your Name',
    packages=find_packages(),
    package_data={'gamepy': ['credentials.json']},
    include_package_data=True,
    install_requires=['google-api-python-client','google_auth_oauthlib'],
)
