from Market import Market
from Stock import Stock
from Enums import Status
from Company import Company
import time, sys
from matplotlib import pyplot as plt
import numpy as np
import os

class Simulation:
    def __init__(self, agents, companies, rounds_per_upkeep=0, rounds_per_stock_revenue=0, round_limit=0, save_folder_path=None, save_file_name='SavedSimulation'):
        self.agents = agents
        self.companies = companies
        self.market = Market(companies)
        self.rounds_per_upkeep = rounds_per_upkeep
        self.round_limit = round_limit
        self.rounds_per_stock_revenue = rounds_per_stock_revenue
        self.save_folder_path = save_folder_path
        self.save_file_name = save_file_name
        os.makedirs(save_folder_path, exist_ok=True)

    def start(self):
        round_count = 1
        upkeep_count = 0
        self._submit_initial_stocks()
        while self.round_limit == 0 or round_count <= self.round_limit:
            self.market.tick()
            self._update_companies_worth(round_count, upkeep_count)
            self._agent_actions()
            self._manage_awarding_stock_revenue(round_count, upkeep_count)
            self._apply_upkeep_costs(round_count, upkeep_count)
            if self.rounds_per_upkeep != 0 and round_count % self.rounds_per_upkeep == 0:
                upkeep_count += 1
            self._archive_agent_worths(round_count, upkeep_count)
            round_count += 1
        self._show_results()
    
    def _update_companies_worth(self, round_count, upkeep_count):
        for company in self.companies:
            company.modify_worth(company.progress_function(upkeep_count))
            company.worth_history.append(company.get_worth())
            if company.status == Status.BANKRUPT:
                for offer in self.market.current_offers:
                    if offer.stock.company == company:
                        self.market.current_offers.remove(offer)
                for agent in self.agents:
                    for stock in agent.stocks:
                        if stock.company == company:
                            agent.stocks.remove(stock)
    
    def _submit_initial_stocks(self):
        for company in self.companies:
            for i in range(1000):
                self.market.submit_offer(Stock(company), company.get_worth()/1000.0, company)
    
    def _agent_actions(self):
        for agent in self.agents:
            agent.play_round(self.market, self.companies)

    def _manage_awarding_stock_revenue(self, round_count, upkeep_count):
        if self.rounds_per_stock_revenue != 0 and round_count % self.rounds_per_stock_revenue == 0:
            for agent in self.agents:
                agent.receive_stock_revenue()
    
    def _apply_upkeep_costs(self, round_count, upkeep_count):
        if self.rounds_per_upkeep != 0 and round_count % self.rounds_per_upkeep == 0:
            for agent in self.agents:
                agent.do_upkeep()
            update_progress(round_count/self.round_limit*1.0)
    
    def _archive_agent_worths(self, round_count, upkeep_count):
        for agent in self.agents:
            agent.net_worth_history.append(agent.get_bits())
    
    def _show_results(self):
        print(self.market)
        self.market.plot_history(self.save_folder_path, self.save_file_name)
        for company in self.companies:
            print(company)
            company.plot_history(self.save_folder_path, self.save_file_name)
        fig = plt.figure()
        max = 0
        for agent in self.agents:
            print(agent)
            agent.plot_history(self.save_folder_path, self.save_file_name)
            if max < len(agent.net_worth_history):
                max = len(agent.net_worth_history)
        x = np.array(range(0, max))
        for agent in self.agents:
            plt.plot(x, np.array(agent.net_worth_history), label=str(agent.name))
        plt.title("Agents")
        plt.legend()
        if self.save_folder_path is None:
            plt.show()
        else:
            plt.savefig(str(self.save_folder_path) + "/" + str(self.save_file_name) + "_agents.png")



def update_progress(progress):
    barLength = 50 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rSimulation progress: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()