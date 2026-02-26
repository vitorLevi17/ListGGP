from django.shortcuts import render,redirect
from users.forms import LoginForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_form = form.cleaned_data["username"]
            senha_form = form.cleaned_data["password"]

            if User.objects.filter(username=username_form).exists():
                user = auth.authenticate(request, username=username_form,
                                     password=senha_form)
                if user is not None:
                    auth.login(request, user)
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

@login_required(login_url='/index')
def index(request):
    return render(request,'index.html')