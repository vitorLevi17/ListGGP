from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

def validar_permissoes_usuario(request,treinamento,mensagem_erro):
    if request.user != treinamento.usuario_cadastrante and not request.user.groups.filter(name='RH GESTOR').exists():
        messages.warning(request,mensagem_erro)
        return redirect('conferir-treinamento',treinamento_id=treinamento.id)
    else:
        return None
    
def validar_horario_inicio_treinamento(request,treinamento):
    limite_inicio = treinamento.data - timezone.timedelta(minutes=30)
    if timezone.now() < limite_inicio:
        messages.warning(request,f'Atenção: O treinamento só pode ser iniciado faltando 30 minutos para o horário marcado.')
        return redirect('conferir-treinamento', treinamento_id=treinamento.id)
    return None

def validar_horario_fim_treinamento(request,treinamento):
    data_treinamento = timezone.localtime(treinamento.data).date()
    data_atual = datetime.combine(data_treinamento, treinamento.horario_final)
    momento_termino = timezone.make_aware(data_atual)
    
    if timezone.now() < momento_termino:
        messages.warning(request,f'Atenção: O treinamento só pode ser finalizado após o horário marcado.')
        return redirect('conferir-treinamento', treinamento_id=treinamento.id)
    return None

def validar_horario_fim_treinamento_cadastro(request,treinamento):
    data_inicio_treinamento = timezone.localtime(treinamento.data)
    
    horario_fim_sem_fuso = datetime.combine(data_inicio_treinamento.date(), treinamento.horario_final)
    horario_fim_completo = timezone.make_aware(horario_fim_sem_fuso)
    
    if data_inicio_treinamento > horario_fim_completo or treinamento.data < timezone.now():
        messages.warning(request,f'Atenção: As datas e horários de inicio e término estão inválidos.')
        return True
    return False   

def validar_horario_fim_aula(request,horario_inicio,horario_final):
    if horario_inicio >= horario_final:
        messages.warning(request,f'Atenção: As datas e horários de inicio e término estão inválidos.')
        return True
    return False

    