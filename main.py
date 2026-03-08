import speech_recognition as sr
import time
import os
#from dotenv import load_dotenv
#load_dotenv()
from comandos.executar import executar
from comandos.abrir import abrir

class assistente:
    def __init__(self):
        # turn on mic
        self.mic = sr.Microphone()
        self.rec = sr.Recognizer()

        # entradas e permissões por fala
        self.entrada = None
        self.gatilho = False
        self.command = None

        # instâncias das funções
        self.exec = executar()
        self.open = abrir()
        self.funçoes = {
            "executar":{
                "update": self.exec.update,
                "clear": self.exec.clear_sys
            },
            "abrir" : {
                "terminal": self.open.kitty
            },
            "fechar": self.fechar
        }


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

            if self.gatilho is False:
                if "sudo" in texto:
                    self.gatilho = True
                    print('DIGA SEU COMANDO')
            else:
                self.gatilho = False
                self.entrada = texto

        except Exception as e:
            print(e)


    def commands(self):
        func = self.entrada.split()[0]
        try:
            cmd = self.entrada.split()[1]
        except:
            cmd = None
            print(F'FUNC É: {func}')     # APAGAR ISSO AQUI DEPOIS
            print(f'CMD É: {cmd}')           # APAGAR ISSO AQUI DEPOIS

        if func in self.funçoes:
            if cmd is not None and cmd in self.funçoes[func] :
                print("func:", func)
                print("cmd:", cmd)
                print("tipo:", type(self.funcoes[func][cmd]))

                self.funçoes[func][cmd]()
                
            elif cmd is None:
                self.funçoes[func]()

            else:
                print('não tem comando assim não seu burro')
        else:
            print('não tem comando assim não seu burro')
        self.gatilho = False



sudo_core = assistente()
sudo_core.voice_call() #voice detect in background

while True:

    if not sudo_core.awake:
        break

    time.sleep(0.5)
