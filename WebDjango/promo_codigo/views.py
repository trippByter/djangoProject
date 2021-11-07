from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

def validar(request):
    responseData = {
        'id' : 4,
        'name': 'Alvaro',
        'roles' : ['Admin', 'User'],
    }
    return JsonResponse(responseData)