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


    def call_back(self, recognizer, voice):
        try:
            texto = recognizer.recognize_google(voice, language="pt-BR").lower()
            if "surdo" in texto:
                texto = texto.replace("surdo", "sudo")
            self.entrada = texto
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
            
            voice = self.rec.listen_in_background(self.mic, self.call_back)
            return self.entrada
        except:
            return None



#--------------------------------------------------------------------

var = assistente()
var.voice_call() #voice detect in background

while True:
    if var.entrada:
        time.sleep(1)
        print(var.entrada)

    if var.entrada in ["sair", "fechar", "break", "tchau", "adeus"]:
        break
