import pytest
import base64

from app import *
from user_storage import *
from user import User


@pytest.fixture(autouse=True)
def prepare_database_to_test():
    connection = sqlite3.connect('weight_saver.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users')
    cursor.execute('DELETE FROM sqlite_sequence where name="users"')
    cursor.execute('DELETE FROM user_weight_data')
    cursor.execute('DELETE FROM sqlite_sequence where name="user_weight_data"')
    connection.commit()
    cursor.execute("""INSERT INTO users (name, height, weight) 
        VALUES 
        ('Antek', 180, 75.5), 
        ('Zosia', 160, 57), 
        ('Kasia', 170, 65)""")
    connection.commit()
    cursor.execute("""INSERT INTO user_weight_data (date, value, user_id)
        VALUES
        ('2018-01-01', 84, 1),
        ('2018-02-01', 82, 1),
        ('2018-03-01', 88, 1),
        ('2018-04-01', 75.5, 1),
        ('2018-05-01', 60, 2),
        ('2018-06-03', 58, 2),
        ('2018-07-02', 57, 2) """)
    connection.commit()


def test_save_user():
    # when
    test_user = User('Janek', 175, 70)
    save_user(test_user)
    # then
    user_from_database = fetch_by_name('Janek')
    assert (user_from_database.name, user_from_database.weight,
            user_from_database.height) == (
               test_user.name, test_user.weight, test_user.height)


def test_update_user():
    # when
    test_user = fetch_by_name('Zosia')
    test_user.weight = 55
    update_user(test_user)
    # then
    user_from_database = fetch_by_name('Zosia')
    assert 55 == user_from_database.weight


def test_delete_user():
    # when
    test_user = fetch_by_name('Kasia')
    delete_user(test_user.id)
    # then
    user_from_database = fetch_by_id(test_user.id)
    assert user_from_database is None


def test_get_weight_endpoint_should_return_200_status_code():
    # when
    response = app.test_client().get('/1/weight')
    # then
    assert 200 == response.status_code


def test_get_weight_endpoint_should_return_json():
    # when
    response = app.test_client().get('/1/weight')
    # then
    assert response.is_json


def test_get_weight_endpoint_should_return_four_objects():
    # when
    response = app.test_client().get('/1/weight')
    weight = response.get_json()
    # then
    assert 4 == len(weight)


def test_when_user_not_exist_get_weight_endpoint_should_return_404_error():
    # when
    response = app.test_client().get('/55/weight')
    # then
    assert 404 == response.status_code


def test_add_actual_weight_endpoint_should_return_200_status_code():
    # when
    response = app.test_client().post('/2/weight',
                                      data='{"value": 55}',
                                      content_type='application/json')
    # then
    assert 200 == response.status_code


def test_add_actual_weight_endpoint_should_return_json():
    # when
    response = app.test_client().post('/2/weight',
                                      data='{"value": 55}',
                                      content_type='application/json')
    # then
    assert response.is_json


def test_add_actual_weight_endpoint_should_return_new_weight():
    # when
    response = app.test_client().post('/2/weight',
                                      data='{"value": 55}',
                                      content_type='application/json')
    # then
    assert 55 == response.get_json()['value']


def test_add_actual_weight_endpoint_should_update_user_weight():
    # when
    response = app.test_client().post('/2/weight',
                                      data='{"value": 55}',
                                      content_type='application/json')
    # then
    user = fetch_by_id(2)
    assert 55 == user.weight


def test_when_user_not_exist_add_actual_weight_endpoint_should_return_404_error():
    # when
    response = app.test_client().post('/55/weight',
                                      data='{"value": 55}',
                                      content_type='application/json')
    # then
    assert 404 == response.status_code


def test_update_weight_by_id_endpoint_should_return_200_status_code():
    # when
    response = app.test_client().put('/2/weight/5',
                                     data='{"value": 61}',
                                     content_type='application/json')
    # then
    assert 200 == response.status_code


