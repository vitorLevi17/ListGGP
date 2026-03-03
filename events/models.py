from django.db import models

class Aula(models.Model):
    nm_aula = models.CharField(max_length=150)
    descricao = models.CharField(max_length=200)
    palestrante = models.CharField(max_length=100)
    carga_horaria = models.IntegerField(null=False)
    
    def __str__(self):
        return self.nm_aula

class Treinamento(models.Model):

    opcoes_local = [
        ("AUDITORIO HSI","hsi"),
        ("AUDITORIO ADM CENTRAL","pupileira"),
    ]
    opcoes_status = [
        ("FINALIZADO","finalizado"),
        ("CANCELADO","cancelado"),
        ("MARCADO","marcado"),
    ]

    nm_evento = models.CharField(max_length=100)
    data = models.DateField()
    local = models.CharField(max_length=50,choices=opcoes_local)
    status = models.CharField(max_length=50,choices=opcoes_status)
    participantes = models.JSONField(default=list,blank=True)
    aulas = models.ManyToManyField(Aula, related_name='aulas')

    def __str__(self):
        return self.nm_evento