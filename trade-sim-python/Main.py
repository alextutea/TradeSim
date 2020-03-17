from Agent import Agent
from Company import Company
from Simulation import Simulation
from random import randint

def main():
    agents = [
        Agent("Agent1", 100000, None, 5),
        Agent("Agent2", 200000, None, 10),
        Agent("Agent3", 60000, None, 1),
        Agent("Agent4", 100000, None, 100)
    ]
    companies = [
        Company("Gogl", 3000000),
        Company("Msft", 2000000),
        Company("Tesl", 100000, custom_progress_function)
    ]
    sim = Simulation(agents, companies, 24, 24*365, 24*365*25, "./test_save_folder2", "test_save1")
    sim.start()

def custom_progress_function(upkeeps_passed):
    modifier = 1000 if upkeeps_passed < 100 else (-100 if upkeeps_passed<300 else (100 if upkeeps_passed<800 else (-10 if upkeeps_passed < 1800 else -100)))
    random_factor = randint(-7000, 7000)
    return modifier+random_factor

if __name__ == "__main__":
    main()
