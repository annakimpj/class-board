# 눈 흰자: 눈마다(왼·오) 가장 큰 덩어리(속눈썹+눈동자)를 볼록하게 감싼 안쪽 빈 곳을 흰색으로 (눈썹은 따로 떨어져 있어서 빠짐)
import sys, numpy as np; from PIL import Image; from scipy import ndimage
from scipy.spatial import ConvexHull; from PIL import ImageDraw
def convex_hull_image(m):
  ys, xs = np.nonzero(m); p = np.c_[xs, ys]; h = ConvexHull(p); c = Image.new('L', m.shape[::-1]); ImageDraw.Draw(c).polygon([tuple(map(int, p[i])) for i in h.vertices], fill=1); return np.array(c) > 0
SRC = sys.argv[1] if len(sys.argv) > 1 else './'; OUT = sys.argv[2] if len(sys.argv) > 2 else './'  # SRC: 흰자 없는 원본 눈 그림 폴더
for k in [k for k in range(16) if k not in (3, 15)]:  # 감은 눈(^^)·점 눈은 흰자 없음
  im = np.array(Image.open(f'{SRC}eye-{k}.png').convert('RGBA')).astype(float); a = im[..., 3] > 90
  white = np.zeros(a.shape, bool)
  for half in (slice(0, 129),) if k == 4 else (slice(0, 129), slice(129, None)):  # 윙크: 감은 오른쪽 눈은 빼고
    m = np.zeros_like(a); m[:, half] = a[:, half]
    lab, n = ndimage.label(m)
    if not n: continue
    sz = ndimage.sum(m, lab, range(1, n + 1)); big = lab == 1 + int(np.argmax(sz))
    if k == 10:  # 놀란 눈: 윗선(호)과 눈동자가 떨어져 있음 → 눈썹(맨 위 덩어리)만 빼고 다 합침
      tops = ndimage.minimum(np.indices(a.shape)[0], lab, range(1, n + 1)); big = (lab > 0) & (lab != 1 + int(np.argmin(tops)))
    hull = convex_hull_image(big); ys, xs = np.nonzero(big); y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    Y, X = np.mgrid[:a.shape[0], :a.shape[1]]; cy, cx, ry, rx = (y0 + y1) / 2, (x0 + x1) / 2, (y1 - y0) / 2 + .5, (x1 - x0) / 2 + .5
    top = np.where(big.any(0), big.argmax(0), a.shape[0])  # 열마다 속눈썹 윗줄 (그 위로는 안 칠함)
    oval = (((Y - cy) / ry) ** 2 + ((X - cx) / rx) ** 2 <= 1) & (Y > top[None, :])
    w = x1 - x0; cx_ = []  # 눈꼬리: 양 끝 1/4 안에서 가장 아래 점의 x. 흰자는 그 사이만
    for lo, hi in ((x0, x0 + w // 4), (x1 - w // 4, x1)):
      yy, xx = np.nonzero(big[:, lo:hi + 1]); cx_.append(lo + xx[np.argmax(yy)])
    white |= ndimage.binary_erosion(hull | oval, iterations=1) & (X >= min(cx_)) & (X <= max(cx_))  # 아래가 일자 대신 둥글게 (타원), 눈꼬리 밖은 안 칠함
  al = im[..., 3:] / 255; w = white[..., None]
  rgb = np.where(w, im[..., :3] * al + 255 * (1 - al), im[..., :3]); A = np.where(white, 255, im[..., 3])
  Image.fromarray(np.dstack([rgb, A]).round().clip(0, 255).astype(np.uint8)).save(f'{OUT}eye-{k}.png', optimize=True)
