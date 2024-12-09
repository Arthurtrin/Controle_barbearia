import os
import webbrowser

# Nome do arquivo .bat que será criado
nome_arquivo_bat = 'iniciar.bat'

# Diretório do seu projeto Django
diretorio_projeto_django = os.path.dirname(os.path.abspath(__file__))

# Conteúdo do arquivo .bat
conteudo_bat = f'''@echo off
rem Navegue até o diretório do seu projeto Django
cd "{diretorio_projeto_django}"

rem Execute o servidor Django
python manage.py runserver

rem Mantenha a janela aberta para visualizar os logs
pause
'''

# Criar e escrever o conteúdo no arquivo .bat
with open(nome_arquivo_bat, 'w') as arquivo:
    arquivo.write(conteudo_bat)

print(f'Arquivo {nome_arquivo_bat} criado com sucesso!')

# Comando para executar o arquivo .bat
os.system(f'start {nome_arquivo_bat}')  # No Windows

# URL que você deseja abrir
url = 'http://127.0.0.1:8000/'

# Abre a URL no navegador padrão
webbrowser.open(url)
