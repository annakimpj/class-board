# 신발 크기 줄이기: 가로 84%(가운데 x=130 기준)·세로 90%(바닥 y=385 기준). 긴 바지 밑으로 옆이 안 튀어나오게
import sys, numpy as np; from PIL import Image
SX, SY, CX, BY = .84, .90, 130, 385
if sys.argv[1:] != ['ankle']:
 for k in range(1, 9):
  im = Image.open(f'shoes-{k}.png').convert('RGBA')
  # 출력 (x, y) ← 원본 ((x-CX)/SX+CX, (y-BY)/SY+BY)
  out = im.transform(im.size, Image.AFFINE, (1 / SX, 0, CX - CX / SX, 0, 1 / SY, BY - BY / SY), resample=Image.BICUBIC)
  out.save(f'shoes-{k}.png', optimize=True)
# 2차(python shoesize.py ankle): 발목 쪽(윗부분)만 바깥으로 넓혀 다리 선과 이어지게 (가운데 x=130 기준). 두 번 돌림: 112%(350→370), 115%(350→372)
import sys
if sys.argv[1:] == ['ankle']:
  for k in range(1, 9):
    a = np.array(Image.open(f'shoes-{k}.png').convert('RGBA')).astype(float); o = np.zeros_like(a); xs = np.arange(a.shape[1])
    for y in range(a.shape[0]):
      f = 1 + .15 * np.clip((372 - y) / 22, 0, 1); src = (xs - CX) / f + CX
      for c in range(4): o[y, :, c] = np.interp(src, xs, a[y, :, c], left=0, right=0)
    Image.fromarray(o.round().clip(0, 255).astype(np.uint8)).save(f'shoes-{k}.png', optimize=True)
