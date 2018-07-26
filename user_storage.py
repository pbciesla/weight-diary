import sqlite3
from user import User


def connect_database():
    connection = sqlite3.connect('weight_saver.db')
    connection.row_factory = sqlite3.Row
    return connection


def fetch_all():
    con = connect_database()
    cur = con.cursor()

    users = []
    cur.execute('SELECT * FROM users')
    for user in cur.fetchall():
        users.append(
            User(user['name'], user['height'], user['weight'], user['id']))
    return users


def fetch_by_id(user_id):
    con = connect_database()
    cur = con.cursor()

    cur.execute('SELECT * FROM users WHERE id=?', (user_id,))
    user = cur.fetchone()
    if user:
        return User(user['name'], user['height'], user['weight'], user['id'])
    else:
        return None


def fetch_by_name(user_name):
    con = connect_database()
    cur = con.cursor()

    cur.execute('SELECT * FROM users WHERE name=?', (user_name,))
    user = cur.fetchone()
    if user:
        return User(user['name'], user['height'], user['weight'], user['id'])
    else:
        return None


def save_user(user):
    con = connect_database()
    cur = con.cursor()

    user_data = (user.name, user.height, user.weight)
    cur.execute('INSERT INTO users VALUES(NULL, ?, ?, ?);', user_data)
    con.commit()
    cur.execute('SELECT id FROM users WHERE name=?', (user.name,))
    user_id = cur.fetchone()['id']
    return user_id


def update_user(user):
    con = connect_database()
    cur = con.cursor()

    cur.execute('UPDATE users SET weight=?, height=? WHERE id=?',
                (user.weight, user.height, user.id))
    con.commit()
    new_user = fetch_by_id(user.id)
    return new_user



def delete_user(user_id):
    con = connect_database()
    cur = con.cursor()

    cur.execute('DELETE FROM users WHERE id=?', (user_id,))
    con.commit()
    # cur.execute('SELECT max(id) FROM  users')  # Why its return none?!
    # max_id = cur.fetchone()
    # cur.execute('ALTER TABLE users AUTO_INCREMENT=?', (max_id,))
    # con.commit()
