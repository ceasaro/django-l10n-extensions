# coding=utf-8
import pytest

from django_l10n_extensions.l10n_threading import activate as activate_l10n, deactivate as deactivate_l10n
from django_l10n_extensions.measures import Distance, Area

from tests.conftest import _reload
from tests.testapp.models import MeasuresTestModel


@pytest.mark.django_db
def test_area(l10n_nl):
    activate_l10n(l10n_nl)
    units = MeasuresTestModel.objects.create(area=240000, height=43, temp=18)
    units = _reload(units)
    assert units.area.sq_m == 240000
    assert units.area.ha == 24
    assert units.area.hectare == 24
    assert units.area.l10n == '240000.0 sq_m'
    assert units.area.as_l10n(decimal_pos=0) == '240000 sq_m'
    assert units.area.default_value == 240000
    assert units.height.default_value == 43


@pytest.mark.django_db
def test_distance(l10n_nl):
    activate_l10n(l10n_nl)
    units = MeasuresTestModel.objects.create(area=24, height=43, temp=18)
    units = _reload(units)
    assert units.height.m == 43
    assert units.height.meter == 43
    assert units.height.cm == 4300
    assert abs(units.height.ft - 141.076) < 0.001
    assert abs(units.height.foot - 141.076) < 0.001

    units.height = Distance(m=11)
    units.save()
    units = _reload(units)
    assert units.height.m == 11
    assert units.height.metre == 11


@pytest.mark.django_db
def test_temperature(l10n_nl, l10n_us):
    activate_l10n(l10n_nl)
    units = MeasuresTestModel.objects.create(area=Area(ha=24), height=43, temp=18)
    units = _reload(units)
    assert units.temp.C == 18.0
    assert units.temp.F == 64.4

    # change language, punctuation should alter
    units.temp = 0
    units.save()
    units = _reload(units)
    assert units.temp.Celsius == 0
    assert units.temp.F == 32

    activate_l10n(l10n_us)
    units.temp = 8  # 8 °F
    units.save()
    units = _reload(units)
    assert abs(units.temp.F - 8.00) < 0.01
    assert abs(units.temp.Celsius - -13.33) < 0.01
    deactivate_l10n()


@pytest.mark.django_db
def test_store():
    units = MeasuresTestModel.objects.create(area=Area(ha=1))
    units = _reload(units)
    assert units.area.ha == 1
    assert units.area.sq_km == 0.01

    units.area = 20000
    units.save()
    units = _reload(units)
    assert units.area.ha == 2
    assert units.area.sq_km == 0.02

    units.area = Area(ha=3)
    units.save()
    units = _reload(units)
    assert units.area.ha == 3
    assert units.area.sq_km == 0.03


@pytest.mark.django_db
def test_store_l10n(l10n_us):
    # set country to US, so values are stored in non default units.
    activate_l10n(l10n_us)
    # store values in the currently active unit.
    units = MeasuresTestModel.objects.create(area=1045462.7681142587, height=43, temp=0)
    units = _reload(units)
    assert abs(units.area.acre - 24) < 0.0001
    assert abs(units.area.ha - 9.7127) < 0.0001
    assert units.height.yard == 43
    assert abs(units.height.m - 39.3192) < 0.001
    assert abs(units.temp.F - 0.00) < 0.01
    assert abs(units.temp.C - -17.78) < 0.01
    # default values should return the value of the default unit.
    assert abs(units.area.default_value - 97126.66936) < 0.0001
    assert abs(units.height.default_value - 39.3192) < 0.01
    assert abs(units.temp.default_value - -17.78) < 0.01
    deactivate_l10n()


@pytest.mark.django_db
def test_velocity(l10n_nl, l10n_us):
    activate_l10n(l10n_nl)
    units = MeasuresTestModel.objects.create(windspeed=10)
    units = _reload(units)  # needed to convert int 10 to windspeed(10) in the units object
    assert units.windspeed.mps == 10
    assert units.windspeed.kmh == 36
    assert abs(units.windspeed.mph - 22.36936) < 0.00001

    assert l10n_nl.unit_velocity, 'mps'
    assert l10n_us.unit_velocity, 'mph'
    deactivate_l10n()


@pytest.mark.django_db
def test_precipitation(l10n_nl, l10n_eg, l10n_us):
    activate_l10n(l10n_nl)
    units = MeasuresTestModel.objects.create(precipitation=10)
    units = _reload(units)
    assert units.precipitation.mm == 10
    assert units.precipitation.inch == 10/25.4

    assert l10n_nl.unit_precipitation == 'mm'
    assert l10n_eg.unit_precipitation == 'mm'
    assert l10n_us.unit_precipitation == 'inch'
    deactivate_l10n()

