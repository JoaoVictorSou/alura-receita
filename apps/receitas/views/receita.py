from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from receitas.models import Receita

# Create your views here.

def index(request):
    receitas = Receita.objects.order_by('-data_receita').filter(postar=True)

    paginator = Paginator(receitas, 3) # Quantidade de receitas por página
    page = request.GET.get('page') # Página atual dentro da paginação [QUERY PARAMS]
    receita_por_pagina = paginator.get_page(page) # Lista de receitas para a página atual
    
    dados = {
        'receitas': receita_por_pagina
    }

    return render(request, "receitas/index.html", dados) # deve-se enviar a requisição juntamente com o arquivo

def receita(request, receita_id):
    receita_escolhida = get_object_or_404(Receita, pk=receita_id)
    dados = {
        'receita': receita_escolhida
    }

    return render(request, "receitas/receita.html", dados)

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

        if campos_preenchidos((nome_receita, ingredientes, modo_preparo, tempo_preparo, rendimento, categoria, foto_receita)):
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
        return render(request, "receitas/cria-receita.html")

def deleta_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk = receita_id)
    receita.delete()

    receita_permanece = Receita.objects.filter(id = receita_id).exists()
    if not receita_permanece:
        messages.success(request, "Receita deletada com sucesso!")
    else:
        messages.error(request, "Houveram problemas para deletar a receita!")
    return redirect("dashboard")
    
def edita_receita(request, receita_id):
    if request.method == "GET":
        receita = get_object_or_404(Receita, pk = receita_id)

        return render(request, "receitas/edita-receita.html", {'receita': receita})
    
    messages.error(request, "A URL utilizada não serve para modificar a receita, apenas para exibir o formulário.")
    return redirect("dashboard")

def atualiza_receita(request):
    receita_id = request.POST['receita_id']
    nome_receita = request.POST['nome_receita']
    ingredientes = request.POST['ingredientes']
    modo_preparo = request.POST['modo_preparo']
    tempo_preparo = request.POST['tempo_preparo']
    rendimento = request.POST['rendimento']

    receita = get_object_or_404(Receita, pk = receita_id)

    if nome_receita:
        receita.nome_receita = nome_receita
    if ingredientes:
        receita.ingredientes = ingredientes
    if modo_preparo:
        receita.modo_preparo = modo_preparo
    if tempo_preparo:
        receita.tempo_preparo = tempo_preparo
    if rendimento:
        receita.rendimento = rendimento
    
    if 'foto_receita' in request.FILES:
        receita.foto_receita = request.FILES['foto_receita']
    
    receita.save()
    
    return redirect("dashboard")

# UTIL
def campos_preenchidos(campos):
    preenchidos = True
    for campo in campos:
        if not str(campo).strip():
            preenchidos = False
            break

    return preenchidos

    