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

        
        atributos_com_valor = nome.strip() and email.strip() and senha.strip() and senha_comfirmacao.strip()
        err = None
        if atributos_com_valor:
            if "@" in email:
                if senha == senha_comfirmacao:
                    email_duplicado = User.objects.filter(email = email).exists()

                    if not email_duplicado:
                        user = User.objects.create_user(username=nome, email=email, password = senha)
                        user.save()
                        messages.success(request, "Cadastrado com sucesso!")
                        return redirect('login')

                    else:
                        err = "email já é reconhecido por um usuário do sistema"
                        messages.error(request, err)
                
                else:
                    err = "senhas não correspondem"
                    messages.error(request, err)
                    
            else:
                err = "email não segue um padrão conhecido"
                messages.error(request, err)
                
        else:
            err = "atributo vazio"
            messages.error(request, err)
            
        print(err)
        return redirect('cadastro')
    
    return render(request, 'usuarios/cadastro.html')

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["password"]

        if email.strip() and senha.strip():
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

def cria_receita(request):
    if request.method == "POST":
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita'] # Serve para capturar os arquivos da requisição
        user = get_object_or_404(User, pk=request.user.id)
        campos_preenchidos = nome_receita and ingredientes and modo_preparo and tempo_preparo and rendimento and categoria and foto_receita

        if campos_preenchidos:
            receita = Receita.objects.create(pessoa=user, nome_receita=nome_receita, modo_preparo=modo_preparo,
            ingredientes=ingredientes, tempo_preparo=tempo_preparo, rendimento=rendimento, categoria=categoria, foto_receita=foto_receita)
            receita.save()
            messages.success(request, "Receita cadastrada com sucesso.")
            return redirect('dashboard')
        else:
            err = "Todos os itens exigidos devem ser informados."
            
            messages.error(request, err)
        
        return redirect('cria_receita')

    else:
        return render(request, "usuarios/cria-receita.html")