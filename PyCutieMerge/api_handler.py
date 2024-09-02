import requests


class APIHandler:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_seasons(self):
        # Запрос сезонов через API
        response = requests.get(f"{self.base_url}/api/v1/seasons")
        if response.status_code == 200:
            return response.json()['seasons']
        else:
            raise Exception(f"Ошибка при запросе сезонов: {response.status_code}")

    def get_episodes(self, season_number):
        # Запрос серий через API
        response = requests.get(f"{self.base_url}/api/v1/seasons/{season_number}/episodes")
        if response.status_code == 200:
            return response.json()['episodes']
        else:
            raise Exception(f"Ошибка при запросе серий: {response.status_code}")

    def get_video_qualities(self, episode_id):
        # Запрос доступных качеств видео через API
        response = requests.get(f"{self.base_url}/api/v1/episodes/{episode_id}/qualities")
        if response.status_code == 200:
            return response.json()['qualities']
        else:
            raise Exception(f"Ошибка при запросе качеств видео: {response.status_code}")

    def get_audio_tracks(self, episode_id):
        # Запрос доступных озвучек через API
        response = requests.get(f"{self.base_url}/api/v1/episodes/{episode_id}/audio_tracks")
        if response.status_code == 200:
            return response.json()['audio_tracks']
        else:
            raise Exception(f"Ошибка при запросе озвучек: {response.status_code}")

    def get_subtitles(self, episode_id):
        # Запрос доступных субтитров через API
        response = requests.get(f"{self.base_url}/api/v1/episodes/{episode_id}/subtitles")
        if response.status_code == 200:
            return response.json()['subtitles']
        else:
            raise Exception(f"Ошибка при запросе субтитров: {response.status_code}")

# Пример использования
# api = APIHandler("https://example.com")
# data = api.get_episode_data("episode_name")