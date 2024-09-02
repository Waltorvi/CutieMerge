from api_handler import APIHandler
from video_processor import VideoProcessor

def main():
    base_url = "https://example.com"  # Указать url
    episode_name = input("Введите название эпизода: ")

    api_handler = APIHandler(base_url)
    video_processor = VideoProcessor()

    try:
        episode_data = api_handler.get_episode_data(episode_name)
        video_url = episode_data['video_url']
        audio_url = episode_data['audio_url']
        subtitles_url = episode_data['subtitles_url']

        output_file = f"{episode_name}.mp4"
        video_processor.merge_video(video_url, audio_url, subtitles_url, output_file)
        print(f"Видео успешно собрано и сохранено как {output_file}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
