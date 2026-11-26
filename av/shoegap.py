# 신발 두 짝 사이를 띄움: 가운데(x=129)에서 갈라 안쪽을 2px 깎고 양쪽으로 2px씩 벌린 뒤, 짝마다 테두리를 다시 그림 (outline.py)
import sys, numpy as np; from PIL import Image; from outline import uniform
CUT, TRIM, MOVE = 129, 2, 2
for k in range(1, 9):
  f = f'shoes-{k}.png'; im = np.array(Image.open(f).convert('RGBA').resize((516, 772), Image.LANCZOS)).astype(float)
  H, W = im.shape[:2]; out = np.zeros_like(im); xs = np.arange(W)
  for side in (-1, 1):
    keep = xs < (CUT - TRIM) * 2 if side < 0 else xs >= (CUT + TRIM) * 2
    a = (im[..., 3] > 128) & keep[None, :]
    a = np.roll(a, side * MOVE * 2, 1); rgb = np.roll(im[..., :3], side * MOVE * 2, 1)
    col, al = uniform(a, rgb, 2)
    m = al[..., None]; out[..., :3] = out[..., :3] * (1 - m) + col * m; out[..., 3] = np.maximum(out[..., 3], al * 255)
  Image.fromarray(out.round().clip(0, 255).astype(np.uint8)).resize((258, 386), Image.LANCZOS).save(f, optimize=True)
# 2차(따로 한 번 돌림): 보는 쪽 오른쪽 짝이 다리보다 3px 안쪽이라 x>=129를 오른쪽으로 3px 옮김
#   a = np.array(Image.open(f)); o = a.copy(); o[:, 129:] = 0; o[:, 132:] = a[:, 129:-3]
