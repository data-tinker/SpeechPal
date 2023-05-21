from __future__ import unicode_literals

import os
import pathlib

from gramformer import Gramformer

from steps.telegram_audio_step import TelegramAudioStep
from util.file import File
from processing.pipeline_builder import PipelineBuilder
from steps.check_grammar import CheckGrammarStep
from steps.cleanup import CleanUpStep
from steps.transcribe_audio_cloud import TranscribeAudioCloudStep
from steps.youtube import YouTubeStep
from util.youtube import get_youtube_video_id


class Processor:
    grammar_model = Gramformer(models=1, use_gpu=False)

    @classmethod
    def process_youtube_video(cls, youtube_link):
        youtube_video_id = get_youtube_video_id(youtube_link)
        report_file = File('tmp', youtube_video_id, f'report_{youtube_video_id}', 'txt')

        if os.path.exists(report_file.full_path()):
            return report_file

        audio_file = File('tmp', youtube_video_id, 'audio', 'm4a')
        audio_chunk_file = File('tmp', youtube_video_id, 'audio_chunk', 'm4a')
        text_file = File('tmp', youtube_video_id, 'text', 'txt')

        pipeline = PipelineBuilder(youtube_video_id) \
            .add_step(YouTubeStep(audio_file, youtube_link)) \
            .add_step(TranscribeAudioCloudStep(
                audio_file,
                audio_chunk_file,
                text_file
            )) \
            .add_step(CheckGrammarStep(cls.grammar_model, text_file, report_file)) \
            .add_step(CleanUpStep([audio_file, audio_chunk_file, text_file])) \
            .build()

        pipeline.run()

        return report_file

    @classmethod
    def process_telegram_voice(cls, downloaded_file, file_id):
        telegram_audio_file = File('tmp', file_id, 'telegram_audio', 'oga')
        return cls._process_audio(file_id, downloaded_file, telegram_audio_file)

    @classmethod
    def process_telegram_audio(cls, downloaded_file, file_id, file_path):
        telegram_file_extension = pathlib.Path(file_path).suffix[1:]

        telegram_audio_file = File('tmp', file_id, 'telegram_audio', telegram_file_extension)
        return cls._process_audio(file_id, downloaded_file, telegram_audio_file)

    @classmethod
    def _process_audio(cls, file_id, downloaded_file, telegram_audio_file):
        report_file = File('tmp', file_id, f'report_{file_id}', 'txt')

        if os.path.exists(report_file.full_path()):
            return report_file

        audio_file = File('tmp', file_id, 'audio', 'm4a')
        audio_chunk_file = File('tmp', file_id, 'audio_chunk', 'm4a')
        text_file = File('tmp', file_id, 'text', 'txt')

        pipeline = PipelineBuilder(file_id) \
            .add_step(TelegramAudioStep(audio_file, telegram_audio_file, downloaded_file)) \
            .add_step(TranscribeAudioCloudStep(
                audio_file,
                audio_chunk_file,
                text_file
            )) \
            .add_step(CheckGrammarStep(cls.grammar_model, text_file, report_file)) \
            .add_step(CleanUpStep([telegram_audio_file, audio_file, audio_chunk_file, text_file])) \
            .build()

        pipeline.run()

        return report_file
