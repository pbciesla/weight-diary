import sqlite3
from user import User

con = sqlite3.connect('weight_saver.db')

con.row_factory = sqlite3.Row

cur = con.cursor()


def fetch_all():
    users = []
    cur.execute('SELECT * FROM users')
    for user in cur.fetchall():
        users.append(
            User(user['name'], user['height'], user['weight'], user['id']))
    return users


def fetch_by_id(user_id):
    cur.execute('SELECT * FROM users WHERE id=?', (user_id,))
    user = cur.fetchone()
    if user:
        return User(user['name'], user['height'], user['weight'], user['id'])
    else:
        return None


def fetch_by_name(user_name):
    cur.execute('SELECT * FROM users WHERE name=?', (user_name,))
    user = cur.fetchone()
    if user:
        return User(user['name'], user['height'], user['weight'], user['id'])
    else:
        return None


def save_user(user):
    user_data = (user.name, user.height, user.weight)
    cur.execute('INSERT INTO users VALUES(NULL, ?, ?, ?);', user_data)
    con.commit()


def update_user(user):
    cur.execute('UPDATE users SET weight=? WHERE id=?', (user.weight, user.id))
    con.commit()


def delete_user(user_id):
    cur.execute('DELETE FROM users WHERE id=?', (user_id,))
    con.commit()
    # cur.execute('SELECT max(id) FROM  users')  # Why its return none?!
    # max_id = cur.fetchone()
    # cur.execute('ALTER TABLE users AUTO_INCREMENT=?', (max_id,))
    # con.commit()
