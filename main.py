from __future__ import unicode_literals

from typing import NamedTuple
import re

from gramformer import Gramformer
from yt_dlp import YoutubeDL
import ffmpeg
import whisper
import torch


class File(NamedTuple):
    path: str
    name: str
    extension: str

    def full_path(self):
        return f'{self.path}/{self.name}.{self.extension}'


def set_seed(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


set_seed(1212)

VIDEO_FILE = File('tmp', 'video', 'webm')
AUDIO_FILE = File('tmp', 'audio', 'wav')
TEXT_FILE = File('tmp', 'text', 'txt')

if __name__ == '__main__':
    youtube_link = 'https://www.youtube.com/watch?v=pQnOBHNKlgs'  # input("Please enter the YouTube link:\n")

    ydl_opts = {
        'outtmpl': f'{VIDEO_FILE.path}/{VIDEO_FILE.name}'
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(youtube_link)

    (
        ffmpeg
        .input(VIDEO_FILE.full_path())
        .output(
            AUDIO_FILE.full_path(),
            format='wav',
            ab='160k',
            ar='44100',
            vn=True
        )
        .overwrite_output()
        .run()
    )
    model = whisper.load_model("base")
    transcribed_text = model.transcribe(AUDIO_FILE.full_path(), fp16=False)

    with open(TEXT_FILE.full_path(), 'w') as f:
        f.write(transcribed_text['text'])

    sentences = re.split(r'(?<=[.!?])\s+', transcribed_text['text'])[:-1]

    gf = Gramformer(models=1, use_gpu=False)

    for sentence in sentences:
        corrected_sentences = gf.correct(sentence, max_candidates=1)
        print("[Input] ", sentence)
        for corrected_sentence in corrected_sentences:
            print("[Edits] ", gf.highlight(sentence, corrected_sentence))
        print("-" * 100)
