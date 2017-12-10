from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm
import os
import imp
import pandas
import models

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def load_script(source, expected_name):
    return_value = None
    script_name = source.path
    mod_name,file_ext = os.path.splitext(os.path.split(script_name)[-1])
    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, script_name)
    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name,script_name)
    if hasattr(py_mod, expected_name):
        return_value = getattr(py_mod,expected_name)
    return return_value

def load_parameters(source):
    return_value = {}
    f = open(source.path,'r')
    for line in f:
         newline = line.replace(' ','')
         (key, val) = newline.split('=')
         return_value[key]=val
    f.close()
    return return_value

def create_image():
    output = models.TemporalImage()
    output.new_name()
    plt.savefig(output.image.path)
    output.test_old()
    return output
