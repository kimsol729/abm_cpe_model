#%%
import mesa
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import batch_run
from mesa.batchrunner import BatchRunner

import numpy as np
#%%
# SIR Model Implementation
class SIRModel(Model):
    def __init__(self, N, width, height, infection_rate, recovery_rate):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.infection_rate = infection_rate
        self.recovery_rate = recovery_rate
        self.running = True
        # Create agents
        for i in range(self.num_agents):
            a = SIRAgent(i, self)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            {"Susceptible": lambda m: self.count_state(m, "S"),
             "Infected": lambda m: self.count_state(m, "I"),
             "Recovered": lambda m: self.count_state(m, "R")}
        )

    def count_state(self, model, state):
        count = 0
        for agent in model.schedule.agents:
            if agent.state == state:
                count += 1
        return count

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

class SIRAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = "S"  # All agents start as Susceptible

    def step(self):
        if self.state == "I":
            if self.random.random() < self.model.recovery_rate:
                self.state = "R"
            else:
                neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
                for neighbor in neighbors:
                    if neighbor.state == "S":
                        if self.random.random() < self.model.infection_rate:
                            neighbor.state = "I"

# Parameters to vary in batch run
parameters = {
    "N": 100,
    "width": 10,
    "height": 10,
    "infection_rate": [0.05, 0.1, 0.2],
    "recovery_rate": [0.02, 0.05, 0.1],
}

# Execute the batch run
batch_results = BatchRunner(
    SIRModel,
    parameters=parameters,
    iterations=50,  # Number of iterations per parameter combination
    max_steps=100,  # Max steps per run
    number_processes=1,  # Use all available CPUs
    # data_collection_period=1,  # Collect data at every step
    display_progress=True
)

# Convert batch results to a DataFrame for analysis
import pandas as pd

df = pd.DataFrame(batch_results)
print(df.head())  # Display the first few rows of the results


# %%
