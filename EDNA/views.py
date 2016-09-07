from django.shortcuts import render, redirect
import django.contrib.auth as auth


from .models import SensorType #just for test
from .models import CalibrationParameters #just for test
from .models import Measurement #just for test
from .models import Visualization #just for test
from .models import PreprocessedData #just for test
from django.core.files.base import ContentFile #just for test

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import zipfile
import os
import datetime
import pandas as pd
import models as md
import forms as fm
import file_handle
import preprocessor

from django.forms import formset_factory
from django.http import HttpResponseRedirect,HttpResponse
# auxiliary

def global_context(request):
    request.session.set_expiry(3600)
    sessionexpiration = request.session. get_expiry_date()
    return {'sessionexpiration':sessionexpiration}

   


# Create your views here.

def edna_home(request):
    context = global_context(request)
    sample = md.Visualization.objects.get(pk=2)
    draw = sample.load_drawing_script()
    preproc = md.PreprocessedData.objects.all().filter(visualization=sample)
    data = pd.DataFrame()
    for i in preproc:
        data = pd.concat([data,i.load()])
    draw(data)
    image = file_handle.create_image()
    context.update({'image':image.ref_url})

    return render(request,'index.html',context)

def login(request):
    context = global_context(request)
    if request.method == 'POST':
        login_form = fm.LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/')
    else:
        login_form = fm.LoginForm()
    context.update({'login_form':login_form}) 
    return render(request,'login.html',context)

def logout(request):
    context = global_context(request)
    auth.logout(request)
    return HttpResponseRedirect('/')


def download_measurement(request):
    context = global_context(request)
    filename = 'measurements.zip'
    meas_ids = request.POST.getlist('meas_id')
    myzip = zipfile.ZipFile(filename,'w')
    for i in meas_ids:
        meas = md.Measurement.objects.get(id=int(i))
        myzip.write(meas.record.name)
    myzip.close()
    fsock = open(filename,"rb")
    response = HttpResponse(fsock, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=measurements.zip'
    fsock.close()
    os.remove(filename)
    return response

def visualize(request):
    context = global_context(request)
    meas_ids = request.POST.getlist('meas_id')
    vis_id = request.POST['vis_id']
    visual = md.Visualization.objects.get(pk=vis_id)
    measures = []
    for i in meas_ids:
        meas = md.Measurement.objects.get(id=int(i))
        measures.append(meas)
    preprocessor.check_visualization(measures,visual)
    active = md.PreprocessedData.objects.all()    
    active = active.filter(visualization__pk = visual.pk)
    for j in measures:
        active = active.filter(measurements__pk = j.pk)
    data = pd.DataFrame()
    draw = visual.load_drawing_script()
    for preproc in active:
        data = pd.concat([data,preproc.load()])
    draw(data)
    image = file_handle.create_image()
    context.update({'image':image.ref_url})
    return render(request,'visualize.html',context)
