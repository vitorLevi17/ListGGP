from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Treinamento
from django.contrib import messages
from .forms import CriarEventoForm,CriarAulaForm

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

@login_required(login_url='/login') #FALTANDO NOME COLABORADOR - DATA E HORARIO DE INICIO
def gerar_relatorio(request,treinamento_id):
    treinamento = Treinamento.objects.get(id=treinamento_id)

    data_formatada = treinamento.data.strftime('%d-%m-%Y')
    nome_arquivo = "Lista de presença - "+treinamento.nm_evento+" - "+ data_formatada
    arquivo = HttpResponse(content_type='text/plain')
    arquivo['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'

    arquivo.write("EVENTO: "+treinamento.nm_evento+" - "+data_formatada+" \n \n")
    horas = 0
    for aula in treinamento.aulas.all():
        arquivo.write("Aula: "+aula.nm_aula+" | Descrição: "+aula.descricao+" | Ministrado por: "+aula.palestrante+" | Duração de: "+str(aula.carga_horaria)+" horas \n")
        horas += aula.carga_horaria

    arquivo.write("\nCarga horária total do treinamento: "+str(horas)+" horas\n")
    arquivo.write("PARTICIPANTES:  \n")
    
    matriculas_formatadas = [f"'00{matricula}'" for matricula in treinamento.participantes]
    lista_participantes = ", ".join(matriculas_formatadas)

    arquivo.write(lista_participantes)
    return arquivo

@login_required(login_url="login/") #ALERTA PARA AULAS VAZIAS
def criar_evento(request):
    if request.method == 'POST':
        form = CriarEventoForm(request.POST)

        if form.is_valid():
            treinamento = form.save(commit=False)
            treinamento.status = 'MARCADO'
            treinamento.save()

            form.save_m2m()
            messages.success(request, 'Novo evento cadastrado com sucesso!')
            return redirect('listar-eventos-marcados')
    else:
        form = CriarEventoForm()
    
    return render(request,'events/criar-evento.html',{'form':form})

@login_required(login_url="login/") #DEVOLVER PARA CRIAR_EVENTO COM OS DADOS SALVOS
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