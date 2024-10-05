import logging
import sys

from colorama import Style, Fore

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(sys.stdout)  # Вывод логов в консоль
                    ])

# Определение уровня SUCCESS
SUCCESS = 25
logging.addLevelName(SUCCESS, 'SUCCESS')

def success(self, message, *args, **kws):
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, message, args, **kws)

logging.Logger.success = success

class ColoredConsoleHandler(logging.StreamHandler):
    """
        Логирование.

        levels:
            Debug (Bright white),
            Info (Yellow),
            Warning (Bright red),
            Error (Red),
            Critical (Bright red),
            Success (Bright Green)
        """
    def emit(self, record):
        log_colors = {
            logging.DEBUG: Style.BRIGHT + Fore.WHITE,
            logging.INFO: Fore.YELLOW,
            logging.WARNING: Style.BRIGHT + Fore.RED,
            logging.ERROR: Fore.RED,
            logging.CRITICAL: Style.BRIGHT + Fore.RED,
            SUCCESS: Style.BRIGHT + Fore.GREEN
        }

        # Префиксы для уровней логирования
        log_prefixes = {
            logging.DEBUG: "[DEBUG]",
            logging.INFO: "[INFO]",
            logging.WARNING: "[WARNING]",
            logging.ERROR: "[ERROR]",
            logging.CRITICAL: "[CRITICAL]",
            SUCCESS: "[SUCCESS]"
        }

        color = log_colors.get(record.levelno, Fore.WHITE)
        prefix = log_prefixes.get(record.levelno, "[LOG]")

        # Форматирование сообщения лога
        record.msg = f"{color}{prefix} - {record.msg}{Style.RESET_ALL}"
        super().emit(record)

# Замена стандартного обработчика на раскрашенный
for handler in logging.root.handlers[:]:
    if isinstance(handler, logging.StreamHandler):
        logging.root.removeHandler(handler)
logging.getLogger().addHandler(ColoredConsoleHandler())
