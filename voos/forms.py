from django import forms
from .models import Aviao, Voo, Cliente, Reserva


class AviaoForm(forms.ModelForm):
    class Meta:
        model = Aviao
        fields = ['modelo', 'fabricante', 'max_passageiros']

    def clean_max_passageiros(self):
        max_passageiros = self.cleaned_data.get('max_passageiros')
        if max_passageiros is not None and max_passageiros <= 0:
            raise forms.ValidationError('A capacidade maxima deve ser maior que 0.')
        return max_passageiros


class VooForm(forms.ModelForm):
    class Meta:
        model = Voo
        fields = ['aviao', 'origem', 'destino', 'data', 'horario']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'cpf', 'telefone']

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if not cpf.isdigit() or len(cpf) != 11:
            raise forms.ValidationError('CPF deve conter exatamente 11 digitos numericos.')
        return cpf


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'voo', 'numero_assento']

    def clean(self):
        cleaned_data = super().clean()
        voo = cleaned_data.get('voo')
        cliente = cleaned_data.get('cliente')
        numero_assento = cleaned_data.get('numero_assento')

        if voo and numero_assento:
            max_pass = voo.aviao.max_passageiros

            if numero_assento > max_pass:
                raise forms.ValidationError(
                    f'Assento {numero_assento} invalido. O aviao comporta no maximo {max_pass} passageiros.'
                )

            qs = Reserva.objects.filter(voo=voo, numero_assento=numero_assento)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(
                    f'Assento {numero_assento} ja esta ocupado neste voo.'
                )

        if voo:
            reservas_count = voo.reservas.count()
            if self.instance.pk:
                reservas_count -= 1
            if reservas_count >= voo.aviao.max_passageiros:
                raise forms.ValidationError('Este voo ja esta com capacidade maxima.')

        if voo and cliente:
            qs = Reserva.objects.filter(voo=voo, cliente=cliente)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Este cliente ja possui reserva neste voo.')

        return cleaned_data
