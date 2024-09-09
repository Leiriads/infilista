from django.db import models

class Crianca(models.Model):
    codCrianca = models.AutoField(primary_key=True)
    nomeCrianca = models.CharField(max_length=100)
    dataNascCrianca = models.DateField()
    nomeResponsavel = models.CharField(max_length=100)
    telefoneResponsavel = models.CharField(max_length=11)
    emailResponsavel = models.CharField(max_length=100)
    cpfResponsavel = models.CharField(max_length=11)
    dataInicialCadastro = models.DateField()
    dataFinalCadastro = models.DateField(null=True, blank=True)
    observacao = models.CharField(max_length=100)
    nomeUsuario = models.CharField(max_length=100)

    def __str__(self):
        return self.nomeCrianca  # Retorna o nome da criança ao imprimir o objeto
