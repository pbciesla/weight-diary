class User:
    def __init__(self, name, height, weight, user_id=None):
        self.name = name
        self.height = height
        self.weight = weight
        if user_id:
            self.id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'height': self.height,
            'weight': self.weight,
        }
