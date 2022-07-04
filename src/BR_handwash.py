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