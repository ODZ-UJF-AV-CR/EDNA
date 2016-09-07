from django import forms

import models
import datetime

class SearchMeasurementsForm(forms.Form):
    show_id = forms.BooleanField(required=False)
    show_start = forms.BooleanField(required=False)
    show_finish = forms.BooleanField(required=False)
    show_sensor = forms.BooleanField(required=False)
    show_calibration = forms.BooleanField(required=False)
    show_remarks = forms.BooleanField(required=False)
    show_timestep = forms.BooleanField(required=False)
    rv = forms.CharField(widget = forms.HiddenInput(), required = False)

class TimeForm(forms.Form):
    earlier_limit = forms.DateTimeField(initial=datetime.datetime(1900,1,1),required=False)
    later_limit = forms.DateTimeField(initial=datetime.datetime(2099,12,31,23,59,59),required=False)
    rv = forms.CharField(widget = forms.HiddenInput(), required = False)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class VisualizeForm(forms.Form):
    vis_id = forms.ModelChoiceField(queryset=models.Visualization.objects.all())

class ExpeditionForm(forms.ModelForm):
    class Meta:
        model = models.Expedition
        fields = ['name','remarks']

class QuantityForm(forms.ModelForm):
    class Meta:
        model = models.Quantity
        fields = ['name','abbreviation','description']

class SensorTypeForm(forms.ModelForm):
    class Meta:
        model = models.SensorType
        fields = ['name','sensor_scripts','quantities']

class SensorForm(forms.ModelForm):
    class Meta:
        model = models.Sensor
        fields = ['sensor_type','name']

class CalibrationParametersForm(forms.ModelForm):
    class Meta:
        model = models.CalibrationParameters
        fields = ['sensor','name','parameters']

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = models.Measurement
        fields = ['sensor','record','remarks']

class VisualizationForm(forms.ModelForm):
    class Meta:
        model = models.Visualization
        fields = ['name','visualization_scripts','quantities']





