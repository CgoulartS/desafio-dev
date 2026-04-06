from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from voos.forms import AviaoForm
from voos.models import Aviao
from .mixins import StaffRequiredMixin


class AviaoListView(LoginRequiredMixin, ListView):
    model = Aviao
    template_name = 'voos/aviao_list.html'
    context_object_name = 'avioes'
    paginate_by = 10


class AviaoCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Aviao
    form_class = AviaoForm
    template_name = 'voos/aviao_form.html'
    success_url = reverse_lazy('aviao-list')
    success_message = 'Aviao cadastrado com sucesso!'


class AviaoUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Aviao
    form_class = AviaoForm
    template_name = 'voos/aviao_form.html'
    success_url = reverse_lazy('aviao-list')
    success_message = 'Aviao atualizado com sucesso!'


class AviaoDeleteView(StaffRequiredMixin, DeleteView):
    model = Aviao
    template_name = 'voos/aviao_confirm_delete.html'
    success_url = reverse_lazy('aviao-list')

    def form_valid(self, form):
        messages.success(self.request, 'Aviao excluido com sucesso!')
        return super().form_valid(form)
