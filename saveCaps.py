# フレーム保存
import numpy as np
import cv2
import os
import math

# 動画ファイル読み込み
idn = 'capDatas'    # 読み込む動画のディレクトリ
vn = 'data1_S_4'    # 動画ファイル名
fe_video = '.mp4'   # 拡張子
vfn = vn + fe_video

cap = cv2.VideoCapture(idn +'/'+ vfn)

# 動画情報の取得
fnum = int(math.floor(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
fps = int(math.ceil(cap.get(cv2.CAP_PROP_FPS)))
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cap.get(cv2.CAP_PROP_FOURCC)

print(vn)
print('frame num : '+ str(fnum))
#print('frame rate : '+ str(fps))
#print('fourcc : '+ str(fourcc))


fnum = int(fnum*0.999)

'''
odn = 'screenCaps/'+ vn +'_truelabel' # フレーム保存ディレクトリ
if not os.path.exists(odn):
    os.mkdir(odn)

rate = 0.05

for i in range(fnum):
    is_read, frame = cap.read()
    cv2.imwrite(odn +'/frame_'+ str(i) +'.jpg', frame)
    if((i/fnum) >= rate):
        print(str(rate*100) +'%')
        rate = rate + 0.05
'''
