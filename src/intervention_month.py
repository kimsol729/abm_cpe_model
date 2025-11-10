# %%
from model.cpe_model_month import CPE_Model_month
from mesa.batchrunner import batch_run
from model.cpe_model_month import getHCWInfec
from model.cpe_model_month import getTotalInfec
from mesa.batchrunner import BatchRunner
from multiprocessing import freeze_support
import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# %%

# Step 1. Data type 정하기
data_type = 'B'
if data_type == 'A':
    runtime = 30*19
    df = pd.read_csv("../emulation_calibration/B_samp_A.csv")
    df = df[2000:]

elif data_type == 'B':
    runtime = 30*36
    df = pd.read_csv("../emulation_calibration/B_samp_B.csv")
    df = df[2000:]

np.random.seed(4321)
samples = np.random.choice(df["x"], 50, replace=True) # of Samples = 50
probTransmission_samples = samples

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.hist(df["x"], bins=30, edgecolor="black", alpha=0.7, label="Original")
plt.xlabel("x values")
plt.ylabel("Frequency")
plt.title("Original Distribution")
plt.legend()
x_min, x_max = df["x"].min(), df["x"].max()
plt.xlim(x_min, x_max)
plt.subplot(1, 2, 2)
plt.hist(samples, bins=30, edgecolor="black", alpha=0.7, label="Sampled")
plt.xlabel("x values")
plt.ylabel("Frequency")
plt.title("Sampled Distribution")
plt.legend()
plt.xlim(x_min, x_max)
plt.tight_layout()
plt.show()

#%% Step2. 어떤 변수를 몇으로 할건지 정하기

# variable_name = 'hcw_wash_rate'
# variable_value = [0.95]

variable_name = 'cleaningDay'
variable_value = [30, 60, 90, 180]

# variable_name = 'isolation_time'
# variable_value = [14]
for i in variable_value:
    probNewPatient = 0.003
    isolationFactor = 0.75
    height=11
    width=32

    fixed_params = {
        "data_type" : data_type , 
        "prob_new_patient" : probNewPatient, 
        "isolation_factor" : isolationFactor, 
        "cleaningDay" : 180,
        "hcw_wash_rate" : 0.9, 
        "isolation_time" : 14, 
        "height" : height, "width" : width 
        }
    del fixed_params[variable_name]
    fixed_params.update({variable_name: i})

    model = CPE_Model_month(
        data_type=data_type,
        prob_new_patient=probNewPatient, 
        prob_transmission=000, 
        isolation_factor=isolationFactor,
        cleaningDay=180,
        hcw_wash_rate=0.9,
        isolation_time=14,
        height=height, width=width
        )
    variable_params = {'prob_transmission' : probTransmission_samples}
    batch_run = BatchRunner(
    CPE_Model_month,
    variable_parameters = variable_params,
    fixed_parameters = fixed_params,
    iterations = 50,
    max_steps = model.ticks_in_day * runtime,
    display_progress=True,
    model_reporters={"HCW_related_infecs" : getTotalInfec}
    )
    print('now run')
    batch_run.run_all()
    run_data = batch_run.get_model_vars_dataframe()
    

    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
        'result/new_intervention_test_cleanB_{}.csv'.format(i))
    run_data.to_csv(csv_path)

    print("done!!")


   
plt.hist(samples, bins=30, edgecolor="black", alpha=0.7, label="Sampled")
plt.xlabel("x values")
plt.ylabel("Frequency")
plt.title("Sampled Distribution")
plt.legend()
plt.xlim(x_min, x_max)
plt.tight_layout()
plt.show()


# Step 1. Data type 정하기
data_type = 'A'
if data_type == 'A':
    runtime = 30*19
    df = pd.read_csv("../emulation_calibration/B_samp_A.csv")
    df = df[2000:]

elif data_type == 'B':
    runtime = 30*36
    df = pd.read_csv("../emulation_calibration/B_samp_B.csv")
    df = df[2000:]

np.random.seed(4321)
samples = np.random.choice(df["x"], 50, replace=True) # of Samples = 50
probTransmission_samples = samples

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.hist(df["x"], bins=30, edgecolor="black", alpha=0.7, label="Original")
plt.xlabel("x values")
plt.ylabel("Frequency")
plt.title("Original Distribution")
plt.legend()
x_min, x_max = df["x"].min(), df["x"].max()
plt.xlim(x_min, x_max)
plt.subplot(1, 2, 2)
plt.hist(samples, bins=30, edgecolor="black", alpha=0.7, label="Sampled")
plt.xlabel("x values")
plt.ylabel("Frequency")
plt.title("Sampled Distribution")
plt.legend()
plt.xlim(x_min, x_max)
plt.tight_layout()
plt.show()

# Step2. 어떤 변수를 몇으로 할건지 정하기

# variable_name = 'hcw_wash_rate'
# variable_value = [0.95]

variable_name = 'cleaningDay'
variable_value = [30, 60, 90, 180]

# variable_name = 'isolation_time'
# variable_value = [14]
for i in variable_value:
    probNewPatient = 0.003
    isolationFactor = 0.75
    height=11
    width=32

    fixed_params = {
        "data_type" : data_type , 
        "prob_new_patient" : probNewPatient, 
        "isolation_factor" : isolationFactor, 
        "cleaningDay" : 180,
        "hcw_wash_rate" : 0.9, 
        "isolation_time" : 14, 
        "height" : height, "width" : width 
        }
    del fixed_params[variable_name]
    fixed_params.update({variable_name: i})

    model = CPE_Model_month(
        data_type=data_type,
        prob_new_patient=probNewPatient, 
        prob_transmission=000, 
        isolation_factor=isolationFactor,
        cleaningDay=180,
        hcw_wash_rate=0.9,
        isolation_time=14, 
        height=height, width=width
        )
    variable_params = {'prob_transmission' : probTransmission_samples}
    batch_run = BatchRunner(
    CPE_Model_month,
    variable_parameters = variable_params,
    fixed_parameters = fixed_params,
    iterations = 50,
    max_steps = model.ticks_in_day * runtime,
    display_progress=True,
    model_reporters={"HCW_related_infecs" : getTotalInfec}
    )
    print('now run')
    batch_run.run_all()
    run_data = batch_run.get_model_vars_dataframe()
    

    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
        'result/new_intervention_test_cleanA_{}.csv'.format(i))
    run_data.to_csv(csv_path)

    print("done!!")

# %%
