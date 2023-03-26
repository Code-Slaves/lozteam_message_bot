import telebot
import json
import requests
import keyboard as kb
import time
from function import get_notifications, clean_text, view_notif
from bs4 import BeautifulSoup as b
from fake_useragent import UserAgent
import threading

with open('config.json') as f:
    config = json.load(f)

class params:
	bot_id = config['config']['bot_id']
	chat_id = config['config']['telegram_chat_id']
	lolz_token = config['config']['lolz_api_token']


def check_condition():
    while True:
    	message_param = (config['config']['message_param'])
    	if message_param is True:
	        time.sleep(10)
	        notific = get_notifications(params.lolz_token)
	        if notific:
	        	time.sleep(5)
	        	view_notif(params.lolz_token)
	        	for i in notific:
	        		time.sleep(0.5)
	        		bot.send_message(chat_id= str(params.chat_id), text=clean_text(str(i['notification_html'])))


t = threading.Thread(target=check_condition)
t.start()









bot = bot = telebot.TeleBot(params.bot_id)


@bot.message_handler(commands=['start'])
def start_message(message):
	username = message.from_user.username
	chat_id = message.chat.id
	if chat_id != params.chat_id:
		bot.send_message(message.chat.id, "Привет, {0.first_name}!\n я буду присылать вам уведомления с сайта lolzteam!".format(message.from_user, bot.get_me()),parse_mode='html', reply_markup=kb.menu)
	else:
		bot.send_message(message.chat.id,"У вас нет прав на использования этого бота!")

@bot.message_handler(content_types=['text'])
def update_message_param(message):
	if message.chat.id != params.chat_id:
		if message.text == 'Отправлять мне сообщения!':
			config['config']['message_param'] = True

			with open('config.json', 'w') as f:
			    commit = json.dump(config, f)

			bot.send_message(message.chat.id,"Я буду присылать вам уведомления с сайта lolzteam!", reply_markup=kb.menu)

		elif message.text == 'Не отправлять мне сообщения!':
			bot.send_message(message.chat.id,"Я не буду присылать вам уведомления!", reply_markup=kb.menu)
			config['config']['message_param'] = False
			
			with open('config.json', 'w') as f:
			    commit = json.dump(config, f)

		else:
			bot.send_message(message.chat.id,"Неизвестная мне команда?&!", reply_markup=kb.menu)

	else:
		bot.send_message(message.chat.id,"У вас нет прав на использования этого бота!")













if __name__ == '__main__':
	bot.infinity_polling()
	