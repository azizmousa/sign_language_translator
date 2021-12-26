import os
import gtts
from playsound import playsound


class Speak:
    """
    Speak class convert the input text to voice
    """
    def __init__(self, language='en', accent='com', slow=False):
        self.__language = language
        self.__accent = accent
        self.__slow = slow

    def speak(self, text):
        """
        def speak(self, text)

        function to convert the input text voice

        Args:
            text (str): string text input

        Returns: None

        """
        if text != "":
            output = gtts.gTTS(text=text, lang=self.__language, slow=self.__slow, tld=self.__accent)
            output.save("speak.mp3")
            playsound("speak.mp3")
            os.remove("speak.mp3")
