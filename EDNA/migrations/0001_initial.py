# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CalibrationParameters',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('parameters', models.FileField(upload_to='calibration_parameters')),
                ('start', models.DateTimeField(default=datetime.datetime(1900, 1, 1, 0, 0))),
            ],
        ),
        migrations.CreateModel(
            name='Expedition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('start', models.DateTimeField(default=datetime.datetime(2100, 12, 31, 23, 59, 59))),
                ('finish', models.DateTimeField(default=datetime.datetime(1900, 1, 1, 0, 0))),
                ('remarks', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('remarks', models.CharField(max_length=255)),
                ('record', models.FileField(upload_to='measurements/')),
                ('start', models.DateTimeField(default=datetime.datetime(2100, 12, 31, 0, 0))),
                ('finish', models.DateTimeField(default=datetime.datetime(1900, 1, 1, 0, 0))),
                ('timestep', models.DurationField(default=datetime.timedelta(0))),
                ('default_calibration', models.ForeignKey(to='EDNA.CalibrationParameters', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
        migrations.CreateModel(
            name='PreprocessedData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('record', models.FileField(upload_to='preprocessed/')),
                ('measurements', models.ManyToManyField(to='EDNA.Measurement')),
            ],
        ),
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SensorType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('sensor_scripts', models.FileField(upload_to='sensor_scripts/')),
                ('quantities', models.ManyToManyField(to='EDNA.Quantity')),
            ],
        ),
        migrations.CreateModel(
            name='TemporalImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'')),
                ('expiration', models.DateTimeField(default=datetime.datetime(2100, 12, 31, 23, 59, 59))),
                ('ref_url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Visualization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('visualization_scripts', models.FileField(upload_to='visualization_scripts/')),
                ('quantities', models.ManyToManyField(to='EDNA.Quantity')),
            ],
        ),
        migrations.AddField(
            model_name='sensor',
            name='sensor_type',
            field=models.ForeignKey(to='EDNA.SensorType', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='preprocesseddata',
            name='visualization',
            field=models.ForeignKey(to='EDNA.Visualization'),
        ),
        migrations.AddField(
            model_name='measurement',
            name='sensor',
            field=models.ForeignKey(to='EDNA.Sensor', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='expedition',
            name='measurements',
            field=models.ManyToManyField(to='EDNA.Measurement'),
        ),
        migrations.AddField(
            model_name='calibrationparameters',
            name='sensor',
            field=models.ForeignKey(to='EDNA.Sensor'),
        ),
    ]
