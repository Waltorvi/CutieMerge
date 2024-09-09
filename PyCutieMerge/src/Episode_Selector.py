import logging

class EpisodeSelector:
    def __init__(self, api):
        self.api = api

    def select_episode(self):
        # Выбор сезона
        season = int(input("Введите номер сезона (1-9): "))
        while season < 1 or season > 9:
            print("Неверный номер сезона.")
            season = int(input("Введите номер сезона (1-9): "))

        # Получение списка эпизодов
        episodes = self.api.get_episodes(season)

        if not episodes:
            print(f"Ошибка: Не удалось получить список эпизодов для сезона {season}.")
            logging.error(f"Не удалось получить список эпизодов для сезона {season}.")
            return

        # Вывод списка эпизодов
        print(f"\nСезон {season}:")
        for i, episode in enumerate(episodes):
            english_title = None
            for translation in episode.get('translations', []):
                if translation.get('locale') == 'en':
                    english_title = translation.get('title')
                    break
            print(f"{i + 1}. {episode['title']} - {english_title}")

        # Выбор эпизода
        episode_number = int(input("Введите номер эпизода: "))
        while episode_number < 1 or episode_number > len(episodes):
            print("Неверный номер эпизода.")
            episode_number = int(input("Введите номер эпизода: "))

        selected_episode = episodes[episode_number - 1]
        english_title = None
        for translation in selected_episode.get('translations', []):
            if translation.get('locale') == 'en':
                english_title = translation.get('title')
                break

        if not english_title:
            logging.error(f"Не удалось найти английское название для эпизода {selected_episode['title']}")
            print("Английское название не найдено.")
            return None

        logging.info(f"Выбран эпизод: {selected_episode['title']} ({english_title})")

        # Получаем дополнительную информацию о серии
        episode_extras = self.api.get_episode_extras(english_title)

        if not episode_extras:
            print(f"Ошибка: Не удалось получить информацию о серии {english_title}.")
            logging.error(f"Не удалось получить информацию о серии {english_title}.")
            return None

        # Вывод доступных качеств видео
        print("\nДоступные качества видео:")
        for i, quality in enumerate(episode_extras['videos']):
            print(f"{i + 1}. {quality}p")

        # Вывод доступных озвучек
        print("\nДоступные озвучки:")
        # Оригинал первым
        original_dub = None
        for dub in episode_extras['dubs']:
            if dub['name'] == 'Original':
                original_dub = dub
                break
        if original_dub:
            print(f"1. {original_dub['name']}")
            other_dubs = sorted([dub for dub in episode_extras['dubs'] if dub['name'] != 'Original'],
                                key=lambda x: x['name'])
            for i, dub in enumerate(other_dubs):
                print(f"{i + 2}. {dub['name']}")
        else:
            other_dubs = sorted(episode_extras['dubs'], key=lambda x: x['name'])
            for i, dub in enumerate(other_dubs):
                print(f"{i + 1}. {dub['name']}")

        print("\nДоступные субтитры:")
        print("1. Без субтитров")
        other_subs = sorted(episode_extras['subs'], key=lambda x: x['name'])
        for i, sub in enumerate(other_subs):
            print(f"{i + 2}. {sub['name']}")

        # Выбор качества видео
        selected_quality_index = int(input("Выберите качество видео (номер): ")) - 1
        while selected_quality_index < 0 or selected_quality_index >= len(episode_extras['videos']):
            print("Неверный номер качества видео.")
            selected_quality_index = int(input("Выберите качество видео (номер): ")) - 1
        selected_quality = episode_extras['videos'][selected_quality_index]

        # Выбор озвучки
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

        confirm = input("Подтвердить выбор? (да/нет): ")
        if confirm.lower() != "да":
            print("Выбор отменен.")
            return None

        return season, selected_episode, english_title, selected_quality, selected_dub, selected_subs