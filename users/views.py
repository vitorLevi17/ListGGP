from django.shortcuts import render
from users.forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                user = authenticate(request, username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    return redirect('index')
                else:
                    form.add_error(None, 'Usuário ou senha incorretos.')            
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'user/login.html', context)