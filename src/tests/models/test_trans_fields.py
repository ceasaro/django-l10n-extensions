import json

import pytest
from django.utils.translation import activate, deactivate
from django.utils.translation import gettext as _

from django_l10n_extensions.models.fields import T9N, TransField
from tests.conftest import _reload
from tests.testapp.models import TransTestModel


def test_sanity_translaiton():
    activate('en')
    assert _('edit') == 'edit', "sanity test to test django translation (en) is working"
    deactivate()

    activate('nl')
    assert _('edit') == 'bewerken', "sanity test to test django translation (nl) is working"
    deactivate()


@pytest.mark.django_db
def test_trans_field():
    # we need to reload the instance from the db, so django converts the varchar value to a I18N object
    t9n_model = _reload(TransTestModel.objects.create(trans_field='edit'))
    activate('en')
    assert str(t9n_model.trans_field) == 'edit'
    assert "In a string '{}'".format(t9n_model.trans_field) == "In a string 'edit'"
    assert t9n_model.trans_field.msgid == 'edit'
    deactivate()

    activate('nl')
    assert str(t9n_model.trans_field) == 'bewerken'
    assert t9n_model.trans_field.msgid == 'edit'
    deactivate()


@pytest.mark.django_db
def test_trans_field_with_context():
    # we need to reload the instance from the db, so django converts the varchar value to a I18N object
    t9n_spring_device = _reload(TransTestModel.objects.create(trans_field=('mechanical device', 'spring')))
    t9n_spring_season = _reload(TransTestModel.objects.create(trans_field=('season', 'spring')))
    activate('en')
    assert str(t9n_spring_device.trans_field) == 'spring'
    assert str(t9n_spring_season.trans_field) == 'spring'
    deactivate()

    activate('nl')
    assert str(t9n_spring_device.trans_field) == 'veer'
    assert str(t9n_spring_season.trans_field) == 'lente'
    deactivate()


@pytest.mark.django_db
def test_trans_field_plural():
    # we need to reload the instance from the db, so django converts the varchar value to a I18N object
    t9n_spring_device = _reload(TransTestModel.objects.create(trans_field={'msgid': 'car', 'plural': 'cars'}))
    activate('en')
    assert t9n_spring_device.trans_field.trans(0) == 'cars'
    assert t9n_spring_device.trans_field.trans(1) == 'car'
    assert t9n_spring_device.trans_field.trans(2) == 'cars'

    activate('nl')
    assert t9n_spring_device.trans_field.trans(0) == "auto's"
    assert t9n_spring_device.trans_field.trans(1) == "auto"
    assert t9n_spring_device.trans_field.trans(2) == "auto's"

    activate('fr')
    assert t9n_spring_device.trans_field.trans(0) == "voiture"
    assert t9n_spring_device.trans_field.trans(1) == "voiture"
    assert t9n_spring_device.trans_field.trans(2) == "voitures"


@pytest.mark.django_db
def test_trans_field_plural_with_context():
    # we need to reload the instance from the db, so django converts the varchar value to a I18N object
    t9n_spring_device = _reload(TransTestModel.objects.create(trans_field={'i': 'tree', 'p': 'trees', 'c': 'in a forest'}))
    activate('en')
    assert t9n_spring_device.trans_field.trans(0) == 'trees'
    assert t9n_spring_device.trans_field.trans(1) == 'tree'
    assert t9n_spring_device.trans_field.trans(2) == 'trees'

    activate('nl')
    assert t9n_spring_device.trans_field.trans(0) == "bomen"
    assert t9n_spring_device.trans_field.trans(1) == "boom"
    assert t9n_spring_device.trans_field.trans(2) == "bomen"

    activate('fr')
    assert t9n_spring_device.trans_field.trans(0) == "arbre"
    assert t9n_spring_device.trans_field.trans(1) == "arbre"
    assert t9n_spring_device.trans_field.trans(2) == "arbres"


@pytest.mark.django_db
def test_trans_field_not_assigned():
    # we need to reload the instance from the db, so django converts the varchar value to a I18N object
    t9n_model = _reload(TransTestModel.objects.create())
    assert t9n_model.trans_field == ''


def test_t9n():
    assert len(T9N(msgid='test t9n')) == 8
    assert len(T9N(msgid='test t9n', msgctxt='my context')) == 8


def test_t9n_field():
    trans_field = TransField(max_length=128, null=False, blank=False)
    assert json.loads(trans_field.get_prep_value(T9N(msgid='test t9n', msgctxt='my context'))) == {
        'i': 'test t9n',
        'c': 'my context',
        'p': None
    }
