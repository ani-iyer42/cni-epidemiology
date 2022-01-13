from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

from numpy import random



class InfectionAgent(Agent):
    """
    Schelling segregation agent
    """

    def __init__(self, unique_id, pos, model, infection_status):
        """
        Create a new Schelling agent.

        Args:
           unique_id: Unique identifier for the agent.
           x, y: Agent initial location.
           agent_type: Indicator for the agent's type (infected=1, uninfected=0)
        """
        
        super().__init__(unique_id, model)
        #self.model = model
        #self.unique_id = unique_id
        self.pos = pos
        self.infection_status = infection_status

    def step(self):
        # similar = 0
        # for neighbor in self.model.grid.neighbor_iter(self.pos):
        #     if neighbor.type == self.type:
        #         similar += 1

        # # If unhappy, move:
        # if similar < self.model.homophily:
        #     self.model.grid.move_to_empty(self)
        # else:
        #     self.model.happy += 1

        #Step 1: infection
        #Step 2: quarantine
        #Step 3: random movement
        if self.infection_status == 1: #infection spread
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                if neighbor.infection_status == 0 and random.binomial(n = 1, p = self.model.transmission_rate):
                    neighbor.infection_status = 1
                    self.model.infected += 1

        #quarantine
        #random movement for the next day
        #self.model.grid.move_to_empty()


class Infection(Model):
    """
    Model class for the Schelling segregation model.
    """

    def __init__(self, height=20, width=20, n_agents = 100, transmission_rate = 0.6, initial_seed = 0.1):
        """ """

        self.height = height
        self.width = width
        self.transmission_rate = transmission_rate
        self.initial_seed = initial_seed
        self.n_agents = n_agents
        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=True)

        self.infected = 0
        self.datacollector = DataCollector(
            {"infected": "infected"},  # Model-level count of happy agents
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)
        self.agents = []
        for i in range(self.n_agents):

            #x = random.randrange(0,20)
            #y = random.randrange(0,20)
            (x,y) = self.grid.find_empty()
            #if self.random.random() < self.density:
            if random.binomial(n = 1, p = self.initial_seed):
                self.infected += 1
                infection_status = 1
            else:
                infection_status = 0


            agent = InfectionAgent(i, (x, y), self, infection_status)
            self.grid.position_agent(agent, (x, y))
            try:
                self.schedule.add(agent)
            except:
                print(agent.unique_id, i)
            self.agents.append(agent)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """
        self.infected = 0  # Reset counter of happy agents
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        for agent in self.agents:
            self.grid.move_to_empty(agent)
        if self.infected == self.schedule.get_agent_count():
            self.running = False
