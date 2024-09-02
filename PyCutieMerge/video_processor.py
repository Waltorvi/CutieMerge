import subprocess


class VideoProcessor:
    def __init__(self, ffmpeg_path='ffmpeg'):
        self.ffmpeg_path = ffmpeg_path

    def merge_video(self, video_url, audio_url, subtitles_url, output_file):
        command = [
            self.ffmpeg_path,
            '-i', video_url,
            '-i', audio_url,
            '-i', subtitles_url,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-c:s', 'mov_text',
            output_file
        ]
        subprocess.run(command, check=True)
