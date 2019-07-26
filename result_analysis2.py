import cv2
import numpy as np
import os
import math
import xlrd
import pprint

excel_fn = 'detect_rally_2.xlsx'
wb = xlrd.open_workbook(excel_fn)

sheet = wb.sheet_by_name('Sheet1')
frame_num = [7341, 10433, 9683, 10938, 8827, 8414]
data_MS_pre = []
data_MS_real = []
for a in range(len(frame_num)):
    data_MS_pre.append([])
    for b in range(frame_num[a]):
        data_MS_pre[a].append(sheet.cell_value(a, b))
for a in range(len(frame_num)):
    data_MS_real.append([])
    for b in range(frame_num[a]):
        data_MS_real[a].append(sheet.cell_value(a+6, b))

for i in range(len(frame_num)):
    for j in range(frame_num[i]):
        if (data_MS_pre[i][j] > 0):
            data_MS_pre[i][j] = True
        if (data_MS_pre[i][j] < 0):
            data_MS_pre[i][j] = False
        if (data_MS_real[i][j] > 0):
            data_MS_real[i][j] = True
        if (data_MS_real[i][j] < 0):
            data_MS_real[i][j] = False

print('Calculation All Diff ...')
True_positive = [0,0,0,0,0,0]
True_negative = [0,0,0,0,0,0]
False_negative = [0,0,0,0,0,0]
False_positive = [0,0,0,0,0,0]
Recall = [0,0,0,0,0,0]
Accuracy = [0,0,0,0,0,0]
Precision = [0,0,0,0,0,0]
Fmeasure = [0,0,0,0,0,0]
for a in range(len(frame_num)):
    for b in range(frame_num[a]):
        if (data_MS_real[a][b] == True and data_MS_pre[a][b] == True):
            True_positive[a] = True_positive[a] + 1
        elif (data_MS_real[a][b] == True and data_MS_pre[a][b] == False):
            False_negative[a] = False_negative[a] + 1
        elif (data_MS_real[a][b] == False and data_MS_pre[a][b] == True):
            False_positive[a] = False_positive[a] + 1
        elif (data_MS_real[a][b] == False and data_MS_pre[a][b] == False):
            True_negative[a] = True_negative[a] + 1
for i in range(len(frame_num)):
    Recall[i] = True_positive[i]/(True_positive[i]+False_negative[i])
    Accuracy[i] = (True_positive[i]+True_negative[i])/frame_num[i]
    Precision[i] = True_positive[i]/(True_positive[i]+False_positive[i])
    Fmeasure[i] = 2*Recall[i]*Precision[i]/(Recall[i]+Precision[i])
    Recall[i] = round(Recall[i]*1000)/1000
    Accuracy[i] = round(Accuracy[i]*1000)/1000
    Precision[i] = round(Precision[i]*1000)/1000
    Fmeasure[i] = round(Fmeasure[i]*1000)/1000

Tp_sum = sum(True_positive)
Tn_sum = sum(True_negative)
Fp_sum = sum(False_positive)
Fn_sum = sum(False_negative)
R_sum = Tp_sum/(Tp_sum + Fn_sum)
A_sum = (Tp_sum + Tn_sum)/sum(frame_num)
P_sum = Tp_sum/(Tp_sum + Fp_sum)
F_sum = 2*R_sum*P_sum/(R_sum + P_sum)

R_sum = round(R_sum*1000)/1000
A_sum = round(A_sum*1000)/1000
P_sum = round(P_sum*1000)/1000
F_sum = round(F_sum*1000)/1000
print(Tp_sum, Tn_sum, Fp_sum, Fn_sum)
print(R_sum, A_sum, P_sum, F_sum)
