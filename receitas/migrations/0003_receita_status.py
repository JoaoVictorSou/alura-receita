# Generated by Django 4.0.4 on 2022-05-21 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receitas', '0002_receita_pessoa'),
    ]

    operations = [
        migrations.AddField(
            model_name='receita',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]