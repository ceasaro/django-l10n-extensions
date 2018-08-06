from setuptools import find_packages, setup

setup(
    name='django-l10n-extensions',
    version='1.0.0',
    author=u'Cees van Wieringen',
    author_email='ceesvw@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['GitPython==1.0.1', 'Django>=2', ],
    url='https://github.com/ceasaro/django-l10n-extensions',
    license='',
    description=open('DESCRIPTION').read(),
    long_description=open('README.md').read(),
    zip_safe=False,
)
