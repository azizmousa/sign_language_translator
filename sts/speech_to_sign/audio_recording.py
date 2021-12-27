import pyaudio
import wave
import time
import threading


class RecordingThread(object):
    def __init__(self, interval=0):
        self.interval = interval
        self.__count = 0
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        """Recording audio files

        Output:
            Writes .wav record files into the system
        """

        while True:
            self.__count = self.__count + 1
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 2
            RATE = 44100
            RECORD_SECONDS = 9
            WAVE_OUTPUT_FILENAME = 'output' + str(self.__count) + '.wav'

            p = pyaudio.PyAudio()

            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

            frames = []

            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            stream.stop_stream()
            stream.close()
            p.terminate()

            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            time.sleep(self.interval)

