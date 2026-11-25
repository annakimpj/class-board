# 헤어 손질: 조금 키우고 살짝 내림 (원본 = 예전 hair-N.png, hair-N-g.png). 귀가 보이는 머리는 예전 귀 구멍을 머리카락으로 메움
# 귀는 ear-0~4.png(몸에서 뗀 귀)를 머리 위에 따로 그림 (avatar.js AV_EAR) → 머리를 키워도 귀는 늘 하나, 제자리
# python3 hairfix.py 원본폴더 출력폴더
from PIL import Image; import numpy as np; from scipy import ndimage
import sys
SRC,OUT=sys.argv[1],sys.argv[2]
SHOWEAR={0,1,4,5,6,7,9,10}; LOOP={4}                      # 귀가 보이는 머리 (avatar.js AV_EAR와 같게)
W,H=258,386; K=1.05; CXY=(129,165); DOWN=2
yy,xx=np.mgrid[:H,:W]
ell=((xx-128)/75.5)**2+((yy-140)/78)**2>1
zone=(yy>=146)&(yy<=203)&((xx<=66)|(xx>=190))
for i in range(5):  # 귀 그림
  b=np.array(Image.open(f'base-{i}.png')); E=(b[...,3]>128)&zone&ell; E=ndimage.binary_opening(E,iterations=2)  # 귀 덩어리만 (머리 테두리 가는 선 빼고)
  m=(b[...,3]>0)&zone&ndimage.binary_dilation(E,iterations=3)&(yy>=150)
  e=b.copy(); e[~m,3]=0; Image.fromarray(e).save(f'{OUT}/ear-{i}.png',optimize=True)
ear=ndimage.binary_dilation((np.array(Image.open('base-0.png'))[...,3]>128)&zone&ell,iterations=1)
near=ndimage.distance_transform_edt(~ear)<=14
def tf(im):
  w,h=round(W*K),round(H*K); big=im.resize((w,h),Image.LANCZOS)
  c=Image.new('RGBA',(W,H)); c.alpha_composite(big,(round(CXY[0]-CXY[0]*K),round(CXY[1]-CXY[1]*K)+DOWN)); return c
for k in range(12):
  ims=[tf(Image.open(f'{SRC}/hair-{k}.png')),tf(Image.open(f'{SRC}/hair-{k}-g.png'))]
  a=np.array(ims[0]).astype(float); A=a[...,3]>128
  hole=ndimage.binary_closing(A,iterations=7)&~A&near
  dark=a[...,:3].max(-1)<90
  fill=hole|(A&dark&(ndimage.distance_transform_edt(~hole)<=8)&near)
  for j,im in enumerate(ims):
    b=np.array(im).astype(float)
    if k in SHOWEAR and fill.any():
      src=A&~dark&~fill; _,idx=ndimage.distance_transform_edt(~src,return_indices=True)
      b[fill]=b[idx[0][fill],idx[1][fill]]; b[fill,3]=255
    if k in LOOP: b[near&ell&(yy>=146)&(yy<=210),3]=0   # 스포츠머리: 귀를 감싸던 머리 고리를 뺌 (귀는 ear 그림이 덮음)
    Image.fromarray(b.round().clip(0,255).astype(np.uint8)).save(f'{OUT}/hair-{k}{"-g" if j else ""}.png',optimize=True)
