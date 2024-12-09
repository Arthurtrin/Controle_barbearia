from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, time, timedelta

def verifica_dia(dia_semana):

    for i in range(7):
        if dia_semana == "Domingo":
            dia_vrf = "dom"
            break
        elif dia_semana == "Segunda-feira":
            dia_vrf = "seg"
            break
        elif dia_semana == "Terça-feira":
            dia_vrf = "ter"
            break
        elif dia_semana == "Quarta-feira":
            dia_vrf = "qua"
            break
        elif dia_semana == "Quinta-feira":
            dia_vrf = "qui"
            break
        elif dia_semana == "Sexta-feira":
            dia_vrf = "sex"
            break
        elif dia_semana == "Sábado":
            dia_vrf = "sab"
            break

    horario = Horario.objects.all()

    # Inicializar os dias como None
    dias_da_semana = {
        "dom": None,
        "seg": None,
        "ter": None,
        "qua": None, 
        "qui": None,
        "sex": None,
        "sab": None,
    }

    # Iterar sobre os horários
    for item in horario:
        if item.dia == "Domingo" and dias_da_semana["dom"] is None:
            dias_da_semana["dom"] = True
        elif item.dia == "Segunda" and dias_da_semana["seg"] is None:
            dias_da_semana["seg"] = True
        elif item.dia == "Terca" and dias_da_semana["ter"] is None:
            dias_da_semana["ter"] = True
        elif item.dia == "Quarta" and dias_da_semana["qua"] is None:
            dias_da_semana["qua"] = True
        elif item.dia == "Quinta" and dias_da_semana["qui"] is None:
            dias_da_semana["qui"] = True
        elif item.dia == "Sexta" and dias_da_semana["sex"] is None:
            dias_da_semana["sex"] = True
        elif item.dia == "Sabado" and dias_da_semana["sab"] is None:
            dias_da_semana["sab"] = True

    return dias_da_semana[dia_vrf]

def verifica_existencia(nome):
    existe = Agenda.objects.filter(nome=nome).exists()
    return existe

def verifica_dispo(tempo, nome):
    agenda = get_object_or_404(Agenda, nome=nome)
    if agenda.hora_disponivel >= tempo:
        return True
    return None

def criar_agenda(request, dia, mes, ano, dia_semana, nome, hora_disponivel):
    aviso = True
    mensagem = 'Horario Marcado!'
    return render(request, "agendamento/novo_agendamento/novo_agendamento.html", {"dia": dia,
                                    "mes": mes, "ano": ano, "dia_semana": dia_semana, "nome": nome,
                                    "hora_disponivel": hora_disponivel, "aviso": aviso,
                                    "msg": mensagem})

def vrf_hora_util(dia_semana):
    for i in range(7):
        if dia_semana == "Domingo":
            dia_vrf = "Domingo"
            break
        elif dia_semana == "Segunda-feira":
            dia_vrf = "Segunda"
            break
        elif dia_semana == "Terça-feira":
            dia_vrf = "Terca"
            break
        elif dia_semana == "Quarta-feira":
            dia_vrf = "Quarta"
            break
        elif dia_semana == "Quinta-feira":
            dia_vrf = "Quinta"
            break
        elif dia_semana == "Sexta-feira":
            dia_vrf = "Sexta"
            break
        elif dia_semana == "Sábado":
            dia_vrf = "Sabado"
            break

    horario = get_object_or_404(Horario, dia=dia_vrf)
    return horario.hora_util

def subtrair_tempo(hora_inicial, tempo_para_subtrair):
    """
    Subtrai um tempo de outro e retorna o resultado no formato HH:MM:SS.

    :param hora_inicial: Um objeto datetime.time representando o horário inicial.
    :param tempo_para_subtrair: Um objeto datetime.time representando o tempo a ser subtraído.
    :return: Uma string no formato HH:MM:SS representando o horário resultante.
    """
    # Converter `hora_inicial` para um objeto datetime
    hora_base = datetime.combine(datetime.today(), hora_inicial)

    # Converter `tempo_para_subtrair` para um timedelta
    tempo_subtraido = timedelta(
        hours=tempo_para_subtrair.hour,
        minutes=tempo_para_subtrair.minute,
        seconds=tempo_para_subtrair.second
    )

    # Realizar a subtração
    resultado = hora_base - tempo_subtraido

    # Garantir que o tempo não seja negativo
    if resultado < datetime.combine(datetime.today(), datetime.min.time()):
        resultado = datetime.combine(datetime.today(), datetime.min.time())

    # Retornar o resultado no formato HH:MM:SS
    return resultado.time().strftime('%H:%M:%S')


