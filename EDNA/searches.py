from django.shortcuts import render, redirect


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import datetime
import pandas as pd
import models as md
import forms as fm

from django.forms import formset_factory
from django.http import HttpResponseRedirect,HttpResponse
from views import global_context
   
# Create your views here.


def measurement(request):
    context = {}
    if 'rv' in request.GET:
        search_form = fm.SearchMeasurementsForm(request.GET)

    else:
        search_form = fm.SearchMeasurementsForm(initial = {
            'show_id':True,
            'show_start':True,
            'show_finish':True,
            'show_calibration':False,
            'show_sensor':True,
            'show_remarks':True,
        })


    if 'rv' in request.GET:
        time_form = fm.TimeForm(request.GET)
    else:
        time_form = fm.TimeForm()
    if time_form.is_valid():
        earlier_limit = request.GET['earlier_limit']
        later_limit = request.GET['later_limit']
    else:
        time_form = fm.TimeForm()
        earlier_limit = datetime.datetime(1900,1,1)
        later_limit = datetime.datetime(2100,12,31,23,59,59)
        if 'rv' in request.GET:        
             context.update({'time_typo':True})

    
    measurementslist = md.Measurement.objects.all()
    measurementslist = measurementslist.filter(finish__gte = earlier_limit)
    measurementslist = measurementslist.filter(start__lt = later_limit)

    context.update({'measurementslist':measurementslist,'search_form':search_form,'time_form':time_form,'checkboxes':True})

    return context

def expedition(request):
    context = {}

    if 'rv' in request.GET:
        time_form = fm.TimeForm(request.GET)
    else:
        time_form = fm.TimeForm()
    if time_form.is_valid():
        earlier_limit = request.GET['earlier_limit']
        later_limit = request.GET['later_limit']
    else:
        time_form = fm.TimeForm()
        earlier_limit = datetime.datetime(1900,1,1)
        later_limit = datetime.datetime(2100,12,31,23,59,59)
        if 'rv' in request.GET:        
             context.update({'time_typo':True})


    expeditionslist = md.Expedition.objects.all()
    expeditionslist = expeditionslist.filter(finish__gte = earlier_limit)
    expeditionslist = expeditionslist.filter(start__lte = later_limit)
    context.update({'expeditionslist':expeditionslist,'time_form':time_form})

    return context

def sensor(request):
    context = {}
    sensorslist = md.Sensor.objects.all()
    context.update({'sensorslist':sensorslist})
    return context

def calibration(request):
    context = {}
    calibrationslist = md.CalibrationParameters.objects.all()
    context.update({'calibrationslist':calibrationslist})
    return context
