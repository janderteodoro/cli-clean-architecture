import inquirer
import tkinter as tk
import utils as ut
from tkinter import filedialog
from app import create_hexagonal_structure
from time import sleep
import platform
from pathlib import Path
import sys

os_name = platform.system()
desktop_path = Path.home() / "Desktop"
folder_windows = desktop_path.resolve()

questions = [
    inquirer.List('database',
                  message='Escolha um banco de dados',
                  choices=['\033[38;2;255;255;0mMySQL\033[0m', '\033[38;2;0;255;0mMongoDB\033[0m']
                  ),
]


def handle_keypress(event):
    if event.name == 'esc':
        print("Tecla ESC pressionada. Encerrando o programa...")
        pass

if __name__ == '__main__':
    ut.print_big_text('CLI\nCLEAN-\nARCHITECTURE', 'magenta')
    print('Esta é uma ferramenta que irá criar uma API em Node.js seguindo o padrão de Arquitetura limpa!!!')
    print('\n\nby: Jander Teodoro\ngithub: \033[38;2;0;0;255mhttps://github.com/janderteodoro\033[0m\n\n')
    ut.loading_animation()
    name = ut.read_str('\r\033[K\nnome do projeto: ')
    answers = inquirer.prompt(questions)
    selected_database = answers['database']
    
    if os_name != 'Windows':
        root = tk.Tk()
        root.withdraw()
        while True:
            try:
                folder_path = filedialog.askdirectory()
            except KeyboardInterrupt:
                continue
            except:
                print('Escolha uma pasta para criar o seu projeto')
            finally:
                try:
                    create_hexagonal_structure(name, folder_path, selected_database)
                    break
                except:
                    print('Encerrando o programa...')
                    sleep(2)
                    sys.exit()
        sys.exit()
    else:
        try:
            create_hexagonal_structure(name, folder_windows, selected_database)
            sys.exit()
        except:
            print('Encerrando o programa...')
            sleep(2)
            sys.exit()