from django import forms
from .models import Treinamento,Aula
from django.utils import timezone
from datetime import datetime
from django.db.models import Q

class CriarEventoForm(forms.ModelForm):
    
    class Meta:
        model = Treinamento
        fields = ['nm_evento', 'data', 'local', 'aulas','horario_final']
        
        widgets = {
            'nm_evento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Treinamento de Integração'}),
            'data': forms.DateTimeInput(format='%Y-%m-%dT%H:%M',attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'local': forms.Select(attrs={'class': 'form-select'}),
            'aulas': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'horario_final': forms.TimeInput(format='%H:%M',attrs={'type':'time','class': 'form-control','min':'00:05'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data'].required = True
        self.fields['horario_final'].required = True

        tempo_limite_busca = timezone.now() - timezone.timedelta(minutes=10)
        if self.instance and self.instance.pk:
            self.fields['aulas'].queryset = Aula.objects.filter(Q(data_criacao__gte=tempo_limite_busca) | Q(aulas=self.instance)).distinct()
        else:
            self.fields['aulas'].queryset = Aula.objects.filter(
                data_criacao__gte=tempo_limite_busca
            )

class CriarAulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ['nm_aula', 'descricao', 'palestrante', 'carga_horaria','horario_inicial_aula','horario_final_aula']
        
        widgets = {
            'nm_aula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Segurança do Trabalho'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breve descrição do conteúdo'}),
            'palestrante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do instrutor'}),
            'carga_horaria': forms.TimeInput(format='%H:%M',attrs={'type':'time','class': 'form-control','min':'00:05'}),
            'horario_inicial_aula': forms.TimeInput(format='%H:%M',attrs={'type':'time','class': 'form-control','min':'00:01'}),
            'horario_final_aula': forms.TimeInput(format='%H:%M',attrs={'type':'time','class': 'form-control','min':'00:01'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['horario_inicial_aula'].required = True
        self.fields['horario_final_aula'].required = True