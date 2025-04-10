# домашнее занадие №1
# задание 1

from datetime import datetime, timedelta

# Словарь для хранения задач
tasks = {}

#переменные для цикла
today = datetime.now().strftime('%Y-%m-%d')
tomorrow = (datetime.now()+timedelta(days=1)).strftime('%Y-%m-%d')
monday = (datetime.now() + timedelta(days=(7 - datetime.now().weekday()))).strftime('%Y-%m-%d')
month = (datetime(datetime.now().year, datetime.now().month + 1, 1) if datetime.now().month < 12
         else datetime(datetime.now().year + 1, 1, 1)).strftime('%Y-%m-%d')
# Функция для ввода произвольной даты
def ask_custom_date():
    while True:
        custom_date = input("Введите произвольную дату напоминания в формате ГГГГ-ММ-ДД: ")
        try:
            datetime.strptime(custom_date, '%Y-%m-%d')
            return custom_date
        except ValueError:
            print("Неверный формат Попробуйте снова")

# Словарь вариантов выбора даты
cycles_1 = {
    1: today,
    2: tomorrow,
    3: monday,
    4: month
}

# Выбор пользователя
for _ in range(3):
    print("Выберите тип задачи:")
    print("1 - Сегодня")
    print("2 - Завтра")
    print("3 - Ближайший понедельник")
    print("4 - Первый день следующего месяца")
    print("5 - Произвольная дата")

    while True:
        try:
            choice = int(input("Введите номер(1-5): "))
            if 1<= choice <=5:
                break
            else:
                print("Выерите число от 1 до 5")
        except ValueError:
            print("Введите число")

    #Обработка даты из словаря
    if choice == 5:
        chosen_date = ask_custom_date()
    else:
        chosen_date = cycles_1[choice]

    #Запрос задачи
    task = input(f"Введите задачу на {chosen_date}: ")

    #сохранение в словарь
    if chosen_date not in tasks:
        tasks[chosen_date] = []
    if task not in tasks[chosen_date]:
        tasks[chosen_date].append(task)

# Результат
print("\nАктуальные задачи:")
for date, task_list in tasks.items():
    formatted_date = "СЕГОДНЯ" if date == today else date
    print(f"{formatted_date}:")
    for task in task_list:
        print(f" - {task}")