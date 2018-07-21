import sqlite3
from datetime import date

con = sqlite3.connect('weight_saver.db')

con.row_factory = sqlite3.Row

cur = con.cursor()


def fetch_all_weight(user_id):
    weight_data = []
    cur.execute('SELECT * FROM user_weight_data WHERE user_id=?', (user_id,))
    for weight in cur.fetchall():
        weight_data.append((weight['date'], weight['value']))
    return weight_data


def fetch_weight_by_id(user_id, weight_id):
    cur.execute('SELECT * FROM user_weight_data WHERE user_id=?, id=?', (user_id, weight_id))
    weight = cur.fetchone()
    if weight:
        return weight
    else:
        return None


def fetch_weight_by_date(weight_date):
    cur.execute('SELECT * FROM user_weight_data WHERE date=?', (weight_date,))
    weight = cur.fetchone()
    if weight:
        return weight
    else:
        return None


def save_weight(weight_value, user_id):
    weight_date = date.today()
    weight = (weight_date, weight_value, user_id)
    cur.execute('INSERT INTO user_weight_data VALUES(NULL, ?, ?, ?);', weight)
    con.commit()


def delete_weight(weight_id):
    cur.execute('DELETE FROM user_weight_data WHERE id=?', (weight_id,))
    con.commit()
