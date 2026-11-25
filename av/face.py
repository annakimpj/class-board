# 새 몸(raw/1.webp)·눈(raw/2.webp)·입(raw/3.webp) 시트를 잘라 av/에 맞춤. 흰 테두리 빼고 검정 테두리 새로 부드럽게
from PIL import Image; import numpy as np; from scipy import ndimage
OUT='./'  # av/ 안에서 실행. 원본 시트 raw/1.webp(몸) raw/2.webp(눈) raw/3.webp(입)는 저장소에 없음
INK=np.array([45,34,38.])
def ramp(m,s): return np.clip((ndimage.gaussian_filter(m.astype(float),s)-.5)*3+.5,0,1)
def clean(a, th, near_px, ring, soft):
  # a: RGB(float) 흰 배경. th: 배경과 나눌 밝기. near_px: 바깥에서 이만큼 안쪽까지의 밝은 픽셀은 흰 테두리로 보고 뺌
  dark=a.min(-1)<th
  m=ndimage.binary_fill_holes(ndimage.binary_closing(dark,iterations=2))
  light=(a.mean(-1)>165)&(a.max(-1)-a.min(-1)<70)
  m&=~((ndimage.distance_transform_edt(m)<=near_px)&light)
  m=ndimage.binary_opening(m,iterations=1); m=ndimage.binary_fill_holes(m)
  core=ndimage.binary_erosion(m,iterations=2) if ring else m
  _,idx=ndimage.distance_transform_edt(~core,return_indices=True)
  rgb=a[idx[0],idx[1]]
  item=ramp(m,soft)
  if ring:  # 고른 검정 테두리 (안쪽 ring px + 바깥 ring/2 px)
    inner=item*(1-ramp(ndimage.binary_erosion(m,iterations=ring),soft))
    outer=ramp(ndimage.distance_transform_edt(~m)<=ring/2,soft)
    edge=np.maximum(inner,outer*(1-item))
    body=ramp(ndimage.binary_erosion(m,iterations=ring),soft)
    rgb=body[...,None]*rgb+(1-body[...,None])*INK
    alpha=np.maximum(item,outer)
  else: alpha=item
  return Image.fromarray(np.dstack([rgb,alpha*255]).round().astype(np.uint8))
def fit(im,k): return im.resize((round(im.width*k),round(im.height*k)),Image.LANCZOS)
# 몸
a=np.array(Image.open('raw/1.webp').convert('RGB')).astype(float)
m=ndimage.binary_fill_holes(a.min(-1)<225); lab,_=ndimage.label(m)
objs=sorted([s for s in ndimage.find_objects(lab) if s[0].stop-s[0].start>300],key=lambda s:s[1].start)
for i,s in enumerate(objs):
  y0,y1,x0,x1=s[0].start-8,s[0].stop+8,s[1].start-8,s[1].stop+8
  sub=a[y0:y1,x0:x1].copy(); keep=ndimage.binary_dilation(lab[y0:y1,x0:x1]==lab[s][lab[s]>0][0],iterations=6); sub[~keep]=255
  im=clean(sub,225,5,5,1.2); bb=im.getbbox(); im=im.crop(bb)
  k=322/im.height; im=fit(im,k); c=Image.new('RGBA',(W,H)); c.alpha_composite(im,(round(129-im.width/2),384-im.height)); c.save(f'{OUT}base-{i}.png',optimize=True)
# 눈·입
def parts(f,rows,cols,name,s,place):
  a=np.array(Image.open(f'raw/{f}.webp').convert('RGB')).astype(float); k=0
  for y0,y1 in rows:
    for x0,x1 in cols:
      sub=a[y0-8:y1+9,x0-8:x1+9]; im=fit(clean(sub,215,3,0,.9),s)
      c=Image.new('RGBA',(W,H)); c.alpha_composite(im,place(im)); c.save(f'{OUT}{name}-{k}.png',optimize=True); k+=1
# 자리: 예전과 같게 (눈 0.38배 위 140, 입 0.24배 가운데 200). 여백 8px 늘어난 만큼 보정
parts('2',[(156,287),(437,566),(708,839),(991,1127)],[(30,284),(340,602),(647,915),(963,1211)],'eye',.38,lambda im:(round(129-im.width/2),round(140-2*.38)))
parts('3',[(219,304),(464,543),(702,790),(958,1028)],[(126,268),(409,560),(705,827),(982,1115)],'mouth',.24,lambda im:(round(129-im.width/2),round(200-im.height/2)))
