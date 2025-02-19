#%%
import numpy as np
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import BaseScheduler, RandomActivation, SimultaneousActivation
from mesa.space import MultiGrid
from model.agents import *

#%%
def getNumSick(model):
    """for patients"""
    count = 0
    l = [(agent.isPatient and agent.colonized) for agent in model.schedule.agents]
    for i in l:
        if i:
            count += 1
    return count

def getNumEnv(model):
    """for Env"""
    count = 0
    l = [(agent.isGoo and agent.colonized) for agent in model.schedule.agents]
    for i in l:
        if i:
            count += 1
    return count

def getMaxEnv(model):
    if len(model.NumEnv)==0:
        max = 0
    else:
        max = np.max(model.NumEnv)
    return max

def getNumColonized(model):
    """for HCW"""
    count = 0
    l = [(agent.isHCW and agent.colonized) for agent in model.schedule.agents]
    for i in l:
        if i:
            count += 1
    return count

def getCumulNumSick(model):
    """cumulative sick patients"""
    return model.cumul_sick_patients

def getHCWInfec(model):
    """every time a HCW infects a patient"""
    return model.num_infecByHCW

def getCumul(model):
    """cumulative patients"""
    return model.cumul_patients

def getNumIsol(model):
    """격리실로 옮겨지는 환자 수"""
    return model.num_move2isol
#%%
ICUA = ['A14','A15','A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12','A13']
ICUB = ['B14','B15','B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','B11','B12','B13']

import numpy as np
path_A = np.array_split(ICUA, 5)
path_B = np.array_split(ICUB, 5)
paths = np.concatenate((path_A, path_B))

