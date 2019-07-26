#-*- coding:utf-8 -*-
import cv2
import numpy as np
import os
import math
import csv

# 動画ファイル読み込み
idn = 'capDatas'    # 読み込む動画のディレクトリ
vn = 'data1_D_1'    # 動画ファイル名
fe_video = '.mp4'   # 拡張子
vfn = vn + fe_video
print('Reading a video file ['+ str(vfn) +'] ...')

frame_list = []
left_list = []
right_list = []
OutOfPlay = [] # 単純な移動量からの判断
OutOfPlay2 = [] # OutOfPlayを5フレーム中の多い方で判断

cap = cv2.VideoCapture(idn +'/'+ vfn)

# 動画情報の取得
fnum = int(math.floor(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
fps = int(math.ceil(cap.get(cv2.CAP_PROP_FPS)))
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cap.get(cv2.CAP_PROP_FOURCC)
fnum = int(0.7*fnum)
print('fnum : '+ str(fnum))

print('Reading frames ...')
for i in range(fnum):
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
print('Left 1st')
left_frame1 = left_list[0]
Lplayer1 = cv2.TrackerTLD_create()
Lb1 = (0, 0, 10, 10)
Lb1 = cv2.selectROI(left_frame1, False)
Lok1 = Lplayer1.init(left_frame1, Lb1)
cv2.destroyAllWindows()
print('Left 2nd')
left_frame2 = left_list[0]
Lplayer2 = cv2.TrackerTLD_create()
Lb2 = (0, 0, 10, 10)
Lb2 = cv2.selectROI(left_frame2, False)
Lok2 = Lplayer2.init(left_frame2, Lb2)
cv2.destroyAllWindows()

print('Right 1st')
right_frame1 = right_list[0]
Rplayer1 = cv2.TrackerTLD_create()
Rb1 = (0, 0, 10, 10)
Rb1 = cv2.selectROI(right_frame1, False)
Rok1 = Rplayer1.init(right_frame1, Rb1)
cv2.destroyAllWindows()
print('Right 2nd')
right_frame2 = right_list[0]
Rplayer2 = cv2.TrackerTLD_create()
Rb2 = (0, 0, 10, 10)
Rb2 = cv2.selectROI(right_frame2, False)
Rok2 = Rplayer2.init(right_frame2, Rb2)
cv2.destroyAllWindows()

print('Tracking Learning and Detection ...')
print('Left 1st')
Lpos1 = []
for i in range(fnum):
    Ltrack1, Lb1 = Lplayer1.update(left_list[i])
    center = ((Lb1[0]+Lb1[0]+Lb1[2])/2, (Lb1[1]+Lb1[1]+Lb1[3])/2)
    Lpos1.append(center)
    if Ltrack1:
        lp1 = (int(Lb1[0]), int(Lb1[1]))
        lp2 = (int(Lb1[0] + Lb1[2]), int(Lb1[1] + Lb1[3]))
        cv2.rectangle(left_list[i], lp1, lp2, (0, 255, 0), 2, 1)
    else:
        cv2.putText(left_list[i], "Failure", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA);
print('Left 2nd')
Lpos2 = []
for i in range(fnum):
    Ltrack2, Lb2 = Lplayer2.update(left_list[i])
    center = ((Lb2[0]+Lb2[0]+Lb2[2])/2, (Lb2[1]+Lb2[1]+Lb2[3])/2)
    Lpos2.append(center)
    if Ltrack2:
        lp1 = (int(Lb2[0]), int(Lb2[1]))
        lp2 = (int(Lb2[0] + Lb2[2]), int(Lb2[1] + Lb2[3]))
        cv2.rectangle(left_list[i], lp1, lp2, (0, 255, 100), 2, 1)
    else:
        cv2.putText(left_list[i], "Failure", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,100), 1, cv2.LINE_AA);

print('Right 1st')
Rpos1 = []
for i in range(fnum):
    Rtrack1, Rb1 = Rplayer1.update(right_list[i])
    center = ((Rb1[0]+Rb1[0]+Rb1[2])/2, (Rb1[1]+Rb1[1]+Rb1[3])/2)
    Rpos1.append(center)
    if Rtrack1:
        rp1 = (int(Rb1[0]), int(Rb1[1]))
        rp2 = (int(Rb1[0] + Rb1[2]), int(Rb1[1] + Rb1[3]))
        cv2.rectangle(right_list[i], rp1, rp2, (255, 0, 0), 2, 1)
    else:
        cv2.putText(right_list[i], "Failure", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA);
print('Right 2nd')
Rpos2 = []
for i in range(fnum):
    Rtrack2, Rb2 = Rplayer2.update(right_list[i])
    center = ((Rb2[0]+Rb2[0]+Rb2[2])/2, (Rb2[1]+Rb2[1]+Rb2[3])/2)
    Rpos2.append(center)
    if Rtrack2:
        rp1 = (int(Rb2[0]), int(Rb2[1]))
        rp2 = (int(Rb2[0] + Rb2[2]), int(Rb2[1] + Rb2[3]))
        cv2.rectangle(right_list[i], rp1, rp2, (255, 0, 100), 2, 1)
    else:
        cv2.putText(right_list[i], "Failure", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,100), 1, cv2.LINE_AA);

