// 우리반 보드 · 아바타 (교사 보드 index.html과 학생 화면 student.html이 같이 씀)
// 그림은 av/ 폴더의 PNG. 모든 그림이 같은 크기(258×386)라 그대로 겹치면 제자리 (av/comp.py가 원본 그림에서 잘라 맞춤)
// 겹치는 순서: 몸(피부, 얼굴 없음) → 볼터치 → 눈 → 입 → 신발(나중에) → 하의 → 상의 → 머리
const AV_SKIN = [["#fff0f1"], ["#ffddd7"], ["#efc7b8"], ["#cea095"], ["#906a68"]]; // 몸 그림 av/base-0~4.png 색 (고르는 동그라미)
// 머리색: 0은 그림 원래 색. 나머지는 회색 머리(av/hair-N-g.png, av/hairgray.py로 만듦)에 색을 곱해서 칠함
const AV_HAIR = [["#6b4a3f"], ["#3a3a46"], ["#ffe066"], ["#ffb347"], ["#ff6b6b"], ["#ff9ccf"], ["#c39bff"], ["#6fa8ff"], ["#7fe3ff"], ["#6ee7b7"], ["#9be36b"], ["#eef1f6"]];
// 볼색: 볼터치 그림(av/cheek-N.png, av/cheek.py로 만듦)은 모양만 있어서 이 색을 곱해서 칠함. 주근깨(av/cheek-N-f.png)는 그림 색 그대로
const AV_CHEEK = [["#ff8fa3"], ["#ffab91"], ["#ff5c8a"], ["#ff6b6b"], ["#ffb36b"], ["#c9a0ff"]];
const AV_FRECK = [2, 3]; // 주근깨가 같이 있는 볼터치 번호
const AV_NAMES = {
  hair: ["부스스 짧은 머리", "레이어드 단발", "일자 단발", "웨이브 단발", "짧은 스포츠머리", "뾰족 머리", "뽀글 머리", "똥머리", "긴 생머리", "양 똥머리", "양 갈래 땋은 머리", "긴 웨이브"],
  top: ["세일러 블라우스", "크림 후드티", "검정 재킷", "분홍 가디건", "고양이 후드티", "흰 셔츠", "야구 점퍼", "곰돌이 니트", "검정 프릴 블라우스", "줄무늬 티", "하얀 패딩", "빨간 망토", "카키 야상", "멜빵 원피스", "검정 후드티", "레이스 블라우스",
    "경찰 제복", "소방관 점퍼", "빨간 로봇 갑옷", "군복 재킷", "공룡 후드티", "우주인 점퍼", "축구 유니폼", "레이싱 재킷", "해적 조끼", "검정 도복", "가죽 재킷", "낙서 후드티",
    "리본 세일러 티", "분홍 블레이저", "공주 상의", "보라 오프숄더", "검정 교복 가디건", "민트 퍼프 블라우스", "보라 별 조끼", "산호 오프숄더", "눈꽃 블라우스", "딸기 멜빵 블라우스", "무지개 리본 조끼", "크림 레이스 가디건"],
  eye: ["기본 눈", "날렵한 눈", "졸린 눈", "웃는 눈", "윙크", "반짝 눈", "울먹 눈", "화난 눈", "옆 보는 눈", "걱정 눈", "놀란 눈", "시큰둥 눈", "하트 눈", "빙글빙글 눈", "속눈썹 눈", "점 눈"],
  cheek: ["볼터치 없음", "볼 정중앙", "콧잔등 + 주근깨", "볼 정중앙 + 주근깨", "빗금 볼터치", "작은 동그라미", "콧잔등", "크게 발그레"],
  mouth: ["미소", "활짝 웃는 입", "고양이 입", "작은 입", "시무룩 입", "삐뚤 입", "씩 웃는 입", "메롱", "이 보이게 웃기", "놀란 입", "뽀뽀 입", "일자 입", "송곳니 웃음", "울먹 입", "크게 웃는 입", "쪽 입"],
  bottom: ["하늘 주름치마", "검정 주름치마", "베이지 반바지", "청반바지", "검정 카고 바지", "회색 운동복 바지", "남색 트레이닝 바지", "프릴 치마", "분홍 체크 치마", "카키 반바지", "체인 치마", "체크 바지",
    "연청 와이드 바지", "검정 슬랙스", "베이지 플리츠 롱스커트", "데님 롱스커트", "카키 카고 바지", "크림 골지 바지", "남색 트레이닝 긴바지", "꽃무늬 캉캉 롱스커트", "갈색 코듀로이 바지", "회색 플리츠 롱스커트", "진청 부츠컷 바지", "체크 와이드 바지",
    "세일러 주름치마", "분홍 프릴 치마", "노랑 공주 치마", "보라 별 치마", "분홍 체크 체인 치마", "하늘 진주 롱스커트", "꽃잎 치마", "빨강 리본 치마", "크림 리본 치마", "무지개 프릴 치마", "보라 달 롱스커트", "하얀 프릴 반바지",
    "세일러 롱스커트", "분홍 프릴 롱스커트", "노랑 공주 롱스커트", "보라 별 롱스커트", "분홍 체크 롱스커트", "하늘 진주 드레스 치마", "꽃잎 롱스커트", "빨강 리본 롱스커트", "크림 리본 롱스커트", "무지개 프릴 롱스커트", "보라 달 드레스 치마", "하얀 프릴 롱스커트"],
};
const AV_PRICE = { // 0이면 무료 (기본으로 입는 것)
  hair: [0, 6, 6, 7, 5, 7, 8, 8, 0, 9, 9, 8],
  top: [8, 7, 9, 7, 9, 0, 10, 8, 9, 0, 9, 10, 9, 9, 8, 10, 11, 11, 12, 10, 11, 12, 9, 11, 11, 10, 10, 10, 9, 10, 11, 10, 10, 9, 11, 10, 11, 10, 11, 9],
  eye: Array(16).fill(0), mouth: Array(16).fill(0), cheek: Array(8).fill(0), // 눈·입·볼터치는 모두 무료
  bottom: [6, 6, 0, 0, 7, 6, 7, 8, 7, 0, 8, 7, 8, 8, 8, 8, 8, 7, 7, 9, 8, 8, 8, 8, 8, 10, 10, 9, 9, 11, 10, 9, 9, 10, 11, 9, 10, 11, 11, 10, 10, 12, 11, 11, 10, 11, 12, 10],
};
// 뺀 물건 (손이 가려지거나 소매가 팔 방향과 안 맞음). 그림 파일도 지움. 다시 그리면 같은 번호로 살림
const AV_GONE = new Set([17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 35, 36, 37, 39].map(i => `top-${i}`));
const AV_ITEMS = Object.entries(AV_NAMES).flatMap(([slot, names]) => names.map((name, i) => ({ id: `${slot}-${i}`, slot, name, price: AV_PRICE[slot][i], img: `av/${slot}-${i}.png` }))).filter(it => !AV_GONE.has(it.id));
const AV_REQ = { eye: "eye-0", mouth: "mouth-0", cheek: "cheek-1", hair: "hair-0", top: "top-5", bottom: "bottom-9" }; // 기본 옷 (흰 셔츠·카키 반바지). 이 칸들은 벗을 수 없어 늘 입고 있음
const AV_ACC = []; // 장신구 칸 (아직 없음)
const AV_TABS = [["eye", "눈"], ["mouth", "입"], ["cheek", "볼터치"], ["hair", "헤어"], ["top", "상의"], ["bottom", "하의"]]; // 신발은 그림이 생기면 추가
// 단위에 맞춘 글: "3 으쓱이 모자라요", "3으쓱으로 바꾸기" (이/가, 으로/로)
const avBat = w => { const c = w.charCodeAt(w.length - 1) - 0xac00; return c >= 0 && c < 11172 ? c % 28 : 0; }; // 받침 (0 없음, 8 ㄹ)
const avShort = (n, unit) => `${n} ${unit}${avBat(unit) ? "이" : "가"} 모자라요`;
const avPay = (n, unit) => `${n}${unit}${[0, 8].includes(avBat(unit)) ? "로" : "으로"} 바꾸기`;
const avItem = id => AV_ITEMS.find(x => x.id === id);
// 입은 것 중 지금 있는 물건만 (예전 픽셀 그림 물건 id는 버리고 기본으로)
const avWear = (wear = {}) => ({ ...AV_REQ, ...Object.fromEntries(Object.entries(wear).filter(([sl, id]) => avItem(id)?.slot === sl)) });
// av = { skin, hc(머리색 번호), cc(볼색 번호) }, wear = { cheek, eye, mouth, hair, top, bottom } → 겹친 그림 (div 하나)
// 처음 그릴 때 모든 그림을 미리 받아 풀어 둠: 색·옷을 바꿀 때 새 <img>가 잠깐 비었다가 뜨지 않게 (Image를 잡아 둬야 풀린 채로 남음)
let avPre = null;
const avPreload = () => avPre ||= [...AV_SKIN.map((_, i) => `av/base-${i}.png`), ...AV_ITEMS.map(it => it.img), ...AV_ITEMS.filter(it => it.slot === "hair").map(it => it.img.replace(".png", "-g.png")), ...AV_FRECK.map(i => `av/cheek-${i}-f.png`)]
  .map(s => { const im = new Image(); im.src = s; im.decode?.().catch(() => {}); return im; });
function avPic(av, wear = {}) {
  avPreload();
  const w = avWear(wear), skin = AV_SKIN[av?.skin] ? av.skin : 0, hc = AV_HAIR[av?.hc] && av.hc, cc = AV_CHEEK[av?.cc] ? av.cc : 0;
  const img = s => `<img src="${s}" alt="" draggable="false">`, hair = avItem(w.hair).img;
  const hairL = !hc ? img(hair) : (g => img(g) + `<i style="background:${AV_HAIR[hc][0]};-webkit-mask-image:url(${g});mask-image:url(${g})"></i>`)(hair.replace(".png", "-g.png"));
  const ck = avItem(w.cheek).img, cn = +w.cheek.split("-")[1];
  const cheekL = !cn ? "" : `<i style="background:${AV_CHEEK[cc][0]};-webkit-mask-image:url(${ck});mask-image:url(${ck})"></i>` + (AV_FRECK.includes(cn) ? img(ck.replace(".png", "-f.png")) : "");
  return `<div class="avp" aria-hidden="true">${img(`av/base-${skin}.png`)}${cheekL}${[avItem(w.eye).img, avItem(w.mouth).img, avItem(w.bottom).img, avItem(w.top).img].map(img).join("")}${hairL}</div>`;
}
