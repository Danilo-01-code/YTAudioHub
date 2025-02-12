import yt_dlp
from .models import Audios
import os

def get_data_url(url, output_path, format):
    """
    Parameters:
    - url: The Youtube url for get resources
    - output_path: the diretory where the file would be save
    - format: the file format (mp3 or wav)

    Returns:
    - author: channel name
    - title: video name
    - thumbnail: the thumbnail url
    """
    not_allowed_chars = ['\\', '|', '/', '｜','[',']','.','"']
    
    with yt_dlp.YoutubeDL({'format': 'bestaudio/best'}) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title')

    for char in not_allowed_chars:
        title = title.replace(char, '_')

    audio = Audios.get_or_none(Audios.title == title)

    if audio:
        return audio.author,audio.title,audio.thumb # Avoid unnecessary downloads

    author = info.get('uploader')
    thumbnail = info.get('thumbnail')
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, f"{title}.%(ext)s"),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,
            'preferredquality': '192',
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return author, title, thumbnail