import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta

# Константы
TOKEN = ""
HELP_TEXT = """
/help — вывести список команд
/add — добавить задачу
/show — показать задачи
/exit — выйти из программы
/random — перенести случайную задачу на сегодня
/new_random — добавить новую случайную задачу
/archive_task — архивировать задачу
/archive_all — архивировать задачи ранее вчера
"""

bot = telebot.TeleBot(TOKEN)

# Хранилище задач и архива
tasks = {}
archive = {}
RANDOM_TASKS = {"Записаться на курс", "Покормить кошку", "Заправить машину"}

# Вспомогательные функции
def get_formatted_date(delta_days=0):
    return (datetime.now() + timedelta(days=delta_days)).strftime('%Y-%m-%d')

def add_task(date, task):
    tasks.setdefault(date, []).append(task)

def move_to_archive(date, task):
    archive.setdefault(date, []).append(task)
    tasks[date].remove(task)
    if not tasks[date]:  # Удаляем дату, если задач больше нет
        del tasks[date]

def create_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        KeyboardButton("/help"),  # Команда остаётся как есть
        KeyboardButton("/add"),
        KeyboardButton("/show"),
        KeyboardButton("/random"),
        KeyboardButton("/new_random"),
        KeyboardButton("/archive_task"),
        KeyboardButton("/archive_all"),
        KeyboardButton("/done")
    ]
    markup.add(*buttons)
    return markup

# Маппинг отображаемых текстов кнопок на команды
DISPLAY_TEXTS = {
    "/help": "Помощь",
    "/add": "Добавить задачу",
    "/show": "Показать задачи",
    "/random": "Случайная задача",
    "/new_random": "Новая задача",
    "/archive_task": "Архивировать задачу",
    "/archive_all": "Архивировать всё",
}

# Отправка кастомизированной клавиатуры
@bot.message_handler(commands=["start"])
def send_welcome(message):
    keyboard = create_main_keyboard()
    # Отправляем клавиатуру с пояснением
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Используйте кнопки ниже для взаимодействия.",
        reply_markup=keyboard
    )

# Переопределение обработки кнопок
@bot.message_handler(func=lambda message: message.text in DISPLAY_TEXTS.values())
def handle_custom_buttons(message):
    # Ищем команду, соответствующую тексту кнопки
    command = next((cmd for cmd, text in DISPLAY_TEXTS.items() if text == message.text), None)
    if command:
        bot.send_message(message.chat.id, f"Вы выбрали команду: {command}")
        # Логика для команды
        bot.process_new_updates([message])  # Пропускаем через существующие обработчики команд
    else:
        bot.send_message(message.chat.id, "Неизвестная команда.")


# Обработчики команд
# Обработка команды /start для показа клавиатуры
@bot.message_handler(commands=["start"])
def start_handler(message):
    markup = create_main_keyboard()
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Выберите команду из меню ниже:",
        reply_markup=markup,
    )

@bot.message_handler(commands=['help'])
def show_help(message):
    bot.send_message(message.chat.id, HELP_TEXT)

