import configparser
import os
import sys
import logging
import tkinter as tk

from tkinter import filedialog
from colorama import init, Fore, Style

from Logs import SUCCESS

init()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(SCRIPT_DIR, ".temp")

# Объявление глобальных переменных
max_retries = 3
num_threads = 4
downloader_type = 'multithreaded'
output_folder = os.path.join(os.path.expanduser("~"), "Downloads", "CutieMerge")
timeout = 10
open_folder_on_completion = True
tdt_sub = False
aria2c_command = f"-c --allow-overwrite=true -x {num_threads} -d {TEMP_DIR} -o"
delete_temp_files = True


# Путь к файлу настроек
config_file = os.path.join(os.path.dirname(sys.executable), 'config.ini')

config = configparser.ConfigParser()

if os.path.exists(config_file):
    config.read(config_file)

if not os.path.exists(config_file):
    with open(config_file, 'w') as f:
        config.add_section('Main')
        config.set('Main', 'open_folder_on_completion', 'True')
        config.set('Main', 'delete_temp_files', 'True')
        config.add_section('ApiHandler')
        config.set('ApiHandler', 'tdt_sub', 'False')
        config.add_section('Downloader')
        config.set('Downloader', 'max_retries', '3')
        config.set('Downloader', 'num_threads', '4')
        config.set('Downloader', 'downloader_type', 'alternative')
        config.set('Downloader', 'output_folder', output_folder)
        config.set('Downloader', 'timeout', '10')
        config.set('Downloader', 'aria2c_command', f"-c --allow-overwrite=true -x {num_threads} -d {TEMP_DIR} -o")
        config.write(f)
    logging.info(f"Создан файл настроек: {config_file}")

def choose_output_folder():
    """Открывает диалоговое окно для выбора папки."""
    root = tk.Tk()
    root.withdraw()  # Скрыть главное окно tkinter
    folder_path = filedialog.askdirectory()
    return folder_path

