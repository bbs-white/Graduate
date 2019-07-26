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
def TrackingLearningAndDetection(player, flist, pos, box, fnum, color):
    for i in range(fnum):
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
    return flist, pos
def CalculatingMigrationDistance(MigDis, pos, fnum):
    MigDis.append(0)
    for i in range(fnum):
        _xu = pos[i][0] - pos[i-1][0]
        _xd = pos[i][1] - pos[i-1][1]
        x = math.sqrt(math.pow(_xd,2) + math.pow(_xu,2))
        MigDis.append(x)
def CalculatingDiffFromServicePosition(cx, cy, c_diff, pos, fnum):
    c_diff.append(0)
    for i in range(1, fnum):
        _cx = cx - pos[i][0]
        _cy = cy - pos[i][1]
        x = math.sqrt(math.pow(_cx,2) + math.pow(_cy,2))
        c_diff.append(x)
def Normalizing(list):
    list_max = max(list)
    for i in range(len(list)):
        list[i] = list[i]/list_max
        if (list[i] >= 0.8):
            list[i] = list[i-1]
    list_max = max(list)
    for i in range(len(list)):
        list[i] = list[i]/list_max
def Listing_Windows(list, five_list, window):
    for i in range(window):
        x = 0
        for j in range(i+1):
            x = x + list[j]
        x = x/(i+1)
        five_list.append(x)
    for i in range(window, len(list)):
        x = 0
        for j in range(i-window, i):
            x = x + list[j]
        x = x/window
        five_list.append(x)
def many_element_window(list, w_list, index):
    for i in range(math.floor(index/2)):
        w_list.append(False)
    for i in range(math.floor(index/2), fnum-math.floor(index/2)):
        count = 0
        for j in range(i, i+index):
            if (list[i] == True):
                count = count+1
            else:
                count = count-1
        if (count > 0):
            w_list.append(True)
        else:
            w_list.append(False)
    for i in range(math.floor(index/2)):
        w_list.append(False)
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
Lplayer1, Lb1 = None, None
Lplayer1, Lb1 = InitializingTLD(Lplayer1, Lb1, left_list[0])
print('Left 2nd')
Lplayer2, Lb2 = None, None
Lplayer2, Lb2 = InitializingTLD(Lplayer2, Lb2, left_list[0])

print('Right 1st')
Rplayer1, Rb1 = None, None
Rplayer1, Rb1 = InitializingTLD(Rplayer1, Rb1, right_list[0])
print('Right 2nd')
Rplayer2, Rb2 = None, None
Rplayer2, Rb2 = InitializingTLD(Rplayer2, Rb2, right_list[0])


print('Tracking Learning and Detection ...')
print('Left 1st')
Lpos1 = []
TrackingLearningAndDetection(Lplayer1, left_list, Lpos1, Lb1, fnum, (0,255,0))
print('Left 2nd')
Lpos2 = []
TrackingLearningAndDetection(Lplayer2, left_list, Lpos2, Lb2, fnum, (0,155,100))

print('Right 1st')
Rpos1 = []
TrackingLearningAndDetection(Rplayer1, right_list, Rpos1, Rb1, fnum, (255,0,0))
print('Right 2nd')
Rpos2 = []
TrackingLearningAndDetection(Rplayer2, right_list, Rpos2, Rb2, fnum, (155,0,100))


# 移動量を計算
print('Calculating migration distance ...')
print('Left 1st')
Ldis1 = []
CalculatingMigrationDistance(Ldis1, Lpos1, fnum)
print('Left 2nd')
Ldis2 = []
CalculatingMigrationDistance(Ldis2, Lpos2, fnum)
print('Right 1st')
Rdis1 = []
CalculatingMigrationDistance(Rdis1, Rpos1, fnum)
print('Right 2nd')
Rdis2 = []
CalculatingMigrationDistance(Rdis2, Rpos2, fnum)


print('Normalizing migration distance ...')
print('Left 1st')
Normalizing(Ldis1)
print('Left 2nd')
Normalizing(Ldis2)
print('Right 1st')
Normalizing(Rdis1)
print('Right 2nd')
Normalizing(Rdis2)


print('Windows frames distance average ...')
print('Left 1st')
L51 = []
Listing_Windows(Ldis1, L51, 5)
print('Left 2nd')
L52 = []
Listing_Windows(Ldis2, L52, 5)
print('Right 1st')
R51 = []
Listing_Windows(Rdis1, R51, 5)
print('Right 2nd')
R52 = []
Listing_Windows(Rdis2, R52, 5)


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
# 左側サーブ位置
lcx, lcy = 530, 90
print('Left 1st')
Lc_diff1 = []
CalculatingDiffFromServicePosition(lcx, lcy, Lc_diff1, Lpos1, fnum)
print('Left 2nd')
Lc_diff2 = []
CalculatingDiffFromServicePosition(lcx, lcy, Lc_diff2, Lpos2, fnum)
# 右側サーブ位置
rcx, rcy = 363, 70
print('Right 1st')
Rc_diff1 = []
CalculatingDiffFromServicePosition(rcx, rcy, Rc_diff1, Rpos1, fnum)
print('Right 2nd')
Rc_diff2 = []
CalculatingDiffFromServicePosition(rcx, rcy, Rc_diff2, Rpos2, fnum)


print('Normalizing diff from service position ...')
print('Left 1st')
Normalizing(Lc_diff1)
print('Left 2nd')
Normalizing(Lc_diff2)
print('Right 1st')
Normalizing(Rc_diff1)
print('Right 2nd')
Normalizing(Rc_diff2)

'''
out = False
inplay = True
for i in range(fnum):
    if (Ldis1[i] <= Ldis1_ave/10 and Rdis1[i] <= Rdis1_ave/10):
        OutOfPlay.append(out) # Out of Play
    else:
        OutOfPlay.append(inplay) # In Play


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
