# -*- encoding: utf-8 -*-
################# Requirements #####################
# sudo pip install speechrecognition
# sudo apt-get install portaudio19-dev
# sudo pip install pyaudio
# sudo pip install snowboy      # Se der erro, tem que compilar na mão
# sudo pip install espeak		# -ven -> english. -vpt -> pt-br
####################################################

from snowboy.snowboydecoder import HotwordDetector
import speech_recognition as sr
import sys
import subprocess

# Parametros
AUDIO_GAIN = 0.95
SENSITIVITY = 0.35
recognized =''
DECODER_MODEL = sys.argv[1]
SR = sr.Recognizer()

def callback_fn():
    # print('I am hear you!')
    subprocess.call(['espeak', '-ven', 'i am ready'])

def record_callback(audio_file):
    print("Running speech recognition...")
    with sr.AudioFile(audio_file) as source:
        audio = SR.record(source)

    try:
    	print('Detecting...')
        recognized = SR.recognize_google(audio, language='en-US')
        print('\n"{}"\n'.format(recognized.encode('utf-8')))

        # Fala o que foi reconhecido usando o espeak
        subprocess.call(['espeak', '-ven', recognized])
        if 'bye-bye' in recognized:
        	sys.exit()

    except sr.UnknownValueError:
        print("Nothing detected!")
    except sr.RequestError:
    	print('Without internet conection!')

    print('Call me when you need!')

# Notifica a falta do segundo argumento da função
if len(sys.argv) != 2:
    print("Usage: {} <model-file>".format(sys.argv[0]))
    print("Put the .pmdl file as second argument")
    sys.exit(1)

print('Hello, my name is DORIS.')

detector = HotwordDetector(DECODER_MODEL, sensitivity=SENSITIVITY,
                        audio_gain=AUDIO_GAIN)
detector.start(callback_fn, audio_recorder_callback=record_callback,
                        recording_timeout=30.)

