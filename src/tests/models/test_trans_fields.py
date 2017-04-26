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
