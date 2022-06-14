from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class Receita(models.Model):
    nome_receita = models.CharField(max_length=200)
    ingredientes = models.TextField()
    modo_preparo = models.TextField()
    tempo_preparo = models.IntegerField()
    rendimento = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    data_receita = models.DateTimeField(default=datetime.now, blank=True)
    foto_receita = models.ImageField(upload_to = "fotos/%d/%m/%Y/", blank = True)
    pessoa = models.ForeignKey(User, on_delete=models.CASCADE)
    postar = models.BooleanField(default=False)

    def __str__(self):
        return self.nome_receita