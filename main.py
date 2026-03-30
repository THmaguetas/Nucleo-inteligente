import speech_recognition as sr
import time
import json
import os
from subprocess import run

from configs import funcs

# arquivo das config do usuário
user_conf = funcs.config()

class assistente:
    def __init__(self):
        # turn on mic
        self.mic = sr.Microphone()
        self.rec = sr.Recognizer()

        # base para toda a ramificação de comandos
        if user_conf["commands_dir"].lower() == "atual":
            os.makedirs(f"{os.getcwd()}/comandos", exist_ok=True)
            self.base_cmd_dir = f"{os.getcwd()}/comandos/"
        else:
            if user_conf["commands_dir"]:
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
            funcs.confirm_action('error')


    def __callback(self, recognizer, voice):
        try:
            texto = recognizer.recognize_google(voice, language="pt-BR").lower()

            if self.gatilho is False:
                if self.name_gatilho in texto:
                    self.gatilho = True
                    funcs.confirm_action('acept')
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
                        run(["sudo", "-n", f"{dir_cmd}/{nome_cmd}{type_cmd}"])
                        return 'success'

                    except Exception as e:
                         print(e)
                         return 'error'
            else:
                return 'error'
        else:
            return 'error'



Core = assistente()
Core.voice_call() #voice detect in background
funcs.confirm_action('start')

while True:
    if Core.entrada:
        print("ENTRADA:", Core.entrada)
        Core.command = Core.entrada.split()
        Core.entrada = None
        cmd = Core.exec_commands()

        Core.gatilho = False
        if cmd == 'acept':
            funcs.confirm_action( 'acept')
        elif cmd == 'success':
            funcs.confirm_action('success')
        elif cmd == 'error':
            funcs.confirm_action('error')

    time.sleep(0.5)
