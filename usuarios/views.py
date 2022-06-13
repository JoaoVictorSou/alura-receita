from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

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
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["password"]

        err = ""
        if email.strip() and senha.strip():
            if "@" in email:
                email_cadastrado = User.objects.filter(email=email).exists()
                if email_cadastrado:
                    name = User.objects.filter(email=email).values_list("username", flat=True) # Pegando apenas o username do usuário com email referente. Flat indica que só quer o nome.
                    user = auth.authenticate(request, username=name[0], password=senha)

                    if user is not None:
                        auth.login(request, user)
                        print("Login realizado com sucesso", name)
                        return redirect("dashboard")
                    else:
                        err = "credencial inválida."
                else:
                    err = "email não existe cadastrado no site."
            else:
                err = "email não segue padrão reconhecido"
        else:
            err = "não é permitido atributos de senha ou email vazios"
        
        print(err)
        return redirect("login")
    
    return render(request, 'usuarios/login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/dashboard.html')
    else:
        return redirect('login')