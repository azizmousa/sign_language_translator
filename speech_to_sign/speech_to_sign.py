import glob
import os
from sts.speech_to_sign.audio_recording import RecordingThread
from sts.speech_to_sign.speech_to_text import SpeechToText


class SpeechToSign:
    def __init__(self):
        # to start recording
        self.__rth = RecordingThread()
        self.__stt = SpeechToText()

    def start_pipeline(self):
        while True:
            try:
                file_name = 'output.wav'
                if len(queue)!= 0:
                    time.sleep(1.95)
                    # Converting a single recorded audio file into text
                    text = self.__stt.convert_recorded_audio(file_name[0])
                    lemmatized_text = self.__stt.lemmatize(text)
                    print(lemmatized_text)
                    os.remove(file_name[0])

                else:
                    continue
            except ValueError:
                continue
            except TypeError:
                continue
            except FileNotFoundError:
                file_name = wave.open('output.wav', 'w') 
            except RequestError:
                print('check internet connection...')