class CPE_Model(Model):
    """A model with some number of agents."""
    def __init__(self, 
    inflow_date,
    prob_new_patient, 
    prob_transmission, 
    isolation_factor, 
    cleaningDay, hcw_wash_rate, isolation_time , 
    height, width):

        self.num_HCWs = 10
        self.num_Patients = 30
        self.NumEnv = []
        self.running = True
        
        # 기본 parameter
        if inflow_date == '2017-1':
            self.inflow_date = [1,90] # list
            self.hospital_period = 7.0 # exp(lambda)
        elif inflow_date == '2017-2':
            self.inflow_date = [1,45, 90, 135] # list
            self.hospital_period = 6.26 # exp(lambda)
        elif inflow_date == '2018-1':
            self.inflow_date = [1] # list
            self.hospital_period = 8.32 # exp(lambda)
        elif inflow_date == '2021-1':
            self.inflow_date = [1, 17, 33, 49, 65, 81, 97, 113, 129, 145, 161] # list
            self.hospital_period = 15.95 # exp(lambda)
        elif inflow_date == '2021-2':
            self.inflow_date = [1, 11, 21, 31, 41, 51, 61, 71, 81, 91, 101, 111, 121, 131, 141, 151, 161] # list
            self.hospital_period = 16.74 # exp(lambda)
        elif inflow_date == '2022-1':
            self.inflow_date = [1, 12, 23, 34, 45, 56 ,67, 78, 89, 100, 111, 123, 134, 145, 156, 168] # list
            self.hospital_period = 18.96 # exp(lambda)
        elif inflow_date == '2022-2':
            self.inflow_date = [1,9, 17, 25, 33, 41, 49, 57, 65, 73, 91, 99, 107, 115, 123, 131, 139, 147, 155, 163, 171] # list
            self.hospital_period = 13.32 # exp(lambda)
        elif inflow_date == '2023-1':
            self.inflow_date = [1, 13, 25, 37, 49, 61, 73, 85, 97, 109, 121, 133, 145, 157] # list
            self.hospital_period = 15.71 # exp(lambda)
        elif inflow_date == '2023-2':
            self.inflow_date = [1, 8, 15, 22, 29, 36, 43, 50, 57, 64, 71, 78, 85, 92, 99, 106, 113, 120, 127, 134, 141, 148, 155, 162, 169] # list
            self.hospital_period = 11.45 # exp(lambda)
        elif inflow_date == 'test0':
            self.inflow_date = [1] # list
            self.hospital_period = 11.45 # exp(lambda)
        elif inflow_date == 'test100':
            self.inflow_date = list(range(1, 181))# list
            self.hospital_period = 11.45 # exp(lambda)


        self.prob_new_patient = prob_new_patient # geometric rv
        self.prob_transmission = prob_transmission
        self.isolation_factor = isolation_factor

        self.cleaningDay = cleaningDay
        self.isolation_time = isolation_time
        self.hcw_wash_rate = hcw_wash_rate

        self.grid = MultiGrid(width, height, torus =False)

        self.ticks_in_hour = 1# 36 ticks to visit 3 patients, 3 cycles per hour
        self.ticks_in_day = 12 * self.ticks_in_hour
        self.day = 0

        self.schedule = BaseScheduler(self)
        self._steps = 0
        self._time = 0
        # Data collect variables 설정
        self.discharged = []
        self.current_patients = [] # List of all patients
        self.empty_beds = set() # empty set
        self.shared_beds = [] # list of all non isolated beds
        self.isol_beds = [] # list of all isolated beds

        self.summon = False
        self.summoner = 0

        self.cumul_patients = self.num_Patients # cumulative patients (*)
        self.cumul_sick_patients = 0 # cumulative sick patients (*)
        self.num_infecByHCW = 0 # HCW에 의한 감염환자 수 (*)
        self.P_I = 0
        self.num_move2isol = 0 # 검사로 인해 Isolated bed로 옮겨지는 환자 수 (*)

        # Create Agents
        # Xray Drs 3명
        strange = XrayDr(-self.num_HCWs - 7, self, colonized = False, hand_wash_rate = self.hcw_wash_rate, x = width-1, y = 0, workHours=24, numCare = 30, shiftsPerDay = 2)
        self.schedule.add(strange)
        self.grid.place_agent(strange, (strange.x, strange.y))

        strange = XrayDr(-self.num_HCWs - 8, self, colonized = False, hand_wash_rate = self.hcw_wash_rate, x = width-2, y = 0, workHours=24, numCare = 20, shiftsPerDay = 1)
        self.schedule.add(strange)
        self.grid.place_agent(strange, (strange.x, strange.y))

        strange = XrayDr(-self.num_HCWs - 9, self, colonized = False, hand_wash_rate = self.hcw_wash_rate, x = width-2, y = 1, workHours=24, numCare = 3, shiftsPerDay = 1)
        self.schedule.add(strange)
        self.grid.place_agent(strange, (strange.x, strange.y))

        # Drs 6명
        strange = Dr(-self.num_HCWs - 6, self, colonized = False, hand_wash_rate = self.hcw_wash_rate, x = width-1, y = height-1, workHours=24, numCare = 30)
        self.schedule.add(strange)
        self.grid.place_agent(strange, (strange.x, strange.y))

        strange = Dr(-self.num_HCWs - 5, self, colonized = False, hand_wash_rate = self.hcw_wash_rate, x = width-2, y = height-1, workHours=12, numCare = 30)
        self.schedule.add(strange)
        self.grid.place_agent(strange, (strange.x, strange.y))

        strange = Dr(-self.num_HCWs - 4, self, colonized = False, hand_wash_rate = self.hcw_wash_rate, x = width-2, y = height-2, workHours=12, numCare = 30)
        self.schedule.add(strange)
        self.grid.place_agent(strange, (strange.x, strange.y))

        strange = Dr(-self.num_HCWs - 3, self, colonized = False, hand_wash_rate = self.hcw_wash_rate, x = width-1, y = height-2, workHours=3, numCare = 30)
        self.schedule.add(strange)
        self.grid.place_agent(strange, (strange.x, strange.y))

        strange = Dr(-self.num_HCWs - 2, self, colonized = False, hand_wash_rate = self.hcw_wash_rate, x = width-4, y = height-1, workHours=1, numCare = 30)
        self.schedule.add(strange)
        self.grid.place_agent(strange, (strange.x, strange.y))

        strange = Dr(-self.num_HCWs - 1, self, colonized = False, hand_wash_rate = self.hcw_wash_rate, x = width-4, y = height-2, workHours=1, numCare = 30)
        self.schedule.add(strange)
        self.grid.place_agent(strange, (strange.x, strange.y))


        # Create HCW agents 간호사 Num_HCWs = 10명(30명/3교대)
        for j in range(-self.num_HCWs, 0):
            b = Nurse(j, self, colonized = False, hand_wash_rate = self.hcw_wash_rate, x = -2*j-2, y = 0)#, path = ex_path)
            self.schedule.add(b)
            self.grid.place_agent(b, (b.x, b.y)) #added 1 to start near patients for route simulation (temporary solution)
            #print(model.schedule.agents)
            b.path = paths[-j-1]
            if b.path[0][0] == 'A':
                b.hall = 6 #ICUA
            else:
                b.hall = 5 #ICUB


        # bed,patient,Goo 30개
        for i in range(30):
            # 위치 정하기
            if i in range(11):
                xpos = 2 * i + 5
                ypos = 1
            elif i in range(11, 13):
                #isolated = True
                xpos = 2 * (i-11) + 1
                ypos = 3
            elif i in range(13, 15):
                #isolated = True
                xpos = 2 * (i-13) + 27
                ypos = 3
            elif i in range(15, 17):
                #isolated = True
                xpos = 2 * (i-15) + 1
                ypos = 8
            elif i in range(17, 19):
                #isolated = True
                xpos = 2 * (i-17) + 27
                ypos = 8
            elif i in range(19, 30):
                xpos = 2 * (i-19) + 5
                ypos = 10

            #isolated status
            isolated = False
            if xpos in {1,3,5,7,23,25,27,29}: #isolation
                isolated = True

            """We first create beds so that patient.checkIsolated() works"""
            # Beds
            if isolated:
                b = IsolatedBed(i, self, colonized = False, x = xpos, y = ypos) # 0~30
                self.schedule.add(b)
                self.grid.place_agent(b, (b.x, b.y))
                self.isol_beds.append(b)
            else:
                b = Bed(i, self, colonized = False, x = xpos, y = ypos) # 0~30
                self.schedule.add(b)
                self.grid.place_agent(b, (b.x, b.y))
                self.shared_beds.append(b)

            # Patients
            a = Patient(self.num_Patients + i, self, colonized = False, x = xpos, y = ypos)#30~60
            self.schedule.add(a)
            self.grid.place_agent(a, (a.x, a.y))
            if a.colonized == True:
                self.cumul_sick_patients += 1
            
            a.stay = round(np.random.exponential(scale=self.hospital_period)) * self.ticks_in_day
            # a.stay = np.round(self.hospital_period) * self.ticks_in_day

            #Goo
            if ypos > 5: # top row
                d = Goo(-self.num_Patients - i, self, colonized = False, x=xpos, y=ypos-1) #-30~-60
            else: # bottom row
                d = Goo(-self.num_Patients - i, self, colonized = False, x=xpos, y=ypos+1) #-30~-60
            self.schedule.add(d)
            self.grid.place_agent(d, (d.x, d.y))

        
        self.datacollector = DataCollector(
            model_reporters={
                "Number of Patients sick": getNumSick,
                "Number of HCW colonized": getNumColonized,
                "Cumulative number of colonized patients": getCumulNumSick,
                "HCW related infections": getHCWInfec,
                "Cumulative Patients": getCumul,
                # "Move to isolation": getNumIsol
                # "Colonized Goo": getNumEnv,
                # "Max Colonized Goo": getMaxEnv
                })
    
        # self.running = True

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.schedule.time %= self.ticks_in_day # to keep the number from getting too large
        # print(f"time : {self.schedule.time}")
        if self.schedule.time == 0:
            self.day += 1
            # print("day : ", self.day)
        # sommon Nurse
        if self.schedule.time % self.ticks_in_hour == 0:
            self.summoner = self.schedule.time // self.ticks_in_hour
            if self.summoner > 0 and self.summoner < 16: # only for patients 1~15
                self.summon = True

        # remove patient
        for ex_patient in self.discharged:
            self.grid.remove_agent(ex_patient)
            self.schedule.remove(ex_patient)
            self.discharged.remove(ex_patient)

        # Move patients to Isolated beds
        for bed in self.shared_beds: # 7-person room
            if bed.filledSick:
                cellmates = self.grid.get_cell_list_contents([bed.pos])
                for cellmate in cellmates: # in case HCW is also in the same cell
                    if not cellmate.isPatient:
                        continue # hcw or THE BED ITSELF
                    else: # cellmate = patient
                        if cellmate.move2isol: # 옮겨야 될 시간이 된 공유침대 감염환자 발견
                            sickguy = cellmate
                            for ibed in self.isol_beds:
                                if ibed.filledSick:
                                    continue
                                if ibed.filled and not ibed.filledSick: # 격리침대 환자가 아프지 않은지 확인
                                    icellmates = self.grid.get_cell_list_contents([ibed.pos])

                                    for icellmate in icellmates:
                                        if icellmate.isPatient: # 아프지 않은 환자일거임
                                            healthyguy = icellmate
                                            self.grid.move_agent(sickguy, (ibed.x, ibed.y))
                                            self.num_move2isol += 1
                                            # print("MOVE 2 ISOLATION!!!")
                                            self.grid.move_agent(healthyguy, (bed.x, bed.y))
                                            ibed.checkFilled() # to label the bed filled
                                            break # we don't need to consider other icellmates

                                    break # we don't need to consider other beds
                                else: # not filled
                                    self.grid.move_agent(sickguy, (ibed.x, ibed.y))
                                    self.num_move2isol += 1
                                    # print("MOVE 2 ISOLATION!!!")
                                    ibed.checkFilled() # to label the bed filled
                                break
            else:
                continue
