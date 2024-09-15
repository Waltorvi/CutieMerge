import requests
import logging

API_BASE_URL = 'https://магиядружбы.рф/api/v1/episodes'
BASE_URL = 'https://база.магиядружбы.рф'

class APIHandler:

    def check_api_availability(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1'
            }
            response = requests.get(API_BASE_URL, headers=headers)
            response.encoding = 'utf-8'
            logging.info(f"Отправлен запрос: {response.request.url}")
            logging.info(f"Получен ответ: {response.status_code} {response.reason}")
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            logging.error(f"Ошибка при проверке доступности API: {e}")
            print(f"API недоступен. Пожалуйста, проверьте ваше интернет-соединение или попробуйте позже.")
            return False

    def get_episodes(self, season_id, count=30):
        url = f"{API_BASE_URL}?count={count}&categoryId={season_id}"
        response = requests.get(url)

        if response.status_code == 200:
            episodes = response.json().get('items', [])
            return episodes
        else:
            logging.error(f"Ошибка при получении эпизодов: {response.status_code}")
            return []

    def get_episode_details(self, season, episode):
        category_id = self.get_category_id_by_season(season)
        episodes = self.get_episodes(category_id)
        if episodes:
            for ep in episodes:
                if ep['localId'] == str(episode):
                    return ep
        return None

    def get_episode_extras(self, episode_name):
        try:
            url = f'{API_BASE_URL}/name/{episode_name.replace(" ", "%20")}'
            logging.info(f"Отправка запроса на получение данных о серии: {url}")
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"Ошибка запроса данных для эпизода: {e}")
        return None