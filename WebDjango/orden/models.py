from django.db import models
from promo_codigo.models import PromoCodigo
from users.models import User
from carts.models import Cart
from django.db.models.signals import pre_save
from DirEnvio.models import DireccionEnvio
from .comun import OrdenStatus
from .comun import choices
import uuid
from enum import Enum
# Create your models here.

class Orden(models.Model):
    ordenID = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=40, choices=choices, default=OrdenStatus.CREATED)
    total = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    direccion_envio = models.ForeignKey(DireccionEnvio, null=True, blank=True, on_delete=models.CASCADE)
    promo_codigo = models.OneToOneField(PromoCodigo, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.ordenID
    
    #aplicamos codigo de descuento con atributo 'promo_codigo'
    def aplicarCodigo(self, promo_codigo):
        #si el codigo no existe antes, se colocará el que se obtenga
        if self.promo_codigo is None:
            self.promo_codigo = promo_codigo
            self.save() #guardamos los cambios
            self.update_total() #actulizamos el total
            promo_codigo.codigo_usado() #cambia el booleano a True. 'Ya usado'
    
    def get_descuento(self):
        #si hay un codigo promocional, tenemos el dcto
        if self.promo_codigo:
            return self.promo_codigo.descuento
        #si no hay un código promocional, retorna cero
        return 0
    
    #operacion resta de descuento de carrito y codigo promocional. Usar la función decimal
    def get_total(self):
        return self.cart.total - self.get_descuento()

    def update_total(self):
        self.total = self.get_total()
        self.save()

    def get_or_set_direccion_envio(self):
        if self.direccion_envio:
            return self.direccion_envio

        direccion_envio = self.user.direccion_envio
        if direccion_envio:
            self.direccion_envio = direccion_envio
            
        return direccion_envio

    def cancelar(self):
        self.status = OrdenStatus.CANCELED
        self.save()
    
    def completado(self):
        self.status = OrdenStatus.COMPLETED
        self.save()

    def update_direccion_envio(self, direccion_envio):
        self.direccion_envio = direccion_envio
        self.save()


def enviarOrden(sender, instance, *args, **kwargs):
    if not instance.ordenID:
        instance.ordenID = str(uuid.uuid4())

def enviar_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()

pre_save.connect(enviarOrden, sender=Orden)
pre_save.connect(enviar_total, sender=Orden)