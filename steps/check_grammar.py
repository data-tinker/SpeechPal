import openai

from steps.step import AbstractStep

import re


class CheckGrammarStep(AbstractStep):
    def __init__(self, grammar_model, text_file, report_file):
        self._model = grammar_model
        self._text_file = text_file
        self._report_file = report_file

    def process(self):
        with open(self._text_file.full_path(), 'r') as f:
            text = f.read()

        sentences = re.split(r'(?<=[.!?])\s+', text)[:-1]

        with open(self._report_file.full_path(), 'w') as f:
            for sentence in sentences:
                corrected_sentences = self._model.correct(sentence, max_candidates=1)

                if len(corrected_sentences) == 1 and corrected_sentences.pop() == sentence:
                    continue

                for corrected_sentence in corrected_sentences:
                    print("[Edits] ", self._model.get_edits(sentence, corrected_sentence))

                edits = openai.Completion.create(
                    model='text-davinci-003',
                    prompt=f'Check the sentence and correct mistakes. Give the explanation. "{sentence}". If no '
                           f'correction is needed, return "Correct."',
                    max_tokens=512
                )['choices'][0]['text'].strip()

                if 'Correct.' in edits:
                    continue

                inputs = f'[Input]\n{sentence}'
                edits = f'[Correction]\n{edits}'

                print(inputs)
                print(edits)
                print()

                f.write(inputs + '\n')
                f.write(edits + '\n')
                f.write('\n')
