from django.db import models
from django.db.models import UniqueConstraint
from core.models import BaseModel
from accounts.models import Cliente
from .voo import Voo


class Reserva(BaseModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas')
    voo = models.ForeignKey(Voo, on_delete=models.CASCADE, related_name='reservas')
    numero_assento = models.PositiveIntegerField()

    class Meta:
        ordering = ['-created_at']
        constraints = [
            UniqueConstraint(fields=['voo', 'numero_assento'], name='unique_assento_por_voo'),
            UniqueConstraint(fields=['voo', 'cliente'], name='unique_cliente_por_voo'),
        ]

    def __str__(self):
        return f'{self.cliente.nome} - Voo {self.voo} - Assento {self.numero_assento}'
