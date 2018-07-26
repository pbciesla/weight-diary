from weight_storage import save_weight


class User:
    def __init__(self, name, height, weight, user_id=None):
        self.name = name
        self.height = height
        self.weight = weight
        if user_id:
            self.id = user_id

    def __str__(self):
        return self.name + ', ' + str(self.height) + ' cm, ' + str(
            self.weight) + ' kg, ' + 'id: ' + str(self.id)
