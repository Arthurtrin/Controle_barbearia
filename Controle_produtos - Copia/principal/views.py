from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Produto, Estoque, Grupo, Fornecedor, Entrada, Saida, Conta, Horario, Corte, Agenda
from datetime import datetime, timedelta
from .add import *
from django.db.models import Sum
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

#############################

###########ESTOQUE###########

#############################

#COMEÇO:
def fprincipal(request):
    return redirect(login)

def fprincipal2(request):
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M:%S')
    produto = Estoque.objects.all().order_by('-id')
    entrada = Entrada.objects.all()
    saida = Saida.objects.all()
    quantidade_entrada = entrada.count()
    quantidade_saida = saida.count()
    quantidade_estoque = produto.count()
    total_gasto = Entrada.objects.aggregate(Sum('gasto'))['gasto__sum']
    total_gasto_conta = Conta.objects.aggregate(Sum('valor'))['valor__sum']
    total_gasto = total_gasto + total_gasto_conta
    total_gasto = round(total_gasto, 2)
    return render(request, "estoque/inicio/principal.html", {"estoque": produto,
                                                     "data": data_e_hora_em_texto, "qtd_estoque":quantidade_estoque,
                                                     "qtd_entrada":quantidade_entrada, "qtd_saida":quantidade_saida,
                                                     "total_gasto":total_gasto})

def redireciona(request):
    return redirect(fprincipal2)

def login(request):
    return render(request, "estoque/inicio/login.html")

def slogin(request):
    usuario = request.POST.get("usuario")
    senha = request.POST.get("senha")
    if Usuario.objects.filter(usuario=usuario, senha=senha).exists():
        return redirect(redireciona)
    else:
        return redirect(login)
    
def sair(request):
    return render(request, "estoque/inicio/sair.html")

def irRegistra(request):
    return render(request, "estoque/inicio/registre.html")

def salvarUsua(request):
    try:
        tnome = request.POST.get("nome")
        ttelefone = request.POST.get("telefone")
        tusuario = request.POST.get("usuario")
        tsenha = request.POST.get("senha")
        if tnome:
            Usuario.objects.create(nome=tnome, telefone=ttelefone, usuario=tusuario, senha=tsenha)
            return redirect(login)
    except Exception as e:
        return render(request, "erro/erro.html")

def relaUsua(request):
    usuario = Usuario.objects.all().order_by('-id') 
    return render(request, "estoque/relatorios/relatorio_usuario.html", {"usuarios": usuario})

def deleteUsua(request, id):
    usua = Usuario.objects.get(id=id)
    usua.delete()
    return redirect(relaUsua)

#PRODUTO
def cadastrarProd(request):
    aviso = None
    aviso_cad = None
    grupo = Grupo.objects.all().order_by('-id') 
    return render(request, "estoque/cadastrar/cadastrarProd.html", {"grupos": grupo, "aviso": aviso, "aviso_cad": aviso_cad})

def salvarProd(request):
    try:
        nome = request.POST.get("nome")
        preco = request.POST.get("preco")
        grupo = request.POST.get("grupo")
        if Produto.objects.filter(nome=nome, preco=float(preco), grupo=grupo).exists():
            aviso = True
            grupo = Grupo.objects.all().order_by('-id') 
            return render(request, "estoque/cadastrar/cadastrarProd.html", {"grupos": grupo, "aviso": aviso})
        elif nome:
            Produto.objects.create(nome=nome, preco=round(float(preco), 2), grupo=grupo)
            Estoque.objects.create(nome=nome, grupo=grupo, quant=0, preco=round(float(preco), 2))
            aviso = None
            aviso_cad = True
            grupo = Grupo.objects.all().order_by('-id') 
            return render(request, "estoque/cadastrar/cadastrarProd.html", {"grupos": grupo, "aviso": aviso, "aviso_cad": aviso_cad})
    except Exception as e:
        return render(request, "erro/erro.html")

