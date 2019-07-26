#-*- coding:utf-8 -*-
import cv2
import numpy as np
import os
import math

def color_detect(bgr_img):
    hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)

    # 白色検出(ネット)
    hsv_min = np.array([0, 0, 200])
    hsv_max = np.array([179, 120, 255])
    white = cv2.inRange(hsv_img, hsv_min, hsv_max)

    # 緑色検出(コートラインとポール)
    hsv_min = np.array([30, 0, 0])
    hsv_max = np.array([110, 255, 255])
    green = cv2.inRange(hsv_img, hsv_min, hsv_max)
    return white

# 動画ファイル読み込み
print('Reading a video file...')
idn = 'capDatas'    # 読み込む動画のディレクトリ
vn = 'data1_S_1'    # 動画ファイル名
fe_video = '.mp4'   # 拡張子
vfn = vn + fe_video

cap = cv2.VideoCapture(idn +'/'+ vfn)

# 動画情報の取得
print('Getting video informations...')
fnum = int(math.floor(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
fps = int(math.ceil(cap.get(cv2.CAP_PROP_FPS)))
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cap.get(cv2.CAP_PROP_FOURCC)

print('Masking image...')
fnum = int(0.7*fnum)
frame_list = []
mask_list = []
for i in range(fnum):
    ret, frame = cap.read()
    frame_list.append(frame)

    mask = color_detect(frame)
    mask_list.append(mask)

print('Dilating mask...')
for i in range(fnum):
    kernel = np.ones((5,5), np.uint8)
    mask_list[i] = cv2.dilate(mask_list[i], kernel, iterations=1)
    mask_list[i] = cv2.morphologyEx(mask_list[i], cv2.MORPH_OPEN, kernel)

diff_list = []
for i in range(1, fnum-1):
    f1 = mask_list[i-1]
    f2 = mask_list[i]
    f3 = mask_list[i+1]

    diff1 = cv2.absdiff(f1, f2)
    diff2 = cv2.absdiff(f2, f3)

    # 2つの差分画像の論理積
    diff = cv2.bitwise_and(diff1, diff2)
    diff_list.append(diff)

print('Saving image...')
odn = 'screenCaps/'+ vn +'_whitesub' # フレーム保存ディレクトリ
if not os.path.exists(odn):
    os.mkdir(odn)
for i in range(0, fnum-2, 50):
    cv2.imwrite(odn +'/sub_'+ str(i) +'.jpg', diff_list[i])
'''
for i in range(0,fnum,50):
    cv2.imwrite(odn +'/frame_'+ str(i) +'.jpg', mask_list[i])
'''

cap.release()
cv2.destroyAllWindows()
