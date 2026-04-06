from django import forms
from accounts.models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'cpf', 'telefone']

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if not cpf.isdigit() or len(cpf) != 11:
            raise forms.ValidationError('CPF deve conter exatamente 11 dígitos numéricos.')
        return cpf
