import mesa

class Heading(mesa.Agent):
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.color = 3
        self.agent_size = 1

    def step(self):
        pass
