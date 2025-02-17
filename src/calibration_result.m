clc; clear; close all;
restoredefaultpath;

%%
beta_a = readmatrix('../data/calibration_beta_A.csv', 'Range', 'B2:B200000');
beta_b = readmatrix('../data/calibration_beta_B.csv', 'Range', 'B2:B200000');

figure(1);

hold on
binWidth_a = (max(beta_a) - min(beta_a)) / 70;
histogram(beta_a, 'BinWidth', binWidth_a, 'Normalization', 'probability')
binWidth_b = (max(beta_b) - min(beta_b)) / 50;
histogram(beta_b, 'BinWidth', binWidth_b, 'Normalization', 'probability')

mean_a = mean(beta_a)
std_a = std(beta_a);
mean_b = mean(beta_b)
yLimits_b = ylim;

yLimits_a = ylim;

plot([mean_a, mean_a], yLimits_a, 'k', 'LineWidth', 2);
plot([mean_b, mean_b], yLimits_b, 'k', 'LineWidth', 2);
title('Histogram of beta')
% xlim([0.065, 0.105])
xlabel('Values')
ylabel('Frequency')
hold off
% 
% figure(2);
% binWidth_b = (max(beta_b) - min(beta_b)) / 100;
% histogram(beta_b, 'BinWidth', binWidth_b);
% % xlim([0.065, 0.105]);
% hold on;
% mean_b = mean(beta_b)
% yLimits_b = ylim;
% plot([mean_b, mean_b], yLimits_b, 'k', 'LineWidth', 2);
% title('Histogram of beta_b');
% xlabel('Values');
% ylabel('Frequency');
% hold off;
% 
% 
% 
% 그래프 설정
title('Histogram of beta', 'FontSize', 14);
xlabel('beta', 'FontSize', 12);
ylabel('Frequency', 'FontSize', 12);
grid on;


%%
clc
clear
clf
close all
data = readcell('../result/emulation_beta_A.csv', 'Range', 'B2:Z100');
P_HAI_b = readmatrix('../result/emulation_beta_A.csv', 'Range', 'B2:B200000');
data_cleaned = regexprep(data, '[,\[\]]', '');

% 2. 문자열을 숫자형 데이터로 변환
numeric_data = cellfun(@str2double, data_cleaned);

% 결과 확인
plot((numeric_data'))
ylim([0, 100])

