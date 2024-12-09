# Generated by Django 5.1.1 on 2024-09-27 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
                ('quant', models.IntegerField()),
                ('usuario', models.CharField(default='vazio', max_length=60)),
                ('preco', models.FloatField(default=0)),
                ('grupo', models.CharField(default='vazio', max_length=60)),
                ('forn', models.CharField(default='vazio', max_length=60)),
                ('data', models.CharField(default='vazio', max_length=60)),
                ('gasto', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60)),
                ('quant', models.IntegerField()),
                ('grupo', models.CharField(default='vazio', max_length=50)),
                ('preco', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60)),
                ('telefone', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60)),
                ('preco', models.FloatField(default=0)),
                ('grupo', models.CharField(default='vazio', max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Saida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
                ('quant', models.IntegerField()),
                ('usuario', models.CharField(default='vazio', max_length=60)),
                ('preco', models.FloatField(default=0)),
                ('forn', models.CharField(default='vazio', max_length=60)),
                ('grupo', models.CharField(default='vazio', max_length=60)),
                ('data', models.CharField(default='vazio', max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('telefone', models.CharField(max_length=60)),
                ('usuario', models.CharField(max_length=20)),
                ('senha', models.CharField(max_length=15)),
            ],
        ),
    ]