import mesa
import numpy as np
import math
import random as rand
# import scipy.cluster.hierarchy as hcluster      # hierarchical clustering
import scipy.stats as stats
# from sklearn.cluster import OPTICS                  # DBSCAN clustering
# import hdbscan                  # HDBSCAN clustering

from .bee import Bee
from .cluster import Cluster        # WIP - to visualize clusters better
# from .heading import Heading        # WIP

import globals

class TrophallaxisABM(mesa.Model):
    # model class to manage hungry and fed bees for an agent based model simulating trophallaxis behavior

    def __init__(self, N, fraction_of_fed_bees=10, attraction_radius=2.5, theta=45, width=32, height=32):
        self.x_min = 0
        self.x_max = 32
        self.y_min = 0
        self.y_max = 32
        # initialize globals
        globals.n3_counter = 0
        globals.n2_counter = 0
        globals.n1_counter = 0
        globals.max_transfer_t = 50     # should be set experimentally
        globals.food_transfer_rate = 0.5 / globals.max_transfer_t  # ~0.01 units of food at each step
        # initiate vars
        self.N = N
        self.fraction_of_fed_bees = fraction_of_fed_bees
        self.attraction_radius = attraction_radius
        self.theta = (theta * np.pi / 180)
        self.width = width
        self.height = height

        # initiate scheduler
        # self.schedule = mesa.time.RandomActivation(self)     # activate agents in random order every time
        self.schedule = mesa.time.BaseScheduler(self)      # activate agents in order of creation

        # initiate mesa SingleGrid class
        self.grid = mesa.space.SingleGrid(self.width, self.height, torus=False)

        # # to store cluster objects
        # self.show_cluster = show_cluster
        # self.clusters = []
        # self.clusterCounter = 0

        # # for heading
        # self.headingCounter = 0
        # self.headings = []

        # for terminal printouts:
        # self.with_headings = with_headings
        self.step_counter = 0
        self.wrong_counter = 0
        self.undone = 0
        # self.smallUndone = 0
        # self.zeroUndone = 0

        self.agent_size = 7.8

        locStore = []
        # points = self.grid.empties()
        # rand.shuffle(points)
        # initiate agents
        for i in range(self.N):
            # loc = points[i]
            # locStore.append(loc)
            a = Bee(i, self)    # create a new Bee instance
            if i < (N * fraction_of_fed_bees/100.0):      # initiate some bees as fed
                a.makeFed()
            self.schedule.add(a)                # add agent to schedule
            self.grid.move_to_empty(a)
            # self.grid.place_agent(a, loc)      # place agent in space
        # self.datacollector = mesa.DataCollector(
        #     model_reporters={"Clusters": compute_clusters_optics,
        #                     "Fed": countFed,
        #                     "Hungry": countHungry,
        #                     "DeltaVar": report_deltaVar,
        #                     "NewVar": report_newvar,
        #                     "MedianFood": get_median_food,
        #                     "BeesInClusters": count_bees_in_clusters},#{"Trophallaxis Encounters": troph_encounters},
        #     # agent_reporters={"Fed": countFed},
        # )
        self.datacollector = mesa.DataCollector(
            model_reporters={"Food Variance": report_newvar,
                             "MedianFood": get_median_food,}
        )

        ## Clusters:
        # if self.show_cluster:
        #     self.update_clusters()
        # if self.with_headings:
        #     self.show_headings()
    # def __init__()


    def step(self):
        # #######################################
        # ### remove clusters
        # if self.show_cluster:
        #     for agent in self.clusters:
        #         self.space.remove_agent(agent)
        #         self.schedule.remove(agent)
        #     self.clusters = []
        # #######################################
        # ### remove headings
        # if self.with_headings:
        #     for agent in self.headings:
        #         self.grid.remove_agent(agent)
        #         self.schedule.remove(agent)
        #     self.headings = []
        # #######################################
        # self.write_data(self.step_counter)              # write agent positions out to text file during each step
        self.schedule.step()        # run step function for each agent
        self.datacollector.collect(self)    # collect data
        counters = [0, 0, 0]
        self.step_counter += 1
        for a in self.schedule.agents:
            # a.getNebCheck()
            if a.wrong:
                counters[0] += 1
                self.wrong_counter += 1
            if a.zero:
                counters[1] += 1
            if a.small:
                counters[2] += 1
        print("Step: " + str(self.step_counter) + " - Hungry Left: " + str(countHungry(self)))
        print("wrong: " + str(counters[0]) + ", zero: " + str(counters[1]) + ", small: " + str(counters[2]))
        print("wrong: " + str(self.wrong_counter) + " (lifetime)\n")
        print(" - Undone: " + str(self.undone))
        # print(" - Sm Und: " + str(self.smallUndone))
        # print(" - Zr Und: " + str(self.zeroUndone))
        self.undone = 0
        self.smallUndone = 0
        self.zeroUndone = 0
        # self.check_for_overlap()
        # self.write_data(self.step_counter)
        # #######################################
        # ### add clusters if true
        # if self.show_cluster:
        #     self.update_clusters()
        # #######################################
        # ### add headings if true
        # if self.with_headings:
        #     self.show_headings()
        # #######################################
    # def step()

    def run_model(self, n):
        for i in range(n):
            self.step()

    def write_data(self, step):
        file_obj = open(r"data_out/log" + str(step) + ".txt", "w")
        for a in self.schedule.agents:
            file_obj.write(r"(" + str(a.pos[0]) + "," + str(a.pos[1]) + r")" + "\n")
        file_obj.close()

    # def show_headings(self):
    #     for a in self.schedule.agents:
    #         hx = a.pos[0]+(0.5*a.heading[0])
    #         hy = a.pos[1]+(0.5*a.heading[1])
    #         if hy > 0 and hy < self.height and hx > 0 and hx < self.width:
    #             h = Heading(1000+self.headingCounter, self, hx, hy)
    #             self.headingCounter += 1
    #             self.headings.append(h)
    #             self.grid.place_agent(h, (hx, hy))
    #             self.schedule.add(h)
# class TrophallaxisABM

########################
### Data Collectors: ###
#
#

#
# Counters:
def countHungry(model):
    count = 0
    for a in model.schedule.agents:
        if a.hungry:
            count += 1
    return count

def countFed(model):
    count = 0
    for a in model.schedule.agents:
        if not a.hungry:
            count += 1
    return count
#
# Reporters:
def report_deltaVar(model):
    return globals.deltavar

def report_newvar(model):
    return globals.newvar

def get_median_food(model):
    foods = []
    for a in model.schedule.agents:
        foods.append(a.food)
    return np.median(foods)
