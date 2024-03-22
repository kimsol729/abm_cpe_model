#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.dates as mdates
from datetime import datetime
import seaborn as sns

# %% 2017-2018 data analysis
current_directory = os.getcwd()
file_path = 'data/2017_2018_data.csv'
data = pd.read_csv(file_path)

# 날짜 형식 변경
def convert_date(date_str):
    return datetime.strptime(date_str, '%m/%d/%y').date()
data['ICU_adm_date'] = data['ICU_adm_date'].apply(convert_date)
data['ICU_discharge_date'] = data['ICU_discharge_date'].apply(convert_date)
data['result_report_date'] = data['result_report_date'].apply(convert_date)


#%% load patients list
number = 1
columns = ['P_ID', 'ICU_adm_date', 'ICU_dis_date', 'CRE_result', 'test_date']
filt_data = pd.DataFrame(columns=columns)
manual_data = pd.DataFrame()

p_id = list(data['P_number'].astype(int).drop_duplicates())

for patient in p_id:
    df = data[data['P_number'] == patient]
    df = df.sort_values(by='ICU_adm_date')
    df = df.sort_values(by='ICU_discharge_date')
    df = df.sort_values(by='result_report_date')
    n = len(df)

    if len(df['CPE_result'].unique()) == 1:
        adm_date = df['ICU_adm_date'].reset_index(drop=True).values
        dis_date = df['ICU_discharge_date'].reset_index(drop=True).values
        timedeltas = adm_date[1:]-dis_date[:-1]
        indices = [0] + list(np.where(timedeltas.astype('timedelta64[D]') > np.timedelta64(1, 'D'))[0] + 1) + [n]

        for i in range(len(indices)-1):
            idx = indices[i]
            last_idx = indices[i+1]-1

            next_pid = filt_data['P_ID'].max() + 1 if not filt_data.empty else 1
            add_data = {'P_ID': next_pid,
                'ICU_adm_date': df.iloc[idx]['ICU_adm_date'], 
                'ICU_dis_date': df.iloc[last_idx]['ICU_discharge_date'], 
                'CRE_result': df.iloc[idx]['CPE_result'], 
                'test_date': df.iloc[idx]['result_report_date']}
            filt_data = pd.concat([filt_data, pd.DataFrame([add_data])], ignore_index=True)

    else:
        manual_data = pd.concat([manual_data, df.reset_index(drop=True)], ignore_index=True)

# manual_data와 filt_data를 엑셀 파일로 저장
manual_data.to_excel('data/manual_data.xlsx', index=False)
filt_data.to_excel('data/filt_data.xlsx', index=False)

# %% 2017-2018 data analysis
"""
FINISH DATA PROCESSING
load filtered data 2017-2018

"""
current_directory = os.getcwd()
file_path = 'data/2017_filt_data.csv'
data = pd.read_csv(file_path)
#%%
# ICU 재원 기간 계산 (ICU_dis_date - ICU_adm_date)
data['ICU_hosp_days'] = pd.to_datetime(data['ICU_dis_date']) - pd.to_datetime(data['ICU_adm_date'])

# 히스토그램 그리기
plt.hist(data['ICU_hosp_days'].dt.days, bins=40, edgecolor='black')
plt.xlabel('ICU Duration (days)')
plt.ylabel('Frequency')
plt.title('Histogram of ICU Duration')
plt.grid(True)
plt.show()

# 평균값 계산
mean_icu_hosp_days = data['ICU_hosp_days'].mean().days
median_icu_hosp_days = data['ICU_hosp_days'].median().days

print("평균 재원 기간:", mean_icu_hosp_days)
print("중간 재원 기간:", median_icu_hosp_days)

#%%
# 'CPE_result'가 1인 경우와 0인 경우로 데이터 분리
cpe_result_1 = data[data['CRE_result'] == 1]['ICU_hosp_days']
cpe_result_0 = data[data['CRE_result'] == 0]['ICU_hosp_days']

