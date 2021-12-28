import speech_recognition as sr
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


class SpeechToText:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        self.__lemmatizer = WordNetLemmatizer()
        self.__r = sr.Recognizer()
        self.__stop_words = ["a", "an", "the", "is", "am",
                             "are", "was", "were", "been",
                             "has", "have", "too", "had",
                             "do", "be", "does", "did", "as",
                             "for", "nor", "by", "further",
                             "into", "these"]

    def lemmatize(self, text):
        """Get the lemmatized version of an input text

        Args:
            text (str): The extracted text from the recorded audio

        Returns:
            list: a list of strings represents the text after lemmatization
        """

        try:
            text_said = text['alternative'][0]['transcript']
            text_tokenized = word_tokenize(text_said)
            no_stop_words = [word for word in text_tokenized if word not in self.__stop_words]
            text_lemmatized = [self.__lemmatizer.lemmatize(token) for token in no_stop_words]

            return text_lemmatized

        except TypeError:
            return ""

    def convert_recorded_audio(self, file_name):
        """Converting an audio file into text

        Args:
            file_name (str): The name of the audio file, which will be converted into text

        Returns:
            text (str): The extracted text from the audio file
        """

        with sr.AudioFile(file_name) as source:
            # listen to data (load audio to memory)
            audio_data = self.__r.record(source)
            # recognize (convert from speech to text)
            text = self.__r.recognize_google(audio_data, language='en-IN', show_all=True)

        return text

