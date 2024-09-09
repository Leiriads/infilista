from django import forms
from .models import ListaEspera
from crianca_app.models import Crianca
from turma_app.models import Turma

class ListaEsperaForm(forms.ModelForm):
    class Meta:
        model = ListaEspera
        fields = ['turma', 'criterio', 'status']

    def __init__(self, *args, **kwargs):
        codCmei = kwargs.pop('codCmei', None)
        super().__init__(*args, **kwargs)
        
        if codCmei:
            self.fields['turma'].queryset = Turma.objects.filter(cmei__codCmei=codCmei)
        else:
            self.fields['turma'].queryset = Turma.objects.none()
    
        
        # Adicionar debug para verificar os valores disponíveis e recebidos
        #print(f"Queryset de turmas: {self.fields['turma'].queryset}")
        #print(f"Valor enviado para turma: {self.data.get('turma')}")