def editarprod(request, id):
    produto = Produto.objects.get(id=id)
    grupo = Grupo.objects.all()
    return render(request, "estoque/edicao/editar_produto.html", {"produto" : produto, "grupos": grupo})

def editarProd(request, id):
    try:
        nome = request.POST.get("nome")
        preco = float(request.POST.get("preco"))
        grupo = request.POST.get("grupo")

        produto = Produto.objects.get(id=id)
        estoque = get_object_or_404(Estoque, nome=produto.nome, grupo=produto.grupo, preco=round(produto.preco, 2))

        # Atualizar Saída
        saida = Saida.objects.filter(nome=produto.nome, grupo=produto.grupo, preco=round(produto.preco, 2))
        saida.update(nome=nome, preco=preco, grupo=grupo)

        # Atualizar Entrada
        entradas = Entrada.objects.filter(nome=produto.nome, grupo=produto.grupo, preco=round(produto.preco, 2))
        if entradas.exists():  # Verifica se existem entradas correspondentes
            # Calcular gasto para cada entrada e atualizar
            for entrada in entradas:
                gasto = round(entrada.quant * preco, 2)  # Use o novo preço
                entrada.nome = nome
                entrada.preco = preco
                entrada.grupo = grupo
                entrada.gasto = gasto  # Se 'gasto' for um campo no modelo
                entrada.save()  # Salva cada entrada

        # Atualizar Estoque
        estoque.nome = nome
        estoque.grupo = grupo
        estoque.preco = preco
        estoque.save()

        # Atualizar Produto
        produto.nome = nome
        produto.preco = preco
        produto.grupo = grupo
        produto.save()
        return redirect(relaProd)

    except Exception as e:
        # Aqui você pode logar o erro ou renderizar uma página de erro
        print(f"Erro: {e}")
        return render(request, "erro/erro.html")

def relaProd(request):
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M:%S')
    produto = Estoque.objects.all().order_by('-id')
    entrada = Entrada.objects.all()
    saida = Saida.objects.all()
    quantidade_entrada = entrada.count()
    quantidade_saida = saida.count()
    quantidade_estoque = produto.count()
    total_gasto = Entrada.objects.aggregate(Sum('gasto'))['gasto__sum']
    total_gasto_conta = Conta.objects.aggregate(Sum('valor'))['valor__sum']
    total_gasto = total_gasto + total_gasto_conta
    total_gasto = round(total_gasto, 2)
    return render(request, "estoque/relatorios/relatorio_produto.html", {"produtos":produto, "data": data_e_hora_em_texto,
                                                                "qtd_estoque":quantidade_estoque,
                                                                "qtd_entrada":quantidade_entrada,
                                                                "qtd_saida":quantidade_saida, "total_gasto":total_gasto})

def deleteProd(request, id):
    produto = get_object_or_404(Produto, id=id)
    estoque = get_object_or_404(Estoque, nome=produto.nome, grupo=produto.grupo, preco=produto.preco)
    estoque.delete()
    produto.delete()
    return redirect(relaProd)

#GRUPO
def cadastrarGrp(request):
    return render(request, "estoque/cadastrar/cadastrarGrp.html")

def salvarGrp(request):
    try:
        snome = request.POST.get("nome")
        if snome:
            Grupo.objects.create(nome=snome)
        return redirect(cadastrarProd)
    except Exception as e:
        return render(request, "erro/erro.html")

def relaGrp(request):
    grupo = Grupo.objects.all().order_by('-id')
    return render(request, "estoque/relatorios/relatorio_grupo.html", {"grupo":grupo})

def deleteGrp(request, id ):
    grupo = Grupo.objects.get(id=id)
    grupo.delete()
    return redirect(relaGrp)

def editargrp(request, id):
    grupo = Grupo.objects.get(id=id)
    return render(request, "estoque/edicao/editar_grupo.html", {"grupo": grupo})

