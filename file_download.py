from pytube import YouTube
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import asyncio
from database_access import update_request_status

async def downloadYoutubeVideos(request_id, video_id):
    update_request_status(request_id, "DOWNLOADING VIDEO")
    base_url = "https://www.youtube.com/watch?"
    yt = YouTube(base_url + "v=" + video_id)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').asc().first()
    if not os.path.exists("videos/"):
        os.makedirs("videos/")
    yt.download("videos/")
    update_request_status(request_id, "DOWNLOADED VIDEO")


async def downloadYoutubeShorts(request_id, video_id):
    update_request_status(request_id, "DOWNLOADING SHORTS")
    base_url = "https://www.youtube.com/shorts/"
    yt = YouTube(base_url + video_id)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').asc().first()
    if not os.path.exists("shorts/"):
        os.makedirs("shorts/")
    yt.download("shorts/")
    update_request_status(request_id, "DOWNLOADED SHORTS")

# downloadYoutubeVideos("_fbq8RaKlxI")
# downloadYoutubeShorts("Jr5-KtUAFzE")
