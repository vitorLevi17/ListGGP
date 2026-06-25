from django.db import models
from django.contrib.auth.models import User

class Aula(models.Model):
    nm_aula = models.CharField(max_length=150)
    descricao = models.CharField(max_length=200)
    palestrante = models.CharField(max_length=100)
    carga_horaria = models.TimeField(null=False)
    data_criacao = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    horario_inicial_aula = models.TimeField(null=True,blank=True)
    horario_final_aula = models.TimeField(null=True,blank=True)
    
    def __str__(self):
        return self.nm_aula

class Treinamento(models.Model):

    opcoes_local = [
        ("CARAVANA - UNIDADES SANTA CASA IN LOCO", "CARAVANA - UNIDADES SANTA CASA IN LOCO"),
        ("PUPILEIRA - SALÃO RAINHA LEONOR", "PUPILEIRA - SALÃO RAINHA LEONOR"),
        ("PUPILEIRA - SALÃO M", "PUPILEIRA - SALÃO M"),
        ("CASA AZUL GGP - SALA", "CASA AZUL GGP - SALA"),
        ("MUSEU - AUDITÓRIO", "MUSEU - AUDITÓRIO"),
        ("HMC - AUDITÓRIO", "HMC - AUDITÓRIO"),
        ("CERII - SALA", "CERII - SALA"),
        ("CASA SOLANGE FRAGA - SALA", "CASA SOLANGE FRAGA - SALA"),
        ("CASA DA LADEIRA - SALA", "CASA DA LADEIRA - SALA"),
        ("CCS - SALA", "CCS - SALA"),
        ("FSC - SALA DE AULA", "FSC - SALA DE AULA"),
        ("HSI - AUDITÓRIO JORGE FIGUEIRA", "HSI - AUDITÓRIO JORGE FIGUEIRA"),
        ("HSI - LABORATÓRIO DE INFORMÁTICA", "HSI - LABORATÓRIO DE INFORMÁTICA"),
        ("HSI - SALÃO NOBRE", "HSI - SALÃO NOBRE"),
        ("HSI - SALÃO PRETO E BRANCO", "HSI - SALÃO PRETO E BRANCO"),
        ("HSI - SALA DE TREINAMENTO 01", "HSI - SALA DE TREINAMENTO 01"),
        ("HSI - SALA DE TREINAMENTO 02", "HSI - SALA DE TREINAMENTO 02"),
        ("HSI - SALA DE TREINAMENTO 03", "HSI - SALA DE TREINAMENTO 03"),
        ("HSI - SALA DE TREINAMENTO 04", "HSI - SALA DE TREINAMENTO 04"),
        ("HSI - SALA DE CONFERÊNCIA (SENEP)", "HSI - SALA DE CONFERÊNCIA (SENEP)"),
        ("HMS - SALA DO LEAN", "HMS - SALA DO LEAN"),
        ("HMS - SALA DE TREINAMENTO 01", "HMS - SALA DE TREINAMENTO 01"),
        ("HMS - SALA DE TREINAMENTO 02", "HMS - SALA DE TREINAMENTO 02"),
        ("HMS - SALA DE TREINAMENTO 03", "HMS - SALA DE TREINAMENTO 03"),
    ]
    
    opcoes_status = [
        ("FINALIZADO", "finalizado"),
        ("CANCELADO", "cancelado"),
        ("MARCADO", "marcado"),
        ("ANDAMENTO", "andamento")
    ]

    nm_evento = models.CharField(max_length=100)
    data = models.DateTimeField()
    local = models.CharField(max_length=50, choices=opcoes_local)
    status = models.CharField(max_length=50, choices=opcoes_status)
    participantes = models.JSONField(default=list, blank=True)
    aulas = models.ManyToManyField(Aula, related_name='aulas')
    horario_final = models.TimeField(null=True, blank=True)
    usuario_cadastrante = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nm_evento