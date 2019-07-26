# 背景差分法による動体検出
import numpy as np
import cv2
import os

# 動画ファイル読み込み
idn = 'capDatas'    # 読み込む動画のディレクトリ
vn = 'data1_S_1'    # 動画ファイル名
fe_video = '.mp4'   # 拡張子
vfn = vn + fe_video

cap = cv2.VideoCapture(idn +'/'+ vfn)

# 動画情報の取得
fnum = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cap.get(cv2.CAP_PROP_FOURCC)

_, bg = cap.read()
bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
fbg = bg

for i in range(10):
    _, bg = cap.read()
    bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    fbg = cv2.addWeighted(fbg, 0.3, bg, 0.7, 0.1)


th = 50
while(cap.isOpened()):
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    mask = cv2.absdiff(gray, fbg)

    mask[mask < th] = 0
    mask[mask >= th] = 255

    mask = cv2.resize(mask, (int(2*W/3), int(2*H/3)))
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
