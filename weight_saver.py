from user_storage import *
from weight_storage import *
from weight_chart import render_chart


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
    new_weight = float(input("Enter your weight (in kg): "))
    app_user.weight = new_weight
    save_weight(new_weight, app_user.id)
    update_user(app_user)


def set_user():
    while True:
        user_name = input("Enter your name: ")
        app_user = fetch_by_name(user_name)
        if app_user:
            return app_user
        else:
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
        print(weight['date'] + ': ' + str(weight['weight']) + ' kg')


print("Hello!")
# is_create_new_user = input("Create new user? Y/N ")
# if is_create_new_user.upper() == 'Y':
#     user = create_user()
#     save_user(user)
# else:
user = set_user()
print_weight_data(user)
# render_chart(user)
do_update = input("Do you want update your weight? Y/N ")
if do_update.upper() == 'Y':
    update_weight(user)
    print(user)

print("Thanks!")
