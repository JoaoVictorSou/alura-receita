from django.shortcuts import render

from receitas.models import Receita

def buscar(request):
    if 'buscar' in request.GET:
        buscar_receita = request.GET['buscar']

    receitas = Receita.objects.order_by('-data_receita').filter(nome_receita__icontains = buscar_receita)
    dados = {
        'receitas': receitas 
    }

    return render(request, 'receitas/buscar.html', dados)