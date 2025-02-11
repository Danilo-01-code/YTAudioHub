import yt_dlp
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
    - file_path: the path of the downloaded file
    """
    
    ydl_opts = {
        'format': 'bestaudio/best', 
        'outtmpl':os.path.join(output_path, "%(title)s.%(ext)s"),
        'postprocessors': [{ 
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,  
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True) 
        title = info_dict.get('title') 
        author = info_dict.get('uploader')
        thumbnail = info_dict.get('thumbnail')

        file_path = ydl.prepare_filename(info_dict)
        file_path = os.path.splitext(file_path)[0] + f".{format}"

    return author, title,thumbnail
