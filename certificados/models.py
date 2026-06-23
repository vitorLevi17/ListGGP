from django.db import models
from django.contrib.auth.models import User

class Certificado(models.Model):

    opcoes_status = [
        ("APROVADO","aprovado"),
        ("REPROVADO","reprovado"),
        ("AGUARDANDO ANÁLISE","aguardando análise")
    ]

    nm_certificado = models.CharField(max_length=150)
    carga_horaria = models.TimeField(null=False)
    palestrante = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    status = models.CharField(max_length=50,choices=opcoes_status)
    url = models.URLField(max_length=500, blank=True, null=True)
    id_usuario = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.nm_certificado