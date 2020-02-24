from Market import Market
from Stock import Stock


class Simulation:
    def __init__(self, agents, companies, rounds_per_upkeep=0, rounds_per_stock_revenue=0, round_limit=0):
        self.agents = agents
        self.companies = companies
        self.market = Market()
        self.rounds_per_upkeep = rounds_per_upkeep
        self.round_limit = round_limit
        self.rounds_per_stock_revenue = rounds_per_stock_revenue

    def start(self):
        round_count = 1
        upkeep_count = 0
        self.market.tick()
        for company in self.companies:
            for i in range(1000):
                self.market.submit_offer(Stock(company), company.get_worth()/1000.0, company)
        while self.round_limit == 0 or round_count <= self.round_limit:
            print("ROUND " + str(round_count))
            for company in self.companies:
                company.modify_worth(company.progress_function(upkeep_count))
                company.worth_history.append(company.get_worth())
            for agent in self.agents:
                agent.play_round(self.market, self.companies)
            if self.rounds_per_stock_revenue != 0 and round_count % self.rounds_per_stock_revenue == 0:
                for agent in self.agents:
                    agent.receive_stock_revenue()
                print("STOCK REVENUE PHASE")
            if self.rounds_per_upkeep != 0 and round_count % self.rounds_per_upkeep == 0:
                for agent in self.agents:
                    agent.do_upkeep()
                upkeep_count += 1
                print("UPKEEP " + str(upkeep_count))
            for agent in self.agents:
                agent.net_worth_history.append(agent.get_bits())
            round_count += 1
        print(self.market)
        for agent in self.agents:
            print(agent)
            agent.plot_history()
        for company in self.companies:
            print(company)
            company.plot_history()