# 크리스마스 한 벌 옷 시트(raw_new/top5.webp, 저장소에 없음) → av/top-47~54.png. tops-new.py와 같고 시트·크기만 다름. 입으면 하의를 안 그림 (avatar.js AV_FULL)
# 상의 시트(raw/top1~3.webp, 저장소에 없음)를 잘라 av/top-0~39.png로. av/ 안에서: python3 tops.py ./
GRID={'top5': [(185, 545, [(23, 308), (351, 628), (673, 949), (981, 1260)]), (668, 1029, [(26, 301), (346, 620), (663, 939), (980, 1263)])]}
FITS={'top5':0.43}
def cells():
  out=[]
  for f,rows in GRID.items():
    a=np.array(Image.open(f'raw_new/{f}.webp').convert('RGB')).astype(float)
    for y0,y1,cols in rows:
      for x0,x1 in cols: out.append((FITS[f],np.pad(a,((12,12),(12,12),(0,0)),constant_values=255)[y0+2:y1+23,x0+2:x1+23]))
  return out
from PIL import Image; import numpy as np; from scipy import ndimage
import sys, os
sys.path.insert(0,r'C:/Users/user/Documents/GitHub/geulgam/av'); from outline import uniform
AV='./'; OUT=sys.argv[1] if len(sys.argv)>1 else './'
W,H=516,772; S=2   # 2배 캔버스에서 작업
FIT=0.39            # 시트 → 몸 크기 (몸에 맞게)
INK=np.array([45,34,38.]); TEE=np.array([246,244,241.])
SC=FIT*S; TOPY=203*S; CX=129*S
OPEN={2,6,12}
HOLE=set()
NOCUT=set()
DY={}                        # 옷별 위아래 보정 (출력 px)
# 위쪽만 늘려 올리기 (출력 px): 목선은 올리고 소매 끝·밑단(y=WARPY 아래)은 제자리. 후드는 후드가 솟아 목선이 내려가 보여서
WARP={1:-10,4:-10,14:-10,10:-6}; WARPY=264
NECK=dict(ny=207, d=9, nw=19) # 목선: 가운데 y=ny+d, 폭 ±nw (출력 px)
def ramp(m,s=1.2): return np.clip((ndimage.gaussian_filter(m.astype(float),s)-.5)*3+.5,0,1)
head=np.array(Image.open(AV+'base-0.png').resize((W,H),Image.NEAREST))[...,3]>128
yy,xx=np.mgrid[0:H,0:W]
head&=yy<212*S
head=ndimage.binary_erosion(head,iterations=3)
nx=(xx-CX)/(NECK['nw']*S); neck=(np.abs(nx)<1)&(yy<(NECK['ny']+NECK['d']*np.sqrt(np.clip(1-nx**2,0,1)))*S)
def make(k,fc):
  fit,c=fc; SC=fit*S
  dark=c.min(-1)<220
  m=ndimage.binary_fill_holes(ndimage.binary_closing(dark,iterations=2))
  lab,n=ndimage.label(m); sz=ndimage.sum(m,lab,range(1,n+1)); m=np.isin(lab,1+np.where(sz>800)[0])
  light=(c.mean(-1)>165)&(c.max(-1)-c.min(-1)<70)
  m&=~((ndimage.distance_transform_edt(m)<=3)&light); m=ndimage.binary_opening(m,iterations=1)
  tee=np.zeros_like(m)
  if k in OPEN:  # 두 쪽 사이 빈 곳 = 흰 티
    cl=ndimage.binary_closing(m,structure=np.ones((1,121)),iterations=1)
    tee=cl&~m; tee=ndimage.binary_opening(tee,iterations=2)
  core=ndimage.binary_erosion(m,iterations=1)
  _,idx=ndimage.distance_transform_edt(~core,return_indices=True); rgb=c[idx[0],idx[1]]
  rgb[tee]=TEE; m=m|tee
  ys,xs=np.where(m); x0,x1,y0=xs.min(),xs.max(),ys.min()
  # 캔버스로
  im=Image.fromarray(np.dstack([rgb,m*255.]).astype(np.uint8)).crop((x0,y0,x1+1,ys.max()+1))
  t=Image.fromarray((tee*255).astype(np.uint8)).crop((x0,y0,x1+1,ys.max()+1))
  sz=(round(im.width*SC),round(im.height*SC)); im=im.resize(sz,Image.LANCZOS); t=t.resize(sz,Image.LANCZOS)
  ox,oy=round(CX-sz[0]/2),round(TOPY+DY.get(k,0)*S)
  cv=np.zeros((H,W,4)); cv[oy:oy+sz[1],ox:ox+sz[0]]=np.array(im); tv=np.zeros((H,W)); tv[oy:oy+sz[1],ox:ox+sz[0]]=np.array(t)
  if k in WARP:  # 줄 y의 그림을 y-d*w(y)에서 가져옴: 위쪽(w=1)은 d만큼 올라가고 WARPY에서 0
    y0=TOPY+WARP[k]*S; w=np.clip((WARPY*S-yy)/(WARPY*S-y0),0,1); src=yy-WARP[k]*S*w
    cv=np.stack([ndimage.map_coordinates(cv[...,i],[src,xx],order=1) for i in range(4)],-1)
    tv=ndimage.map_coordinates(tv,[src,xx],order=1)
  a=cv[...,3]>128; rgb=cv[...,:3]; tm=tv>128
  a&=~head
  if k in HOLE:  # 목 안쪽 흰 빈 곳(깃 안, 후드 안)도 흰 티로
    wz=(np.abs(xx-CX)<26*S)&(yy<228*S)
    lab,n=ndimage.label(a&(rgb.min(-1)>232))
    for i in range(1,n+1):
      r=lab==i
      if (r&wz).any() and r.sum()<1500*S*S: tm|=r
    if tm.any(): rgb[tm]=TEE
  if k not in NOCUT: a&=~(neck&~tm)
  rib=np.zeros_like(a)
  if tm.any():  # 흰 티 동그란 목선 + 목 시보리
    tx=(xx-CX)/(14*S); yc=(212+6*np.sqrt(np.clip(1-tx**2,0,1)))*S
    tn=(np.abs(tx)<1)&(yy<yc); tm&=a
    a&=~(tn&tm); rib=tm&a&(np.abs(tx)<1.15)&(yy<yc+3*S)
    _rgb=rgb.copy(); rgb[rib]=[222,218,214]
  a=ndimage.binary_opening(a,iterations=1)
  # 고른 검정 테두리 + 부드럽게
  out,al=uniform(a,rgb,S)  # 바깥 선 굵기 통일 (outline.py)
  # 흰 티 안쪽 옷과 닿는 곳에 얇은 선
  if tm.any():
    tl=(tm&a&ndimage.binary_dilation(a&~tm,iterations=2))|(rib&ndimage.binary_dilation(~a|~tm,iterations=1)&(yy>yc-S))|(tm&a&(yy>=yc+3*S)&(yy<yc+4*S)&(np.abs(tx)<1.1))
    f=ramp(tl,.7)[...,None]*.9; out=f*INK+(1-f)*out
  img=Image.fromarray(np.dstack([out,al*255]).round().clip(0,255).astype(np.uint8)).resize((W//2,H//2),Image.LANCZOS)
  img.save(f'{OUT}top-{k}.png',optimize=True)
C=cells()
for k,c in enumerate(C,47): make(k,c)
