from django import forms
from .models import Crianca

class CriancaForm(forms.ModelForm):
    class Meta:
        model = Crianca
        fields = ['nome', 'idade', 'responsavel', 'telefone']
