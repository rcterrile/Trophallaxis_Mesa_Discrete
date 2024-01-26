import mesa
import numpy as np
import math
from sklearn.preprocessing import normalize
import random as rand

import globals

import warnings

class Bee(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)          # inherit attributes from super class
        # self.x = x  # possibly unecessary
        # self.y = y  # possibly unecessary
        self.old_xcor = -1
        self.old_ycor = -1
        self.hind = rand.randrange(4)
        self.heading = globals.possible_headings[self.hind] #rand.Uniform(0,2pi)      # store agents heading
        self.initial_pos = (-1,-1)                # store initial position of agent
        self.hungry = True                  # is the agent hungry? (initally true for all)
        self.occupied = False
        self.food = 0                       # store how much food agent has
        self.counts = 0

        self.delta_t = 0
        self.nearby_agents = []
        self.dist_to_neighbors = None
        self.blockers = None
        self.dist_to_blocks = None
        self.rol_blocks = None

        self.wrong = False
        self.zero = False
        self.small = False
        self.ok = False
        self.clusterID = 0
        self.nearestCluster = []
        # for food exchange:
        self.times = 0
        # for plotting:
        self.color = 0
        self.agent_size = model.agent_size

        # collision helpers:
        self.nearest_neighbor = None
        self.zero_hold = False
        self.small_dist = -1
        self.zero_neighbors = []
        self.mturn = -1

    def step(self):     # scheduler runs this function for each time step
        self.old_xcor = self.pos[0]
        self.old_ycor = self.pos[1]

        self.wrong = False
        self.color = 0
        self.zero = False
        self.small = False
        self.ok = False
        self.zero_hold = False      # error helper
        self.small_dist = -1
        self.mturn += 1         # collision helper
        if self.occupied:
            if self.counts > 0:
                self.counts -= 1
            else:
                self.occupied = False
                self.attempt_move()
        else: # occupied = false
            self.getNeighbors(1)
            if len(self.nearby_agents) > 0:
                self.getDistToNeighbors()

                target = self.nearby_agents[np.argmin(self.dist_to_neighbors)]     # set target as nearest agent
                if rand.random() > 0.8:
                    target = rand.choice(self.nearby_agents)

                if target:
                    # global n3_counter
                    globals.n3_counter += 1
                    if not target.occupied:
                        # global n2_counter
                        globals.n2_counter += 1
                        globals.delta_food = (self.food - target.food)
                        if globals.delta_food != 0:
                            # global n1_counter
                            globals.n1_counter += 1
                        if globals.delta_food > 0:
                            # global tro_counter
                            globals.tro_counter += 1
                            self.occupied = True
                            self.delta_t = np.round((globals.delta_food / 2) / globals.food_transfer_rate)
                            self.counts = self.delta_t
                            self.exchange_food(target)
                        else:
                            self.attempt_move()
                    else:
                        self.attempt_move()
                else:
                    self.attempt_move()
            else:
                self.attempt_move()
        # n_count = ...
        # u_counter = ...
        # hungry_left = ...
        # nn = self.model.space.get_neighbors(self.pos, radius=1.0)
        # nn = self.getImmediateNeighbors()
        # if len(nn) > 0:     # check if any other agents are (dist < 1) away, and undo move if true
        #     print("=== === === === === === === ===")
        #     print(self.pos)
        #     print("(" + str(self.old_xcor) + "," + str(self.old_ycor) +")")
        #     ct = 0
        #     for a in nn:
        #         print(str(ct) + " - " + str(a.pos))
        #         ct += 1
        #     self.model.grid.move_agent(self, [self.old_xcor, self.old_ycor])
        #     self.model.undone += 1
        #     if self.small:
        #         self.model.smallUndone += 1
        #     if not self.zero:
        #         self.model.zeroUndone += 1
        #     # self.zero = True

    ###########################
    ## Functions for Moving: ##
    ###########################

    def attempt_move(self):
        # update heading:
        self.check_attraction()
        # rv = rand.randrange(3)
        # if rv == 0:
        #     self.rotateCW()
        # elif rv == 1:
        #     self.rotateCCW()
        # else:
        #     pass
        # self.updateHeading()     # add deviation to heading in range (+/- pi)
        # check for blockers:
        # self.getNeighbors(2)
        neighborhood = self.model.grid.get_neighborhood(self.pos, False)
        open_moves = []
        for m in neighborhood:
            open_moves.append(self.model.grid.is_cell_empty(m))
        if np.sum(open_moves) < 1:
            self.zero = True
            return
        possible_moves = [neighborhood[i] for i, x in enumerate(open_moves) if x]
        self.move_to_open(possible_moves)
        # i = 0
        # while i < len(possible_moves):
        #     if not self.model.grid.is_cell_empty(possible_moves[i]):
        #         possible_moves.pop(i)
        #     else:
        #         i += 1
        # if len(possible_moves) < 1:
        #     # Cant move
        #     return
        # self.forward(possible_moves)      # will need to update so agents go to targets
    # attempt_move()

    def setHeading(self, hd):   # hd = heading in radians
        self.hind = hd
        self.heading = globals.possible_headings[self.hind]

    def rotateCW(self):        # add noise to heading
        if self.hind == 3:
            self.hind = 0
        else:
            self.hind += 1
        self.heading = globals.possible_headings[self.hind]

    def rotateCCW(self):        # add noise to heading
        if self.hind == 0:
            self.hind = 3
        else:
            self.hind -= 1
        self.heading = globals.possible_headings[self.hind]

    def move_to_open(self, pos_mvs):
        # Move to random position from provided coordinate list
        if len(pos_mvs) < 1:
            return
        elif len(pos_mvs) == 1:
            self.model.grid.move_agent(self, pos_mvs[0])
        else:
            self.model.grid.move_agent_to_one_of(self, pos_mvs)

    def forward(self, pos_mvs):    # helper function for movement
        # move to new position
        new_position = (self.pos[0] + self.heading[0], self.pos[1] + self.heading[1])       # Calculate new position
        if not self.model.grid.out_of_bounds(new_position) and self.model.grid.is_cell_empty(new_position):
            self.model.grid.move_agent(self, new_position)         # set new position
        else:
            if len(pos_mvs) == 1:
                self.model.grid.move_agent(self, pos_mvs)
            else:
                self.model.grid.move_agent_to_one_of(self, pos_mvs)
    # forward()

    ###########################
    ##  Collision Handling:  ##
    ###########################

    def check_blockers(self):       # essentially the same as in netlogo code
        self.dist_to_blocks = []
        for b in self.blockers:
            if b.unique_id == self.unique_id:   # error check
                print("BAD")
            self.dist_to_blocks.append(self.get_distance_to_point(b.pos))
            if self.dist_to_blocks[-1] > 0 and self.dist_to_blocks[-1] <= 0.9:
                self.wrong = True       # error
            elif self.dist_to_blocks[-1] <= 1.1 and self.dist_to_blocks[-1] > 0.9:
                self.zero = True        # need to find new direction
                self.zero_neighbors.append(b)
            elif self.dist_to_blocks[-1] > 1.1 and self.dist_to_blocks[-1] <= 2:
                self.small = True       # should take a small step
            elif self.dist_to_blocks[-1] > 2:
                self.ok = True          # can move one whole step
    # check_blockers()

    ##############################
    ##  Relation to Neighbors:  ##
    ##############################

    def getNeighbors(self, r):     # helper
        ## Gets nearby agents using Mesa's built in method
        #  - returns agents in diagonal spaces from current agent
        self.nearby_agents = self.model.grid.get_neighbors(self.pos, True, False, r)  # use mesa function to get agents within radius

    def getDistToNeighbors(self):       # Gets distance to all agents in nearby_agents list
        self.dist_to_neighbors = []
        if len(self.nearby_agents) > 0:
            for n in self.nearby_agents:
                tmp = self.get_distance_to_point(n.pos)
                self.dist_to_neighbors.append(tmp)

    ##############################
    ##  Relationship to Point:  ##
    ##############################

    # def get_heading_to_point(self, tup):
    #     h = math.atan2(tup[1] - self.pos[1], tup[0] - self.pos[0])
    #     h2 = self.model.space.get_heading(self.pos, tup)
    #     h2 = math.atan2(h2[0], h2[1])
    #     if h != h2:
    #         return self.normalizeHeading(h2)
    #     # return self.normalizeHeading(math.atan2(tup[1] - self.pos[1], tup[0] - self.pos[0]))
    #     return self.normalizeHeading(h)

    def get_distance_to_point(self, tup):   # helper
        # returns the manhatten distance between points
        return np.abs(self.pos[0] - tup[0]) + np.abs(self.pos[1] - tup[1])

    ###############################
    ##  BEE Specific Functions:  ##
    ###############################

    def makeFed(self):
        self.food = 1
        self.hungry = False

    def check_attraction(self):     # find any agents within attraction range
        self.getNeighbors(self.model.attraction_radius)
        self.getDistToNeighbors()
        if len(self.nearby_agents) < 1 or np.max(self.dist_to_neighbors) == 1:
            return False
        inds = [i for i in range(len(self.nearby_agents))]
        rand.shuffle(inds)
        i = 0
        while self.dist_to_neighbors[i] < 2:
            i += 1
            if i == len(self.nearby_agents):
                return False
        dx = self.nearby_agents[i].pos[0] - self.pos[0]
        dy = self.nearby_agents[i].pos[1] - self.pos[1]
        if np.abs(dx) <= np.abs(dy):
            if dy < 0:
                self.heading = [0, -1]
            else:
                self.heading = [0, 1]
        else:
            if dx < 0:
                self.heading = [-1, 0]
            else:
                self.heading = [1, 0]
        return True
    # check_attraction()

    def exchange_food(self, target):
        globals.donor_list.append(self.unique_id)
        globals.foods_list.append(globals.delta_food)
        globals.xcor_list.append(self.pos[0])
        globals.ycor_list.append(self.pos[1])

        # show target
        transfer_amount = globals.delta_food / 2
        self.times += 1
        self.food -= transfer_amount
        self.hungry = False

        # update target's attributes:
        target.occupied = True
        target.hungry = False
        globals.target_list.append(target.unique_id)

        target.food += transfer_amount
        target.counts = self.delta_t
        target.times += 1

        self.update_variance()   # need to update variances after each food exchange
    # exchange_food

    def update_variance(self):
        # update value of variances only if food exchange happens:
        globals.var = globals.newvar
        bee_vars = []
        for a in self.model.schedule.agents:
            bee_vars.append(a.food)
        globals.newvar = np.var(bee_vars)
    # update_variance

# class Bee
