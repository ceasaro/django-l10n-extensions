import json

from django.db import models
from django.utils.translation import gettext, pgettext, npgettext, ngettext

from django_l10n_extensions.forms import fields
from django_l10n_extensions.exceptions import L10NException
from django_l10n_extensions import measures


class T9N(object):
    def __init__(self, msgid=None, msgctxt=None, msgid_plural=None, **kwargs):
        self.msgid = msgid or kwargs.get('i')
        self.msgctxt = msgctxt or kwargs.get('c')
        self.plural = msgid_plural or kwargs.get('p')
        if not self.msgid:
            raise ValueError("Invalid arguments passed, need at least a msgid")

    def __str__(self):
        if self.msgctxt:
            return pgettext(self.msgctxt, self.msgid)
        return gettext(self.msgid)

    def trans(self, count):
        if self.msgctxt:
            return npgettext(self.msgctxt, self.msgid, self.plural, count)
        return ngettext(self.msgid, self.plural, count)

    def __eq__(self, other):
        if not other:
            return False
        if isinstance(other, self.__class__):
            return other.msgid == self.msgid and other.msgctxt == self.msgctxt and other.plural == self.plural
        return False

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.__str__())


class TransField(models.CharField):

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if isinstance(value, T9N) or not value  :
            return value
        try:
            return T9N(**json.loads(value))
        except ValueError:
            # db value isn't in json format, assigned the complete string as msgid.
            return T9N(msgid=value)

    def get_prep_value(self, value):
        if not value:
            return super(TransField, self).get_prep_value(value)
        data = {}
        if isinstance(value, T9N):
            data = {'i': value.msgid, 'c': value.msgctxt, 'p': value.plural}
        elif isinstance(value, (tuple, list)):
            length = len(value)
            if length == 1:
                data['i'] = value[0]
            elif length == 2:
                data['c'] = value[0]
                data['i'] = value[1]
            elif length == 3:
                data['c'] = value[0]
                data['i'] = value[1]
                data['p'] = value[2]
        elif isinstance(value, dict):
            data['i'] = value.get('msgid') or value.get('i')
            data['c'] = value.get('msgctxt') or value.get('c')
            data['p'] = value.get('plural') or value.get('p')
        else:
            data['i'] = value
        return json.dumps(data)


class BaseMeasureField(models.FloatField):
    measure_class = None
    DEFAULT_UNIT = measures.MeasureBase.STANDARD_UNIT

    def __init__(self, default_unit=None, **kwargs):
        if default_unit:
            self.DEFAULT_UNIT = default_unit
        super(BaseMeasureField, self).__init__(**kwargs)

    def construct_measure(self, value, unit=None):
        if not self.measure_class:
            raise L10NException('A measure class is required for {0}'.format(self.__class__))
        if not self.DEFAULT_UNIT:
            raise L10NException('A DEFAULT_UNIT is required for {0}'.format(self.__class__))
        return self.measure_class(**{unit if unit else self.DEFAULT_UNIT: value})

    def from_db_value(self, value, expression, connection):
        if type(value) in [float, int]:
            return self.construct_measure(value)

    def to_python(self, value):
        if isinstance(value, self.measure_class):
            return value
        if value is not None:
            return self.measure_class(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, self.measure_class):
            value = getattr(value, self.DEFAULT_UNIT)
        else:
            value = float(value)
            unit = self.measure_class().get_unit()
            if unit != self.DEFAULT_UNIT:
                measure = self.construct_measure(value, unit=unit)
                value = measure.get_l10n_value(unit=self.DEFAULT_UNIT)
        return value


class BaseDecimalMeasureField(models.DecimalField):
    measure_class = None
    DEFAULT_UNIT = measures.MeasureBase.STANDARD_UNIT

    def construct_measure(self, value, unit=None):
        if not self.measure_class:
            raise L10NException('A measure class is required for {0}'.format(self.__class__))
        if not self.DEFAULT_UNIT:
            raise L10NException('A DEFAULT_UNIT is required for {0}'.format(self.__class__))
        return self.measure_class(**{unit if unit else self.DEFAULT_UNIT: value})

    def from_db_value(self, value, expression, connection):
        if type(value) in [float, int]:
            return self.construct_measure(value)

    def to_python(self, value):
        if isinstance(value, self.measure_class):
            return value
        if value is not None:
            return self.measure_class(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, self.measure_class):
            value = getattr(value, self.DEFAULT_UNIT)
        else:
            value = float(value)
            unit = self.measure_class().get_unit()
            if unit != self.DEFAULT_UNIT:
                measure = self.construct_measure(value, unit=unit)
                value = measure.get_l10n_value(unit=self.DEFAULT_UNIT)
        return value


class DistanceField(BaseMeasureField):
    measure_class = measures.Distance
    DEFAULT_UNIT = measures.Distance.METER

    def formfield(self, **kwargs):
        defaults = {'form_class': fields.DistanceFormField}
        defaults.update(kwargs)
        return super(models.FloatField, self).formfield(**defaults)


class AreaField(BaseMeasureField):
    measure_class = measures.Area
    DEFAULT_UNIT = measures.Area.DEFAULT_UNIT

    def formfield(self, **kwargs):
        defaults = {'form_class': fields.AreaFormField}
        defaults.update(kwargs)
        return super(models.FloatField, self).formfield(**defaults)


class WeightField(BaseMeasureField):
    measure_class = measures.Weight
    DEFAULT_UNIT = measures.Weight.DEFAULT_UNIT

    def formfield(self, **kwargs):
        defaults = {'form_class': fields.WeightFormField}
        defaults.update(kwargs)
        return super(models.FloatField, self).formfield(**defaults)


class VolumeField(BaseMeasureField):
    measure_class = measures.Volume
    DEFAULT_UNIT = measures.Volume.DEFAULT_UNIT

    def formfield(self, **kwargs):
        defaults = {'form_class': fields.VolumeFormField}
        defaults.update(kwargs)
        return super(models.FloatField, self).formfield(**defaults)


class TemperatureField(BaseMeasureField):
    measure_class = measures.Temperature
    DEFAULT_UNIT = measures.Temperature.CELSIUS

    def formfield(self, **kwargs):
        defaults = {'form_class': fields.TemperatureFormField}
        defaults.update(kwargs)
        return super(models.FloatField, self).formfield(**defaults)


class VelocityField(BaseMeasureField):
    measure_class = measures.Velocity
    DEFAULT_UNIT = measures.Velocity.MPS

    def formfield(self, **kwargs):
        defaults = {'form_class': fields.VelocityFormField}
        defaults.update(kwargs)
        return super(models.FloatField, self).formfield(**defaults)


class PrecipitationField(BaseMeasureField):
    measure_class = measures.Precipitation
    DEFAULT_UNIT = measures.Precipitation.MM

    def formfield(self, **kwargs):
        defaults = {'form_class': fields.PrecipitationFormField}
        defaults.update(kwargs)
        return super(models.FloatField, self).formfield(**defaults)
