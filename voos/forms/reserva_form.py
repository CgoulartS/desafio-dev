from django import forms
from django.core.exceptions import ValidationError as DjangoValidationError
from voos.models import Reserva
from voos.services import ReservaService


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'voo', 'numero_assento']

    def clean(self):
        cleaned_data = super().clean()
        voo = cleaned_data.get('voo')
        cliente = cleaned_data.get('cliente')
        numero_assento = cleaned_data.get('numero_assento')
        excluir_pk = self.instance.pk if self.instance.pk else None

        try:
            if voo and numero_assento:
                ReservaService.validar_assento(voo, numero_assento, excluir_pk)
            if voo:
                ReservaService.validar_capacidade(voo, excluir_pk)
            if voo and cliente:
                ReservaService.validar_cliente_unico(voo, cliente, excluir_pk)
        except DjangoValidationError as e:
            raise forms.ValidationError(e.message)

        return cleaned_data
