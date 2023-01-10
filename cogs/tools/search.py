import pytube
from requests import get


class Youtube:
    def __init__(self, video: str) -> None:
        try:
            get(video)
        except:
            self.video = pytube.YouTube(pytube.Search(video).results[0].watch_url)
        else:
            self.video = pytube.YouTube(video)

    def get_audio(self):
        return self.video.streams.get_by_itag(251).url

    def get_info(self):
        info = dict({
                "Thumbnail": self.video.thumbnail_url,
                "Titulo": self.video.title,
                "Canal": self.video.author,
                "Views": self.video.views,
                "Time": self.video.length
                })

        return info
