import tkinter as tk
import utils as ut
from termcolor import colored
from tkinter import filedialog
from time import sleep
from app import create_hexagonal_structure

if __name__ == '__main__':
    ut.print_big_text('CLI-CLEAN-ARCHITECTURE', 'magenta')
    print('Esta é uma ferramenta que irá criar um projeto em Node.js seguindo o padrão de Arquitetura limpa')
    ut.loading_animation()
    name = ut.read_str('\r\033[K\nnome do projeto: ')
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    create_hexagonal_structure(name, folder_path)
