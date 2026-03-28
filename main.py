from vosk import Model, KaldiRecognizer
import speech_recognition as sr
import json
import time
import os
from subprocess import run
#from dotenv import load_dotenv
#load_dotenv()

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
        # vosk config 
        self.model = Model("vosk_model/vosk-model-small-pt-0.3")
        self.vosk_rec = KaldiRecognizer(self.model, 44100)

        # mic config
        self.mic = sr.Microphone()
        self.rec = sr.Recognizer()
        self.sample_rate = self.mic.SAMPLE_RATE

        with self.mic as micro:
            self.rec.adjust_for_ambient_noise(micro, duration=4)
        self.rec.dynamic_energy_threshold = False
        self.rec.energy_threshold = 200

        # modos de escuta
        self.recognizer_gatilho = KaldiRecognizer(self.model, self.sample_rate,  '["sudo"]' )
        self.recognizer_comando = KaldiRecognizer(self.model, self.sample_rate)

        # base para toda a ramificação de comandos
        self.base_cmd_dir = f"{os.getcwd()}/comandos"

        # entradas e permissões por fala
        self.gatilho = False
        self.entrada = None
        self.command = None


    def voice_call(self):
        try:
            self.rec.pause_threshold = 0.8
            self.rec.non_speaking_duration = 0.5

            self.rec.listen_in_background(
                self.mic,
                self.__callback,
                phrase_time_limit=5
                )
        except Exception:
            confirm_action('error')


    def __callback(self, recognizer, voice): # não tenho a menor ideia do porque, mas o código só funciona com o parâmetro "recognizer" escrito, mesmo sem uso.
        # trata toda a entrada por voz e transforma em texto
        try:
            data = voice.get_raw_data()
            if self.vosk_rec.AcceptWaveform(data):
                result = json.loads(self.vosk_rec.Result())
                texto = result.get("text", "").lower()
            else:
                if self.vosk_rec.AcceptWaveform(data):
                    result = json.loads(self.vosk_rec.Result())
                    texto = result.get("text", "").lower()
                else:
                    return

            if "surdo" in texto:
                texto = texto.replace("surdo", "sudo")

            print("OUVI:", texto)

            # ativa o gatilho e troca o modo de escuta
            if not self.gatilho:
                if "sudo" in texto:
                    self.gatilho = True
                    confirm_action('acept')
                    self.vosk_rec = self.recognizer_comando
                    self.vosk_rec.Reset()
            else:
                self.entrada = texto
                self.gatilho = False
                self.vosk_rec = self.recognizer_gatilho
                self.vosk_rec.Reset()

            self.vosk_rec.Reset()

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

                print(nome_cmd, verify_name)
                if nome_cmd == verify_name:
                    try:
                        run([f"{dir_cmd}/{nome_cmd}{type_cmd}"])
                        print('sucesso')
                        return 'success'

                    except Exception as e:
                         print(e)
                         return 'error'
            else:
                print('ERRO: nome_cmd == verify_name não é verdade')
                return 'error'
        else:
            print('ERRO: a pasta não existe')
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
