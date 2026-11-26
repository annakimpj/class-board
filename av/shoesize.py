# 신발 크기 줄이기: 가로 84%(가운데 x=130 기준)·세로 90%(바닥 y=385 기준). 긴 바지 밑으로 옆이 안 튀어나오게
import numpy as np; from PIL import Image
SX, SY, CX, BY = .84, .90, 130, 385
for k in range(1, 9):
  im = Image.open(f'shoes-{k}.png').convert('RGBA')
  # 출력 (x, y) ← 원본 ((x-CX)/SX+CX, (y-BY)/SY+BY)
  out = im.transform(im.size, Image.AFFINE, (1 / SX, 0, CX - CX / SX, 0, 1 / SY, BY - BY / SY), resample=Image.BICUBIC)
  out.save(f'shoes-{k}.png', optimize=True)
