# Generated by Django 4.0.4 on 2022-05-21 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receitas', '0004_rename_status_receita_postar'),
    ]

    operations = [
        migrations.AddField(
            model_name='receita',
            name='foto_receita',
            field=models.ImageField(blank=True, upload_to='fotos/%d/%m/%Y/'),
        ),
    ]