# Create your models here.

from django.db import models

class Crianca(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    responsavel = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.nome
