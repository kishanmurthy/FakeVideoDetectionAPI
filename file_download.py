from pytube import YouTube
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def downloadYoutube(video_id):
    base_url = "https://www.youtube.com/watch?"
    yt = YouTube(base_url + "v=" + video_id)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').asc().first()
    if not os.path.exists("downloads/"):
        os.makedirs("downloads/")
    yt.download("downloads/")


downloadYoutube("_fbq8RaKlxI")