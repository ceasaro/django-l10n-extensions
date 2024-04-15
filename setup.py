from setuptools import find_packages, setup

setup(
    name='django-l10n-extensions',
    version='1.1.1',
    author=u'Cees van Wieringen',
    author_email='ceesvw@gmail.com',
    package_dir={'': 'src'},
    packages=find_packages(where='./src'),
    include_package_data=True,
    install_requires=['GitPython==1.0.1', 'Django>=2', 'polib>=1.0'],
    url='https://github.com/ceasaro/django-l10n-extensions',
    license='',
    description=open('DESCRIPTION').read(),
    long_description=open('README.md').read(),
    zip_safe=False,
    key_words=['django', 'l10n', ]
)
