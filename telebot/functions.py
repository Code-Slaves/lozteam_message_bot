import sqlite3
import telebot
import config
from config import db, TOKEN

def first_join(user_id, username, balance_, _btc_, _eth_, _busd_, _sol_,_usdc_,_usdt_, _bnb_):
    connection = sqlite3.connect(db)
    q = connection.cursor()
    q = q.execute('SELECT * FROM users WHERE user_id IS '+str(user_id))
    row = q.fetchone()
    if row is None:
        q.execute("INSERT INTO users (user_id,  nick, balance, btc, eth, busd, sol,usdc,usdt,bnb) VALUES ('%s', '%s','%s','%s', '%s','%s','%s', '%s','%s','%s')"%(user_id,username,balance_,_btc_, _eth_, _busd_, _sol_,_usdc_,_usdt_,_bnb_))
        connection.commit()
    connection.close()


def stats():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT user_id FROM users').fetchone()
    amount_user_all = 0
    while row is not None:
        amount_user_all += 1
        row = cursor.fetchone()
    msg = ' Информация:\n\n Пользователей в боте - ' + str(amount_user_all)
    return msg
    conn.close()
