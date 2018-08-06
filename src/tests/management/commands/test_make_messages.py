import pytest

from django_l10n_extensions.management.commands import makemessages
from django_l10n_extensions.models.fields import T9N
from tests.conftest import _reload
from tests.testapp.models import TransTestModel


@pytest.mark.django_db
def test_collect_model_messages():
    collected_messages = {}

    def mock_update_messages(locale, t9n_list=None):
        print("locale: {}".format(locale))
        print("t9n_list: {}".format(t9n_list))
        messages = collected_messages.get(locale, [])
        messages += t9n_list
        collected_messages[locale] = messages

    # mock the update_messages with this test version to see which messages are all collected
    makemessages.update_messages = mock_update_messages
    TransTestModel.objects.create(trans_field=('mechanical device', 'spring'), other_trans_field='hurry')
    TransTestModel.objects.create(trans_field=('one', ))
    _reload(TransTestModel.objects.create(trans_field=('one', )))

    assert collected_messages == {}, "nothing collected yet, should still be empty."
    makemessages.Command().collect_model_messages({'locale': ['nl']})
    assert len(collected_messages.keys()) == 1 and 'nl' in collected_messages.keys(), \
        "Only 'nl' should be present in the collected messages keys"
    for t9n in [T9N('spring', msgctxt='mechanical device'), T9N('hurry'), T9N('one'), T9N('one')]:
        assert t9n in collected_messages['nl'], "{} not found in collected messages." \
                                                " Are msgid({}), msgctxt({}) and plural({}) the same?".\
            format(t9n,
                   "'{}'".format(t9n.msgid) if t9n.msgid else '',
                   "'{}'".format(t9n.msgctxt) if t9n.msgctxt else '',
                   "'{}'".format(t9n.plural) if t9n.plural else '',
                   )