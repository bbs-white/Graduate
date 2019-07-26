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
idn = 'capDatas'    # 読み込む動画のディレクトリ
vn = 'data1_D_2'    # 動画ファイル名
vfn = vn + '.mp4'

print('Reading a video file ['+ str(vfn) +']...')
cap = cv2.VideoCapture(idn +'/'+ vfn)

# 動画情報の取得
fnum = int(math.floor(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
fnum = int(0.999*fnum)

print('Reading frames ...')
frame_list = []
rate = 0.1
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%')
        rate = rate + 0.1
    ret, frame = cap.read()
    frame_list.append(frame)
del ret
del frame
gc.collect()
cap.release()


print('Masking image...')
mask_list = []
rate = 0.1
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%')
        rate = rate + 0.1
    mask = color_detect(frame_list[i])
    mask_list.append(mask)
del mask
gc.collect()

# マスク領域を少し膨らませる
print('Dilating mask...')
rate = 0.1
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%')
        rate = rate + 0.1
    kernel = np.ones((3,3), np.uint8)
    mask_list[i] = cv2.dilate(mask_list[i], kernel, iterations=1)
    mask_list[i] = cv2.morphologyEx(mask_list[i], cv2.MORPH_OPEN, kernel)
del kernel
gc.collect()

# マスク領域を除去し周りの画素から補完
print('Image Inpainting...')
rate = 0.1
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%')
        rate = rate + 0.1
    frame_list[i] = cv2.inpaint(frame_list[i], mask_list[i], 3, cv2.INPAINT_TELEA)
del mask_list
gc.collect()

# TLDの初期化
print('Making Tracker...')
# 1人目の追跡器の追跡器
player1, b1 = None, None
player1, b1 = InitializingTLD(player1, b1, frame_list[0])
# 2人目の追跡器の初期化
player2, b2 = None, None
player2, b2 = InitializingTLD(player2, b2, frame_list[0])

# TLDの初期化
print('Tracking Learning Detection...')
rate = 0.1
for i in range(fnum):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%')
        rate = rate + 0.1
    # 1人目の追跡
    track1, b1 = player1.update(frame_list[i])
    if track1:
        p1 = (int(b1[0]), int(b1[1]))
        p2 = (int(b1[0] + b1[2]), int(b1[1] + b1[3]))
        cv2.rectangle(frame_list[i], p1, p2, (0, 255, 0), 2, 1)
    else:
        cv2.putText(frame_list[i], "Failure", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA);
    # 2人目の追跡
    track2, b2 = player2.update(frame_list[i])
    if track2:
        p1 = (int(b2[0]), int(b2[1]))
        p2 = (int(b2[0] + b2[2]), int(b2[1] + b2[3]))
        cv2.rectangle(frame_list[i], p1, p2, (255, 0, 0), 2, 1)
    else:
        cv2.putText(frame_list[i], "Failure", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA);


# 結果画像を保存
print('Saving image...')
odn = 'screenCaps/'+ vn +'_II' # フレーム保存ディレクトリ
if not os.path.exists(odn):
    os.mkdir(odn)
rate = 0.1
for i in range(0, fnum, 30):
    if((i/fnum) >= rate):
        print(str(round(rate*100)) +'%')
        rate = rate + 0.1
    cv2.imwrite(odn +'/IIframe_'+ str(i) +'.jpg', frame_list[i])


cv2.destroyAllWindows()
