import uuid
from django.db import models
from django.db.models import UniqueConstraint
from .cliente import Cliente
from .voo import Voo


class Reserva(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas')
    voo = models.ForeignKey(Voo, on_delete=models.CASCADE, related_name='reservas')
    numero_assento = models.PositiveIntegerField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        constraints = [
            UniqueConstraint(fields=['voo', 'numero_assento'], name='unique_assento_por_voo'),
            UniqueConstraint(fields=['voo', 'cliente'], name='unique_cliente_por_voo'),
        ]

    def __str__(self):
        return f'{self.cliente.nome} - Voo {self.voo} - Assento {self.numero_assento}'
