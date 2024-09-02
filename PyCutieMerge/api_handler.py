import requests


class APIHandler:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_episode_data(self, episode_name):
        url = f"{self.base_url}/api/v1/episodes/name/{episode_name}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка при запросе данных эпизода: {response.status_code}")

# Пример использования
# api = APIHandler("https://example.com")
# data = api.get_episode_data("episode_name")