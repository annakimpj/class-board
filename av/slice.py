from PIL import Image
import numpy as np
from scipy import ndimage
SRC=r'C:/Users/user/AppData/Local/Temp/claude/97e6b7a1001ffbb2/58a05c23-d38c-4916-869c-3afb6d3f0eca/images/'
for f,name in [('1.webp','top'),('2.webp','hair'),('3.webp','bottom'),('4.webp','body')]:
  a=np.array(Image.open(SRC+f).convert('RGBA'))
  bg=(a[...,3]<20)|(a[...,:3].min(-1)>235)
  m=ndimage.binary_fill_holes(ndimage.binary_closing(~bg,iterations=3))
  lab,n=ndimage.label(m)
  objs=[(i+1,s) for i,s in enumerate(ndimage.find_objects(lab)) if (s[0].stop-s[0].start)*(s[1].stop-s[1].start)>5000]
  objs.sort(key=lambda o:(round(o[1][0].start/200),o[1][1].start))
  for k,(li,s) in enumerate(objs):
    c=a[s].copy()
    if f=='1.webp': c[...,3]=np.where(lab[s]==li,255,0)  # RGB sheet: alpha = filled silhouette
    else: c[...,3]=np.where(lab[s]==li,c[...,3],0)
    Image.fromarray(c).save(f'raw/{name}-{k}.png')
