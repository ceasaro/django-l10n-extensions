# Django L10N extensions
Django L10N extensions adds some useful L10N extensions to the Django framework

The project in maintained on [github](https://github.com/ceasaro/django-l10n-extensions)

[Read the docs](http://django-l10n-extensions.readthedocs.io)


 ## Create new distribution
 To create a new distribution from this package follow these steps:
 1) create new virualenv met python 3 `mkvirtualenv -p /usr/bin/python3 django-l10n-extensions`
 2) install requirements `pip install -r setup/requirements.txt`
 3) update the version in `./setup.py`, otherwise you will overwrite an already existing version. 
 4) Make a new distribution run: `python setup.py sdist bdist_wheel`
 5) Optional upload to pypi TEST: `twine upload --repository-url https://test.pypi.org/legacy/ dist/*` 
 
 to upload to PRODUCTION remove the `--repository-url` argument (make sure your local `~/.pypirc` is correct)
 