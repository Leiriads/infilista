from django.db import models
from crianca_app.models import Crianca
from turma_app.models import Turma

class ListaEspera(models.Model):
    STATUS_CHOICES = [
        ('confirmado', 'Confirmado'),
        ('nao_confirmado', 'Não Confirmado'),
    ]
    
    crianca = models.ForeignKey(Crianca, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    dataEntrada = models.DateField(auto_now_add=True)
    dataSaida = models.DateField(null=True, blank=True)
    ordem = models.IntegerField(null=True, blank=True)
    criterio = models.CharField(max_length=40)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='nao_confirmado')

    def save(self, *args, **kwargs):
        #print(f"Salvando: {self}")  # Adicione esta linha para depuração
        if self.pk and self.status == 'confirmado':
            if not self.dataSaida:
                self.dataSaida = self.dataEntrada
        super().save(*args, **kwargs)