def show_settings_menu():
    """Отображает меню настроек в консоли."""
    logging.info(f"Файл конфигурации: {config_file}")

    # Main
    global open_folder_on_completion
    global delete_temp_files

    # ApiHandler
    global tdt_sub

    # Downloader
    global max_retries
    global num_threads
    global downloader_type
    global output_folder
    global timeout
    global aria2c_command

    # Получение значений настроек из конфига
    # Main
    open_folder_on_completion = config.getboolean('Main', 'open_folder_on_completion', fallback=open_folder_on_completion)
    delete_temp_files = config.getboolean('Main', 'delete_temp_files', fallback=delete_temp_files)

    # ApiHandler
    tdt_sub = config.getboolean('Main', 'tdt_sub', fallback=tdt_sub)

    # Downloader
    max_retries = config.getint('Downloader', 'max_retries', fallback=max_retries)
    num_threads = config.getint('Downloader', 'num_threads', fallback=num_threads)
    downloader_type = config.get('Downloader', 'downloader_type', fallback=downloader_type)
    output_folder = config.get('Downloader', 'output_folder', fallback=output_folder)
    timeout = config.getint('Downloader', 'timeout', fallback=timeout)
    aria2c_command = config.get('Downloader', 'aria2c_command', fallback=aria2c_command)

    while True:
        print("\nМеню настроек:")
        print(f"1. Максимальное количество попыток загрузки =", Style.BRIGHT + Fore.CYAN + f"{max_retries}" + Style.RESET_ALL)
        print(f"2. Количество потоков загрузки =", Style.BRIGHT + Fore.CYAN + f"{num_threads}" + Style.RESET_ALL)
        print(f"3. Тип загрузчика =", Style.BRIGHT + Fore.CYAN + f"{downloader_type}" + Style.RESET_ALL)
        print(f"4. Папка вывода =", Style.BRIGHT + Fore.CYAN + f"{output_folder}" + Style.RESET_ALL)
        print(f"5. Значение таймаута =", Style.BRIGHT + Fore.CYAN + f"{timeout}" + Style.RESET_ALL)
        print(f"6. Открывать папку по завершению загрузки =", Style.BRIGHT + Fore.CYAN + f"{open_folder_on_completion}" + Style.RESET_ALL)
        print(f"7. Загружать субтитры команды TheDoctorTeam с их сайта =" , Style.BRIGHT + Fore.CYAN + f"{tdt_sub}" + Style.RESET_ALL)
        print(f"8. Удаление временных файлов =", Style.BRIGHT + Fore.CYAN + f"{delete_temp_files}" + Style.RESET_ALL)
        # Параметры сохранения файла (имя)
        print("9. Сохранить и выйти")

        choice = input("Выберите пункт меню: ")

        if choice == '1':
            new_max_retries = int(input("Введите новое значение для 'Максимальное количество попыток загрузки': "))
            max_retries = new_max_retries
            config.set('Downloader', 'max_retries', str(max_retries))
            logging.info(f"Установлено новое значение кол-ва попыток: {max_retries}")
            mr = config.getint('Downloader', 'max_retries', fallback=max_retries)
            if mr == new_max_retries:
                logging.log(SUCCESS, "Настройка успешно изменена")

        elif choice == '2':
            new_num_threads = int(input("Введите новое значение для 'Количество потоков загрузки': "))
            num_threads = new_num_threads
            config.set('Downloader', 'num_threads', str(num_threads))
            logging.info(f"Установлено новое количество потоков загрузки: {num_threads}")

        elif choice == '3':
            print("Выберите тип загрузчика:")
            print("1. Альтернативный")
            print("2. aria2c - РЕКОМЕНДУЕТСЯ")
            print("3. wget")
            print("4. Многопоточный (EXP) - НЕ РЕКОМЕНДУЕТСЯ")

            downloader_choice = input("Введите номер: ")
            if downloader_choice == '1':
                downloader_type = 'alternative'
            elif downloader_choice == '2':
                downloader_type = 'aria2c'
            elif downloader_choice == '3':
                downloader_type = 'wget'
            elif downloader_choice == '4':
                downloader_type = 'multithreaded'
            else:
                print("Неверный выбор.")

            config.set('Downloader', 'downloader_type', downloader_type)
            logging.info(f"Установлен тип загрузчика: {downloader_type}")

        elif choice == '4':
            print("\nВыберите папку вывода:")
            print("1. Папка 'CutieMerge' в директории загрузок")
            print("2. Папка 'CutieMerge' в директории программы")
            print("3. Выбрать другую папку")

            folder_choice = input("Введите номер: ")

            if folder_choice == '1':
                output_folder = os.path.join(os.path.expanduser("~"), "Downloads", "CutieMerge")
            elif folder_choice == '2':
                output_folder = os.path.join(os.path.dirname(sys.executable), "CutieMerge")
            elif folder_choice == '3':
                output_folder = choose_output_folder()
                if not output_folder:
                    logging.info("Выбор папки отменен")
                    continue
            else:
                print("Неверный выбор.")
                continue

            config.set('Downloader', 'output_folder', output_folder)
            logging.info(f"Установлена папка вывода: {output_folder}")

        elif choice == '5':
            new_timeout = int(input("Введите новое значение для 'Таймаут (в секундах)': "))
            timeout = new_timeout
            config.set('Downloader', 'timeout', str(timeout))
            logging.info(f"Установлено новое значение таймаута: {timeout}")

        elif choice == '6':
            print("\nОткрывать папку с серией по завершению загрузки?:")
            print("1. Да")
            print("2. Нет")

            open_folder_choice = input("Введите номер: ")

            if open_folder_choice == '1':
                open_folder_on_completion = True
            elif open_folder_choice == '2':
                open_folder_on_completion = False
            else:
                print("Неверный выбор.")
                continue

            config.set('Main', 'open_folder_on_completion', str(open_folder_on_completion))
            logging.info(f"Настройка 'Открывать папку по завершению' установлена в: {open_folder_on_completion}")

        elif choice == '7':
            print("Скачивать субтитры команды TDT с их сайта?")
            print("1. Да")
            print("2. Нет")

            tdt_sub_choice = input("Введите номер: ")

            if tdt_sub_choice == '1':
                tdt_sub = True
            elif tdt_sub_choice == '2':
                tdt_sub = False
            else:
                print("Неверный выбор")
                continue

            config.set('ApiHandler', 'tdt_sub', str(tdt_sub))
            logging.info(f"Настройка 'Субтитры с сайта TDT' установлена в: {tdt_sub}")

        elif choice == '8':
            print("Удалять временные файлы после объединения?")
            print("1. Да")
            print("2. Нет")

            dtmp = input("Введите номер: ")

            if dtmp == '1':
                delete_temp_files = True
            elif dtmp == '2':
                delete_temp_files = False

            config.set('Main', 'delete_temp_files', str(delete_temp_files))
            logging.info(f"Настройка 'Удалять временные файлы' установлена в: {delete_temp_files}")

        elif choice == '9':
            logging.info(f"Пользователь завершил настройку.")
            logging.log(SUCCESS, f"Настройки успешно сохранены")
            break
        else:
            logging.error("Неверный пункт меню")

    # Сохранение настроек в файл
    with open(config_file, 'w') as f:
        config.write(f)

