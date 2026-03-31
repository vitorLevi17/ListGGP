from django.db import models
from django.contrib.auth.models import User

class Aula(models.Model):
    nm_aula = models.CharField(max_length=150)
    descricao = models.CharField(max_length=200)
    palestrante = models.CharField(max_length=100)
    carga_horaria = models.TimeField(null=False)
    data_criacao = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
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
        ("ANDAMENTO","andamento")
    ]

    nm_evento = models.CharField(max_length=100)
    data = models.DateTimeField()
    local = models.CharField(max_length=50,choices=opcoes_local)
    status = models.CharField(max_length=50,choices=opcoes_status)
    participantes = models.JSONField(default=list,blank=True)
    aulas = models.ManyToManyField(Aula, related_name='aulas')
    horario_final = models.TimeField(null=True,blank=True)
    usuario_cadastrante = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self):
        return self.nm_evento