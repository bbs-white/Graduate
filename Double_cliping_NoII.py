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
vn = 'data1_D_1'    # 動画ファイル名
odn = 'screenCaps/'+ vn +'_CP' # フレーム保存ディレクトリ
if not os.path.exists(odn):
    os.mkdir(odn)

print('Reading a video file ['+ str(vn) +']...')
cap = cv2.VideoCapture('capDatas/'+ vn +'.mp4')
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
    img = frame_list[i][int(H*0.4):int(H*(0.6)), int(W*0.45):int(W*0.85)]
    right_list.append(img)
del img
gc.collect()



print('Making Left Tracker ...')
Lplayer1, Lb1 = None, None
Lplayer1, Lb1 = InitializingTLD(Lplayer1, Lb1, left_list[0])
Lplayer2, Lb2 = None, None
Lplayer2, Lb2 = InitializingTLD(Lplayer2, Lb2, left_list[0])

print('Making Right Tracker ...')
Rplayer1, Rb1 = None, None
Rplayer1, Rb1 = InitializingTLD(Rplayer1, Rb1, right_list[0])
Rplayer2, Rb2 = None, None
Rplayer2, Rb2 = InitializingTLD(Rplayer2, Rb2, right_list[0])



print('Left 1st TLD ...')
Lpos1 = TrackingLearningAndDetection(Lplayer1, left_list, Lb1, (255,0,0))
print('Left 2nd TLD ...')
Lpos2 = TrackingLearningAndDetection(Lplayer2, left_list, Lb2, (0,255,0))
print('Saving image...')
rate = 0.1
for i in range(0, fnum, 30):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%')
        rate = rate + 0.1
    cv2.imwrite(odn +'/CPL_'+ str(i) +'.jpg', left_list[i])
del left_list
gc.collect()


print('Right 1st TLD ...')
Rpos1 = TrackingLearningAndDetection(Rplayer1, right_list, Rb1, (0,0,255))
print('Right 2nd TLD ...')
Rpos2 = TrackingLearningAndDetection(Rplayer2, right_list, Rb2, (255,255,255))
print('Saving image...')
rate = 0.1
for i in range(0, fnum, 30):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%')
        rate = rate + 0.1
    cv2.imwrite(odn +'/CPR_'+ str(i) +'.jpg', right_list[i])
del right_list
gc.collect()


cv2.destroyAllWindows()
