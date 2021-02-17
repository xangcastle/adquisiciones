from .views import *
from django.urls import path

app_name = "riesgo"

urlpatterns = [
    path('crear_evaluaciones/', crear_evaluaciones, name="crear_evaluaciones"),
]
