from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import CriarCertificadoForm
from django.contrib import messages

@login_required (login_url='/login')
def pagina_inicial(request):
    return render(request,'pagina-inicial.html')

def cadastrar_certificado(request):
    if request.method == 'POST':
        form = CriarCertificadoForm(request.POST)

        if form.is_valid():
            certificado = form.save(commit=False)
            certificado.status = 'AGUARDANDO ANÁLISE'
            certificado.id_usuario = request.user
            certificado.save()

            form.save_m2m()
            messages.success(request, 'Novo certificado cadastrado com sucesso!')
            return redirect('pagina-inicial')

    else:
    
        form = CriarCertificadoForm()
    return render(request, 'certificados/cadastrar-certificado.html', {'form': form})