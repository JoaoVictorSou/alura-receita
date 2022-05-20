from django.contrib import admin
from .models import Pessoa

class ListagemPessoas(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email')
    list_display_links = ('id', 'nome')

admin.site.register(Pessoa, ListagemPessoas)
