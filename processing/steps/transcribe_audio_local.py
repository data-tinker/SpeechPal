from processing.step import AbstractStep


class TranscribeAudioLocalStep(AbstractStep):
    def __init__(self, model, audio_file, text_file):
        self._model = model
        self._audio_file = audio_file
        self._text_file = text_file

    def process(self):
        transcribed_text = self._model.transcribe(
            self._audio_file.full_path(),
            fp16=False
        )

        with open(self._text_file.full_path(), 'w') as f:
            f.write(transcribed_text['text'])
