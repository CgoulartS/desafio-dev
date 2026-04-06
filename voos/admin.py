from django.contrib import admin
from .models import Aviao, Voo, Cliente, Reserva


@admin.register(Aviao)
class AviaoAdmin(admin.ModelAdmin):
    list_display = ['modelo', 'fabricante', 'max_passageiros']
    search_fields = ['modelo', 'fabricante']
    list_filter = ['fabricante']


@admin.register(Voo)
class VooAdmin(admin.ModelAdmin):
    list_display = ['origem', 'destino', 'data', 'horario', 'aviao']
    search_fields = ['origem', 'destino']
    list_filter = ['data', 'aviao']
    date_hierarchy = 'data'
    list_select_related = ['aviao']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'cpf', 'telefone']
    search_fields = ['nome', 'email', 'cpf']
    readonly_fields = ['id']


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'voo', 'numero_assento', 'criado_em']
    search_fields = ['cliente__nome', 'voo__origem', 'voo__destino']
    list_filter = ['voo__data', 'criado_em']
    readonly_fields = ['id', 'criado_em']
    list_select_related = ['cliente', 'voo', 'voo__aviao']
