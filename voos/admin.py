from django.contrib import admin
from .models import Aviao, Voo, Cliente, Reserva


@admin.register(Aviao)
class AviaoAdmin(admin.ModelAdmin):
    list_display = ['modelo', 'fabricante', 'max_passageiros']


@admin.register(Voo)
class VooAdmin(admin.ModelAdmin):
    list_display = ['origem', 'destino', 'data', 'horario', 'aviao']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'cpf', 'telefone']


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'voo', 'numero_assento', 'criado_em']
