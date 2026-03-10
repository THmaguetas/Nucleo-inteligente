import speech_recognition as sr
import time
import os
#from dotenv import load_dotenv
#load_dotenv()

class assistente:
    def __init__(self):
        # turn on mic
        self.mic = sr.Microphone()
        self.rec = sr.Recognizer()

        # pasta local
        self.atual_dir = os.getcwd()

        # entradas e permissões por fala
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


    def commands(self,):
        dir_commands = f"{self.atual_dir}/comandos"

        term_one = self.command.split()[0]
        term_two = self.command.split()[1]
        try: 
            term_tree = self.command.split()[2]
        except:
            term_tree = None

        # acho q se o chosen_cmd for feito dessa forma o aplicativo vai ficar muito engessado e limitado, preciso pensar em uma maneira de deixar isso mais genérico
        if term_tree is not None:
            chosen_cmd = f"{dir_commands}/{term_one}/{term_two}/{term_tree}"
        else:
            chosen_cmd = f"{dir_commands}/{term_one}/{term_two}"
            
        print(chosen_cmd)
        if True == False:
            os.system(f"bash  exec {chosen_cmd}")



sudo_core = assistente()
sudo_core.voice_call() #voice detect in background

while True:
    if sudo_core.entrada:
        sudo_core.command = sudo_core.entrada
        sudo_core.entrada = None
        sudo_core.commands()

    time.sleep(0.5)
