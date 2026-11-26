# 눈 흰자: 눈마다(왼·오) 가장 큰 덩어리(속눈썹+눈동자) 아래, 양 눈꼬리에서 둥글게 내려가 눈동자 밑까지를 흰색으로 (눈썹은 따로 떨어져 있어서 빠짐)
import sys, numpy as np; from PIL import Image; from scipy import ndimage
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
    ys, xs = np.nonzero(big); y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max(); w = x1 - x0
    Y, X = np.mgrid[:a.shape[0], :a.shape[1]]
    top = np.where(big.any(0), big.argmax(0), a.shape[0])  # 열마다 속눈썹 윗줄 (그 위로는 안 칠함)
    cor = []  # 눈꼬리: 양 끝 1/4 안 열들의 아랫끝 가운데 값(높이)과 그 가장 바깥 열
    for lo, hi in ((x0, x0 + w // 4), (x1 - w // 4, x1)):
      seg = big[:, lo:hi + 1]; cols = np.nonzero(seg.any(0))[0]; bot = np.array([np.nonzero(seg[:, c])[0].max() for c in cols])
      yc = int(np.median(bot)); c = cols[np.argmin(np.abs(bot - yc) + (0 if lo == x0 else -1) * cols * 1e-3)]  # 한 줄만 길게 늘어진 속눈썹은 무시 (가운데 값)
      cor.append((lo + (cols[bot == yc].min() if lo == x0 else cols[bot == yc].max()) if (bot == yc).any() else lo + c, yc))
    (xl, yl), (xr, yr) = cor; t = np.clip((X - xl) / max(1, xr - xl), 0, 1)
    low = yl + (yr - yl) * t + (y1 + .5 - (yl + yr) / 2) * np.sin(np.pi * t)  # 아랫선: 눈꼬리에서 둥글게 내려가 눈동자 밑까지
    white |= ndimage.binary_erosion((Y > top[None, :]) & (Y <= low) & (X >= xl) & (X <= xr), iterations=1)
  al = im[..., 3:] / 255; w = white[..., None]
  rgb = np.where(w, im[..., :3] * al + 255 * (1 - al), im[..., :3]); A = np.where(white, 255, im[..., 3])
  Image.fromarray(np.dstack([rgb, A]).round().clip(0, 255).astype(np.uint8)).save(f'{OUT}eye-{k}.png', optimize=True)
