from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
from random import choice
import json

class TrafficModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
    """
    def __init__(self, N):

        dataDictionary = json.load(open("mapDictionary.json"))

        self.traffic_lights = []

        with open('2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)
            
            Des = []

            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)

            self.timeToChange = 10

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r_{r*self.width+c}", self, (r, c), dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col in ["S", "s"]:
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False if col == "S" else True)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == "D":
                        # Des.append((c,r))
                        agent = Destination(f"d_{r*self.width+c}", self,(r, c))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        
                        
        Des= [(3,22),(21,22),(13,20),(18,20),(4,19),(2,16),(5,16),(12,16),(18,14),(7,10),(5,4),(12,4),(19,2)]
        for i in range(10):
            car = Car(i + 1000, self, (0, 24 - i), choice(Des))
            self.grid.place_agent(car, (0, 24 - i))
            self.schedule.add(car)

        for i in range(10):
            car = Car(i + 2000, self, (1, 24 - i), choice(Des))
            self.grid.place_agent(car, (1, 24 - i))
            self.schedule.add(car)
        
        for i in range(10):
            car = Car(i + 3000, self, (22, 24 - i), choice(Des))
            self.grid.place_agent(car, (22, 24 - i))
            self.schedule.add(car)

        for i in range(10):
            car = Car(i + 4000, self, (23, 24 - i), choice(Des))
            self.grid.place_agent(car, (23, 24 - i))
            self.schedule.add(car)

        self.num_agents = N
        self.running = True

    def step(self):
        '''Advance the model by one step.'''
        if self.schedule.steps % self.timeToChange == 0:
            for agent in self.traffic_lights:
                agent.state = not agent.state
        self.schedule.step()
