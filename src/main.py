import os
import tkinter as tk
import pyfiglet
import sys
from termcolor import colored
from tkinter import filedialog
import contents 
from time import sleep

def loading_animation():
    animation = "|/-\\"
    for i in range(50):
        sleep(0.1)
        sys.stdout.write("\rCarregando " + animation[i % len(animation)] + " ")
        sys.stdout.flush()

def print_big_text(text, color):
    ascii_text = pyfiglet.figlet_format(text)
    colored_text = colored(ascii_text, color)
    print(colored_text)

def create_folder(name):
    if not os.path.exists(name):
        os.makedirs(name)

def create_file(path, content):
    with open(path, 'w') as file:
        file.write(content)

def create_hexagonal_structure(name_project, local):
    os.chdir(local)
    create_folder(name_project)
    os.chdir(name_project)
    os.system('npm init')
    os.system('npm install express dotenv mongodb debug')
    os.system('npm install -D jest eslint')
    os.system('git init')

    # folders source
    create_folder('src')
    create_folder('tests')
    create_folder('.vscode')

    # src
    os.chdir('src')
    create_folder('bin')
    create_folder('domain')
    create_folder('infrastructure')
    create_folder('interfaces')
    create_folder('useCases')

    # bin
    os.chdir('bin')
    create_file('www', contents.www)

    # domain
    os.chdir('..')
    os.chdir('domain')
    create_folder('user')
    os.chdir('user')
    create_file('index.js', contents.domain_user_index)
    create_file('userDomain.js', contents.domain_user_user_domain)
    create_file('userValidate.js', contents.domain_user_validate)

    # infrastructure
    os.chdir('..')
    os.chdir('..')
    os.chdir('infrastructure')
    create_folder('user')
    os.chdir('user')
    create_folder('db')
    create_folder('webserver')
    os.chdir('db')
    create_file('index.js', contents.infrastructure_user_db)
    os.chdir('..')
    os.chdir('webserver')
    create_file('routes.js', contents.infrastructure_user_webserver_routes)
    create_file('index.js', contents.infrastructure_user_webserver_index)

    # interfaces
    os.chdir('..')
    os.chdir('..')
    os.chdir('..')
    os.chdir('interfaces')
    create_folder('user')
    os.chdir('user')
    create_folder('controllers')
    create_folder('data-access')
    create_folder('express-callback')
    os.chdir('controllers')
    create_file('index.js', contents.interfaces_user_controllers_index)
    create_file('user-post.js', contents.interfaces_user_controllers_post)
    os.chdir('..')
    os.chdir('data-access')
    create_file('index.js', contents.interfaces_user_data_access_index)
    create_file('user-db.js', contents.interfaces_user_data_access_user_db)
    os.chdir('..')
    os.chdir('express-callback')
    create_file('index.js', contents.interfaces_user_express_callback)

    # useCases
    os.chdir('..')
    os.chdir('..')
    os.chdir('..')
    os.chdir('useCases')
    create_folder('user')
    os.chdir('user')
    create_file('index.js', contents.use_cases_user_index)
    create_file('createUser.js', contents.use_cases_user_create)

    # tests
    os.chdir('..')
    os.chdir('..')
    os.chdir('..')
    os.chdir('tests')
    create_folder('unit')
    os.chdir('unit')
    create_folder('domain')
    create_folder('interfaces')
    create_folder('useCases')


if __name__ == '__main__':
    print_big_text('CLI-CLEAN-ARCHITECTURE', 'magenta')
    print('Esta é uma ferramenta que irá criar um projeto em Node.js seguindo o padrão de Arquitetura limpa')
    loading_animation()
    name = str(input('\r\033[K\nnome do projeto: '))
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    create_hexagonal_structure(name, folder_path)
