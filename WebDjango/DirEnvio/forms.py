from django.forms import ModelForm
from .models import DireccionEnvio

class DireccionEnvioForm(ModelForm):
    class Meta:
        model = DireccionEnvio
        fields = [
            'line1', 'line2', 'city', 'state', 'postal_code', 'reference',
        ]
        labels = {
            'line1': 'Calle 1',
            'line2': 'Calle 2',
            'city': 'Ciudad',
            'state': 'Region',
            'postal_code': 'Codigo Postal',
            'reference': 'Referencia',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['line1'].widget.attrs.update({
            'class' : 'form-control',
        })
        self.fields['line2'].widget.attrs.update({
            'class' : 'form-control',
        })
        self.fields['city'].widget.attrs.update({
            'class' : 'form-control',
        })
        self.fields['state'].widget.attrs.update({
            'class' : 'form-control',
        })
        self.fields['postal_code'].widget.attrs.update({
            'class' : 'form-control',
            'placeholder' : '9876543',
        })
        self.fields['reference'].widget.attrs.update({
            'class' : 'form-control',
            'placeholder' : '(Ejemplo: Portón Blanco)',
        })
        