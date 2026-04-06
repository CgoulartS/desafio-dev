from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView,
)

from .forms import AviaoForm, ClienteForm, ReservaForm, VooForm
from .models import Aviao, Cliente, Reserva, Voo


# --- Story 3.1: Dashboard ---

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'voos/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_avioes'] = Aviao.objects.count()
        context['total_voos'] = Voo.objects.count()
        context['total_clientes'] = Cliente.objects.count()
        context['total_reservas'] = Reserva.objects.count()

        voos_com_dados = Voo.objects.annotate(
            num_reservas=Count('reservas')
        ).select_related('aviao')

        total_reservas = sum(v.num_reservas for v in voos_com_dados)
        total_capacidade = sum(v.aviao.max_passageiros for v in voos_com_dados)
        context['taxa_ocupacao'] = round(
            (total_reservas / total_capacidade * 100), 1
        ) if total_capacidade > 0 else 0

        context['proximos_voos'] = Voo.objects.filter(
            data__gte=date.today()
        ).select_related('aviao').order_by('data', 'horario')[:5]

        return context


# --- Aviao CRUD ---

class AviaoListView(LoginRequiredMixin, ListView):
    model = Aviao
    template_name = 'voos/aviao_list.html'
    context_object_name = 'avioes'
    paginate_by = 10


class AviaoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Aviao
    form_class = AviaoForm
    template_name = 'voos/aviao_form.html'
    success_url = reverse_lazy('aviao-list')
    success_message = 'Aviao cadastrado com sucesso!'


class AviaoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Aviao
    form_class = AviaoForm
    template_name = 'voos/aviao_form.html'
    success_url = reverse_lazy('aviao-list')
    success_message = 'Aviao atualizado com sucesso!'


class AviaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Aviao
    template_name = 'voos/aviao_confirm_delete.html'
    success_url = reverse_lazy('aviao-list')

    def form_valid(self, form):
        messages.success(self.request, 'Aviao excluido com sucesso!')
        return super().form_valid(form)


# --- Voo CRUD (Story 3.2: filtros) ---

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


class VooCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Voo
    form_class = VooForm
    template_name = 'voos/voo_form.html'
    success_url = reverse_lazy('voo-list')
    success_message = 'Voo cadastrado com sucesso!'


class VooUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Voo
    form_class = VooForm
    template_name = 'voos/voo_form.html'
    success_url = reverse_lazy('voo-list')
    success_message = 'Voo atualizado com sucesso!'


class VooDeleteView(LoginRequiredMixin, DeleteView):
    model = Voo
    template_name = 'voos/voo_confirm_delete.html'
    success_url = reverse_lazy('voo-list')

    def form_valid(self, form):
        messages.success(self.request, 'Voo excluido com sucesso!')
        return super().form_valid(form)


# --- Story 3.4: Endpoint JSON de assentos ---

class VooAssentosView(LoginRequiredMixin, View):
    def get(self, request, pk):
        voo = Voo.objects.select_related('aviao').get(pk=pk)
        assentos_ocupados = list(
            voo.reservas.values_list('numero_assento', flat=True)
        )
        return JsonResponse({
            'max_passageiros': voo.aviao.max_passageiros,
            'assentos_ocupados': assentos_ocupados,
        })


# --- Cliente CRUD (Story 3.2: filtros) ---

class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'voos/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(
                Q(nome__icontains=q) | Q(email__icontains=q) | Q(cpf__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


class ClienteCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'voos/cliente_form.html'
    success_url = reverse_lazy('cliente-list')
    success_message = 'Cliente cadastrado com sucesso!'


class ClienteUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'voos/cliente_form.html'
    success_url = reverse_lazy('cliente-list')
    success_message = 'Cliente atualizado com sucesso!'


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'voos/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente-list')

    def form_valid(self, form):
        messages.success(self.request, 'Cliente excluido com sucesso!')
        return super().form_valid(form)


# --- Reserva CRUD ---

class ReservaListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'voos/reserva_list.html'
    context_object_name = 'reservas'
    paginate_by = 10


class ReservaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'voos/reserva_form.html'
    success_url = reverse_lazy('reserva-list')
    success_message = 'Reserva criada com sucesso!'


class ReservaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'voos/reserva_form.html'
    success_url = reverse_lazy('reserva-list')
    success_message = 'Reserva atualizada com sucesso!'


class ReservaDeleteView(LoginRequiredMixin, DeleteView):
    model = Reserva
    template_name = 'voos/reserva_confirm_delete.html'
    success_url = reverse_lazy('reserva-list')

    def form_valid(self, form):
        messages.success(self.request, 'Reserva cancelada com sucesso!')
        return super().form_valid(form)
