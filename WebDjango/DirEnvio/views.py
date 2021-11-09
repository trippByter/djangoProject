from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from orden.utils import funcionOrden
from .models import DireccionEnvio
from django.views.generic import ListView # De esta clase se hereda para EnvioDirecciones
from .forms import DireccionEnvioForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin 
from django.shortcuts import reverse
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from carts.funciones import funcionCarrito

# Create your views here.

class EnvioDirecciones(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = DireccionEnvio
    template_name = 'direccion_envios/direccion_envio.html'
    # Método para sobreescribir el queryset con la dir default. El default aparacerá primero
    def get_queryset(self):
        return DireccionEnvio.objects.filter(user=self.request.user).order_by('-default')


# Función que renderiza un formulario que permite agregar nueva dirección
@login_required(login_url='login')
def FormularioDir(request):
    # Instancia de DireccionEnvioForm de forms.py, para crear un nuevo formulario
    form = DireccionEnvioForm(request.POST or None) # Aseguramos que al peticion sea un metodo POST
    if request.method == 'POST' and form.is_valid():
        direccion_envio = form.save(commit=False) # Aqui se genera la instancia. No se guarda aun
        direccion_envio.user = request.user
        direccion_envio.default = not request.user.has_direccion_envio() # Aqui la primera dir queda como default
        direccion_envio.save() # Aqui se guarda la direccion

        if request.GET.get('next'):
            if request.GET['next'] == reverse('direccion'):
                cart = funcionCarrito(request)
                orden = funcionOrden(cart, request)
                orden.update_direccion_envio(direccion_envio)

                return HttpResponseRedirect(request.GET['next'])

        messages.success(request, 'Direccion creada correctamente') # Mensaje de creacion correcta
        return redirect('direccion_envio') # Una vez ingresada la dir, se redirige a pagina con todas las direcciones
    # Return de FormularioDir. Renderiza a través de formulario.html
    return render(request, 'direccion_envios/formulario.html', {
        'form' : form, # Contexto 'form' instanciado del model DireccionEnvioForm
    })


class UpdateDireccion(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    model = DireccionEnvio
    form_class = DireccionEnvioForm
    template_name = 'direccion_envios/actualizar.html'
    success_message = 'Direccion Actualizada'

    def get_success_url(self):
        return reverse('direccion_envio')


class DeleteDireccion(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = DireccionEnvio
    template_name = 'direccion_envios/delete.html'
    success_url = reverse_lazy('direccion_envio')
    
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().default:
            return redirect('direccion_envio')

        if self.get_object().has_orden():
            messages.error(request, 'Esta direccion está asociada a una compra, no se puede eliminar.')
            return redirect('direccion_envio')

        if request.user.id != self.get_object().user_id:
            return redirect('index')

        return super(DeleteDireccion, self).dispatch(request, *args, **kwargs)


@login_required(login_url='login')
def FunDefault(request, pk):
    direccion_envio = get_object_or_404(DireccionEnvio, pk=pk)

    if request.user.id != direccion_envio.user_id:
        return redirect('index')

    if request.user.has_direccion_envio():
        request.user.direccion_envio.update_default()

    direccion_envio.update_default(True)

    return redirect('direccion_envio')


