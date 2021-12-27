from happytransformer import HappyTextToText
from happytransformer import TTSettings


happy_tt = HappyTextToText("T5",  "vennify/t5-base-grammar-correction")
settings = TTSettings(do_sample=True, top_k=10, temperature=0.5,  min_length=1, max_length=100)


def parsing(text):
    tmp_text = "gec: " + text
    result = happy_tt.generate_text(tmp_text, args=settings)
    return result.text
