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
    form = DireccionEnvioForm(request.POST or None) 
    if request.method == 'POST' and form.is_valid():
        direccion_envio = form.save(commit=False)
        direccion_envio.user = request.user
        direccion_envio.default = not request.user.has_direccion_envio()
        direccion_envio.save()

        if request.GET.get('next'):
            if request.GET['next'] == reverse('direccion'):
                cart = funcionCarrito(request)
                orden = funcionOrden(cart, request)
                orden.update_direccion_envio(direccion_envio)

                return HttpResponseRedirect(request.GET['next'])

        messages.success(request, 'Direccion creada correctamente')
        return redirect('direccion_envio')
    # Return de FormularioDir. Renderiza a través de formulario.html
    return render(request, 'direccion_envios/formulario.html', {
        # Contexto 'form' instanciado del model DireccionEnvioForm
        'form' : form,
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


