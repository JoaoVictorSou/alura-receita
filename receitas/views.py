from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse

import receitas
from .models import Receita

# Create your views here.

def index(request):
    receitas = Receita.objects.order_by('-data_receita').filter(postar=True)

    dados = {
        'receitas': receitas
    }

    return render(request, "receitas/index.html", dados) # deve-se enviar a requisição juntamente com o arquivo

def receita(request, receita_id):
    receita_escolhida = get_object_or_404(Receita, pk=receita_id)
    dados = {
        'receita': receita_escolhida
    }

    return render(request, "receitas/receita.html", dados)

def buscar(request):
    if 'buscar' in request.GET:
        buscar_receita = request.GET['buscar']

    receitas = Receita.objects.order_by('-data_receita').filter(nome_receita__icontains = buscar_receita)
    dados = {
        'receitas': receitas 
    }

    return render(request, 'receitas/buscar.html', dados)

    