import os
import subprocess

def runserver():
    """Abre um novo terminal e executa o comando `runserver` do Django no diretório do script."""

    # Obtém o diretório atual (onde o script está localizado)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Comando a ser executado no novo terminal
    command = f'python manage.py runserver'

    # Constrói o comando para abrir um novo cmd e executar o comando Django
    full_command = f'start cmd /k "cd /d {current_dir} && {command}"'

    # Executa o comando para abrir o novo cmd
    subprocess.run(full_command, shell=True)

if __name__ == "__main__":
    runserver()
