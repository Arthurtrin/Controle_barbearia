from django.contrib import admin
from .models import Produto, Usuario, Entrada, Saida, Grupo, Estoque, Fornecedor, Conta, Horario, Corte, Agenda

# Register your models here.
admin.site.register(Produto)
admin.site.register(Usuario)
admin.site.register(Fornecedor)
admin.site.register(Entrada)
admin.site.register(Saida)
admin.site.register(Grupo)
admin.site.register(Estoque)
admin.site.register(Conta)
admin.site.register(Horario)
admin.site.register(Corte)
admin.site.register(Agenda)