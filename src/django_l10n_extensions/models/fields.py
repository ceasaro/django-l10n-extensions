import json

from django.db import models
from django.utils.translation import ugettext, pgettext

from django_l10n_extensions.forms import fields
from django_l10n_extensions.exceptions import L10NException
from django_l10n_extensions.models import measures


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


class TransField(models.CharField):

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


class BaseMeasureField(models.FloatField):
    measure_class = None
    DEFAULT_UNIT = measures.MeasureBase.STANDARD_UNIT

    def construct_measure(self, value, unit=None):
        if not self.measure_class:
            raise L10NException('A measure class is required for {0}'.format(self.__class__))
        if not self.DEFAULT_UNIT:
            raise L10NException('A DEFAULT_UNIT is required for {0}'.format(self.__class__))
        return self.measure_class(**{unit if unit else self.DEFAULT_UNIT: value})

    def from_db_value(self, value, expression, connection, context):
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
                value = measure.default_value
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

    def from_db_value(self, value, expression, connection, context):
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
                value = measure.default_value
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


class TemperatureField(BaseMeasureField):
    measure_class = measures.Temperature
    DEFAULT_UNIT = measures.Temperature.CELSIUS

    def formfield(self, **kwargs):
        defaults = {'form_class': fields.TemperatureFormField}
        defaults.update(kwargs)
        return super(models.FloatField, self).formfield(**defaults)


class SpeedField(BaseMeasureField):
    measure_class = measures.Speed
    DEFAULT_UNIT = measures.Speed.MPS

    def formfield(self, **kwargs):
        defaults = {'form_class': fields.SpeedFormField}
        defaults.update(kwargs)
        return super(models.FloatField, self).formfield(**defaults)


class PrecipitationField(BaseMeasureField):
    measure_class = measures.Precipitation
    DEFAULT_UNIT = measures.Precipitation.MM

    def formfield(self, **kwargs):
        defaults = {'form_class': fields.PrecipitationFormField}
        defaults.update(kwargs)
        return super(models.FloatField, self).formfield(**defaults)
