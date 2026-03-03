from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Treinamento

@login_required(login_url='/login')
def listar_treinamentos_marcados(request):
    lista_treinamentos = Treinamento.objects.filter(status__in=['MARCADO', 'ANDAMENTO'])
    return render(request,'events/listar-treinamento.html',{'treinamentos':lista_treinamentos})

@login_required(login_url='/login')
def conferir_treinamento(request,treinamento_id):
    treinamento = Treinamento.objects.get(id=treinamento_id)
    return render(request,'events/conferir-treinamento.html',{'treinamento':treinamento})

def iniciar_treinamento(request,treinamento_id):
    treinamento = Treinamento.objects.get(id=treinamento_id)
    treinamento.status = "ANDAMENTO"
    treinamento.save()
    return redirect('conferir-treinamento',treinamento_id=treinamento.id)
    

