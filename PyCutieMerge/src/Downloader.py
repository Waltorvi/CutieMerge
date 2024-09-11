import requests
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
TEMP_DIR = os.path.join(DOWNLOADS_DIR, ".temp")

BASE_URL = "https://база.магиядружбы.рф/"


def DownloadFile(url, filename, num_threads=8):
    """
    Скачивает файл по заданному URL и сохраняет его с указанным именем,
    используя многопоточную загрузку.

    Args:
        url (str): URL файла для скачивания.
        filename (str): Имя файла для сохранения.
        num_threads (int, optional): Количество потоков для загрузки. Defaults to 8.
    """
    try:
        with requests.Session() as session:
            response = session.head(url)
            response.raise_for_status()
            file_size = int(response.headers.get('content-length', 0))

            chunk_size = file_size // num_threads
            chunks = [(i * chunk_size, (i + 1) * chunk_size - 1) for i in range(num_threads - 1)]
            chunks.append(((num_threads - 1) * chunk_size, file_size - 1))

            with ThreadPoolExecutor(max_workers=num_threads) as executor, open(filename, 'wb') as f:
                futures = []
                t = tqdm(total=file_size, unit='iB', unit_scale=True, desc=filename)

                def download_chunk(start, end):
                    headers = {'Range': f'bytes={start}-{end}'}
                    response = session.get(url, headers=headers, stream=True)
                    response.raise_for_status()
                    for data in response.iter_content(chunk_size=1024):
                        t.update(len(data))
                        f.seek(start)
                        f.write(data)
                        start += len(data)

                for start, end in chunks:
                    futures.append(executor.submit(download_chunk, start, end))

                for future in futures:
                    future.result()

                t.close()

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