## Units of measure

Measure can be expressed in serveral units, e.g. distance can be in meters, yards, km, miles, etc. This extention
makes is easy to convert a measure in an other unit, see example below.

Units of measures are different in serveral countries. While most countries use the metric system, there are 
countries using other unities for measures. This extention also make it possible to automatically convert a measure
into the unit used for that country. See [Units of measure L10N](units_of_measure_l10n.md)

Django-l10n-extensions have unit conversion/localization for the following measures:

1. Distance (meters, yards, km, miles, etc.)
2. Weight (gram, pound, tonnes, short tons, etc.)
3. Area (square meter, square foot, hectare, acre, etc.)
4. Volume (liter, gallon, cubic dm, cubic gallon, etc.)
5. Temperature (Celsius, Fahrenheit, Kelvin)
6. Velocity (meter/sec., km/hour, miles/hour)
7. Precipitation (millimeter, inches)


__NOTE__:
The `Measure`-classes are inspired by and build on the `django.contrib.gis.measure` package.

### Distance
convert distance to any other unit, see `Distance.UNITS.keys()` for all supported units

_example_
```python
Distance(3).m == 3.0
Distance(m=4).m == 4.0
Distance(m=4).km == 0.004
Distance(m=4).yard == 4.374453193350831
```

### Weight
convert weight to any other unit, see `Weight.UNITS.keys()` for all supported units

_example_
```python
weight = Weight(g=3)
weight.g → 3.0
weight.mg → 3000.0
weight.lb → 0.006613867865546327  # pounds
```

### Area
convert area to any other unit, see `Area.UNITS.keys()` for all supported units

_example_
```python
weight = Area(ha=20)
weight.ha → 20.0
weight.sq_m → 200000.0  # square meter
weight.sq_yd → 239198.00926021606  # square yard
weight.feddan → 47.62
```

### Volume
convert volume to any other unit, see `Volume.UNITS.keys()` for all supported units

_example_
```python
volume = Volume(l=1)
volume.l → 1.0
volume.cu_dm → 0.9999999999999998  # square meter, rounding due to conversions with floats
volume.sq_yd → 239198.00926021606  # square yard
volume.feddan → 47.62
```

### Temperature
convert temperature to any other unit, see `Temperature.UNITS.keys()` for all supported units

_example_
```python
temperature = Temperature(C=5)
temperature.C → 5.0  # Celsius
temperature.F → 41.0  # Fahrenheit
temperature.K → 278.15  # Kelvin
```

### Velocity
convert velocity to any other unit, see `Velocity.UNITS.keys()` for all supported units

_example_
```python
velocity = Velocity(mps=6)
velocity.mps → 6.0  # Meter / second
velocity.mph → 13.421617752326414  # Miles / hour
velocity.mph → 21.599999999999998  # km / hour, rounding due to conversions with floats
```

### Precipitation
convert precipitation to any other unit, see `Precipitation0.UNITS.keys()` for all supported units

_example_
```python
precipitation = Precipitation(mps=2.4)
precipitation.mm → 2.4  # millimeter
precipitation.inch → 0.09448818897637795  # inches
```
