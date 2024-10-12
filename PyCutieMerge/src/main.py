import logging
import os

from pathlib import Path
from colorama import init, Fore, Style

from API_Handler import APIHandlerTO
from Downloader import download_video, download_audio, download_subs, download_file_wget, download_file_aria2c, sanitize_filename
from ALTDownloader import download_video_alt, download_audio_alt, download_subs_alt
from Merge import merge_video_audio_subs, cleanup_temp_files
from Episode_Selector import EpisodeSelector
from Config import config
from Logs import ColoredConsoleHandler

init()  # colorama

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = str(Path.home() / "Downloads")
TEMP_DIR = os.path.join(SCRIPT_DIR, ".temp")
OUTPUT_DIR = config.get('Downloader', 'output_folder')

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
    logging.debug(f"Создана папка временных файлов: {TEMP_DIR}")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    logging.info(f"Создана папка для серий: {OUTPUT_DIR}")


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
        print(Fore.MAGENTA + "- /settings - меню настроек" + Style.RESET_ALL)
        if config.get('Downloader', 'downloader_type') == 'aria2c':
            print(Fore.MAGENTA + "- /aria2c - настройка команды aria2c (СКОРО)" + Style.RESET_ALL)
        if config.get('Downloader', 'downloader_type') == 'wget':
            print(Fore.MAGENTA + "- /wget - настройка команды wget (СКОРО)" + Style.RESET_ALL)
        print(Fore.MAGENTA + "- /defaults - выбор значений серии по умолчанию (СКОРО)" + Style.RESET_ALL)
        print(Fore.MAGENTA + "- /help - меню помощи (СКОРО)\n" + Style.RESET_ALL)

        ColoredConsoleHandler()

        to = APIHandlerTO()
        tdt = None

        if config.getboolean('ApiHandler', 'tdt_sub'):
            from API_Handler import ApiHandlerTDT
            tdt = ApiHandlerTDT()
            logging.info("Выбран Api TDT для загрузки субтитров от команды TheDoctorTeam")

            if not tdt.check_api_availability():
                logging.error("Api TheDoctorTeam.ru недоступен. Проверьте соединение с интернетом или попробуйте позже")

        if not to.check_api_availability():
            input(Fore.RED + "Нажмите Enter для выхода..." + Style.RESET_ALL)
            return

        selector = EpisodeSelector(to, tdt)
        season, selected_episode, english_title, selected_quality, selected_dub, selected_subs = selector.select_episode()
        sanitized_title = sanitize_filename(selected_episode['title'])

        if not season or not selected_episode or not english_title or not selected_quality or not selected_dub:
            input(Fore.RED + "Нажмите Enter для выхода..." + Style.RESET_ALL)  # Ожидание ввода перед закрытием
            return

        if config.get('Downloader', 'downloader_type') == 'multithreaded':
            if not download_video(season, selected_episode['localId'], selected_quality):
                logging.warning(f"Ошибка при скачивании видео.")
                return

            if not download_audio(season, selected_episode['localId'], selected_dub['code']):
                logging.warning(f"Ошибка при скачивании аудио.")
                return

            if selected_subs and not download_subs(season, selected_episode['localId'], selected_subs['code']):
                logging.warning(f"Ошибка при скачивании субтитров.")
                return
        elif config.get('Downloader', 'downloader_type') == 'alternative':
            if not download_video_alt(season, selected_episode['localId'], selected_quality):
                logging.warning(f"Ошибка при скачивании видео.")
                return

            if not download_audio_alt(season, selected_episode['localId'], selected_dub['code']):
                logging.warning(f"Ошибка при скачивании аудио.")
                return

            if selected_subs and not download_subs_alt(season, selected_episode['localId'], selected_subs['code']):
                logging.error(f"Ошибка при скачивании субтитров.")
                return
        elif config.get('Downloader', 'downloader_type') == 'wget':
            url_sub = ''
            if selected_subs:
                if selected_subs.get('name') == 'TheDoctorTeam (TDT original)' and 'url' in selected_subs:  # Проверяем, если это TDT Original
                    url_sub = selected_subs['url']
                else:
                    url_sub = f"https://xn--80aabz.xn--80acfekkz0b1a6ftb.xn--p1ai/video/G4/FiM/media/s{season}/e{selected_episode['localId']}/{selected_subs['code']}.ass"
            if int(selected_quality) <= 1080:
                ext = "mp4"
            else:
                ext = "webm"
            url_video = f"https://xn--80aabz.xn--80acfekkz0b1a6ftb.xn--p1ai/video/G4/FiM/media/s{season}/e{selected_episode['localId']}/{selected_quality}.{ext}"
            url_dub = f"https://xn--80aabz.xn--80acfekkz0b1a6ftb.xn--p1ai/video/G4/FiM/media/s{season}/e{selected_episode['localId']}/{selected_dub['code']}.opus"

            if not download_file_wget(
                    url_video,
                    os.path.join(TEMP_DIR, f"video.webm")):
                logging.warning(f"Ошибка при скачивании видео.")
                return
            if not download_file_wget(
                    url_dub,
                    os.path.join(TEMP_DIR, f"audio.opus")):
                logging.warning(f"Ошибка при скачивании аудио.")
                return
            if not download_file_wget(
                    url_sub,
                    os.path.join(TEMP_DIR, f"subs.ass")):
                logging.warning(f"Ошибка при скачивании субтитров.")
                return
        elif config.get('Downloader', 'downloader_type') == 'aria2c':
            url_sub = ''
            if selected_subs:
                if selected_subs.get('name') == 'TheDoctorTeam (TDT original)' and 'url' in selected_subs:  # Проверяем, если это TDT Original
                    url_sub = selected_subs['url']
                else:
                    url_sub = f"https://xn--80aabz.xn--80acfekkz0b1a6ftb.xn--p1ai/video/G4/FiM/media/s{season}/e{selected_episode['localId']}/{selected_subs['code']}.ass"

            if int(selected_quality) <= 1080:  # Добавлено
                ext = "mp4"
            else:
                ext = "webm"
            url_video = f"https://xn--80aabz.xn--80acfekkz0b1a6ftb.xn--p1ai/video/G4/FiM/media/s{season}/e{selected_episode['localId']}/{selected_quality}.{ext}"
            url_dub = f"https://xn--80aabz.xn--80acfekkz0b1a6ftb.xn--p1ai/video/G4/FiM/media/s{season}/e{selected_episode['localId']}/{selected_dub['code']}.opus"

            if not download_file_aria2c(
                    url_video,
                    os.path.join(TEMP_DIR, f"video.webm")):
                logging.warning(f"Ошибка при скачивании видео.")
                return
            if not download_file_aria2c(
                    url_dub,
                    os.path.join(TEMP_DIR, f"audio.opus")):
                logging.warning(f"Ошибка при скачивании аудио.")
                return
            if not download_file_aria2c(
                    url_sub,
                    os.path.join(TEMP_DIR, f"subs.ass")):
                logging.warning(f"Ошибка при скачивании субтитров.")
                input('fff')
                return
        else:
            if selected_subs and 'code' in selected_subs:
                if not download_subs(season, selected_episode['localId'], selected_subs['code']):
                    logging.error(f"Ошибка при скачивании субтитров.")
                    return
            logging.warning(f"Неизвестный тип загрузчика: {config.get('Downloader', 'downloader_type')}")
            return

        video_filename = os.path.join(TEMP_DIR, "video.mp4") if int(selected_quality) <= 1080 else os.path.join(TEMP_DIR, "video.webm")
        audio_filename = os.path.join(TEMP_DIR, "audio.opus")
        subs_filename = os.path.join(TEMP_DIR, "subs.ass") if selected_subs else None
        output_folder = config.get('Downloader', 'output_folder')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            logging.debug(f"Отсутствует папка серий: {output_folder}")
            logging.info(f"Создана папка для серий: {output_folder}")
        output_filename = os.path.join(output_folder, f"[{selected_episode['categoryId']}] {selected_episode['localId']} {sanitized_title}.mkv")

        if not merge_video_audio_subs(video_filename, audio_filename, subs_filename, output_filename):
            logging.error(f"Ошибка при объединении видео")
            return

        if config.getboolean('Main', 'delete_temp_files'):
            cleanup_temp_files()

        print(Fore.MAGENTA + "\nСерия " + Fore.CYAN + f"{selected_episode['title']}" + Fore.MAGENTA + " успешно скачана и объединена!\n" + Fore.MAGENTA +
                           "Ты можешь найти ее в директории загрузок " + Fore.YELLOW + f"{OUTPUT_DIR}" + Style.RESET_ALL)


        if config.getboolean('Main', 'open_folder_on_completion'):
            os.startfile(OUTPUT_DIR)

    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
    input(Fore.RED + "Нажмите Enter для выхода..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()