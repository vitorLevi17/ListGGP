from django.db import models

# Create your models here.
#AULAS
#SETORES
#TREINAMENTOS
class Aula(models.Model):
    nm_aula = models.CharField(max_length=150)
    descricao = models.CharField(max_length=200)
    palestrante = models.CharField(max_length=100)
    carga_horaria = models.IntegerField(null=False)
    

