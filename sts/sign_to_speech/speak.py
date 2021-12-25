import os
import gtts
from playsound import playsound


class Speak:

    def __init__(self, language='en', accent='com', slow=False):
        self.__language = language
        self.__accent = accent
        self.__slow = slow

    def speak(self, text):
        if text != "":
            output = gtts.gTTS(text=text, lang=self.__language, slow=self.__slow, tld=self.__accent)
            output.save("speak.mp3")
            playsound("speak.mp3")
            os.remove("speak.mp3")
