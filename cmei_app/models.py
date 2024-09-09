from django.db import models

class CMEI(models.Model):
    codCmei = models.AutoField(primary_key=True)  # Campo auto-incremento
    nomeCmei = models.CharField(max_length=100)
    

    def __str__(self):
        return self.nomeCmei  # Retorna o nome do CMEI ao imprimir o objeto