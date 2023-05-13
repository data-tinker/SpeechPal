from __future__ import unicode_literals

import os

from gramformer import Gramformer

from processing.steps.cleanup import CleanUpStep
from util.file import File
from processing.pipeline_builder import PipelineBuilder
from processing.steps.check_grammar import CheckGrammarStep
from processing.steps.extract_audio import ExtractAudioStep
from processing.steps.transcribe_audio_cloud import TranscribeAudioCloudStep
from processing.steps.youtube import YouTubeStep


class Processor:
    grammar_model = Gramformer(models=1, use_gpu=False)

    @classmethod
    def process_youtube_video(cls, youtube_link, youtube_video_id):
        report_file = File('tmp', youtube_video_id, f'report_{youtube_video_id}', 'txt')

        if os.path.exists(report_file.full_path()):
            return report_file

        video_file = File('tmp', youtube_video_id, 'video', 'webm')
        audio_file = File('tmp', youtube_video_id, 'audio', 'wav')
        audio_chunk_file = File('tmp', youtube_video_id, 'audio_chunk', 'wav')
        text_file = File('tmp', youtube_video_id, 'text', 'txt')

        pipeline = PipelineBuilder(youtube_video_id) \
            .add_step(YouTubeStep(video_file, youtube_link)) \
            .add_step(ExtractAudioStep(video_file, audio_file)) \
            .add_step(TranscribeAudioCloudStep(
                audio_file,
                audio_chunk_file,
                text_file
            )) \
            .add_step(CheckGrammarStep(cls.grammar_model, text_file, report_file)) \
            .add_step(CleanUpStep(
                video_file,
                audio_file,
                audio_chunk_file,
                text_file
            )) \
            .build()

        pipeline.run()

        return report_file
