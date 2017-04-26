# First of all load and configure the django test app
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.testapp.settings")
django.setup()

# now django is configured continue ...
import pytest
from django.utils.translation import pgettext, gettext, ngettext

from django_l10n_extensions.models import measures
from django_l10n_extensions.models.models import L10n


def _reload(instance):
    """
    :param instance: a django model instance
    :return: a refreshed instance of the same django model instance
    """
    return type(instance).objects.get(pk=instance.pk)


def setup_translations():
    gettext('edit')
    pgettext('season', 'spring')
    pgettext('mechanical device', 'spring')
    gettext('"double quote"')
    gettext("'single quote'")
    gettext("'single quote' with escaped \"double\"")
    gettext('"double quote" with exceped \'single\'')
    count = 3
    ngettext("You bought {} apple", "You bought {} apples", count)


@pytest.fixture
def l10n_nl():
    return L10n(unit_area=measures.Area.HECTARE,
                unit_distance=measures.Distance.METER,
                unit_temp=measures.Temperature.CELSIUS,
                unit_windspeed=measures.Speed.MPS,
                unit_precipitation=measures.Precipitation.MM,
                unit_volume=measures.Volume.LITER,
                unit_mass=measures.Mass.KG,
                )


@pytest.fixture
def l10n_us():
    return L10n(unit_area=measures.Area.ACRE,
                unit_distance=measures.Distance.FOOT,
                unit_temp=measures.Temperature.FAHRENHEIT,
                unit_windspeed=measures.Speed.MPH,
                unit_precipitation=measures.Precipitation.INCH,
                unit_volume=measures.Volume.GALLON,
                unit_mass=measures.Mass.POUND,
                )


@pytest.fixture
def l10n_eg():
    return L10n(unit_area=measures.Area.FEDDAN,
                unit_distance=measures.Distance.METER,
                unit_temp=measures.Temperature.CELSIUS,
                unit_windspeed=measures.Speed.MPS,
                unit_precipitation=measures.Precipitation.MM,
                unit_volume=measures.Volume.LITER,
                unit_mass=measures.Mass.KG,
                )
