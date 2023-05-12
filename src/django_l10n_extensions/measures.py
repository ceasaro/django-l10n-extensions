# coding=utf-8
from copy import deepcopy

from django.contrib.gis.measure import MeasureBase, NUMERIC_TYPES, Distance as GisDistance, Area as GisArea, \
    AREA_PREFIX, pretty_name
from django.utils.formats import number_format

from django_l10n_extensions.l10n_threading import get_l10n

VOLUME_PREFIX = 'cu_'


class MeasureL10nBase(MeasureBase):

    UNITS_REPR = {}

    def __init__(self, value=None, default_unit=None, decimal_pos=2, **kwargs):
        if value is not None:
            if isinstance(value, NUMERIC_TYPES + (str,)):
                unit = self.get_unit() or default_unit or self.STANDARD_UNIT
                kwargs[unit] = value
            else:
                # assume value is in the form of a dict like {'value': 1.0, 'unit': 'ha'}
                try:
                    kwargs[value['unit']] = value['value']
                except KeyError:
                    raise ValueError(u'invalid constructor parameter {}'.format(value))
            self._default_unit = default_unit
        self.decimal_pos = decimal_pos
        super(MeasureL10nBase, self).__init__(default_unit, **kwargs)

    @property
    def default_value(self):
        return getattr(self, self._default_unit)

    @property
    def l10n_value(self):
        return self.get_l10n_value()

    def get_l10n_value(self, unit=None):
        if not unit:
            unit = self.get_unit()
        return self.__getattr__(unit)

    @property
    def l10n_unit(self):
        unit = self.get_unit()
        return self.UNITS_REPR.get(unit, unit)

    @property
    def l10n(self):
        return self.as_l10n()

    def as_dict(self):
        return {u"value": self.l10n_value, u"unit": self.l10n_unit}

    def as_l10n(self, decimal_pos=None):
        value = number_format(self.l10n_value, decimal_pos=decimal_pos if decimal_pos is not None else self.decimal_pos)
        return u'{0} {1}'.format(value, self.l10n_unit)

    def get_unit(self):
        return self.DEFAULT_UNIT

    def __radd__(self, other):
        if other == 0:  # a little tricky cause the sum() operations starts with the value 0!
            other = Area(0)
        return self + other

    def __deepcopy__(self, memo):
        class_instance = self.__class__
        copied_class = class_instance.__new__(class_instance)
        memo[id(self)] = copied_class
        for field_name, field_instance in self.__dict__.items():
            setattr(copied_class, field_name, deepcopy(field_instance, memo))
        return copied_class

    def __getattr__(self, name):
        try:
            return super(MeasureL10nBase, self).__getattr__(self.unit_attname(name))
        except Exception as e:
            raise AttributeError(e)


class Distance(MeasureL10nBase, GisDistance):
    METER = u'm'
    FOOT = u'ft'
    YARD = u'yard'
    DEFAULT_UNIT = METER

    UNITS = GisDistance.UNITS.copy()
    UNITS.update({
        'hm': 100,
        'dm': 0.1,
    })

    def __init__(self, value=None, default_unit=DEFAULT_UNIT, **kwargs):
        super(Distance, self).__init__(value, default_unit, **kwargs)

    def get_unit(self):
        l10n = get_l10n()
        unit = l10n.unit_distance if l10n else self._default_unit
        return unit

    def __mul__(self, other):
        if isinstance(other, Area):
            return Volume(default_unit=VOLUME_PREFIX + self._default_unit,
                **{VOLUME_PREFIX + self.STANDARD_UNIT: (self.standard * other.standard)})
        else:
            return super(Distance, self).__mul__(other)


