# 펫 시트(raw/pet1.webp 12마리, raw/pet2.webp 8마리, 저장소에 없음)를 잘라 av/pet-1~20.png로. av/ 안에서: python3 pets.py ./
# 하늘을 나는 펫은 오른쪽 허공, 나머지는 왼쪽 아래 발치. 반짝이 같은 떨어진 조각은 뺌, 테두리는 옷과 같은 굵기
from PIL import Image; import numpy as np; from scipy import ndimage
import sys, os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from outline import uniform
OUT=sys.argv[1] if len(sys.argv)>1 else './'
W,H=516,772; S=2
AIR={7,8,9,10,11,12,19}          # 펫 번호 (1부터): 날개 고양이, 아기 드래곤, 천사 별, 달 고양이, 로봇, 불새, 천사 종
BOX=66                           # 펫 크기 (출력 px, 긴 쪽)
FOOT=(40,384); SKY=(226,228)     # 발치: 가운데 x·바닥 y / 허공: 가운데 (출력 px)
def items(f):
  a=np.array(Image.open(f'raw/{f}.webp').convert('RGB')).astype(float)
  m=a.min(-1)<225; lab,n=ndimage.label(ndimage.binary_dilation(m,iterations=14))
  objs=[s for s in ndimage.find_objects(lab) if (s[0].stop-s[0].start)*(s[1].stop-s[1].start)>15000]
  objs=sorted(objs,key=lambda s:s[0].start); rows=[]
  for o in objs:
    if rows and o[0].start-rows[-1][0][0].start<150: rows[-1].append(o)
    else: rows.append([o])
  out=[]
  for o in [o for r in rows for o in sorted(r,key=lambda s:s[1].start)]:
    li=lab[o][lab[o]>0]; li=np.bincount(li).argmax()
    out.append((a[o],m[o]&(lab[o]==li)))
  return out
def make(c,m0,n):
  m=ndimage.binary_fill_holes(ndimage.binary_closing(m0,iterations=2))
  lab,k=ndimage.label(m); sz=ndimage.sum(m,lab,range(1,k+1))
  m=np.isin(lab,1+np.where(sz>=sz.max()*0.03)[0])   # 반짝이처럼 작은 조각은 뺌 (후광·날개는 남김)
  light=(c.mean(-1)>200)&(c.max(-1)-c.min(-1)<40)
  m&=~((ndimage.distance_transform_edt(m)<=3)&light)
  ys,xs=np.where(m); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
  core=ndimage.binary_erosion(m,iterations=1); _,idx=ndimage.distance_transform_edt(~core,return_indices=True); rgb=c[idx[0],idx[1]]
  im=Image.fromarray(np.dstack([rgb,m*255.]).astype(np.uint8)).crop((x0,y0,x1,y1))
  k=BOX*S/max(im.size); im=im.resize((round(im.width*k),round(im.height*k)),Image.LANCZOS)
  if n in AIR: ox,oy=SKY[0]*S-im.width//2,SKY[1]*S-im.height//2
  else: ox,oy=FOOT[0]*S-im.width//2,FOOT[1]*S-im.height
  ox=int(np.clip(ox,2*S,W-im.width-2*S))
  cv=np.zeros((H,W,4)); cv[oy:oy+im.height,ox:ox+im.width]=np.array(im)
  out,al=uniform(cv[...,3]>128,cv[...,:3],S)
  Image.fromarray(np.dstack([out,al*255]).round().clip(0,255).astype(np.uint8)).resize((W//2,H//2),Image.LANCZOS).save(f'{OUT}pet-{n}.png',optimize=True)
n=1
for f in ['pet1','pet2']:
  for c,m in items(f): make(c,m,n); n+=1
print(n-1,'pets')
