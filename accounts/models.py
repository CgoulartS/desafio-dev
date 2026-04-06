from django.conf import settings
from django.db import models
from core.models import BaseModel


class Cliente(BaseModel):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clientes',
    )
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=20)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome
