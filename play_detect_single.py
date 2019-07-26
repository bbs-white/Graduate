#-*- coding:utf-8 -*-
import cv2
import numpy as np
import os
import math
import csv
import gc

def InitializingTLD(player, box, iniframe):
    player = cv2.TrackerTLD_create()
    box = (0, 0, 10, 10)
    box = cv2.selectROI(iniframe, False)
    ok = player.init(iniframe, box)
    cv2.destroyAllWindows()
    return player, box
def TrackingLearningAndDetection(player, flist, box, color):
    rate = 0.14
    pos = []
    for i in range(len(flist)):
        if (i/len(flist) >= rate):
            print(str(round(rate*100))+'%')
            rate = rate + 0.14
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
def CalculatingMigrationDistance(pos):
    MigDis = []
    MigDis.append(0.0)
    for i in range(1, len(pos)):
        _xu = pos[i][0] - pos[i-1][0]
        _xd = pos[i][1] - pos[i-1][1]
        x = math.sqrt(math.pow(_xd,2) + math.pow(_xu,2))
        MigDis.append(x)
    return MigDis
def CalculatingDiffFromServicePosition(cx, cy, pos):
    c_diff = []
    c_diff.append(0.0)
    for i in range(1, len(pos)):
        _cx = cx - pos[i][0]
        _cy = cy - pos[i][1]
        x = math.sqrt(math.pow(_cx,2) + math.pow(_cy,2))
        c_diff.append(x)
    return c_diff
def Normalizing(list):
    list_max = max(list)
    for i in range(len(list)):
        list[i] = list[i]/list_max
        if (list[i] >= 0.8):
            list[i] = list[i-1]
    list_max = max(list)
    for i in range(len(list)):
        list[i] = list[i]/list_max
def Listing_Windows(list, window):
    new_list = []
    for i in range(window):
        x = 0
        for j in range(i+1):
            x = x + list[j]
        x = x/(i+1)
        new_list.append(x)
    for i in range(window, len(list)):
        x = 0
        for j in range(i-window, i):
            x = x + list[j]
        x = x/window
        new_list.append(x)
    return new_list
def many_element_window(list, index):
    w_list = []
    for i in range(math.floor(index/2)):
        w_list.append(False)
    for i in range(math.floor(index/2), len(list)-math.floor(index/2)):
        count = 0
        for j in range(i-math.floor(index/2), i+math.floor(index/2)):
            if (list[j] == True):
                count = count+1
            else:
                count = count-1
        if (count > 0):
            w_list.append(True)
        elif (count < 0):
            w_list.append(False)
        else:
            w_list.append(list[i])
    for i in range(math.floor(index/2)):
        w_list.append(False)
    return w_list
def converting2num(list):
    inplay = 1
    out = -1
    new_list = []
    for i in range(len(list)):
        if (list[i] == True):
            new_list.append(inplay)
        else:
            new_list.append(out)
    return new_list
def detectinterval(list, space):
    new_list = []
    for i in range(len(list)):
        new_list.append(list[i])
    for i in range(20, len(new_list)-space):
        if (new_list[i-1] == True and new_list[i] == False):
            count_in = 0
            for j in range(i, i+space):
                if (new_list[j] == True):
                    count_in = count_in+1
            if (count_in <= space*0.5):
                for j in range(i, i+space):
                    new_list[j] = False
                i = i+int(space*0.9)
            else:
                i = i+int(space*0.3)
    return new_list
def copyList(list):
    new_list = []
    for i in range(len(list)):
        new_list.append(list[i])
    return new_list
def repair_out(list):
    new_list = []
    for i in range(len(list)):
        new_list.append(list[i])
    for i in range(len(new_list)):
        if (new_list[i] == True):
            in_prev = 0
            for j in range(i, len(new_list)):
                if (new_list[j] == True):
                    in_prev = in_prev + 1
                else:
                    break

            out_count = 0
            for j in range(i+in_prev, len(new_list)):
                if (new_list[j] == False):
                    out_count = out_count + 1
                else:
                    break

            in_next = 0
            for j in range(i+in_prev+out_count, len(new_list)):
                if (new_list[j] == True):
                    in_next = in_next + 1
                else:
                    break

            if (int((in_prev+in_next)*0.9) >= out_count and out_count <= 80):
                for j in range(i+in_prev, i+in_prev+out_count):
                    new_list[j] = True
            i = i + in_prev + out_count + in_next
    return new_list
def repair_inplay(list):
    new_list = []
    for i in range(len(list)):
        new_list.append(list[i])

    in_count = 0
    for i in range(len(list)):
        if (new_list[i] == True):
            in_count = in_count + 1
        else:
            if (in_count <= 60 and in_count > 0):
                for j in range(i - in_count, i):
                    new_list[j] = False
            in_count = 0
    return new_list


