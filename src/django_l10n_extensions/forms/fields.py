from django.forms.fields import Field


class DistanceFormField(Field):

    def to_python(self, value):
        from django_l10n_extensions.models.measures import Distance
        return Distance(value)


class AreaFormField(Field):

    def to_python(self, value):
        from django_l10n_extensions.models.measures import Area
        return Area(value)


class TemperatureFormField(Field):

    def to_python(self, value):
        from django_l10n_extensions.models.measures import Temperature
        return Temperature(value)


class SpeedFormField(Field):

    def to_python(self, value):
        from django_l10n_extensions.models.measures import Speed
        return Speed(value)

class PrecipitationFormField(Field):

    def to_python(self, value):
        from django_l10n_extensions.models.measures import Precipitation
        return Precipitation(value)
