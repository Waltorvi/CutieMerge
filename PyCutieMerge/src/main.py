import logging
import os
import sys
import shutil
import subprocess

from API_Handler import APIHandler
from Downloader import download_video, download_audio, download_subs
from Merge import merge_video_audio_subs, cleanup_temp_files
from Episode_Selector import EpisodeSelector

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(sys.stdout)  # Вывод логов в консоль
                    ])

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(SCRIPT_DIR, ".temp")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "CutieMerge")

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def main():
    try:
        api = APIHandler()

        if not api.check_api_availability():
            input("Нажмите Enter для выхода...")
            return

        selector = EpisodeSelector(api)
        season, selected_episode, english_title, selected_quality, selected_dub, selected_subs = selector.select_episode()

        if not season or not selected_episode or not english_title or not selected_quality or not selected_dub:
            input("Нажмите Enter для выхода...")  # Ожидание ввода перед закрытием
            return

        if not download_video(season, selected_episode['localId'], selected_quality):
            print("Ошибка при скачивании видео.")
            return

        if not download_audio(season, selected_episode['localId'], selected_dub['code']):
            print("Ошибка при скачивании аудио.")
            return

        if selected_subs and not download_subs(season, selected_episode['localId'], selected_subs['code']):
            print("Ошибка при скачивании субтитров.")
            return

        video_filename = os.path.join(TEMP_DIR, "video.mp4") if int(selected_quality) <= 1080 else os.path.join(TEMP_DIR,
                                                                                                               "video.webm")
        audio_filename = os.path.join(TEMP_DIR, "audio.opus")
        subs_filename = os.path.join(TEMP_DIR, "subs.ass") if selected_subs else None
        output_filename = os.path.join(OUTPUT_DIR, f"{selected_episode['title']}.mkv")

        if not merge_video_audio_subs(video_filename, audio_filename, subs_filename, output_filename):
            print("Ошибка при объединении видео.")
            return

        cleanup_temp_files()

        print(f"\nСерия {selected_episode['title']} успешно скачана и объединена!\n"
                           f"Ты можешь найти ее в папке {OUTPUT_DIR}")

    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
    input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()