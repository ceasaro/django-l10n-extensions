from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='django-l10n-extensions-django-3',
    version='1.0.9',
    author=u'Jon Miller',
    author_email='iamjonamiller@gmail.com',
    package_dir={'': 'src'},
    packages=find_packages(where='./src'),
    include_package_data=True,
    install_requires=['Django>=3.2.12', 'polib>=1.0'],
    url='https://github.com/iamjonmiller/django-l10n-extensions',
    license='',
    description="Extend Django 3+ with L10N features",
    long_description=long_description,
    long_description_content_type='text/markdown',
    zip_safe=False,
    key_words=['django', 'l10n', ]
)
