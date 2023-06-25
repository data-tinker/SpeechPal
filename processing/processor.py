from __future__ import unicode_literals

import os
import pathlib

from persistence.reports_repository import ReportsRepository
from processing.pipeline_builder import PipelineBuilder
from steps.check_grammar import CheckGrammarStep
from steps.cleanup import CleanUpStep
from steps.process_report import ProcessReportStep
from steps.telegram_audio_step import TelegramAudioStep
from steps.transcribe_audio_cloud import TranscribeAudioCloudStep
from steps.youtube import YouTubeStep
from util.file import File
from util.youtube import get_youtube_video_id

mongo_db_connection = os.getenv('MONGO_DB_CONNECTION')
REPORT_URL_TEMPLATE = "https://speechpal.co/reports/{}"


class Processor:
    reports_repository = ReportsRepository(mongo_db_connection)

    @classmethod
    def process_youtube_video(cls, youtube_link):
        youtube_video_id = get_youtube_video_id(youtube_link)
        report_file = File('tmp', youtube_video_id, f'report_{youtube_video_id}', 'txt')

        report = cls.reports_repository.get_by_id(youtube_video_id)

        if report is not None:
            return report

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
            .add_step(CheckGrammarStep(text_file, report_file)) \
            .add_step(ProcessReportStep(youtube_video_id, report_file, cls.reports_repository)) \
            .add_step(CleanUpStep([audio_file, audio_chunk_file, text_file])) \
            .build()

        pipeline.run()

        return REPORT_URL_TEMPLATE.format(youtube_video_id)

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

        report = cls.reports_repository.get_by_id(file_id)

        if report is not None:
            return report

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
            .add_step(CheckGrammarStep(text_file, report_file)) \
            .add_step(ProcessReportStep(file_id, report_file, cls.reports_repository)) \
            .add_step(CleanUpStep([telegram_audio_file, audio_file, audio_chunk_file, text_file, report_file])) \
            .build()

        pipeline.run()

        return REPORT_URL_TEMPLATE.format(file_id)
