from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm
from django.core.files.base import ContentFile
import os
import imp
import pandas
import file_handle
import datetime
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


# Create your models here.

class Quantity(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length = 255)
    description = models.TextField()
    def __str__(self):
        return self.abbreviation

class SensorType(models.Model):
    name = models.CharField(max_length=255)
    sensor_scripts = models.FileField(upload_to='sensor_scripts/')
    quantities = models.ManyToManyField(Quantity)

    def __str__(self):
        return self.name

    def load_calibration_script(self):
        return file_handle.load_script(self.sensor_scripts,'calibrate')

    def load_metadata_script(self):
        return file_handle.load_script(self.sensor_scripts,'get_metadata')

class Sensor(models.Model):
    name = models.CharField(max_length=255)
    sensor_type = models.ForeignKey(SensorType,on_delete=models.PROTECT)
    def __str__(self):
        return self.name


class CalibrationParameters(models.Model):
    name = models.CharField(max_length=255)
    sensor = models.ForeignKey(Sensor,on_delete=models.CASCADE)
    parameters = models.FileField(upload_to='calibration_parameters')
    start = models.DateTimeField(default=datetime.datetime(1900,1,1))
    def __str__(self):
        return self.name

    def load_calibration_parameters(self):
        return file_handle.load_parameters(self.parameters)




class Measurement(models.Model):
    remarks = models.CharField(max_length=255)
    sensor = models.ForeignKey(Sensor,on_delete=models.PROTECT)
    default_calibration = models.ForeignKey(CalibrationParameters,on_delete=models.PROTECT)
    record = models.FileField(upload_to='measurements/')
    start = models.DateTimeField(default=datetime.datetime(2100,12,31))
    finish = models.DateTimeField(default=datetime.datetime(1900,1,1))
    timestep = models.DurationField(default=datetime.timedelta(seconds=0))

    def __str__(self):
        return self.remarks

    def calibrate(self):
        script = self.sensor.sensor_type.load_calibration_script()
        parameters = self.default_calibration.load_calibration_parameters()
        f = self.record.name
        return_value = script(parameters, self)
        return return_value

    def load_metadata(self):
        script = self.sensor.sensor_type.load_metadata_script()
        script(self)
        self.save()

@receiver(pre_delete, sender=Measurement)
def pre_delete_measurement(sender, instance, **kwargs):
    preprocs = instance.preprocesseddata_set.all()
    for preproc in preprocs:
        preproc.delete()

class Expedition(models.Model):
    name = models.CharField(max_length=255)
    measurements = models.ManyToManyField(Measurement)
    start = models.DateTimeField(default=datetime.datetime(2100,12,31,23,59,59))
    finish = models.DateTimeField(default=datetime.datetime(1900,1,1))
    remarks = models.TextField()

    def __str__(self):
        return self.name

    def load_dates(self):
        for meas in self.measurements:
            if meas.start < self.start:
                self.start = meas.start
            if meas.finish > self.finish:
                self.finish = meas.finish


class Visualization(models.Model):
    name = models.CharField(max_length=255)
    visualization_scripts = models.FileField(upload_to='visualization_scripts/')
    quantities = models.ManyToManyField(Quantity)
    def __str__(self):
        return self.name

    def load_preprocessing_script(self):
        return file_handle.load_script(self.visualization_scripts,'preprocess')

    def load_drawing_script(self):
        return file_handle.load_script(self.visualization_scripts,'draw')

class PreprocessedData(models.Model):
    measurements = models.ManyToManyField(Measurement)
    visualization = models.ForeignKey(Visualization,on_delete=models.CASCADE)
    record = models.FileField(upload_to='preprocessed/')

    def calculate(self):
        self.record.delete()
        desired_name = 'pd'+str(self.id)
        for i in self.measurements.all():
            desired_name = desired_name+'m'+str(i.id)
        self.record.save(desired_name,ContentFile(""))
        script = self.visualization.load_preprocessing_script()
        processed_value = script(self)
        outpfile = open(self.record.path,'w')
        processed_value.to_csv(outpfile)
        outpfile.close()

    def load(self):
        inpfile = open (self.record.path)
        return_value = pandas.read_csv(inpfile)
        inpfile.close()
        return return_value

@receiver(pre_delete, sender=PreprocessedData)
def preprocessed_data_delete(sender, instance, **kwargs):
    instance.record.delete(False)


class TemporalImage(models.Model):
    image = models.ImageField()
    expiration = models.DateTimeField(default = datetime.datetime(2100,12,31,23,59,59))
    ref_url = models.CharField(max_length=255)

    def __str__(self):
        return self.image.name

    def test_old(self):
        images = TemporalImage.objects.all()
        for image in images:
            if datetime.datetime.now()>image.expiration:
                image.remove()

    def new_name(self):
        self.save()
        self.image.name='EDNA/static/tmp/tmpimg_'+str(self.pk)+'.png'
        self.ref_url = '/static/tmp/tmpimg_'+str(self.pk)+'.png'
        self.expiration=datetime.datetime.now()+datetime.timedelta(minutes=5)
        self.save()


    def remove(self):
        self.image.delete()
        self.delete()
