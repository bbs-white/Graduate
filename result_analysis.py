import cv2
import numpy as np
import os
import math
import csv

inplay = 1
out = 0

data_MS_real = []
data_MS_real_serve = []
data_MS_real_end = []
data_MS_pre = []
data_MS_pre_serve = []
data_MS_pre_end = []


length_real = []
length_pre = []

print('Input Data ...')
frame_num = [7341, 10433, 9683, 10938, 8827, 8414]
for i in range(len(frame_num)):
    data_MS_pre.append([])
    data_MS_real.append([])
    for j in range(frame_num[i]):
        data_MS_pre[i].append(out)
        data_MS_real[i].append(out)

data_MS_pre_serve.append([295, 677, 851,  1266, 2606, 3243, 3769, 4666, 5524, 6168, 6801, 7300])
data_MS_pre_end.append([487, 769, 1029, 2198, 2962, 3489, 4496, 5140, 5998, 6628, 7127, 7340])
data_MS_pre_serve.append([8, 423, 927, 1456, 1871, 2493, 3490, 3879, 4615, 5537, 5975, 6884, 7873, 8387, 8637, 9079, 9513, 10086])
data_MS_pre_end.append([205, 757, 1273, 1655, 2206, 3320, 3666, 4020, 5367, 5805, 6702, 7260, 8159, 8467, 8905, 9343, 9842, 10432])
data_MS_pre_serve.append([66, 568, 1091, 1367, 1737, 2201, 2606, 3377, 3784, 4311, 4868, 5596, 6199, 6734, 7214, 7833, 8863])
data_MS_pre_end.append([398, 673, 1163, 1567, 2025, 2436, 3185, 3614, 4229, 4698, 5207, 6027, 6564, 7044, 7488, 8693, 9683])
data_MS_pre_serve.append([8, 467, 984, 1254, 1556, 3016, 3353, 4035, 5825, 6254, 7463, 8260, 9128, 9828, 10066, 10337])
data_MS_pre_end.append([297, 903, 1084, 1365, 2846, 3093, 3613, 5743, 6084, 7293, 8090, 8937, 9658, 9896, 10167, 10937])
data_MS_pre_serve.append([8, 722, 1009, 1294, 1824, 2456, 2983, 3243, 3523, 4250, 5285, 6207, 6525, 6759, 7862, 8673])
data_MS_pre_end.append([522, 839, 1121, 1603, 2286, 2785, 3073, 3352, 3900, 5115, 5851, 6308, 6589, 7692, 8503, 8826])
data_MS_pre_serve.append([395, 855, 1226, 3405, 3747, 6106, 6564, 7500])
data_MS_pre_end.append([685, 1048, 3235, 3577, 5936, 6394, 7258, 8413])
data_MS_real_serve.append([18, 589, 1229, 1645, 1939, 2412, 2740, 3101, 3444, 3731, 4464, 4773, 5095, 5355, 5737, 6114, 6363, 6771, 7087])
data_MS_real_end.append([270, 875, 1290, 1721, 2011, 2490, 2824, 3188, 3500, 3817, 4571, 4916, 5154, 5481, 5782, 6196, 6501, 6889, 7293])
data_MS_real_serve.append([10, 392, 822, 1334, 1822, 2165, 2572, 2964, 3376, 4299, 4722, 5157, 5495, 5914, 6418, 6857, 7323, 7905, 8567, 8969, 9457, 9910, 10288])
data_MS_real_end.append([209, 591, 1111, 1550, 1879, 2329, 2696, 3075, 3983, 4465, 4883, 5229, 5666, 6099, 6527, 7091, 7571, 8266, 8696, 9180, 9595, 10008, 10406])
data_MS_real_serve.append([32, 280, 819, 1239, 1779, 2136, 2529, 2891, 3204, 3697, 3994, 4291, 4764, 5310, 6012, 6317, 6849, 7169, 7718, 8312, 8812, 9256, 9573])
data_MS_real_end.append([66, 541, 994, 1432, 1835, 2271, 2627, 2956, 3477, 3758, 4070, 4473, 5034, 5721, 6083, 6523, 6915, 7329, 7985, 8386, 8954, 9330, 9651])
data_MS_real_serve.append([22, 339, 664, 965, 1495, 2141, 2453, 2976, 3302, 3563, 3973, 4339, 4643, 4953, 5219, 5634, 6160, 6480, 6805, 7104, 7336, 7826, 8198, 8505, 8928, 9794, 10827])
data_MS_real_end.append([163, 474, 774, 1292, 1879, 2316, 2757, 3103, 3352, 3716, 4079, 4433, 4748, 5035, 5399, 5799, 6225, 6614, 6903, 7182, 7564, 7944, 8326, 8702, 9385, 10059, 10895])
data_MS_real_serve.append([35, 427, 915, 1354, 1676, 2178, 2642, 3247, 3554, 3950, 4373, 4855, 5148, 5453, 5957, 6347, 6783, 7800, 8180, 8618])
data_MS_real_end.append([197, 679, 1113, 1471, 1869, 2368, 2918, 3333, 3761, 4140, 4546, 4948, 5238, 5696, 6049, 6507, 6974, 7948, 8365, 8788])
data_MS_real_serve.append([59, 351, 756, 1144, 1998, 2272, 2707, 3340, 3650, 4048, 4494, 4798, 5330, 5728, 6024, 6451, 6979, 7497, 7743, 8206])
data_MS_real_end.append([115, 486, 864, 1385, 2061, 2497, 2994, 3424, 3735, 4133, 4587, 5019, 5445, 5785, 6171, 6621, 7152, 7527, 7941, 8386])

