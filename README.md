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
 

# Date and time in python
**CONCEPT version**

Always work in UTC and use date / datetime aware instances

e.g. python 3
datetime.utcfromtimestamp(0).timestamp() --> -3600  # datetime instance has no timezone and python fallback on OS timezone

datetime.utcnow() is also timezone unaware
use 
datetime.utc(tz=timezone.utc)

datetime.strptime("1970-0101T00:00:00", "%Y-%m-%dT%H:%M:%S) is also timezone unaware
use
datetime.strptime("1970-0101T00:00:00", "%Y-%m-%dT%H:%M:%S).replace(tzinfo=timezone.utc)