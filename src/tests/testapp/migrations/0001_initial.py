# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-26 08:51
from __future__ import unicode_literals

from django.db import migrations, models
import django_l10n_extensions.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MeasuresTestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=51)),
                ('area', django_l10n_extensions.models.fields.AreaField(blank=True, null=True)),
                ('height', django_l10n_extensions.models.fields.DistanceField(blank=True, null=True)),
                ('temp', django_l10n_extensions.models.fields.TemperatureField(blank=True, null=True)),
                ('windspeed', django_l10n_extensions.models.fields.SpeedField(blank=True, null=True)),
                ('precipitation', django_l10n_extensions.models.fields.PrecipitationField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransTestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_field', django_l10n_extensions.models.fields.TransField(max_length=128)),
            ],
        ),
    ]
