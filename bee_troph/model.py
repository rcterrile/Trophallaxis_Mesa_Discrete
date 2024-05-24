import mesa
import numpy as np
import pandas as pd
import math
import random as rand

from .bee import Bee

import datacollectors

import globals

class TrophallaxisABM(mesa.Model):

    def __init__(self, N, fraction_of_fed_bees=10, attraction_radius=2.5, theta=180,
                solid_bounds=True, attraction_bias=True, always_random_walk=True,
                data_out=False, food_out=False,
                session_id=0, batch_id=0, run_id=0,
                a_boost=10, eps_boost=8, end_boost=8,
                width=32, height=32):
        ## Super:
        super().__init__()

        ## Initialize globals:
        globals.n3_counter = 0
        globals.n2_counter = 0
        globals.n1_counter = 0
        globals.max_transfer_t = 50
        globals.food_transfer_rate = 0.5 / globals.max_transfer_t
        globals.newvar = 0.1
        globals.var = 0.0
        globals.epsilon = 10**-eps_boost    # 10**-8

        ## init vars:
        self.N = N
        self.fraction_of_fed_bees = fraction_of_fed_bees
        self.attraction_radius = attraction_radius
        self.theta = np.deg2rad(theta)
        self.width = width
        self.height = height
        self.always_random_walk = always_random_walk

        ## End check vars:
        self.end_check = 0.0001
        self.troph_thresh = self.end_check * a_boost
        self.att_boost = a_boost
        self.end_boost = end_boost
        self.all_fed = False

        ## Scenting:

        ## Scheduler:
        self.schedule = mesa.time.RandomActivation(self)

        ## Space:
        self.space = mesa.space.ContinuousSpace(self.width, self.height, torus=(not solid_bounds))
        self.is_toroidal = not solid_bounds
        self.bee_positions = {}

        ## For analysis:
        self.output_data = data_out
        self.food_output = food_out
        self.t_i = 0

        ## Parameter sweep:
        self.data = {}
        self.food_data = {}
        self.session_id = session_id
        self.batch_id = batch_id
        self.run_id = run_id #globals.run_counter

        ## add bee agents:
        self.initiate_bees(attraction_bias)

        ## DataCollector:
        self.data_collector = mesa.DataCollector(
            model_reporters={"Fed .50": datacollectors.num_fed_50,
                             "Fed .25": datacollectors.num_fed_25,
                             "Fed .12": datacollectors.num_fed_12,
                             "Fed .05": datacollectors.num_fed_05,
                             "Fed .01": datacollectors.num_fed_01,
                             "Fed 0.0": datacollectors.num_fed_00,
                            }
        )

        ## initialize CSV output file:
        # if self.output_data:
        self.initialize_data()
    # __init__()

    def step(self):
        ## Invrement counter and reset tracker:
        self.t_i += 1
        self.all_fed = True

        ## Do agent steps:
        bee_agents = self.agents.select(lambda agent: agent.type == 0)
        for a in bee_agents:
            a.step()

        ## Collect data:
        self.data_collector.collect(self)
        # if self.output_data:
        self.write_data(self.t_i)

        ## Check stopping condition:
        globals.deltavar = np.abs(globals.newvar - globals.var)
        if self.all_fed:
            self.check_stop_condition()
        if self.t_i >= 1000:
            self.running = False
            print("- overtime -")
        #     print("----")
        #     print(np.max(self.food_data[self.t_i]))
        #     print(np.min(self.food_data[self.t_i]))
        #     print("-")
        #     print(globals.newvar)
        #     print(self.end_check * self.end_boost)
        #     print(globals.newvar < (self.end_check * self.end_boost))
        #     print(globals.deltavar)
        #     print(globals.epsilon * self.end_boost)
        #     print(globals.deltavar < (globals.epsilon * self.end_boost))
        #     print("-")
        if not self.running:
            return
    # step()

    def check_stop_condition(self):
        if globals.deltavar < globals.epsilon and globals.newvar < (self.end_check * self.end_boost):
            if self.output_data:
                self.save_data()
            if self.food_output:
                self.save_food()
            self.running = False
            # globals.run_counter += 1
            # print("----")
            # print(np.max(self.food_data[self.t_i]))
            # print(np.min(self.food_data[self.t_i]))
            # print("-")
            # print(globals.newvar)
            # print(globals.deltavar)
    # check_stop_condition()

    def initiate_bees(self, attraction_bias):
        ## find starting points:
        points = [[x,y] for x in range(1,self.width) for y in range(1,self.height)]
        rand.shuffle(points)

        ## initiate bee agents:
        for i in range(self.N):
            loc = points[i]
            b = Bee(i, self, float(loc[0]), float(loc[1]), attraction_bias)
            self.bee_positions[f'bee_{b.unique_id}'] = [b.x, b.y]
            if i < (self.N * self.fraction_of_fed_bees/100.0):
                b.make_fed()
            self.schedule.add(b)
            self.space.place_agent(b, loc)
    # initiate_bees()

    def initialize_data(self):
        xs = []
        ys = []
        food = []
        bee_agents = self.agents.select(lambda agent: agent.type == 0)
        for a in bee_agents:
            xs.append(a.pos[0])
            ys.append(a.pos[1])
            food.append(a.food)
        self.data = {
            "x_0": xs,
            "y_0": ys
        }
        self.food_data = {
            0: food
        }
    # initialize_data()

    def write_data(self, step):
        xs = []
        ys = []
        food = []
        bee_agents = self.agents.select(lambda agent: agent.type == 0)
        for a in bee_agents:
            coords = self.bee_positions[f'bee_{a.unique_id}']
            xs.append(coords[0])
            ys.append(coords[1])
            food.append(a.food)
        self.data["x_" + str(step)] = xs
        self.data["y_" + str(step)] = ys
        self.food_data[step] = food
    # write_data()

    def save_data(self):
        df = pd.DataFrame(self.data)
        path = "data_out/session_" + str(self.session_id) + "/batch_" + str(self.batch_id) + "/run_" + str(self.run_id) + ".csv"
        df.to_csv(path)
    # save_data()

    def save_food(self):
        df = pd.DataFrame(self.food_data)
        path = "data_out/session_" + str(self.session_id) + "/batch_" + str(self.batch_id) + "/food_" + str(self.run_id) + ".csv"
        df.to_csv(path)
    # save_food()

# Class TrophallaxisABM()
