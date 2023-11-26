# Generated by Django 4.2 on 2023-06-02 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='inscricao_estadual',
            field=models.CharField(max_length=14, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='inscricao_municipal',
            field=models.CharField(max_length=14, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='rg',
            field=models.CharField(max_length=7, null=True, unique=True),
        ),
    ]
