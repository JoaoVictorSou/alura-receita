from email import message
from http.client import HTTPResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita

# Create your views here.

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha_comfirmacao = request.POST['password2']

        if campos_preenchidos((nome, email, senha, senha_comfirmacao)):
            if "@" in email:
                if senha_confirmacao_correspondem(senha, senha_comfirmacao):
                    if email_unico(email):
                        if nome_unico(nome):
                            user = User.objects.create_user(username=nome, email=email, password = senha)
                            user.save()
                            messages.success(request, "Cadastrado com sucesso!")
                            return redirect('login')
                        else:
                            messages.error(request, "Nome de usuário já está utilizado no sistema. Tente outro.")

                    else:
                        messages.error(request, "Email já é reconhecido por um usuário do sistema.")
                
                else:
                    messages.error(request, "a Senha e a confirmação não correspondem.")
                    
            else:
                messages.error(request, "Email não segue um padrão conhecido.")
                
        else:
            messages.error(request, "Atributos vazios.")
            
        return redirect('cadastro')
    
    return render(request, 'usuarios/cadastro.html')

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["password"]

        if campos_preenchidos((email, senha)):
            if "@" in email:
                email_cadastrado = User.objects.filter(email=email).exists()
                if email_cadastrado:
                    name = User.objects.filter(email=email).values_list("username", flat=True) # Pegando apenas o username do usuário com email referente. Flat indica que só quer o nome.
                    user = auth.authenticate(request, username=name[0], password=senha)

                    if user is not None:
                        auth.login(request, user)
                        return redirect("dashboard")
                    else:
                        messages.error(request, "Credenciais inválidas.")
                else:
                    messages.error(request, "Email não existe cadastrado no site.")
            else:
                messages.error(request, "Email não segue padrão reconhecido.")
        else:
            messages.error(request, "Não é permitido atributos de senha ou email vazios.")
        
        return redirect("login")
    
    return render(request, 'usuarios/login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    if request.user.is_authenticated:
        id = request.user.id

        receitas = Receita.objects.order_by("-data_receita").filter(pessoa=id)
        return render(request, 'usuarios/dashboard.html', {"receitas": receitas})
    else:
        return redirect('login')

def campos_preenchidos(campos):
    preenchidos = True
    for campo in campos:
        if not str(campo).strip():
            preenchidos = False
            break

    return preenchidos

def senha_confirmacao_correspondem(senha, confirmacao_senha):
    if senha == confirmacao_senha:
        return True
    
    return False

def email_unico(email):
    email_existe = User.objects.filter(email = email).exists()

    return not email_existe

def nome_unico(nome):
    nome_existe = User.objects.filter(username = nome).exists()

    return not nome_existe