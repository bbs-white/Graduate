import cv2
import numpy as np
import os
import math
import csv

inplay = 1.1
out = -1.1

data1_S_1 = []
data1_S_2 = []
data1_S_3 = []
data1_S_4 = []
data1_S_5 = []
data1_S_6 = []
frame_num = [7341, 10433, 9683, 10938, 8827, 8414]

for i in range(7341):
    data1_S_1.append(out)
for i in range(10433):
    data1_S_2.append(out)
for i in range(9683):
    data1_S_3.append(out)
for i in range(10938):
    data1_S_4.append(out)
for i in range(8827):
    data1_S_5.append(out)
for i in range(8414):
    data1_S_6.append(out)

# data1_S_1の場合
for i in range(18, 270):
    data1_S_1[i] = inplay
for i in range(589, 875):
    data1_S_1[i] = inplay
for i in range(1229, 1290):
    data1_S_1[i] = inplay
for i in range(1645, 1721):
    data1_S_1[i] = inplay
for i in range(1939, 2011):
    data1_S_1[i] = inplay
for i in range(2412, 2490):
    data1_S_1[i] = inplay
for i in range(2740, 2824):
    data1_S_1[i] = inplay
for i in range(3101, 3188):
    data1_S_1[i] = inplay
for i in range(3444, 3500):
    data1_S_1[i] = inplay
for i in range(3731, 3817):
    data1_S_1[i] = inplay
for i in range(4464, 4571):
    data1_S_1[i] = inplay
for i in range(4773, 4916):
    data1_S_1[i] = inplay
for i in range(5095, 5154):
    data1_S_1[i] = inplay
for i in range(5355, 5481):
    data1_S_1[i] = inplay
for i in range(5737, 5782):
    data1_S_1[i] = inplay
for i in range(6114, 6196):
    data1_S_1[i] = inplay
for i in range(6363, 6501):
    data1_S_1[i] = inplay
for i in range(6771, 6889):
    data1_S_1[i] = inplay
for i in range(7087, 7293):
    data1_S_1[i] = inplay

# data1_S_2の場合
for i in range(10, 209):
    data1_S_2[i] = inplay
for i in range(392, 591):
    data1_S_2[i] = inplay
for i in range(822, 1111):
    data1_S_2[i] = inplay
for i in range(1334, 1550):
    data1_S_2[i] = inplay
for i in range(1822, 1879):
    data1_S_2[i] = inplay
for i in range(2165, 2329):
    data1_S_2[i] = inplay
for i in range(2572, 2696):
    data1_S_2[i] = inplay
for i in range(2964, 3075):
    data1_S_2[i] = inplay
for i in range(3376, 3983):
    data1_S_2[i] = inplay
for i in range(4299, 4465):
    data1_S_2[i] = inplay
for i in range(4722, 4883):
    data1_S_2[i] = inplay
for i in range(5157, 5229):
    data1_S_2[i] = inplay
for i in range(5495, 5666):
    data1_S_2[i] = inplay
for i in range(5914, 6099):
    data1_S_2[i] = inplay
for i in range(6418, 6527):
    data1_S_2[i] = inplay
for i in range(6857, 7091):
    data1_S_2[i] = inplay
for i in range(7323, 7571):
    data1_S_2[i] = inplay
for i in range(7905, 8266):
    data1_S_2[i] = inplay
for i in range(8567, 8696):
    data1_S_2[i] = inplay
for i in range(8969, 9180):
    data1_S_2[i] = inplay
for i in range(9457, 9595):
    data1_S_2[i] = inplay
for i in range(9910, 10008):
    data1_S_2[i] = inplay
for i in range(10288, 10406):
    data1_S_2[i] = inplay

# data1_S_3の場合
for i in range(32, 66):
    data1_S_3[i] = inplay
for i in range(280, 541):
    data1_S_3[i] = inplay
for i in range(819, 994):
    data1_S_3[i] = inplay
for i in range(1239, 1432):
    data1_S_3[i] = inplay
for i in range(1779, 1835):
    data1_S_3[i] = inplay
for i in range(2136, 2271):
    data1_S_3[i] = inplay
for i in range(2529, 2627):
    data1_S_3[i] = inplay
for i in range(2891, 2956):
    data1_S_3[i] = inplay
for i in range(3204, 3477):
    data1_S_3[i] = inplay
for i in range(3697, 3758):
    data1_S_3[i] = inplay
for i in range(3994, 4070):
    data1_S_3[i] = inplay
for i in range(4291, 4473):
    data1_S_3[i] = inplay
for i in range(4764, 5034):
    data1_S_3[i] = inplay
for i in range(5310, 5721):
    data1_S_3[i] = inplay
for i in range(6012, 6083):
    data1_S_3[i] = inplay
for i in range(6317, 6523):
    data1_S_3[i] = inplay
for i in range(6849, 6915):
    data1_S_3[i] = inplay
for i in range(7169, 7329):
    data1_S_3[i] = inplay
for i in range(7718, 7985):
    data1_S_3[i] = inplay
for i in range(8312, 8386):
    data1_S_3[i] = inplay
for i in range(8812, 8954):
    data1_S_3[i] = inplay
for i in range(9256, 9330):
    data1_S_3[i] = inplay
