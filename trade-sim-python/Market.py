class Market:
    def __init__(self):
        self.current_offers = []
        self.offer_history = []

    def submit_offer(self, stock, price, seller):
        self.current_offers.append(Offer(stock, price, seller))

    def delete_offer(self, offer):
        self.current_offers.remove(offer)

    def archive_completed_offer(self, offer):
        self.delete_offer(offer)
        self.offer_history.append(offer)

    def accept_offer(self, offer, buyer):
        offer.register_buyer(buyer)
        self.archive_completed_offer(offer)


class Offer:
    def __init__(self, stock, price, seller):
        self.stock = stock
        self.price = price
        self.seller = seller
        self.buyer = None

    def register_buyer(self, buyer):
        self.buyer = buyer

