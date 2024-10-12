import requests
import logging
import os
import time
import re
import subprocess
import threading

from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

from Config import config
from Logs import SUCCESS

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(SCRIPT_DIR, ".temp")

BASE_URL = "https://база.магиядружбы.рф/"

chunk_lock = threading.Lock()


def DownloadFile(url, filename):
    """
    Скачивает файл по заданному URL и сохраняет его с указанным именем,
    используя многопоточную загрузку с ограничением скорости.

    Args:
        url (str): URL файла для скачивания.
        filename (str): Имя файла для сохранения.
    """
    try:
        max_retries = config.getint('Downloader', 'max_retries')
        num_threads = config.getint('Downloader', 'num_threads')
        downloader_type = config.get('Downloader', 'downloader_type')
        timeout = config.getint('Downloader', 'timeout')

        logging.info(f"Запуск загрузки файла: {filename}")
        logging.info(f"URL: {url}")
        logging.info(f"Выбран загрузчик: {downloader_type}")
        logging.info(f"Максимальное количество повторных попыток при ошибке загрузки: {max_retries}")
        logging.info(f"Число потоков для скачивания: {num_threads}")
        with requests.Session() as session:
            response = session.head(url, timeout=timeout)
            response.raise_for_status()
            file_size = int(response.headers.get('content-length', 0))
            logging.info(f"Размер файла: {file_size} байт")

            chunk_size = file_size // num_threads
            logging.info(f"Размер чанка: {chunk_size} байт")

            chunks = [(i * chunk_size, (i + 1) * chunk_size - 1) for i in range(num_threads - 1)]
            chunks.append(((num_threads - 1) * chunk_size, file_size - 1))
            logging.info(f"Список чанков: {chunks}")

            with ThreadPoolExecutor(max_workers=num_threads) as executor, open(filename, 'wb') as f:
                futures = []
                t = tqdm(total=file_size, unit='iB', unit_scale=True, desc=filename)

                def download_chunk(start, end, retry_count=0):
                    """
                    Скачивает заданный чанк файла.

                    Args:
                        start (int): Начальная позиция чанка.
                        end (int): Конечная позиция чанка.
                        retry_count (int, optional): Количество попыток загрузки. Defaults to 0.
                    """
                    logging.info(f"Загрузка чанка ({start}-{end})")
                    try:
                        headers = {'Range': f'bytes={start}-{end}'}
                        logging.info(f"Заголовки запроса: {headers}")

                        response = session.get(url, headers=headers, stream=True, timeout=timeout)
                        response.raise_for_status()
                        logging.info(f"Код ответа сервера: {response.status_code}")

                        downloaded_bytes = 0

                        for data in response.iter_content(chunk_size=1024):
                            with chunk_lock:  # Синхронизация записи чанков
                                logging.debug(f"Запись чанка в файл: {filename}")
                                f.seek(start)
                                f.write(data)
                                start += len(data)
                                logging.debug(f"Чанк записан.")

                            downloaded_bytes += len(data)
                            t.update(len(data))

                        logging.info(f"Чанк ({start}-{end}) успешно загружен.")

                    except requests.exceptions.RequestException as e:
                        logging.warning(f"Ошибка при загрузке фрагмента: {e}")
                        if retry_count < max_retries:
                            logging.info(f"Повторная попытка загрузки фрагмента (попытка {retry_count + 1})...")
                            time.sleep(1)
                            download_chunk(start, end, retry_count + 1)
                        else:
                            logging.error(f"Не удалось загрузить фрагмент после {max_retries} попыток.")
                            raise

                for i, (start, end) in enumerate(chunks):
                    logging.info(f"Создание потока {i + 1} для чанка ({start}-{end})")
                    futures.append(executor.submit(download_chunk, start, end))

                for i, future in enumerate(futures):
                    logging.info(f"Ожидание завершения потока {i + 1}")
                    future.result()
                    logging.info(f"Поток {i + 1} завершен.")

                t.close()

        logging.log(SUCCESS, "Файл '{filename}' успешно скачан.")
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при скачивании файла '{filename}': {e}")
        return False


