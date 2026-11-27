# 선생님이 그린 머리·옷·신발 (raw_user/*-2x.png, 516×772) → hair-N.png(절반) + hair-N-g.png(머리색 칠하기용 회색)
# 흰색으로 칠해진 빈 곳(이마·귀 구멍 둘레)은 투명하게
import os, numpy as np; from PIL import Image; from scipy import ndimage; from outline import uniform
for k in sorted(int(f[5:-7]) for f in os.listdir('raw_user') if f.startswith('hair-') and f.endswith('-2x.png')):  # raw_user/hair-N-2x.png 모두
  a = np.array(Image.open(f'raw_user/hair-{k}-2x.png').convert('RGBA').crop((0, 0, 516, 772))).astype(float)  # 아래 여백이 있는 기본형(516×832)에 그려도 위 772만
  w = np.clip((a[..., :3].min(-1) - 215) / 30, 0, 1); a[..., 3] *= 1 - w  # 흰색일수록 투명
  im = Image.fromarray(a.round().astype(np.uint8)).resize((258, 386), Image.LANCZOS); im.save(f'hair-{k}.png', optimize=True)
  b = np.array(im).astype(float) / 255; l = b[..., :3] @ [.299, .587, .114]; g = .12 + np.clip((l - .15) / .4, 0, 1) ** .6 * .88
  Image.fromarray((np.dstack([g, g, g, b[..., 3]]) * 255).round().astype(np.uint8)).save(f'hair-{k}-g.png', optimize=True)
