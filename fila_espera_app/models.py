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
        # Se a ordem não foi definida, calculamos o valor sequencial
        if self.ordem is None:
            # Obtém o maior valor de 'ordem' na mesma turma
            ultimo_na_turma = ListaEspera.objects.filter(turma=self.turma).order_by('ordem').last()
            if ultimo_na_turma:
                self.ordem = ultimo_na_turma.ordem + 1
            else:
                self.ordem = 1  # Se for o primeiro da turma, começa com 1
        
        # Se o status for confirmado e não houver dataSaida, atribui a dataEntrada
        if self.pk and self.status == 'confirmado' and not self.dataSaida:
            self.dataSaida = self.dataEntrada
        
        # Salva o registro
        super().save(*args, **kwargs)
