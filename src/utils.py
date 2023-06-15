import sys
import pyfiglet
import os
from time import sleep
from termcolor import colored

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

def read_str(txt):
    while True:
        try:
            option = str(input(txt)).strip()
            return option
        except:
            print('Insira um valor valido')
            continue
