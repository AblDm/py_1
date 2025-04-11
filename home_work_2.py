from datetime import datetime, timedelta

# Справка
HELP = """
help — справка о программе
add — добавить задачу
show — показать задачи
exit — выйти из программы
"""

# Словарь для хранения задач
tasks = {}

# Переменные для дат
today = datetime.now().strftime('%Y-%m-%d')
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
monday = (datetime.now() + timedelta(days=(7 - datetime.now().weekday()))).strftime('%Y-%m-%d')
month = (datetime(datetime.now().year, datetime.now().month + 1, 1) if datetime.now().month < 12
         else datetime(datetime.now().year + 1, 1, 1)).strftime('%Y-%m-%d')

# Функция для произвольной даты (5)
def ask_custom_date():
    while True:
        custom_date = input("Введите произвольную дату напоминания в формате ГГГГ-ММ-ДД: ")
        try:
            datetime.strptime(custom_date, '%Y-%m-%d')
            return custom_date
        except ValueError:
            print("Неверный формат! Попробуйте снова.")

# Функция для получения выбора пользователя с валидацией ввода
def get_choice():
    while True:
        try:
            choice = input("Введите номер (1-5, 0 для выхода): ").strip()
            if choice == "0":
                return None  # Выход из цикла
            choice = int(choice)
            if 1 <= choice <= 5:
                return choice
            else:
                print("Введите число от 1 до 5 или 0 для выхода.")
        except ValueError:
            print("Пожалуйста, введите число.")

# Основной цикл
run = True

while run:
    command = input("Введите команду: ")
    if command == "help":
        print(HELP)
    elif command == "show":
        print("\nАктуальные задачи:")
        for date, task_list in tasks.items():
            if date == today:
                formatted_date = "СЕГОДНЯ"
            elif date == tomorrow:
                formatted_date = "ЗАВТРА"
            else:
                formatted_date = date
            print(f"{formatted_date}:")
            for task in task_list:
                print(f" - {task}")
    elif command == "add":
        while True:
            print("Выберите тип задачи:")
            print("1 - Сегодня")
            print("2 - Завтра")
            print("3 - Ближайший понедельник")
            print("4 - Первый день следующего месяца")
            print("5 - Произвольная дата")
            print("0 - Вернуться в главное меню")

            choice = get_choice()
            if choice is None:  # Пользователь выбрал 0
                print("Возврат в главное меню.")
                break

            # Выбор даты
            if choice == 5:
                chosen_date = ask_custom_date()
            else:
                chosen_date = {
                    1: today,
                    2: tomorrow,
                    3: monday,
                    4: month
                }[choice]

            # Запрос задачи
            task = input(f"Введите задачу на {chosen_date} (или 'exit' для выхода): ").strip()
            if task.lower() == "exit":
                print("Возврат в главное меню.")
                break

            # Сохранение задачи
            if chosen_date not in tasks:
                tasks[chosen_date] = []
            if task not in tasks[chosen_date]:
                tasks[chosen_date].append(task)
                print(f"Задача добавлена на {chosen_date}.")
    elif command == "exit":
        print("Спасибо за использование! До свидания!")
        break
    else:
        print("Неизвестная команда. Попробуйте ввести help для вызова справки")