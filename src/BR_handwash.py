#%%
from CPEmodel import CPE_Model
from CPEmodel import height, width, getNumSick, getHCWInfec
from mesa.batchrunner import BatchRunner

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
import pandas as pd
import time
import seaborn as sns
# %%
num_iter = 10
runtime = 300

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
    "cleaningDay" : 180, # 기존 60
    "isolate_sick" : True,
    "prob_transmission" : 0.001, # 기존 0.0003
    "isolation_factor" : 0.5, # 기존 0.5
    "height" : height,
    "width" : width 
    }

# %% Specify the variable I want to change separately.
"""Batch run different values of

1. handwashing (ICU and Outside)
2. Environment Cleansing
3. Isolation"""


# xs =  np.arange(.97, .99, .02)  #np.arange(.02, .96, 0.02)
# ys =  np.arange(.96, .99, .02) #np.arange(.6, .91, 0.1)#np.arange(.05, .6, 0.15)
xs = [0.89,0.92,0.95,0.98]
ys = [0.89,0.92,0.95,0.98]
variable_params = {"icu_hcw_wash_rate" : xs, "outside_hcw_wash_rate" : ys}


batch_run = BatchRunner(
    CPE_Model,
    variable_parameters = variable_params,
    fixed_parameters = fixed_params,
    iterations=num_iter,
    max_steps=model.ticks_in_day * runtime,
    model_reporters={"HCW_related_infecs" : getHCWInfec,"Number_of_Patients_sick":getNumSick}
)

# Running all cases that I want to change.
batch_run.run_all()
print("done!!")

# %%
#%% coarser
run_data = batch_run.get_model_vars_dataframe()
# print(run_data)
# run_data = run_data.rename(columns = {"icu_hcw_wash_rate": "outside_hcw_wash_rate", "outside_hcw_wash_rate":"icu_hcw_wash_rate"})
data_mean = run_data.groupby(["icu_hcw_wash_rate", "outside_hcw_wash_rate"])['HCW_related_infecs'].mean()
print(data_mean)
print('\n\n')
data_mean = data_mean.reset_index()
print(data_mean['HCW_related_infecs'])

# %%
mean_patients_sick_handwash = data_mean['HCW_related_infecs'] #The avg number for the iterations

# %%
xv, yv = np.meshgrid(xs, ys)
elev = 50 # good angle for graph
azim = 30 # good angle for graph
fig, ax= plt.subplots(1)

fig.suptitle("HCW related infecions ({} iterations)".format(num_iter))
ax = plt.axes(projection='3d')
ax.scatter(xv,yv,mean_patients_sick_handwash, c = mean_patients_sick_handwash, cmap = 'winter')
ax.set_xlabel('ICU worker handwash prob')
ax.set_ylabel('Other dept. handwash prob')
ax.set_zlabel('Infections')
ax.view_init(elev, azim)
# %%
sns.boxplot(x = 'outside_hcw_wash_rate', y = 'HCW_related_infecs', hue= 'icu_hcw_wash_rate', data = np.around(run_data, 2) )
#%%
sns.boxplot(x = 'icu_hcw_wash_rate', y = 'HCW_related_infecs', hue= 'outside_hcw_wash_rate', data = np.around(run_data, 2) )
# %%
image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../',
    'result/batchrun/handwash_fine.png')

fig.savefig(image_path)
#%%
csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../',
    'result/batchrun/handwash.csv')
run_data.to_csv(csv_path)
print("--- %s seconds ---" % (time.time() - start_time))
#%%
plt.show()