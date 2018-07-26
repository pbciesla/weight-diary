import pygal

from weight_storage import fetch_all_weight


def prepare_data(app_user):
    weight_data = fetch_all_weight(app_user.id)
    weight_values = []
    weight_date = []
    for weight in weight_data:
        weight_values.append(weight[1])
        weight_date.append(weight[0])
    return weight_date, weight_values


def render_chart(app_user):
    weight_date, weight_values = prepare_data(app_user)
    weight_chart = pygal.Line(x_label_rotation=20)
    weight_chart.x_labels = weight_date
    weight_chart.add("Weight [kg]", weight_values)
    weight_chart.render_to_file('weight_chart.svg')
