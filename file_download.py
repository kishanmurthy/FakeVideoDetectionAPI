from pytube import YouTube
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import asyncio

async def downloadYoutubeVideos(video_id):
    base_url = "https://www.youtube.com/watch?"
    yt = YouTube(base_url + "v=" + video_id)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').asc().first()
    if not os.path.exists("videos/"):
        os.makedirs("videos/")
    yt.download("videos/")


async def downloadYoutubeShorts(video_id):
    base_url = "https://www.youtube.com/shorts/"
    yt = YouTube(base_url + video_id)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').asc().first()
    if not os.path.exists("shorts/"):
        os.makedirs("shorts/")
    yt.download("shorts/")

downloadYoutubeVideos("_fbq8RaKlxI")
downloadYoutubeShorts("Jr5-KtUAFzE")
