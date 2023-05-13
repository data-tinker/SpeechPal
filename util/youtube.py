import re

youtube_id_regex = re.compile('((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)')


def get_youtube_video_id(youtube_video):
    return youtube_id_regex.search(youtube_video).group(0)
