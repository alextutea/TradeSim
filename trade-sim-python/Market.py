class Market:
    def __init__(self):
        self.current_offers = []
        self.offer_history = []
        self.tick_count = 0

    def __repr__(self):
        out_str = "-- MARKET --\n\n"
        for offer in self.current_offers:
            out_str += str(offer.stock.company.name) + " " + str(offer.price) + " " + str(offer.seller.name) + "\n"
        return out_str

    def submit_offer(self, stock, price, seller):
        self.current_offers.append(Offer(stock, price, seller))

    def delete_offer(self, offer):
        self.current_offers.remove(offer)

    def archive_completed_offer(self, offer):
        self.delete_offer(offer)
        self.offer_history.append(offer)

    def accept_offer(self, offer, buyer):
        offer.register_buyer(buyer)
        offer.sell_time = self.tick_count
        self.archive_completed_offer(offer)

    def tick(self):
        self.tick_count += 1



class Offer:
    def __init__(self, stock, price, seller):
        self.stock = stock
        self.price = price
        self.seller = seller
        self.buyer = None
        self.sell_time = None

    def register_buyer(self, buyer):
        self.buyer = buyer

