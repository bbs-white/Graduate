#-*- coding:utf-8 -*-
import cv2
import numpy as np
import os
import math
import csv

def InitializingTLD(player, box, iniframe):
    player = cv2.TrackerTLD_create()
    box = (0, 0, 10, 10)
    box = cv2.selectROI(iniframe, False)
    ok = player.init(iniframe, box)
    cv2.destroyAllWindows()
    return player, box

# 動画ファイル読み込み
idn = 'capDatas'    # 読み込む動画のディレクトリ
vn = 'data1_S_1'    # 動画ファイル名
fe_video = '.mp4'   # 拡張子
vfn = vn + fe_video
print('Reading a video file ['+ str(vfn) +'] ...')

frame_list = []
left_list = []
right_list = []
PL = [] # 単純な移動量からの判断
PL2 = [] # PLを5フレーム中の多い方で判断

cap = cv2.VideoCapture(idn +'/'+ vfn)

# 動画情報の取得
fnum = int(math.floor(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
fps = int(math.ceil(cap.get(cv2.CAP_PROP_FPS)))
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cap.get(cv2.CAP_PROP_FOURCC)
fnum = int(0.8*fnum)
print('fnum : '+ str(fnum))

print('Reading frames ...')
rate = 0.04
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(math.ceil(rate*100)) +'%')
        rate = rate + 0.08
    ret, frame = cap.read()
    frame_list.append(frame)
cap.release()

print('Clipping Player ...')
print('Left')
for i in range(fnum):
    left_img = frame_list[i][int(H*0.4):H, 0:int(W*(0.7))]
    left_list.append(left_img)
print('Right')
for i in range(fnum):
    right_img = frame_list[i][int(H*0.4):int(H*(0.6)), int(W*0.4):int(W*0.85)]
    right_list.append(right_img)

# TLDの初期化
print('Making Player Tracker ...')
print('Left')
Lplayer, Lbox = None, None
Lplayer, Lbox = InitializingTLD(Lplayer, Lbox, left_list[0])
print('Right')
Rplayer, Rbox = None, None
Rplayer, Rbox = InitializingTLD(Rplayer, Rbox, right_list[0])


print('Tracking Learning and Detection ...')
print('Left')
Lpos = []
for i in range(fnum):
    # 1人目の追跡
    Ltrack, Lbox = Lplayer.update(left_list[i])
    center = ((Lbox[0]+Lbox[0]+Lbox[2])/2, (Lbox[1]+Lbox[1]+Lbox[3])/2)
    Lpos.append(center)
    if Ltrack:
        lp1 = (int(Lbox[0]), int(Lbox[1]))
        lp2 = (int(Lbox[0] + Lbox[2]), int(Lbox[1] + Lbox[3]))
        cv2.rectangle(left_list[i], lp1, lp2, (0, 255, 0), 2, 1)
    else:
        cv2.putText(left_list[i], "Failure", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA);

print('Right')
Rpos = []
for i in range(fnum):
    Rtrack, Rbox = Rplayer.update(right_list[i])
    center = ((Rbox[0]+Rbox[0]+Rbox[2])/2, (Rbox[1]+Rbox[1]+Rbox[3])/2)
    Rpos.append(center)
    if Rtrack:
        rp1 = (int(Rbox[0]), int(Rbox[1]))
        rp2 = (int(Rbox[0] + Rbox[2]), int(Rbox[1] + Rbox[3]))
        cv2.rectangle(right_list[i], rp1, rp2, (255, 0, 0), 2, 1)
    else:
        cv2.putText(right_list[i], "Failure", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA);

# 左側サーブ位置
lcx = 530
lcy = 90
# 右側サーブ位置
rcx = 363
rcy = 70

# 移動量を計算
print('Calculating migration distance ...')
print('Left')
Ldis = []
Ldis.append(0)
for i in range(1,fnum):
    _xu = Lpos[i][0] - Lpos[i-1][0]
    _xd = Lpos[i][1] - Lpos[i-1][1]
    x = math.sqrt(math.pow(_xd,2) + math.pow(_xu,2))
    Ldis.append(x)
print('Right')
Rdis = []
Rdis.append(0)
for i in range(1,fnum):
    _xu = Rpos[i][0] - Rpos[i-1][0]
    _xd = Rpos[i][1] - Rpos[i-1][1]
    x = math.sqrt(math.pow(_xd,2) + math.pow(_xu,2))
    Rdis.append(x)


print('Calculating diff from service position ...')
print('Left')
Lc_diff = []
Lc_diff.append(0)
for i in range(1,fnum):
    _lcx = lcx - Lpos[i][0]
    _lcy = lcy - Lpos[i][1]
    x = math.sqrt(math.pow(_lcx,2) + math.pow(_lcy,2))
    Lc_diff.append(x)
print('Right')
Rc_diff = []
Rc_diff.append(0)
for i in range(1,fnum):
    _rcx = rcx - Rpos[i][0]
    _rcy = rcy - Rpos[i][1]
    x = math.sqrt(math.pow(_rcx,2) + math.pow(_rcy,2))
    Rc_diff.append(x)


print('Normalizing migration distance ...')
print('Left')
lmax =  max(Ldis)
for i in range(fnum):
    Ldis[i] = Ldis[i]/lmax
    if (Ldis[i] >= 0.8):
        Ldis[i] = Ldis[i-1]
lmax = max(Ldis)
for i in range(fnum):
    Ldis[i] = Ldis[i]/lmax
print('Right')
rmax = max(Rdis)
for i in range(fnum):
    Rdis[i] = Rdis[i]/rmax
    if (Rdis[i] >= 0.8):
        Rdis[i] = Rdis[i-1]
rmax = max(Rdis)
for i in range(fnum):
    Rdis[i] = Rdis[i]/rmax

print('Calculating average migration distance ...')
print('Left')
Ldis_sum = sum(Ldis)
Ldis_ave = Ldis_sum/fnum
print('Right')
Rdis_sum = sum(Rdis)
Rdis_ave = Rdis_sum/fnum

print('Normalizing diff from service position ...')
print('Left')
lmax = max(Lc_diff)
for i in range(fnum):
    Lc_diff[i] = Lc_diff[i]/lmax
    if (Lc_diff[i] >= 0.8):
        Lc_diff[i] = Lc_diff[i-1]
lmax = max(Lc_diff)
for i in range(fnum):
    Lc_diff[i] = Lc_diff[i]/lmax
print('Right')
rmax = max(Rc_diff)
for i in range(fnum):
    Rc_diff[i] = Rc_diff[i]/rmax
    if (Rc_diff[i] >= 0.8):
        Rc_diff[i] = Rc_diff[i-1]
rmax = max(Rc_diff)
for i in range(fnum):
    Rc_diff[i] = Rc_diff[i]/rmax


print('5 frames distance average ...')
r_5_dis = []
l_5_dis = []
for i in range(4):
    _Ldis = 0
    _Rdis = 0
    for j in range(i+1):
        _Ldis = _Ldis + Ldis[j]
        _Rdis = _Rdis + Rdis[j]
    _Ldis/(i+1)
    _Rdis/(i+1)
    l_5_dis.append(_Ldis)
    r_5_dis.append(_Rdis)
for i in range(5, fnum):
    _Ldis = 0
    _Rdis = 0
    for j in range(i-5,i):
        _Ldis = _Ldis + Ldis[j]
        _Rdis = _Rdis + Rdis[j]
    _Ldis = _Ldis/5
    _Rdis = _Rdis/5
    l_5_dis.append(_Ldis)
    r_5_dis.append(_Rdis)

out = -2.0
inplay = -0.4


for i in range(fnum):
    if (Ldis[i] <= Ldis_ave/10 and Rdis[i] <= Rdis_ave/10):
        PL.append(out) # Out of Play
    else:
        PL.append(inplay) # In Play

# 5フレーム毎に移動量から判断
index_out2 = 5
for i in range(math.floor(index_out2/2)):
    PL2.append(out)
for i in range(math.floor(index_out2/2), fnum-math.floor(index_out2/2)):
    k = 0
    for j in range(i-math.floor(index_out2/2), i+math.floor(index_out2/2)):
        k = k + PL[j]
    if (k <= (out/2 + inplay/2)*math.ceil(index_out2/2)):
        PL2.append(out) # Out of Play
    else:
        PL2.append(inplay) # In Play
for i in range(math.floor(index_out2/2)):
    PL2.append(inplay)

# さらに多くのフレーム毎に移動量から判断
index_out3 = 9
PL3 = [] # PL2から多くのフレーム中から判断
for i in range(math.floor(index_out3/2)):
    PL3.append(out)
for i in range(math.floor(index_out3/2), fnum-math.floor(index_out3/2)):
    k = 0
    for j in range(i-math.floor(index_out3/2), i+math.floor(index_out3/2)):
        k = k+PL2[j]
    if (k <= (out/2 + inplay/2)*math.ceil(index_out3/2)):
        PL3.append(out)
    else:
        PL3.append(inplay)
for i in range(math.floor(index_out3/2)):
    PL3.append(inplay)

# インターバルの時間を考慮
print('Detecting interval ...')
PL4 = []
space = 100
for i in range(fnum):
    PL4.append(PL3[i])
for i in range(math.ceil(index_out3), fnum-space):
    if (PL3[i] == inplay):
        count_in = 0
        count_out = 0
        for j in range(i, i+space):
            if (PL3[j] >= -1):
                count_in = count_in+1
            else:
                count_out = count_out+1
        if (count_in >= space*0.6):
            for j in range(i, i+space):
                PL4[j] = inplay
            i = i+int(space*0.9)
        elif (count_in <= space*0.3):
            for j in range(i, i+space):
                PL4[j] = out
            i = i+space
        else:
            i = i+int(space*0.3)

space = 20
for i in range(fnum-space):
    if (PL4[i] == inplay):
        err = 0
        for j in range(i, i+space):
            if (PL4[j] == out):
                err = err+1
        if (err > space*0.4):
            for j in range(i, i+space):
                PL4[j] = out
        i = i+space
true_label = []
for i in range(fnum):
    true_label.append(out)


print('Saving data in Excel ...')
f = open(vn+'_serve_pre.csv','w')
writer = csv.writer(f, lineterminator='\n')

writer.writerow(Ldis)
writer.writerow(Rdis)
writer.writerow(l_5_dis)
writer.writerow(r_5_dis)
writer.writerow(Lc_diff)
writer.writerow(Rc_diff)
writer.writerow(PL)
writer.writerow(PL2)
writer.writerow(PL3)
writer.writerow(PL4)
