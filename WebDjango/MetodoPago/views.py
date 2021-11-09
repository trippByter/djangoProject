from django.shortcuts import render
from django.contrib.auth.decorators import login_required # Importar decoradoes para restringir acceso a usuario no reguistafos
# Create your views here.
# Se recibe la request y se renderiza en el profile_pago.html
@login_required(login_url='login')
def crear(request):
    return render(request, 'metodos_pago/profile_pago.html', {

    })