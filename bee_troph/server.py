import mesa

from .model import TrophallaxisABM
from .SimpleContinuousModule import SimpleCanvas

import numpy as np

def _get_agent_color(agent):
    if agent.food == 0:
        return "rgb(0,0,0)"
    elif agent.food > 0.5:
        return "rgb(255,0,0)"
    elif agent.food > 0.24:
        return "rgb(255,51,51)"
    elif agent.food > 0.12:
        return "rgb(255,102,102)"
    elif agent.food > 0.06:
        return "rgb(255,153,153)"
    else:
        return "rgb(255,204,204)"
# _get_agent_color()

def bee_draw(agent):
    portrayal = {"Filled": "true"}

    ## Set shape, size, and color:
    portrayal["Shape"] = "circle"
    portrayal["r"] = 7.8
    portrayal["Color"] = _get_agent_color(agent)
    return portrayal
# bee_draw()

## Make Bee Canvas:
bee_canvas = SimpleCanvas(bee_draw, 500, 500)

## Set Model Parameters:
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
    ),
    "attraction_radius": mesa.visualization.Slider(
        "Attraction Radius",
        2.5,
        0,
        10,
        0.5,
    ),
    "theta": mesa.visualization.Slider(
        "Theta: random walk",
        180,
        0,
        360,
        5,
    ),
    # "solid_bounds": mesa.visualization.Checkbox(
    #     "Use Solid Arena Boundaries?",
    #     True,
    # ),
    # "attraction_bias": mesa.visualization.Checkbox(
    #     "Use Attraction Bias?",
    #     True,
    # ),
    # "always_random_walk": mesa.visualization.Checkbox(
    #     "Always Random Walk?",
    #     True,
    # ),
    # "data_out": mesa.visualization.Checkbox(
    #     "data csv?",
    #     False,
    # ),
    # "food_out": mesa.visualization.Checkbox(
    #     "food csv?",
    #     False,
    # ),
    # "a_boost": mesa.visualization.Slider(
    #     "Attraction Bias Strength",
    #     10,
    #     1,
    #     20,
    #     1,
    # ),
    # "eps_boost": mesa.visualization.Slider(
    #     "Epsilon Booster",
    #     8,
    #     4,
    #     8,
    #     1,
    # ),
    # "end_boost": mesa.visualization.Slider(
    #     "End Check Booster",
    #     8,
    #     1,
    #     20,
    #     1,
    # ),
    # "batch_id": mesa.visualization.Slider(
    #     "batch number",
    #     0,
    #     0,
    #     10,
    #     1,
    # ),
    # "run_id": mesa.visualization.Slider(
    #     "run ID",
    #     0,
    #     0,
    #     30,
    #     1,
    # ),
    "width": 32,
    "height": 32,
}

## Plots and Data:
foodBar = mesa.visualization.BarChartModule([
    {"Label": "Fed .50",
     "Color": "rgb(255,0,0)"},
    {"Label": "Fed .25",
     "Color": "rgb(255,51,51)"},
    {"Label": "Fed .12",
     "Color": "rgb(255,102,102)"},
    {"Label": "Fed .05",
     "Color": "rgb(255,153,153)"},
    {"Label": "Fed .01",
     "Color": "rgb(255,204,204)"},
    {"Label": "Fed 0.0",
     "Color": "rgb(0,0,0)"},
    ],
    canvas_height=300,
    canvas_width=550,
    data_collector_name="data_collector")

tmpchart = mesa.visualization.ChartModule([
    {"Label": "Fed .50",
     "Color": "Blue"}
],
    canvas_height=300,
    data_collector_name="data_collector")

## Make Server and Run:
server = mesa.visualization.ModularServer(
    TrophallaxisABM, [bee_canvas, foodBar], "Trophallaxis", model_params
)
