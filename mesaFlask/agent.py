from mesa import Agent

"""

Guarda una lista con las ultimas 10 posiciones. Si la ubicación esta en esa lista, no se va allá

"""
     
class Car(Agent):
    """ 
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model, pos,destination,LastFewSteps = [] ,flag = False,lastDirection = None,parking = 0):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.parking = parking
        self.destination = destination
        self.pos = pos
        self.lastDirection = lastDirection
        self.direction = None
        self.LastFewSteps = LastFewSteps
        self.flag = flag
        self.parking = parking

    def sense(self):
        Tracks = []
        ListofNeighborNeighbors = []
        
        self.LastFewSteps.append(self.pos)
        
        coin = [1,2]
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        neighbors = self.model.grid.iter_neighbors(self.pos,moore = False, include_center=True)        
        
        if self.pos == self.destination:
            if self.parking <= 10:
                self.parking += 1
                pass
            else:
                self.parking = 0
                for neighbor in neighbors:
                   if isinstance(neighbor,Road):
                        self.direction = neighbor.direction
                        self.MoveToPlace(neighbor.pos)
                
        
        if len(self.LastFewSteps) >= 200:
            self.LastFewSteps = self.LastFewSteps[1:]
            
        # print(self.destination)
        # print(self.pos)
        

        for neighbor in neighbors:    
            ListofNeighborNeighbors = self.model.grid.iter_neighbors(neighbor.pos,moore = False, include_center=False)
            if isinstance(neighbor,Road) and neighbor.direction != self.direction and neighbor.pos not in self.LastFewSteps and neighbor not in ListofNeighborNeighbors:
                Tracks.append(neighbor)  
            if isinstance(neighbor,Destination) and neighbor.pos == self.destination:
                self.direction = "Parked"
                self.MoveToPlace(self.destination)   
                
                
            
        if len(Tracks) == 0 or self.direction == None:
            for neighbor in cellmates:
                if isinstance(neighbor, Traffic_Light):
                    if neighbor.state == True:
                        self.move()
                    else:
                        pass
                elif isinstance(neighbor, Road):
                    lastDirection = self.direction
                    self.direction = neighbor.direction
                    self.move()
            
        elif len(Tracks) == 1:   
            throw = self.random.choice(coin)
            if throw == 1 and self.flag == False and self.lastDirection != Tracks[0].direction:
                self.flag = True
                for neighbor in cellmates:
                    if isinstance(neighbor, Traffic_Light):
                        if neighbor.state == True:
                            self.lastDirection = self.direction
                            self.direction = Tracks[0].direction
                            self.MoveToPlace(Tracks[0].pos)       
                        else:
                            pass
                    elif isinstance(neighbor,Road):
                        self.lastDirection = self.direction
                        self.direction = Tracks[0].direction
                        self.MoveToPlace(Tracks[0].pos)                          
            else:
                self.flag = False
                for neighbor in cellmates:
                    if isinstance(neighbor, Traffic_Light):
                        if neighbor.state == True:
                            self.move()
                        else:
                            pass
                    elif isinstance(neighbor, Road):
                        self.lastDirection = self.direction
                        self.direction = neighbor.direction
                        self.move()  

        else:
            for neighbor in cellmates:
                if isinstance(neighbor, Traffic_Light):
                    if neighbor.state == True:
                        self.move()
                    else:
                        pass
                elif isinstance(neighbor, Road):
                    self.lastDirection = self.direction
                    self.direction = neighbor.direction
                    self.move()


    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        new_position = (0, 0)
        if self.direction == "Left":
            
            new_position = (self.pos[0] - 1, self.pos[1])
            cellmates = self.model.grid.get_cell_list_contents([new_position])    
            for neighbor in cellmates:
                if isinstance(neighbor, Car):
                    pass
                else:
                    self.model.grid.move_agent(self, new_position)                    
        elif self.direction == "Right":
            new_position = (self.pos[0] + 1, self.pos[1])
            cellmates = self.model.grid.get_cell_list_contents([new_position])   
            for neighbor in cellmates:
                if isinstance(neighbor, Car):
                    pass
                elif new_position:
                    self.model.grid.move_agent(self, new_position)                    
        elif self.direction == "Down":
            new_position = (self.pos[0], self.pos[1] - 1)
            cellmates = self.model.grid.get_cell_list_contents([new_position])   
            for neighbor in cellmates:
                if isinstance(neighbor, Car):
                    pass    
                else:
                    self.model.grid.move_agent(self, new_position)                    
        elif self.direction == "Up":
            new_position = (self.pos[0], self.pos[1] + 1)
            cellmates = self.model.grid.get_cell_list_contents([new_position])            
            for neighbor in cellmates:
                if isinstance(neighbor, Car):
                    pass
                else:
                    self.model.grid.move_agent(self, new_position)
        
    def MoveToPlace(self, new_position):
        self.model.grid.move_agent(self, new_position)

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.sense()

class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change color 
        """
        self.state = state
        self.timeToChange = timeToChange
        self.rotate = state

    def step(self):
        """ 
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
        pass

class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model,pos):
        super().__init__(unique_id, model)
        
        self.pos = pos 

    def step(self):
        pass

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """
    def __init__(self, unique_id, model, pos, direction):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.direction = direction

    def step(self):
        pass