def lista_horario(dia_semana, dia, mes, ano, tempo):
    for i in range(7):
        if dia_semana == "Domingo":
            dia_horario = "Domingo"
            break
        elif dia_semana == "Segunda-feira":
            dia_horario = "Segunda"
            break
        elif dia_semana == "Terça-feira":
            dia_horario = "Terca"
            break
        elif dia_semana == "Quarta-feira":
            dia_horario = "Quarta"
            break
        elif dia_semana == "Quinta-feira":
            dia_horario = "Quinta"
            break
        elif dia_semana == "Sexta-feira":
            dia_horario = "Sexta"
            break
        elif dia_semana == "Sábado":
            dia_horario = "Sabado"
            break

    horario = get_object_or_404(Horario, dia=dia_horario)
    total_hora_disponivel = horario.hora_util
    #h_util = calcular_intervalos(h_util, tempo)
    #print(horario.inicio, horario.termino, tempo)
    horarios = gerar_horarios(horario.inicio, horario.termino, tempo)
    return horarios
    
def obter_dia(dia_semana):
    for i in range(7):
        if dia_semana == "Domingo":
            dia = "Domingo"
            break
        elif dia_semana == "Segunda-feira":
            dia = "Segunda"
            break
        elif dia_semana == "Terça-feira":
            dia = "Terca"
            break
        elif dia_semana == "Quarta-feira":
            dia = "Quarta"
            break
        elif dia_semana == "Quinta-feira":
            dia = "Quinta"
            break
        elif dia_semana == "Sexta-feira":
            dia = "Sexta"
            break
        elif dia_semana == "Sábado":
            dia = "Sabado"
            break
    return dia

def calcular_intervalos(tempo_total, intervalo):
    """
    Calcula quantas vezes um intervalo de tempo cabe dentro de um tempo total.

    :param tempo_total: Um objeto datetime.time representando o tempo total.
    :param intervalo: Um objeto datetime.time representando o intervalo.
    :return: Um número inteiro representando a quantidade de vezes que o intervalo cabe dentro do tempo total.
    """
    def time_to_timedelta(t):
        """
        Converte um objeto datetime.time para um objeto timedelta.
        """
        return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    
    # Converter os tempos para timedelta
    try:
        tempo_total_timedelta = time_to_timedelta(tempo_total)
        intervalo_timedelta = time_to_timedelta(intervalo)
    except AttributeError:
        raise TypeError("Os parâmetros devem ser do tipo datetime.time.")
    
    # Verificar se o intervalo é válido
    if intervalo_timedelta.total_seconds() == 0:
        raise ValueError("O intervalo não pode ser zero.")

    # Calcular a quantidade de intervalos
    return tempo_total_timedelta // intervalo_timedelta


def gerar_horarios(h_inicio, h_fim, incremento):
    """
    Gera uma lista de horários incrementados entre `h_inicio` e `h_fim`, com um intervalo definido por `incremento`.

    :param h_inicio: Um objeto datetime.time ou string no formato HH:MM:SS representando o horário inicial.
    :param h_fim: Um objeto datetime.time ou string no formato HH:MM:SS representando o horário final.
    :param incremento: Um objeto datetime.time ou string no formato HH:MM:SS representando o incremento.
    :return: Uma lista de strings no formato HH:MM:SS representando os horários incrementados.
    """
    def convert_to_timedelta(horario):
        """
        Converte um horário no formato string ou datetime.time para um objeto timedelta.
        """
        if isinstance(horario, str):  # Caso seja string
            horas, minutos, segundos = map(int, horario.split(':'))
            return timedelta(hours=horas, minutes=minutos, seconds=segundos)
        elif isinstance(horario, time):  # Caso seja objeto datetime.time
            return timedelta(hours=horario.hour, minutes=horario.minute, seconds=horario.second)
        else:
            raise ValueError("Formato inválido. Deve ser string no formato HH:MM:SS ou objeto datetime.time")

    # Converte os horários para timedelta
    h_inicio_timedelta = convert_to_timedelta(h_inicio)
    h_fim_timedelta = convert_to_timedelta(h_fim)
    incremento_timedelta = convert_to_timedelta(incremento)

    # Verifica se o incremento é válido
    if incremento_timedelta.total_seconds() <= 0:
        raise ValueError("O incremento deve ser maior que zero.")
    if h_inicio_timedelta > h_fim_timedelta:
        raise ValueError("O horário inicial não pode ser maior que o horário final.")

    horarios = []
    horario_atual = h_inicio_timedelta

    # Adiciona horários incrementais à lista
    while horario_atual < h_fim_timedelta:
        horarios.append(str((datetime.min + horario_atual).time()))
        horario_atual += incremento_timedelta

    return horarios