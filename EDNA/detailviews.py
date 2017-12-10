from django.shortcuts import render, redirect


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import datetime
import pandas as pd
import models as md
import forms as fm
import file_handle
import searches

from django.forms import formset_factory
from django.http import HttpResponseRedirect,HttpResponse
from views import global_context
   


# Create your views here.

def quantity(request, db_id):
    context = global_context(request)
    quantity = md.Quantity.objects.get(pk=db_id)
    context.update({'quantity':quantity})
    return render(request,'detailview_quantity.html',context)

def expedition(request, db_id):
    context = global_context(request)
    expedition = md.Expedition.objects.get(pk=db_id)
    context.update({'expedition':expedition})
    context.update(searches.measurement(request))

    measurementslist = expedition.measurements.all()
    context.update({'measurementslist':measurementslist})

    context.update({'checkboxes':True})
    return render(request,'detailview_expedition.html',context)


def sensortype(request, db_id):
    context = global_context(request)

    sensortype = md.SensorType.objects.get(pk=db_id)
    with open(sensortype.sensor_scripts.path) as inp:
        script = inp.read()
    context.update({'sensortype':sensortype,'script':script})

    context.update(searches.sensor(request))
    context['sensorslist']=context['sensorslist'].filter(sensor_type=db_id)
    context['sensorslist']=context['sensorslist'].order_by('pk')
    sensor_columns = {
        'show_pk':True,
        'show_name':True,
        'show_sensortype':False,
    }
    context.update({'sensor_columns':sensor_columns})

    return render(request,'detailview_sensortype.html',context)


def sensor(request, db_id):
    context = global_context(request)
    sensor = md.Sensor.objects.get(pk=db_id)
    context.update({'sensor':sensor})

    context.update(searches.calibration(request))
    context['calibrationslist']=context['calibrationslist'].order_by('pk')
    context['calibrationslist']=context['calibrationslist'].filter(sensor=db_id)

    context.update(searches.measurement(request))
    context.update({'checkboxes':False})
    context['measurementslist']=context['measurementslist'].order_by('pk')
    context['measurementslist']=context['measurementslist'].filter(sensor=db_id)

    return render(request,'detailview_sensor.html',context)


def measurement(request, db_id):
    context = global_context(request)
    measurement = md.Measurement.objects.get(pk=db_id)
    context.update({'measurement':measurement})

    return render(request,'detailview_measurement.html',context)

def visualization(request, db_id):
    context = global_context(request)
    visualization = md.Visualization.objects.get(pk=db_id)
    context.update({'visualization':visualization})
    with open(visualization.visualization_scripts.path) as inp:
        script = inp.read()
    context.update({'script':script})    

    draw = visualization.load_drawing_script()
    preproc = md.PreprocessedData.objects.all().filter(visualization=db_id)
    data = pd.DataFrame()
    for i in preproc:
        data = pd.concat([data,i.load()])
    draw(data)

    image = file_handle.create_image()
    context.update({'image':image.ref_url})

    return render(request,'detailview_visualization.html',context)


def calibration(request, db_id):
    context = global_context(request)
    calibration = md.CalibrationParameters.objects.get(pk=db_id)
    param = calibration.load_calibration_parameters()
    print param
    context.update({'calibration':calibration,'param':param})


    context.update(searches.measurement(request))
    context['measurementslist']=context['measurementslist'].filter(default_calibration=db_id)
    context['measurementslist']=context['measurementslist'].order_by('pk')

    return render(request,'detailview_calibration.html',context)

