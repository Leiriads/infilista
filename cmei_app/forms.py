from django import forms
from cmei_app.models import CMEI

class CMEIForm(forms.ModelForm):
    class Meta:
        model = CMEI
        fields = [
            'nomeCmei',
        ]

