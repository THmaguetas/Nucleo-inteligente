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

    def __callback(self, recognizer, voice):
        try:
            texto = recognizer.recognize_google(voice, language="pt-BR").lower()
            if "surdo" in texto:
                texto = texto.replace("surdo", "sudo")

            self.entrada = texto
            print(self.entrada)             # APAGAR ISSO AQUI DEPOIS

            if self.gatilho is False:
                self.verify_gatilho()
                self.entrada = None

            elif self.gatilho:
                print('GATILHO TRUE, fale seu comando:')
                self.commands()

            
        except:
            pass

    def verify_gatilho(self):
        if "sudo" in self.entrada:
            self.gatilho = True
            self.entrada = None


    def commands(self):
        cmd = self.entrada.split()[0]
        if cmd == "executar":
            print('o comando irá executar seu pinto, desculpe a demora senhor')
            #  executa um .sh q eu tenho feito
        elif cmd == "abrir":
            pass # abrir um aplicativo do meu pc (vindo daquela pasta de atalhos)
        else:
            print('não tem comando assim não seu burro')
        self.gatilho = False



sudo_core = assistente()
sudo_core.voice_call() #voice detect in background

while True:
    gatilho = sudo_core.gatilho
    if gatilho is False:
        time.sleep(1)
        continue
    else:
         time.sleep(1)
         print(sudo_core.gatilho)
    print(sudo_core.entrada)
