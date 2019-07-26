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
def TrackingLearningAndDetection(player, flist, box, color):
    rate = 0.1
    pos = []
    for i in range(len(flist)):
        if (i/len(flist) >= rate):
            print(str(round(rate*100))+'%')
            rate = rate + 0.1
        track, box = player.update(flist[i])
        center = ((box[0]+box[0]+box[2])/2, (box[1]+box[1]+box[3])/2)
        pos.append(center)
        if track:
            lp1 = (int(box[0]), int(box[1]))
            lp2 = (int(box[0] + box[2]), int(box[1] + box[3]))
            cv2.rectangle(flist[i], lp1, lp2, color, 2, 1)
        else:
            pos[i] = pos[i-1]
            cv2.putText(flist[i], "Failure", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA);
    return pos

# 動画ファイル読み込み
vn = 'data1_S_4'    # 動画ファイル名
print('Reading a video file ['+ str(vn) +']...')
cap = cv2.VideoCapture('capDatas/'+ vn +'.mp4')
odn = 'screenCaps/'+ vn +'_IICP' # フレーム保存ディレクトリ
fnum = int(math.floor(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fnum = int(0.999*fnum)
print('fnum : '+ str(fnum))
if not os.path.exists(odn):
    os.mkdir(odn)


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

print('Masking left image ...')
Lmask_list = []
rate = 0.1
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%  (' +str(i) +'/'+ str(fnum) +')')
        rate = rate + 0.1
    Lmask_list.append(color_detect(left_list[i]))

print('Dilating left mask ...')
rate = 0.1
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%  (' +str(i) +'/'+ str(fnum) +')')
        rate = rate + 0.1
    kernel = np.ones((3,3), np.uint8)
    Lmask_list[i] = cv2.dilate(Lmask_list[i], kernel, iterations=1)
    Lmask_list[i] = cv2.morphologyEx(Lmask_list[i], cv2.MORPH_OPEN, kernel)

print('Left Image Inpainting ...')
rate = 0.1
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%  (' +str(i) +'/'+ str(fnum) +')')
        rate = rate + 0.1
    left_list[i] = cv2.inpaint(left_list[i], Lmask_list[i], 3, cv2.INPAINT_TELEA)
del Lmask_list
gc.collect()

print('Cliping right player ...')
right_list = []
for i in range(fnum):
    img = frame_list[i][int(H*0.4):int(H*(0.6)), int(W*0.45):int(W*0.85)]
    right_list.append(img)

print('Masking right image ...')
Rmask_list = []
rate = 0.1
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%  (' +str(i) +'/'+ str(fnum) +')')
        rate = rate + 0.1
    Rmask_list.append(color_detect(right_list[i]))

print('Dilating right mask ...')
rate = 0.1
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%  (' +str(i) +'/'+ str(fnum) +')')
        rate = rate + 0.1
    kernel = np.ones((3,3), np.uint8)
    Rmask_list[i] = cv2.dilate(Rmask_list[i], kernel, iterations=1)
    Rmask_list[i] = cv2.morphologyEx(Rmask_list[i], cv2.MORPH_OPEN, kernel)

print('Right Image Inpainting ...')
rate = 0.1
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%  (' +str(i) +'/'+ str(fnum) +')')
        rate = rate + 0.1
    right_list[i] = cv2.inpaint(right_list[i], Rmask_list[i], 3, cv2.INPAINT_TELEA)
del Rmask_list
gc.collect()

# TLDの初期化
print('Making Tracker...')
Lplayer1, Lb1 = None, None
Lplayer1, Lb1 = InitializingTLD(Lplayer1, Lb1, left_list[0])
Lplayer2, Lb2 = None, None
Lplayer2, Lb2 = InitializingTLD(Lplayer2, Lb2, left_list[0])
Rplayer1, Rb1 = None, None
Rplayer1, Rb1 = InitializingTLD(Rplayer1, Rb1, right_list[0])
Rplayer2, Rb2 = None, None
Rplayer2, Rb2 = InitializingTLD(Rplayer2, Rb2, right_list[0])

# TLDの初期化
print('Left TLD ...')
Lpos1 = TrackingLearningAndDetection(Lplayer1, left_list, Lb1, (255,0,0))
Lpos2 = TrackingLearningAndDetection(Lplayer2, left_list, Lb2, (0,255,0))
print('Saving image...')
rate = 0.1
for i in range(0, fnum, 30):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%')
        rate = rate + 0.1
    cv2.imwrite(odn +'/CPIIL_'+ str(i) +'.jpg', left_list[i])
del left_list
gc.collect()

print('Right TLD ...')
Rpos1 = TrackingLearningAndDetection(Rplayer1, right_list, Rb1, (0,0,255))
Rpos2 = TrackingLearningAndDetection(Rplayer2, right_list, Rb2, (255,255,255))
print('Saving image...')
rate = 0.1
for i in range(0, fnum, 30):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%  (' +str(i) +'/'+ str(fnum) +')')
        rate = rate + 0.1
    cv2.imwrite(odn +'/CPIIR_'+ str(i) +'.jpg', right_list[i])
del right_list
gc.collect()

cv2.destroyAllWindows()