@bot.message_handler(commands=['add'])
def add_task_command(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Сегодня", callback_data=f"add:{get_formatted_date()}"),
        InlineKeyboardButton("Завтра", callback_data=f"add:{get_formatted_date(1)}")
    )
    markup.add(
        InlineKeyboardButton("Ближайший понедельник", callback_data=f"add:{get_formatted_date(7 - datetime.now().weekday())}"),
        InlineKeyboardButton("Со следующего месяца", callback_data="add:next_month")
    )
    markup.add(InlineKeyboardButton("Произвольная дата", callback_data="add:custom"))
    bot.send_message(message.chat.id, "Выберите дату для задачи:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('add:'))
def add_task_date(call):
    date = call.data.split(':')[1]
    if date == 'next_month':
        next_month_date = (datetime.now().replace(day=1) + timedelta(days=31)).strftime('%Y-%m-%d')
        bot.send_message(call.message.chat.id, f"Дата {next_month_date}. Введите задачу:")
        bot.register_next_step_handler(call.message, lambda msg: handle_task_input(msg, next_month_date))
    elif date == 'custom':
        bot.send_message(call.message.chat.id, "Введите дату в формате ГГГГ-ММ-ДД:")
        bot.register_next_step_handler(call.message, handle_custom_date_input)
    else:
        bot.send_message(call.message.chat.id, f"Дата {date}. Введите задачу:")
        bot.register_next_step_handler(call.message, lambda msg: handle_task_input(msg, date))

def handle_custom_date_input(message):
    try:
        date = datetime.strptime(message.text.strip(), '%Y-%m-%d').strftime('%Y-%m-%d')
        bot.send_message(message.chat.id, f"Выбрана дата {date}. Введите задачу:")
        bot.register_next_step_handler(message, lambda msg: handle_task_input(msg, date))
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат даты. Попробуйте еще раз:")
        bot.register_next_step_handler(message, handle_custom_date_input)

def handle_task_input(message, date):
    task = message.text.strip()
    if not task:
        bot.send_message(message.chat.id, "Задача не может быть пустой. Попробуйте еще раз:")
        bot.register_next_step_handler(message, lambda msg: handle_task_input(msg, date))
        return

    # Добавляем проверку на корректность даты
    if date not in tasks:
        tasks[date] = []
    add_task(date, task)
    bot.send_message(message.chat.id, f"Задача '{task}' добавлена на {date}.")



@bot.message_handler(commands=['random'])
def random_task_command(message):
    if not RANDOM_TASKS:
        bot.send_message(message.chat.id, "Список случайных задач пуст.")
    else:
        task = RANDOM_TASKS.pop()
        add_task(get_formatted_date(), task)
        bot.send_message(message.chat.id, f"Случайная задача '{task}' добавлена на сегодня.")

@bot.message_handler(commands=['archive_task'])
def archive_task_command(message):
    if not tasks:
        bot.send_message(message.chat.id, "Нет задач для архивации.")
        return
    bot.send_message(message.chat.id, "Введите дату задачи для архивации (ГГГГ-ММ-ДД):")
    bot.register_next_step_handler(message, handle_archive_task_date)

def handle_archive_task_date(message):
    try:
        date = message.text.strip()
        if date not in tasks:
            bot.send_message(message.chat.id, f"На дату {date} задач не найдено. Попробуйте ещё раз.")
            bot.register_next_step_handler(message, handle_archive_task_date)
            return

        task_list = "\n".join([f"- {task}" for task in tasks[date]])
        bot.send_message(message.chat.id, f"Задачи на {date}:\n{task_list}\nВведите задачу для архивации:")
        bot.register_next_step_handler(message, lambda msg: handle_archive_task(msg, date))
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")
        bot.register_next_step_handler(message, handle_archive_task_date)

@bot.message_handler(commands=['show'])
def show_tasks(message):
    if not tasks:
        bot.send_message(message.chat.id, "Список задач пуст.")
        return

    # Улучшение вывода задач
    response = "Ваши задачи:\n"
    for date, task_list in sorted(tasks.items()):
        tasks_str = "\n".join([f"  - {task}" for task in task_list])
        response += f"{date}:\n{tasks_str}\n"
    bot.send_message(message.chat.id, response)

def handle_archive_task(message, date):
    task = message.text.strip()
    if task in tasks[date]:
        move_to_archive(date, task)
        bot.send_message(message.chat.id, f"Задача '{task}' перенесена в архив.")
    else:
        bot.send_message(message.chat.id, "Задача не найдена. Попробуйте еще раз.")

@bot.message_handler(commands=['archive_task'])
def archive_task_command(message):
    if not tasks:
        bot.send_message(message.chat.id, "Нет задач для архивации.")
        return

    # Добавляем лог на случай пустого ввода
    bot.send_message(message.chat.id, "Введите дату задачи для архивации (ГГГГ-ММ-ДД):")
    bot.register_next_step_handler(message, handle_archive_task_date)

from telebot.types import ReplyKeyboardRemove
import random



# Обработчик команды /new_random
@bot.message_handler(commands=["new_random"])
def new_random_handler(message):
    bot.send_message(
        message.chat.id,
        "Введите текст задачи, чтобы добавить её в список:",
        reply_markup=ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(message, add_new_random_task)

def add_new_random_task(message):
    task_text = message.text.strip()
    if task_text.startswith("/"):
        bot.send_message(message.chat.id, "Нельзя использовать команды как текст задачи.")
        return
    RANDOM_TASKS.add(task_text)
    bot.send_message(message.chat.id, f"Задача '{task_text}' добавлена в список!")

# Обработчик команды /random
@bot.message_handler(commands=["random"])
def random_handler(message):
    if not RANDOM_TASKS:
        bot.send_message(message.chat.id, "Список случайных задач пуст.")
        return

    random_task = random.choice(list(RANDOM_TASKS))
    RANDOM_TASKS.remove(random_task)
    bot.send_message(message.chat.id, f"Случайная задача '{random_task}' добавлена на сегодня.")

def add_custom_task(message):
    new_task = message.text.strip()
    if new_task:
        RANDOM_TASKS.add(new_task)
        bot.send_message(message.chat.id, f"Задача '{new_task}' добавлена в список!")
    else:
        bot.send_message(message.chat.id, "Ошибка: задача не может быть пустой.")

@bot.message_handler(commands=['archive_all'])
def archive_all_command(message):
    if not tasks:
        bot.send_message(message.chat.id, "Нет задач для архивации.")
        return

    # Получаем дату вчерашнего дня
    yesterday = get_formatted_date(-1)

    # Метод для перебора задач и присвоения номеров

    # Обработчик выбора задачи по номеру
def handle_task_selection(message):
    try:
        task_number = int(message.text.strip())
        task_list = []
        task_counter = 1
        # Перебираем все задачи для поиска выбранной по номеру
        for date, tasks_on_date in sorted(tasks.items()):
            for task in tasks_on_date:
                if task_counter == task_number:
                    bot.send_message(message.chat.id, f"Вы выбрали задачу:\nДата: {date}\nЗадача: {task}")
                    return task  # Возвращаем выбранную задачу
                task_counter += 1

        # Если номер не найден
        bot.send_message(message.chat.id, "Неверный номер задачи. Попробуйте снова.")
        bot.register_next_step_handler(message, handle_task_selection)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите правильный номер задачи.")
        bot.register_next_step_handler(message, handle_task_selection)



# Метод для перебора задач и присвоения номеров
def list_tasks_with_numbers(message):
    if not tasks:
        bot.send_message(message.chat.id, "Нет задач для выбора.")
        return

    # Строим список задач с номерами
    task_list = []
    task_counter = 1
    for date, tasks_on_date in sorted(tasks.items()):
        for task in tasks_on_date:
            task_list.append(f"{task_counter}. {date} - {task}")
            task_counter += 1

    # Отправляем список задач пользователю
    task_list_message = "\n".join(task_list)
    bot.send_message(message.chat.id, f"Выберите задачу из списка, введя её номер:\n\n{task_list_message}")
    bot.register_next_step_handler(message, handle_task_selection)

@bot.message_handler(commands=['archive_task'])
def archive_task_command(message):
    if not tasks:
        bot.send_message(message.chat.id, "Нет задач для архивации.")
        return

    # Запрашиваем выбор задачи для архивации
    bot.send_message(message.chat.id, "Выберите задачу для архивации:")
    list_tasks_with_numbers(message)  # Вызываем метод для выбора задачи


@bot.message_handler(commands=['archive_all'])
def archive_all_command(message):
    if not tasks:
        bot.send_message(message.chat.id, "Нет задач для архивации.")
        return

    # Получаем дату вчерашнего дня
    yesterday = get_formatted_date(-1)

    # Архивируем задачи до вчерашнего дня
    archived_any = False  # Флаг для проверки, были ли архивированы задачи
    for date in list(tasks.keys()):
        if date < yesterday:  # Если дата задачи раньше чем вчера
            for task in tasks[date]:
                move_to_archive(date, task)
            archived_any = True

    if archived_any:
        bot.send_message(message.chat.id, f"Все задачи, созданные до {yesterday}, были архивированы.")
    else:
        bot.send_message(message.chat.id, "Нет задач для архивации до вчерашнего дня.")

# Запуск бота
bot.polling(none_stop=True)