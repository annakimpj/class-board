# 신발 시트(raw_new/shoes1.webp, 저장소에 없음) → av/shoes-1~8.png (shoes-0은 맨발, 그림 없음). 켤레를 가운데 빈 곳에서 갈라 왼발·오른발에 한 짝씩
from PIL import Image; import numpy as np; from scipy import ndimage
import sys
sys.path.insert(0, r'C:/Users/user/Documents/GitHub/geulgam/av'); from outline import uniform
OUT = sys.argv[1] if len(sys.argv) > 1 else './'
BOX = [(18,329,369,470),(399,322,743,470),(769,336,1132,470),(1158,322,1506,470),(16,600,372,734),(397,601,744,734),(771,592,1127,735),(1149,601,1504,734)]
W, H, S = 516, 772, 2          # 2배 캔버스
FEET = (108, 150)              # 두 다리 가운데 x (출력 px, base-N.png에서 잼)
SOLE = 381                     # 신발 바닥 y (출력 px). 테두리까지 그림 안에 들어오게
SHOE_W = 44                    # 한 짝 폭 (출력 px)
sheet = np.array(Image.open('raw_new/shoes1.webp').convert('RGB')).astype(float)
for k, (x0, y0, x1, y1) in enumerate(BOX):
  c = np.pad(sheet, ((12, 12), (12, 12), (0, 0)), constant_values=255)[y0+2:y1+23, x0+2:x1+23]
  m = ndimage.binary_fill_holes(ndimage.binary_closing(c.min(-1) < 225, iterations=2))
  lab, n = ndimage.label(m); sz = ndimage.sum(m, lab, range(1, n+1)); m = np.isin(lab, 1 + np.where(sz > 400)[0])
  cols = m.sum(0); mid = m.shape[1] // 2; w = m.shape[1] // 6
  cut = mid - w + int(np.argmin(cols[mid-w:mid+w]))  # 두 짝 사이 가장 얇은 곳
  cv = np.zeros((H, W, 4))
  for half, (a, b) in enumerate([(0, cut), (cut, m.shape[1])]):
    mm = m[:, a:b].copy(); cc = c[:, a:b]
    lab, n = ndimage.label(mm); sz = ndimage.sum(mm, lab, range(1, n+1)); mm = lab == 1 + int(np.argmax(sz))  # 큰 덩어리 = 이 짝
    ys, xs = np.where(mm); mm = mm[ys.min():ys.max()+1, xs.min():xs.max()+1]; cc = cc[ys.min():ys.max()+1, xs.min():xs.max()+1]
    sc = SHOE_W * S / mm.shape[1]
    im = Image.fromarray(np.dstack([cc, mm * 255.]).astype(np.uint8)).resize((round(mm.shape[1]*sc), round(mm.shape[0]*sc)), Image.LANCZOS)
    ox, oy = round(FEET[half]*S - im.width/2), round(SOLE*S - im.height)
    p = np.array(im).astype(float); reg = cv[oy:oy+im.height, ox:ox+im.width]
    al = p[..., 3:] / 255; reg[:] = reg * (1 - al) + p * al
  a = cv[..., 3] > 128; out, alpha = uniform(a, cv[..., :3], S)  # 고른 검정 테두리 (outline.py)
  Image.fromarray(np.dstack([out, alpha*255]).round().clip(0, 255).astype(np.uint8)).resize((W//2, H//2), Image.LANCZOS).save(f'{OUT}shoes-{k+1}.png', optimize=True)