class Area(MeasureL10nBase, GisArea):
    SQUARE_METER = AREA_PREFIX + Distance.METER
    SQUARE_FOOT = AREA_PREFIX + Distance.FOOT
    ACRE = u'acre'
    FEDDAN = u'feddan'
    HECTARE = u'ha'
    MU = u'mu'
    DEFAULT_UNIT = AREA_PREFIX + Distance.STANDARD_UNIT

    UNITS = GisArea.UNITS.copy()
    UNITS.update({
        HECTARE: 10000.0,
        ACRE: 10000 / 2.471,
        FEDDAN: 10000 / 2.381,
        MU: 10000 / 15.0,
    })
    ALIAS = GisArea.ALIAS.copy()
    ALIAS.update({
        u'hectare': u'ha',
        u'acre': u'acre',
        u'feddan': u'feddan',
        u'mŭ': u'mu',
    })
    LALIAS = {k.lower(): v for k, v in ALIAS.items()}
    UNITS_REPR = {
        MU: u'mŭ',
        HECTARE: u'ha',
        ACRE: u'acre',
        FEDDAN: u'feddan',
    }

    def __init__(self, value=None, default_unit=DEFAULT_UNIT, decimal_pos=1, **kwargs):
        super(Area, self).__init__(value, default_unit, decimal_pos=decimal_pos, **kwargs)

    def get_unit(self):
        l10n = get_l10n()
        unit = l10n.unit_area if l10n else self._default_unit
        return unit

    def __mul__(self, other):
        if isinstance(other, Distance):
            return Volume(default_unit=VOLUME_PREFIX + self._default_unit[len(AREA_PREFIX):],
                **{VOLUME_PREFIX + self.STANDARD_UNIT[len(AREA_PREFIX): ]: (self.standard * other.standard)})
        elif isinstance(other, NUMERIC_TYPES):
            return self.__class__(default_unit=self._default_unit,
                                  **{self.STANDARD_UNIT: (self.standard * other)})
        else:
            raise TypeError('{area} must be multiplied with number or {distance}' % {
                'area': pretty_name(self.__class__),
                'distance': pretty_name(Distance),
            })



# weight
# 1000 g = 0,00220462 lb = 2 kati
class Weight(MeasureL10nBase):
    GRAM = u'g'
    KG = u'kg'
    MG = u'mg'
    TON = u'ton'
    POUND = u'lb'
    SHORT_TON = u'short ton'
    MARKET_CATTY = u'市斤'

    DEFAULT_UNIT = GRAM
    STANDARD_UNIT = GRAM  # this is the base unit and its value is used to recalculate other unit values
    UNITS = {
        GRAM: 1,
        KG: 1000,
        MG: 0.001,
        TON: 1000000,
        POUND: 453.59237,
        SHORT_TON: 907184.75,
        MARKET_CATTY: 500,
    }
    ALIAS = {
        u'gram': GRAM,
        u'kilogram': KG,
        u'milligram': MG,
        u'tonne': TON,
        u'US_ton': SHORT_TON,
        u'short_ton': SHORT_TON,
        u'lbm': POUND,
        u'pound': POUND,
        u'kati': MARKET_CATTY,
    }
    LALIAS = {k.lower(): v for k, v in ALIAS.items()}
    UNITS_REPR = {
        GRAM: u'g',
        KG: u'kg',
        MG: u'mg',
        TON: u'ton',
        POUND: u'lb',
        SHORT_TON: u'short ton',
        MARKET_CATTY: u'市斤',
    }

    def get_unit(self):
        l10n = get_l10n()
        unit = l10n.unit_weight if l10n else self._default_unit
        return unit


# volume
# 1 l = 0,264172 gal = 2,11338 pt = 33,814 oz
class Volume(MeasureL10nBase):
    LITER = u'l'

    GALLON = u'gal'
    DL = u'dl'
    CL = u'cl'
    ML = u'ml'

    DEFAULT_UNIT = LITER
    STANDARD_UNIT = VOLUME_PREFIX + Distance.STANDARD_UNIT  # this is the base unit and its value is used to recalculate other unit values
    UNITS = {'%s%s' % (VOLUME_PREFIX, k): v ** 3 for k, v in Distance.UNITS.items()}
    UNITS.update({
        LITER: 0.001,
        GALLON: 0.00378541178,
        CL: 0.00001,
        ML: 0.000001,
    })
    ALIAS = {
        u'liter': LITER,
        u'gallon': GALLON,
        u'deciliter': DL,
        u'centiliter': CL,
        u'milliliter': ML,
    }
    LALIAS = {k.lower(): v for k, v in ALIAS.items()}
    UNITS_REPR = {
        LITER: u'l',
        GALLON: u'gal',
        ML: u'ml',
    }

    def get_unit(self):
        l10n = get_l10n()
        unit = l10n.unit_volume if l10n else self._default_unit
        return unit


