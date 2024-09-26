import configparser
import os
import logging

# Объявление глобальных переменных
max_retries = 3
num_threads = 4

# Путь к файлу настроек
config_file = os.path.join(os.path.dirname(__file__), 'config.ini')

# Создание объекта configparser
config = configparser.ConfigParser()

# Чтение настроек из файла (если он существует)
if os.path.exists(config_file):
    config.read(config_file)

if not os.path.exists(config_file):
    with open(config_file, 'w') as f:
        config.add_section('Downloader')
        config.set('Downloader', 'max_retries', '3')
        config.set('Downloader', 'num_threads', '4')
        config.write(f)

def show_settings_menu():
    """
    Отображает меню настроек в консоли.
    """

    global max_retries  # Объявление глобальных переменных
    global num_threads

    # Получение значений настроек из конфига
    max_retries = config.getint('Downloader', 'max_retries', fallback=max_retries)
    num_threads = config.getint('Downloader', 'num_threads', fallback=num_threads)

    while True:
        print("\nМеню настроек:")
        print(f"1. Максимальное количество попыток загрузки. Текущее значение: <{max_retries}>")
        print(f"2. Количество потоков загрузки. Текущее значение: <{num_threads}>")
        print("3. Сохранить и выйти")

        choice = input("Выберите пункт меню: ")

        if choice == '1':
            new_max_retries = int(input("Введите новое значение для 'Максимальное количество попыток загрузки': "))
            max_retries = new_max_retries
            config.set('Downloader', 'max_retries', str(max_retries))
            logging.info(f"Установлено новое значение кол-ва попыток: {max_retries}")
        elif choice == '2':
            new_num_threads = int(input("Введите новое значение для 'Количество потоков загрузки': "))
            num_threads = new_num_threads
            config.set('Downloader', 'num_threads', str(num_threads))
            logging.info(f"Установлено новое количество потоков загрузки: {num_threads}")
        elif choice == '3':
            logging.info(f"Пользователь завершил настройку.")
            logging.info(f"Настройки успешно сохранены")
            break
        else:
            print("Неверный пункт меню.")

    # Сохранение настроек в файл
    with open(config_file, 'w') as f:
        config.write(f)