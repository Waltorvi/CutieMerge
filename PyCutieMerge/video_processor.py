import os
import subprocess
from utils import pony_log

class VideoProcessor:
    def __init__(self, ffmpeg_path='ffmpeg'):
        self.ffmpeg_path = ffmpeg_path

    def process_video(self, episode, quality, audio, subtitles):
        video_url = self.get_video_url(episode, quality)
        audio_url = self.get_audio_url(episode, audio)
        subtitle_url = self.get_subtitle_url(episode, subtitles)

        output_file = f"{episode}_final.mp4"

        pony_log(f"Скачиваю видео: {video_url}")
        pony_log(f"Скачиваю аудио: {audio_url}")
        pony_log(f"Скачиваю субтитры: {subtitle_url if subtitles else 'Без субтитров'}")

        # Скачивание и сборка файла через ffmpeg
        command = [
            self.ffmpeg_path,
            '-i', video_url,
            '-i', audio_url,
            '-c:v', 'copy',
            '-c:a', 'aac',
        ]

        if subtitles:
            command.extend(['-i', subtitle_url, '-c:s', 'mov_text'])

        command.append(output_file)
        subprocess.run(command, check=True)

        pony_log(f"Видео собрано и сохранено как {output_file}", style="success")

        self.cleanup_temp_files()

    def get_video_url(self, episode, quality):
        # Возвращает URL для скачивания видео
        return f"https://example.com/videos/{episode}/{quality}.mp4"

    def get_audio_url(self, episode, audio):
        # Возвращает URL для скачивания аудио
        return f"https://example.com/audios/{episode}/{audio}.aac"

    def get_subtitle_url(self, episode, subtitles):
        # Возвращает URL для скачивания субтитров
        return f"https://example.com/subtitles/{episode}/{subtitles}.srt"

    def cleanup_temp_files(self):
        # Удаляет временные файлы
        pony_log("Удаление временных файлов...")
        # os.remove("temporary_file")
