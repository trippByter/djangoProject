from django.db import models
from django.db.models.base import ModelState #
import string #para generar el codigo aleatoriamente
import random #para generar el codigo aleatoriamente
from django.db.models.signals import pre_save 

# Create your models here.

class PromoCodigo(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descuento = models.FloatField(default=0.0)
    fecha_inicio = models.DateTimeField()
    fecha_final = models.DateTimeField()
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.codigo

#guardar un presave antes de que se genere un codigo promocional, crear un nuevo callback
def set_codigo(sender, instance, *args, **kwargs):
    #si existe un código, lo retornamos
    if instance. codigo:
        return 
    #si no existe, usar "random y strings libs" para generar el codigo aleatoriamente
    coders = string.ascii_uppercase + string.digits #ambos hacen una lista, junto con instance.codigo
    instance.codigo = ''.join(random.choice(coders)for _ in range(5)) #el for es para saber la longitud de nuestro código
    #el random choice elige aleatoriamente el string en el random de 5
#antes de guardar, va a ejecutar el callback
pre_save.connect(set_codigo, sender=PromoCodigo)