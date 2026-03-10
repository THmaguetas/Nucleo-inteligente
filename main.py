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


    def exec_commands(self,):
        dir_commands = f"{self.atual_dir}/comandos"
        comando = self.command

        self.__verify_command(cmd=comando)

        # acho q se o chosen_cmd for feito dessa forma o aplicativo vai ficar muito engessado e limitado, preciso pensar em uma maneira de deixar isso mais genérico
        if len(comando) == 3:
            chosen_cmd = f"{comando[0]}/{comando[1]}/{comando[2]}"
        else:
            chosen_cmd = f"{comando[0]}/{comando[1]}"
        print(chosen_cmd)

        if True == False:
            os.system(f"bash  exec {dir_commands}/{chosen_cmd}")


    def __verify_command(self, cmd):
        list_commands = os.listdir(f'{self.atual_dir}/comandos')
        print( list_commands)
        
        if cmd[0] in list_commands:
            list_params = os.listdir(f'{self.atual_dir}/comandos/{cmd[0]}')
            print(list_params)
            if cmd[1] in list_params:
                return True
        else:
            return False



sudo_core = assistente()
sudo_core.voice_call() #voice detect in background

while True:
    if sudo_core.entrada:
        sudo_core.command = sudo_core.entrada.split()
        sudo_core.entrada = None
        sudo_core.exec_commands()

    time.sleep(0.5)
