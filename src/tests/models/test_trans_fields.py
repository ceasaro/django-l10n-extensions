import pytest
from django.utils.translation import activate, deactivate
from django.utils.translation import gettext as _

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
    i18n_model = _reload(TransTestModel.objects.create(trans_field='edit'))
    activate('en')
    assert str(i18n_model.trans_field) == 'edit'
    assert "In a string '{}'".format(i18n_model.trans_field) == "In a string 'edit'"
    assert i18n_model.trans_field.msgid == 'edit'
    deactivate()

    activate('nl')
    assert str(i18n_model.trans_field) == 'bewerken'
    assert i18n_model.trans_field.msgid == 'edit'
    deactivate()


@pytest.mark.django_db
def test_trans_field_with_context():
    # we need to reload the instance from the db, so django converts the varchar value to a I18N object
    i18n_spring_device = _reload(TransTestModel.objects.create(trans_field=('mechanical device', 'spring')))
    i18n_spring_season = _reload(TransTestModel.objects.create(trans_field=('season', 'spring')))
    activate('en')
    assert str(i18n_spring_device.trans_field) == 'spring'
    assert str(i18n_spring_season.trans_field) == 'spring'
    deactivate()

    activate('nl')
    assert str(i18n_spring_device.trans_field) == 'veer'
    assert str(i18n_spring_season.trans_field) == 'lente'
    deactivate()


@pytest.mark.django_db
def test_trans_field_plural():
    # we need to reload the instance from the db, so django converts the varchar value to a I18N object
    i18n_spring_device = _reload(TransTestModel.objects.create(trans_field={'msgid': 'car', 'plural': 'cars'}))
    activate('en')
    assert i18n_spring_device.trans_field.trans(0) == 'cars'
    assert i18n_spring_device.trans_field.trans(1) == 'car'
    assert i18n_spring_device.trans_field.trans(2) == 'cars'

    activate('nl')
    assert i18n_spring_device.trans_field.trans(0) == "auto's"
    assert i18n_spring_device.trans_field.trans(1) == "auto"
    assert i18n_spring_device.trans_field.trans(2) == "auto's"

    activate('fr')
    assert i18n_spring_device.trans_field.trans(0) == "voiture"
    assert i18n_spring_device.trans_field.trans(1) == "voiture"
    assert i18n_spring_device.trans_field.trans(2) == "voitures"


@pytest.mark.django_db
def test_trans_field_plural_with_contxt():
    # we need to reload the instance from the db, so django converts the varchar value to a I18N object
    i18n_spring_device = _reload(TransTestModel.objects.create(trans_field={'i': 'tree', 'p': 'trees', 'c': 'in a wood'}))
    activate('en')
    assert i18n_spring_device.trans_field.trans(0) == 'trees'
    assert i18n_spring_device.trans_field.trans(1) == 'tree'
    assert i18n_spring_device.trans_field.trans(2) == 'trees'

    activate('nl')
    assert i18n_spring_device.trans_field.trans(0) == "bomen"
    assert i18n_spring_device.trans_field.trans(1) == "boom"
    assert i18n_spring_device.trans_field.trans(2) == "bomen"

    activate('fr')
    assert i18n_spring_device.trans_field.trans(0) == "arbre"
    assert i18n_spring_device.trans_field.trans(1) == "arbre"
    assert i18n_spring_device.trans_field.trans(2) == "arbres"
