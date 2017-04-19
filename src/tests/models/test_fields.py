# First of all load and configure the django test app
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.testapp.settings")
django.setup()

import pytest
from django.utils.translation import activate, deactivate
from django.utils.translation import gettext as _

from tests.conftest import _reload
from tests.testapp.models import I18NTestModel


def test_sanity_translaiton():
    activate('en')
    assert _('edit') == 'edit', "sanity test to test django translation (en) is working"
    deactivate()

    activate('nl')
    assert _('edit') == 'bewerken', "sanity test to test django translation (nl) is working"
    deactivate()


@pytest.mark.django_db
def test_i18n_field():
    # we need to reload the instance from the db, so django converts the varchar value to a I18N object
    i18n_model = _reload(I18NTestModel.objects.create(i18n_field='edit'))
    activate('en')
    assert str(i18n_model.i18n_field) == 'edit'
    assert "In a string '{}'".format(i18n_model.i18n_field) == "In a string 'edit'"
    assert i18n_model.i18n_field.msgid == 'edit'
    deactivate()

    activate('nl')
    assert str(i18n_model.i18n_field) == 'bewerken'
    assert i18n_model.i18n_field.msgid == 'edit'
    deactivate()


@pytest.mark.django_db
def test_i18n_field_with_context():
    # we need to reload the instance from the db, so django converts the varchar value to a I18N object
    i18n_spring_device = _reload(I18NTestModel.objects.create(i18n_field=('mechanical device', 'spring' )))
    i18n_spring_season = _reload(I18NTestModel.objects.create(i18n_field=('season', 'spring' )))
    activate('en')
    assert str(i18n_spring_device.i18n_field) == 'spring'
    assert str(i18n_spring_season.i18n_field) == 'spring'
    deactivate()

    activate('nl')
    assert str(i18n_spring_device.i18n_field) == 'veer'
    assert str(i18n_spring_season.i18n_field) == 'lente'
    deactivate()
