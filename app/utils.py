import yt_dlp

def download_yt_audio(url, output_path, format):
    ydl_opts = {
        'format': 'bestaudio/best', 
        'outtmpl': f'{output_path}/%(title)s.%(ext)s', 
        'postprocessors': [{ 
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
def get_video_info(video_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        return info.get("uploader"), info.get("title")