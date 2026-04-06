from django import forms
from voos.models import Voo


class VooForm(forms.ModelForm):
    class Meta:
        model = Voo
        fields = ['aviao', 'origem', 'destino', 'data', 'horario']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
        }
