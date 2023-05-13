from yt_dlp import YoutubeDL

from processing.step import AbstractStep


class YouTubeStep(AbstractStep):
    def __init__(self, video_file, video_link):
        self._video_file = video_file
        self._video_link = video_link

    def process(self):
        ydl_opts = {
            'outtmpl': self._video_file.path_without_extension(),
            'format': 'bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]'
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(self._video_link)
