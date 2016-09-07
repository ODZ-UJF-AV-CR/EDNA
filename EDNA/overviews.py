from django.shortcuts import render, redirect

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import datetime
import pandas as pd
import models as md
import forms as fm
import searches

from django.forms import formset_factory
from django.http import HttpResponseRedirect,HttpResponse


from views import global_context

# auxiliary

   


# Create your views here.


def sensortype(request):
    context = global_context(request)
    sensortypelist = md.SensorType.objects.all()
    context.update({'sensortypelist':sensortypelist}) 

    if request.user.has_perm('edna.delete_sensortype'):
        context.update({'checkboxes':True})

    if request.user.has_perm('edna.add_sensortype'):
        stform = fm.SensorTypeForm()
        context.update({'stform':stform}) 

    return render(request,'overview_sensortype.html',context)


def sensor(request):
    context = global_context(request)
    context.update(searches.sensor(request))

    sensor_columns = {
        'show_pk':True,
        'show_name':True,
        'show_sensortype':True,
    }
    context.update({'sensor_columns':sensor_columns})

    if request.user.has_perm('edna.delete_sensor'):
        context.update({'checkboxes':True})

    if request.user.has_perm('edna.add_sensor'):
        sensorform = fm.SensorForm()
        context.update({'sensorform':sensorform}) 


    return render(request,'overview_sensor.html',context)


def calibration(request):
    context = global_context(request)
    context.update(searches.calibration(request))

    if request.user.has_perm('edna.delete_calibrationparameters'):
        context.update({'checkboxes':True})

    if request.user.has_perm('edna.add_calibrationparameters'):
        calibform = fm.CalibrationParametersForm()
        context.update({'calibform':calibform}) 

    return render(request,'overview_calibration.html',context)

def measurement(request):
    context = global_context(request)
    
    context.update(searches.measurement(request))
    context['measurementslist'] = context['measurementslist'].order_by('id')

    visualizeform = fm.VisualizeForm()
    context.update({'visualizeform':visualizeform})

    if request.user.has_perm('edna.add_measurement'):
        measureform = fm.MeasurementForm()
        context.update({'measureform':measureform}) 

    if request.user.has_perm('edna.add_expedition'):
        expedform = fm.ExpeditionForm()
        context.update({'expedform':expedform}) 


    return render(request,'overview_measurement.html',context)


def expedition(request):
    context = global_context(request)

    context.update(searches.expedition(request))
    context['expeditionslist'] = context['expeditionslist'].order_by('id')

    if request.user.has_perm('edna.add_expedition'):
        expedform = fm.ExpeditionForm()
        context.update({'expedform':expedform})


    if request.user.has_perm('edna.delete_expedition'):
        context.update({'checkboxes':True})

    return render(request,'overview_expedition.html',context)


def visualization(request):
    context = global_context(request)
    visualizationslist = md.Visualization.objects.all().order_by('pk')
    context.update({'visualizationslist':visualizationslist})

    if request.user.has_perm('edna.delete_visualization'):
        context.update({'checkboxes':True})

    if request.user.has_perm('edna.add_visualization'):
        visform = fm.VisualizationForm()
        context.update({'visform':visform})

    return render(request,'overview_visualization.html',context)


def quantity(request):
    context = global_context(request)
    quantitieslist = md.Quantity.objects.all().order_by('abbreviation')
    context.update({'quantitieslist':quantitieslist})

    if request.user.has_perm('edna.add_quantity'):
        quantityform = fm.QuantityForm()
        context.update({'quantityform':quantityform})


    if request.user.has_perm('edna.delete_quantity'):
        context.update({'checkboxes':True})

    return render(request,'overview_quantity.html',context)