# 左側サーブ位置
lcx = 530
lcy = 90
# 右側サーブ位置
rcx = 363
rcy = 70

# 移動量を計算
print('Calculating migration distance ...')
print('Left 1st')
Ldis1 = []
Ldis1.append(0)
for i in range(1,fnum):
    _xu = Lpos1[i][0] - Lpos1[i-1][0]
    _xd = Lpos1[i][1] - Lpos1[i-1][1]
    x = math.sqrt(math.pow(_xd,2) + math.pow(_xu,2))
    Ldis1.append(x)
print('Left 2nd')
Ldis2 = []
Ldis2.append(0)
for i in range(1,fnum):
    _xu = Lpos2[i][0] - Lpos2[i-1][0]
    _xd = Lpos2[i][1] - Lpos2[i-1][1]
    x = math.sqrt(math.pow(_xd,2) + math.pow(_xu,2))
    Ldis2.append(x)

print('Right 1st')
Rdis1 = []
Rdis1.append(0)
for i in range(1,fnum):
    _xu = Rpos1[i][0] - Rpos1[i-1][0]
    _xd = Rpos1[i][1] - Rpos1[i-1][1]
    x = math.sqrt(math.pow(_xd,2) + math.pow(_xu,2))
    Rdis1.append(x)
print('Right 2nd')
Rdis2 = []
Rdis2.append(0)
for i in range(1,fnum):
    _xu = Rpos2[i][0] - Rpos2[i-1][0]
    _xd = Rpos2[i][1] - Rpos2[i-1][1]
    x = math.sqrt(math.pow(_xd,2) + math.pow(_xu,2))
    Rdis2.append(x)


print('Normalizing migration distance ...')
print('Left 1st')
lmax =  max(Ldis1)
for i in range(fnum):
    Ldis1[i] = Ldis1[i]/lmax
    if (Ldis1[i] >= 0.8):
        Ldis1[i] = Ldis1[i-1]
lmax = max(Ldis1)
for i in range(fnum):
    Ldis1[i] = Ldis1[i]/lmax
print('Left 2nd')
lmax =  max(Ldis2)
for i in range(fnum):
    Ldis2[i] = Ldis2[i]/lmax
    if (Ldis2[i] >= 0.8):
        Ldis2[i] = Ldis2[i-1]
lmax = max(Ldis2)
for i in range(fnum):
    Ldis2[i] = Ldis2[i]/lmax
print('Right 1st')
rmax = max(Rdis1)
for i in range(fnum):
    Rdis1[i] = Rdis1[i]/rmax
    if (Rdis1[i] >= 0.8):
        Rdis1[i] = Rdis1[i-1]
rmax = max(Rdis1)
for i in range(fnum):
    Rdis1[i] = Rdis1[i]/rmax
print('Right 2nd')
rmax = max(Rdis2)
for i in range(fnum):
    Rdis2[i] = Rdis2[i]/rmax
    if (Rdis2[i] >= 0.8):
        Rdis2[i] = Rdis1[i-1]
rmax = max(Rdis2)
for i in range(fnum):
    Rdis2[i] = Rdis2[i]/rmax