for i in range(9573, 9651):
    data1_S_3[i] = inplay

# data1_S_4の場合
for i in range(22, 163):
    data1_S_4[i] = inplay
for i in range(339, 474):
    data1_S_4[i] = inplay
for i in range(664, 774):
    data1_S_4[i] = inplay
for i in range(965, 1292):
    data1_S_4[i] = inplay
for i in range(1495, 1879):
    data1_S_4[i] = inplay
for i in range(2141, 2316):
    data1_S_4[i] = inplay
for i in range(2453, 2757):
    data1_S_4[i] = inplay
for i in range(2976, 3103):
    data1_S_4[i] = inplay
for i in range(3302, 3352):
    data1_S_4[i] = inplay
for i in range(3563, 3716):
    data1_S_4[i] = inplay
for i in range(3973, 4079):
    data1_S_4[i] = inplay
for i in range(4339, 4433):
    data1_S_4[i] = inplay
for i in range(4643, 4748):
    data1_S_4[i] = inplay
for i in range(4953, 5035):
    data1_S_4[i] = inplay
for i in range(5219, 5399):
    data1_S_4[i] = inplay
for i in range(5634, 5799):
    data1_S_4[i] = inplay
for i in range(6160, 6225):
    data1_S_4[i] = inplay
for i in range(6480, 6614):
    data1_S_4[i] = inplay
for i in range(6805, 6903):
    data1_S_4[i] = inplay
for i in range(7104, 7182):
    data1_S_4[i] = inplay
for i in range(7336, 7564):
    data1_S_4[i] = inplay
for i in range(7826, 7944):
    data1_S_4[i] = inplay
for i in range(8198, 8326):
    data1_S_4[i] = inplay
for i in range(8505, 8702):
    data1_S_4[i] = inplay
for i in range(8928, 9385):
    data1_S_4[i] = inplay
for i in range(9794, 10059):
    data1_S_4[i] = inplay
for i in range(10827, 10895):
    data1_S_4[i] = inplay

# data1_S_5の場合
for i in range(35, 197):
    data1_S_5[i] = inplay
for i in range(427, 679):
    data1_S_5[i] = inplay
for i in range(915, 1113):
    data1_S_5[i] = inplay
for i in range(1354, 1471):
    data1_S_5[i] = inplay
for i in range(1676, 1869):
    data1_S_5[i] = inplay
for i in range(2178, 2368):
    data1_S_5[i] = inplay
for i in range(2642, 2918):
    data1_S_5[i] = inplay
for i in range(3247, 3333):
    data1_S_5[i] = inplay
for i in range(3554, 3761):
    data1_S_5[i] = inplay
for i in range(3950, 4140):
    data1_S_5[i] = inplay
for i in range(4373, 4546):
    data1_S_5[i] = inplay
for i in range(4855, 4948):
    data1_S_5[i] = inplay
for i in range(5148, 5238):
    data1_S_5[i] = inplay
for i in range(5453, 5696):
    data1_S_5[i] = inplay
for i in range(5957, 6049):
    data1_S_5[i] = inplay
for i in range(6347, 6507):
    data1_S_5[i] = inplay
for i in range(6783, 6974):
    data1_S_5[i] = inplay
for i in range(7800, 7948):
    data1_S_5[i] = inplay
for i in range(8180, 8365):
    data1_S_5[i] = inplay
for i in range(8618, 8788):
    data1_S_5[i] = inplay

# data1_S_6の場合
for i in range(59, 115):
    data1_S_6[i] = inplay
for i in range(351, 486):
    data1_S_6[i] = inplay
for i in range(756, 864):
    data1_S_6[i] = inplay
for i in range(1144, 1385):
    data1_S_6[i] = inplay
for i in range(1998, 2061):
    data1_S_6[i] = inplay
for i in range(2272, 2497):
    data1_S_6[i] = inplay
for i in range(2707, 2994):
    data1_S_6[i] = inplay
for i in range(3340, 3424):
    data1_S_6[i] = inplay
for i in range(3650, 3735):
    data1_S_6[i] = inplay
for i in range(4048, 4133):
    data1_S_6[i] = inplay
for i in range(4494, 4587):
    data1_S_6[i] = inplay
for i in range(4798, 5019):
    data1_S_6[i] = inplay
for i in range(5330, 5445):
    data1_S_6[i] = inplay
for i in range(5728, 5785):
    data1_S_6[i] = inplay
for i in range(6024, 6171):
    data1_S_6[i] = inplay
for i in range(6451, 6621):
    data1_S_6[i] = inplay
for i in range(6979, 7152):
    data1_S_6[i] = inplay
for i in range(7497, 7527):
    data1_S_6[i] = inplay
for i in range(7743, 7941):
    data1_S_6[i] = inplay
for i in range(8206, 8386):
    data1_S_6[i] = inplay


print('Saving data in Excel ...')
f = open('True_Label.csv','w')
writer = csv.writer(f, lineterminator='\n')
writer.writerow(data1_S_1)
writer.writerow(data1_S_2)
writer.writerow(data1_S_3)
writer.writerow(data1_S_4)
writer.writerow(data1_S_5)
writer.writerow(data1_S_6)
