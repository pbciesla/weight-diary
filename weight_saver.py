from user_storage import *


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
    user_name = input("Enter your name: ")
    return fetch_by_name(user_name)


def is_available(user_name):
    if fetch_by_name(user_name):
        return False
    else:
        return True


def print_users():
    users = fetch_all()
    for app_user in users:
        print(app_user)


print("Hello!")
is_create_new_user = input("Create new user? Y/N ")
if is_create_new_user.upper() == 'Y':
    user = create_user()
    save(user)
else:
    user = set_user()
    do_update = input("Do you want update your weight? Y/N ")
    if do_update.upper() == 'Y':
        update_weight(user)
        print(user)

print("Thanks!")
