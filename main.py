import speech_recognition as sr
import time
import os
from subprocess import run
#from dotenv import load_dotenv
#load_dotenv()

class assistente:
    def __init__(self):
        # turn on mic
        self.mic = sr.Microphone()
        self.rec = sr.Recognizer()

        # base para toda a ramificação de comandos
        self.base_cmd_dir = f"{os.getcwd()}/comandos"

        # entradas e permissões por fala
        self.gatilho = False
        self.entrada =None
        self.command = None


    def voice_call(self):
        try:
            with self.mic as micro:
                self.rec.adjust_for_ambient_noise(micro, duration=2)
            self.rec.energy_threshold = 250
            self.rec.pause_threshold = 1.2
            self.rec.non_speaking_duration = 1
            self.rec.dynamic_energy_threshold = True

            self.rec.listen_in_background(self.mic, self.__callback)
        except Exception as e:
            print(e)


    def __callback(self, recognizer, voice):
        try:
            texto = recognizer.recognize_google(voice, language="pt-BR").lower()
            if "surdo" in texto:
                texto = texto.replace("surdo", "sudo")

            if self.gatilho is False:
                if "sudo" in texto:
                    self.gatilho = True
                    print('DIGA SEU COMANDO')
            else:
                self.entrada = texto
                self.gatilho = False

        except Exception as e:
            print(e)


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

                    except Exception as e:
                        print(e)
        else:
            print("comando não existe")




sudo_core = assistente()
sudo_core.voice_call() #voice detect in background

while True:
    if sudo_core.entrada:
        sudo_core.command = sudo_core.entrada.split()
        sudo_core.entrada = None
        sudo_core.exec_commands()
        sudo_core.gatilho = False

    time.sleep(0.5)
