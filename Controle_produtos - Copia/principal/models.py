from django.db import models

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=60)
    preco = models.FloatField(default=0)
    grupo = models.CharField(max_length=60, default='vazio')
    def __str__(self):
        return self.nome

class Grupo(models.Model):
    nome = models.CharField(max_length=60)
    def __str__(self):
        return self.nome

class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=60)
    usuario = models.CharField(max_length=20)
    senha = models.CharField(max_length=15)
    def __str__(self):
        return self.nome

class Estoque(models.Model):
    nome = models.CharField(max_length=60)
    quant = models.IntegerField()
    grupo = models.CharField(max_length=50, default='vazio')
    preco = models.FloatField(default=0)
    def __str__(self):
        return self.nome

class Entrada(models.Model):
    nome = models.CharField(max_length=150)
    quant = models.IntegerField()
    usuario = models.CharField(max_length=60, default='vazio')
    preco = models.FloatField(default=0)
    grupo = models.CharField(max_length=60, default='vazio')
    forn = models.CharField(max_length=60, default='vazio')
    data = models.CharField(max_length=60, default='vazio')
    gasto = models.FloatField(default=0)
    def __str__(self):
        return self.nome

class Saida(models.Model):
    nome = models.CharField(max_length=150)
    quant = models.IntegerField()
    usuario =  models.CharField(max_length=60, default='vazio')
    preco = models.FloatField(default=0)
    forn = models.CharField(max_length=60, default='vazio')
    grupo = models.CharField(max_length=60, default='vazio')
    data = models.CharField(max_length=60, default='vazio')
    def __str__(self):
        return self.nome

class Fornecedor(models.Model):
    nome = models.CharField(max_length=60)
    telefone = models.CharField(max_length=60)
    def __str__(self):
        return self.nome
    
class Conta(models.Model):
    nome = models.CharField(max_length=60)
    valor = models.FloatField(default=0)
    def __str__(self):
        return self.nome
    
class Horario(models.Model):
    dia = models.CharField(max_length=20)  # Exemplo: 'Domingo', 'Segunda-feira', etc.
    dia_de_trabalho = models.BooleanField(default=False)
    inicio = models.TimeField(null=True, blank=True)
    termino = models.TimeField(null=True, blank=True)
    hora_util = models.TimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.dia} - {'Trabalho' if self.dia_de_trabalho else 'Folga'}"

class Corte(models.Model):
    nome = models.CharField(max_length=60)
    tempo = models.TimeField(null=True, blank=True)
    preco = models.FloatField(default=0)
    def __str__(self):
        return self.nome

class Agenda(models.Model):
    nome = models.CharField(max_length=100, default="")
    dia_semana = models.CharField(max_length=60, default="")
    dia = models.IntegerField()
    mes = models.IntegerField()
    ano = models.IntegerField()
    horario = models.TimeField(null=True, blank=True)
    hora_disponivel = models.TimeField(null=True, blank=True)
    def __str__(self):
        return self.nome
