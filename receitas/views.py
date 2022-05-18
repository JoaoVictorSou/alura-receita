from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from .models import Receita

# Create your views here.

def index(request):
    receitas = Receita.objects.all()

    dados = {
        'receitas': receitas
    }

    return render(request, "index.html", dados) # deve-se enviar a requisição juntamente com o arquivo

def receita(request, receita_id):
    receita_escolhida = get_object_or_404(Receita, pk=receita_id)
    dados = {
        'receita': receita_escolhida
    }

    return render(request, "receita.html", dados)