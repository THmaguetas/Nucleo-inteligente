import os
import json

# arquivo das config do usuário
def config():
    with open("config.json", 'r')as arq:
        return json.load(arq)


def confirm_action(tipo):
    if tipo == 'acept':
        os.system("beep -f 3000 -l 30 -r2")
    elif tipo == 'success':
        os.system("beep -f 3000 -l 150")
    elif tipo == 'error':
        os.system("beep -f 500 -l 250")
    elif tipo == 'start':
        os.system("beep -f 4000 -l 100 -r4")
    else:
        pass

