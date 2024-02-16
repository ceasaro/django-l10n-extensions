from django.db import models

from django_l10n_extensions import measures


class L10n(models.Model):
    DISTANCE_CHOICES = [(distance_unit, measures.Distance.UNITS_REPR.get(distance_unit, distance_unit))
                        for distance_unit in measures.Distance.UNITS.keys()]

    AREA_CHOICES = [(area_unit, measures.Area.UNITS_REPR.get(area_unit, area_unit))
                    for area_unit in measures.Area.UNITS.keys()]

    WEIGHT_CHOICES = [(weight_unit, measures.Weight.UNITS_REPR.get(weight_unit, weight_unit))
                      for weight_unit in measures.Weight.UNITS.keys()]

    VOLUME_CHOICES = [(volume_unit, measures.Volume.UNITS_REPR.get(volume_unit, volume_unit))
                      for volume_unit in measures.Volume.UNITS.keys()]

    TEMP_CHOICES = [(temp_unit, measures.Temperature.UNITS_REPR.get(temp_unit, temp_unit))
                    for temp_unit in measures.Temperature.UNITS.keys()]

    VELOCITY_CHOICES = [(velocity_unit, measures.Velocity.UNITS_REPR.get(velocity_unit, velocity_unit))
                        for velocity_unit in measures.Velocity.UNITS.keys()]

    PRECIPITATION_CHOICES = [
        (precipitation_unit, measures.Precipitation.UNITS_REPR.get(precipitation_unit, precipitation_unit))
        for precipitation_unit in measures.Precipitation.UNITS.keys()]

    unit_distance = models.CharField(choices=DISTANCE_CHOICES, max_length=64, null=True, blank=True)
    unit_area = models.CharField(choices=AREA_CHOICES, max_length=64, null=True, blank=True)
    unit_weight = models.CharField(choices=WEIGHT_CHOICES, max_length=64, null=True, blank=True)
    unit_volume = models.CharField(choices=VOLUME_CHOICES, max_length=64, null=True, blank=True)
    unit_temp = models.CharField(choices=TEMP_CHOICES, max_length=64, null=True, blank=True)
    unit_velocity = models.CharField(choices=VELOCITY_CHOICES, max_length=64, null=True, blank=True)
    unit_precipitation = models.CharField(choices=PRECIPITATION_CHOICES, max_length=64, null=True,
                                          blank=True)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"L10n (Area= {area}) (Distance= {distance}) " \
               u"(Weight= {weight}) (Temperature= {temperature}) (Volume= {volume}) " \
               u"(Velocity = {velocity}) (Precipitation= {precipitation})".format(
            distance=self.get_unit_distance_display(),
            area=self.get_unit_area_display(),
            weight=self.get_unit_weight_display(),
            volume=self.get_unit_volume_display(),
            temperature=self.get_unit_temp_display(),
            velocity=self.get_unit_velocity_display(),
            precipitation=self.get_unit_precipitation_display(),
        )

    def as_dict(self):
        return {
            'unit_distance': self.unit_distance,
            'unit_distance_display': self.get_unit_distance_display(),

            'unit_area': self.unit_area,
            'unit_area_display': self.get_unit_area_display(),

            'unit_weight': self.unit_weight,
            'unit_weight_display': self.get_unit_weight_display(),

            'unit_volume': self.unit_volume,
            'unit_volume_display': self.get_unit_volume_display(),

            'unit_temp': self.unit_temp,
            'unit_temp_display': self.get_unit_temp_display(),

            'unit_windspeed': self.unit_velocity,
            'unit_windspeed_display': self.get_unit_velocity_display(),

            'unit_precipitation': self.unit_precipitation,
            'unit_precipitation_display': self.get_unit_precipitation_display(),
        }


DEFAULT_L10N = L10n(
    unit_distance=measures.Distance.METER,
    unit_area=measures.Area.SQUARE_METER,
    unit_weight=measures.Weight.GRAM,
    unit_volume=measures.Volume.LITER,
    unit_temp=measures.Temperature.CELSIUS,
    unit_velocity=measures.Velocity.MPS,
    unit_precipitation=measures.Precipitation.MM
)
