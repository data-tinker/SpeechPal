from yt_dlp import YoutubeDL

from steps.step import AbstractStep


class YouTubeStep(AbstractStep):
    def __init__(self, audio_file, video_link):
        self._audio_file = audio_file
        self._video_link = video_link

    def process(self):
        ydl_opts = {
            'outtmpl': self._audio_file.full_path(),
            'format': 'bestaudio[ext=m4a]',
            'audioformat': 'm4a',
            'extract_audio': True,
            'nooverwrites': True
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(self._video_link)
