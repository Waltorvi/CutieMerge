import logging

from colorama import init, Fore, Style

from Config import config, show_settings_menu
from Commands import set_aria2c_command

class EpisodeSelector:
    def __init__(self, to_api, tdt_api):
        self.api = to_api
        self.tdt_api = tdt_api

    def select_episode(self):
        # Выбор сезона
        season_input = input(Fore.WHITE + "Введите номер сезона (1-9): " + Style.RESET_ALL)
        if season_input == '/settings':
            show_settings_menu()
        elif season_input == '/aria2c':
            set_aria2c_command()
        else:
            try:
                season = int(season_input) # Преобразование в число только если это не команда
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите число от 1 до 9.")
                return None

        while season < 1 or season > 9:
            print("Неверный номер сезона или команда.")
            season_input = input(Fore.WHITE + "Введите номер сезона (1-9): " + Style.RESET_ALL)
            if season_input == '/settings':
                show_settings_menu()
            elif season_input == '/aria2c':
                set_aria2c_command()
            else:
                try:
                    season = int(season_input)
                except ValueError:
                    print("Неверный ввод. Пожалуйста, введите число от 1 до 9.")
                    return None

        # Получение списка эпизодов
        episodes = self.api.get_episodes(season)

        if not episodes:
            logging.error(f"Не удалось получить список эпизодов для сезона {season}.")
            return

        # Получение названия сезона
        for episode in episodes:
            for translation in episode['category']['translations']:
                if translation['locale'] == 'en':
                        season_title = translation['subtitle']

        # Вывод списка эпизодов
        print(f"\nСезон {season} // {season_title}:")
        for i, episode in enumerate(episodes):
            english_title = None
            for translation in episode.get('translations', []):
                if translation.get('locale') == 'en':
                    english_title = translation.get('title')
                    break
            print(f"{i + 1}. {episode['title']} - {english_title}")

        # Выбор эпизода
        episode_input = input(Fore.GREEN + "Введите номер эпизода: " + Style.RESET_ALL)
        if episode_input == '/settings':
            show_settings_menu()
        else:
            try:
                episode_number = int(episode_input)
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите число.")
                return None

        while episode_number < 1 or episode_number > len(episodes):
            episode_input = input(
                Fore.GREEN + "Введите номер эпизода: " + Style.RESET_ALL)
            if episode_input == '/settings':
                show_settings_menu()
            else:
                try:
                    episode_number = int(episode_input)
                except ValueError:
                    print("Неверный ввод. Пожалуйста, введите число.")
                    return None

        selected_episode = episodes[episode_number - 1]
        english_title = None
        for translation in selected_episode.get('translations', []):
            if translation.get('locale') == 'en':
                english_title = translation.get('title')
                break

        if not english_title:
            logging.error(f"Не удалось найти английское название для эпизода {selected_episode['title']}")
            return None

        logging.info(f"Выбран эпизод: {selected_episode['title']} ({english_title})")

        # Получаем дополнительную информацию о серии
        episode_extras = self.api.get_episode_extras(english_title)

        if not episode_extras:
            logging.error(f"Не удалось получить информацию о серии {english_title}.")
            return None

        # Выбор качества видео
        print(Fore.WHITE + "\nДоступное качество видео:" + Style.RESET_ALL)
        quality_labels = {
            "2160": "[4K]",
            "1440": "[2K]",
            "1080": "[Full HD]",
            "720": "[HD]"
        }
        sorted_qualities = sorted(episode_extras['videos'], key=lambda x: int(x), reverse=True)
        for i, quality in enumerate(sorted_qualities):
            label = quality_labels.get(quality, "")
            print(f"{i + 1}. {label} {quality}p")

        selected_quality_index = int(input(Fore.GREEN + "Выберите качество видео (номер): " + Style.RESET_ALL)) - 1
        while selected_quality_index < 0 or selected_quality_index >= len(sorted_qualities):
            print("Неверный номер качества видео.")
            selected_quality_index = int(input(Fore.GREEN + "Выберите качество видео (порядковый номер): " + Style.RESET_ALL)) - 1
        selected_quality = sorted_qualities[selected_quality_index]

        # Выбор озвучки
        print(Fore.WHITE + "\nДоступные озвучки:" + Style.RESET_ALL)
        # Оригинал первым
        original_dub = None
        for dub in episode_extras['dubs']:
            if dub['name'] == 'Original':
                original_dub = dub
                break
        if original_dub:
            print(f"1. [{original_dub['lang']}] {original_dub['name']}")

        # Остальные озвучки в алфавитном порядке
        other_dubs = sorted([dub for dub in episode_extras['dubs'] if dub['name'] != 'Original'],
                            key=lambda x: x['name'])
        for i, dub in enumerate(other_dubs):
            print(f"{i + 2}. [{dub['lang']}] {dub['name']}")

        selected_dub_index = int(input(Fore.GREEN + "Выберите озвучку (номер): " + Style.RESET_ALL)) - 1
        if original_dub:
            if selected_dub_index == 0:
                selected_dub = original_dub
            elif 1 <= selected_dub_index <= len(other_dubs):
                selected_dub = other_dubs[selected_dub_index - 1]
            else:
                print("Неверный номер озвучки.")
                return None
        else:
            if 0 <= selected_dub_index <= len(other_dubs) - 1:
                selected_dub = other_dubs[selected_dub_index]
            else:
                print("Неверный номер озвучки.")
                return None

        # Выбор субтитров
        other_subs = sorted(episode_extras['subs'], key=lambda x: x['name'])

        if config.getboolean('ApiHandler', 'tdt_sub'):
            tdt_sub = self.tdt_api.get_sub(season, selected_episode['localId'], 'Rus')
            if tdt_sub:
                logging.info(f"Субтитры с сайта TDT для серии [{selected_episode['categoryId']}] {selected_episode['localId']} '{selected_episode['title']}' найдены!")
                other_subs = [sub for sub in other_subs if sub.get('name') != 'TheDoctor Team']
                other_subs.insert(0, tdt_sub)

        print(Fore.WHITE + "\nДоступные субтитры:" + Style.RESET_ALL)
        print("1. Без субтитров")

        for i, sub in enumerate(other_subs):
            print(f"{i + 2}. [{sub.get('lang', 'N/A')}] {sub['name']}")

        selected_subs_index = int(input(Fore.GREEN + "Выберите субтитры (номер): " + Style.RESET_ALL)) - 1
        if selected_subs_index == 0:
            selected_subs = None  # Без субтитров
        elif 1 <= selected_subs_index <= len(other_subs):
            selected_subs = other_subs[selected_subs_index - 1]
        else:
            print("Неверный номер субтитров.")
            return None

        # Подтверждение выбора
        print("\nВы выбрали:")
        print(f"- Сезон: {season}")
        print(f"- Эпизод: {selected_episode['title']} ({english_title})")
        print(f"- Качество видео: {selected_quality}p")
        print(f"- Озвучка: {selected_dub['name']}")
        print(f"- Субтитры: {selected_subs['name'] if selected_subs else 'Без субтитров'}")

        confirm = input(Fore.GREEN + "Подтвердить выбор? (да/нет): " + Style.RESET_ALL)
        if confirm.lower() != "да":
            print("Выбор отменен.")
            return()

        return season, selected_episode, english_title, selected_quality, selected_dub, selected_subs