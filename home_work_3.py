from datetime import datetime, timedelta
import random
from itertools import count

# Справка
HELP = """
help — справка о программе
add — добавить задачу
show — показать задачи
exit — выйти из программы
random - перенести случайную задачу из списка на сегодня
"""

# Словарь для хранения задач
tasks = {}
# Список для архивных задач
archived_tasks = {}

RANDOM_TASKS = {"Записаться на курс", "Покормить кошку", "Заправить машину"}

# Переменные для дат
today = datetime.now().strftime('%Y-%m-%d')
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
monday = (datetime.now() + timedelta(days=(7 - datetime.now().weekday()))).strftime('%Y-%m-%d')
month = (datetime(datetime.now().year, datetime.now().month + 1, 1) if datetime.now().month < 12
         else datetime(datetime.now().year + 1, 1, 1)).strftime('%Y-%m-%d')

# Функция для вывода задач
def show_tasks():
    if not tasks:
        print("\nАктуальные задачи отсутствуют.")
        return

    print("\nАктуальные задачи:")
    for date, task_list in tasks.items():
        formatted_date = "СЕГОДНЯ" if date == today else "ЗАВТРА" if date == tomorrow else date
        print(f"{formatted_date}:")
        if not task_list:
            print("  - Нет задач")
        for task in task_list:
            print(f" - {task}")

# Функция для добавления задачи на произвольную дату
def ask_custom_date():
    while True:
        custom_date = input("Введите произвольную дату напоминания в формате ГГГГ-ММ-ДД: ")
        try:
            datetime.strptime(custom_date, '%Y-%m-%d')
            return custom_date
        except ValueError:
            print("Неверный формат! Попробуйте снова.")

# Функция для добавления задачи в список
def add_task_to_date(date, task):
    if date not in tasks:
        tasks[date] = []
    if task not in tasks[date]:
        tasks[date].append(task)
        print(f"Задача '{task}' добавлена на {date}.")
    else:
        print(f"Задача '{task}' уже существует на {date}.")

def add_random_tasks():
    task_random = input("Введите задачу для добавления в список на потом: ").strip()
    if task_random in RANDOM_TASKS:
        print(f"Задача '{task_random}' уже существует.")
    else:
        RANDOM_TASKS.add(task_random)
        print(f"Задача '{task_random}' добавлена в список случайных.")

    # Функция для добавления задачи
def add_task():
    while True:
        print("Выберите тип задачи:")
        print("1 - Сегодня")
        print("2 - Завтра")
        print("3 - Ближайший понедельник")
        print("4 - Первый день следующего месяца")
        print("5 - Произвольная дата")
        print("6 - Добавить в список на любое свободное время (рандомные дела)")
        print("0 - Вернуться в главное меню")

        choice = get_choice()
        if choice is None:  # Пользователь выбрал 0
            print("Возврат в главное меню.")
            break

        # Выбор даты
        if choice in [1, 2, 3, 4]:
            chosen_date = {
                1: today,
                2: tomorrow,
                3: monday,
                4: month
            }[choice]
            print(f"Выбрана дата: {chosen_date}.")  # Информируем о выбранной дате

            # Запрос задачи
            task = input(f"Введите задачу на {chosen_date} (или 'exit' для выхода): ").strip()
            if task.lower() == "exit":
                print("Возврат в главное меню.")
                break

            # Сохранение задачи
            add_task_to_date(chosen_date, task)

        elif choice == 5:
            chosen_date = ask_custom_date()
            task = input(f"Введите задачу на {chosen_date} (или 'exit' для выхода): ").strip()
            if task.lower() == "exit":
                print("Возврат в главное меню.")
                break
            add_task_to_date(chosen_date, task)

        elif choice == 6:
            add_random_tasks()  # Добавляем задачу в случайный список
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")

        # Сохранение задачи
        if chosen_date not in tasks:
            tasks[chosen_date] = []
        if task not in tasks[chosen_date]:
            tasks[chosen_date].append(task)
            print(f"Задача добавлена на {chosen_date}.")

# Функция для добавления случайной задачи
def add_random_task():
    if not RANDOM_TASKS:
        print("Список случайных задач пуст. Добавьте задачи для выбора.")
        return

    RANDOM_TASK = random.choice(list(RANDOM_TASKS))
    add_task_to_date(today, RANDOM_TASK)
    RANDOM_TASKS.remove(RANDOM_TASK)  # Убираем задачу из множества
    print(f"Случайная задача '{RANDOM_TASK}' добавлена на сегодня.")

# Функция для получения выбора пользователя
def get_choice():
    while True:
        try:
            choice = input("Введите номер (1-6, 0 для выхода): ").strip()
            if choice == "0":
                return None  # Выход из цикла
            choice = int(choice)
            if 1 <= choice <= 6:
                return choice
            else:
                print("Введите число от 1 до 6 или 0 для выхода.")
        except ValueError:
            print("Пожалуйста, введите число.")

# Основной цикл
def main():
    while True:
        command = input("Введите команду: ").strip().lower()
        if command == "help":
            print(HELP)
        elif command == "show":
            show_tasks()
        elif command == "random":
            add_random_task()
        elif command == "add":
            add_task()
        elif command == "exit":
            print("Спасибо за использование! До свидания!")
            break
        else:
            print("Неизвестная команда. Попробуйте ввести help для вызова справки.")

#задание 1
def count_letter(words, letter):
    count = 0
    for word in words:
        if letter in word:
            count += 1
    return count

# Запуск программы
if __name__ == "__main__":
    main()