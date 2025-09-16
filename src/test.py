import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
        matrices = [np.array([convert_to_list(type_interv[i][j]) for i in range(len(type_interv))]).reshape(150, length)
                    for j in range(4)]

        q1_all, q3_all = [], []
        for data in matrices:
            cumsum = np.cumsum(data, axis=1)
            q1_all += np.percentile(cumsum, 25, axis=0).tolist()
            q3_all += np.percentile(cumsum, 75, axis=0).tolist()
        y_min, y_max = min(q1_all), max(q3_all)
        y_pad = (y_max - y_min) * 0.05
        y_lim = (0, y_max + y_pad)

        filename = "../data/dataA_per_months.csv" if type_ == 'A' else "../data/dataB_per_months.csv"
        df2 = pd.read_csv(filename, sep=",")
        if df2.columns[0] == 'Unnamed: 0':
            df2.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
        df2['PHAI_cumsum'] = df2['PHAI_counts'].cumsum()

        fig, ax1 = plt.subplots(figsize=(12, 8))
        for data, label in zip(matrices, labels):
            cumsum = np.cumsum(data, axis=1)
            q2 = np.percentile(cumsum, 50, axis=0)
            # q2 = np.mean(cumsum, axis=0)
            q1 = np.percentile(cumsum, 25, axis=0)
            q3 = np.percentile(cumsum, 75, axis=0)
            x = np.arange(length)
            ax1.plot(x, q2, label=f'{label} median', linewidth=3)
            ax1.fill_between(x, q1, q3, alpha=0.2)
        
        ax1.plot(np.arange(len(df2['PHAI_cumsum'])), df2['PHAI_cumsum'],
                 marker='*', color='black', linestyle='None', label='PHAI cumulative counts')
        if type_=='B'and intvn == 'hand':
            ax1.set_ylim([0,80])
        else:
            ax1.set_ylim(y_lim)
        ax1.grid()
        ax1.set_ylabel('PHAI cumulative counts')
        ax1.set_xticks(np.arange(length))
        ax1.set_xticklabels(x_labels, rotation=45)

        ax2 = ax1.twinx()
        ax2.bar(np.arange(len(df2['PI_counts'])), df2['PI_counts'],
                color='tab:grey', alpha=0.4, label='Input patients')
        ax2.set_ylim(0, 10)
        ax2.set_ylabel('Input patients', color='tab:orange')
        ax2.tick_params(axis='y', labelcolor='tab:orange')

        lines, labels_comb = [], []
        for ax in [ax1, ax2]:
            l, lb = ax.get_legend_handles_labels()
            lines += l
            labels_comb += lb
        ax1.legend(lines, labels_comb, loc='upper left')
        # ax1.spines['bottom'].set_visible(False)
        # ax2.spines['bottom'].set_visible(False)

        plt.title(f'Input patients (bar), PHAI (*), Intervention - Type {type_} - {intvn}')
        plt.tight_layout()
        plt.savefig(f'../result/intervention/figureNtable/combined_{type_}_{intvn}.png')
        # plt.show()