from django import forms
from .models import Turma, CMEI

class TurmaForm(forms.ModelForm):
    codTurma = forms.CharField(
        required=False,  # Campo não obrigatório para edição
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'uk-input'})
    )

    class Meta:
        model = Turma
        fields = ['codTurma', 'nomeTurma', 'observacaoTurma', 'cmei']
        widgets = {
            'cmei': forms.Select(attrs={'class': 'uk-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(TurmaForm, self).__init__(*args, **kwargs)
        self.fields['observacaoTurma'].required = False  # Tornando o campo "observacao" opcional
