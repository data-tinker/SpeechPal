from processing.step import AbstractStep

import re


class CheckGrammarStep(AbstractStep):
    def __init__(self, model, text_file):
        self._model = model
        self._text_file = text_file

    def process(self):
        with open(self._text_file.full_path(), 'r') as f:
            text = f.read()

        sentences = re.split(r'(?<=[.!?])\s+', text)[:-1]

        for sentence in sentences:
            corrected_sentences = self._model.correct(sentence, max_candidates=1)
            print("[Input] ", sentence)
            for corrected_sentence in corrected_sentences:
                print("[Edits] ", self._model.highlight(sentence, corrected_sentence))
            print("-" * 100)
