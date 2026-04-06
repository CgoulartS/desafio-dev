from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from flights.forms import AviaoForm
from flights.models import Aviao
from .mixins import StaffRequiredMixin


class AviaoListView(LoginRequiredMixin, ListView):
    model = Aviao
    template_name = 'flights/aviao_list.html'
    context_object_name = 'avioes'
    paginate_by = 10


class AviaoCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Aviao
    form_class = AviaoForm
    template_name = 'flights/aviao_form.html'
    success_url = reverse_lazy('aviao-list')
    success_message = 'Avião cadastrado com sucesso!'


class AviaoUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Aviao
    form_class = AviaoForm
    template_name = 'flights/aviao_form.html'
    success_url = reverse_lazy('aviao-list')
    success_message = 'Avião atualizado com sucesso!'


class AviaoDeleteView(StaffRequiredMixin, DeleteView):
    model = Aviao
    template_name = 'flights/aviao_confirm_delete.html'
    success_url = reverse_lazy('aviao-list')

    def form_valid(self, form):
        messages.success(self.request, 'Avião excluído com sucesso!')
        return super().form_valid(form)
