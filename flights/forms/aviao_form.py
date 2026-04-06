from django import forms
from flights.models import Aviao


class AviaoForm(forms.ModelForm):
    class Meta:
        model = Aviao
        fields = ['modelo', 'fabricante', 'max_passageiros']

    def clean_max_passageiros(self):
        v = self.cleaned_data.get('max_passageiros')
        if v is not None and v <= 0:
            raise forms.ValidationError('A capacidade máxima deve ser maior que 0.')
        return v
