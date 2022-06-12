from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha_comfirmacao = request.POST['password2']

        
        atributos_com_valor = nome.strip() and email.strip() and senha.strip() and senha_comfirmacao.strip()
        err = None
        if atributos_com_valor:
            if "@" in email:
                if senha == senha_comfirmacao:
                    email_duplicado = User.objects.filter(email = email).exists()

                    if not email_duplicado:
                        user = User.objects.create_user(username=nome, email=email, password = senha)
                        user.save()
                        return redirect('login')

                    else:
                        err = "email já é reconhecido por um usuário do sistema"
                
                else:
                    err = "senhas não correspondem"
                    
            else:
                err = "email não segue um padrão conhecido"
                
        else:
            err = "atributo vazio"
            
        print(err)
        return redirect('cadastro')
    
    return render(request, 'usuarios/cadastro.html')

def login(request):
    return render(request, 'usuarios/login.html')

def logout(request):
    pass

def dashboard(request):
    pass