print('Calculation average migration distance ...')
print('Left 1st')
Ldis1_sum = sum(Ldis1)
Ldis1_ave = Ldis1_sum/fnum
print('Left 2nd')
Ldis2_sum = sum(Ldis2)
Ldis2_ave = Ldis2_sum/fnum

print('Right 1st')
Rdis1_sum = sum(Rdis1)
Rdis1_ave = Rdis1_sum/fnum
print('Right 2nd')
Rdis2_sum = sum(Rdis2)
Rdis2_ave = Rdis2_sum/fnum


print('Calculating diff from service position ...')
print('Left 1st')
Lc_diff1 = []
Lc_diff1.append(0)
for i in range(1, fnum):
    _lcx = lcx - Lpos1[i][0]
    _lcy = lcy - Lpos1[i][1]
    x = math.sqrt(math.pow(_lcx,2) + math.pow(_lcy,2))
    Lc_diff1.append(x)
print('Left 2nd')
Lc_diff2 = []
Lc_diff2.append(0)
for i in range(1, fnum):
    _lcx = lcx - Lpos2[i][0]
    _lcy = lcy - Lpos2[i][1]
    x = math.sqrt(math.pow(_lcx,2) + math.pow(_lcy,2))
    Lc_diff2.append(x)

print('Right 1st')
Rc_diff1 = []
Rc_diff1.append(0)
for i in range(1, fnum):
    _rcx = rcx - Rpos1[i][0]
    _rcy = rcy - Rpos1[i][1]
    x = math.sqrt(math.pow(_rcx,2) + math.pow(_rcy,2))
    Rc_diff1.append(x)
print('Right 2nd')
Rc_diff2 = []
Rc_diff2.append(0)
for i in range(1, fnum):
    _rcx = rcx - Rpos2[i][0]
    _rcy = rcy - Rpos2[i][1]
    x = math.sqrt(math.pow(_rcx,2) + math.pow(_rcy,2))
    Rc_diff2.append(x)


print('Normalizing diff from service position ...')
print('Left 1st')
lmax = max(Lc_diff1)
for i in range(fnum):
    Lc_diff1[i] = Lc_diff1[i]/lmax
    if (Lc_diff1[i] >= 0.8):
        Lc_diff1[i] = Lc_diff1[i-1]
lmax = max(Lc_diff1)
for i in range(fnum):
    Lc_diff1[i] = Lc_diff1[i]/lmax
print('Left 2nd')
lmax = max(Lc_diff2)
for i in range(fnum):
    Lc_diff2[i] = Lc_diff2[i]/lmax
    if (Lc_diff2[i] >= 0.8):
        Lc_diff2[i] = Lc_diff2[i-1]
lmax = max(Lc_diff2)
for i in range(fnum):
    Lc_diff2[i] = Lc_diff2[i]/lmax

print('Right 1st')
rmax = max(Rc_diff1)
for i in range(fnum):
    Rc_diff1[i] = Rc_diff1[i]/rmax
    if (Rc_diff1[i] >= 0.8):
        Rc_diff1[i] = Rc_diff1[i-1]
rmax = max(Rc_diff1)
for i in range(fnum):
    Rc_diff1[i] = Rc_diff1[i]/rmax
print('Right 2nd')
rmax = max(Rc_diff2)
for i in range(fnum):
    Rc_diff2[i] = Rc_diff2[i]/rmax
    if (Rc_diff2[i] >= 0.8):
        Rc_diff2[i] = Rc_diff2[i-1]
rmax = max(Rc_diff1)
for i in range(fnum):
    Rc_diff2[i] = Rc_diff2[i]/rmax