def editarGrp(request, id):
    nome = request.POST.get("nome")
    grupo = Grupo.objects.get(id=id)

    saida = Saida.objects.filter(grupo=grupo.nome)
    saida.update(grupo=nome)
    entrada = Entrada.objects.filter(grupo=grupo.nome)
    entrada.update(grupo=nome)

    produto = Produto.objects.filter(grupo=grupo.nome)
    produto.update(grupo=nome)

    estoque = Estoque.objects.filter(grupo=grupo.nome)
    estoque.update(grupo=nome)

    grupo.nome = nome
    grupo.save()
    return redirect(relaGrp)

#ENTRADA
def entrada(request, id):
    produto = Estoque.objects.get(id=id)
    usuario = Usuario.objects.all().order_by('-id').order_by('-id') 
    fornecedor = Fornecedor.objects.all().order_by('-id').order_by('-id') 
    return render(request, "estoque/entrada_saida/entrada.html", {"produto": produto, "usuarios":usuario, "fornecedores": fornecedor})

def salvarEnt(request, id):
    try:
        produto = Estoque.objects.get(id=id)
        data_e_hora_atuais = datetime.now()
        data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M:%S')
        quant= int(request.POST.get("quant"))
        usuario = request.POST.get("usuario")
        forn = request.POST.get("fornecedor")
        entforn = Fornecedor.objects.get(id=forn)
        entusua = Usuario.objects.get(id=usuario)
        if usuario:
            Entrada.objects.create(nome=produto.nome, usuario=entusua,
                                    quant=quant, forn=entforn, preco=round(produto.preco, 2),
                                    grupo=produto.grupo, data=data_e_hora_em_texto, gasto=(round(quant*produto.preco, 2)))
            produto.quant = round(produto.quant + quant, 2)
            produto.save()
            return redirect(redireciona)
    except Exception as e:
        return render(request, "estoque/erro/erro.html")
    
def deleteEnt(request, id):
    try:
        entrada = Entrada.objects.get(id=id)
        try:
            estoque = get_object_or_404(Estoque, nome=entrada.nome, grupo=entrada.grupo, preco=entrada.preco)
            print(estoque)
            estoque.quant = int(estoque.quant) - int(entrada.quant)
            print(estoque.quant)
            estoque.save()
            entrada.delete()
            return redirect(relaEnt)
        except Exception as e:
            return render(request, "erro/erro.html")
    except Exception as e:
        return render(request, "erro/erro.html")

def relaEnt(request):
    entrada = Entrada.objects.all().order_by('-id')
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M:%S')
    produto = Estoque.objects.all().order_by('-id')
    entrada = Entrada.objects.all()
    saida = Saida.objects.all()
    quantidade_entrada = entrada.count()
    quantidade_saida = saida.count()
    quantidade_estoque = produto.count()
    total_gasto = Entrada.objects.aggregate(Sum('gasto'))['gasto__sum']
    total_gasto_conta = Conta.objects.aggregate(Sum('valor'))['valor__sum']
    total_gasto = total_gasto + total_gasto_conta
    total_gasto = round(total_gasto, 2)
    return render(request, "estoque/relatorios/relatorio_entrada.html", {"entradas": entrada, "data": data_e_hora_em_texto, "qtd_estoque":quantidade_estoque,
                                                     "qtd_entrada":quantidade_entrada, "qtd_saida":quantidade_saida, "total_gasto":total_gasto})

def editarent(request, id):
    entrada = Entrada.objects.get(id=id)
    qtd = entrada.quant
    usuario = Usuario.objects.all().order_by('-id')
    fornecedor = Fornecedor.objects.all().order_by('-id')
    grupo = Grupo.objects.all().order_by('-id')
    return render(request, "estoque/edicao/editar_entrada.html", {"entrada": entrada, "usuarios": usuario,
                                                   "fornecedores": fornecedor, "grupos": grupo, "qtd": qtd})
