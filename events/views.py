from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Treinamento
from django.contrib import messages

@login_required(login_url='/login')
def listar_treinamentos_marcados(request):
    lista_treinamentos = Treinamento.objects.filter(status__in=['MARCADO', 'ANDAMENTO'])
    return render(request,'events/listar-treinamento.html',{'treinamentos':lista_treinamentos})

@login_required(login_url='/login')
def conferir_treinamento(request,treinamento_id):
    treinamento = Treinamento.objects.get(id=treinamento_id)
    return render(request,'events/conferir-treinamento.html',{'treinamento':treinamento})

@login_required(login_url='/login')
def iniciar_treinamento(request,treinamento_id):
    treinamento = Treinamento.objects.get(id=treinamento_id)
    treinamento.status = "ANDAMENTO"
    treinamento.save()
    return redirect('conferir-treinamento',treinamento_id=treinamento.id)

@login_required(login_url='/login')
def adicionar_participante(request,treinamento_id,matricula_participante):
    treinamento = Treinamento.objects.get(id=treinamento_id)
    
    if(matricula_participante in treinamento.participantes):
        messages.warning(request, f'Atenção: A matrícula {matricula_participante} já foi registrada neste evento!')
        return redirect('conferir-treinamento',treinamento_id=treinamento.id)

    treinamento.participantes.append(matricula_participante)
    treinamento.save()
    return redirect('conferir-treinamento',treinamento_id=treinamento.id)

@login_required(login_url='/login')
def finalizar_treinamento(request,treinamento_id):
    treinamento = Treinamento.objects.get(id=treinamento_id)
    treinamento.status = "FINALIZADO"
    treinamento.save()
    messages.success(request,'Evento finalizado com sucesso!')
    return redirect('conferir-treinamento',treinamento_id=treinamento.id) 