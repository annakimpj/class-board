# 새 하의 시트 2장(raw_new/s18.webp, s19.webp, 저장소에 없음) → av/bottom-12~31.png. bottoms.py와 같은 방식이지만 골반선에 맞추고(HIP) 허리는 셔츠보다 좁게(WAISTW), 짧은 하의는 늘리고(MINHEM), 긴 바지는 신발 위까지(LONG)
# 하의 시트(raw/bot7~10.webp, 저장소에 없음)를 잘라 av/bottom-N.png로. av/ 안에서: python3 bottoms.py ./
# 하의 12개 (bot8)
from PIL import Image; import numpy as np; from scipy import ndimage
import sys, os
sys.path.insert(0,r'C:/Users/user/Documents/GitHub/geulgam/av'); from outline import uniform
OUT=sys.argv[1] if len(sys.argv)>1 else './'
W,H=516,772; S=2                      # 2배 캔버스에서 작업
INK=np.array([45,34,38.])
TOPY=260; CX=129*S                    # 허리 위 끝 (출력 px). 상의 밑단 안쪽에서 시작해 허리가 상의보다 넓어 보이지 않게
WAIST=64                              # 허리 폭 (출력 px)
FOOT=374                              # 긴 바지·치마 끝 (발목). 이보다 길면 세로로 줄임
MINHEM=325                            # 짧은 하의 밑단 최소 (출력 px). 셔츠 밑단(~290)보다 충분히 아래
LONG=360; LONGIF=328                  # 밑단이 LONGIF 넘는 긴 바지는 LONG(신발 위)까지
WAISTW=60                             # 허리(하의 위 끝) 폭: 셔츠 밑단(~62)보다 좁게
HIPY=298; HIP=84                      # 골반선 y와 그 줄의 하의 폭 (몸 골반 폭 74 + 테두리·여유). 허벅지가 안 삐져나오게
SHEETS=['s18','s19']
def ramp(m,s=1.2): return np.clip((ndimage.gaussian_filter(m.astype(float),s)-.5)*3+.5,0,1)
def items(f):
  a=np.array(Image.open(f'raw_new/{f}.webp').convert('RGB')).astype(float)
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
  # 골반선에 맞춤: 출력 y=HIPY 줄에서 하의 폭이 HIP이 되게 (허리띠 폭 대신). 세로 길이 규칙(MINHEM·LONG)에 따라 그 줄이 바뀌어 몇 번 되풀이
  mm=np.array(im)[...,3]>128; k=WAIST*S/ww
  for _ in range(6):
    sh=round(im.height*k)
    if TOPY+sh/S>=LONGIF: sh=round((LONG-TOPY)*S)   # 긴 바지: 신발 바로 위까지 (신발을 조금 덮어도 됨)
    if TOPY+sh/S<MINHEM: sh=round((MINHEM-TOPY)*S)  # 짧은 치마·반바지: 셔츠 밑으로 보이게 세로로 늘림
    r=min(mm.shape[0]-1,int((HIPY-TOPY)*S*im.height/sh)); xs_=np.where(mm[r])[0]
    k=HIP*S/(xs_.max()-xs_.min())
  sw=round(im.width*k)
  im=im.resize((sw,sh),Image.LANCZOS)
  cx=(band.min()+band.max())/2-xs.min()
  ox,oy=round(CX-cx*k),TOPY*S
  cv=np.zeros((H,W,4)); cv[oy:oy+sh,ox:ox+sw]=np.array(im)
  # 허리 쪽만 좁히기: 위 끝에서 폭이 WAISTW, 골반선(HIPY)부터 원래 폭. 셔츠 밑단보다 하의가 넓어 보이지 않게
  yy,xx=np.mgrid[0:H,0:W]; row=cv[...,3].max(1)>128
  top_=np.where(row)[0][0]; tx=np.where(cv[top_+4,:,3]>128)[0]; f0=min(1,WAISTW*S/(tx.max()-tx.min()))
  t=np.clip((yy-TOPY*S)/((HIPY-TOPY)*S),0,1); f=f0+(1-f0)*t
  src=CX+(xx-CX)/f
  cv=np.stack([ndimage.map_coordinates(cv[...,i],[yy,src],order=1) for i in range(4)],-1)
  a=ndimage.binary_opening(cv[...,3]>128,iterations=1); rgb=cv[...,:3]
  out,al=uniform(a,rgb,S)  # 바깥 선 굵기 통일 (outline.py)
  Image.fromarray(np.dstack([out,al*255]).round().clip(0,255).astype(np.uint8)).resize((W//2,H//2),Image.LANCZOS).save(f'{OUT}bottom-{name}.png',optimize=True)
k=12
for f in SHEETS:
  its=items(f); print(f,len(its))
  for c in its: make(c,k); k+=1
