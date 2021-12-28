import wavio as wv
import sounddevice as sd
import threading
import time


class RecordingThread(object):
    def __init__(self, interval=0):
        self.interval = interval
        self.__count = 0
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        self.__loop = True
        thread.start()

    def run(self):
        """Record an audio file
        Returns:
            Writes .wav record files
        """

        while self.__loop:
            self.__count = self.__count + 1
            RATE = 44100
            RECORD_DURATION = 6
            # CHUNK = 1024
            WAVE_OUTPUT_FILENAME = 'output' + str(self.__count) + '.wav'
            recording = sd.rec(int(RECORD_DURATION * RATE),samplerate=RATE, channels=2)
            sd.wait()
            wv.write(WAVE_OUTPUT_FILENAME, recording, RATE, sampwidth=2)
            time.sleep(self.interval)

    def stop(self):
        self.__loop = False
