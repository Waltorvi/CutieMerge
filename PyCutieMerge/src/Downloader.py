import requests
import logging
import os

DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
TEMP_DIR = os.path.join(DOWNLOADS_DIR, ".temp")

BASE_URL = "https://база.магиядружбы.рф/"

def DownloadFile(url, filename):
    """
    Скачивает файл по заданному URL и сохраняет его с указанным именем.

    Args:
        url (str): URL файла для скачивания.
        filename (str): Имя файла для сохранения.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        logging.info(f"Файл '{filename}' успешно скачан.")
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при скачивании файла '{filename}': {e}")
        return False

def download_video(season, episode, quality):
    if int(quality) <= 1080:
        ext = "mp4"
    else:
        ext = "webm"
    url = f"{BASE_URL}video/G4/FiM/media/s{season}/e{episode}/{quality}.{ext}"
    filename = os.path.join(TEMP_DIR, f"video.{ext}")
    return DownloadFile(url, filename)

def download_audio(season, episode, dub_code):
    url = f"{BASE_URL}video/G4/FiM/media/s{season}/e{episode}/{dub_code}.opus"
    filename = os.path.join(TEMP_DIR, "audio.opus")
    return DownloadFile(url, filename)

def download_subs(season, episode, subs_code):
    url = f"{BASE_URL}video/G4/FiM/media/s{season}/e{episode}/{subs_code}.ass"
    filename = os.path.join(TEMP_DIR, "subs.ass")
    return DownloadFile(url, filename)