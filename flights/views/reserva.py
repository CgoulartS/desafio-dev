from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from flights.forms import ReservaForm
from flights.models import Reserva
from .mixins import StaffRequiredMixin


class ReservaListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'flights/reserva_list.html'
    context_object_name = 'reservas'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('cliente', 'voo', 'voo__aviao')
        if not self.request.user.is_staff:
            qs = qs.filter(cliente__usuario=self.request.user)
        return qs


class ReservaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'flights/reserva_form.html'
    success_url = reverse_lazy('reserva-list')
    success_message = 'Reserva criada com sucesso!'


class ReservaUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'flights/reserva_form.html'
    success_url = reverse_lazy('reserva-list')
    success_message = 'Reserva atualizada com sucesso!'


class ReservaDeleteView(LoginRequiredMixin, DeleteView):
    model = Reserva
    template_name = 'flights/reserva_confirm_delete.html'
    success_url = reverse_lazy('reserva-list')

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(cliente__usuario=self.request.user)
        return qs

    def form_valid(self, form):
        messages.success(self.request, 'Reserva cancelada com sucesso!')
        return super().form_valid(form)
