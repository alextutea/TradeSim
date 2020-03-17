from matplotlib import pyplot as plt
from Company import Company
import numpy as np
plt.style.use('seaborn-whitegrid')


class Market:
    def __init__(self, companies):
        self.current_offers = []
        self.offer_history = []
        self.tick_count = 0
        self.companies = companies

    def __repr__(self):
        out_str = "-- MARKET --\n\n"
        for offer in self.current_offers:
            out_str += str(offer.stock.company.name) + " " + str(offer.get_price()) + " " + str(offer.seller.name) + "\n"
        return out_str

    def submit_offer(self, stock, price, seller):
        self.current_offers.append(Offer(stock, price, seller))

    def delete_offer(self, offer):
        self.current_offers.remove(offer)

    def archive_completed_offer(self, offer):
        #print(str(offer.seller.name) + " -> " + str(offer.buyer.name) + " S:" + str(offer.stock.company.name) + " B:" + str(offer.price) +" T:" + str(offer.sell_time))
        self.delete_offer(offer)
        self.offer_history.append(offer)

    def accept_offer(self, offer, buyer):
        offer.price = offer.get_price()
        offer.register_buyer(buyer)
        offer.sell_time = self.tick_count
        self.archive_completed_offer(offer)

    def tick(self):
        self.tick_count += 1

    def plot_history(self, save_folder_path, save_file_name):
        fig = plt.figure()
        x = np.array(range(0, self.tick_count))
        ax = plt.axes()
        for company in self.companies:
            sell_times = []
            prices = []
            for completed_offer in self.offer_history:
                if completed_offer.stock.company == company:
                    sell_times.append(completed_offer.sell_time)
                    prices.append(completed_offer.get_price())
            scatter = ax.scatter(sell_times, prices, s=3, label=str(company.name))
        plt.xlim(0, self.tick_count)
        plt.legend()
        if save_folder_path is None:
            plt.show()
        else:
            plt.savefig(str(save_folder_path) + "/" + str(save_file_name) + "_market_sales.png")

class Offer:
    def __init__(self, stock, price, seller):
        self.stock = stock
        self.price = price
        self.seller = seller
        self.buyer = None
        self.sell_time = None

    def register_buyer(self, buyer):
        self.buyer = buyer

    def get_price(self):
        if isinstance(self.seller, Company) and self.buyer is None:
            return self.seller.get_worth()/1000.0
        else:
            return self.price

