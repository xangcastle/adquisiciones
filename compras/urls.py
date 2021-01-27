from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^asignar_cuenta/$', asignar_cuenta, name='asignar_cuenta'),
    url(r'^imprimir_evaluacion/$', imprimir_evaluacion, name='imprimir_evaluacion'),
]
