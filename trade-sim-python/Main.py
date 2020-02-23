from Agent import Agent
from Company import Company
from Simulation import Simulation


if __name__ == "__main__":
    agents = [
        Agent("Gica", 100000, None, 5)
    ]
    companies = [
        Company("Gogl", 3000000),
        Company("Tesl", 2000000)
    ]
    sim = Simulation(agents, companies, 24, 24*365, 100000)
    sim.start()