def editarEnt(request, id, qtd):
    try:
        usuario = request.POST.get("usuario")
        quant = int(request.POST.get("quant"))
        forn = request.POST.get("fornecedor")

        entrada = Entrada.objects.get(id=id)
        entusuario = Usuario.objects.get(id=usuario)
        entforn = Fornecedor.objects.get(id=forn)

        estoque = get_object_or_404(Estoque, nome=entrada.nome, grupo=entrada.grupo, preco=round(entrada.preco, 2))
        estoque.quant = round(estoque.quant - qtd + quant, 2)
        estoque.save()

        # Atualizar
        entrada.usuario = entusuario.usuario
        entrada.quant = round(quant, 2)
        entrada.forn = entforn.nome
        print(quant)
        print(entrada.preco)
        print(quant * entrada.preco)
        entrada.gasto = round(quant * entrada.preco, 2)
        entrada.save()
        return redirect(relaEnt)
    
    except Exception as e:
        return render(request, "erro/erro.html")

# SAIDA
def saida(request, id):
    produto = Estoque.objects.get(id=id)
    usuario = Usuario.objects.all().order_by('-id') 
    fornecedor = Fornecedor.objects.all().order_by('-id') 
    return render(request, "estoque/entrada_saida/saida.html", {"produto": produto, "usuarios":usuario, "fornecedores": fornecedor})

def salvarSai(request, id):
    try:
        produto = Estoque.objects.get(id=id)
        data_e_hora_atuais = datetime.now()
        data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M:%S')
        quant= int(request.POST.get("quant"))
        usuario = request.POST.get("usuario")
        forn = request.POST.get("fornecedor")
        entforn = Fornecedor.objects.get(id=forn)
        entusua = Usuario.objects.get(id=usuario)
        if usuario:
            Saida.objects.create(nome=produto.nome, usuario=entusua,
                                    quant=round(quant, 2), forn=entforn, preco=round(produto.preco, 2),
                                    grupo=produto.grupo, data=data_e_hora_em_texto)
            produto.quant = round(produto.quant - quant, 2)
            produto.save()
            return redirect(redireciona)
    except Exception as e:
        return render(request, "erro/erro.html")

def relaSai(request):
    saida = Saida.objects.all().order_by('-id')
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M:%S')
    produto = Estoque.objects.all().order_by('-id')
    entrada = Entrada.objects.all()
    saida = Saida.objects.all()
    quantidade_entrada = entrada.count()
    quantidade_saida = saida.count()
    quantidade_estoque = produto.count()
    total_gasto = Entrada.objects.aggregate(Sum('gasto'))['gasto__sum']
    total_gasto_conta = Conta.objects.aggregate(Sum('valor'))['valor__sum']
    total_gasto = total_gasto + total_gasto_conta
    total_gasto = round(total_gasto, 2)
    return render(request, "estoque/relatorios/relatorio_saida.html", {"saidas": saida, "data": data_e_hora_em_texto, "qtd_estoque":quantidade_estoque,
                                                     "qtd_entrada":quantidade_entrada, "qtd_saida":quantidade_saida, "total_gasto":total_gasto})

def deleteSai(request, id):
    try:
        saida = Saida.objects.get(id=id)
        print(saida)
        try:
            estoque = get_object_or_404(Estoque, nome=saida.nome, grupo=saida.grupo, preco=saida.preco)
            estoque.quant = int(estoque.quant) + int(saida.quant)
            estoque.save()
            saida.delete()
            return redirect(relaSai)
        except Exception as e:
            return render(request, "erro/erro.html")
    except Exception as e:
        return render(request, "erro/erro.html")

