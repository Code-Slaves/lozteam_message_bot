from telebot import types


menu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

menu.add(
    types.KeyboardButton('Отправлять мне сообщения!'),
    types.KeyboardButton('Не отправлять мне сообщения!')
)


