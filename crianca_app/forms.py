from django import forms
from .models import Crianca

class CriancaForm(forms.ModelForm):
    class Meta:
        model = Crianca
        fields = [
            'nomeCrianca',
            'dataNascCrianca',
            'nomeResponsavel',
            'telefoneResponsavel',
            'emailResponsavel',
            'cpfResponsavel',
            'observacao',
        ]
        widgets = {
            'dataNascCrianca': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(CriancaForm, self).__init__(*args, **kwargs)
        self.fields['observacao'].required = False  # Tornando o campo "observacao" opcional
