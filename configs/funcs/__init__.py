import os
import json

# arquivo das config do usuário
def config(dir):
    os.makedirs(dir, exist_ok=True)

    arquivo = f"{dir}/config.json"
    default_config = {
        "nome_gatilho": "pitaya",
        "commands_dir": "atual"
    }

    if not os.path.exists(arquivo):
        with open(arquivo, 'w') as arq:
            json.dump(default_config, arq)
        return default_config 

    with open(arquivo, 'r') as arq:
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

