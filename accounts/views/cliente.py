from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from accounts.forms import ClienteForm
from accounts.models import Cliente


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class ClienteListView(StaffRequiredMixin, ListView):
    model = Cliente
    template_name = 'accounts/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(Q(nome__icontains=q) | Q(email__icontains=q) | Q(cpf__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


class ClienteCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'accounts/cliente_form.html'
    success_url = reverse_lazy('cliente-list')
    success_message = 'Cliente cadastrado com sucesso!'


class ClienteUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'accounts/cliente_form.html'
    success_url = reverse_lazy('cliente-list')
    success_message = 'Cliente atualizado com sucesso!'


class ClienteDeleteView(StaffRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'accounts/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente-list')

    def form_valid(self, form):
        messages.success(self.request, 'Cliente excluído com sucesso!')
        return super().form_valid(form)
