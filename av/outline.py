# 옷 테두리 통일: 시트마다 다른 원래 바깥 선을 벗기고, 같은 굵기의 검정 선을 새로 그림 (tops.py, bottoms.py가 씀)
import numpy as np; from scipy import ndimage
INK=np.array([45,34,38.])
def ramp(m,s=1.0): return np.clip((ndimage.gaussian_filter(m.astype(float),s)-.5)*3+.5,0,1)
def uniform(a, rgb, S, R=2.0, D=2.5):
  # a: 옷 자리(bool), rgb: 색. 2배 캔버스. R: 새 선 굵기, D: 벗길 원래 선 두께 (둘 다 출력 px)
  din=ndimage.distance_transform_edt(a)
  strip=a&(rgb.max(-1)<120)&(din<=D*S)          # 가장자리의 어두운 픽셀 = 원래 선
  inner=ndimage.binary_opening(a&~strip,iterations=1)
  sil=ndimage.distance_transform_edt(~inner)<=R*S  # 안쪽 + 고른 굵기 선
  _,idx=ndimage.distance_transform_edt(~inner,return_indices=True); col=rgb[idx[0],idx[1]]
  body=ramp(inner)[...,None]
  return body*col+(1-body)*INK, ramp(sil)
