from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login as lg
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from .forms import Registro
from users.models import User
from products.models import Product
from django.http import HttpResponseRedirect
# Request contiene metadatos de la peticion de la página. En este caso index.html
def index(request):
    productos = Product.objects.all()
    # Render recibe la peticion request||En el HTML devulve la rpta||El dicc es para el contexto que se muestran en el html
    return render(request, 'index.html', { 
        'mensaje' : 'Ingreso',  # Contexto que se envia al templates/index.html|{{mensaje}}
        'titulo' : 'Personas',
        'productos' : productos,
    })


def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuarios= authenticate(username=username, password=password)
        if usuarios:
            lg(request, usuarios)
            messages.success(request, f'Hola {usuarios.username}, que tal.')
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'])
            return redirect('index')
        else:
            messages.error(request, 'Datos incorrectos')

    return render(request, 'users/login.html', {})


def salir(request):
    logout(request)
    messages.success(request, 'Good logout.')
    return redirect(login)


def registro(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = Registro(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        usuario = form.save()
        if usuario:
            lg(request, usuario)
            messages.success(request, f'Registro correcto, bienvenido {usuario}.')
            return redirect('index')

    return render(request, 'users/registro.html', {
        'form' : form
    })
