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
    rate = 0.18
    pos = []
    for i in range(len(flist)):
        if (i/len(flist) >= rate):
            print(str(round(rate*100))+'%')
            rate = rate + 0.18
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
vn = 'data1_D_2'    # 動画ファイル名
print('Reading a video file ['+ str(vn) +']...')

cap = cv2.VideoCapture('capDatas/'+ vn +'.mp4')
fnum = int(math.floor(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
fnum = int(0.999*fnum)

rate = 0.18
print('Reading frames...')
frame_list = []
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(math.ceil(rate*100)) +'%')
        rate = rate + 0.18
    ret, frame = cap.read()
    frame_list.append(frame)
cap.release()

# TLDの初期化
print('Making Tracker...')
Lplayer1, Lb1 = None, None
Lplayer1, Lb1 = InitializingTLD(Lplayer1, Lb1, frame_list[0])
Lplayer2, Lb2 = None, None
Lplayer2, Lb2 = InitializingTLD(Lplayer2, Lb2, frame_list[0])
'''
Rplayer1, Rb1 = None, None
Rplayer1, Rb1 = InitializingTLD(Rplayer1, Rb1, frame_list[0])
Rplayer2, Rb2 = None, None
Rplayer2, Rb2 = InitializingTLD(Rplayer2, Rb2, frame_list[0])
'''

# TLDの初期化
print('Tracking Learning Detection...')
Lpos1 = TrackingLearningAndDetection(Lplayer1, frame_list, Lb1, (255,0,0))
Lpos2 = TrackingLearningAndDetection(Lplayer2, frame_list, Lb2, (0,255,0))
'''
Rpos1 = TrackingLearningAndDetection(Rplayer1, frame_list, Rb1, (0,0,255))
Rpos2 = TrackingLearningAndDetection(Rplayer2, frame_list, Rb2, (255,255,255))
'''

# 結果画像を保存
print('Saving image...')
odn = 'screenCaps/'+ vn +'_Normal' # フレーム保存ディレクトリ
if not os.path.exists(odn):
    os.mkdir(odn)
rate = 0.18
for i in range(0, fnum, 30):
    if((i/fnum) >= rate):
        print(str(math.ceil(rate*100)) +'%')
        rate = rate + 0.18
    cv2.imwrite(odn +'/NoIIframe_'+ str(i) +'.jpg', frame_list[i])

cap.release()
cv2.destroyAllWindows()