# 옷·신발: 흰 옷이 있어서 테두리 바깥(그림 밖과 이어진) 흰색만 지우고 절반으로
import glob, os
for f in glob.glob('raw_user/*-2x.png'):
  n = os.path.basename(f)[:-7]
  if n.startswith('hair-'): continue
  a = np.array(Image.open(f).convert('RGBA').crop((0, 0, 516, 772))).astype(float)  # shortcut: 772 아래(신발을 더 내려 그린 것)는 잘림, 신발을 그렇게 그려 오면 신발만 따로 키워 그리기
  wh = (a[..., 3] < 30) | (a[..., :3].min(-1) > 200)  # 빈 곳 또는 흰색
  G = ~wh; ys = np.nonzero(G.any(1))[0]
  if len(ys):  # 목 트임으로 바깥과 이어진 흰 옷 안쪽(가운 속 셔츠 등)이 지워지지 않게: 옷 맨 위 1/5은 줄마다 양끝 사이를 막음
    for y in range(ys[0], ys[0] + (ys[-1] - ys[0]) // 5):
      xs = np.nonzero(G[y])[0]
      if len(xs): wh[y, xs[0]:xs[-1] + 1] = False
  lab, _ = ndimage.label(wh); out = np.isin(lab, np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) & (lab > 0)  # 그림 가장자리와 이어진 것 = 테두리 바깥
  if len(ys):  # 목 구멍: 열마다 옷 맨 위에서 아래로, 깃 선(흰색 아닌 곳)을 만날 때까지의 흰색
    W0 = (a[..., 3] < 30) | (a[..., :3].min(-1) > 200)
    for x in range(a.shape[1]):
      y = ys[0]
      while y < ys[-1] and W0[y, x]: out[y, x] = True; y += 1
  for _ in range(2): out |= ndimage.binary_dilation(out) & (a[..., :3].min(-1) > 170) & (a[..., 3] > 0)  # 바깥 흰색에 붙은 옅은 테두리 번짐도
  a[out, 3] = 0
  if n.startswith('top-'): # 옷: 테두리를 매끈하고 같은 굵기로 다시 그림 (outline.py, 다른 옷과 같게)
    col, al = uniform(a[..., 3] > 128, a[..., :3], 2); a = np.dstack([col, al * 255])
  Image.fromarray(a.round().clip(0, 255).astype(np.uint8)).resize((258, 386), Image.LANCZOS).save(f'{n}.png', optimize=True)
# 몸(raw_user/base-2x.png): 흰 배경 지우고 테두리 4px로 고르게 → base-0, 피부색 4개 더(base-1~4: 예전 피부색 비율로), 귀만 떼어 ear-0~4 (귀 보이는 머리 위에 그림)
SKIN = [[248, 225, 221], [246, 210, 198], [229, 186, 169], [201, 152, 139], [143, 103, 96]]  # 피부 평균색 (예전 base-0~4에서 잼)
if os.path.exists('raw_user/base-2x.png'):
  a = np.array(Image.open('raw_user/base-2x.png').convert('RGBA').crop((0, 0, 516, 772))).astype(float)
  wh = (a[..., 3] < 30) | (a[..., :3].min(-1) > 200)
  lab, _ = ndimage.label(wh); out = np.isin(lab, np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) & (lab > 0)
  for _ in range(2): out |= ndimage.binary_dilation(out) & (a[..., :3].min(-1) > 170) & (a[..., 3] > 0)
  a[out, 3] = 0
  col, al = uniform(a[..., 3] > 128, a[..., :3], 2, R=4.0, D=4.5)  # 몸 테두리는 옷(3px)보다 조금 굵게 4px
  b0 = np.array(Image.fromarray(np.dstack([col, al * 255]).round().clip(0, 255).astype(np.uint8)).resize((258, 386), Image.LANCZOS)).astype(float)
  rgb = b0[..., :3]; pale = (b0[..., 3] > 0) & (rgb.min(-1) > 175) & (rgb[..., 0] - rgb[..., 2] < 14)  # 흰·회색
  lab, n = ndimage.label(pale); big = np.isin(lab, 1 + np.nonzero(ndimage.sum(pale, lab, range(1, n + 1)) > 60)[0])
  under = ndimage.binary_dilation(big, iterations=1) & (b0[..., 3] > 0) & (rgb.min(-1) > 120)  # 속옷(큰 흰 덩어리)만 그대로
  skin = (b0[..., 3] > 0) & ~under  # 나머지(피부·테두리 번짐·볼)는 피부색 비율로
  # 귀: 머리를 원으로 맞춰(귀 위쪽 줄들의 폭으로) 원 안쪽은 빼고, 귀 높이의 양옆만
  A = b0[..., 3] > 128; ys = np.array([y for y in range(66, 140) if A[y].any()]); w = np.array([np.ptp(np.nonzero(A[y])[0]) / 2 + .5 for y in ys])
  M = np.c_[2 * ys, np.ones_like(ys)]; (cy, c0), *_ = np.linalg.lstsq(M, w ** 2 + ys ** 2, rcond=None); R = np.sqrt(c0 + cy ** 2); cx = 128.5
  Y, X = np.mgrid[:386, :258]; dd = np.hypot(X - cx, Y - cy); side = (X < 75) | (X > 183)
  out = A & (dd > R + 2) & side & (Y > 120) & (Y < 220)  # 머리 원 밖으로 확실히 나온 곳 = 귀
  rows = np.nonzero(out.any(1))[0]; ear = A & (dd > R - 3) & side & (Y >= rows.min() - 1) & (Y <= rows.max() + 1)  # 귀 높이 안에서 머리 테두리에 붙은 데까지
  ear = ndimage.binary_dilation(ear, iterations=1) & (b0[..., 3] > 0)
  for k, sc in enumerate(SKIN):
    bk = b0.copy(); f = np.array(sc) / np.array(SKIN[0]); bk[skin, :3] = (rgb[skin] * f).clip(0, 255)
    Image.fromarray(bk.round().astype(np.uint8)).save(f'base-{k}.png', optimize=True)
    ek = bk.copy(); ek[~ear, 3] = 0; Image.fromarray(ek.round().astype(np.uint8)).save(f'ear-{k}.png', optimize=True)
# 모자·헬멧(raw_user/hat-N-2x.png → hair-N.png, 헤어 칸): 흰 털·이빨이 있어서 그림 밖과 이어진 흰색 + 얼굴 구멍(가운데 가장 큰 흰 덩어리)만 지우고 테두리 정리. 머리색은 안 칠함
for f in glob.glob('raw_user/hat-*-2x.png'):
  k = int(os.path.basename(f)[4:-7])
  a = np.array(Image.open(f).convert('RGBA').crop((0, 0, 516, 772))).astype(float)
  wh = (a[..., 3] < 30) | (a[..., :3].min(-1) > 225)
  lab, n = ndimage.label(wh); edge = np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])
  inner = [i for i in range(1, n + 1) if i not in edge]; face = max(inner, key=lambda i: (lab == i).sum()) if inner else -1
  out = np.isin(lab, edge) & (lab > 0) | (lab == face)
  for _ in range(2): out |= ndimage.binary_dilation(out) & (a[..., :3].min(-1) > 170) & (a[..., 3] > 0)
  a[out, 3] = 0
  col, al = uniform(a[..., 3] > 128, a[..., :3], 2); a = np.dstack([col, al * 255])
  Image.fromarray(a.round().clip(0, 255).astype(np.uint8)).resize((258, 386), Image.LANCZOS).save(f'hair-{k}.png', optimize=True)
# 눈·입(raw_user/eye-N-2x.png, mouth-N-2x.png): 그림 밖과 이어진 흰색만 지우고(눈 속 반짝이는 그대로) 절반으로. 가는 선이라 테두리는 안 다시 그림
for f in glob.glob('raw_user/eye-*-2x.png') + glob.glob('raw_user/mouth-*-2x.png'):
  n = os.path.basename(f)[:-7]
  a = np.array(Image.open(f).convert('RGBA').crop((0, 0, 516, 772))).astype(float)
  wh = (a[..., 3] < 30) | (a[..., :3].min(-1) > 200)
  lab, _ = ndimage.label(wh); out = np.isin(lab, np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) & (lab > 0)
  a[..., 3] *= np.clip((255 - a[..., :3].min(-1)) / 40, 0, 1)  # 옅은 흰 번짐은 흰 만큼 투명하게
  a[out, 3] = 0
  Image.fromarray(a.round().clip(0, 255).astype(np.uint8)).resize((258, 386), Image.LANCZOS).save(f'{n}.png', optimize=True)
