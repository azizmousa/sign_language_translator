import os
import threading
from stos.sign_to_speech import model_prepare
from stos.sign_to_speech.model import Model
from stos.sign_to_speech.speak import Speak
from stos.sign_to_speech.parser import Parser


class SignToSpeech:
    """
    SignToSpeech class that build the pipeline of converting the sings to speech

    Attributes:
        __model (Model): model object that control the sign prediction

        __sentence_queue (list): list of detected sentences as a queue

        __listener_thread (Thread): sentence listener thread

        __speak (Speak): speak object to speak the sentences

        __parser (Parser): parser object to construct the right sentence

        __display_window (bool, optional):
            True if you want the class to display the output window
            False otherwise

    """

    def __init__(self, source, sequence_length, model_path, names_path, display_keypoint=False, display_window=True):
        model_exist = os.path.exists(model_path)
        if not model_exist:
            print('Downloading the __model.')
            model_url = 'https://drive.google.com/u/0/uc?id=1LkQWfCo4T9uAZAykKvkVs8bKub6b96LC&export=download'
            model_prepare.download_file(model_url, model_path)
            print('Downloading names file.')
            names_url = 'https://drive.google.com/u/0/uc?id=1VmT3F9X9E_kavPKheSk4q5QZjyS9bgNn&export=download'
            model_prepare.download_file(names_url, names_path)
        self.__model = Model(source, sequence_length, model_path, names_path, display_keypoint, display_window)
        self.__sentence_queue = []
        self.__listener_thread = threading.Thread(target=self.sentence_listener)
        self.__speak = Speak()
        self.__parser = Parser()
        self.__display_window = display_window

    def sentence_listener(self):
        """
        function to listen to the __sentence_queue attribute if there is a sentence it will process it.

        Returns:
            None

        """
        while len(self.__sentence_queue) > 0:
            sentence = self.__parser.parse(self.__sentence_queue[0])
            print('sentence:', self.__sentence_queue[0])
            print('parsed:', sentence)
            self.__speak.speak(sentence)
            del self.__sentence_queue[0]

    def start_pipeline(self):
        """
        this function start the whole pipeline to convert the sign language to spoken language.

        Returns:
                word (string): the predicted word.
                frame (2d-np_array): the frame that return from the stream.

        """
        words = []
        for word, frame in self.__model.start_stream():
            # print(word)
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
            yield word, frame
