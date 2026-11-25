from PIL import Image
import numpy as np
from scipy import ndimage
import sys, os
PX, PY, W, H = 70, 110, 337+140, 632+120   # body sits at (PX,PY) on canvas
OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'
os.makedirs(OUT, exist_ok=True)
EAR_BOTTOM, EAR_CX = 250, 168.5   # body ear bottom y / ear midpoint x
HS = 1.23   # hair sheet -> body scale (from buzz cut ear width 265 vs body 325)
HAIR_FIX = {2: 245, 11: 245}   # no visible ears: assumed ear-bottom y in sprite
TS, TOP_Y, TOP_DY = 1.08, 285, {}   # tops: scale, neckline y on body
BS, BOT_Y, BOT_DY = 0.62, 372, {}   # bottoms: scale, waist y on body
def clean(im):
  # white fringe off + smooth outer edge: drop light pixels near the outside, soften alpha, pull edge color from nearest opaque pixel
  a=np.array(im.convert('RGBA')).astype(float); al=a[...,3]>128
  near=ndimage.distance_transform_edt(al)<=3
  rgb=a[...,:3]; light=(rgb.mean(-1)>150)&(rgb.max(-1)-rgb.min(-1)<60)
  al&=~(near&light); al=ndimage.binary_opening(al,iterations=1)
  _,idx=ndimage.distance_transform_edt(~al,return_indices=True)
  rgb=rgb[idx[0],idx[1]]
  ramp=lambda m: np.clip((ndimage.gaussian_filter(m.astype(float),1.5)-.5)*4+.5,0,1)
  item=ramp(al); line=ramp(ndimage.distance_transform_edt(~al)<=3)  # fresh even dark outline under the item
  out=item[...,None]*rgb+(1-item[...,None])*np.array(INK); alpha=np.maximum(item,line)
  return Image.fromarray(np.dstack([out,alpha*255]).round().astype(np.uint8))
INK=(45,34,38)
def put(c, im, x, y): c.alpha_composite(im, (int(round(x)), int(round(y))))
def scale(im, s): return im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
def ears(a):
  m=(a[...,3]>128)&(a[...,0]>200)&(a[...,1]>150)&(a[...,0]-a[...,2]<60)
  lab,n=ndimage.label(m)
  return [(s, lab[s]>0) for s in ndimage.find_objects(lab) if (lab[s]>0).sum()>150]
def save(im, name): im.resize((W//2, H//2), Image.LANCZOS).save(f'{OUT}/{name}.png', optimize=True)
for i in range(5):
  c=Image.new('RGBA',(W,H)); put(c, clean(Image.open(f'raw/body-{i}.png')), PX, PY); save(c, f'body-{i}')
for i in range(12):
  a=np.array(Image.open(f'raw/hair-{i}.png')); e=ears(a)
  for s,m in e: a[s][...,3]=np.where(ndimage.binary_dilation(m,iterations=1),0,a[s][...,3])  # cut ears so body skin shows
  eb = HAIR_FIX.get(i, max((s[0].stop for s,_ in e), default=245))
  cx = np.mean([(s[1].start+s[1].stop)/2 for s,_ in e]) if len(e)==2 else a.shape[1]/2
  im=scale(clean(Image.fromarray(a)),HS); c=Image.new('RGBA',(W,H))
  put(c, im, PX+EAR_CX-cx*HS, PY+EAR_BOTTOM-eb*HS); save(c, f'hair-{i}')
for i in range(16):
  im=scale(clean(Image.open(f'raw/top-{i}.png')),TS); c=Image.new('RGBA',(W,H))
  put(c, im, PX+EAR_CX-im.width/2, PY+TOP_Y+TOP_DY.get(i,0)); save(c, f'top-{i}')
for i in range(12):
  im=scale(clean(Image.open(f'raw/bottom-{i}.png')),BS); c=Image.new('RGBA',(W,H))
  put(c, im, PX+EAR_CX-im.width/2, PY+BOT_Y+BOT_DY.get(i,0)); save(c, f'bottom-{i}')
# preview sheet: each top/bottom/hair on body
def outfit(b,bo,t,h):
  c=Image.open(f'{OUT}/body-{b}.png').copy()
  for n in (f'bottom-{bo}',f'top-{t}',f'hair-{h}'): c.alpha_composite(Image.open(f'{OUT}/{n}.png'))
  return c
cols=8; sheet=Image.new('RGBA',((W//2)*cols,(H//2)*2),'white')
for k in range(16):
  sheet.alpha_composite(outfit(k%5,k%12,k,k%12),((k%cols)*(W//2),(k//cols)*(H//2)))
sheet.save('preview.png')
