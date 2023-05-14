from __future__ import unicode_literals

import os

from gramformer import Gramformer

from util.file import File
from processing.pipeline_builder import PipelineBuilder
from steps.check_grammar import CheckGrammarStep
from steps.cleanup import CleanUpStep
from steps.transcribe_audio_cloud import TranscribeAudioCloudStep
from steps.youtube import YouTubeStep


class Processor:
    grammar_model = Gramformer(models=1, use_gpu=False)

    @classmethod
    def process_youtube_video(cls, youtube_link, youtube_video_id):
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
