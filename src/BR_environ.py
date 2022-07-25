# %%
from matplotlib import image
from CPEmodel import CPE_Model
from CPEmodel import getNumSick, getHCWInfec
from mesa.batchrunner import BatchRunner

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
import pandas as pd
import time

# %%
num_iter = 1
runtime = 3

start_time = time.time()

# Parameters
# numHCW = 10
# numPatients = 30 # the number of patients is 30
numGoo = 30
probPatientSick = 0.01 # from data # Prob. of being hospitalizes with Infec.
probNewPatient = 0.003 # 0.053, Old Calibration # 1/2000, 2592 ticks per day
probTransmission = 0.00003
isolationFactor = 0.33
cleanDay = 40
isolateSick = False
ICUwashrate = 0.88
OUTSIDEwashrate = 0.67
height=11
width=32

# %%
fixed_params = {
    "prob_patient_sick" : probPatientSick, "prob_new_patient" : probNewPatient, "prob_transmission" : probTransmission,
    "isolation_factor" : isolationFactor, # "cleaningDay" : cleanDay, # "isolate_sick" : isolateSick,
    "icu_hcw_wash_rate" : ICUwashrate, "outside_hcw_wash_rate" : OUTSIDEwashrate,
    "height" : height, "width" : width 
    }

# Specify the variable I want to change separately.

a = [10, 30, 60, 100, 180] # Change the cleaning Day
b = [0, 1] # When a patient is hospotalized, it can be non-infec or infec.
variable_params = {"cleaningDay" : a , "isolate_sick" : b}
# %% 
model = CPE_Model(
    prob_patient_sick=probPatientSick,prob_new_patient=probNewPatient, prob_transmission=probTransmission, 
    isolation_factor=isolationFactor,cleaningDay=cleanDay, isolate_sick=True, 
    icu_hcw_wash_rate=ICUwashrate, outside_hcw_wash_rate=OUTSIDEwashrate,
    height=height, width=width
    )

batch_run = BatchRunner(
    CPE_Model,
    variable_parameters = variable_params,
    fixed_parameters = fixed_params,
    iterations=num_iter,
    max_steps=model.ticks_in_day * runtime,
    model_reporters = {"HCW_related_infecs": getHCWInfec, "Number_of_Patients_sick":getNumSick}
)

# Running all cases that I want to change.
print('loading...\n\n')
batch_run.run_all()
print("done!!")


# %%
run_data = batch_run.get_model_vars_dataframe()
data_mean = run_data.groupby(["cleaningDay","isolate_sick"])['HCW_related_infecs'].mean()
print(data_mean)
print('\n\n')
data_mean = data_mean.reset_index()
mean_patients_sick = data_mean["HCW_related_infecs"] # The avg number for the iterations.

# %% 
isolated = data_mean.loc[data_mean['isolate_sick']==1]
nonisolated = data_mean.loc[data_mean['isolate_sick']==0]
# %%
w = 0.4
zz = np.arange(len(a)) # 0,1,2,3,4
zi = [i+w for i in np.arange(len(a))] # 0.4, 1.4, 2.4, 3.4, 4.4

z = list(map(str, a)) # ['0','1']

# %%
fig = plt.figure()
plt.bar(zz, nonisolated["HCW_related_infecs"], w, label = "No Isolation")
plt.bar(zi, isolated["HCW_related_infecs"],w,label = "Isolation")
plt.xlabel("Days before cleaning enviroment")
plt.ylabel("Number of HCW related infectious")
plt.xticks(zz + w/2, z)
plt.title("HCW related infectious after {} days ({} iterations)".format(runtime,num_iter))
plt.legend()

plt.show()
# %%
image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../',
    'result/batchrun/environ_isol_300.png')
fig.savefig(image_path)
