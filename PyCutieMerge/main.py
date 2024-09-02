import os
import sys
import time
from api_handler import APIHandler
from video_processor import VideoProcessor
from utils import display_menu, pony_log, confirm_choice


def main():
    # Стилизация и приветствие
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
 _______                _         _______                             
(_______)          _   (_)       (_______)                            
 _        _   _  _| |_  _  _____  _  _  _  _____   ____   ____  _____ 
| |      | | | |(_   _)| || ___ || ||_|| || ___ | / ___) / _  || ___ |
| |_____ | |_| |  | |_ | || ____|| |   | || ____|| |    ( (_| || ____|
 \______)|____/    \__)|_||_____)|_|   |_||_____)|_|     \___ ||_____)
                                                        (_____|        
    """)
    print("Made by Waltorvi\n")

    base_url = "https://example.com"  # Укажи актуальный URL API
    api_handler = APIHandler(base_url)

    # Шаг 2: Выбор сезона
    seasons = api_handler.get_seasons()
    season_choice = display_menu("Выберите сезон:", seasons)

    # Шаг 3: Выбор серии
    episodes = api_handler.get_episodes(season_choice)
    episode_choice = display_menu(f"Сезон {season_choice}:", episodes)

    # Шаг 4: Выбор качества видео
    qualities = api_handler.get_video_qualities(episode_choice)
    quality_choice = display_menu("Выберите качество видео:", qualities)

    # Шаг 5: Выбор озвучки
    audios = api_handler.get_audio_tracks(episode_choice)
    audio_choice = display_menu("Выберите озвучку:", audios)

    # Шаг 6: Выбор субтитров
    subtitles = api_handler.get_subtitles(episode_choice)
    subtitle_choice = display_menu("Выберите субтитры:", subtitles)

    # Шаг 7: Подтверждение выбора
    final_choice = confirm_choice({
        "Сезон": season_choice,
        "Серия": episode_choice,
        "Качество": quality_choice,
        "Озвучка": audio_choice,
        "Субтитры": subtitle_choice
    })

    if final_choice:
        # Шаг 8: Загрузка и сборка видео
        pony_log("Начинается загрузка и сборка видео...")
        video_processor = VideoProcessor()
        video_processor.process_video(
            episode_choice,
            quality_choice,
            audio_choice,
            subtitle_choice
        )
        pony_log("Видео успешно собрано!", style="success")
    else:
        pony_log("Выбор отменён, программа завершена.", style="error")


if __name__ == "__main__":
    main()

