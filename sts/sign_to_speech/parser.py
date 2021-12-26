from happytransformer import HappyTextToText
from happytransformer import TTSettings


class Parser:

    def __init__(self):
        self.__happy_tt = HappyTextToText("T5",  "prithivida/grammar_error_correcter_v1")
        self.__settings = TTSettings(do_sample=True, top_k=10, temperature=0.5, min_length=1, max_length=100)

    def parse(self, text):
        tmp_text = "gec: " + text
        result = self.__happy_tt.generate_text(tmp_text, args=self.__settings)
        return result.text
