# %%
from model.cpe_model import CPE_Model
import mesa
from plot_distribution import dist_1v
from mesa.batchrunner import batch_run
import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %
durations= ['2017-1']
for duration in durations:
    print("Duration ", duration)
    num_iter = 50; np.int64(num_iter)

    # Parameters
    cleanDay = 180
    washrate = 0.9
    isolationTime = 14

    runtime = 180 # 6 months
    probNewPatient = 0.003 # 0.053, Old Calibration # 1/2000, 2592 ticks per day
    probTransmission = 0.00005 # calibration result
    isolationFactor = 0.75 # fix
    height=11
    width=32

    params = {
        "inflow_date" : duration, 
        "prob_new_patient" : probNewPatient, 
        "prob_transmission" :[0.021, 0.023, 0.025],
        "isolation_factor" : isolationFactor, 
        "cleaningDay" : cleanDay,
        "hcw_wash_rate" : washrate, 
        "isolation_time" : isolationTime, 
        "height" : height, "width" : width 
        }

    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
        'result/240818_gamma_fix_{}_021_026.csv'.format(duration))
    start_time = time.time()

    # STEP4
    model = CPE_Model(
        inflow_date=duration,
        prob_new_patient=probNewPatient, 
        prob_transmission=probTransmission, 
        isolation_factor=isolationFactor,
        cleaningDay=cleanDay,
        hcw_wash_rate=washrate,
        isolation_time=isolationTime,
        height=height, width=width
        )
    print('loading...\n\n')
    results = mesa.batch_run(
        CPE_Model,
        parameters=params,
        iterations = num_iter,
        max_steps = model.ticks_in_day * runtime,
        number_processes=1,
        # data_collection_period=-1,
        display_progress=True
        
    )


    print("done!!")
    results_df = pd.DataFrame(results)
    data_selected = results_df.groupby("prob_transmission").apply(lambda x: x[["HCW related infections", "Cumulative Patients", "Max Colonized Goo"]].reset_index(drop=True))
    data_selected.to_csv(csv_path, index=True)
    data_mean = results_df.groupby(["prob_transmission"])[['HCW related infections', 'Cumulative Patients',"Max Colonized Goo"]].mean()
    print(data_mean)
    print('\n\n')
    print("--- %s seconds ---" % (time.time() - start_time))

    print(results_df)


    # %%
