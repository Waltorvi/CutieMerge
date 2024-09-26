import logging
import os
import sys
from pathlib import Path

from colorama import init, Fore, Style
import re

from API_Handler import APIHandler
from Downloader import download_video, download_audio, download_subs
from Merge import merge_video_audio_subs, cleanup_temp_files
from Episode_Selector import EpisodeSelector

init()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(sys.stdout)  # Вывод логов в консоль
                    ])

class ColoredConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        if record.levelno == logging.ERROR:
            record.msg = Fore.RED + record.msg + Style.RESET_ALL
        elif record.levelno == logging.INFO:
            record.msg = Fore.YELLOW + record.msg + Style.RESET_ALL
        super().emit(record)

# Замена стандартного обработчика на раскрашенный
for handler in logging.root.handlers[:]:
    if isinstance(handler, logging.StreamHandler):
        logging.root.removeHandler(handler)
logging.getLogger().addHandler(ColoredConsoleHandler())

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = str(Path.home() / "Downloads")
TEMP_DIR = os.path.join(SCRIPT_DIR, ".temp")
OUTPUT_DIR = os.path.join(DOWNLOADS_DIR, "CutieMerge")

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

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


def main():
    try:
        print(Fore.MAGENTA + " _______                _         _______                             " + Style.RESET_ALL)
        print(Fore.MAGENTA + "(_______)          _   (_)       (_______)                            " + Style.RESET_ALL)
        print(Fore.MAGENTA + " _        _   _  _| |_  _  _____  _  _  _  _____   ____   ____  _____ " + Style.RESET_ALL)
        print(Fore.MAGENTA + "| |      | | | |(_   _)| || ___ || ||_|| || ___ | / ___) / _  || ___ |" + Style.RESET_ALL)
        print(Fore.MAGENTA + "| |_____ | |_| |  | |_ | || ____|| |   | || ____|| |    ( (_| || ____|" + Style.RESET_ALL)
        print(Fore.MAGENTA + " \______)|____/    \__)|_||_____)|_|   |_||_____)|_|     \___ ||_____)" + Style.RESET_ALL)
        print(Fore.MAGENTA + "                                                        (_____|  " + Style.RESET_ALL)
        print(
            Fore.MAGENTA + "Сделано " + Fore.CYAN + "Waltorvi" + Fore.MAGENTA + " для " + Fore.WHITE + "МагияДружбы.рф" + Style.RESET_ALL)

        print(Fore.MAGENTA + "\nДоступные команды:" + Style.RESET_ALL)
        print(Fore.MAGENTA + "- /settings - меню настроек\n" + Style.RESET_ALL)

        ColoredConsoleHandler()

        api = APIHandler()

        if not api.check_api_availability():
            input(Fore.RED + "Нажмите Enter для выхода..." + Style.RESET_ALL)
            return

        selector = EpisodeSelector(api)
        season, selected_episode, english_title, selected_quality, selected_dub, selected_subs = selector.select_episode()
        sanitized_title = sanitize_filename(selected_episode['title'])

        if not season or not selected_episode or not english_title or not selected_quality or not selected_dub:
            input(Fore.RED + "Нажмите Enter для выхода..." + Style.RESET_ALL)  # Ожидание ввода перед закрытием
            return

        if not download_video(season, selected_episode['localId'], selected_quality):
            print(Fore.RED + "Ошибка при скачивании видео." + Style.RESET_ALL)
            return

        if not download_audio(season, selected_episode['localId'], selected_dub['code']):
            print(Fore.RED + "Ошибка при скачивании аудио." + Style.RESET_ALL)
            return

        if selected_subs and not download_subs(season, selected_episode['localId'], selected_subs['code']):
            print(Fore.RED + "Ошибка при скачивании субтитров." + Style.RESET_ALL)
            return

        video_filename = os.path.join(TEMP_DIR, "video.mp4") if int(selected_quality) <= 1080 else os.path.join(TEMP_DIR, "video.webm")
        audio_filename = os.path.join(TEMP_DIR, "audio.opus")
        subs_filename = os.path.join(TEMP_DIR, "subs.ass") if selected_subs else None
        output_filename = os.path.join(OUTPUT_DIR, f"[{selected_episode['categoryId']}] " + f"{selected_episode['localId']} " + f"{sanitized_title}.mkv")

        if not merge_video_audio_subs(video_filename, audio_filename, subs_filename, output_filename):
            print(Fore.RED + "Ошибка при объединении видео." + Style.RESET_ALL)
            return

        cleanup_temp_files()

        print(Fore.MAGENTA + "\nСерия " + Fore.CYAN + f"{selected_episode['title']}" + Fore.MAGENTA + " успешно скачана и объединена!\n" + Fore.MAGENTA +
                           "Ты можешь найти ее в директории загрузок " + Fore.YELLOW + f"{OUTPUT_DIR}" + Style.RESET_ALL)

        os.startfile(OUTPUT_DIR)

    except Exception as e:
        logging.error(Fore.RED + f"Произошла ошибка: {e}" + Style.RESET_ALL)
    input(Fore.RED + "Нажмите Enter для выхода..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()