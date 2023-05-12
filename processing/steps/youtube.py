from yt_dlp import YoutubeDL

from processing.step import AbstractStep


class YouTubeStep(AbstractStep):
    def __init__(self, ydl_opts, video_file, video_link):
        self._ydl_opts = ydl_opts
        self._video_file = video_file
        self._video_link = video_link

    def process(self):
        with YoutubeDL(self._ydl_opts) as ydl:
            ydl.download(self._video_link)
