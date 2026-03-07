import speech_recognition as sr
import os
import subprocess
import time
from dotenv import load_dotenv
load_dotenv()

class assistente:
    def __init__(self):
        self.mic = sr.Microphone()
        self.rec = sr.Recognizer()
        self.entrada = None
        self.gatilho = False
        self.command = None


    def verify_gatilho(self):
        if "sudo" in self.entrada:
            self.gatilho = True
            self.entrada = None

    def __callback(self, recognizer, voice):
        try:
            texto = recognizer.recognize_google(voice, language="pt-BR").lower()
            if "surdo" in texto:
                texto = texto.replace("surdo", "sudo")

            self.entrada = texto

            if self.gatilho is False:
                self.verify_gatilho()

        except:
            pass

    def voice_call(self):
        try:
            with self.mic as micro:
                self.rec.adjust_for_ambient_noise(micro, duration=2)
            self.rec.energy_threshold = 250
            self.rec.pause_threshold = 1.2
            self.rec.non_speaking_duration = 1
            self.rec.dynamic_energy_threshold = True

            self.rec.listen_in_background(self.mic, self.__callback)
        except:
            pass

    def input_command(self):
        cmd = self.entrada[0]
        if cmd == "executar":
            pass #  executa um .sh q eu tenho feito
        elif cmd == "abrir":
            pass # abrir um aplicativo do meu pc (vindo daquela pasta de atalhos)



sudo = assistente()
sudo.voice_call() #voice detect in background

while True:
    gatilho = sudo.gatilho
    if gatilho is False:
        time.sleep(1)
        continue
    print(gatilho)

    sudo.input_command()
    command = sudo.command


    kills = ["sair", "fechar", "break", "tchau", "adeus"]
    if command in kills:
        break
