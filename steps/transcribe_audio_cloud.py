import openai
from pydub import AudioSegment
from pydub.silence import split_on_silence

from steps.step import AbstractStep


class TranscribeAudioCloudStep(AbstractStep):
    def __init__(
            self,
            audio_file,
            audio_chunk_file,
            text_file
    ):
        self._audio_file = audio_file
        self._audio_chunk_file = audio_chunk_file
        self._text_file = text_file

    def process(self):
        audio_file = AudioSegment.from_file(self._audio_file.full_path(), format='m4a')

        transcript = ''
        if self._audio_file.size_in_bytes() / (1024 * 1024) < 24:
            with open(self._audio_file.full_path(), "rb") as f:
                chunk_transcript = openai.Audio.transcribe("whisper-1", f, language='en')
                transcript += chunk_transcript['text']
        else:
            audio_chunks = split_on_silence(
                audio_file,
                min_silence_len=200,
                silence_thresh=-40,
                seek_step=100
            )

            for i, chunk in enumerate(audio_chunks):
                chunk.export(self._audio_chunk_file.full_path(), format="mp4")

                with open(self._audio_chunk_file.full_path(), "rb") as f:
                    chunk_transcript = openai.Audio.transcribe("whisper-1", f, language='en')
                    transcript += chunk_transcript['text']

        with open(self._text_file.full_path(), 'w') as f:
            f.write(transcript)
