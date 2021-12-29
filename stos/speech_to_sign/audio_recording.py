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
        self.__audio_queue = []
        thread.start()

    def run(self):
        """Record an audio file
        Returns:
            Writes .wav record files
        """

        while self.__loop:
            self.__count = self.__count + 1
            rate = 44100
            duration = 6
            # CHUNK = 1024
            # WAVE_OUTPUT_FILENAME = 'output' + str(self.__count) + '.wav'
            recording = sd.rec(int(duration * rate), samplerate=rate, channels=2)
            sd.wait()
            self.__audio_queue.append(recording)
            time.sleep(self.interval)

    def stop(self):
        self.__loop = False

    def get_current_audio(self):
        # print(self.__audio_queue)
        if len(self.__audio_queue) > 0:
            ca = self.__audio_queue[0]
            del self.__audio_queue[0]
            return ca
        return None
