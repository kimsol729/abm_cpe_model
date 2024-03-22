
#%%
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from model.cpe_model import CPE_Model
from model.agents import *
import matplotlib.pyplot as plt

#%%
def agent_portrayal(agent):
    portrayal = {"Shape":"circle",
                    "Filled": "true",
                    "r": 0.4}
    if agent.isPatient == True:
        # First start with Patients
        if agent.colonized == False:
                portrayal["Color"] = "#666666" # 아프지 않은 환자
                portrayal["Layer"] = 3
                # if agent.stay == 1:
                #     portrayal["Color"] = "#FDFEFE" # shine before leaving
                portrayal["r"] = .3

        else:
            # if agent.infecByHCW == True:
            #     portrayal["Color"] = "#FFA500" # orange
            # else:
            portrayal["Color"] = "#000000"
            portrayal["Layer"] = 2
            portrayal["r"] = .4
            if agent.isol_time > 0:
                portrayal["text"] = f"Isol Time: {np.round(agent.isol_time/agent.model.ticks_in_day,2)}"
                portrayal["Color"] = "#cd5c5c" # 격리실로 옮겨질 예정

            # if agent.stay <= 4*agent.model.ticks_in_day and agent.stay > 2*agent.model.ticks_in_day:
            #     portrayal["Color"] = "#CD5C5C" # indianred
            # if agent.stay <= 2*agent.model.ticks_in_day and agent.stay > 1:
            #     portrayal["Color"] = "#E9967A" # dark salmon
            # if agent.stay == 1:
            #     portrayal["Color"] = "#ffc300" # 
                
    if isinstance(agent, Nurse):
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 4
        portrayal["w"] = 0.2 #width
        portrayal["h"] = 0.2 #height of rectangle
        if agent.colonized == True:
            portrayal["Color"] = "red"
        else:
            if agent.hall == 6: # ICUA
                portrayal["Color"] = "#0ababa"
            else:
                portrayal["Color"] = "#096363"
    
    if isinstance(agent, Dr):
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 4
        portrayal["w"] = 0.2 #width
        portrayal["h"] = 0.2 #height of rectangle
        if agent.colonized == True:
            portrayal["Color"] = "red"
        else:
            if isinstance(agent, XrayDr):
                portrayal["Color"] = "navy"
            else:
                portrayal["Color"] = "black"

    # if agent.isWall == True:
    #     portrayal["Shape"] = "rect"
    #     portrayal["Layer"] = 10
    #     portrayal["w"] = .99 #width
    #     portrayal["h"] = .99 #height of rectangle
    #     portrayal["Color"] = "#000000"
    #     #"#273746"

    if agent.isBed == True:
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 1
        portrayal["w"] = .55 #width
        portrayal["h"] = .9 #height of rectangle
        if agent.isIsolatedBed:
            portrayal["Color"] = "#fdc4ac" #salmon
        else:
            portrayal["Color"] = "#fff2c7" #yellow
        #"#273746"

    # if agent.isIsolatedBed == True:
    #     portrayal["Shape"] = "rect"
    #     portrayal["Layer"] = 1
    #     portrayal["w"] = .55 #width
    #     portrayal["h"] = .9 #height of rectangle
    #     portrayal["Color"] = "#43165B"
    #     #"#273746"
    
    if agent.isGoo == True:
        portrayal["Shape"] = "rect"
        
        portrayal["Layer"] = 1
        portrayal["w"] = .8 #width
        portrayal["h"] = .8 #height of rectangle
        if agent.colonized == True:
            portrayal["Color"] = "#808000"
        else:
            portrayal["Color"] = "#00FF00"

    # if agent.isEnvironment == True:
    #     portrayal = {"Shape":"rect",
    #                 "Filled": "false",
    #                 "Layer" : 0,
    #                 "w" : 1,
    #                 "h" : 1}
        
    #     if agent.isBed == True:
    #         portrayal["Color"] = "#999966"
    #     if agent.isWater == True:
    #         portrayal["Color"] = "#33cccc"
    """FIX"""
    return portrayal


grid = CanvasGrid(agent_portrayal, 32, 11, 900, 300) #sets the size of grid on screen (does not mean agents will use all)
chart = ChartModule(
    [{"Label": "Number of Patients sick", "Color": "#800000"}, 
    {"Label": "Number of HCW colonized", "Color": "#00FFFF"},
    # {"Label": "Total number of Patients", "Color": "#D2691E"},
    # {"Label": "Cumulative Patients", "Color": "#black"},
    {"Label": "HCW related infections", "Color": "black"},
    {"Label": "Move to isolation", "Color": "#D2691E"}
    ],
    data_collector_name="datacollector"
)


model_params = {
    # "num_HCWs": UserSettableParameter(
    #     "slider", #param type
    #     "Nurses", #name
    #     10, #default value
    #     1, # min value
    #     10, #max value
    #     1, # step
    #     description="How many HCWs?",
    # ),
    
    "hcw_wash_rate": UserSettableParameter(
        "slider", #param type
        "Handwash probability (ICU worker)", #name
        .9, #default value
        .1, # min value
        1, #max value
        .05, # step
        #description="How many HCWs?",
    ),
    
    # "outside_hcw_wash_rate": UserSettableParameter(
    #     "slider", #param type
    #     "Handwash probability (outside worker)", #name
    #     .8, #default value
    #     .1, # min value
    #     1, #max value
    #     .05, # step
    #     #description="How many HCWs?",
    # ),
    
    # "num_Patients": 30,

    # "num_Goo": 30,

    "prob_patient_sick": UserSettableParameter(
        "slider", #param type
        "Probability incoming patient is sick", #name
        .01, #default value
        0.005, # min value
        .9, #max value
        .01, # step
        description="Probability that incoming patient is already sick",
    ),

    "prob_new_patient": UserSettableParameter(
        "slider", #param type
        "Probability of a admission of new patient", #name
        .1, #default value
        0, # min value
        1, #max value
        .1, # step
        description="Probability of a admission of new patient",
    ),

    "cleaningDay": UserSettableParameter(
            "slider", #param type
            "Days before cleaning", #name
            40, #default value
            10, # min value
            360, #max value
            10, # step
            description="How often to wash hands?",
        ),

    "prob_transmission": UserSettableParameter(
        "slider", #param type
        "Probability of transmission", #name
        .1, #default value
        0, # min value
        1, #max value
        .1, # step
        description="Probability of transmission",
    ),
    
    "isolation_factor": UserSettableParameter(
        "slider", #param type
        "Isolation factor", #name
        .2, #default value
        0, # min value
        1, #max value
        .1, # step
        description="How safe are the isolated beds?",
    ),
    

      "isolation_time": UserSettableParameter(
        "slider", #param type
        "Isolated Period for sick patients", #name
        14, #default value
        1, #min value
        14, #max
        1, # step
        description="Up to how long after you get infected, you'll be taken to the isolation room",
    ),
    
    # "randomMotion": UserSettableParameter(
    #     "checkbox", #param type
    #     "Random Motion", #name
    #     value = False, #default value
    #     #description="",
    # ),

    "width": 32, # sets which squares agents occupy
    "height": 11,
}

class TickCounter(TextElement):
    def render(self, model):
        return f"DAY: {np.round(model.day)} days   {np.round(model.schedule.time/model.ticks_in_hour + 1)} o'clock"

tick_counter = TickCounter()
server = ModularServer(CPE_Model, [grid, chart, tick_counter], "CPE Model", model_params)
# server = ModularServer(CPE_Model, [grid, chart], "CPE Model", model_params)
server.port = 8502
server.launch()
# %%

# %%
