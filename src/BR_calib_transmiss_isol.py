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

#%%
# %% STEP1,STEP2
num_iter = 10
runtime = 360 #(Days)

start_time = time.time()

# Parameters
probPatientSick = 0.01 # from data # Prob. of being hospitalizes with Infec.
probNewPatient = 0.003 # 0.053, Old Calibration # 1/2000, 2592 ticks per day
probTransmission = 0.00003
isolationFactor = 0.75 # fix
isolationTime = 14
cleanDay = 40
isolateSick = False
ICUwashrate = 0.88
OUTSIDEwashrate = 0.67
height=11
width=32

# %% STEP3
fixed_params = {
    "prob_patient_sick" : probPatientSick, "prob_new_patient" : probNewPatient, "prob_transmission" : probTransmission,
    "isolation_factor" : isolationFactor, # "cleaningDay" : cleanDay, # "isolate_sick" : isolateSick,
    "isolation_time" : isolationTime, "icu_hcw_wash_rate" : ICUwashrate, "outside_hcw_wash_rate" : OUTSIDEwashrate, 
    "height" : height, "width" : width 
    }

# Specify the variable I want to change separately.
a = [10, 30, 60, 100, 180] # Change the cleaning Day
b = [0, 1] # When a patient is hospotalized, it can be non-infec or infec.
variable_params = {"cleaningDay" : a , "isolate_sick" : b}
# %% STEP4
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

#%% coarser
run_data = batch_run.get_model_vars_dataframe()

#####rename
run_data = run_data.rename(columns = {"icu_hcw_wash_rate": "outside_hcw_wash_rate", "outside_hcw_wash_rate":"icu_hcw_wash_rate"})
#####

data_mean = run_data.groupby(["icu_hcw_wash_rate", "outside_hcw_wash_rate"])['HCW_related_infecs'].mean()
print(data_mean)
print('\n\n')
data_mean = data_mean.reset_index()
print(data_mean['HCW_related_infecs'])
mean_patients_sick = data_mean['HCW_related_infecs'] #The avg number for the iterations


#%% coarser
xv, yv = np.meshgrid(a, b)
elev = 0 # good angle for graph
azim = 90 # good angle for graph
fig, ax= plt.subplots(1)

fig.suptitle("HCW related infecions ({} iterations)".format(num_iter))
ax = plt.axes(projection='3d')
ax.scatter(xv,yv,mean_patients_sick, c = mean_patients_sick, cmap = 'winter')
ax.set_xlabel('ICU worker handwash prob')
ax.set_ylabel('Other dept. handwash prob')
ax.set_zlabel('Infections')
ax.view_init(elev, azim)
#%%
sns.boxplot(x = 'outside_hcw_wash_rate', y = 'HCW_related_infecs', hue= 'icu_hcw_wash_rate', data = np.around(run_data, 2) )
#%%
sns.boxplot(x = 'icu_hcw_wash_rate', y = 'HCW_related_infecs', hue= 'outside_hcw_wash_rate', data = np.around(run_data, 2) )

#%%
image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
    'result\\batchrun\\handwash_fine.png')

fig.savefig(image_path)
#%%
csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
    'result\\batchrun\\handwash.csv')
run_data.to_csv(csv_path)
print("--- %s seconds ---" % (time.time() - start_time))
#%%
plt.show()
# %%
