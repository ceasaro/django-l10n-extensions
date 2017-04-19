import json

from django.db import models
from django.utils.translation import ugettext, pgettext


class I18N(object):
    def __init__(self, *args):
        if len(args) > 2:
            raise ValueError("Invalid arguments passed")
        super(I18N, self).__init__()
        self.msgid = args[-1]  # last argument contains msg id.
        self.msgctxt = args[0] if len(args) == 2 else None

    def __str__(self):
        if self.msgctxt:
            return pgettext(self.msgctxt, self.msgid)
        return ugettext(self.msgid)

    def __unicode__(self):
        self.__str__()

    def __repr__(self):
        self.__str__()


class I18NField(models.CharField):

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return None
        return I18N(*json.loads(value))

    def to_python(self, value):
        if isinstance(value, I18N) or value is None:
            return value
        return I18N(*json.loads(value))

    def get_prep_value(self, value):
        if isinstance(value, I18N):
            return json.dumps([value.msgid])
        if isinstance(value, (tuple, list)):
            return json.dumps(value)
        return json.dumps([value])

