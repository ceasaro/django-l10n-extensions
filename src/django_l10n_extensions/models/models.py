from django.db import models

from django_l10n_extensions.models import measures


class L10n(models.Model):
    DISTANCE_CHOICES = [(distance_unit, measures.Distance.UNITS_REPR.get(distance_unit, distance_unit))
                        for distance_unit in measures.Distance.UNITS.keys()]

    AREA_CHOICES = [(area_unit, measures.Area.UNITS_REPR.get(area_unit, area_unit))
                    for area_unit in measures.Area.UNITS.keys()]

    MASS_CHOICES = [(mass_unit, measures.Mass.UNITS_REPR.get(mass_unit, mass_unit))
                    for mass_unit in measures.Mass.UNITS.keys()]

    VOLUME_CHOICES = [(volume_unit, measures.Volume.UNITS_REPR.get(volume_unit, volume_unit))
                      for volume_unit in measures.Volume.UNITS.keys()]

    TEMP_CHOICES = [(temp_unit, measures.Temperature.UNITS_REPR.get(temp_unit, temp_unit))
                    for temp_unit in measures.Temperature.UNITS.keys()]

    SPEED_CHOICES = [(speed_unit, measures.Speed.UNITS_REPR.get(speed_unit, speed_unit))
                     for speed_unit in measures.Speed.UNITS.keys()]

    PRECIPITATION_CHOICES = [
        (precipitation_unit, measures.Precipitation.UNITS_REPR.get(precipitation_unit, precipitation_unit))
        for precipitation_unit in measures.Precipitation.UNITS.keys()]

    unit_distance = models.CharField(choices=DISTANCE_CHOICES, max_length=24, null=True, blank=True)
    unit_area = models.CharField(choices=AREA_CHOICES, max_length=24, null=True, blank=True)
    unit_mass = models.CharField(choices=MASS_CHOICES, max_length=24, null=True, blank=True)
    unit_volume = models.CharField(choices=VOLUME_CHOICES, max_length=24, null=True, blank=True)
    unit_temp = models.CharField(choices=TEMP_CHOICES, max_length=24, null=True, blank=True)
    unit_windspeed = models.CharField(choices=SPEED_CHOICES, max_length=24, null=True, blank=True)
    unit_precipitation = models.CharField(choices=PRECIPITATION_CHOICES, max_length=24, null=True,
                                          blank=True)

    def __unicode__(self):
        return u"L10n (Area= {area}) (Distance= {distance}) " \
               u"(Mass= {mass}) (Temperature= {temperature}) (Volume= {volume}) " \
               u"(Speed = {speed}) (Precipitation= {precipitation})".format(
            distance=self.get_unit_distance_display(),
            area=self.unit_area_display,
            mass=self.get_unit_mass_display(),
            volume=self.get_unit_volume_display(),
            temperature=self.unit_temp_display,
            speed=self.unit_windspeed_display,
            precipitation=self.unit_precipitation_display,
        )

    @property
    def unit_area_display(self):
        return self.get_unit_area_display()

    @property
    def unit_temp_display(self):
        return self.get_unit_temp_display()

    @property
    def unit_windspeed_display(self):
        return self.get_unit_windspeed_display()

    @property
    def unit_precipitation_display(self):
        return self.get_unit_precipitation_display()

    # TODO remove this property
    @property
    def unit_system(self):
        return 'metric' if self.unit_temp == 'C' else 'imperial'

    def as_dict(self):
        return {
            'unit_distance': self.unit_distance,
            'unit_distance_display': self.get_unit_distance_display(),

            'unit_area': self.unit_area,
            'unit_area_display': self.unit_area_display,

            'unit_mass': self.unit_mass,
            'unit_mass_display': self.get_unit_mass_display(),

            'unit_volume': self.unit_volume,
            'unit_volume_display': self.get_unit_volume_display(),

            'unit_temp': self.unit_temp,
            'unit_temp_display': self.unit_temp_display,

            'unit_windspeed': self.unit_windspeed,
            'unit_windspeed_display': self.unit_windspeed_display,

            'unit_precipitation': self.unit_precipitation,
            'unit_precipitation_display': self.unit_precipitation_display,

            'unit_system': self.unit_system
        }


DEFAULT_L10N = L10n(
    unit_distance=measures.Distance.METER,
    unit_area=measures.Area.SQUARE_METER,
    unit_mass=measures.Mass.GRAM,
    unit_volume=measures.Volume.LITER,
    unit_temp=measures.Temperature.CELSIUS,
    unit_windspeed=measures.Speed.MPS,
    unit_precipitation=measures.Precipitation.MM
)
