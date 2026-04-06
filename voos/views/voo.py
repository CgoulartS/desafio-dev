from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from voos.forms import VooForm
from voos.models import Voo
from voos.services import ReservaService
from .mixins import StaffRequiredMixin


class VooListView(LoginRequiredMixin, ListView):
    model = Voo
    template_name = 'voos/voo_list.html'
    context_object_name = 'voos'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('aviao')
        q = self.request.GET.get('q', '')
        data = self.request.GET.get('data', '')
        if q:
            qs = qs.filter(Q(origem__icontains=q) | Q(destino__icontains=q))
        if data:
            qs = qs.filter(data=data)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['data_filtro'] = self.request.GET.get('data', '')
        return context


class VooDetailView(LoginRequiredMixin, DetailView):
    model = Voo
    template_name = 'voos/voo_detail.html'
    context_object_name = 'voo'


class VooCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Voo
    form_class = VooForm
    template_name = 'voos/voo_form.html'
    success_url = reverse_lazy('voo-list')
    success_message = 'Voo cadastrado com sucesso!'


class VooUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Voo
    form_class = VooForm
    template_name = 'voos/voo_form.html'
    success_url = reverse_lazy('voo-list')
    success_message = 'Voo atualizado com sucesso!'


class VooDeleteView(StaffRequiredMixin, DeleteView):
    model = Voo
    template_name = 'voos/voo_confirm_delete.html'
    success_url = reverse_lazy('voo-list')

    def form_valid(self, form):
        messages.success(self.request, 'Voo excluido com sucesso!')
        return super().form_valid(form)


class VooAssentosView(LoginRequiredMixin, View):
    def get(self, request, pk):
        voo = Voo.objects.select_related('aviao').get(pk=pk)
        return JsonResponse({
            'max_passageiros': voo.aviao.max_passageiros,
            'assentos_ocupados': ReservaService.obter_assentos_ocupados(voo),
        })
