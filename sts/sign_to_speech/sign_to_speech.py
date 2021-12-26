import os
import threading
from sts.sign_to_speech import model_prepare
from sts.sign_to_speech.model import Model
from sts.sign_to_speech.speak import Speak
from sts.sign_to_speech.parser import Parser


class SignToSpeech:

    def __init__(self, source, sequence_length, model_path, names_path, display_keypoint=False, display_window=True):
        model_exist = os.path.exists(os.path.join('model', 'cv_model.h5'))
        if not model_exist:
            print('Downloading the model.')
            model_url = 'https://drive.google.com/u/0/uc?id=1cd3aCeG618_O8N4MvAFJfHXrXiX-Udny&export=download'
            model_prepare.download_file(model_url, model_path)
            print('Downloading names file.')
            names_url = 'https://drive.google.com/u/0/uc?id=1OKafl9zFwYPCJfUr_W0wESbkvrZCgFRY&export=download'
            model_prepare.download_file(names_url, names_path)
        self.__model = Model(source, sequence_length, model_path, names_path, display_keypoint, display_window)
        self.__sentence_queue = []
        self.__listen = True
        self.__listener_thread = threading.Thread(target=self.sentence_listener)
        self.__speak = Speak()
        self.__parser = Parser()

    def sentence_listener(self):
        while len(self.__sentence_queue) > 0:
            sentence = self.__parser.parse(self.__sentence_queue[0])
            # sentence = self.__sentence_queue[0]
            print('sentence:', self.__sentence_queue[0])
            print('parsed:', sentence)
            self.__speak.speak(sentence)
            del self.__sentence_queue[0]

    def start_pipeline(self):
        words = []

        for word, frame in self.__model.start_stream():
            if word != "":
                if word == 'na':
                    self.__sentence_queue.append(' '.join(words))
                    words = []
                    if not self.__listener_thread.is_alive():
                        del self.__listener_thread
                        self.__listener_thread = threading.Thread(target=self.sentence_listener)
                        self.__listener_thread.start()
                else:
                    words.append(word)
        self.__listen = False


