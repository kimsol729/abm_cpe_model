#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
# # %%
# # source path
# # %pwd : current path
# source_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../result')
# os.chdir(source_path)
# save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../result/pic')
# # %%
# df = pd.read_csv('[2022.8.31]environ50.csv')
# # cleaning_day = df.groupby("cleaningDay")["Number_of_Patients_sick"]
# # cleaning_day.describe()

# clean_30 = df.query("cleaningDay == 30 ")["Number_of_Patients_sick"] 
# clean_90 = df.query("cleaningDay == 90 ")["Number_of_Patients_sick"] 
# clean_180 = df.query("cleaningDay == 180 ")["Number_of_Patients_sick"] 
# clean_360 = df.query("cleaningDay == 360 ")["Number_of_Patients_sick"] 

# fig , ax = plt.subplots(2, 2,figsize=(10, 8))
# bin_= 1
# x_range = [0,7];y_range = [0,0.4]

# plt.subplot(221)
# sns.histplot(clean_30, stat = 'density' ,binwidth=bin_,color='green')
# sns.kdeplot(clean_30, color="k")
# plt.ylim(y_range);plt.xlim(x_range);plt.xlabel('')
# plt.title("30 day Period")

# plt.subplot(222)
# sns.histplot(clean_90, stat = 'density' ,binwidth=bin_,color='green')
# sns.kdeplot(clean_90, color="k")
# plt.ylim(y_range);plt.xlim(x_range);plt.xlabel('')
# plt.title("90 day Period")

# plt.subplot(223)
# sns.histplot(clean_180, stat = 'density' ,binwidth=bin_,color='green')
# sns.kdeplot(clean_180, color="k")
# plt.ylim(y_range);plt.xlim(x_range);plt.xlabel('')
# plt.title("180 day Period")

# plt.subplot(224)
# sns.histplot(clean_360, stat = 'density' ,binwidth=bin_,color='green')
# sns.kdeplot(clean_360, color="k")
# plt.ylim(y_range);plt.xlim(x_range);plt.xlabel('')
# plt.title("360 day Period")

# fig.suptitle('Histogram of patient occurrence according to cleaning period',fontweight ="bold",fontsize = 15)
# os.chdir(save_path)
# plt.savefig('clean_dist50.eps', dpi=600)
# plt.show()

# # %%
# os.chdir(source_path)
# df = pd.read_csv('[2022.9.5]handwash_50.csv')
# hand_wash = df.groupby("icu_hcw_wash_rate")["Number_of_Patients_sick"]
# hand_wash.describe()
# rate_80 = df.query("icu_hcw_wash_rate == 0.80")["Number_of_Patients_sick"] 
# rate_90 = df.query("icu_hcw_wash_rate == 0.90")["Number_of_Patients_sick"] 
# rate_95 = df.query("icu_hcw_wash_rate == 0.95")["Number_of_Patients_sick"] 
# rate_99 = df.query("icu_hcw_wash_rate == 0.99")["Number_of_Patients_sick"] 

# fig , ax = plt.subplots(2, 2,figsize=(10, 8))
# bin_ = 1
# x_range = [0,8];y_range = [0,0.4]

# plt.subplot(221)
# sns.histplot(rate_80,stat = 'density' ,binwidth=bin_)
# sns.kdeplot(rate_80, color="k")
# plt.ylim(y_range);plt.xlim(x_range);plt.xlabel('')
# plt.title("hand wash rate 80%")

# plt.subplot(222)
# sns.histplot(rate_90,stat = 'density' ,binwidth=bin_)
# sns.kdeplot(rate_90, color="k")
# plt.ylim(y_range);plt.xlim(x_range);plt.xlabel('')
# plt.title("hand wash rate 90%")

# plt.subplot(223)
# sns.histplot(rate_95,stat = 'density' ,binwidth=bin_)
# sns.kdeplot(rate_95, color="k")
# plt.ylim(y_range);plt.xlim(x_range);plt.xlabel('')
# plt.title("hand wash rate 95%")

# plt.subplot(224)
# sns.histplot(rate_99,stat = 'density' ,binwidth=bin_)
# sns.kdeplot(rate_99, color="k")
# plt.ylim(y_range);plt.xlim(x_range);plt.xlabel('')
# plt.title("hand wash rate 99%")
# fig.suptitle('Histogram of patient occurrence according to hand wash rate',fontweight ="bold",fontsize = 15)
# os.chdir(save_path)
# plt.savefig('handwash_dist50.eps', dpi=600)
# plt.show()

