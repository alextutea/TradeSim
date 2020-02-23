from Enums import Status


class Agent:
    def __init__(self, name="unnamed agent", starting_bits=0, starting_stocks=None, upkeep=0):
        if starting_stocks is None:
            starting_stocks = []
        self.stocks = starting_stocks
        self.starting_bits = starting_bits
        self._bits = starting_bits
        self.upkeep = upkeep
        self.status = Status.ACTIVE
        self.name = name
        self.net_worth_history = [starting_bits]

    def __repr__(self):
        return "@" + str(self.name) + " B:" + str(self._bits) + " U:" + str(self.upkeep) + " " + str(self.status)

    def modify_bits(self, modifier):
        if self.status == Status.BANKRUPT:
            return
        self._bits += modifier
        if self._bits <= 0:
            self.status = Status.BANKRUPT

    def receive_stock_revenue(self):
        if self.status == Status.BANKRUPT:
            return
        for stock in self.stocks:
            self.modify_bits(stock.calculate_value())

    def do_upkeep(self):
        if self.status == Status.BANKRUPT:
            return
        self.modify_bits(-self.upkeep)

    def play_round(self, market, companies):
        pass
