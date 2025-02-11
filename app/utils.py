from yt_dlp import YoutubeDL

def download_yt_audio(url, output_path="./files", format = 'mp3'):
    ydl_opts = {
        'format': 'bestaudio/best', 
        'outtmpl': f'{output_path}/%(title)s.%(ext)s', 
        'postprocessors': [{ 
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,
            'preferredquality': '192',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])