def editarsai(request, id):
    saida = Saida.objects.get(id=id)
    qtd = saida.quant
    usuario = Usuario.objects.all().order_by('-id')
    fornecedor = Fornecedor.objects.all().order_by('-id')
    grupo = Grupo.objects.all().order_by('-id')
    return render(request, "estoque/edicao/editar_saida.html", {"saida": saida, "usuarios": usuario,
                                                   "fornecedores": fornecedor, "grupos": grupo, "qtd": qtd})

def editarSai(request, id, qtd):
    try:
        usuario = request.POST.get("usuario")
        quant = int(request.POST.get("quant"))
        forn = request.POST.get("fornecedor")

        saida = Saida.objects.get(id=id)
        entusuario = Usuario.objects.get(id=usuario)
        entforn = Fornecedor.objects.get(id=forn)

        estoque = get_object_or_404(Estoque, nome=saida.nome, grupo=saida.grupo, preco=round(saida.preco, 2))
        estoque.quant = round(estoque.quant + qtd - quant, 2)
        estoque.save()

        # Atualizar
        saida.usuario = entusuario.usuario
        saida.quant = round(quant, 2)
        saida.forn = entforn.nome
        print(quant)
        print(saida.preco)
        print(quant * saida.preco)
        saida.save()
        return redirect(relaSai)
    except Exception as e:
        return render(request, "erro/erro.html")

#FORNECEDOR
def cadastrarForn(request):
    return render(request, "estoque/cadastrar/cadastrarForn.html")

def salvarForn(request):
    try:
        nome = request.POST.get("nome")
        telefone = request.POST.get("telefone")
        if nome:
            Fornecedor.objects.create(nome=nome, telefone=telefone)
            return redirect(redireciona)
    except Exception as e:
        return render(request, "erro/erro.html")

def relaForn(request):
    fornecedor = Fornecedor.objects.all().order_by('-id')
    return render(request, "estoque/relatorios/relatorio_fornecedor.html", {"fornecedor" : fornecedor})

def deleteForn(request, id):
    try:
        forn = Fornecedor.objects.get(id=id)
        forn.delete()
        return redirect(relaForn)
    except Exception as e:
        return render(request, "erro/erro.html")

def editarforn(request, id):
    forn = Fornecedor.objects.get(id=id)
    return render(request, "estoque/edicao/editar_fornecedor.html", {"fornecedor": forn})

def editarForn(request, id):
    try:
        nome = request.POST.get("nome")
        telefone = request.POST.get("tel")
        forn = Fornecedor.objects.get(id=id)
        entrada = Entrada.objects.filter(forn=forn.nome)
        entrada.update(forn=nome)
        saida = Saida.objects.filter(forn=forn.nome)
        saida.update(forn=nome)
        forn.nome = nome
        forn.telefone = telefone
        forn.save()
        return redirect(relaForn)
    except Exception as e:
        return render(request, "erro/erro.html")

# RELATORIO GERAL
def relatorio(request):
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M:%S')
    estoque = Estoque.objects.all().order_by('-id')
    entrada = Entrada.objects.all().order_by('-id')
    saida = Saida.objects.all().order_by('-id')
    produto = Produto.objects.all().order_by('-id')
    conta = Conta.objects.all().order_by('-id')
    quantidade_entrada = entrada.count()
    quantidade_saida = saida.count()
    quantidade_estoque = produto.count()
    total_gasto = Entrada.objects.aggregate(Sum('gasto'))['gasto__sum']
    total_gasto_conta = Conta.objects.aggregate(Sum('valor'))['valor__sum']
    total_gasto = total_gasto + total_gasto_conta
    total_gasto = round(total_gasto, 2)
    return render(request, "estoque/relatorios/relatorio.html", {"produto":produto, "estoque": estoque, "entradas": entrada,
                                                         "conta": conta, "saidas": saida, "data": data_e_hora_em_texto,
                                                                "qtd_estoque":quantidade_estoque,
                                                                "qtd_entrada":quantidade_entrada,
                                                                "qtd_saida":quantidade_saida, "total_gasto":total_gasto})

