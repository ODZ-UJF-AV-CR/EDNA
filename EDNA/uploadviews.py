from django.shortcuts import render, redirect

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import datetime
import pandas as pd
import models as md
import forms as fm

from preprocessor import check_visualization
from django.forms import formset_factory
from django.http import HttpResponseRedirect,HttpResponse
from views import global_context
   
# Create your views here.

def measurement(request):
    context = global_context(request)
    if request.user.has_perm('edna.add_maesurement'):
        form = fm.MeasurementForm(request.POST, request.FILES)
        if form.is_valid():
            meas = form.save(commit=False)
            calibs = md.CalibrationParameters.objects.all()
            calibs = calibs.filter(sensor=meas.sensor)
            meas.default_calibration = calibs.earliest('start')
            meas.save()
            meas.load_metadata()
            for i in calibs:
                if (i.start<datetime.datetime.now()) and (i.start>meas.default_calibration.start):
                    meas = i
            meas.save()
            return HttpResponseRedirect('/detailview/measurement/'+str(meas.pk))
        else:
            return HttpResponseRedirect('/overview/measurement/')
    else:
        return HttpResponseRedirect('/overview/measurement/')
 


def expedition(request):
    context = global_context(request)
    if (request.method == 'POST') and (request.user.has_perm('edna.add_expedition')):
        expedname = request.POST['name']
        if expedname:
            meas_ids = request.POST.getlist('meas_id')
            newexped = md.Expedition()
            newexped.name = expedname
            newexped.remarks = request.POST['remarks']
            newexped.start = datetime.datetime(2100,12,31)
            newexped.finish = datetime.datetime(1900,1,1)
            newexped.save()
            measures = []
            for i in meas_ids:
                meas = md.Measurement.objects.get(id=int(i))
                measures.append(meas)
                newexped.measurements.add(meas)
                if meas.start<newexped.start:
                    newexped.start = meas.start
                if meas.finish>newexped.finish:
                    newexped.finish = meas.finish
            newexped.save()
            for i in md.Visualization.objects.all():
                check_visualization(measures,i)
        else:
            return HttpResponseRedirect('/overview/expedition/')
    else:
        return HttpResponseRedirect('/overview/expedition/')
    return HttpResponseRedirect('/detailview/expedition/'+str(newexped.pk))

def quantity(request):
    context = global_context(request)
    if (request.method == 'POST') and (request.user.has_perm('edna.add_quantity')):
        form = fm.QuantityForm(request.POST)
        if form.is_valid():
            quantity = form.save()
            return HttpResponseRedirect('/detailview/quantity/'+str(quantity.pk))
        else:
            return HttpResponseRedirect('/overview/quantity/')
    else:
        return HttpResponseRedirect('/overview/quantity/')

def sensor(request):
    context = global_context(request)
    if (request.method == 'POST') and (request.user.has_perm('edna.add_sensor')):
        form = fm.SensorForm(request.POST)
        if form.is_valid():
            sensor = form.save()
            return HttpResponseRedirect('/detailview/sensor/'+str(sensor.pk))
        else:
            return HttpResponseRedirect('/overview/sensor/')
    else:
        return HttpResponseRedirect('/overview/sensor/')

def calibration(request):
    context = global_context(request)
    if (request.method == 'POST') and (request.user.has_perm('edna.add_calibrationparameters')):
        form = fm.CalibrationParametersForm(request.POST, request.FILES)
        if form.is_valid():
            calibration = form.save()
            return HttpResponseRedirect('/detailview/calibration/'+str(calibration.pk))
        else:
            return HttpResponseRedirect('/overview/calibration/')
    else:
        return HttpResponseRedirect('/overview/calibration/')

def sensortype(request):
    context = global_context(request)
    if (request.method == 'POST') and (request.user.has_perm('edna.add_sensortype')):
        form = fm.SensorTypeForm(request.POST, request.FILES)
        if form.is_valid():
            sensortype = form.save()
            return HttpResponseRedirect('/detailview/sensortype/'+str(sensortype.pk))
        else:
            return HttpResponseRedirect('/overview/sensortype/')
    else:
        return HttpResponseRedirect('/overview/sensortype/')

def visualization(request):
    context = global_context(request)
    if (request.method == 'POST') and (request.user.has_perm('edna.add_visualization')):
        form = fm.VisualizationForm(request.POST, request.FILES)
        if form.is_valid():
            visualization = form.save()
            for i in md.Expedition.objects.all():
                measures = []
                for j in i.measurements.all():
                    measures.append(j)
                check_visualization(measures,visualization)
            return HttpResponseRedirect('/detailview/visualization/'+str(visualization.pk))
        else:
            return HttpResponseRedirect('/overview/visualization/')
    else:
        return HttpResponseRedirect('/overview/visualization/')
