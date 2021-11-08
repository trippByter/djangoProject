from django.db import models
from django.db.models.base import ModelState 
import string # Para generar el codigo aleatoriamente
import random # Para generar el codigo aleatoriamente
from django.db.models.signals import pre_save 
from django.utils import timezone
# Create your models here.

class PromoCodigoManager(models.Manager):
    # Validar fecha de cod. prom.
    def get_validar(self, code):
        actual = timezone.now()
        #    ||Filtrar por id codigo  ||Filtrar por uso  ||Filtrar por fecha de inicio y final
        return self.filter(codigo=code).filter(used=False).filter(fecha_inicio__lte=actual).filter(fecha_final__gte=actual).first()


class PromoCodigo(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descuento = models.IntegerField(default=0)
    fecha_inicio = models.DateTimeField()
    fecha_final = models.DateTimeField()
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # Inicializamos el object de PromoCodigoManager
    objects = PromoCodigoManager()

    def __str__(self):
        return self.codigo
    
    # Funcion para cambiar el valor de 'used' a True y dejar el codigo como ya usado
    def codigo_usado(self):
        self.used = True # Cambio en el atributo de la clase
        self.save() # Guardar los cambios

# Guardar un presave antes de que se genere un codigo promocional, crear un nuevo callback
def set_codigo(sender, instance, *args, **kwargs):
    # Si existe un código, lo retornamos
    if instance.codigo:
        return 
    # Si no existe, usar "random y strings libs" para generar el codigo aleatoriamente,
    # Ambos hacen una lista, junto con instance.codigo 
    coders = string.ascii_uppercase + string.digits 
    # El random choice elige aleatoriamente el string en el random de 5, el for es para saber la longitud del cod. prom.
    instance.codigo = ''.join(random.choice(coders)for _ in range(5))
    
# Antes de guardar, va a ejecutar el callback
pre_save.connect(set_codigo, sender=PromoCodigo)