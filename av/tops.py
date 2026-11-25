# 상의 시트(raw/top1~3.webp, 저장소에 없음)를 잘라 av/top-0~39.png로. av/ 안에서: python3 tops.py ./
GRID={
 'top1':[(21,242,[(75,375),(420,732),(807,1113),(1171,1492)]),(266,487,[(69,355),(426,730),(799,1126),(1186,1505)]),(526,735,[(67,377),(434,737),(803,1126),(1196,1494)]),(767,991,[(63,378),(433,742),(818,1118),(1188,1505)])],
 'top2':[(120,385,[(35,335),(373,698),(717,1028),(1050,1376)]),(414,689,[(27,340),(370,699),(726,1016),(1050,1376)]),(739,1026,[(11,339),(370,683),(703,1022),(1043,1363)])],
 'top3':[(99,330,[(34,335),(379,685),(721,1040),(1084,1416)]),(412,648,[(23,343),(372,692),(735,1026),(1080,1410)]),(728,960,[(7,360),(381,696),(749,1014),(1062,1432)])],
}
def cells():
  out=[]
  for f,rows in GRID.items():
    a=np.array(Image.open(f'raw/{f}.webp').convert('RGB')).astype(float)
    for y0,y1,cols in rows:
      for x0,x1 in cols: out.append(np.pad(a,((12,12),(12,12),(0,0)),constant_values=255)[y0+2:y1+23,x0+2:x1+23])
  return out
from PIL import Image; import numpy as np; from scipy import ndimage
import sys, os
AV='./'; OUT=sys.argv[1] if len(sys.argv)>1 else './'
W,H=516,772; S=2   # 2배 캔버스에서 작업
INK=np.array([45,34,38.]); TEE=np.array([246,244,241.])
SC=0.48*S; TOPY=203*S; CX=129*S
OPEN={2,6,12,26}           # 앞이 열린 자켓: 사이를 흰 티로
HOLE={17,19,20,21,23}       # 목 안쪽 흰 빈 곳이 있는 옷: 흰 티로
NOCUT={0,3,5,8,13,15,16,24,28,29,30,31,33,35,36,37}  # 앞 깃이 목에 걸친 옷: 목선 자르지 않음
DY={}                        # 옷별 위아래 보정 (출력 px)
NECK=dict(ny=207, d=9, nw=19) # 목선: 가운데 y=ny+d, 폭 ±nw (출력 px)
def ramp(m,s=1.2): return np.clip((ndimage.gaussian_filter(m.astype(float),s)-.5)*3+.5,0,1)
head=np.array(Image.open(AV+'base-0.png').resize((W,H),Image.NEAREST))[...,3]>128
yy,xx=np.mgrid[0:H,0:W]
head&=yy<212*S
head=ndimage.binary_erosion(head,iterations=3)
nx=(xx-CX)/(NECK['nw']*S); neck=(np.abs(nx)<1)&(yy<(NECK['ny']+NECK['d']*np.sqrt(np.clip(1-nx**2,0,1)))*S)
def make(k,c):
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
  ring=2
  body=ramp(ndimage.binary_erosion(a,iterations=ring)); item=ramp(a)
  outer=ramp(ndimage.distance_transform_edt(~a)<=1)
  core=ndimage.binary_erosion(a,iterations=ring)
  _,idx=ndimage.distance_transform_edt(~core,return_indices=True); rgb=rgb[idx[0],idx[1]]
  # 원래 선은 그대로 살리고, 가장자리만 새 선
  out=body[...,None]*rgb+(1-body[...,None])*INK; al=np.maximum(item,outer)
  # 흰 티 안쪽 옷과 닿는 곳에 얇은 선
  if tm.any():
    tl=(tm&a&ndimage.binary_dilation(a&~tm,iterations=2))|(rib&ndimage.binary_dilation(~a|~tm,iterations=1)&(yy>yc-S))|(tm&a&(yy>=yc+3*S)&(yy<yc+4*S)&(np.abs(tx)<1.1))
    f=ramp(tl,.7)[...,None]*.9; out=f*INK+(1-f)*out
  img=Image.fromarray(np.dstack([out,al*255]).round().clip(0,255).astype(np.uint8)).resize((W//2,H//2),Image.LANCZOS)
  img.save(f'{OUT}top-{k}.png',optimize=True)
C=cells()
for k,c in enumerate(C): make(k,c)
