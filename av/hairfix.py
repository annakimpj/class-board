# 헤어 손질: 조금 키우고 내림. 귀가 보이는 머리는 예전 귀 구멍 테두리를 머리카락으로 채우고 몸 귀 자리만 비움 (귀가 둘로 보이지 않게)
# python3 hairfix.py 원본폴더 출력폴더   (원본 = 예전 hair-N.png, hair-N-g.png)
from PIL import Image; import numpy as np; from scipy import ndimage
import sys
SRC,OUT=sys.argv[1],sys.argv[2]
SHOWEAR={0,1,4,5,6,7,9,10}                      # 귀가 보이는 머리 (나머지는 머리카락이 귀를 덮음)
W,H=258,386; K=1.05; CXY=(129,130); DOWN=3      # 키우는 배율·중심, 내리는 px
yy,xx=np.mgrid[:H,:W]
body=np.array(Image.open('base-0.png'))[...,3]>128
ell=((xx-128)/75.5)**2+((yy-140)/78)**2>1          # 머리 동그라미 밖
ear=body&(yy>=150)&(yy<=199)&((xx<=64)|(xx>=192))&ell  # 몸 귀
near=ndimage.distance_transform_edt(~ear)<=12
def tf(im):
  w,h=round(W*K),round(H*K); big=im.resize((w,h),Image.LANCZOS)
  c=Image.new('RGBA',(W,H)); c.alpha_composite(big,(round(CXY[0]-CXY[0]*K),round(CXY[1]-CXY[1]*K)+DOWN)); return c
for k in range(12):
  ims=[tf(Image.open(f'{SRC}/hair-{k}.png')),tf(Image.open(f'{SRC}/hair-{k}-g.png'))]
  a=np.array(ims[0]).astype(float); A=a[...,3]>128
  hole=ndimage.binary_closing(A,iterations=7)&~A&near
  dark=a[...,:3].max(-1)<90
  ring=A&dark&(ndimage.distance_transform_edt(~hole)<=6)&near
  fill=hole|ring
  for j,im in enumerate(ims):
    b=np.array(im).astype(float)
    if k in SHOWEAR:
      src=A&~dark&~ring
      _,idx=ndimage.distance_transform_edt(~src,return_indices=True)
      b[fill]=b[idx[0][fill],idx[1][fill]]; b[fill,3]=255
      b[ear,3]=0
      b[near&ell&~(A&~dark),3]=0   # 귀 둘레 옛 선·흐린 픽셀
      M=b[...,3]>0; lab,n=ndimage.label(M); sz=ndimage.sum(M,lab,range(1,n+1)); b[np.isin(lab,1+np.where(sz<60)[0]),3]=0  # 떨어진 부스러기
    Image.fromarray(b.round().clip(0,255).astype(np.uint8)).save(f'{OUT}/hair-{k}{"-g" if j else ""}.png',optimize=True)
