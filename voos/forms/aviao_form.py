from django import forms
from voos.models import Aviao


class AviaoForm(forms.ModelForm):
    class Meta:
        model = Aviao
        fields = ['modelo', 'fabricante', 'max_passageiros']

    def clean_max_passageiros(self):
        max_passageiros = self.cleaned_data.get('max_passageiros')
        if max_passageiros is not None and max_passageiros <= 0:
            raise forms.ValidationError('A capacidade maxima deve ser maior que 0.')
        return max_passageiros
