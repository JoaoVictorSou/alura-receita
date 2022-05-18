from django.shortcuts import render
from django.http import HttpResponse
from .models import Receita

# Create your views here.

def index(request):
    receitas = Receita.objects.all()

    dados = {
        'receitas': receitas
    }

    return render(request, "index.html", {"nomes_das_receitas": receitas}) # deve-se enviar a requisição juntamente com o arquivo

def receita(request):
    return render(request, "receita.html")