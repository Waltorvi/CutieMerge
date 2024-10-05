import logging
import os

from Config import config, num_threads

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(SCRIPT_DIR, ".temp")

aria2c_command = [
                "aria2c",
                "-c",
                "--allow-overwrite=true",
                "-x", str(num_threads),
                "-d", TEMP_DIR,
                "-o", "{os.path.basename(filename)}",
                "{url}"
        ]

def set_aria2c_command():
    """
    Позволяет пользователю настроить команду aria2c.
    """
    global aria2c_command
    print("\nТекущая команда aria2c:", aria2c_command)
    new_command = input("Введите новую команду aria2c (оставьте пустым, чтобы использовать команду по умолчанию): ")
    if new_command:
        aria2c_command = new_command
        config.set('Downloader', 'aria2c_command', aria2c_command)
        logging.info(f"Установлена новая команда aria2c: {aria2c_command}")
    else:
        aria2c_command = f"-c --allow-overwrite=true -x {num_threads} -d {TEMP_DIR} -o"
        config.set('Downloader', 'aria2c_command', aria2c_command)
        logging.info(f"Используется команда aria2c по умолчанию.")

    # Сохранение настроек в файл
    with open(config.config_file, 'w') as f:
        config.write(f)