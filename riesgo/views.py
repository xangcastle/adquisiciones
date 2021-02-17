from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *


def crear_evaluaciones(request):
    if request.method == "POST":
        for n, p in enumerate(request.POST.getlist('proveedor')):
            EvaluacionRiesgo(
                proveedor_id=request.POST.getlist('proveedor')[n],
                user_id=request.POST.getlist('user')[n]
            ).save()
        return redirect(to=reverse('admin:riesgo_evaluacionriesgo_changelist'))
    return render(request, "riesgo/evaluar_proveedores.html", {
        'proveedores': Proveedor.objects.all(),
        'usuarios': User.objects.filter(is_active=True, is_staff=True),
    })
