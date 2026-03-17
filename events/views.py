from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Treinamento
from django.contrib import messages
from .forms import CriarEventoForm,CriarAulaForm
from django.utils import timezone

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

@login_required(login_url='/login')
def gerar_relatorio(request,treinamento_id):
    treinamento = Treinamento.objects.get(id=treinamento_id)

    data_local = timezone.localtime(treinamento.data)
    data_formatada = data_local.strftime('%d-%m-%Y %H:%M')
    nome_arquivo = "Lista de presença - "+treinamento.nm_evento+" - "+ data_formatada + ".txt"
    arquivo = HttpResponse(content_type='text/plain')
    arquivo['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'

    arquivo.write("EVENTO: "+treinamento.nm_evento+" - "+data_formatada+" até "+treinamento.horario_final.strftime('%H:%M')+ "\n \n")
    minutos_totais = 0
    for aula in treinamento.aulas.all():
        hora_formatada = aula.carga_horaria.strftime('%H:%M')
        arquivo.write(f"Aula: "+aula.nm_aula+" | Descrição: "+aula.descricao+" | Ministrado por: "+aula.palestrante+" | Duração de: "+str(hora_formatada)+" horas \n")
        minutos_totais += (aula.carga_horaria.hour * 60) + aula.carga_horaria.minute
    
    horas_finais = minutos_totais // 60
    minutos_finais = minutos_totais % 60
    arquivo.write(f"\nCarga horária total do treinamento: {horas_finais:02d}:{minutos_finais:02d} horas\n")
    arquivo.write("PARTICIPANTES:  \n")
    
    matriculas_formatadas = [f"'{str(matricula).zfill(7)}'" for matricula in treinamento.participantes]
    lista_participantes = ", ".join(matriculas_formatadas)

    arquivo.write(lista_participantes)
    return arquivo

@login_required(login_url="login/")
def criar_evento(request):
    if request.method == 'POST':
        form = CriarEventoForm(request.POST)

        if form.is_valid():
            treinamento = form.save(commit=False)
            treinamento.status = 'MARCADO'
            treinamento.save()

            form.save_m2m()
            messages.success(request, 'Novo evento cadastrado com sucesso!')
            return redirect('conferir-treinamento',treinamento_id=treinamento.id )
        else:
            if 'aulas' in form.errors:
                messages.error(request, 'Atenção: Você precisa selecionar pelo menos uma Aula Vinculada para criar o treinamento!')
            else:
                messages.error(request, 'Atenção: Insira uma data e horário para inicio e fim do treinamento.')
    else:
        form = CriarEventoForm()
    
    return render(request,'events/criar-evento.html',{'form':form})

@login_required(login_url="login/")
def criar_aula(request):
    if request.method == 'POST':
        form = CriarAulaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Nova aula cadastrada com sucesso! Ela já está disponível para seleção.')
            
            return redirect('criar-evento') 
    else:
        form = CriarAulaForm()
    
    return render(request, 'events/criar-aula.html', {'form': form})

@login_required(login_url="login/")
def treinamentos_finalizados(request):
    lista_treinamentos = Treinamento.objects.filter(status__in=['FINALIZADO', 'CANCELADO'])
    return render(request,'events/listar-treinamento.html',{'treinamentos':lista_treinamentos})

def cancelar_treinamento(request,treinamento_id):
    treinamento = Treinamento.objects.get(id = treinamento_id)
    treinamento.status = "CANCELADO"
    treinamento.save()
    return redirect('conferir-treinamento',treinamento_id=treinamento.id)

#@login_required(login_url="login/")
#def alterar_data_finalizacao(request,treinamento_id):
    #treinamento = Treinamento.objects.get(id = treinamento_id) 