import ffmpeg

from steps.step import AbstractStep


class ExtractAudioStep(AbstractStep):
    def __init__(self, video_file, audio_file):
        self._video_file = video_file
        self._audio_file = audio_file

    def process(self):
        input_stream = ffmpeg.input(self._video_file.full_path())
        output_stream = ffmpeg.output(input_stream, self._audio_file.full_path(), ac=1, y='-y')
        output_stream = output_stream.global_args('-vn')

        ffmpeg.run(output_stream)
