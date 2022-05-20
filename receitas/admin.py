from django.contrib import admin
from .models import Receita

class ListandoReceitas(admin.ModelAdmin):
    list_display = ('id', 'nome_receita', 'categoria', 'tempo_preparo') # itens exibidos na listagem
    list_display_links = ('id', 'nome_receita') # links para a tela específica
    search_fields = ('nome_receita',) # campo de busca dentro da listagem
    list_filter = ('categoria',) # Lista de categoria na aside
    list_per_page = 3 # quantidade de receitas por página


admin.site.register(Receita, ListandoReceitas)
