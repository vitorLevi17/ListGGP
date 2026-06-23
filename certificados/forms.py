from django import forms
from .models import Certificado

class CriarCertificadoForm(forms.ModelForm):

    class Meta:
        model = Certificado
        fields = ['nm_certificado',
        'carga_horaria', 
        'palestrante' ,
        'empresa',
        'descricao'
        #,'url'
        ]

        widgets = {
        'nm_certificado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Treinamento de Integração'}),
        'carga_horaria': forms.TimeInput(format='%H:%M',attrs={'type':'time','class': 'form-control','min':'00:05'}),
        'palestrante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do instrutor'}),
        'empresa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da empresa ofertante do curso'}),
        'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breve descrição do conteúdo'})
        #'url'
        }
