import telebot

import settings
from cf_data.function import data_for_printing
from db_data.db_manager import ManagerDB

data_select = {}
bot = telebot.TeleBot(settings.TG_BOT_TOKEN)
start_db = ManagerDB(db_user=settings.DB_USER, db_password=settings.DB_PASSWORD, db_name=settings.DB_NAME, db_host=settings.DB_HOST, db_port=settings.DB_PORT)


@bot.message_handler(commands=['start'])  # команда /start или кнопка "Запустить" !!!!
def welcome(message):
    min_max_data = start_db.select_problem_rating()
    # print(start_db.tags_words)
    chat_id = message.chat.id
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_select = telebot.types.InlineKeyboardButton(text="Подобрать задачи",
                                                       callback_data='select_push')
    button_cancel = telebot.types.InlineKeyboardButton(text="Отмена",
                                                       callback_data='cancel_push')
    keyboard.add(button_select, button_cancel)
    bot.send_message(chat_id,
                     f'Привет! На данный момент в базе хранится {start_db.get_count_data()} задач с сайта codeforces.org. '
                     f'В базе присутствуют задачи по следующим темам: \n\n\t{" ,".join(start_db.tags_words)}\n\n'
                     f'Сложность задач варьируется от {min_max_data["min"]} до {min_max_data["max"]} с шагом в 100 ед. Для получения подборки задач нажми на копку '
                     f'"Подобрать задачи", для отмены нажми кнопку "Отмена". ',
                     reply_markup=keyboard)


# функция обработки нажатия на кнопку "Подобрать задачи" или "Отмена"
@bot.callback_query_handler(func=lambda call: call.data == 'select_push')
def select_func(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    # следующее изменение сообщения удалит кнопки и вместо них оставит како-енибудь сообщение
    # bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Данные сохранены!')
    bot.send_message(chat_id, f'Ввдите через пробел тему задачи:')
    # следующая команда нужна, чтоб сразу обработать следующее сообщение введенное пользователем.
    bot.register_next_step_handler(message, input_tags)


def input_tags(message):
    data_select['tag'] = message.text
    chat_id = message.chat.id
    bot.send_message(chat_id, f'Введите уровень сложности задач')
    bot.register_next_step_handler(message, input_level)


def input_level(message):
    level = message.text
    chat_id = message.chat.id
    if level.isdigit() and int(level) % 100 == 0:
        data_select['level'] = level
        output_list = start_db.result_select(data_select)
        if len(output_list) == 0:
            bot.send_message(chat_id, 'Задачи не найдены')
        else:
            result_data = data_for_printing(output_list)
            for print_elem in result_data:
                bot.send_message(chat_id, print_elem)

    else:
        bot.send_message(chat_id, f'Разрешается ввод только чисел от ... до ... с шагом 100')
        bot.register_next_step_handler(message, input_level)


@bot.callback_query_handler(func=lambda call: call.data == 'cancel_push')
def cancel_func(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    # следующее изменение сообщения удалит кнопки и вместо них оставит како-енибудь сообщение
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Если передумаете, введите команду "/start"')
