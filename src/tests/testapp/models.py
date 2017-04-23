# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import CharField, IntegerField

from django_l10n_extensions.models.fields import TransField

class TransTestModel(models.Model):
    trans_field = TransField(max_length=128)

