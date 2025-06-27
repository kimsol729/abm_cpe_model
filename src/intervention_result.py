
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import ast
# load data B
df = pd.read_csv('../result/intervention/B1_50_B3_100_copy.csv')
# Probability Transmission b
plt.hist(df['prob_transmission'], bins=30, color='skyblue', edgecolor='none')
plt.xlabel('prob_transmission')
plt.ylabel('Frequency')
plt.title('Histogram of prob_transmission')
plt.grid(True)
plt.show()

#
df_hand = df.iloc[:, 2:6]
def convert_to_list(text):
    return ast.literal_eval(text)
B_hand = np.array([df_hand.iloc[i].values.tolist() for i in range(len(df_hand))])
B_hand1 = np.array([convert_to_list(B_hand[i][0]) for i in range(len(B_hand))]).reshape(150, 19)
B_hand2 = np.array([convert_to_list(B_hand[i][1]) for i in range(len(B_hand))]).reshape(150, 19)
B_hand3 = np.array([convert_to_list(B_hand[i][2]) for i in range(len(B_hand))]).reshape(150, 19)
B_hand4 = np.array([convert_to_list(B_hand[i][3]) for i in range(len(B_hand))]).reshape(150, 19)

matrices = [B_hand1, B_hand2, B_hand3, B_hand4]
# labels = ['80%', '90%', '95%', '99%']
# labels = ['30 days', '60 days', '90 days', '180 days']
labels = ['3 days', '7 days', '10 days', '14 days']
#
# B x축 라벨: '2021-01' ~ '2023-12'
x_labels = pd.date_range(start='2017-01-01', periods=19, freq='MS').strftime('%Y-%m')

plt.figure(figsize=(14, 8))

for data, label in zip(matrices, labels):
    # 누적합 (각 샘플에 대해 열 방향 누적합)
    cumsum_data = np.cumsum(data, axis=1)  # shape (150, 36)

    # 평균값 (상하위 5% 제거 후 평균) 계산
    trimmed_means = []
    q1_vals = []
    q3_vals = []

    for col in range(cumsum_data.shape[1]):
        column_data = cumsum_data[:, col]

        # 분위 계산
        lower = np.percentile(column_data, 5)
        upper = np.percentile(column_data, 95)

        # 5% ~ 95% 범위 내 값만 선택
        trimmed = column_data[(column_data >= lower) & (column_data <= upper)]

        # 평균 및 분위수
        trimmed_means.append(np.mean(trimmed))
        q1_vals.append(np.percentile(column_data, 25))
        q3_vals.append(np.percentile(column_data, 75))

    x = np.arange(19)
    trimmed_means = np.array(trimmed_means)
    q1_vals = np.array(q1_vals)
    q3_vals = np.array(q3_vals)

    # 평균값 그래프
    plt.plot(x, trimmed_means, label=f'{label} trimmed mean', linewidth=2)

    # IQR 영역
    plt.fill_between(x, q1_vals, q3_vals, alpha=0.2)

# x축 설정
plt.xticks(ticks=np.arange(19), labels=x_labels, rotation=45)
plt.title('Delayed Isolation Time(2021–2023)')
plt.xlabel('Month')
plt.ylabel('Cumulative Sum')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# #%%

# hand_hygiene_rates = [80, 90, 95, 99]
# env_cleaning_intervals = [30, 60, 90, 180]
# isolation_delays = [3, 7, 10, 14]

# hai_hand = [120, 90, 70, 40]     # 손소독률에 따른 감염자 수
# hai_cleaning = [50, 65, 85, 120] # 청소주기에 따른 감염자 수
# hai_isolation = [45, 65, 80, 100] # 격리지연시간에 따른 감염자 수

# # Figure and subplots
# fig, axes = plt.subplots(2, 3, figsize=(18, 10))
# fig.suptitle('Impact of Infection Control Measures on Healthcare-Associated Infections', fontsize=16)

# # Column titles
# column_titles = ['Effect of Hand Hygiene Rate on HAIs',
#                  'Effect of Environmental Cleaning on HAIs',
#                  'Effect of Isolation Delay on HAIs']

# # Set titles
# for col, title in enumerate(column_titles):
#     axes[0, col].set_title(title, fontsize=14)

# # Plot: Top row
# axes[0, 0].plot(hand_hygiene_rates, hai_hand, marker='o')
# axes[0, 1].plot(env_cleaning_intervals, hai_cleaning, marker='s', color='green')
# axes[0, 2].plot(isolation_delays, hai_isolation, marker='^', color='red')

# # Duplicate same plots in bottom row for any variation later
# axes[1, 0].plot(hand_hygiene_rates, hai_hand, marker='o')
# axes[1, 1].plot(env_cleaning_intervals, hai_cleaning, marker='s', color='green')
# axes[1, 2].plot(isolation_delays, hai_isolation, marker='^', color='red')

# # Axis labels
# for ax in axes[:, 0]:
#     ax.set_xlabel('Hand Hygiene Rate (%)')
#     ax.set_ylabel('Number of HAIs')

# for ax in axes[:, 1]:
#     ax.set_xlabel('Environmental Cleaning Interval (days)')
#     ax.set_ylabel('Number of HAIs')

# for ax in axes[:, 2]:
#     ax.set_xlabel('Isolation Delay Time (days)')
#     ax.set_ylabel('Number of HAIs')

# # Grid & layout
# for row in axes:
#     for ax in row:
#         ax.grid(True)

# plt.tight_layout(rect=[0, 0.03, 1, 0.95])
# plt.show()


# # %%