# Histogram 비교
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.hist(cpe_result_1.dt.days, bins=20, color='skyblue', edgecolor='black')
plt.xlabel('ICU Hospital Days')
plt.ylabel('Frequency')
plt.title('Histogram of ICU Hospital Days (CPE_result = 1)')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.hist(cpe_result_0.dt.days, bins=20, color='lightgreen', edgecolor='black')
plt.xlabel('ICU Hospital Days')
plt.ylabel('Frequency')
plt.title('Histogram of ICU Hospital Days (CPE_result = 0)')
plt.grid(True)

plt.tight_layout()
plt.show()

# 중앙값과 평균값 계산
median_cpe_result_1 = cpe_result_1.median()
median_cpe_result_0 = cpe_result_0.median()

mean_cpe_result_1 = cpe_result_1.mean()
mean_cpe_result_0 = cpe_result_0.mean()

print("CPE_result가 1인 경우의 중앙값:", median_cpe_result_1)
print("CPE_result가 1인 경우의 평균값:", mean_cpe_result_1)
print("CPE_result가 0인 경우의 중앙값:", median_cpe_result_0)
print("CPE_result가 0인 경우의 평균값:", mean_cpe_result_0)
# #%%
# filtered_data = data[data['ICU_hosp_days'] != 0]

# plt.hist(filtered_data['ICU_hosp_days'].dt.days, bins=30, color='skyblue', edgecolor='black')
# plt.xlabel('ICU Hospital Days')
# plt.ylabel('Frequency')
# plt.title('Histogram of ICU Hospital Days (Excluding 0)')
# plt.grid(True)
# plt.show()
# %%
"""
여기서 부터 2017-2018 버전으로 변경하고 결과 정리
"""
# 데이터 불러오기
file_path = 'data/2017_infection_data.csv'
df = pd.read_csv(file_path)

# 날짜 형식으로 변환
df['in'] = pd.to_datetime(df['in'])
df['out'] = pd.to_datetime(df['out'])
df['test'] = pd.to_datetime(df['test'])


# 분석할 날짜 범위 설정
start_date = pd.Timestamp('2017-01-01')
end_date = pd.Timestamp('2019-01-01')
date_ranges = pd.date_range(start=start_date, end=end_date, freq='6MS')

#%% 기간별 입원 환자 수 확인

num_ps = []
mean_ps = []
median_ps = []

for i in range(len(date_ranges) - 1):
    start_range = date_ranges[i]
    end_range = date_ranges[i + 1]
    num_p = ((df['in'] >= start_range) & (df['in'] < end_range)).sum()
    mean_p = np.mean((df['out'] - df['in'])[((df['in'] >= start_range) & (df['in'] < end_range))].astype('timedelta64[D]'))
    median_p = np.median((df['out'] - df['in'])[((df['in'] >= start_range) & (df['in'] < end_range))].astype('timedelta64[D]'))
    num_ps.append(num_p)
    mean_ps.append(round(mean_p, 2))
    median_ps.append(round(median_p, 2))

print("Number of patients admitted each month:", num_ps)
print("Mean length of stay each month (days):", mean_ps)
print("Median length of stay each month (days):", median_ps)

#%%
num_cre = []

for i in range(len(date_ranges) - 1):
    start_range = date_ranges[i]
    end_range = date_ranges[i + 1]
    num_p = ((df['in'] >= start_range) & (df['in'] < end_range) & (df['infect'] == 1)).sum()
    num_cre.append(num_p)  # num_p 값을 num_ps 리스트에 추가

print(num_cre)  # 각 기간별 입원 환자 수가 담긴 리스트 출력

#%%
# 그래프 그리기
plt.figure(figsize=(12,10))
plt.subplot(211)
for n in range(0, 4, 3):
    date_n = pd.Timedelta(days=n)

    # P_I 계산
    P_I = df[(df['test'] < df['in'] + date_n) & (df['infect'] == 1)]
    P_I_total = df[df['test'] < df['in'] + date_n]

    # P_I 확률 계산
    PI_probs = []
    for i in range(len(date_ranges) - 1):
        start_range = date_ranges[i]
        end_range = date_ranges[i + 1]
        PI_count = ((P_I['in'] >= start_range) & (P_I['in'] < end_range)).sum()
        PI_total_count = ((P_I_total['in'] >= start_range) & (P_I_total['in'] < end_range)).sum()
        PI_prob = PI_count / PI_total_count if PI_total_count != 0 else 0
        PI_probs.append(PI_prob)

    plt.plot(PI_probs, label=f'n={n} (PI)')

plt.xticks(ticks=range(len(date_ranges)-1), labels=[date.strftime('%Y-%m') for date in date_ranges[:-1]], rotation=45)
plt.legend()
plt.subplot(212)
for n in range(3, 4, 3):
    date_n = pd.Timedelta(days=n)
    date_m = pd.Timedelta(days=3)

    # P_HAI 계산
    P_HAI = df[((df['in'] + date_n <= df['test']) & (df['test'] <= df['out'] + date_m)) & (df['infect'] == 1)]
    P_HAI_total = df[((df['in'] + date_n <= df['test']) & (df['test'] <= df['out'] + date_m))]

    # P_HAI 확률 계산
    PHAI_probs = []
    for i in range(len(date_ranges) - 1):
        start_range = date_ranges[i]
        end_range = date_ranges[i + 1]
        PHAI_count = ((P_HAI['in'] >= start_range) & (P_HAI['in'] < end_range)).sum()
        PHAI_total_count = ((P_HAI_total['in'] >= start_range) & (P_HAI_total['in'] < end_range)).sum()
        PHAI_prob = PHAI_count / PHAI_total_count if PHAI_total_count != 0 else 0
        PHAI_probs.append(PHAI_prob)

    plt.plot(PHAI_probs, label=f'n={n} (PHAI)')

plt.xticks(ticks=range(len(date_ranges)-1), labels=[date.strftime('%Y-%m') for date in date_ranges[:-1]], rotation=45)
plt.legend()
plt.show()
# %% The Number of Positive
plt.figure(figsize=(12,10))
plt.subplot(211)
for n in range(3, 4, 3):
    date_n = pd.Timedelta(days=n)

    # P_I 계산
    P_I = df[(df['test'] < df['in'] + date_n) & (df['infect'] == 1)]

    # P_I 확률 계산
    PI_counts = []
    for i in range(len(date_ranges) - 1):
        start_range = date_ranges[i]
        end_range = date_ranges[i + 1]
        PI_count = ((P_I['in'] >= start_range) & (P_I['in'] < end_range)).sum()
        PI_counts.append(PI_count)

    plt.plot(PI_counts,'*-', label=f'n={n} (PI)')

plt.xticks(ticks=range(len(date_ranges)-1), labels=[date.strftime('%Y-%m') for date in date_ranges[:-1]], rotation=45)
plt.legend()

plt.subplot(212)
for n in range(3, 4, 3):
    date_n = pd.Timedelta(days=n)
    date_m = pd.Timedelta(days=3)

    # P_HAI 계산
    P_HAI = df[((df['in'] + date_n <= df['test']) & (df['test'] <= df['out'] + date_m)) & (df['infect'] == 1)]
    # P_HAI 확률 계산
    PHAI_counts = []
    for i in range(len(date_ranges) - 1):
        start_range = date_ranges[i]
        end_range = date_ranges[i + 1]
        PHAI_count = ((P_HAI['in'] >= start_range) & (P_HAI['in'] < end_range)).sum()
        PHAI_counts.append(PHAI_count)

    plt.plot(PHAI_counts,'*-', label=f'n={n} (PHAI)')

plt.xticks(ticks=range(len(date_ranges)-1), labels=[date.strftime('%Y-%m') for date in date_ranges[:-1]], rotation=45)
plt.legend()
plt.show()
# %% 재원기간 평가
# date_n과 date_m 변수 정의
date_n = pd.Timedelta(days=3)
date_m = pd.Timedelta(days=3)
a = {'date_diff': (df['out'] - df['in']).dt.days.tolist(),
     'CRE': (df['infect'] == 1).tolist(),
     'P_I': (df['test'] < df['in'] + date_n) & (df['infect'] == 1),
     'P_HAI': ((df['in'] + date_n <= df['test']) & (df['test'] <= df['out'] + date_m)) & (df['infect'] == 1)}
period_icu = pd.DataFrame(a)


#%%
# 데이터의 분포에 적합한 지수함수 만들기
lam = 1/np.mean(period_icu['date_diff'])
x = np.linspace(min(period_icu['date_diff']), max(period_icu['date_diff']), 100)
y = lam * np.exp(- lam * x)

plt.hist(period_icu['date_diff'], bins=40, color='blue',alpha =0.3, density=True,label='Total patients')
plt.plot(x, y, 'k--', label=f'Exponential Function E[X] = {1/lam:.2f}')
plt.title('ICU Hospitalization period (2017-2018)')
plt.xlabel('Days')
plt.ylabel('Probability density')
plt.legend()
plt.show()
# %%
# 'date_diff' 열의 평균값과 중앙값 계산
mean_value = np.mean(period_icu['date_diff'])
median_value = np.median(period_icu['date_diff'])

# 히스토그램 생성
plt.hist(period_icu['date_diff'], bins=30, color='lightblue')
plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=1, label=f'Mean: {mean_value:.2f}')
plt.axvline(median_value, color='green', linestyle='dashed', linewidth=1, label=f'Median: {median_value}')
plt.xlabel('Date Difference')
plt.ylabel('Frequency')
plt.title('ICU hospitalization period (2017-2018)')
plt.legend()
plt.grid(True)
plt.show()

# %%

cre_true_df = period_icu[period_icu['CRE'] == 1]
cre_false_df = period_icu[period_icu['CRE'] == 0]

# 'date_diff' 열의 평균값과 중앙값 계산
mean_value_t = np.mean(cre_true_df['date_diff'])
median_value_t = np.median(cre_true_df['date_diff'])
mean_value_f = np.mean(cre_false_df['date_diff'])
median_value_f = np.median(cre_false_df['date_diff'])

# 히스토그램 생성
plt.figure(figsize=(10,4))
plt.subplot(121)
plt.hist(cre_true_df['date_diff'], bins=30, color='pink')
plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=1, label=f'Mean: {mean_value_t:.2f}')
plt.axvline(median_value, color='green', linestyle='dashed', linewidth=1, label=f'Median: {median_value_t}')
plt.xlabel('Date Difference')
plt.ylabel('Frequency')
plt.title('ICU hospitalization period (CRE Positive)')
plt.legend()
plt.grid(True)
plt.subplot(122)
plt.hist(cre_false_df['date_diff'], bins=30, color='lightgreen')
plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=1, label=f'Mean: {mean_value_f:.2f}')
plt.axvline(median_value, color='green', linestyle='dashed', linewidth=1, label=f'Median: {median_value_f}')
plt.xlabel('Date Difference')
plt.ylabel('Frequency')
plt.title('ICU hospitalization period (CRE Negative)')
plt.legend()
plt.grid(True)
plt.show()
# %%

cre_true_df = period_icu[period_icu['P_I'] == 1]
cre_false_df = period_icu[period_icu['P_I'] == 0]

# 'date_diff' 열의 평균값과 중앙값 계산
mean_value_t = np.mean(cre_true_df['date_diff'])
median_value_t = np.median(cre_true_df['date_diff'])
mean_value_f = np.mean(cre_false_df['date_diff'])
median_value_f = np.median(cre_false_df['date_diff'])

# 히스토그램 생성
plt.figure(figsize=(10,4))
plt.subplot(121)
plt.hist(cre_true_df['date_diff'], bins=30, color='pink')
plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=1, label=f'Mean: {mean_value_t:.2f}')
plt.axvline(median_value, color='green', linestyle='dashed', linewidth=1, label=f'Median: {median_value_t}')
plt.xlabel('Date Difference')
plt.ylabel('Frequency')
plt.title('ICU hospitalization period (CRE Positive)')
plt.legend()
plt.grid(True)
plt.subplot(122)
plt.hist(cre_false_df['date_diff'], bins=30, color='lightgreen')
plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=1, label=f'Mean: {mean_value_f:.2f}')
plt.axvline(median_value, color='green', linestyle='dashed', linewidth=1, label=f'Median: {median_value_f}')
plt.xlabel('Date Difference')
plt.ylabel('Frequency')
plt.title('ICU hospitalization period (CRE Negative)')
plt.legend()
plt.grid(True)
plt.show()
# %%