# CONTAS
def nconta(request):
    aviso = None
    aviso_cad = None
    return render(request, "estoque/contas/nova_conta.html", {"aviso":aviso, "aviso_cad":aviso_cad})

def salvarconta(request):
    try:
        nome = request.POST.get("nome")
        valor = request.POST.get("valor")
        valor = float(valor)
        if Conta.objects.filter(nome=nome, valor=float(valor)).exists():
            aviso = True
            aviso_cad = None
            return render(request, "estoque/contas/nova_conta.html", {"aviso":aviso, "aviso_cad":aviso_cad})
        else:
            Conta.objects.create(nome=nome, valor=valor)
            aviso = None
            aviso_cad = True
            return render(request, "estoque/contas/nova_conta.html", {"aviso":aviso, "aviso_cad":aviso_cad})
    except Exception as e:
        return render(request, "erro/erro.html")
    
def relaConta(request):
    conta = Conta.objects.all().order_by('-id')
    return render(request, "estoque/contas/relatorio_conta.html", {"conta":conta})

def edicao(request, id):
    conta = Conta.objects.get(id=id)
    return render(request, "estoque/contas/editar.html", {"conta":conta})

def editarConta(request, id):
    conta = Conta.objects.get(id=id)
    nome = request.POST.get("nome")
    valor = request.POST.get("valor")
    conta.nome = nome
    conta.valor = valor
    conta.save()
    return redirect(relaConta)

