import pytest
import base64

from user_storage import *
from weight_storage import save_weight
from user import User


@pytest.fixture(autouse=True)
def prepare_database_to_test():
    connection = sqlite3.connect('weight_saver.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users')
    cursor.execute('DELETE FROM sqlite_sequence where name="users"')
    connection.commit()
    cursor.execute("""INSERT INTO users (name, height, weight) 
        VALUES 
        ('Antek', 180, 75.5), 
        ('Zosia', 160, 57), 
        ('Kasia', 170, 65)""")
    connection.commit()


def test_save_user():
    test_user = User('Janek', 175, 70)
    save_user(test_user)
    user_from_database = fetch_by_name('Janek')
    assert (user_from_database.name, user_from_database.weight,
            user_from_database.height) == (
               test_user.name, test_user.weight, test_user.height)


def test_update_user():
    test_user = fetch_by_name('Zosia')
    test_user.weight = 55
    update_user(test_user)
    user_from_database = fetch_by_name('Zosia')
    assert 55 == user_from_database.weight


def test_delete_user():
    test_user = fetch_by_name('Kasia')
    delete_user(test_user.id)
    user_from_database = fetch_by_id(test_user.id)
    assert user_from_database is None