def test_update_weight_by_id_endpoint_should_return_json():
    # when
    response = app.test_client().put('/2/weight/5',
                                     data='{"value": 61}',
                                     content_type='application/json')
    # then
    assert response.is_json


def test_update_weight_by_id_endpoint_should_update_weight():
    # when
    response = app.test_client().put('/2/weight/5',
                                     data='{"value": 61}',
                                     content_type='application/json')
    # then
    assert 61 == response.get_json()['value']


def test_when_user_not_exist_update_weight_by_id_endpoint_should_return_return_404_error():
    # when
    response = app.test_client().put('/55/weight/5',
                                     data='{"value": 55}',
                                     content_type='application/json')
    # then
    assert 404 == response.status_code


def test_when_weight_id_not_exist_update_weight_by_id_endpoint_should_return_return_404_error():
    # when
    response = app.test_client().put('/2/weight/55',
                                     data='{"value": 55}',
                                     content_type='application/json')
    # then
    assert 404 == response.status_code


def test_delete_weight_by_id_endpoint_should_return_200_status_code():
    # when
    response = app.test_client().delete('/2/weight/5')
    # then
    assert 200 == response.status_code


def test_delete_weight_by_id_endpoint_should_delete_weight():
    # when
    app.test_client().delete('/2/weight/5')
    # then
    weight = fetch_weight_by_id(2, 5)
    assert weight is None


def test_when_user_not_exist_delete_weight_by_id_endpoint_should_return_return_404_error():
    # when
    response = app.test_client().delete('/22/weight/5')
    # then
    assert 404 == response.status_code


def test_when_weight_id_not_exist_delete_weight_by_id_endpoint_should_return_return_404_error():
    # when
    response = app.test_client().delete('/2/weight/55')
    # then
    assert 404 == response.status_code


def test_create_user_endpoint_should_return_200_status_code():
    # when
    response = app.test_client().post('/users',
                                      data='{"name": "Franek", "height": 189, "weight": 94}',
                                      content_type='application/json')
    # then
    assert 200 == response.status_code


def test_create_user_weight_endpoint_should_return_json():
    # when
    response = app.test_client().post('/users',
                                      data='{"name": "Franek", "height": 189, "weight": 94}',
                                      content_type='application/json')
    # then
    assert response.is_json


def test_create_user_weight_endpoint_should_return_new_user():
    # when
    response = app.test_client().post('/users',
                                      data='{"name": "Franek", "height": 189, "weight": 94.5}',
                                      content_type='application/json')
    # then
    assert ('Franek', 189, 94.5) == (
        response.get_json()['name'], response.get_json()['height'],
        response.get_json()['weight'])


def test_update_user_by_id_endpoint_should_return_200_status_code():
    # when
    response = app.test_client().put('/users/3',
                                     data='{"weight": 64}',
                                     content_type='application/json')
    # then
    assert 200 == response.status_code


def test_update_user_by_id_endpoint_should_return_json():
    # when
    response = app.test_client().put('/users/3',
                                     data='{"weight": 64}',
                                     content_type='application/json')
    # then
    assert response.is_json


def test_update_user_by_id_endpoint_should_update_weight():
    # when
    response = app.test_client().put('/users/3',
                                     data='{"weight": 64}',
                                     content_type='application/json')
    # then
    assert 64 == response.get_json()['weight']


def test_when_user_not_exist_update_user_by_id_endpoint_should_return_return_404_error():
    # when
    response = app.test_client().put('/users/44',
                                     data='{"weight": 64}',
                                     content_type='application/json')
    # then
    assert 404 == response.status_code


def test_delete_weight_by_id_endpoint_should_return_200_status_code():
    # when
    response = app.test_client().delete('/users/3')
    # then
    assert 200 == response.status_code


def test_delete_user_by_id_endpoint_should_delete_user():
    # when
    app.test_client().delete('/users/3')
    # then
    user = fetch_by_id(3)
    assert user is None


def test_when_user_not_exist_delete_user_by_id_endpoint_should_return_return_404_error():
    # when
    response = app.test_client().delete('/users/33')
    # then
    assert 404 == response.status_code
