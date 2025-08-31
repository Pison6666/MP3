import os
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from yt_dlp import YoutubeDL

# --- การตั้งค่า (สำคัญมาก) ---
# แนะนำให้ตั้งค่าเป็น Environment Variables เพื่อความปลอดภัย
# แต่เพื่อความง่าย จะใส่ไว้ในโค้ดก่อน
# ใส่ Client ID และ Client Secret ที่ได้จาก Spotify Developer Dashboard
SPOTIPY_CLIENT_ID = '63a453141048451d96ea1444910b0bae'
SPOTIPY_CLIENT_SECRET = 'ab4bb120be7d4c4eb3c1d4bd2b9b3b19'

# โฟลเดอร์ที่จะบันทึกไฟล์ MP3
DOWNLOAD_FOLDER = 'downloads'

# --- เริ่มโค้ด ---

# ตั้งค่าการเชื่อมต่อกับ Spotify API
try:
    auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except Exception as e:
    print(f"Error setting up Spotify API: {e}")
    sp = None

def get_spotify_track_info(track_url):
    """ดึงข้อมูลชื่อเพลงและศิลปินจากลิงก์ Spotify"""
    if not sp:
        print("Spotify API not configured.")
        return None

    try:
        track = sp.track(track_url)
        song_title = track['name']
        artists = [artist['name'] for artist in track['artists']]
        artist_str = ", ".join(artists)
        return f"{song_title} {artist_str}"
    except Exception as e:
        print(f"Could not get track info from Spotify: {e}")
        return None

def download_audio_from_youtube(search_query):
    """ค้นหาและดาวน์โหลดเสียงจาก YouTube เป็น MP3"""
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'default_search': 'ytsearch1', # ค้นหาและเลือกวิดีโอแรก
        'noplaylist': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=True)
            # แก้ชื่อไฟล์ให้ถูกต้องหลังดาวน์โหลดเสร็จ
            downloaded_file = ydl.prepare_filename(info)
            base, ext = os.path.splitext(downloaded_file)
            final_path = base + '.mp3'
            print(f"Downloaded and converted to: {final_path}")
            return final_path
    except Exception as e:
        print(f"Error during download: {e}")
        return None


def start_download(url):
    """
    ตรวจจับลิงก์และเริ่มกระบวนการดาวน์โหลด
    """
    if "spotify.com" in url:
        print("Spotify link detected...")
        search_query = get_spotify_track_info(url)
        if search_query:
            print(f"Searching for '{search_query}' on YouTube...")
            return download_audio_from_youtube(search_query)
        else:
            return None
    elif "youtube.com" in url or "youtu.be" in url:
        print("YouTube link detected...")
        return download_audio_from_youtube(url)
    else:
        print("Invalid URL. Please provide a YouTube or Spotify link.")
        return None

# ตัวอย่างการใช้งาน (หากรันไฟล์นี้โดยตรง)
if __name__ == '__main__':
    test_url = input("Enter a YouTube or Spotify URL to test: ")
    start_download(test_url)