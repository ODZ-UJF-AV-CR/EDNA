"""ODZ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from EDNA import views
from EDNA import overviews
from EDNA import detailviews
from EDNA import uploadviews
from EDNA import deleteviews

urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^login',views.login),
    url(r'^logout',views.logout),
    url(r'^visualize',views.visualize),
#    url(r'^jupyter',views.jupyter),

    url(r'^download/measurement',views.download_measurement),
    url(r'^upload/sensortype',uploadviews.sensortype),
    url(r'^upload/calibration',uploadviews.calibration),
    url(r'^upload/sensor',uploadviews.sensor),
    url(r'^upload/expedition',uploadviews.expedition),
    url(r'^upload/quantity',uploadviews.quantity),
    url(r'^upload/measurement',uploadviews.measurement),
    url(r'^upload/visualization',uploadviews.visualization),

    url(r'^delete/measurement',deleteviews.measurement),
    url(r'^delete/expedition',deleteviews.expedition),
    url(r'^delete/sensortype',deleteviews.sensortype),
    url(r'^delete/sensor',deleteviews.sensor),
    url(r'^delete/calibration',deleteviews.calibration),
    url(r'^delete/visualization',deleteviews.visualization),
    url(r'^delete/quantity',deleteviews.quantity),

    url(r'^overview/sensortype',overviews.sensortype),
    url(r'^overview/sensor',overviews.sensor),
    url(r'^overview/calibration',overviews.calibration),
    url(r'^overview/measurement',overviews.measurement),
    url(r'^overview/expedition',overviews.expedition),
    url(r'^overview/quantity',overviews.quantity),
    url(r'^overview/visualization',overviews.visualization),

    url(r'^detailview/sensortype/([0-9]+)',detailviews.sensortype),
    url(r'^detailview/sensor/([0-9]+)',detailviews.sensor),
    url(r'^detailview/calibration/([0-9]+)',detailviews.calibration),
    url(r'^detailview/measurement/([0-9]+)',detailviews.measurement),
    url(r'^detailview/expedition/([0-9]+)',detailviews.expedition),
    url(r'^detailview/quantity/([0-9]+)',detailviews.quantity),
    url(r'^detailview/visualization/([0-9]+)',detailviews.visualization),

    url(r'^',views.edna_home),
  

]
