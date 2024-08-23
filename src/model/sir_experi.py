from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Define the SIR Agent
class SIRAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = "S"  # All agents start as susceptible

    def step(self):
        if self.state == "I":
            # Get neighboring agents
            neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
            for neighbor in neighbors:
                if neighbor.state == "S" and np.random.random() < self.model.infection_prob:
                    neighbor.state = "I"

            # Chance to recover
            if np.random.random() < self.model.recovery_prob:
                self.state = "R"


# Define the SIR Model
class SIRModel(Model):
    def __init__(self, width, height, density, infection_prob, recovery_prob):
        super().__init__()  # Ensure parent class initialization
        self.num_agents = int(width * height * density)
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.infection_prob = infection_prob
        self.recovery_prob = recovery_prob
        self._steps = 0  # Initialize the _steps attribute

        # Create agents
        for i in range(self.num_agents):
            agent = SIRAgent(i, self)
            self.schedule.add(agent)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        # Infect one random agent at the start
        initial_infected = self.random.choice(self.schedule.agents)
        initial_infected.state = "I"

        # Data collection
        self.datacollector = DataCollector(
            model_reporters={"Infected": lambda m: self.count_state(m, "I")}
        )

    def count_state(self, model, state):
        count = sum([1 for a in model.schedule.agents if a.state == state])
        return count

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self._steps += 1  # Increment the step counter


# Run the model
def run_model():
    width, height = 20, 20  # Grid size
    density = 0.8  # Percentage of grid occupied by agents
    infection_prob = 0.2  # Probability of infection
    recovery_prob = 0.05  # Probability of recovery

    model = SIRModel(width, height, density, infection_prob, recovery_prob)

    steps = 100
    infection_data = []

    for step in range(steps):
        model.step()
        # Save data every 30 steps (days)
        if (step + 1) % 5 == 0:
            infections = model.datacollector.get_model_vars_dataframe()["Infected"].iloc[-1]
            infection_data.append({"Day": step + 1, "Infected": infections})

    # Convert to DataFrame
    df = pd.DataFrame(infection_data)

    # Save to Excel
    df.to_excel("sir_model_infections.xlsx", index=False)

    # Plot results
    df.plot(x="Day", y="Infected", kind="line", marker='o')
    plt.title("Number of Infections Every 30 Days")
    plt.xlabel("Day")
    plt.ylabel("Infected")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    run_model()
