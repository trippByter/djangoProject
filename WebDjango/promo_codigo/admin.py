from django.contrib import admin
#importar la clase para poder entrar a ella desde el panel admin web"
from .models import PromoCodigo

# Register your models here.

#Excluir el codigo del web admin, para que se genere autom. y no manual
class CodigoPromoAdmin(admin.ModelAdmin):
    exclude = ['codigo']


admin.site.register(PromoCodigo, CodigoPromoAdmin)