import telebot

import settings

data_select = {}

bot = telebot.TeleBot(settings.TG_BOT_TOKEN)

@bot.message_handler(commands=['start'])  # команда /start или кнопка "Запустить" !!!!
def welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     'Привет! Добро пожаловать в бота сбора обратной связи!')

    # bot.send_message(chat_id,
    #                  'Привет! На данный момент в базе хранится ... задач с сайта codeforces.org. В базе присутствуют задачи по следующим темам: ...'
    #                  'Сложность задач варьируется от ... до ... с шагом в 100 ед. Для получения подборки задач нажми на копку "Подобрать задачи", для отмены нажми кнопку "Отмена". ')

    keyboard = telebot.types.InlineKeyboardMarkup()
    button_select = telebot.types.InlineKeyboardButton(text="Подобрать задачи",
                                                       callback_data='select_push')
    button_cancel = telebot.types.InlineKeyboardButton(text="Отмена",
                                                       callback_data='cancel_push')
    keyboard.add(button_select, button_cancel)
    bot.send_message(chat_id,
                     'Привет! На данный момент в базе хранится ... задач с сайта codeforces.org. В базе присутствуют задачи по следующим темам: ...'
                     'Сложность задач варьируется от ... до ... с шагом в 100 ед. Для получения подборки задач нажми на копку "Подобрать задачи", для отмены нажми кнопку "Отмена". ',
                     reply_markup=keyboard)


# функция обработки нажатия на кнопку "Подобрать задачи" или "Отмена"
@bot.callback_query_handler(func=lambda call: call.data == 'select_push')
def select_func(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    # следующее изменение сообщения удалит кнопки и вместо них оставит како-енибудь сообщение
    # bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Данные сохранены!')
    bot.send_message(chat_id, f'Ввдите через пробел темы задач:')
    # следующая команда нужна, чтоб сразу обработать следующее сообщение введенное пользователем.
    bot.register_next_step_handler(message, input_tags)


def input_tags(message):
    data_select['tags'] = message.text()
    chat_id = message.chat_id
    bot.send_message(chat_id, f'Введите уровень сложность задач')
    bot.register_next_step_handler(message, input_level)


def input_level(message):
    level = message.text()
    chat_id = message.chat_id
    if level.is_digit() and level % 100 == 0:
        data_select['level'] = level
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
