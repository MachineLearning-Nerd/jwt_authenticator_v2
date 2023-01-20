from setuptools import setup

setup(
    name='jupyterhub-jwt_authenticator-v2',
    version='2.0.3',
    description='JSONWebToken Authenticator for JupyterHub',
    url='https://github.com/MachineLearning-Nerd/jwt_authenticator_v2',
    author='ppodolsky',
    author_email='ppodolsky@me.com',
    license='Apache 2.0',
    packages=['jwtauthenticator'],
    install_requires=[
        'jupyterhub',
        'pyjwt',
    ]
)
