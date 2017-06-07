## L10N Units of measure

Measures can be divined 
Units of measures are also different in serveral countries. While most countries use the metric system, there are 
countries using other unities for measures.
The  

Django-l10n-extensions have unit localization for the following measures:

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
convert distance to any other unit, see the source code of `Distance` for all supported units

_example_
```python
Distance(3).m == 3
Distance(m=4).m == 4
Distance(m=4).km == 0.004
Distance(m=4).yard == 4.374453193350831
```

### Weight
convert distance to any other unit, see the source code of `Distance` for all supported units

_example_
```python
Weight(3).g == 3.0
```