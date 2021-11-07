from django.shortcuts import render
from django.http import JsonResponse
from .models import PromoCodigo
# Create your views here.

"""
Esta función valida el code que contiene 
el cod. promocional en la url del request del código de descuento.
en el console log de la página 
orden/templates/confirmacion.html
"""
def validar(request):
        codigo = request.GET.get('code') #obtenemos el codigo del request
        promo_codigo = PromoCodigo.objects.filter(codigo=codigo).first() #se invoca el objeto que se forma con 'codigo' que es PK en el model
        #si promo_codigo NO existe devuelve un 404 en un json
        if promo_codigo is None:
            return JsonResponse({
                'status' : False,
            },   status = 404)
        #si el codigo EXISTE devuelve:
        return JsonResponse({
            'status' : True,
            'codigo' : promo_codigo.codigo,
            'descuento': promo_codigo.descuento,
        })