from Market import Market

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
        while self.round_limit == 0 or round_count <= self.round_limit:
            print("ROUND " + str(round_count))
            for company in self.companies:
                company.modify_worth(company.progress_function(upkeep_count))
                company.worth_history.append(company._worth)
            for agent in self.agents:
                agent.play_round(self.market, self.companies)
            if self.rounds_per_stock_revenue != 0 and round_count % self.rounds_per_stock_revenue == 0:
                for agent in self.agents:
                    agent.receive_stock_revenue()
                print("STOCK REVENUE PHASE")
            if self.rounds_per_upkeep != 0 and round_count % self.rounds_per_upkeep == 0:
                for agent in self.agents:
                    agent.do_upkeep()
                    agent.net_worth_history.append(agent._bits)
                upkeep_count += 1
                print("UPKEEP " + str(upkeep_count))
            round_count += 1
        for agent in self.agents:
            print(agent)
        for company in self.companies:
            print(company)