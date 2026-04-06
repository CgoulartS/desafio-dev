from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'cpf', 'telefone']
    search_fields = ['nome', 'email', 'cpf']
    readonly_fields = ['id', 'created_at', 'updated_at']
