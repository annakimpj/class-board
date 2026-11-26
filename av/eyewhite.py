# 눈 흰자: 눈마다(왼·오) 가장 큰 덩어리(속눈썹+눈동자)를 볼록하게 감싼 안쪽 빈 곳을 흰색으로 (눈썹은 따로 떨어져 있어서 빠짐)
import sys, numpy as np; from PIL import Image; from scipy import ndimage
from scipy.spatial import ConvexHull; from PIL import ImageDraw
def convex_hull_image(m):
  ys, xs = np.nonzero(m); p = np.c_[xs, ys]; h = ConvexHull(p); c = Image.new('L', m.shape[::-1]); ImageDraw.Draw(c).polygon([tuple(map(int, p[i])) for i in h.vertices], fill=1); return np.array(c) > 0
SRC = sys.argv[1] if len(sys.argv) > 1 else './'; OUT = sys.argv[2] if len(sys.argv) > 2 else './'
for k in [k for k in range(16) if k not in (3, 5, 15)]:  # 감은 눈(^^)·점 눈은 흰자 없음
  im = np.array(Image.open(f'{SRC}eye-{k}.png').convert('RGBA')).astype(float); a = im[..., 3] > 90
  white = np.zeros(a.shape, bool)
  for half in (slice(0, 129), slice(129, None)):
    m = np.zeros_like(a); m[:, half] = a[:, half]
    lab, n = ndimage.label(m)
    if not n: continue
    sz = ndimage.sum(m, lab, range(1, n + 1)); big = lab == 1 + int(np.argmax(sz))
    white |= ndimage.binary_erosion(convex_hull_image(big), iterations=1)
  al = im[..., 3:] / 255; w = white[..., None]
  rgb = np.where(w, im[..., :3] * al + 255 * (1 - al), im[..., :3]); A = np.where(white, 255, im[..., 3])
  Image.fromarray(np.dstack([rgb, A]).round().clip(0, 255).astype(np.uint8)).save(f'{OUT}eye-{k}.png', optimize=True)
