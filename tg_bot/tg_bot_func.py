import telebot

import settings
from cf_data.function import data_for_printing
from db_data.db_manager import ManagerDB

data_select = {}
bot = telebot.TeleBot(settings.TG_BOT_TOKEN)
start_db = ManagerDB(
    db_user=settings.DB_USER,
    db_password=settings.DB_PASSWORD,
    db_name=settings.DB_NAME,
    db_host=settings.DB_HOST,
    db_port=settings.DB_PORT,
)


@bot.message_handler(commands=["start"])
def welcome(message):
    """
    Команда /start или кнопка "Запустить" !!!!
    Выводит приветственное сообщение, сообщает о количестве задач,
    их сложности и темах, а так же отрисовывает кнопки выбора действий
    :param message:
    :return:
    """
    min_max_data = start_db.select_problem_rating()
    chat_id = message.chat.id
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_select = telebot.types.InlineKeyboardButton(
        text="Подобрать задачи", callback_data="select_push"
    )
    button_cancel = telebot.types.InlineKeyboardButton(
        text="Отмена", callback_data="cancel_push"
    )
    keyboard.add(button_select, button_cancel)
    bot.send_message(
        chat_id,
        f"Привет! "
        f"На данный момент в базе хранится {start_db.get_count_data()} "
        f"задач с сайта codeforces.com. "
        f'В базе присутствуют задачи по следующим темам: '
        f'\n\n\t{" ,".join(start_db.tags_words)}\n\n'
        f'Сложность задач варьируется от '
        f'{min_max_data["min"]} до {min_max_data["max"]} '
        f'с шагом в 100 ед. Для получения подборки задач нажми на копку '
        f'"Подобрать задачи", для отмены нажми кнопку "Отмена". ',
        reply_markup=keyboard,
    )


# функция обработки нажатия на кнопку "Подобрать задачи" или "Отмена"
@bot.callback_query_handler(func=lambda call: call.data == "select_push")
def select_func(call):
    """
    Функция обработки нажатия на кнопку "Подобрать задачи"
    :param call:
    :return:
    """
    message = call.message
    chat_id = message.chat.id
    # следующее изменение сообщения удалит кнопки и
    # вместо них оставит какое-нибудь сообщение
    bot.send_message(chat_id, "Введите тему задачи:")
    # следующая команда нужна,
    # чтоб сразу обработать следующее сообщение введенное пользователем.
    bot.register_next_step_handler(message, input_tags)


def input_tags(message):
    """
    Функция обработки введенной темы задачи
    :param message:
    :return:
    """
    data_select["tag"] = message.text.lower()
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите уровень сложности задач")
    bot.register_next_step_handler(message, input_level)


def input_level(message):
    """
    Функция обработки введенной сложности задач и вывода задач,
        соответствующих введенным данным
    :param message:
    :return:
    """
    level = message.text
    chat_id = message.chat.id
    min_max_data = start_db.select_problem_rating()
    if level.isdigit() and int(level) % 100 == 0:
        data_select["level"] = level
        output_list = start_db.result_select(data_select)
        if len(output_list) == 0:
            bot.send_message(chat_id, "Задачи не найдены")
        else:
            result_data = data_for_printing(output_list)
            for print_elem in result_data:
                bot.send_message(chat_id, print_elem)

    else:
        bot.send_message(
            chat_id, f"Разрешается ввод только чисел от "
                     f"{min_max_data['min']} до "
                     f"{min_max_data['max']} с шагом 100"
        )
        bot.register_next_step_handler(message, input_level)


@bot.callback_query_handler(func=lambda call: call.data == "cancel_push")
def cancel_func(call):
    """
    Функция обработки нажатия кнопки "отмена"
    :param call:
    :return:
    """
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    # следующее изменение сообщения удалит кнопки и
    # вместо них оставит како-енибудь сообщение
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text='Если передумаете, введите команду "/start"',
    )
