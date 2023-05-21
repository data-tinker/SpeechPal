import os

import ffmpeg

from steps.step import AbstractStep


class TelegramAudioStep(AbstractStep):
    def __init__(self, audio_file, telegram_audio_file, downloaded_file):
        self._audio_file = audio_file
        self._telegram_audio_file = telegram_audio_file
        self._downloaded_file = downloaded_file

    def process(self):
        os.mkdir(os.path.dirname(self._telegram_audio_file.full_path()))
        with open(self._telegram_audio_file.full_path(), 'wb') as f:
            f.write(self._downloaded_file)

        input_stream = ffmpeg.input(self._telegram_audio_file.full_path())
        output_stream = ffmpeg.output(input_stream, self._audio_file.full_path())

        ffmpeg.run(output_stream)
