# First of all load and configure the django test app
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.testapp.settings")
django.setup()

# now django is configured continue ...
import pytest
from django.utils.translation import pgettext, gettext, ngettext, npgettext

from django_l10n_extensions import measures
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
    npgettext('in a forest', 'tree', 'trees', 3)
    gettext('"double quote"')
    gettext("'single quote'")
    gettext("'single quote' with escaped \"double\"")
    gettext('"double quote" with exceped \'single\'')
    count = 3
    ngettext("You bought {} apple", "You bought {} apples", count)


@pytest.fixture
def l10n_nl():
    return L10n(
        unit_distance=measures.Distance.METER,
        unit_area=measures.Area.SQUARE_METER,
        unit_volume=measures.Volume.LITER,
        unit_weight=measures.Weight.GRAM,
        unit_temp=measures.Temperature.CELSIUS,
        unit_velocity=measures.Velocity.MPS,
        unit_precipitation=measures.Precipitation.MM,
    )


@pytest.fixture
def l10n_us():
    return L10n(
        unit_distance=measures.Distance.YARD,
        unit_area=measures.Area.SQUARE_FOOT,
        unit_volume=measures.Volume.GALLON,
        unit_weight=measures.Weight.POUND,
        unit_temp=measures.Temperature.FAHRENHEIT,
        unit_velocity=measures.Velocity.MPH,
        unit_precipitation=measures.Precipitation.INCH,
    )


@pytest.fixture
def l10n_eg():
    return L10n(
        unit_distance=measures.Distance.METER,
        unit_area=measures.Area.FEDDAN,
        unit_volume=measures.Volume.LITER,
        unit_weight=measures.Weight.GRAM,
        unit_temp=measures.Temperature.CELSIUS,
        unit_velocity=measures.Velocity.MPS,
        unit_precipitation=measures.Precipitation.MM,
    )
