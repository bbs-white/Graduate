#-*- coding:utf-8 -*-
import cv2
import numpy as np
import os
import math

def color_detect(bgr_img):
    hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)

    # 白色検出
    hsv_min = np.array([0, 0, 200])
    hsv_max = np.array([179, 120, 255])
    white = cv2.inRange(hsv_img, hsv_min, hsv_max)

    # 緑色検出(コートラインとポール)
    hsv_min = np.array([30, 0, 0])
    hsv_max = np.array([110, 255, 255])
    green = cv2.inRange(hsv_img, hsv_min, hsv_max)
    return white

# 動画ファイル読み込み
idn = 'capDatas'    # 読み込む動画のディレクトリ
vn = 'data1_S_1'    # 動画ファイル名
fe_video = '.mp4'   # 拡張子
vfn = vn + fe_video
print('Reading a video file ['+ str(vfn) +']...')

frame_list = []
mask_list = []
tld_list = []

cap = cv2.VideoCapture(idn +'/'+ vfn)

# 動画情報の取得
fnum = int(math.floor(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
fps = int(math.ceil(cap.get(cv2.CAP_PROP_FPS)))
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cap.get(cv2.CAP_PROP_FOURCC)
fnum = int(fnum/5)

print('Reading frames...')
for i in range(fnum):
    ret, frame = cap.read()
    # frame = cv2.resize(frame, (int(W/3), int(H/3)))
    frame_list.append(frame)
    tld_list.append(frame)

'''
# 指定領域をマスキング
print('Masking image...')
for i in range(fnum):
    mask = color_detect(frame_list[i])
    mask_list.append(mask)

# マスク領域を少し膨らませる
print('Dilating mask...')
for i in range(fnum):
    kernel = np.ones((3,3), np.uint8)
    mask_list[i] = cv2.dilate(mask_list[i], kernel, iterations=1)
    mask_list[i] = cv2.morphologyEx(mask_list[i], cv2.MORPH_OPEN, kernel)
'''
# TLDの初期化
print('Making Tracker...')
frame = tld_list[0]
ball = cv2.TrackerTLD_create()
b1 = (0, 0, 10, 10)
b1 = cv2.selectROI(frame, False)
ok = ball.init(frame, b1)

# TLDの初期化
print('Tracking Learning Detection...')
for i in range(fnum):
    # 1人目の追跡
    track, b1 = ball.update(tld_list[i])
    if track:
        p1 = (int(b1[0]), int(b1[1]))
        p2 = (int(b1[0] + b1[2]), int(b1[1] + b1[3]))
        cv2.rectangle(tld_list[i], p1, p2, (0, 255, 0), 2, 1)
    else:
        cv2.putText(tld_list[i], "Failure", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA);

# 結果画像を保存
print('Saving image...')
odn = 'screenCaps/'+ vn # フレーム保存ディレクトリ
if not os.path.exists(odn):
    os.mkdir(odn)
for i in range(1, fnum, 10):
    cv2.imwrite(odn +'/ball_'+ str(i) +'.jpg', tld_list[i])

cap.release()
cv2.destroyAllWindows()
