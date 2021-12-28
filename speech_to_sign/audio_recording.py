import wavio as wv
import sounddevice as sd
from scipy.io.wavfile import write
import threading
import speech_to_text
import speech_recognition as sr
import wave
import nltk
import glob
import time
import os 
import speech_recognition as sr
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
global queue
queue = []

class RecordingThread(object):
    def __init__(self, interval=0):
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()
		

			

    def run(self):
        """Record an audio file

        Returns:
            Writes .wav record files
        """

        while True:
            RATE = 44100
            RECORD_DURATION = 3
            CHUNK = 1024
            WAVE_OUTPUT_FILENAME = 'output.wav'
            
			
			recording = sd.rec(int(RECORD_DURATION * RATE),samplerate=RATE, channels=2)
            sd.wait()
            queue.append(recording)
            wv.write(WAVE_OUTPUT_FILENAME,queue[0], RATE, sampwidth=2)
            time.sleep(self.interval)
            queue.pop(0)
