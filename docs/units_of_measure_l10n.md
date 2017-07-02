## Units of measure L10N

See [Units of measure](units_of_measure.md) for all available measures in django l10n extensions.

### L10N class
Django L10N extensions comes with an `L10n` class. This `L10n` class contains a setting for every available measure in
django L10N extensions.

below an L10N example of the default L10n settings of none is activated.:
```python
DEFAULT_L10N = L10n(
    unit_distance=Distance.METER,
    unit_area=Area.SQUARE_METER,
    unit_weight=Weight.GRAM,
    unit_volume=Volume.LITER,
    unit_temp=Temperature.CELSIUS,
    unit_velocity=Velocity.MPS,
    unit_precipitation=Precipitation.MM
)
```

On every Measure class you can request the l10n value of that measure e.g.:
```python
distance = Distance(11)
distance.l10n → '11.00 m'  # complete representation
distance.l10n_value → 11  # only the value
distance.l10n_unit → 'm'  # only the unit
distance.as_l10n(decimal_pos=0) → '11 m'  # specify the precision
```

To create an L10n for e.g. the United States see below:
```python
l10n_us = L10n(
    unit_distance=Distance.YARD,
    unit_area=Area.SQUARE_FOOT,
    unit_volume=Volume.GALLON,
    unit_weight=Weight.POUND,
    unit_temp=Temperature.FAHRENHEIT,
    unit_velocity=Velocity.MPH,
    unit_precipitation=Precipitation.INCH,
)
```

To activate an L10n object you can use the same approach as with django translations and use 
a simular `activate` method.

```python
from django_l10n_extensions.l10n_threading import activate

distance = Distance(m=11)
activate(l10n_us)

distance.l10n → '12.02 yard'
distance.l10n_value → 12.02974
distance.l10n_unit → 'yard'
```


### Django middleware to active L10n for a user (TODO)

We still need to implement some middleware to activate an `L10n` instance for a given user. 

TODO: add `L10n` instances for all countries.