class Temperature(MeasureL10nBase):
    CELSIUS = u'C'
    FAHRENHEIT = u'F'
    KELVIN = u'K'

    DEFAULT_UNIT = CELSIUS
    STANDARD_UNIT = CELSIUS  # this is the base unit and its value is used to recalculate other unit values
    UNITS = {
        CELSIUS: lambda x: x,
        FAHRENHEIT: lambda x: x * 9.0 / 5.0 + 32.0,
        KELVIN: lambda x: x + 273.15
    }
    UNITS_REVERSE = {
        CELSIUS: lambda x: x,
        FAHRENHEIT: lambda x: (x - 32) / 9.0 * 5.0,
        KELVIN: lambda x: x - 273.15
    }
    UNITS_REPR = {
        CELSIUS: u'°C',
        FAHRENHEIT: u'°F',
        KELVIN: u'K',
    }
    ALIAS = {
        u'Celsius': CELSIUS,
        u'Fahrenheit': FAHRENHEIT,
        u'Kelvin': KELVIN,
    }
    LALIAS = {k.lower(): v for k, v in ALIAS.items()}

    def __getattr__(self, name):
        try:
            return self.UNITS[self.unit_attname(name)](self.standard)
        except Exception as e:
            raise AttributeError(e)

    def get_unit(self):
        l10n = get_l10n()
        unit = l10n.unit_temp if l10n else self._default_unit
        return unit

    def default_units(self, kwargs):
        """
        Return the unit value and the default units specified
        from the given keyword arguments dictionary.
        """
        val = 0.0
        default_unit = self.STANDARD_UNIT
        for unit, value in kwargs.items():
            if not isinstance(value, float):
                value = float(value)
            if unit in self.UNITS:
                val = self.UNITS_REVERSE[unit](value)
            elif unit in self.ALIAS:
                u = self.ALIAS[unit]
                val = self.UNITS_REVERSE[u](value)
            else:
                lower = unit.lower()
                if lower in self.UNITS:
                    val = self.UNITS_REVERSE[lower](value)
                elif lower in self.LALIAS:
                    u = self.LALIAS[lower]
                    val = self.UNITS_REVERSE[u](value)
                else:
                    raise AttributeError(u'Unknown unit type: %s' % unit)
        return val, default_unit

    def __radd__(self, other):
        pass


class Velocity(MeasureL10nBase):
    MPS = u'mps'
    KMH = u'kmh'
    MPH = u'mph'

    DEFAULT_UNIT = MPS
    STANDARD_UNIT = MPS  # this is the base unit and its value is used to recalculate other unit values
    UNITS = {
        MPS: 1,
        KMH: 1000.0/3600.0,
        MPH: 0.44704,  # from Wikipedia
    }
    ALIAS = {
        u'm/s': MPS,
        u'km/h': KMH,
        u'mph': MPH,
    }
    LALIAS = {k.lower(): v for k, v in ALIAS.items()}
    UNITS_REPR = {
        MPS: u'm/s',
        KMH: u'km/h',
        MPH: u'mph',
    }

    def get_unit(self):
        l10n = get_l10n()
        unit = l10n.unit_velocity if l10n else self._default_unit
        return unit


class Precipitation(MeasureL10nBase):
    MM = u'mm'
    INCH = u'inch'

    DEFAULT_UNIT = MM
    STANDARD_UNIT = MM  # this is the base unit and its value is used to recalculate other unit values
    UNITS = {
        MM: 1,
        INCH: 25.4,
    }
    ALIAS = {
        u'mm': MM,
        u'mm water': MM,
        u'inch': INCH,
        u'inches water': INCH,
    }
    LALIAS = {k.lower(): v for k, v in ALIAS.items()}
    UNITS_REPR = {
        MM: u'mm',
        INCH: u'inch',
    }

    def get_unit(self):
        l10n = get_l10n()
        unit = l10n.unit_precipitation if l10n else self._default_unit
        return unit

