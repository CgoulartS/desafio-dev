from django.contrib import admin
from .models import Aviao, Voo, Reserva


@admin.register(Aviao)
class AviaoAdmin(admin.ModelAdmin):
    list_display = ['modelo', 'fabricante', 'max_passageiros']
    search_fields = ['modelo', 'fabricante']
    list_filter = ['fabricante']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Voo)
class VooAdmin(admin.ModelAdmin):
    list_display = ['origem', 'destino', 'data', 'horario', 'aviao']
    search_fields = ['origem', 'destino']
    list_filter = ['data', 'aviao']
    date_hierarchy = 'data'
    list_select_related = ['aviao']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'voo', 'numero_assento', 'created_at']
    search_fields = ['cliente__nome', 'voo__origem', 'voo__destino']
    list_filter = ['voo__data', 'created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_select_related = ['cliente', 'voo', 'voo__aviao']
