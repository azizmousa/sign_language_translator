import os
import gtts
from playsound import playsound


class Speak:
    """
    Speak class convert the input text to voice

    Attributes:
        __language (string, optional): The language (IETF language tag) to
            read the text in. Default is ``en``.

        __accent (string, optional): Top-level domain for the Google Translate host,
            i.e `https://translate.google.<tld>`. Different Google domains
            can produce different localized 'accents' for a given
            language. This is also useful when ``google.com`` might be blocked
            within a network but a local or different Google host
            (e.g. ``google.cn``) is not. Default is ``com``.

        __slow (bool, optional): Reads text more slowly. Defaults to ``False``.
    """
    def __init__(self, language='en', accent='com', slow=False):
        self.__language = language
        self.__accent = accent
        self.__slow = slow

    def speak(self, text):
        """
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
