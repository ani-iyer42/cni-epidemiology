from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import Infection


class InfectedElement(TextElement):
    """
    Display a text count of how many happy agents there are.
    """

    def __init__(self):
        pass

    def render(self, model):
        return "Infected agents: " + str(model.infected)


def infection_draw(agent):
    """
    Portrayal Method for canvas
    """
    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0, "text": agent.unique_id}

    if agent.infection_status == 1:
        portrayal["Color"] = ["#FF0000", "#FF9999"]
        portrayal["stroke_color"] = "#00FF00"
    else:
        portrayal["Color"] = ["#0000FF", "#9999FF"]
        portrayal["stroke_color"] = "#000000"
    return portrayal


infected_element = InfectedElement()
canvas_element = CanvasGrid(infection_draw, 20, 20, 500, 500)
infection_chart = ChartModule([{"Label": "infected", "Color": "Black"}])

model_params = {
    "height": 20,
    "width": 20,
    "n_agents": 100,
    "transmission_rate": UserSettableParameter(
        "slider", "Transmission_Rate", 0.6, 0.00, 1.0, 0.05
    ),
    "initial_seed": UserSettableParameter(
        "slider", "Initial_Seed", 0.4, 0.00, 0.5, 0.05
    ),
}

server = ModularServer(
    Infection, [canvas_element, infected_element, infection_chart], "Infection", model_params
)
