#!/usr/bin/env python3

import speech_recognition as sr
import time
from glob import glob
import os
from subprocess import run
#from dotenv import load_dotenv
#load_dotenv()

def confirm_action(tipo):
    if tipo == True:
        os.system("beep -f 3000 -l 30 -r2")
    elif tipo == False:
        os.system("beep -f 500 -l 250")
    elif tipo == 'start':
        os.system("beep -f 4000 -l 100 -r4")
    else:
        pass


class assistente:
    def __init__(self):
        # turn on mic
        self.mic = sr.Microphone()
        self.rec = sr.Recognizer()

        # base para toda a ramificação de comandos
        self.base_cmd_dir = f"{os.getcwd()}/comandos"

        # entradas e permissões por fala
        self.gatilho = True
        self.entrada = "executar config"
        self.command = None


    def voice_call(self):
        try:
            with self.mic as micro:
                self.rec.adjust_for_ambient_noise(micro, duration=4)
            #self.rec.energy_threshold = 250
            self.rec.pause_threshold = 0.8
            self.rec.non_speaking_duration = 0.5
            self.rec.dynamic_energy_threshold = True

            self.rec.listen_in_background(
                self.mic,
                self.__callback,
                phrase_time_limit=5
                )
        except Exception:
            confirm_action(False)


    def __callback(self, recognizer, voice):
        try:
            texto = recognizer.recognize_google(voice, language="pt-BR").lower()
            if "surdo" in texto:
                texto = texto.replace("surdo", "sudo")

            if self.gatilho is False:
                if "sudo" in texto:
                    self.gatilho = True
                    confirm_action(True)
            else:
                self.entrada = texto
                self.gatilho = False

        except Exception:
            pass


    def exec_commands(self):
        base_commands = self.base_cmd_dir
        comando = self.command

        full_dir_cmd = os.path.join(base_commands, *comando)
        print('FULL DIR CMD: ', full_dir_cmd)

        if os.path.exists(full_dir_cmd):
            print('diretório existe')
            true_cmd = next(
                (f for f in os.path.listdir(dir_cmd) if os.path.isfile(os.path.join(dir_cmd, f)) and os.path.splitext(f)[0] == name_cmd),
                None
            )
            print(true_cmd)

            if os.path.isfile(true_cmd):
                print('diretório é um arquivo')
                dir_cmd = os.path.join(base_commands, *comando[:-1])
                name_cmd = comando[-1]

                print(dir_cmd, name_cmd)

                try:
                    run([f"{dir_cmd}/{true_cmd}"])
                    return True
                except Exception as e:
                    print(e)
                    return False


            elif os.path.isdir(full_dir_cmd):
                pasta = os.listdir(dir_cmd)
                if len(pasta) > 0:
                    arq_correct = None
                    cont = 0
                    for arq in pasta:
                        if os.path.isfile(f"{dir_cmd}/{arq}") and os.access(f"{dir_cmd}/{arq}", os.X_OK):
                            cont += 1
                            arq_correct = arq
                    if cont == 1:
                        try:
                            run([f"{dir_cmd}/{arq_correct}"])
                            return True
                        except Exception:
                            return False

            else:
                return False

        else:
            parametro = comando[-1]
            cmd_full = os.path.join(base_commands, *comando[:-1])
            try:
                run([cmd_full, parametro])
                return True
            except Exception:
                return False




sudo_core = assistente()
sudo_core.voice_call() #voice detect in background
confirm_action('start')

while True:
    if sudo_core.entrada:
        sudo_core.command = sudo_core.entrada.split()
        sudo_core.entrada = None
        cmd = sudo_core.exec_commands()

        sudo_core.gatilho = False
        if cmd == True:
            confirm_action(True)
        elif cmd == False:
            confirm_action(False)

    time.sleep(0.5)
