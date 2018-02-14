from django.shortcuts import render
from .models import *
from django.http.response import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def asignar_cuenta(request):
    obj_json = {}
    id_sec = request.POST.get('sectorizacion', None)
    id_nue = request.POST.get('nuevo', None)
    print (id_sec, id_nue)
    if not id_sec or not id_nue:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Datos Invalidos"
    else:
        try:
            s = sectorizacion.objects.get(id=int(id_sec))
            n = nuevo.objects.get(id=int(id_nue))
        except:
            s = None
            n = None
        print (s, n)
        if not s or not n:
            obj_json['code'] = 400
            obj_json['mensaje'] = "Cuentas no encontradas"
        else:
            obj_json['code'] = 200
            obj_json['mensaje'] = "Cuenta asignada!"
            s.nuevo = n
            s.save()
    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')
