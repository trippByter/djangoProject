from django.shortcuts import render
from django.http import JsonResponse
from .models import PromoCodigo
from orden.decorador import validar_cart_and_orden
# Create your views here.

"""
Esta función valida el code que contiene 
el cod. promocional en la url del request del código de descuento.
en el console log de la página 
orden/templates/confirmacion.html
"""
# Accedemos al carrito y a la orden y responder con la funcion qeu acabamos de crear
# Usamos el carrito y la orden
@validar_cart_and_orden
def validar(request, cart, orden):
    # Obtenemos el codigo del request
    codigo = request.GET.get('code')
    # Se invoca el objeto que se forma con 'codigo' que es PK en el model
    promo_codigo = PromoCodigo.objects.filter(codigo=codigo).first() 
    # Si promo_codigo NO existe devuelve un 404 en un json
    if promo_codigo is None:
        print('hola')
        return JsonResponse({
            'status' : False,
        },  status = 404)
    # Si el promo código EXISTE,
    # Aplicar la orden. Tenemos el dcto como parametro.
    orden.aplicarCodigo(promo_codigo)
    # Devuelve:
    return JsonResponse({
        'status' : True,
        'codigo' : promo_codigo.codigo,
        'descuento': promo_codigo.descuento,
        'total' : orden.total,
    })