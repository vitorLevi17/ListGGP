from django.shortcuts import render,redirect
from users.forms import LoginForm,MudarSenhaForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

def login_view(request):
    #CORREÇÃO DO 403 VERIFICAÇÃO CSRF
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_form = form.cleaned_data["username"]
            senha_form = form.cleaned_data["password"]

            if User.objects.filter(username=username_form).exists():
                user = auth.authenticate(request, username=username_form,
                                     password=senha_form)
                if user is not None:
                    primeiro_acesso = (user.last_login is None)
                    auth.login(request, user)
                    if primeiro_acesso:
                        return redirect('usuario_altera_senha')
                    else:
                        return redirect('index')
                else:
                    form.add_error(None, 'Usuário ou senha incorretos.') 
            else:
                form.add_error(None,'Usuário ou senha incorretos.')           
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'user/login.html', context)

@login_required(login_url='/login')
def index(request):
    return render(request,'index.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='/login')
def usuario_altera_senha(request):
    user = request.user
    if request.method == 'POST':
        form = MudarSenhaForm(request.POST)        
        if form.is_valid():
            nova_senha = form.cleaned_data["new_password"]
            confirmacao_senha = form.cleaned_data["confirm_new_password"]
            if nova_senha == confirmacao_senha:
                user.set_password(confirmacao_senha)
                user.save()
                update_session_auth_hash(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'As senhas não coincidem.')
    else:
        form = MudarSenhaForm()
                
    context = {'form': form}
    return render(request,'user/alterar_senha.html',context)