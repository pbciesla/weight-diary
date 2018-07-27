class User:
    def __init__(self, name, height, weight, user_id=None):
        self.name = name
        self.height = height
        self.weight = weight
        if user_id:
            self.id = user_id

    def calculate_bmi(self):
        height_in_meters = self.height / 100
        bmi = self.weight / (height_in_meters ** 2)
        if bmi < 18.5:
            bmi_meaning = 'underweight'
        elif bmi < 25:
            bmi_meaning = 'norm'
        elif bmi < 30:
            bmi_meaning = 'overweight'
        else:
            bmi_meaning = 'obesity'
        return "{0:.2f}".format(bmi) + ': ' + bmi_meaning

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'height': self.height,
            'weight': self.weight,
        }