def download_file_wget(url, filename):
    """Скачивает файл с помощью wget"""
    output_filename = None
    try:
        ext = os.path.splitext(url)[1]
        output_filename = os.path.splitext(filename)[0] + ext
        max_retries = config.getint('Downloader', 'max_retries')
        logging.info(f"Скачивание файла '{output_filename}' с помощью wget2...")
        command = [
            "wget",
            "-t", max_retries,
            "-O", output_filename,
            url
        ]
        logging.info(f"Команда wget2: {command}")
        subprocess.run(" ".join(command), check=True, cwd=TEMP_DIR)
        logging.log(SUCCESS, f"Файл '{output_filename}' успешно скачан с помощью wget2.")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при скачивании файла '{output_filename}' с помощью wget2: {e}")
        return False


def download_file_aria2c(url, filename):
    """Скачивает файл с помощью aria2c."""
    output_filename = None
    try:
        ext = os.path.splitext(url)[1]
        output_filename = os.path.splitext(filename)[0] + ext
        num_threads = config.getint('Downloader', 'num_threads')
        # aria2c_command = config.get('Downloader', 'aria2c_command')
        logging.info(f"Скачивание файла '{output_filename}' с помощью aria2c...")
        logging.info(f"URL: {url}")
        command = [
                "aria2c",
                "-c",
                "--allow-overwrite=true",
                "-x", str(num_threads),
                "-d", TEMP_DIR,
                "-o", os.path.basename(output_filename),
                url
        ]
        logging.info(f"Команда aria2c: {command}")
        subprocess.run(command, check=True)
        logging.log(SUCCESS, f"Файл '{output_filename}' успешно скачан с помощью aria2c.")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при скачивании файла '{output_filename}' с помощью aria2c: {e}")
        return False


def download_video(season, episode, quality):
    from Config import downloader_type

    if int(quality) <= 1080:
        ext = "mp4"
    else:
        ext = "webm"
    url = f"{BASE_URL}video/G4/FiM/media/s{season}/e{episode}/{quality}.{ext}"
    filename = os.path.join(TEMP_DIR, f"video.{ext}")
    logging.info(f"Скачивание видео: {filename}")
    if downloader_type == 'multithreaded':
        return DownloadFile(url, filename)
    elif downloader_type == 'wget':
        return download_file_wget(url, filename)
    elif downloader_type == 'aria2c':
        return download_file_aria2c(url, filename)
    else:
        logging.error(f"Неизвестный тип загрузчика: {downloader_type}")
        return False


def download_audio(season, episode, dub_code):
    from Config import downloader_type

    url = f"{BASE_URL}video/G4/FiM/media/s{season}/e{episode}/{dub_code}.opus"
    filename = os.path.join(TEMP_DIR, "audio.opus")
    logging.info(f"Скачивание аудио: {filename}")
    if downloader_type == 'multithreaded':
        return DownloadFile(url, filename)
    elif downloader_type == 'wget':
        return download_file_wget(url, filename)
    elif downloader_type == 'aria2c':
        return download_file_aria2c(url, filename)
    else:
        logging.error(f"Неизвестный тип загрузчика: {downloader_type}")
        return False


def download_subs(season, episode, subs_code):
    from Config import downloader_type

    url = f"{BASE_URL}video/G4/FiM/media/s{season}/e{episode}/{subs_code}.ass"
    filename = os.path.join(TEMP_DIR, "subs.ass")
    logging.info(f"Скачивание субтитров: {filename}")
    if downloader_type == 'multithreaded':
        return DownloadFile(url, filename)
    elif downloader_type == 'wget':
        return download_file_wget(url, filename)
    elif downloader_type == 'aria2c':
        return download_file_aria2c(url, filename)
    else:
        logging.error(f"Неизвестный тип загрузчика: {downloader_type}")
        return False


def sanitize_filename(filename):
    """
    Удаляет недопустимые символы из имени файла.

    Args:
        filename (str): Имя файла.

    Returns:
        str: Очищенное имя файла.
    """
    invalid_chars = r'[\\/:*?"<>|]'  # Запрещенные символы в Windows
    sanitized_filename = re.sub(invalid_chars, '', filename)

    if sanitized_filename != filename:
        logging.info(f"Из названия серии удалены недопустимые символы: '{filename}' -> '{sanitized_filename}'")

    return sanitized_filename
