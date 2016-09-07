from django.shortcuts import render, redirect

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import os
import datetime
import pandas as pd
import models as md
import forms as fm

from django.forms import formset_factory
from django.http import HttpResponseRedirect,HttpResponse
from views import global_context
   
# Create your views here.


def measurement(request):
    context = global_context(request)
    if request.method == 'POST':
        meas_ids = request.POST.getlist('meas_id')
        for i in meas_ids:
            meas = md.Measurement.objects.get(id=int(i))
            os.remove(meas.record.path)
            meas.delete()
    return HttpResponseRedirect('/overview/measurement/')


def expedition(request):
    context = global_context(request)
    if request.method == 'POST':
        exped_ids = request.POST.getlist('exped_id')
        for i in exped_ids:
            exped = md.Expedition.objects.get(id=int(i))
            exped.delete()
    return HttpResponseRedirect('/overview/expedition/')

def sensor(request):
    context = global_context(request)
    if request.method == 'POST':
        sens_ids = request.POST.getlist('sens_id')
        for i in sens_ids:
            sens = md.Sensor.objects.get(id=int(i))
            sens.delete()
    return HttpResponseRedirect('/overview/sensor/')


def sensortype(request):
    context = global_context(request)
    if request.method == 'POST':
        st_ids = request.POST.getlist('st_id')
        for i in st_ids:
            st = md.SensorType.objects.get(id=int(i))
            os.remove(st.sensor_scripts.path)
            st.delete()
    return HttpResponseRedirect('/overview/sensortype/')

def quantity(request):
    context = global_context(request)
    if request.method == 'POST':
        quan_ids = request.POST.getlist('quan_id')
        for i in quan_ids:
            quan = md.Quantity.objects.get(id=int(i))
            quan.delete()
    return HttpResponseRedirect('/overview/quantity/')


def calibration(request):
    context = global_context(request)
    if request.method == 'POST':
        calib_ids = request.POST.getlist('calib_id')
        for i in calib_ids:
            calib = md.CalibrationParameters.objects.get(id=int(i))
            os.remove(calib.parameters.path)
            calib.delete()
    return HttpResponseRedirect('/overview/calibration/')

def visualization(request):
    context = global_context(request)
    if request.method == 'POST':
        vis_ids = request.POST.getlist('vis_id')
        for i in vis_ids:
            vis = md.Visualization.objects.get(id=int(i))
            os.remove(vis.visualization_scripts.path)
            vis.delete()
    return HttpResponseRedirect('/overview/visualization/')