'''
print('5 frames distance average ...')
r_5_dis = []
l_5_dis = []
for i in range(4):
    _Ldis1 = 0
    _Rdis1 = 0
    for j in range(i+1):
        _Ldis1 = _Ldis1 + Ldis1[j]
        _Rdis1 = _Rdis1 + Rdis1[j]
    _Ldis1/(i+1)
    _Rdis1/(i+1)
    l_5_dis.append(_Ldis1)
    r_5_dis.append(_Rdis1)

for i in range(5, fnum):
    _Ldis1 = 0
    _Rdis1 = 0
    for j in range(i-5,i):
        _Ldis1 = _Ldis1 + Ldis1[j]
        _Rdis1 = _Rdis1 + Rdis1[j]
    _Ldis1 = _Ldis1/5
    _Rdis1 = _Rdis1/5
    l_5_dis.append(_Ldis1)
    r_5_dis.append(_Rdis1)

out = -2.0
inplay = -0.4


for i in range(fnum):
    if (Ldis1[i] <= Ldis1_ave/10 and Rdis1[i] <= Rdis1_ave/10):
        OutOfPlay.append(out) # Out of Play
    else:
        OutOfPlay.append(inplay) # In Play

# 5フレーム毎に移動量から判断
index_out2 = 5
for i in range(math.floor(index_out2/2)):
    OutOfPlay2.append(out)
for i in range(math.floor(index_out2/2), fnum-math.floor(index_out2/2)):
    k = 0
    for j in range(i-math.floor(index_out2/2), i+math.floor(index_out2/2)):
        k = k + OutOfPlay[j]
    if (k <= (out/2 + inplay/2)*math.ceil(index_out2/2)):
        OutOfPlay2.append(out) # Out of Play
    else:
        OutOfPlay2.append(inplay) # In Play
for i in range(math.floor(index_out2/2)):
    OutOfPlay2.append(inplay)

# さらに多くのフレーム毎に移動量から判断
index_out3 = 9
OutOfPlay3 = [] # OutOfPlay2から多くのフレーム中から判断
for i in range(math.floor(index_out3/2)):
    OutOfPlay3.append(out)
for i in range(math.floor(index_out3/2), fnum-math.floor(index_out3/2)):
    k = 0
    for j in range(i-math.floor(index_out3/2), i+math.floor(index_out3/2)):
        k = k+OutOfPlay2[j]
    if (k <= (out/2 + inplay/2)*math.ceil(index_out3/2)):
        OutOfPlay3.append(out)
    else:
        OutOfPlay3.append(inplay)
for i in range(math.floor(index_out3/2)):
    OutOfPlay3.append(inplay)

# インターバルの時間を考慮
print('Detecting interval ...')
OutOfPlay4 = []
space = 100
for i in range(fnum):
    OutOfPlay4.append(OutOfPlay3[i])
for i in range(math.ceil(index_out3), fnum-space):
    if (OutOfPlay3[i] == inplay):
        count_in = 0
        count_out = 0
        for j in range(i, i+space):
            if (OutOfPlay3[j] >= -1):
                count_in = count_in+1
            else:
                count_out = count_out+1
        if (count_in >= space*0.6):
            for j in range(i, i+space):
                OutOfPlay4[j] = inplay
            i = i+int(space*0.9)
        elif (count_in <= space*0.3):
            for j in range(i, i+space):
                OutOfPlay4[j] = out
            i = i+space
        else:
            i = i+int(space*0.3)

space = 20
for i in range(fnum-space):
    if (OutOfPlay4[i] == inplay):
        err = 0
        for j in range(i, i+space):
            if (OutOfPlay4[j] == out):
                err = err+1
        if (err > space*0.4):
            for j in range(i, i+space):
                OutOfPlay4[j] = out
        i = i+space
true_label = []
for i in range(fnum):
    true_label.append(out)


print('Saving data in Excel ...')
f = open(vn+'_serve.csv','w')
writer = csv.writer(f, lineterminator='\n')

writer.writerow(Ldis1)
writer.writerow(Ldis2)
writer.writerow(Rdis1)
writer.writerow(Rdis2)
#writer.writerow(OutOfPlay)
#writer.writerow(OutOfPlay2)
#writer.writerow(OutOfPlay3)
#writer.writerow(OutOfPlay4)
writer.writerow(true_label)
writer.writerow(Lc_diff1)
writer.writerow(Lc_diff2)
writer.writerow(Rc_diff1)
writer.writerow(Rc_diff2)
'''


# 結果画像を保存
print('Saving image ...')
odn = 'screenCaps/'+ vn +'_NoII' # フレーム保存ディレクトリ
if not os.path.exists(odn):
    os.mkdir(odn)
'''
for i in range(fnum):
    if (OutOfPlay3[i] == -1):
        cv2.imwrite(odn +'/playing_'+ str(i) +'.jpg', frame_list[i])
'''
for i in range(0,fnum,20):
    cv2.imwrite(odn +'/playing_'+ str(i) +'.jpg', frame_list[i])
