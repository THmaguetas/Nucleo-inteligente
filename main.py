import speech_recognition as sr
import time
import json
import os
from subprocess import run

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


class assistente:
    def __init__(self):
        # config do user
        user_conf = config()

        # turn on mic
        self.mic = sr.Microphone()
        self.rec = sr.Recognizer()

        # base para toda a ramificação de comandos
        if user_conf["commands_dir"].lower() == "atual":
            self.base_cmd_dir = f"{os.getcwd()}/comandos"
        else:
            self.base_cmd_dir = f"{user_conf["commands_dir"]}"

        # entradas e permissões por fala
        self.name_gatilho = user_conf["nome_gatilho"]
        self.gatilho = False
        self.entrada = None
        self.command = None


    def voice_call(self):
        try:
            with self.mic as micro:
                self.rec.adjust_for_ambient_noise(micro, duration=4)
            self.rec.pause_threshold = 0.8
            self.rec.non_speaking_duration = 0.5
            self.rec.dynamic_energy_threshold = True

            self.rec.listen_in_background(
                self.mic,
                self.__callback,
                phrase_time_limit=5
                )
        except Exception:
            confirm_action('error')


    def __callback(self, recognizer, voice):
        try:
            texto = recognizer.recognize_google(voice, language="pt-BR").lower()
            if self.name_gatilho in texto:
                texto = texto.replace("surdo", "sudo")

            if self.gatilho is False:
                if self.name_gatilho in texto:
                    self.gatilho = True
                    confirm_action('acept')
            else:
                self.entrada = texto
                self.gatilho = False

        except Exception:
            pass


    def exec_commands(self):
        base_commands = self.base_cmd_dir
        comando = self.command

        dir_cmd = os.path.join(base_commands, *comando[:-1])
        nome_cmd = comando[-1]

        if os.path.isdir(dir_cmd):
            for arq in os.listdir(dir_cmd):
                verify_name = os.path.splitext(arq)[0]
                type_cmd =  os.path.splitext(arq)[-1]

                if nome_cmd == verify_name:
                    try:
                        run([f"{dir_cmd}/{nome_cmd}{type_cmd}"])
                        return 'success'

                    except Exception:
                         return 'error'
            else:
                return 'error'
        else:
            return 'error'



sudo_core = assistente()
sudo_core.voice_call() #voice detect in background
confirm_action('start')

while True:
    if sudo_core.entrada:
        sudo_core.command = sudo_core.entrada.split()
        sudo_core.entrada = None
        cmd = sudo_core.exec_commands()

        sudo_core.gatilho = False
        if cmd == 'acept':
            confirm_action( 'acept')
        elif cmd == 'success':
            confirm_action('success')
        elif cmd == 'error':
            confirm_action('error')

    time.sleep(0.5)
