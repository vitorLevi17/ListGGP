from django import forms
from .models import Treinamento,Aula

class CriarEventoForm(forms.ModelForm):
    
    class Meta:
        model = Treinamento
        fields = ['nm_evento', 'data', 'local', 'aulas']
        
        widgets = {
            'nm_evento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Treinamento de Integração'}),
            'data': forms.DateTimeInput(format='%Y-%m-%dT%H:%M',attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'local': forms.Select(attrs={'class': 'form-select'}),
            'aulas': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

class CriarAulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ['nm_aula', 'descricao', 'palestrante', 'carga_horaria']
        
        widgets = {
            'nm_aula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Segurança do Trabalho'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breve descrição do conteúdo'}),
            'palestrante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do instrutor'}),
            'carga_horaria': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }