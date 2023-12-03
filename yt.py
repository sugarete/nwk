from pytube import YouTube
import os
from urllib.parse import unquote

FORMAT = "utf8"

download_directory = 'downloaded_videos'
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

def youtubeProcessing(request):
    url = request.split("url=")[1].split(" ")[0]
    url = unquote(url)
    print("Downloading video at: ", url)
    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    video_path = video.download(download_directory)
    print("Downloaded video at: ", video_path)
    return video_path

def createVideoResponse(video_path):
    with open (video_path, "rb") as f:
        video_content = f.read()
    response = (
        "HTTP/1.1 200 OK\r\n"
        f"Content-Disposition: attachment; filename={os.path.basename(video_path)}\r\n"
        f"Content-Type: video/mp4\r\n"
        f"Content-Length: {len(video_content)}\r\n\r\n"
    ).encode(FORMAT) + video_content
    return response

def handle_video_request(request):
    video_file = unquote(request.split()[1][1:].split("/")[1])
    video_path = os.path.abspath(os.path.join('downloaded_videos', video_file))
    print("Sending video: ", video_path)
    return video_path

def list_videos():
    video_files = os.listdir("downloaded_videos")
    video_list = "<ul>"
    for video_file in video_files:
        video_list += f'<li><a href="/videos/{video_file}">{video_file}</a></li>'
    video_list += "</ul>"
    return video_list
