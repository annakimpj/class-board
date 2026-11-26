# 선생님이 그린 머리·옷·신발 (raw_user/*-2x.png, 516×772) → hair-N.png(절반) + hair-N-g.png(머리색 칠하기용 회색)
# 흰색으로 칠해진 빈 곳(이마·귀 구멍 둘레)은 투명하게
import numpy as np; from PIL import Image
for k in range(12, 24):
  a = np.array(Image.open(f'raw_user/hair-{k}-2x.png').convert('RGBA')).astype(float)
  w = np.clip((a[..., :3].min(-1) - 215) / 30, 0, 1); a[..., 3] *= 1 - w  # 흰색일수록 투명
  im = Image.fromarray(a.round().astype(np.uint8)).resize((258, 386), Image.LANCZOS); im.save(f'hair-{k}.png', optimize=True)
  b = np.array(im).astype(float) / 255; l = b[..., :3] @ [.299, .587, .114]; g = .12 + np.clip((l - .15) / .4, 0, 1) ** .6 * .88
  Image.fromarray((np.dstack([g, g, g, b[..., 3]]) * 255).round().astype(np.uint8)).save(f'hair-{k}-g.png', optimize=True)
# 옷·신발: 흰 옷이 있어서 흰색은 그대로 두고 절반으로만
import glob, os
for f in glob.glob('raw_user/*-2x.png'):
  n = os.path.basename(f)[:-7]
  if not n.startswith('hair-'): Image.open(f).convert('RGBA').resize((258, 386), Image.LANCZOS).save(f'{n}.png', optimize=True)
