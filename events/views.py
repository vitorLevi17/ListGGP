from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Treinamento
from django.contrib import messages
from .forms import CriarEventoForm,CriarAulaForm
from django.utils import timezone
from datetime import datetime
from .validators import *

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
    
    bloqueio_permissoes = validar_permissoes_usuario(request,treinamento,f'{request.user.first_name}, você não tem permissão para iniciar o evento')
    if bloqueio_permissoes:
        return bloqueio_permissoes
    
    bloqueio_horario = validar_horario_inicio_treinamento(request,treinamento)
    if bloqueio_horario:
        return bloqueio_horario
    
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
    messages.success(request,f'Usuário {matricula_participante} adicionado ao evento com sucesso!')
    return redirect('conferir-treinamento',treinamento_id=treinamento.id)

@login_required(login_url='/login')
def finalizar_treinamento(request,treinamento_id):
    treinamento = Treinamento.objects.get(id=treinamento_id)
    
    bloqueio_permissoes = validar_permissoes_usuario(request,treinamento,f'{request.user.first_name}, você não tem permissão para finalizar o evento')
    if bloqueio_permissoes:
        return bloqueio_permissoes
    
    bloqueio_horario = validar_horario_fim_treinamento(request,treinamento)
    if bloqueio_horario:
        return bloqueio_horario

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
        arquivo.write(f"Aula: "+aula.nm_aula+" | Descrição: "+aula.descricao+" | Ministrado por: "+aula.palestrante+" | Duração de: "+str(hora_formatada)+" horas entre "+aula.horario_inicial_aula.strftime('%H:%M')+" e "+aula.horario_final_aula.strftime('%H:%M')+'\n')
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
    
            erro_horario = validar_horario_fim_treinamento_cadastro(request, form.instance)
            if erro_horario:
                return render(request, 'events/criar-evento.html', {'form': form})

            treinamento = form.save(commit=False)
            treinamento.status = 'MARCADO'
            treinamento.usuario_cadastrante = request.user
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

@login_required(login_url="login/")
def cancelar_treinamento(request,treinamento_id):
    treinamento = Treinamento.objects.get(id = treinamento_id)

    validar_permissoes = validar_permissoes_usuario(request,treinamento,f'{request.user.first_name}, você não tem permissão para cancelar o evento')
    if validar_permissoes:
        return validar_permissoes
    
    treinamento.status = "CANCELADO"
    treinamento.save()
    return redirect('conferir-treinamento',treinamento_id=treinamento.id)

@login_required(login_url="login/")
def alterar_data_finalizacao(request,treinamento_id):
    if request.method == 'POST':
        treinamento = Treinamento.objects.get(id = treinamento_id)

        validar_permissoes = validar_permissoes_usuario(request,treinamento,f'{request.user.first_name}, você não tem permissão para alterar o horário de término do evento')
        if validar_permissoes:
            return validar_permissoes 
        
        novo_horario_final = request.POST.get('novo_horario')

        if novo_horario_final:
            treinamento.horario_final = novo_horario_final
            treinamento.save()
    return redirect('conferir-treinamento',treinamento_id=treinamento.id)

@login_required(login_url="login/")
def editar_treinamento(request,treinamento_id):
    treinamento = Treinamento.objects.get(id=treinamento_id)

    validar_permissoes = validar_permissoes_usuario(request,treinamento,f'{request.user.first_name}, você não tem permissão para editar evento')
    if validar_permissoes:
        return validar_permissoes
    
    if request.method == 'POST':
        form = CriarEventoForm(request.POST, instance=treinamento)

        if form.is_valid():
            bloqueio = validar_horario_fim_treinamento_cadastro(request, form.instance)
            if bloqueio:
                return render(request, 'events/criar-evento.html', {'form': form})
            form.save()
            messages.success(request, 'Treinamento atualizado com sucesso!')
            return redirect('conferir-treinamento', treinamento_id=treinamento.id)
        else:
            if 'horario_final' in form.errors:
                messages.error(request, 'Atenção: O Horário de Término é obrigatório!')
            else:
                messages.error(request, 'Atenção: Verifique os campos preenchidos.')
    else:
        form = CriarEventoForm(instance=treinamento)
    
    return render(request, 'events/editar-treinamento.html', {'form': form, 'treinamento': treinamento})

@login_required(login_url="login/")
def remover_participante(request,treinamento_id,matricula_participante):
    treinamento = Treinamento.objects.get(id=treinamento_id)
    if matricula_participante in treinamento.participantes:
        treinamento.participantes.remove(matricula_participante)
        treinamento.save()
        messages.success(request,f'Usuário {matricula_participante} removido do evento com sucesso!')
    else:
        messages.warning(request, f'Atenção: A matrícula {matricula_participante} não foi registrada neste evento!')
         
    return redirect('conferir-treinamento',treinamento_id=treinamento.id)