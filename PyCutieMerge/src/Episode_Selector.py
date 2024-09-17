import logging
from colorama import init, Fore, Style

class EpisodeSelector:
    def __init__(self, api):
        self.api = api

    def select_episode(self):
        # Выбор сезона
        season = int(input(Fore.WHITE + "Введите номер сезона (1-9): " + Style.RESET_ALL))
        while season < 1 or season > 9:
            print("Неверный номер сезона.")
            season = int(input(Fore.WHITE + "Введите номер сезона (1-9): " + Style.RESET_ALL))

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
        episode_number = int(input(Fore.WHITE + "Введите номер эпизода: " + Style.RESET_ALL))
        while episode_number < 1 or episode_number > len(episodes):
            print("Неверный номер эпизода.")
            episode_number = int(input(Fore.WHITE + "Введите номер эпизода': " + Style.RESET_ALL))

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

        selected_quality_index = int(input("Выберите качество видео (номер): ")) - 1
        while selected_quality_index < 0 or selected_quality_index >= len(sorted_qualities):
            print("Неверный номер качества видео.")
            selected_quality_index = int(input("Выберите качество видео (порядковый номер): ")) - 1
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

        selected_dub_index = int(input("Выберите озвучку (номер): ")) - 1
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
        print(Fore.WHITE + "\nДоступные субтитры:" + Style.RESET_ALL)
        print("1. Без субтитров")

        other_subs = sorted(episode_extras['subs'], key=lambda x: x['name'])
        for i, sub in enumerate(other_subs):
            print(f"{i + 2}. [{sub['lang']}] {sub['name']}")

        selected_subs_index = int(input("Выберите субтитры (номер): ")) - 1
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

        confirm = input(Fore.WHITE + "Подтвердить выбор? (да/нет): " + Style.RESET_ALL)
        if confirm.lower() != "да":
            print("Выбор отменен.")
            return None

        return season, selected_episode, english_title, selected_quality, selected_dub, selected_subs