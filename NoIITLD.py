#-*- coding:utf-8 -*-
import cv2
import numpy as np
import os
import math
import gc


# 動画ファイル読み込み
vn = 'data1_D_2'    # 動画ファイル名
print('Reading a video file ['+ str(vn) +']...')

frame_list = []

cap = cv2.VideoCapture('capDatas/'+ vn +'.mp4')

# 動画情報の取得
fnum = int(math.floor(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
fps = int(math.ceil(cap.get(cv2.CAP_PROP_FPS)))
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cap.get(cv2.CAP_PROP_FOURCC)
fnum = int(0.999*fnum)

rate = 0.1
print('Reading frames...')
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(math.ceil(rate*100)) +'%')
        rate = rate + 0.1
    ret, frame = cap.read()
    frame_list.append(frame)

# TLDの初期化
print('Making Tracker...')
frame = frame_list[0]

# 1人目の追跡器の追跡器
player1 = cv2.TrackerTLD_create()
b1 = (0, 0, 10, 10)
b1 = cv2.selectROI(frame, False)
ok = player1.init(frame, b1)

# 2人目の追跡器の初期化
player2 = cv2.TrackerTLD_create()
b2 = (0, 0, 10, 10)
b2 = cv2.selectROI(frame, False)
ok = player2.init(frame, b2)
cv2.destroyAllWindows()

# TLDの初期化
rate = 0.1
print('Tracking Learning Detection...')
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(math.ceil(rate*100)) +'%')
        rate = rate + 0.1

    # 1人目の追跡
    track, b1 = player1.update(frame_list[i])
    if track:
        p1 = (int(b1[0]), int(b1[1]))
        p2 = (int(b1[0] + b1[2]), int(b1[1] + b1[3]))
        cv2.rectangle(frame_list[i], p1, p2, (0, 255, 0), 2, 1)
    else:
        cv2.putText(frame_list[i], "Failure", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA);

    # 2人目の追跡
    track, b2 = player2.update(frame_list[i])
    if track:
        p1 = (int(b2[0]), int(b2[1]))
        p2 = (int(b2[0] + b2[2]), int(b2[1] + b2[3]))
        cv2.rectangle(frame_list[i], p1, p2, (255, 0, 0), 2, 1)
    else:
        cv2.putText(frame_list[i], "Failure", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA);

# 結果画像を保存
print('Saving image...')
odn = 'screenCaps/'+ vn +'_Normal' # フレーム保存ディレクトリ
if not os.path.exists(odn):
    os.mkdir(odn)
rate = 0.1
for i in range(0, fnum, 30):
    if((i/fnum) >= rate):
        print(str(math.ceil(rate*100)) +'%')
        rate = rate + 0.1
    cv2.imwrite(odn +'/NoIIframe_'+ str(i) +'.jpg', frame_list[i])

cap.release()
cv2.destroyAllWindows()
