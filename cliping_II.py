#-*- coding:utf-8 -*-
import cv2
import numpy as np
import os
import math
import gc

def color_detect(bgr_img):
    hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
    hsv_min = np.array([0, 0, 200])
    hsv_max = np.array([179, 120, 255])
    white = cv2.inRange(hsv_img, hsv_min, hsv_max)
    return white
def InitializingTLD(player, box, iniframe):
    player = cv2.TrackerTLD_create()
    box = (0, 0, 10, 10)
    box = cv2.selectROI(iniframe, False)
    ok = player.init(iniframe, box)
    cv2.destroyAllWindows()
    return player, box

# 動画ファイル読み込み
vn = 'data1_S_4'    # 動画ファイル名
print('Reading a video file ['+ str(vn) +']...')
cap = cv2.VideoCapture('capDatas/'+ vn +'.mp4')
odn = 'screenCaps/'+ vn +'_IICP' # フレーム保存ディレクトリ
if not os.path.exists(odn):
    os.mkdir(odn)

# 動画情報の取得
fnum = int(math.floor(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fnum = int(0.999*fnum)
print('fnum : '+ str(fnum))

print('Reading frames...')
frame_list = []
rate = 0.1
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%  (' +str(i) +'/'+ str(fnum) +')')
        rate = rate + 0.1
    ret, frame = cap.read()
    frame_list.append(frame)
cap.release()
del frame
gc.collect()

print('Cliping left player ...')
left_list = []
for i in range(fnum):
    img = frame_list[i][int(H*0.4):H, 0:int(W*(0.7))]
    left_list.append(img)
del frame_list
gc.collect()

print('Left Image Inpainting ... ')
rate = 0.05
kernel = np.ones((3,3), np.uint8)
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%  (' +str(i) +'/'+ str(fnum) +')')
        rate = rate + 0.05
    mask = color_detect(left_list[i])
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    left_list[i] = cv2.inpaint(left_list[i], mask, 3, cv2.INPAINT_TELEA)
del mask
del kernel
gc.collect()


'''
print('Cliping right player ...')
right_list = []
for i in range(fnum):
    img = frame_list[i][int(H*0.4):int(H*(0.6)), int(W*0.4):int(W*0.85)]
    right_list.append(img)

print('Right Image Inpainting ... ')
rate = 0.05
kernel = np.ones((3,3), np.uint8)
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%  (' +str(i) +'/'+ str(fnum) +')')
        rate = rate + 0.05
    mask = color_detect(right_list[i])
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    right_list[i] = cv2.inpaint(right_list[i], mask, 3, cv2.INPAINT_TELEA)
del mask
del kernel
gc.collect()

'''

# TLDの初期化
# 1人目の追跡器の追跡器
print('Making left player Tracker...')
player1, b1 = None, None
player1, b1 = InitializingTLD(player1, b1, left_list[0])

'''
# 2人目の追跡器の初期化
print('Making right player Tracker...')
player2, b2 = None, None
player2, b2 = InitializingTLD(player2, b2, right_list[0])
'''

print('Left player TLD...')
rate = 0.1
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%  (' +str(i) +'/'+ str(fnum) +')')
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
        print(str(round(rate*100)) +'%  (' +str(i) +'/'+ str(fnum) +')')
        rate = rate + 0.1
    cv2.imwrite(odn +'/CPIIL_'+ str(i) +'.jpg', left_list[i])
del left_list
gc.collect()


'''
print('Right player TLD...')
rate = 0.1
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%  (' +str(i) +'/'+ str(fnum) +')')
        rate = rate + 0.1
    track2, b2 = player2.update(right_list[i])
    if track2:
        rp1 = (int(b2[0]), int(b2[1]))
        rp2 = (int(b2[0] + b2[2]), int(b2[1] + b2[3]))
        cv2.rectangle(right_list[i], rp1, rp2, (255, 0, 0), 2, 1)
    else:
        cv2.putText(right_list[i], "Failure", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA);

print('Saving image...')
rate = 0.1
for i in range(0, fnum, 30):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%  (' +str(i) +'/'+ str(fnum) +')')
        rate = rate + 0.1
    cv2.imwrite(odn +'/CPIIR_'+ str(i) +'.jpg', right_list[i])
del right_list
gc.collect()
'''

cv2.destroyAllWindows()
