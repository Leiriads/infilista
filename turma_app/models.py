from django.db import models
from cmei_app.models import CMEI  # Certifique-se de importar o modelo CMEI

class Turma(models.Model):
    codTurma = models.AutoField(primary_key=True)  # Campo auto-incremento
    nomeTurma = models.CharField(max_length=20)
    observacaoTurma = models.CharField(max_length=100)
    cmei = models.ForeignKey(CMEI, on_delete=models.CASCADE)  # Remover related_name

    def __str__(self):
        return self.nomeTurma