#%%
def dist_1v(df,n,save_iter,variable,title):
        fig , ax = plt.subplots(2, 2,figsize=(10, 8))
        bin_= 1
        x_range = [0,df.max().max()];y_range = [0,0.5]
        
        pic_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
        'result/pic/1v_{}_dist_{}.png'.format(variable,n))
        
        plt.subplot(221)
        sns.histplot(df.iloc[:n-save_iter,0], stat = 'density' ,binwidth=bin_,color='k',alpha = 0.3, edgecolor = "none")
        sns.histplot(df.iloc[:,0], stat = 'density' ,binwidth=bin_,color='blue',alpha = 0.5, edgecolor = "none")
        plt.axvline(df.iloc[:,0].mean(),color = 'k')
        plt.ylim(y_range);plt.xlim(x_range);plt.xlabel('')
        plt.title("{}".format(title['sub_1']))

        plt.subplot(222)
        sns.histplot(df.iloc[:n-save_iter,1], stat = 'density' ,binwidth=bin_,color='k',alpha = 0.3, edgecolor = "none")
        sns.histplot(df.iloc[:,1], stat = 'density' ,binwidth=bin_,color='orange',alpha = 0.5, edgecolor = "none")
        plt.axvline(df.iloc[:,1].mean(),color = 'k')
        plt.ylim(y_range);plt.xlim(x_range);plt.xlabel('')
        plt.title("{}".format(title['sub_2']))

        plt.subplot(223)
        sns.histplot(df.iloc[:n-save_iter,2], stat = 'density' ,binwidth=bin_,color='k',alpha = 0.3, edgecolor = "none")
        sns.histplot(df.iloc[:,2], stat = 'density' ,binwidth=bin_,color='green',alpha = 0.5, edgecolor = "none")
        plt.axvline(df.iloc[:,2].mean(),color = 'k')
        plt.ylim(y_range);plt.xlim(x_range);plt.xlabel('')
        plt.title("{}".format(title['sub_3']))

        plt.subplot(224)
        sns.histplot(df.iloc[:n-save_iter,3], stat = 'density' ,binwidth=bin_,color='k',alpha = 0.3, edgecolor = "none")
        sns.histplot(df.iloc[:,3], stat = 'density' ,binwidth=bin_,color='red',alpha = 0.5, edgecolor = "none")
        plt.axvline(df.iloc[:,3].mean(),color = 'k')
        plt.ylim(y_range);plt.xlim(x_range);plt.xlabel('')
        plt.title("{}".format(title['sub_4']))
        
        fig.suptitle('Histogram According To {}(simul : {})'.format(title['main'],n),fontweight ="bold",fontsize = 15)
        plt.savefig(pic_path,dpi = 600)
#%%
def dist_2v(df,n,save_iter,variable,title):
        fig , ax = plt.subplots(2, 2,figsize=(10, 8))
        bin_= 1
        x_range = [0,df.max().max()];y_range = [0,0.5]
        
        pic_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
        'result/pic/2v_{}_dist_{}.png'.format(variable,n))
        
        plt.subplot(221)
        sns.histplot(df.iloc[:n-save_iter,0], stat = 'density' ,binwidth=bin_,color='k',alpha = 0.3, edgecolor = "none")
        sns.histplot(df.iloc[:,0], stat = 'density' ,binwidth=bin_,color='blue',alpha = 0.5, edgecolor = "none")
        plt.axvline(df.iloc[:,0].mean(),color = 'k')
        plt.ylim(y_range);plt.xlim(x_range);plt.xlabel('')
        plt.title("{}".format(title['sub_1']))

        plt.subplot(222)
        sns.histplot(df.iloc[:n-save_iter,1], stat = 'density' ,binwidth=bin_,color='k',alpha = 0.3, edgecolor = "none")
        sns.histplot(df.iloc[:,1], stat = 'density' ,binwidth=bin_,color='orange',alpha = 0.5, edgecolor = "none")
        plt.axvline(df.iloc[:,1].mean(),color = 'k')
        plt.ylim(y_range);plt.xlim(x_range);plt.xlabel('')
        plt.title("{}".format(title['sub_2']))

        plt.subplot(223)
        sns.histplot(df.iloc[:n-save_iter,2], stat = 'density' ,binwidth=bin_,color='k',alpha = 0.3, edgecolor = "none")
        sns.histplot(df.iloc[:,2], stat = 'density' ,binwidth=bin_,color='green',alpha = 0.5, edgecolor = "none")
        plt.axvline(df.iloc[:,2].mean(),color = 'k')
        plt.ylim(y_range);plt.xlim(x_range);plt.xlabel('')
        plt.title("{}".format(title['sub_3']))

        plt.subplot(224)
        sns.histplot(df.iloc[:n-save_iter,3], stat = 'density' ,binwidth=bin_,color='k',alpha = 0.3, edgecolor = "none")
        sns.histplot(df.iloc[:,3], stat = 'density' ,binwidth=bin_,color='red',alpha = 0.5, edgecolor = "none")
        plt.axvline(df.iloc[:,3].mean(),color = 'k')
        plt.ylim(y_range);plt.xlim(x_range);plt.xlabel('')
        plt.title("{}".format(title['sub_4']))
        
        fig.suptitle('Histogram According To {}(simul : {})'.format(title['main'],n),fontweight ="bold",fontsize = 15)
        plt.savefig(pic_path,dpi = 600)
# %%
