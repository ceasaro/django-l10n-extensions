# -*- coding: utf-8 -*-
from django.db import models

from django_l10n_extensions.models.fields import I18NField

class I18NTestModel(models.Model):
    i18n_field = I18NField(max_length=128)

