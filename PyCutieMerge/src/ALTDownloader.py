import requests
import logging
import os
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(SCRIPT_DIR, ".temp")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "CutieMerge")

BASE_URL = "https://база.магиядружбы.рф/"


def DownloadFileALT(url, filename):
    """
    Скачивает файл по заданному URL и сохраняет его с указанным именем.

    Args:
        url (str): URL файла для скачивания.
        filename (str): Имя файла для сохранения.
    """
    try:
        with requests.Session() as session:
            response = session.get(url, stream=True)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))

            with open(filename, 'wb') as f, tqdm(total=total_size, unit='iB', unit_scale=True, desc=filename) as pbar:
                for data in response.iter_content(chunk_size=1024):
                    f.write(data)
                    pbar.update(len(data))

        logging.info(f"Файл '{filename}' успешно скачан.")
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при скачивании файла '{filename}': {e}")
        return False


def download_video_alt(season, episode, quality):
    if int(quality) <= 1080:
        ext = "mp4"
    else:
        ext = "webm"
    url = f"{BASE_URL}video/G4/FiM/media/s{season}/e{episode}/{quality}.{ext}"
    filename = os.path.join(TEMP_DIR, f"video.{ext}")
    logging.info("Скачивание видео")
    return DownloadFileALT(url, filename)


def download_audio_alt(season, episode, dub_code):
    url = f"{BASE_URL}video/G4/FiM/media/s{season}/e{episode}/{dub_code}.opus"
    filename = os.path.join(TEMP_DIR, "audio.opus")
    logging.info("Скачивание аудио")
    return DownloadFileALT(url, filename)


def download_subs_alt(season, episode, subs_code):
    url = f"{BASE_URL}video/G4/FiM/media/s{season}/e{episode}/{subs_code}.ass"
    filename = os.path.join(TEMP_DIR, "subs.ass")
    logging.info("Скачивание субтитров")
    return DownloadFileALT(url, filename)