for a in range(len(frame_num)):
    length_pre.append(len(data_MS_pre_serve[a]))
    length_real.append(len(data_MS_real_serve[a]))
    for b in range(length_pre[a]):
        for c in range(data_MS_pre_serve[a][b], data_MS_pre_end[a][b]):
            data_MS_pre[a][c] = inplay
    for b in range(length_real[a]):
        for c in range(data_MS_real_serve[a][b], data_MS_real_end[a][b]):
            data_MS_real[a][c] = inplay

print('Calculation rally length ...')
Rally_length = []
Rally_length_ave = []
for i in range(len(frame_num)):
    Rally_length.append([])
    for j in range(length_real[i]):
        Rally_length[i].append(data_MS_real_end[i][j] - data_MS_real_serve[i][j])
    Rally_length_ave.append(round(sum(Rally_length[i])/length_pre[i]))

Long_Rally = []
for a in range(len(frame_num)):
    Long_Rally.append([])
    for b in range(length_real[a]):
        if (Rally_length[a][b] >= Rally_length_ave[a]):
            Long_Rally[a].append(True)
        else:
            Long_Rally[a].append(False)

print('Calculation Service frame Diff ...')
serve_diff = []
serve_diff_sum = []
serve_diff_ave = []
for a in range(len(frame_num)):
    serve_diff.append([])
    for b in range(length_real[a]):
        min = frame_num[a]
        for c in range(length_pre[a]):
            t = abs(data_MS_real_serve[a][b] - data_MS_pre_serve[a][c])
            if (t < min):
                min = t
        serve_diff[a].append(min)
    serve_diff_sum.append(sum(serve_diff[a]))
    serve_diff_ave.append(round(serve_diff_sum[a]/length_real[a]))

print(serve_diff_sum)
print(serve_diff_ave)

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
        if (data_MS_real[a][b] == inplay and data_MS_pre[a][b] == inplay):
            True_positive[a] = True_positive[a] + 1
        elif (data_MS_real[a][b] == inplay and data_MS_pre[a][b] == out):
            False_negative[a] = False_negative[a] + 1
        elif (data_MS_real[a][b] == out and data_MS_pre[a][b] == inplay):
            False_positive[a] = False_positive[a] + 1
        elif (data_MS_real[a][b] == out and data_MS_pre[a][b] == out):
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
