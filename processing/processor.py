from __future__ import unicode_literals

from gramformer import Gramformer
import whisper

from file import File
from processing.pipeline_builder import PipelineBuilder
from processing.steps.check_grammar import CheckGrammarStep
from processing.steps.extract_audio import ExtractAudioStep
from processing.steps.transcribe_audio import TranscribeAudioStep
from processing.steps.youtube import YouTubeStep

VIDEO_FILE = File('tmp', 'video', 'webm')
AUDIO_FILE = File('tmp', 'audio', 'wav')
TEXT_FILE = File('tmp', 'text', 'txt')


class Processor:
    ydl_opts = {
        'outtmpl': f'{VIDEO_FILE.path}/{VIDEO_FILE.name}'
    }
    ffmpeg_opt = {
        'format': 'wav',
        'ab': '160k',
        'ar': '44100',
        'vn': True
    }
    transcribe_model = whisper.load_model("base")
    grammar_model = Gramformer(models=1, use_gpu=False)
    random_step = ExtractAudioStep({}, VIDEO_FILE, AUDIO_FILE)

    @classmethod
    def process_youtube_link(cls, youtube_link):
        pipeline = PipelineBuilder() \
            .add_step(YouTubeStep(cls.ydl_opts, VIDEO_FILE, youtube_link)) \
            .add_step(ExtractAudioStep(cls.ffmpeg_opt, VIDEO_FILE, AUDIO_FILE)) \
            .add_step(TranscribeAudioStep(cls.transcribe_model, AUDIO_FILE, TEXT_FILE)) \
            .add_step(CheckGrammarStep(cls.grammar_model, TEXT_FILE)) \
            .build()

        pipeline.run()
