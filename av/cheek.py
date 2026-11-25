# 볼터치 그림 만들기: cheek-N.png = 모양(알파만, 색은 avatar.js가 칠함), cheek-N-f.png = 주근깨(색 그대로)
from PIL import Image, ImageDraw, ImageFilter
W, H, S = 258, 386, 4                      # 4배로 그리고 줄여서 가장자리 부드럽게
LC, RC, CY = 92, 166, 194                  # 볼 가운데 (눈 아래 바깥쪽)
def new(): return Image.new("L", (W*S, H*S), 0)
def done(m, blur=0):
  if blur: m = m.filter(ImageFilter.GaussianBlur(blur*S))
  m = m.resize((W, H), Image.LANCZOS); im = Image.new("RGBA", (W, H), (255, 255, 255, 0)); im.putalpha(m); return im
def ell(d, cx, cy, rx, ry, v): d.ellipse([(cx-rx)*S, (cy-ry)*S, (cx+rx)*S, (cy+ry)*S], fill=v)
def round_cheeks(rx=12, ry=7.5, v=150, blur=3):
  m = new(); d = ImageDraw.Draw(m)
  for cx in (LC, RC): ell(d, cx, CY, rx, ry, v)
  return done(m, blur)
def nose_band():   # 볼에서 콧잔등을 지나 반대쪽 볼까지 이어진 띠
  m = new(); d = ImageDraw.Draw(m)
  for cx in (LC, RC): ell(d, cx, CY-1, 13, 7, 140)
  d.rounded_rectangle([LC*S, (CY-6)*S, RC*S, (CY+2)*S], radius=4*S, fill=110)
  return done(m, 3)
def hatch():       # 빗금 볼터치 ///
  m = new(); d = ImageDraw.Draw(m)
  for cx in (LC, RC):
    ell(d, cx, CY, 11, 6, 70)
    for dx in (-6, 0, 6): d.line([((cx+dx+3)*S, (CY-4)*S), ((cx+dx-3)*S, (CY+4)*S)], fill=255, width=int(1.6*S))
  return done(m, .4)
def dots():        # 작은 동그라미
  m = new(); d = ImageDraw.Draw(m)
  for cx in (LC, RC): ell(d, cx, CY+1, 5, 5, 190)
  return done(m, 1)
def freckles(pts):
  im = Image.new("RGBA", (W*S, H*S)); d = ImageDraw.Draw(im)
  for x, y in pts: d.ellipse([(x-1.1)*S, (y-1.1)*S, (x+1.1)*S, (y+1.1)*S], fill=(150, 95, 75, 200))
  return im.resize((W, H), Image.LANCZOS)
FN = [(119, 191), (124, 194), (134, 194), (139, 191), (129, 189)]  # 콧잔등 주근깨
FC = [(85, 191), (91, 195), (97, 191), (88, 198), (161, 191), (167, 195), (173, 191), (170, 198)]  # 볼 주근깨
shapes = [done(new()), round_cheeks(), nose_band(), round_cheeks(), hatch(), dots(), nose_band(), round_cheeks(15, 9, 120, 4)]
fr = {2: FN + FC, 3: FC}
for i, im in enumerate(shapes):
  im.save(f"cheek-{i}.png", optimize=True)
  if i in fr: freckles(fr[i]).save(f"cheek-{i}-f.png", optimize=True)
