from random import randint
from Enums import Status


class Company:
    def __init__(self, name="unnamed company", starting_worth=1000, progress_function=0):
        self.name = name
        self.starting_worth = starting_worth
        self.worth_history = [starting_worth]
        self._worth = starting_worth
        if progress_function == 0:
            progress_function = default_progress_function
        self.progress_function = progress_function
        self.status = Status.ACTIVE
        if self._worth <= 0:
            self.status = Status.BANKRUPT

    def __repr__(self):
        return "Name: " + str(self.name) + " B:" + str(self._worth) + " " + str(self.status)

    def modify_worth(self, modifier):
        if self.status == Status.BANKRUPT:
            return
        self._worth += modifier
        if self._worth <= 0:
            self.status = Status.BANKRUPT


def default_progress_function(upkeeps_passed):
    modifier = 100 if upkeeps_passed < 300 else -100
    random_factor = randint(-10, 10)
    return modifier + random_factor
