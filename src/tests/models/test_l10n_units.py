# coding=utf-8
import pytest

from django_l10n_extensions.l10n_threading import activate as activate_l10n
from django_l10n_extensions.measures import Distance


@pytest.mark.django_db
def test_l10n(l10n_nl, l10n_us):
    activate_l10n(l10n_nl)
    distance = Distance(11)
    assert distance.m == 11
    assert abs(distance.yard - 12.02974) < 0.0001
    assert distance.l10n == '11.00 m'
    assert distance.as_l10n(decimal_pos=0) == '11 m'
    assert distance.l10n_value == 11
    assert distance.l10n_unit == 'm'

    # change l10n
    # TODO punctuation should alter
    activate_l10n(l10n_us)
    assert distance.l10n == '12.02 yard'
    assert abs(distance.l10n_value - 12.02974) < 0.0001
    assert distance.l10n_unit == 'yard'
