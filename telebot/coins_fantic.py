import sqlite3
from config import db, TOKEN


def get_coin_balance(coin, user_id):
    connection = sqlite3.connect(db)
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(f'SELECT {str(coin)} FROM users WHERE user_id = {str(user_id)}')
    row = str(cursor.fetchall())
    row1 = row.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "")
    return float(row1)

def send_fantic(coin, user_id, value):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(f'UPDATE users SET {(coin)} = {str(value)} where user_id = {str(user_id)}')
    conn.commit()
    cursor.close()