def deleteConta(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    return redirect(relaConta)



#############################

#########AGENDAMENTO#########

#############################

def pg_age(request):
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M:%S')
    produto = Estoque.objects.all().order_by('-id')
    entrada = Entrada.objects.all()
    saida = Saida.objects.all()
    quantidade_entrada = entrada.count()
    quantidade_saida = saida.count()
    quantidade_estoque = produto.count()
    total_gasto = Entrada.objects.aggregate(Sum('gasto'))['gasto__sum']
    total_gasto_conta = Conta.objects.aggregate(Sum('valor'))['valor__sum']
    total_gasto = total_gasto + total_gasto_conta
    total_gasto = round(total_gasto, 2)
    return render(request, "agendamento/inicio/principal_age.html", {"estoque": produto,
                                                     "data": data_e_hora_em_texto, "qtd_estoque":quantidade_estoque,
                                                     "qtd_entrada":quantidade_entrada, "qtd_saida":quantidade_saida,
                                                     "total_gasto":total_gasto})

def cad_horario(request):
    return render(request, "agendamento/cadastrar/cad_horario.html")

def salvarhorario(request):
    if request.method == 'POST':
        dias_da_semana = ["domingo", "segunda", "terca", "quarta", "quinta", "sexta", "sabado"]

        # Apaga os horários existentes (caso queira sobrescrever os dados anteriores)
        Horario.objects.all().delete()
        
        for dia in dias_da_semana:
            # Obtém o valor do checkbox para o dia
            campo_dia = request.POST.get(dia)
            
            # Verifica se o checkbox está marcado
            if campo_dia:
                # Obtém os valores de início e término para o dia
                inicio = request.POST.get(f"inicio{dia.capitalize()}")
                termino = request.POST.get(f"termino{dia.capitalize()}")

                formato_hora = "%H:%M"
                inicio_time = datetime.strptime(inicio, formato_hora)
                termino_time = datetime.strptime(termino, formato_hora)

                # Calculando a diferença entre o término e o início
                diferenca = termino_time - inicio_time

                # Extraindo as horas e minutos da diferença
                horas, minutos = divmod(diferenca.seconds, 3600)
                minutos = minutos // 60

                # Exibindo o resultado no formato HH:MM
                hora_util = f"{horas:02}:{minutos:02}"
                
                # Salva as informações no banco de dados
                Horario.objects.create(
                    dia=dia.capitalize(),  # Salva o nome do dia capitalizado
                    inicio=inicio,
                    termino=termino,
                    hora_util=hora_util,
                    dia_de_trabalho=True
                )
        
        # Exibe uma mensagem de sucesso
        return redirect(cad_horario)

    # Exibe o formulário caso o método seja GET
    return render(request, "erro/erro.html")

def novo_agendamento(request):
    cortes = Corte.objects.all()
    return render(request, "agendamento/novo_agendamento/novo_agendamento.html", {"cortes": cortes})

def cad_corte(request):
    return render(request, "agendamento/cadastrar/cad_corte.html")

def salvar_corte(request):
    nome = request.POST.get("nome")
    preco = request.POST.get("preco")
    tempo = request.POST.get("tempo")
    Corte.objects.create(nome=nome, preco=preco, tempo=tempo)
    return redirect(cad_corte)

def age_corte(request, id):
    return render(request, "agendamento/novo_agendamento/conf_agenda.html")

def ir_teste(request, id):
    corte = Corte.objects.get(id=id)
    return render(request, "agendamento/novo_agendamento/teste.html", {"corte":corte})

@csrf_exempt  # Para testes, mas é melhor habilitar CSRF para segurança
def marcar(request):
    if request.method == 'POST':
        dia = request.POST.get('day')
        mes = request.POST.get('month')
        ano = request.POST.get('year')
        dia_semana = request.POST.get('weekday')
        id = request.POST.get('corte_id')
        corte = Corte.objects.get(id=id)
        nome = f"{dia_semana} {dia}-{mes}-{ano}"
        if verifica_dia(dia_semana):
            hor = True                                                                                                                             
            horarios = lista_horario(dia_semana, dia, mes, ano, corte.tempo)
            cortes = Corte.objects.all()
            return render(request, "agendamento/novo_agendamento/novo_agendamento.html", {"dia": dia,
                                    "mes": mes, "ano": ano, "dia_semana": dia_semana, "tempo": corte.tempo,
                                     "hor": hor, "horarios":horarios, "cortes": cortes})
            #aviso = True
            #mensagem = 'Horario Marcado!'
            #return render(request, "agendamento/novo_agendamento/novo_agendamento.html", {"cortes": cortes, "aviso": aviso, "msg": mensagem})
        elif verifica_existencia(nome) and verifica_dia(dia_semana) and verifica_dispo(corte.tempo, nome):
            agenda = get_object_or_404(Agenda, nome=nome)
            agenda.hora_disponivel = subtrair_tempo(agenda.hora_disponivel, corte.tempo)
            agenda.save()
            cortes = Corte.objects.all()
            aviso = True
            mensagem = 'Horario Marcado!'
            return render(request, "agendamento/novo_agendamento/novo_agendamento.html", {"cortes": cortes, "aviso": aviso, "msg": mensagem})
        else:
            cortes = Corte.objects.all()
            aviso = True
            mensagem = 'Não Foi Possivel Agendar, Tente Novamente!'
            return render(request, "agendamento/novo_agendamento/novo_agendamento.html", {"cortes": cortes, "aviso": aviso, "msg": mensagem})

def marcar_conf(request, dia_semana, dia, mes, ano, tempo, horario):
    nome = f"{dia_semana} {dia}-{mes}-{ano} - {horario}"
    hora = get_object_or_404(Horario, dia=obter_dia(dia_semana))
    hora = hora.hora_util
    if not verifica_existencia(nome):
        Agenda.objects.create(nome=nome, dia_semana=dia_semana, dia=dia,
                                mes=mes, ano=ano, horario=horario,
                                hora_disponivel=hora)
        cortes = Corte.objects.all()
        aviso = True
        mensagem = 'Horario Marcado!'
        return render(request, "agendamento/novo_agendamento/novo_agendamento.html", {"cortes": cortes,
                                "aviso": aviso, "msg":mensagem})
    else:
        return redirect(novo_agendamento)
