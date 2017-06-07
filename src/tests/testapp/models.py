# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import CharField

from django_l10n_extensions.models import fields as l10n_fields


class TransTestModel(models.Model):
    trans_field = l10n_fields.TransField(max_length=128)
    other_trans_field = l10n_fields.TransField(max_length=128)


class MeasuresTestModel(models.Model):
    name = CharField(max_length=51)  # 'My units'
    area = l10n_fields.AreaField(null=True, blank=True)
    height = l10n_fields.DistanceField(null=True, blank=True)
    temp = l10n_fields.TemperatureField(null=True, blank=True)
    windspeed = l10n_fields.VelocityField(null=True, blank=True)
    precipitation = l10n_fields.PrecipitationField(null=True, blank=True)
