class Stock:
    def __init__(self, company):
        self.company = company

    def calculate_value(self):
        return self.company.worth/1000.0

