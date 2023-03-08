# %%
from model.cpe_model import CPE_Model
from model.cpe_model import getHCWInfec
from plot_distribution import dist_1v
from mesa.batchrunner import BatchRunner
import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %%
variable = 'clean' # clean, wash or isol
num_iter = 50; np.int64(num_iter)
save_iter = 10

# Parameters
cleanDay = 360
washrate = 0.9
isolationTime = 14
runtime = 360
probPatientSick = 0.01 # from data # Prob. of being hospitalizes with Infec.
probNewPatient = 0.003 # 0.053, Old Calibration # 1/2000, 2592 ticks per day
probTransmission = 0.00005 # calibration result
isolationFactor = 0.75 # fix
height=11
width=32

fixed_params = {
    "prob_patient_sick" : probPatientSick, 
    "prob_new_patient" : probNewPatient, 
    "prob_transmission" : probTransmission, 
    "isolation_factor" : isolationFactor, 
    "cleaningDay" : cleanDay,
    "hcw_wash_rate" : washrate, 
    "isolation_time" : isolationTime, 
    "height" : height, "width" : width 
    }
if variable == 'clean':
    variable_name = 'cleaningDay'
    variable_value = [30,90,180,360]
    title = dict(sub_1 = '30 Days Period', sub_2 = '90 Days Period',
                sub_3 = '180 Days Period', sub_4 = '360 Days Period',
                main = "Cleaning Period")
elif variable == 'wash':
    variable_name = 'hcw_wash_rate'
    variable_value = [0.8, 0.9, 0.95, 0.99]
    title = dict(sub_1 = 'Hand Wash Rate 80%', sub_2 = 'Hand Wash Rate 90%',
                sub_3 = 'Hand Wash Rate 95%', sub_4 = 'Hand Wash Rate 99%',
                main = "HCW Wash Rate")
elif variable == 'isol':
    variable_name = 'isolation_time'
    variable_value = [3, 7, 10, 14]
    title = dict(sub_1 = 'In 3 Days', sub_2 = 'In 10 Days',
                sub_3 = 'In 10 Days', sub_4 = 'In 14 Days',
                main = "Maximum number of days in quarantine")
else:
    print("insert variable")

del fixed_params[variable_name]
variable_params = {variable_name : variable_value}

csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
    'result/infec_1v_{}_{}.csv'.format(variable,num_iter))
start_time = time.time()

# %% STEP4
model = CPE_Model(
    prob_patient_sick=probPatientSick,
    prob_new_patient=probNewPatient, 
    prob_transmission=probTransmission, 
    isolation_factor=isolationFactor,
    cleaningDay=cleanDay,
    hcw_wash_rate=washrate,
    isolation_time=isolationTime,
    height=height, width=width
    )

batch_run = BatchRunner(
    CPE_Model,
    variable_parameters = variable_params,
    fixed_parameters = fixed_params,
    iterations = save_iter,
    max_steps = model.ticks_in_day * runtime,
    model_reporters={"HCW_related_infecs" : getHCWInfec}
                    #  "Number_of_Patients_sick":getNumSick}
)

print('loading...\n\n')
for _ in range(num_iter):
    batch_run.run_all()
    run_data = batch_run.get_model_vars_dataframe()
    df = pd.DataFrame()
    for value in variable_value:
        temp = run_data.query('{}=={}'.format(variable_name,value))['HCW_related_infecs']
        df[value] = temp.reset_index(drop = True)

    if os.path.isfile(csv_path):
        saved_df = pd.read_csv(csv_path,index_col=0)
        saved_df.columns = variable_value
        df = pd.concat([saved_df,df], ignore_index=True)
    df.to_csv(csv_path)

    # Visualize Distribution
    n = len(df.iloc[:,0])
    if not n-save_iter == 0:
        dist_1v(df,n,save_iter,variable,title)
print("done!!")

# %%
data_mean = run_data.groupby(["cleaningDay"])['HCW_related_infecs']
print(data_mean)
print('\n\n')
data_mean = data_mean.reset_index()
mean_patients_sick = data_mean["HCW_related_infecs"] # The avg number for the iterations.
print("--- %s seconds ---" % (time.time() - start_time))
# %%
