import mesa # mesa             : 2.1.4
            # mesa-viz-tornado : 0.1.3
from .model import TrophallaxisABM
from .SimpleContinuousModule import SimpleCanvas


def bee_draw(agent):
    portrayal = {"Shape": "circle"}#, "r": 7.8}
    if agent.agent_size == 7.0:
        # portrayal = {"Shape": "circle", "r": 7.0}
        portrayal["r"] = 7.0
    elif agent.agent_size <= 7.4:
        # portrayal = {"Shape": "circle", "r": 7.4}
        portrayal["r"] = 7.4
    elif agent.agent_size <= 7.8:
        # portrayal = {"Shape": "circle", "r": 7.8}
        portrayal["r"] = 7.8
    elif agent.agent_size <= 8.0:
        # portrayal = {"Shape": "circle", "r": 8.0}
        portrayal["r"] = 8.0
    if agent.color == 0:
        if agent.food > 0.9:                        # max red if full of food
            portrayal["Color"] = "rgb(255,0,0)"
            portrayal["Filled"] = "true"
        elif agent.food > 0.75:
            portrayal["Color"] = "rgb(220,0,0)"
            portrayal["Filled"] = "true"
        elif agent.food > 0.5:
            portrayal["Color"] = "rgb(200,0,0)"
            portrayal["Filled"] = "true"
        elif agent.food > 0.25:
            portrayal["Color"] = "rgb(180,0,0)"
            portrayal["Filled"] = "true"
        elif agent.food > 0.2:
            portrayal["Color"] = "rgb(160,0,0)"
            portrayal["Filled"] = "true"
        elif agent.food > 0.15:
            portrayal["Color"] = "rgb(140,0,0)"
            portrayal["Filled"] = "true"
        elif agent.food > 0.1:
            portrayal["Color"] = "rgb(120,0,0)"
            portrayal["Filled"] = "true"
        elif agent.food > 0.01:
            portrayal["Color"] = "rgb(100,0,0)"
            portrayal["Filled"] = "true"
        else:
            portrayal["Color"] = "rgb(0,0,0)"
            portrayal["Filled"] = "true"
    elif agent.color == 1:
        portrayal["Color"] = "green"
    elif agent.color == 2:
        portrayal["Color"] = "green"
        portrayal["Fill"] = "false"
        portrayal["r"] = 28
    elif agent.color == 3:
        portrayal["Color"] = "rgb(0,255,50)"
        portrayal["Filled"] = "true"
        portrayal["r"] = 1
    return portrayal


bee_canvas = SimpleCanvas(bee_draw, 500, 500)
model_params = {
    "N": mesa.visualization.Slider(
        "N",
        110,    # default
        0,      # min
        500,    # max
        5,      # step
    ),
    "fraction_of_fed_bees": mesa.visualization.Slider(
        "Fraction of fed bees",
        10,
        0,
        100,
        1,
        "The percentage of bees that start out fed",
    ),
    "attraction_radius": mesa.visualization.Slider(
        "Attraction Radius",
        3,
        0,
        10,
        1,
    ),
    "theta": mesa.visualization.Slider(
        "Agent FOV",
        180,
        0,
        360,
        5,
    ),
    # "agent_size": mesa.visualization.Slider(
    #     "Agent Size",
    #     7.8,
    #     7.0,
    #     8.0,
    #     0.1,
    # ),
    "width": 32,
    "height": 32,
}

# chart = mesa.visualization.ChartModule(
#     [{"Label": "Clusters", "Color": "Black", "Name": "# of Clusters"}], data_collector_name="datacollector")
#
# chart2 = mesa.visualization.PieChartModule(
#     [{"Label": "Fed", "Color": "Red"}, {"Label": "Hungry", "Color": "Black"}], data_collector_name="datacollector")
#
# deltaVarChart = mesa.visualization.ChartModule(
#     [{"Label": "DeltaVar", "Color": "RED"}], data_collector_name="datacollector")
# # , "Name": "Delta Variance"
# countBeesInClustersChart = mesa.visualization.ChartModule(
#     [{"Label": "BeesInClusters", "Color": "Green"}], data_collector_name="datacollector")
#
# newvarChart = mesa.visualization.ChartModule(
#     [{"Label": "NewVar", "Color": "Red"}], data_collector_name="datacollector")
#
# medianFoodChart = mesa.visualization.ChartModule(
#     [{"Label": "MedianFood", "Color": "Blue"}], data_collector_name="datacollector")

newVarDeltaVarChart = mesa.visualization.ChartModule([
    {"Label": "Food Variance",
     "Color": "#ff0000",
     "Filled": "true"},
    {"Label": "MedianFood",
     "Color": "Blue"}
],
    canvas_height=300,
    data_collector_name="datacollector")

server = mesa.visualization.ModularServer(
    # TrophallaxisABM, [bee_canvas, chart, chart2], "Trophallaxis", model_params)
    TrophallaxisABM, [bee_canvas, newVarDeltaVarChart], "Trophallaxis", model_params)

# [bee_canvas, countBeesInClustersChart, chart, medianFoodChart, newvarChart, deltaVarChart]
