# coding=utf-8
import pytest

from django_l10n_extensions.l10n_threading import activate as activate_l10n, deactivate as deactivate_l10n
from django_l10n_extensions.models.measures import Distance, Area, Volume, Mass


def test_compare_area_operations():
    area_1 = Area(ha=11.000)
    area_2 = Area(ha=11)
    assert area_1 == area_2

    assert (area_1 + area_2).ha == 22.0000
    assert (area_1 - area_2).ha == 0.0000
    assert (area_1 / 11).ha == 1.0000
    assert (area_1 / 11).sq_m == 10000.0000
    assert (area_1 * 11).ha == 121.0000
    assert (area_1 * 11).sq_m == 1210000.0000

    assert area_1 > Area(ha=2)
    assert area_1 < Area(ha=22)

    area_sum = sum([Area(ha=3), Area(5), Area(2)])
    assert area_sum.ha == 3.0007

    assert abs(round(Area(1).l10n_value / 3, 2) - 0.33) <  0.0001


def test_constructors():
    assert Distance(3).m == 3
    assert Distance(m=4).m == 4

    assert Distance({'unit':'m', 'value':3}).m, 3
    with pytest.raises(ValueError):
        assert Distance({'distance':'m', 'value':3}).m == 3


def test_mass():
    assert Mass(1).g == 1
    assert Mass(kg=1).g == 1000
    assert abs(Mass(kg=4.5).us_ton - 0.0049604009) < 0.00001
    assert abs(Mass(kg=4.5).short_ton - 0.0049604009) < 0.00001
    assert Mass(lb=4.5).pound == 4.5


def test_volume():
    assert Volume(1).l == 1
    assert Volume(gal=1).l == 3.78541178
    assert abs(Volume(ml=44).gal - 0.0116235703) < 0.0001
    assert Volume(cu_m=5).l == 5000
    assert Volume(cu_yd=3).cu_yd == 3


def test_add():
    assert Volume(l=1) + Volume(ml=100) == Volume(l=1.1)
    with pytest.raises(TypeError):
        assert Volume(l=1) + Mass(kg=1), 'can not add up Volumes and Masses'
    assert Distance(5) + Distance(hm=5) == Distance(m=505)
    with pytest.raises(TypeError):
        assert Distance(km=3) + 4, 'can not add plain numeric values (in what unit is the numeric value?'

def test_mul():
    assert Distance(5) * 2 == Distance(10)
    assert Distance(m=5) * Distance(km=0.01) == Area(sq_m=50)
    assert Area(sq_m=2) * 4 == Area(sq_m=8)
    assert Area(sq_m=2) * Distance(km=0.02) == Volume(cu_m=40)
    assert Distance(m=15) * Area(sq_m=3) == Volume(cu_m=45)
    assert Area(ha=1) * 3 == Area(ha=3)
    assert 3 * Area(ha=1) == Area(ha=3)
    with pytest.raises(TypeError):
        assert Area(ha=1) * Area(ha=1)