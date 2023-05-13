import os

from processing.step import AbstractStep


class CleanUpStep(AbstractStep):
    def __init__(
        self,
        video_file,
        audio_file,
        audio_chunk_file,
        text_file
    ):
        self._video_file = video_file
        self._audio_file = audio_file
        self._audio_chunk_file = audio_chunk_file
        self._text_file = text_file

    def process(self):
        for file in (self._video_file, self._audio_file, self._audio_chunk_file, self._text_file):
            if os.path.exists(file.full_path()):
                os.remove(file.full_path())
