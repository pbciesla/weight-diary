from user_storage import *
from weight_storage import *


def create_user():
    while True:
        name = input("What's your name? ")
        if is_available(name):
            height = float(input("Enter your height (in cm): "))
            weight = float(input("Enter your weight (in kg): "))
            return User(name, height, weight)
        else:
            print("Name is not available. Try again.")


def update_weight(app_user):
    app_user.update_weight()
    update(app_user)


def set_user():
    while True:
        user_name = input("Enter your name: ")
        app_user = fetch_by_name(user_name)
        if app_user:
            return app_user
        else:
            # is_create = input("This user is not exist. Do you want create new user (press C) or try again (press A)?")
            # if is_create.upper() == 'C':
            #     create_user()
            print("This user is not exist. Try again.")


def is_available(user_name):
    if fetch_by_name(user_name):
        return False
    else:
        return True


def print_users():
    users = fetch_all()
    for app_user in users:
        print(app_user)


def print_weight_data(app_user):
    weight_data = fetch_all_weight(app_user.id)
    for weight in weight_data:
        print(weight[0] + ': ' + str(weight[1]) + ' kg')


print("Hello!")
is_create_new_user = input("Create new user? Y/N ")
if is_create_new_user.upper() == 'Y':
    user = create_user()
    save(user)
else:
    user = set_user()
    print_weight_data(user)
    do_update = input("Do you want update your weight? Y/N ")
    if do_update.upper() == 'Y':
        update_weight(user)
        print(user)

print("Thanks!")
