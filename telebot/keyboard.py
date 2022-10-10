from telebot import types
import sqlite3


import functions as func

admin = types.InlineKeyboardMarkup(row_width=2)
admin.add(
    types.InlineKeyboardButton('?INFO?',callback_data='users'),
    types.InlineKeyboardButton('Статистика', callback_data='statistics')
)

menu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
menu.add(
    types.KeyboardButton('♻️Chenge'),
    types.KeyboardButton('👛Wallet')
)

markup = types.InlineKeyboardMarkup(row_width=2)
markup.add(
      types.InlineKeyboardButton("BTC/BUSD", callback_data = 'BTC_ch'),
      types.InlineKeyboardButton("ETH/BUSD", callback_data = 'ETH_ch'),
      types.InlineKeyboardButton("BNB/BUSD", callback_data = 'BNB_ch'),
      types.InlineKeyboardButton("SOL/BUSD", callback_data = 'SOL_ch'),
      types.InlineKeyboardButton("USDT/BUSD", callback_data = 'USDT_ch'),
      types.InlineKeyboardButton("USDC/BUSD", callback_data = 'USDC_ch')
)

markup2 = types.InlineKeyboardMarkup(row_width=2)
markup2.add(
    types.InlineKeyboardButton("Пополнить", parse_mode='html', callback_data='depo'),
    types.InlineKeyboardButton("Вывести", parse_mode='html', callback_data='withdraw')
    )

depo = types.InlineKeyboardMarkup(row_width=3)
depo.add(
    types.InlineKeyboardButton("BUSD", callback_data ='BUSD'),
    types.InlineKeyboardButton("BTC", callback_data ='BTC'),
    types.InlineKeyboardButton("USDC", callback_data ='USDC'),
    types.InlineKeyboardButton("ETH", callback_data ='ETH'),
    types.InlineKeyboardButton("SOL", callback_data ='SOL'),
    types.InlineKeyboardButton("BNB", callback_data ='BNB'),
    types.InlineKeyboardButton("USDT", callback_data ='USDT')
    )

withdrawn = types.InlineKeyboardMarkup(row_width=3)
withdrawn.add(
    types.InlineKeyboardButton("BUSD", callback_data ='BUSD_'),
    types.InlineKeyboardButton("BTC", callback_data ='BTC_'),
    types.InlineKeyboardButton("USDC", callback_data ='USDC_'),
    types.InlineKeyboardButton("ETH", callback_data ='ETH_'),
    types.InlineKeyboardButton("SOL", callback_data ='SOL_'),
    types.InlineKeyboardButton("BNB", callback_data ='BNB_'),
    types.InlineKeyboardButton("USDT", callback_data ='USDT_')
    )

buy_sell  = types.InlineKeyboardMarkup(row_width=2)
buy_sell.add(
    types.InlineKeyboardButton("Купить", callback_data = 'buy'),
    types.InlineKeyboardButton("Продать", callback_data = 'sell')
    )

send_  = types.InlineKeyboardMarkup(row_width=2)
send_.add(
    types.InlineKeyboardButton("Отправлено!", callback_data = 'send'),
    )
