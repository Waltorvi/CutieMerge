import time

def display_menu(prompt, options):
    print(prompt)
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    choice = int(input("Введите номер: ")) - 1
    return options[choice]

def pony_log(message, style="info"):
    styles = {
        "info": "\033[94m",   # Синий
        "success": "\033[92m",# Зелёный
        "error": "\033[91m",  # Красный
        "reset": "\033[0m"    # Сброс цвета
    }
    print(f"{styles.get(style, styles['info'])}{message}{styles['reset']}")
    time.sleep(1)

def confirm_choice(choices):
    print("\nВы выбрали:")
    for key, value in choices.items():
        print(f"{key}: {value}")
    confirmation = input("\nЭто правильный выбор? (y/n): ").lower()
    return confirmation == 'y'
