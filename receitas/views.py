from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    receitas = {
        1:'Lasanha',
        2:'Sopa de legumes',
        3:'Sorvete',
        4: 'bolo de chocolate'
    }

    return render(request, "index.html", {"nomes_das_receitas": receitas}) # deve-se enviar a requisição juntamente com o arquivo

def receita(request):
    return render(request, "receita.html")