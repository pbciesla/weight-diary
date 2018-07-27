import sqlite3
from datetime import date

from user_storage import connect_database


def fetch_all_weight(user_id):
    con = connect_database()
    cur = con.cursor()

    weight_data = []
    cur.execute('SELECT * FROM user_weight_data WHERE user_id=?', (user_id,))
    for weight in cur.fetchall():
        weight_data.append({'id': weight['id'], 'date': weight['date'], 'value': weight['value']})
    return weight_data


def fetch_weight_by_id(user_id, weight_id):
    con = connect_database()
    cur = con.cursor()

    cur.execute('SELECT * FROM user_weight_data WHERE user_id=? and id=?',
                (user_id, weight_id))
    weight = cur.fetchone()
    if weight:
        return {'id': weight['id'], 'date': weight['date'], 'value': weight['value']}
    else:
        return None


def fetch_weight_by_date(weight_date):
    con = connect_database()
    cur = con.cursor()

    cur.execute('SELECT * FROM user_weight_data WHERE date=?', (weight_date,))
    weight = cur.fetchone()
    if weight:
        weight_data = []
        for weight in cur.fetchall():
            weight_data.append(
                {'id': weight['id'], 'date': weight['date'], 'value': weight['value']})
        return weight_data
    else:
        return None


def save_weight(weight_value, user_id):
    con = connect_database()
    cur = con.cursor()

    weight_date = date.today()
    weight = (weight_date, weight_value, user_id)
    cur.execute('INSERT INTO user_weight_data VALUES(NULL, ?, ?, ?);', weight)
    con.commit()
    cur.execute('SELECT id FROM user_weight_data WHERE value=? and date=?', (weight_value, weight_date))
    weight_id = cur.fetchone()['id']
    cur.execute('UPDATE users SET weight=? WHERE id=?', (weight_value, user_id))
    con.commit()
    return weight_id


def update_weight(user_id, weight_id, weight_value):
    con = connect_database()
    cur = con.cursor()

    cur.execute(
        'UPDATE user_weight_data SET value=? WHERE id=? and user_id=?',
        (weight_value, weight_id, user_id))
    con.commit()
    return fetch_weight_by_id(user_id, weight_id)


def delete_weight(weight_id):
    con = connect_database()
    cur = con.cursor()

    cur.execute('DELETE FROM user_weight_data WHERE id=?', (weight_id,))
    con.commit()
