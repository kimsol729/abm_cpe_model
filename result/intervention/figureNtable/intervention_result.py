import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import ast

def convert_to_list(text):
    return ast.literal_eval(text)

for type_ in ['A', 'B']:
    for intvn in ['hand', 'clean', 'iso']:
        df = pd.read_csv(f'../result/intervention/{type_}_{intvn}.csv')
        length = 19 if type_ == 'A' else 36
        x_labels = pd.date_range(start='2017-01-01' if type_ == 'A' else '2021-01-01',
                                 periods=length, freq='MS').strftime('%Y-%m')
        labels = {'hand': ['80%', '90%', '95%', '99%'],
                  'clean': ['30 days', '60 days', '90 days', '180 days'],
                  'iso': ['3 days', '7 days', '10 days', '14 days']}[intvn]

        df_inter = df.iloc[:, 2:6]
        type_interv = np.array([df_inter.iloc[i].values.tolist() for i in range(len(df_inter))])
        interv1 = np.array([convert_to_list(type_interv[i][0]) for i in range(len(type_interv))]).reshape(150, length)
        interv2 = np.array([convert_to_list(type_interv[i][1]) for i in range(len(type_interv))]).reshape(150, length)
        interv3 = np.array([convert_to_list(type_interv[i][2]) for i in range(len(type_interv))]).reshape(150, length)
        interv4 = np.array([convert_to_list(type_interv[i][3]) for i in range(len(type_interv))]).reshape(150, length)

        matrices = [interv1, interv2, interv3, interv4]

        for i, mat in enumerate(matrices):
            pd.DataFrame(mat).to_csv(f'matrix_{type_}_{intvn}_{labels[i]}.csv', index=False)

        plt.figure(figsize=(14, 8))
        for data, label in zip(matrices, labels):
            cumsum_data = np.cumsum(data, axis=1)
            q2_vals = np.percentile(cumsum_data, 50, axis=0)
            q1_vals = np.percentile(cumsum_data, 25, axis=0)
            q3_vals = np.percentile(cumsum_data, 75, axis=0)
            x = np.arange(length)
            plt.plot(x, q2_vals, label=f'{label} median', linewidth=2)
            plt.fill_between(x, q1_vals, q3_vals, alpha=0.2)
        plt.xticks(ticks=np.arange(length), labels=x_labels, rotation=45)
        plt.xlabel('Month')
        plt.ylabel('Cumulative Sum')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'lineplot_{type_}_{intvn}.png')
        plt.close()

        q1_all, q3_all = [], []
        for data in matrices:
            cumsum = np.cumsum(data, axis=1)
            q1_all += [np.percentile(cumsum[:, i], 25) for i in range(cumsum.shape[1])]
            q3_all += [np.percentile(cumsum[:, i], 75) for i in range(cumsum.shape[1])]
        y_min, y_max = min(q1_all), max(q3_all)
        y_pad = (y_max - y_min) * 0.05
        y_lim = (y_min - y_pad, y_max + y_pad)

        plt.figure(figsize=(16, 10))
        for i, (data, label) in enumerate(zip(matrices, labels)):
            ax = plt.subplot(2, 2, i + 1)
            cumsum = np.cumsum(data, axis=1)
            x = np.arange(cumsum.shape[1])
            q1 = np.percentile(cumsum, 25, axis=0)
            q3 = np.percentile(cumsum, 75, axis=0)
            med = np.percentile(cumsum, 50, axis=0)
            for xi, y1, y3 in zip(x, q1, q3):
                ax.add_patch(plt.Rectangle((xi - 0.3, y1), 0.6, y3 - y1,
                                           facecolor='lightblue', edgecolor='blue', alpha=0.5))
            ax.plot(x, med, 'o-', color='red', label='Median')
            ax.set_xticks(x)
            ax.set_xticklabels(x_labels, rotation=45)
            ax.set_ylim(y_lim)
            ax.set_title(label)
            ax.grid(True)
            ax.legend()
        plt.tight_layout()
        plt.savefig(f'boxplot_{type_}_{intvn}.png')
        plt.close()