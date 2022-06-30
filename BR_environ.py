# %%
from CPEmodel import CPE_Model
from CPEmodel import height, width, getNumSick, getHCWInfec
from mesa.batchrunner import BatchRunner

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import time

# %%
num_iter = 1
runtime = 2

start_time = time.time()
numPatients = 30 # the number of patients is 30
numHCW = 4
numGoo = 3
model = CPE_Model(
    num_HCWs=numHCW , 
    num_Patients=numPatients, 
    num_Goo=numGoo, 
    prob_new_patient=0.5, 
    prob_patient_sick=0.01,
    cleaningDay=40, 
    prob_transmission=0.1, 
    isolation_factor=0.5,
    isolate_sick=True, 
    icu_hcw_wash_rate=0.9, 
    outside_hcw_wash_rate=0.9,
    height=height, 
    width=width
    )

fixed_params = {
    "num_HCWs" : numHCW, # 4 HCWs
    "num_Patients" : numPatients, # 30 patients
    "num_Goo" : 4, # What is Goo??
    "prob_patient_sick" : 0.01, # from data # Prob. of being hospitalizes with Infec.
    "prob_new_patient" : 0.003, # 0.053, Old Calibration
                               # 1/2000, 2592 ticks per day
    # "cleaningDay" : 40,
    # "isolate_sick" : False,
    "prob_transmission" : 0.00003,
    "isolation_factor" : 0.33,
    "icu_hcw_wach_rate" : 0.88,
    "outside_hcw_wash_rate" : 0.67,
    "height" : height,
    "width" : width 
    }

# %%
