from natasha import (
    Segmenter,
    Doc
)

# Модуль обработки текста
class Processing:
    def __init__(self):
        self.__segmenter = Segmenter()

    def split_by_sentences(self, text):
        doc = Doc(text)
        doc.segment(self.__segmenter)

        result = [x.text for x in doc.sents]
        return result