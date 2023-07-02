import inquirer
import tkinter as tk
import utils as ut
from tkinter import filedialog
from app import create_hexagonal_structure_mongo
import sys

questions = [
    inquirer.List('database',
                  message='Escolha um banco de dados:',
                  choices=['MySQL', 'MongoDB']
                  ),
]


def handle_keypress(event):
    if event.name == 'esc':
        print("Tecla ESC pressionada. Encerrando o programa...")
        pass

if __name__ == '__main__':
    ut.print_big_text('CLI-CLEAN-ARCHITECTURE', 'magenta')
    print('Esta é uma ferramenta que irá criar um projeto em Node.js seguindo o padrão de Arquitetura limpa')
    ut.loading_animation()
    name = ut.read_str('\r\033[K\nnome do projeto: ')
    answers = inquirer.prompt(questions)
    selected_database = answers['database']
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
            create_hexagonal_structure_mongo(name, folder_path, selected_database)
            break
    sys.exit()