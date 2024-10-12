import requests
import logging

from Logs import SUCCESS
from Config import config

TO_API_URL = 'https://магиядружбы.рф/api/v1/episodes'
TO_BASE_URL = 'https://база.магиядружбы.рф'

TDT_API_URL = 'https://thedoctorteam.ru'  # URL
TDT_BASE_URL = 'https://media.thedoctor.team/videos'  # Database URL


class APIHandlerTO:
    """
    Парсер API для магиядрубы.рф
    """

    def check_api_availability(self):
        try:
            timeout = config.getint('Downloader', 'timeout')
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
            response = requests.get(TO_API_URL, headers=headers, timeout=timeout)
            response.encoding = 'utf-8'
            if config.getboolean('ApiHandler', 'tdt_sub'):  # С проверкой на tdt_sub
                logging.info(f"Отправлен запрос TO: {response.request.url}")
            else:
                logging.info(f"Отправлен запрос: {response.request.url}")
            if response.status_code == 200:
                if config.getboolean('ApiHandler', 'tdt_sub'):
                    logging.log(SUCCESS, f"Получен ответ TO: {response.status_code} - {response.reason}")
                else:
                    logging.log(SUCCESS, f"Получен ответ: {response.status_code} - {response.reason}")
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            logging.critical(f"Ошибка при проверке доступности API: {e}")
            print(f"API недоступен. Пожалуйста, проверьте ваше интернет-соединение или попробуйте позже.")
            return False

    def get_episodes(self, season_id, count=30):
        url = f"{TO_API_URL}?count={count}&categoryId={season_id}"
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
            url = f'{TO_API_URL}/name/{episode_name.replace(" ", "%20")}'
            logging.info(f"Отправка запроса на получение данных о серии: {url}")
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"Ошибка запроса данных для эпизода: {e}")
        return None


class ApiHandlerTDT:
    """
    Парсер API для TheDoctorTeam.ru
    """

    def check_api_availability(self):
        try:
            timeout = config.getint('Downloader', 'timeout')
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
            response = requests.get(f"{TDT_API_URL}/project/mlp", headers=headers, timeout=timeout)
            response.encoding = 'utf-8'
            logging.info(f"Отправлен запрос TDT: {response.request.url}")
            if response.status_code == 200:
                logging.log(SUCCESS, f"Получен ответ TDT: {response.status_code} - {response.reason}")
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            logging.critical(f"Ошибка при проверке доступности API TDT: {e}")
            print(f"API недоступен. Пожалуйста, проверьте ваше интернет-соединение или попробуйте позже TDT.")
            return False

    def get_sub(self, season_id, episode, langSub):
        logging.debug("get_sub(), принятые значения:")
        logging.debug(f"season_id = {season_id}")
        logging.debug(f"episode = {episode}")
        """
        Получает URL субтитров с сайта TDT.

        Args:
            season_id (int): Номер сезона.
            episode (int): Номер эпизода.
            langSub (str): Код языка субтитров c заглавной буквы (например, 'Rus').

        Returns:
            str: URL субтитров или None, если субтитры не найдены.
            bool: True, если субтитры найдены
        """
        episode_str = f"{episode:02s}"
        url = f"{TDT_BASE_URL}/season{season_id}/{season_id}x{episode_str}_{langSub}Subtitles.ass"
        try:
            timeout = int(config.get('Downloader', 'timeout'))
            logging.debug(f"timeout = {timeout}")

            response = requests.head(url, timeout=timeout)
            logging.debug(f"status_code = {response.status_code}")
            if response.status_code == 200:
                logging.debug(f"Субтитры с сайта TDT для серии [{season_id}] {episode} найдены!")
                logging.debug(f"TDT original url = {url}")
                return {'url': url, 'lang': langSub, 'name': 'TheDoctorTeam (TDT original)',}
            else:
                logging.info(f"Субтитры с сайта TDT не найдены")
                logging.debug(f"TDT original url = {url}")
                return None
        except requests.RequestException as e:
            logging.error(f"Ошибка при проверке субтитров TDT: {e}")
            return None