# 動画ファイル読み込み
vn = 'data1_S_6'    # 動画ファイル名
print('Reading a video file ['+ str(vn) +'] ...')
cap = cv2.VideoCapture('capDatas/'+ vn +'.mp4')

# 動画情報の取得
fnum = int(math.floor(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
fps = int(math.ceil(cap.get(cv2.CAP_PROP_FPS)))
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cap.get(cv2.CAP_PROP_FOURCC)
fnum = int(0.999*fnum)
print('fnum : '+ str(fnum))


print('Reading frames ...')
frame_list = []
for i in range(fnum):
    ret, frame = cap.read()
    frame_list.append(frame)
cap.release()


print('Clipping Player ...')
print('Left')
left_list = []
for i in range(fnum):
    left_img = frame_list[i][int(H*0.4):H, 0:int(W*0.7)]
    left_list.append(left_img)
del left_img
print('Right')
right_list = []
for i in range(fnum):
    right_img = frame_list[i][int(H*0.4):int(H*0.6), int(W*0.45):int(W*0.87)]
    right_list.append(right_img)
del right_img
gc.collect()


Lplayer, Lb = None, None
Lplayer, Lb = InitializingTLD(Lplayer, Lb, left_list[0])
Rplayer, Rb = None, None
Rplayer, Rb = InitializingTLD(Rplayer, Rb, right_list[0])


print('Tracking Learning and Detection ...')
print('Left')
Lpos = TrackingLearningAndDetection(Lplayer, left_list, Lb, (0,255,0))
print('Right')
Rpos = TrackingLearningAndDetection(Rplayer, right_list, Rb, (255,0,0))

window_num = 10
print('Calculating migration distance ...')
Ldis = CalculatingMigrationDistance(Lpos)
Rdis = CalculatingMigrationDistance(Rpos)
Ldis_w = Listing_Windows(Ldis, window_num)
Rdis_w = Listing_Windows(Rdis, window_num)


print('Normalizing migration distance ...')
Normalizing(Ldis)
Normalizing(Rdis)
Normalizing(Ldis_w)
Normalizing(Rdis_w)


print('Calculating diff from service position ...')
Lcd = CalculatingDiffFromServicePosition(530, 90, Lpos)
Rcd = CalculatingDiffFromServicePosition(363, 70, Rpos)
Lcd_w = Listing_Windows(Lcd, window_num)
Rcd_w = Listing_Windows(Rcd, window_num)


print('Normalizing migration distance ...')
Normalizing(Lcd)
Normalizing(Rcd)
Normalizing(Lcd_w)
Normalizing(Rcd_w)


print('Calculating average ...')
Ldis_ave = sum(Ldis_w)/fnum
Lc_ave = sum(Lcd_w)/fnum
Rdis_ave = sum(Rdis_w)/fnum
Rc_ave = sum(Rcd_w)/fnum
print('Ldis_ave :'+ str(Ldis_ave))
print('Lc_ave : '+ str(Lc_ave))
print('Rdis_ave :'+ str(Rdis_ave))
print('Rc_ave : '+ str(Rc_ave))


# 移動距離の平均で閾値
print('Detecting Rally ...')
PL1 = []
for i in range(fnum):
    if (Ldis_w[i] <= Ldis_ave and Rdis_w[i] <= Rdis_ave):
        PL1.append(False) # Out of Play
    else:
        PL1.append(True)
PL2 = copyList(PL1)
for i in range(fnum):
    if (Lcd_w[i] <= Lc_ave and Rcd_w[i] <= Rc_ave):
        PL2[i] = False
    else:
        PL2[i] = True

PL3 = many_element_window(PL1, 9)
PL4 = many_element_window(PL2, 15)
PL5 = detectinterval(PL4, 170)
PL6 = repair_out(PL5)
PL7 = repair_inplay(PL6)


print('Saving data in Excel ...')
f = open(vn+'_serve.csv','w')
writer = csv.writer(f, lineterminator='\n')

writer.writerow(Ldis)
writer.writerow(Rdis)
writer.writerow(Ldis_w)
writer.writerow(Rdis_w)
writer.writerow(Lcd)
writer.writerow(Rcd)
writer.writerow(Lcd_w)
writer.writerow(Rcd_w)
writer.writerow(converting2num(PL1))
writer.writerow(converting2num(PL2))
writer.writerow(converting2num(PL3))
writer.writerow(converting2num(PL4))
writer.writerow(converting2num(PL5))
writer.writerow(converting2num(PL6))
writer.writerow(converting2num(PL7))
