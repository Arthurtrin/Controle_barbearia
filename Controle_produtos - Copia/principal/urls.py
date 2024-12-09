"""URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [

    #############################

    ###########ESTOQUE###########

    #############################

    #INICO
    path('', fprincipal),
    path('home', fprincipal2, name='fprincipal2'),
    path('redireciona', redireciona, name='redireciona'),
    path('login', login, name='login'),
    path('slogin', slogin, name='slogin'),
    path('irRegistra', irRegistra, name='irRegistra'),
    path('sair', sair, name='sair'),

    #SALVAR
    path('salvarUsua', salvarUsua, name='salvarUsua'),
    path('salvarProd', salvarProd, name='salvarProd'),
    path('salvar_grupo', salvarGrp, name='salvarGrp'),
    path('salvarforn', salvarForn, name='salvarForn'),
    path('SalvarEnt/<int:id>', salvarEnt, name='salvarEnt'),
    path('salvarSai/<int:id>', salvarSai, name='salvarSai'),


    #CADASTRAR
    path('cadastrar_produto', cadastrarProd, name='cadastrarProd'),
    path('cadastrar_grupo', cadastrarGrp, name='cadastrarGrp'),
    path('cadastrar_fornecedor', cadastrarForn, name='cadastrarForn'),

    # ENTRADA E SAIDA
    path('entrada/<int:id>', entrada, name='entrada'),
    path('saida/<int:id>', saida, name='saida'),

    #RELATORIO
    path('relatorio_entrada', relaEnt, name='relaEnt'),
    path('relatorio_saida', relaSai, name='relaSai'),
    path('relatorio_usuario', relaUsua, name='relaUsua'),
    path('relatorio_fornecedor', relaForn, name='relaForn'),
    path('relatorio_produto', relaProd, name='relaProd'),
    path('relatorio_grupo', relaGrp, name='relaGrp'),
    path('relatorio', relatorio, name='relatorio'),

    #DELETE
    path('deleteEnt/<int:id>', deleteEnt, name='deleteEnt'),
    path('deleteSai/<int:id>', deleteSai, name='deleteSai'),
    path('deleteUsua/<int:id>', deleteUsua, name='deleteUsua'),
    path('deleteForn/<int:id>', deleteForn, name='deleteForn'),
    path('deleteProd/<int:id>', deleteProd, name="deleteProd"),
    path('deleteGrp/<int:id>', deleteGrp, name="deleteGrp"),

    #EDITAR
    path('editar_entrada/<int:id>', editarent, name='editarent'),
    path('editar_saida/<int:id>', editarsai, name='editarsai'),
    path('editarEnt/<int:id>/<int:qtd>', editarEnt, name="editarEnt"),
    path('editarSai/<int:id>/<int:qtd>', editarSai, name="editarSai"),
    path('editar_produto/<int:id>', editarprod, name='editarprod'),
    path('editarProd/<int:id>', editarProd, name='editarProd'),
    path('editar_fornecedor/<int:id>', editarforn, name='editarforn'),
    path('editarForn/<int:id>', editarForn, name='editarForn'),
    path('editar_grupo/<int:id>', editargrp, name='editargrp'),
    path('editar_grupo/<int:id>', editargrp, name='editargrp'),
    path('editarGrp/<int:id>', editarGrp, name='editarGrp'),

    #CONTAS
    path('nova_conta', nconta, name='nconta'),
    path('salvarconta', salvarconta, name='salvarconta'),
    path('editar_conta/<int:id>', edicao, name='edicao'),
    path('editarconta/<int:id>', editarConta, name='editarConta'),
    path('relatorio_conta', relaConta, name='relaConta'),
    path('deleteConta/<int:id>', deleteConta, name='deleteConta'),


    #############################

    #########AGENDAMENTO#########

    #############################

    path('agendamento', pg_age, name='pg_age'),
    path('cadastrar_horario', cad_horario, name='cad_horario'),
    path('cadastrar_horario_prox', salvarhorario, name='salvarhorario'),
    path('novo_agendamento', novo_agendamento, name='novo_agendamento'),
    path('cadastrar_corte', cad_corte, name='cad_corte'),
    path('salvar_corte', salvar_corte, name='salvar_corte'),
    path('marcar_corte/<int:id>', age_corte, name='age_corte'),
    path('marcar/', marcar, name='marcar'),
    path('ir_teste/<int:id>', ir_teste, name='ir_teste'),
    path('confirma/<str:dia_semana>/<int:dia>/<int:mes>/<int:ano>/<str:tempo>/<str:horario>', marcar_conf, name='marcar_conf'),
    

]