# hair-N.png -> hair-N-g.png: light gray hair (dark outline kept) for CSS color multiply
from PIL import Image
import numpy as np
for i in range(12):
  a = np.array(Image.open(f'hair-{i}.png')).astype(float) / 255
  l = a[..., :3] @ [.299, .587, .114]
  t = np.clip((l - .15) / .4, 0, 1) ** .6
  g = .12 + t * .88
  Image.fromarray((np.dstack([g, g, g, a[..., 3]]) * 255).round().astype(np.uint8)).save(f'hair-{i}-g.png', optimize=True)
