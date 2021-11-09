from django import forms
from django.contrib.auth.models import User
from users.models import User
# Formulario para registrar nuevos usuarios
# Se agregan clases de bootstrap a través de dicc key value
class Registro(forms.Form):
    username = forms.CharField(
        required=True, 
        min_length=5, 
        max_length=40,
        widget=forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder' : 'Usuario',
        })
    )
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs={
            'class' : 'form-control',
            'placeholder' : 'ejemplo@yimail.com',
        })
    )
    password = forms.CharField(required=True,
        widget=forms.PasswordInput(attrs={
            'class' : 'form-control',
            'placeholder' : 'Clave',
        })
    )
    password2 = forms.CharField(
        required=True,
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class' : 'form-control',
            'placeholder' : 'Confirmar contraseña',
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Usuario ya creado.')
    
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Correo ya creado.')
    
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'Las contraseñas no coinciden.')
    
    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )