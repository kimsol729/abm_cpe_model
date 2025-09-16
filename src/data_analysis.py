#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.dates as mdates
import datetime
import seaborn as sns
#%% load the file
current_directory = os.getcwd()
file_path = 'data/2023_organized.csv'
data = pd.read_csv(file_path)

#%% DATA PROCESSING
zero_count = (data['hospitalization_period'] == 0).sum()  # 데이터 오류
nan_count = data['hospitalization_period'].isna().sum()  # 아직 퇴원을 안한 환자
refine_data = data[(data['hospitalization_period'].notna()) & (data['hospitalization_period'] != 0)]
refine_data = refine_data.drop([18, 266, 354, 488]) # 중복입력 제거
# 결과 출력
print(f"* Current hospitalization: {nan_count}")
print(f"* 전출<전입: {zero_count}")
print("* NaN 및 0값, 중복 이 제거된 데이터의 shape:", refine_data.shape)

# 데이터의 분포에 적합한 지수함수 만들기
lam = 1/np.mean(refine_data['hospitalization_period'])
x = np.linspace(min(refine_data['hospitalization_period']), max(refine_data['hospitalization_period']), 100)
y = lam * np.exp(- lam * x)

plt.hist(refine_data['hospitalization_period'], bins=40, color='blue',alpha =0.3, density=True,label='Total patients')
plt.plot(x, y, 'k--', label=f'Exponential Function E[X] = {1/lam:.2f}')
plt.title('ICU Hospitalization period')
plt.xlabel('Days')
plt.ylabel('Probability density')
plt.legend()
plt.show()


#%%

# year별 hospitalization_period의 중앙값 계산 및 출력
for year in range(6):
    median_value = np.median(refine_data[refine_data['year'] == year]['hospitalization_period'])
    print(f"Year {year}: Median hospitalization period = {median_value}")

#%%
S = refine_data[refine_data['infect'] == 0]
I = refine_data[refine_data['infect'] == 1]
S_period = S['hospitalization_period']
I_period = I['hospitalization_period']

plt.figure(figsize=(10,4))
plt.subplot(121)
plt.hist(S_period, bins=30, color='pink')
plt.axvline(np.mean(S_period), color='red', linestyle='dashed', linewidth=1, label=f'Mean: {np.mean(S_period):.2f}')
plt.axvline(np.median(S_period), color='green', linestyle='dashed', linewidth=1, label=f'Median: {np.median(S_period)}')
plt.xlabel('Date Difference')
plt.ylabel('Frequency')
plt.title('ICU hospitalization period (CRE Positive)')
plt.legend()
plt.grid(True)
plt.subplot(122)
plt.hist(I_period, bins=30, color='lightgreen')
plt.axvline(np.mean(I_period), color='red', linestyle='dashed', linewidth=1, label=f'Mean: {np.mean(I_period):.2f}')
plt.axvline(np.median(I_period), color='green', linestyle='dashed', linewidth=1, label=f'Median: {np.median(I_period)}')
plt.xlabel('Date Difference')
plt.ylabel('Frequency')
plt.title('ICU hospitalization period (CRE Negative)')
plt.legend()
plt.grid(True)
plt.show()

# %%
# infect 컬럼을 기준으로 데이터 분할
S = refine_data[refine_data['infect'] == 0]
I = refine_data[refine_data['infect'] == 1]
S_period = S['hospitalization_period']
I_period = I['hospitalization_period']

# # 재원기간 분포 시각화
# plt.figure(figsize=(12, 6))

# # infect가 0일 때의 재원기간 분포
# plt.subplot(1, 2, 1)
# plt.hist(S_period, bins=40, color='lightblue', density=True,label='Susceptible')
# x = np.linspace(min(S_period), max(I_period), 100)
# lam = 1/np.mean(S_period)
# y = lam * np.exp(- lam * x)
# plt.plot(x, y, 'b--', label=f'Exponential Function E[X]= {1/lam:.2f}')
# plt.title('Non infect')
# plt.xlabel('ICU Hospitalization period')
# plt.ylabel('probability')
# plt.legend()

# # infect가 1일 때의 재원기간 분포
# plt.subplot(1, 2, 2)
# plt.hist(I_period,bins=40, color='pink', density=True,label='Infectious')
# x = np.linspace(min(I_period), max(I_period), 100)
# lam = 1/np.mean(I_period)
# y = lam * np.exp(- lam * x)
# plt.plot(x, y, 'r--', label=f'Exponential Function E[X]= {1/lam:.2f}')
# plt.title('CRE infect')
# plt.xlabel('ICU Hospitalization period')
# plt.ylabel('probability')
# plt.legend()
# plt.tight_layout()
# plt.show()

I_count = (refine_data['infect'] == 1).sum()
S_count = (refine_data['infect'] == 0).sum()
print("The number of Susceptiable: ", S_count)
print("The number of Infectious: ", I_count)

bin_width = 5
min_val = min(np.min(S_period), np.min(I_period))
max_val = max(np.max(S_period), np.max(I_period))
bins = np.arange(min_val, max_val + bin_width, bin_width)
# 첫 번째 그래프: Non infect
# plt.figure(figsize=(8, 6))

plt.hist(S_period, bins=bins, color='lightblue', density=True, label='Susceptible')
x1 = np.linspace(min(S_period), max(I_period), 100)
lam1 = 1 / np.mean(S_period)
y1 = lam1 * np.exp(-lam1 * x1)
plt.plot(x1, y1, 'b--', label=f'Exponential Function E[X]= {1/lam1:.2f}')

# 두 번째 그래프: CRE infect
plt.hist(I_period, bins=bins, color='pink', density=True, label='Infectious', alpha=0.7)  # alpha 값을 통해 투명도 조절
x2 = np.linspace(min(I_period), max(I_period), 100)
lam2 = 1 / np.mean(I_period)
y2 = lam2 * np.exp(-lam2 * x2)
plt.plot(x2, y2, 'r--', label=f'Exponential Function E[X]= {1/lam2:.2f}')

# 그래프 세부 설정
plt.title('ICU Hospitalization Period Distribution')
plt.xlabel('ICU Hospitalization period')
plt.ylabel('Probability')
plt.legend()
plt.grid(True)

plt.show()
# %%
P_I = refine_data[refine_data['P^I'] == 1]
non_P_I = refine_data[refine_data['P^I'] == 0]

PI_period = P_I['hospitalization_period']
non_period = non_P_I['hospitalization_period']

# 재원기간 분포 시각화
plt.figure(figsize=(12, 6))

# infect가 0일 때의 재원기간 분포
plt.subplot(1, 2, 1)
plt.hist(non_period, bins=40, color='lightblue', density=True,label='Non_PI_period')
x = np.linspace(min(non_period), max(non_period), 100)
lam = 1/np.mean(non_period)
y = lam * np.exp(- lam * x)
plt.plot(x, y, 'b--', label=f'Exponential Function E[X]= {1/lam:.2f}')
plt.title('Non infect')
plt.xlabel('ICU Hospitalization period')
plt.ylabel('probability')
plt.legend()

# infect가 1일 때의 재원기간 분포
plt.subplot(1, 2, 2)
plt.hist(PI_period,bins=40, color='pink', density=True,label='PI_Infectious')
x = np.linspace(min(PI_period), max(PI_period), 100)
lam = 1/np.mean(PI_period)
y = lam * np.exp(- lam * x)
plt.plot(x, y, 'r--', label=f'Exponential Function E[X]= {1/lam:.2f}')
plt.title('CRE infect')
plt.xlabel('ICU Hospitalization period')
plt.ylabel('probability')
plt.legend()
plt.tight_layout()
plt.show()
# %% CRE 양성, 검사 시기에 따른 분석
before = refine_data[refine_data['CRE_test_time'] == 0]
hospital = refine_data[refine_data['CRE_test_time'] == 1]
after = refine_data[refine_data['CRE_test_time'] == 2]
plt.plot(before['test_hospital'])
plt.plot(hospital['test_hospital'])
plt.plot(after['test_hospital'])
plt.show()
# %%
df = pd.read_csv('data/test_time.csv')
df = df[(df['duration']<40000)]
idx = pd.date_range(start='2021-01-08', end='2023-12-31', freq='D')

test_time = pd.DataFrame(index=idx)
for t in range(3):
    temp_df = df[df['type']==t].copy()
    temp_df['hospital_date'] = pd.to_datetime(temp_df['hospital_date'])
    temp_df = temp_df.groupby('hospital_date').mean()
    temp_df = temp_df.reindex(idx)
    test_time[f'type{t}']=temp_df['duration']

# %%
start_date = datetime.datetime.strptime('2021-01-01', '%Y-%m-%d')
end_date = datetime.datetime.strptime('2023-12-31', '%Y-%m-%d')
plt.figure(figsize=(10,10))
plt.subplot(311)
plt.scatter(test_time.index, test_time['type0'], s=7)
plt.ylabel('Before Hospitalization')
plt.xlim(start_date, end_date)
plt.ylim([-80,0])
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.subplot(312)
plt.scatter(test_time.index, test_time['type1'], s=7)
plt.ylabel('During Hospitalization')
plt.xlim(start_date, end_date)
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.subplot(313)
plt.scatter(test_time.index, test_time['type2'], s=7)
plt.ylabel('After Outpatient')
plt.xlim(start_date, end_date)
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.show()
# %%
# 데이터 불러오기
file_path = 'data/2023_infection_data.csv'
df = pd.read_csv(file_path)

# 날짜 형식으로 변환
df['in'] = pd.to_datetime(df['in'])
df['out'] = pd.to_datetime(df['out'])
df['test'] = pd.to_datetime(df['test'])

# 잘못된 데이터 제거
df.drop([18, 266, 354, 488], inplace=True)
df = df[df['in'] <= df['out']]
df = df.dropna(subset=['out'])

# 분석할 날짜 범위 설정
start_date = pd.Timestamp('2021-01-01')
end_date = pd.Timestamp('2024-01-01')
date_ranges = pd.date_range(start=start_date, end=end_date, freq='1MS')

#%%
num_ps = []

for i in range(len(date_ranges) - 1):
    start_range = date_ranges[i]
    end_range = date_ranges[i + 1]
    num_p = ((df['in'] >= start_range) & (df['in'] < end_range)).sum()
    num_ps.append(num_p)  # num_p 값을 num_ps 리스트에 추가

print(num_ps)  # 각 기간별 입원 환자 수가 담긴 리스트 출력
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
for n in range(0, 4, 3):
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

    plt.plot(PI_counts, '*-',label=f'n={n} (PI)')

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

# %%
# 데이터프레임으로 변환
date_labels = [date.strftime('%Y-%m') for date in date_ranges[:-1]]


df_PI = pd.DataFrame(PI_counts, columns=['PI_counts'], index=date_labels)
df_PHAI = pd.DataFrame(PHAI_counts, columns=['PHAI_counts'], index=date_labels)

# 하나의 DataFrame으로 결합
df_combined = pd.concat([df_PI, df_PHAI], axis=1)

# CSV 파일로 저장
df_combined.to_csv('data/dataB_per_months.csv', index=True)
# %%
