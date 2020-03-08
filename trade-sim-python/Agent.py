from Enums import Status
from matplotlib import pyplot as plt
import numpy as np
from random import randint
plt.style.use('seaborn-whitegrid')


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
        return "@" + str(self.name) + " B:" + str(self._bits) + " U:" + str(self.upkeep) + " " + "Sc: " + str(len(self.stocks)) + " " + str(self.status)

    def get_bits(self):
        return self._bits

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

    def buy_stock(self, market_offer):
        if self.status == Status.BANKRUPT:
            return
        self.modify_bits(-market_offer.get_price())
        if self.status == Status.BANKRUPT:
            return
        self.stocks.append(market_offer.stock)

    def play_round(self, market, companies):
        if self.status == Status.BANKRUPT:
            return
        if len(market.current_offers) > 0:
            rand = randint(0, 1000)
            if rand % 999 == 0:
                rand = randint(0, len(market.current_offers)-1)
                self.buy_stock(market.current_offers[rand])
                market.accept_offer(market.current_offers[rand], self)

    def plot_history(self):
        fig = plt.figure()
        ax = plt.axes()
        plt.title(self.name)
        x = np.array(range(0, len(self.net_worth_history)))
        ax.plot(x, np.array(self.net_worth_history))
        plt.show()

