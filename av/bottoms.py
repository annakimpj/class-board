# 하의 시트(raw/bot7~10.webp, 저장소에 없음)를 잘라 av/bottom-N.png로. av/ 안에서: python3 bottoms.py ./
# 순서: bot8(예전 하의 12개, 번호 그대로) → bot7 → bot9 → bot10
from PIL import Image; import numpy as np; from scipy import ndimage
import sys
OUT=sys.argv[1] if len(sys.argv)>1 else './'
W,H=516,772; S=2                      # 2배 캔버스에서 작업
INK=np.array([45,34,38.])
TOPY=248; CX=129*S                    # 허리 위 끝 (출력 px), 상의 밑에 들어감
WAIST=70                              # 허리 폭 (출력 px): 몸통 60 + 여유
FOOT=374                              # 긴 바지·치마 끝 (발목). 이보다 길면 세로로 줄임
SHEETS=['bot8','bot7','bot9','bot10']
def ramp(m,s=1.2): return np.clip((ndimage.gaussian_filter(m.astype(float),s)-.5)*3+.5,0,1)
def items(f):
  a=np.array(Image.open(f'raw/{f}.webp').convert('RGB')).astype(float)
  m=a.min(-1)<220; lab,n=ndimage.label(ndimage.binary_dilation(m,iterations=8))
  objs=[s for s in ndimage.find_objects(lab) if (s[0].stop-s[0].start)*(s[1].stop-s[1].start)>8000]
  objs=sorted(objs,key=lambda s:s[0].start); rows=[]  # 위 끝이 비슷한 것끼리 한 줄 → 줄마다 왼쪽부터
  for o in objs:
    if rows and o[0].start-rows[-1][0][0].start<150: rows[-1].append(o)
    else: rows.append([o])
  objs=[o for r in rows for o in sorted(r,key=lambda s:s[1].start)]
  out=[]
  for s in objs:
    y0,y1,x0,x1=max(s[0].start-4,0),s[0].stop+4,max(s[1].start-4,0),s[1].stop+4
    out.append(a[y0:y1,x0:x1])
  return out
def make(c,name):
  dark=c.min(-1)<220
  m=ndimage.binary_fill_holes(ndimage.binary_closing(dark,iterations=2))
  lab,n=ndimage.label(m); sz=ndimage.sum(m,lab,range(1,n+1)); m=np.isin(lab,1+np.where(sz>800)[0])
  light=(c.mean(-1)>165)&(c.max(-1)-c.min(-1)<70)
  m&=~((ndimage.distance_transform_edt(m)<=3)&light); m=ndimage.binary_opening(m,iterations=1)
  core=ndimage.binary_erosion(m,iterations=1)
  _,idx=ndimage.distance_transform_edt(~core,return_indices=True); rgb=c[idx[0],idx[1]]
  ys,xs=np.where(m); y0=ys.min()
  band=np.where(m[y0+4:y0+16].any(0))[0]; ww=band.max()-band.min()        # 허리띠 폭
  im=Image.fromarray(np.dstack([rgb,m*255.]).astype(np.uint8)).crop((xs.min(),y0,xs.max()+1,ys.max()+1))
  k=WAIST*S/ww; sw,sh=round(im.width*k),round(im.height*k)
  if TOPY+sh/S>FOOT: sh=round((FOOT-TOPY)*S)
  im=im.resize((sw,sh),Image.LANCZOS)
  cx=(band.min()+band.max())/2-xs.min()
  ox,oy=round(CX-cx*k),TOPY*S
  cv=np.zeros((H,W,4)); cv[oy:oy+sh,ox:ox+sw]=np.array(im)
  a=ndimage.binary_opening(cv[...,3]>128,iterations=1); rgb=cv[...,:3]
  ring=2; body=ramp(ndimage.binary_erosion(a,iterations=ring)); item=ramp(a)
  outer=ramp(ndimage.distance_transform_edt(~a)<=1)
  core=ndimage.binary_erosion(a,iterations=ring)
  _,idx=ndimage.distance_transform_edt(~core,return_indices=True); rgb=rgb[idx[0],idx[1]]
  out=body[...,None]*rgb+(1-body[...,None])*INK; al=np.maximum(item,outer)
  Image.fromarray(np.dstack([out,al*255]).round().clip(0,255).astype(np.uint8)).resize((W//2,H//2),Image.LANCZOS).save(f'{OUT}bottom-{name}.png',optimize=True)
k=0
for f in SHEETS:
  its=items(f); print(f,len(its))
  for c in its: make(c,k); k+=1
