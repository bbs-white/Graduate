#-*- coding:utf-8 -*-
import cv2
import numpy as np
import os
import math
import gc

def InitializingTLD(player, box, iniframe):
    player = cv2.TrackerTLD_create()
    box = (0, 0, 10, 10)
    box = cv2.selectROI(iniframe, False)
    ok = player.init(iniframe, box)
    cv2.destroyAllWindows()
    return player, box

# 動画ファイル読み込み
idn = 'capDatas'    # 読み込む動画のディレクトリ
vn = 'data1_S_6'    # 動画ファイル名
odn = 'screenCaps/'+ vn +'_CP' # フレーム保存ディレクトリ
if not os.path.exists(odn):
    os.mkdir(odn)
print('Reading a video file ['+ str(vn) +']...')

cap = cv2.VideoCapture(idn +'capDatas/'+ vn +'.mp4')

# 動画情報の取得
fnum = int(math.floor(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fnum = int(0.999*fnum)

print('Reading frames...')
frame_list = []
rate = 0.1
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%')
        rate = rate + 0.1
    ret, frame = cap.read()
    frame_list.append(frame)
cap.release()

print('Cliping Left player ...')
left_list = []
for i in range(fnum):
    img = frame_list[i][int(H*0.4):H, 0:int(W*(0.7))]
    left_list.append(img)
del img
gc.collect()

print('Cliping Right player ...')
right_list = []
for i in range(fnum):
    img = frame_list[i][int(H*0.4):int(H*(0.6)), int(W*0.4):int(W*0.85)]
    right_list.append(img)
del img
gc.collect()

# TLDの初期化
# 1人目の追跡器の追跡器
print('Making left player Tracker...')
player1, b1 = None, None
player1, b1 = InitializingTLD(player1, b1, left_list[0])

print('Making right player Tracker...')
player2, b2 = None, None
player2, b2 = InitializingTLD(player2, b2, right_list[0])

print('Left player TLD...')
rate = 0.1
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%')
        rate = rate + 0.1
    # 1人目の追跡
    track1, b1 = player1.update(left_list[i])
    if track1:
        lp1 = (int(b1[0]), int(b1[1]))
        lp2 = (int(b1[0] + b1[2]), int(b1[1] + b1[3]))
        cv2.rectangle(left_list[i], lp1, lp2, (0, 255, 0), 2, 1)
    else:
        cv2.putText(left_list[i], "Failure", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA);

print('Saving image...')
rate = 0.1
for i in range(0, fnum, 30):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%')
        rate = rate + 0.1
    cv2.imwrite(odn +'/CPframe_'+ str(i) +'.jpg', left_list[i])
del left_list
gc.collect()

print('Right player TLD...')
rate = 0.1
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%')
        rate = rate + 0.1
    track2, b2 = player2.update(right_list[i])
    if track2:
        rp1 = (int(b2[0]), int(b2[1]))
        rp2 = (int(b2[0] + b2[2]), int(b2[1] + b2[3]))
        cv2.rectangle(right_list[i], rp1, rp2, (255, 0, 0), 2, 1)
    else:
        cv2.putText(right_list[i], "Failure", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA);

print('Saving image...')
rate = 0.1
for i in range(0, fnum, 30):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%')
        rate = rate + 0.1
    cv2.imwrite(odn +'/CPframe_'+ str(i) +'.jpg', right_list[i])
del right_list
gc.collect()

cv2.destroyAllWindows()
