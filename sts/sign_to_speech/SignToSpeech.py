import os
from sts.sign_to_speech import model_prepare
from sts.sign_to_speech.model import Model


class SignToSpeech:

    def __init__(self, source, sequence_length, model_path, names_path, display_keypoint=False, display_window=True):
        model_exist = os.path.exists(os.path.join('model', 'cv_model.h5'))
        if not model_exist:
            print('Downloading the model.')
            model_url = 'https://drive.google.com/u/0/uc?id=1cd3aCeG618_O8N4MvAFJfHXrXiX-Udny&export=download'
            model_prepare.download_file(model_url, model_path)
            print('Downloading names file.')
            names_url = 'https://drive.google.com/u/0/uc?id=1vDyKqqZpQ3_zzK0T26leeZFnSSqUl-Y5&export=download'
            model_prepare.download_file(names_url, names_path)
        self.__model = Model(source, sequence_length, model_path, names_path, display_keypoint, display_window)
        self.__sentence_queue = []

    def start_pipeline(self):
        words = []
        for word, frame in self.__model.start_stream():
            if word != "":
                if word == 'na':
                    self.__sentence_queue.append(' '.join(words))
                    words = []
                else:
                    words.append(word)



