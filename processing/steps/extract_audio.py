import ffmpeg
from processing.step import AbstractStep


class ExtractAudioStep(AbstractStep):
    def __init__(self, ffmpeg_opt, video_file, audio_file):
        print("wtf")
        self._ffmpeg_opt = ffmpeg_opt
        self._video_file = video_file
        self._audio_file = audio_file

    def process(self):
        (
            ffmpeg
            .input(self._video_file.full_path())
            .output(
                self._audio_file.full_path(),
                **self._ffmpeg_opt
            )
            .overwrite_output()
            .run()
        )
