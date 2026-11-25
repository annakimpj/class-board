// 우리반 보드 · 아바타 (교사 보드 index.html과 학생 화면 student.html이 같이 씀)
// 그림은 av/ 폴더의 PNG. 모든 그림이 같은 크기(258×386)라 그대로 겹치면 제자리 (av/comp.py가 원본 그림에서 잘라 맞춤)
// 겹치는 순서: 몸(피부, 얼굴 없음) → 볼터치 → 눈 → 입 → 신발(나중에) → 하의 → 상의 → 머리 → 펫 (오른쪽 허공이나 왼쪽 발치)
const AV_SKIN = [["#fff0f1"], ["#ffddd7"], ["#efc7b8"], ["#cea095"], ["#906a68"]]; // 몸 그림 av/base-0~4.png 색 (고르는 동그라미)
// 머리색: 0은 그림 원래 색. 나머지는 회색 머리(av/hair-N-g.png, av/hairgray.py로 만듦)에 색을 곱해서 칠함
const AV_HAIR = [["#6b4a3f"], ["#3a3a46"], ["#ffe066"], ["#ffb347"], ["#ff6b6b"], ["#ff9ccf"], ["#c39bff"], ["#6fa8ff"], ["#7fe3ff"], ["#6ee7b7"], ["#9be36b"], ["#eef1f6"]];
// 볼색: 볼터치 그림(av/cheek-N.png, av/cheek.py로 만듦)은 모양만 있어서 이 색을 곱해서 칠함. 주근깨(av/cheek-N-f.png)는 그림 색 그대로
const AV_CHEEK = [["#ff8fa3"], ["#ffab91"], ["#ff5c8a"], ["#ff6b6b"], ["#ffb36b"], ["#c9a0ff"]];
const AV_FRECK = [2, 3]; // 주근깨가 같이 있는 볼터치 번호
const AV_NAMES = {
  hair: ["부스스 짧은 머리", "레이어드 단발", "일자 단발", "웨이브 단발", "짧은 스포츠머리", "뾰족 머리", "뽀글 머리", "똥머리", "긴 생머리", "양 똥머리", "양 갈래 땋은 머리", "긴 웨이브"],
  top: ["세일러 블라우스", "크림 후드티", "검정 재킷", "분홍 가디건", "고양이 후드티", "흰 셔츠", "야구 점퍼", "곰돌이 니트", "검정 프릴 블라우스", "줄무늬 티", "하얀 패딩", "빨간 망토", "카키 야상", "멜빵 원피스", "검정 후드티", "레이스 블라우스"],
  eye: ["기본 눈", "날렵한 눈", "졸린 눈", "웃는 눈", "윙크", "반짝 눈", "울먹 눈", "화난 눈", "옆 보는 눈", "걱정 눈", "놀란 눈", "시큰둥 눈", "하트 눈", "빙글빙글 눈", "속눈썹 눈", "점 눈"],
  cheek: ["볼터치 없음", "볼 정중앙", "콧잔등 + 주근깨", "볼 정중앙 + 주근깨", "빗금 볼터치", "작은 동그라미", "콧잔등", "크게 발그레"],
  mouth: ["미소", "활짝 웃는 입", "고양이 입", "작은 입", "시무룩 입", "삐뚤 입", "씩 웃는 입", "메롱", "이 보이게 웃기", "놀란 입", "뽀뽀 입", "일자 입", "송곳니 웃음", "울먹 입", "크게 웃는 입", "쪽 입"],
  bottom: ["하늘 주름치마", "검정 주름치마", "베이지 반바지", "청반바지", "검정 카고 바지", "회색 운동복 바지", "남색 트레이닝 바지", "프릴 치마", "분홍 체크 치마", "카키 반바지", "체인 치마", "체크 바지"],
};
AV_NAMES.pet = ["펫 없음", "강아지", "삼색 고양이", "토끼", "햄스터", "아기 펭귄", "아기 공룡", "날개 고양이", "아기 드래곤", "천사 별", "달 고양이", "꼬마 로봇", "불새",
  "루돌프", "눈사람", "트리", "진저브레드", "산타 강아지", "북극곰", "천사 종", "스웨터 펭귄"]; // pet-0은 그림 없음
const AV_PRICE = {
  pet: [0, 12, 12, 12, 12, 12, 14, 16, 18, 16, 16, 18, 20, 14, 14, 14, 14, 15, 15, 16, 15], // 0이면 무료 (기본으로 입는 것)
  hair: [0, 6, 6, 7, 5, 7, 8, 8, 0, 9, 9, 8],
  top: [8, 7, 9, 7, 9, 0, 10, 8, 9, 0, 9, 10, 9, 9, 8, 10],
  eye: Array(16).fill(0), mouth: Array(16).fill(0), cheek: Array(8).fill(0), // 눈·입·볼터치는 모두 무료
  bottom: [6, 6, 0, 0, 7, 6, 7, 8, 7, 0, 8, 7],
};
const AV_ITEMS = Object.entries(AV_NAMES).flatMap(([slot, names]) => names.map((name, i) => ({ id: `${slot}-${i}`, slot, name, price: AV_PRICE[slot][i], img: `av/${slot}-${i}.png` })));
const AV_REQ = { pet: "pet-0", eye: "eye-0", mouth: "mouth-0", cheek: "cheek-1", hair: "hair-0", top: "top-5", bottom: "bottom-9" }; // 기본 옷 (흰 셔츠·카키 반바지). 이 칸들은 벗을 수 없어 늘 입고 있음
const AV_ACC = []; // 장신구 칸 (아직 없음)
const AV_TABS = [["eye", "눈"], ["mouth", "입"], ["cheek", "볼터치"], ["hair", "헤어"], ["top", "상의"], ["bottom", "하의"], ["pet", "펫"]]; // 신발은 그림이 생기면 추가
// 단위에 맞춘 글: "3 으쓱이 모자라요", "3으쓱으로 바꾸기" (이/가, 으로/로)
const avBat = w => { const c = w.charCodeAt(w.length - 1) - 0xac00; return c >= 0 && c < 11172 ? c % 28 : 0; }; // 받침 (0 없음, 8 ㄹ)
const avShort = (n, unit) => `${n} ${unit}${avBat(unit) ? "이" : "가"} 모자라요`;
const avPay = (n, unit) => `${n}${unit}${[0, 8].includes(avBat(unit)) ? "로" : "으로"} 바꾸기`;
const avItem = id => AV_ITEMS.find(x => x.id === id);
// 입은 것 중 지금 있는 물건만 (예전 픽셀 그림 물건 id는 버리고 기본으로)
const avWear = (wear = {}) => ({ ...AV_REQ, ...Object.fromEntries(Object.entries(wear).filter(([sl, id]) => avItem(id)?.slot === sl)) });
// av = { skin, hc(머리색 번호), cc(볼색 번호) }, wear = { pet, cheek, eye, mouth, hair, top, bottom } → 겹친 그림 (div 하나)
// 처음 그릴 때 모든 그림을 미리 받아 풀어 둠: 색·옷을 바꿀 때 새 <img>가 잠깐 비었다가 뜨지 않게 (Image를 잡아 둬야 풀린 채로 남음)
let avPre = null;
const avPreload = () => avPre ||= [...AV_SKIN.map((_, i) => `av/base-${i}.png`), ...AV_ITEMS.filter(it => it.id !== "pet-0").map(it => it.img), ...AV_ITEMS.filter(it => it.slot === "hair").map(it => it.img.replace(".png", "-g.png")), ...AV_FRECK.map(i => `av/cheek-${i}-f.png`)]
  .map(s => { const im = new Image(); im.src = s; im.decode?.().catch(() => {}); return im; });
function avPic(av, wear = {}) {
  avPreload();
  const w = avWear(wear), skin = AV_SKIN[av?.skin] ? av.skin : 0, hc = AV_HAIR[av?.hc] && av.hc, cc = AV_CHEEK[av?.cc] ? av.cc : 0;
  const img = s => `<img src="${s}" alt="" draggable="false">`, hair = avItem(w.hair).img;
  const hairL = !hc ? img(hair) : (g => img(g) + `<i style="background:${AV_HAIR[hc][0]};-webkit-mask-image:url(${g});mask-image:url(${g})"></i>`)(hair.replace(".png", "-g.png"));
  const ck = avItem(w.cheek).img, cn = +w.cheek.split("-")[1];
  const cheekL = !cn ? "" : `<i style="background:${AV_CHEEK[cc][0]};-webkit-mask-image:url(${ck});mask-image:url(${ck})"></i>` + (AV_FRECK.includes(cn) ? img(ck.replace(".png", "-f.png")) : "");
  // .avp = 펫 칸(378×426), 그 안의 .avb = 아바타 칸(258×386, 위 40·왼쪽 60 띄움). 펫 그림은 펫 칸 크기
  return `<div class="avp" aria-hidden="true"><div class="avb">${img(`av/base-${skin}.png`)}${cheekL}${[avItem(w.eye).img, avItem(w.mouth).img, avItem(w.bottom).img, avItem(w.top).img].map(img).join("")}${hairL}</div>${w.pet !== "pet-0" ? img(avItem(w.pet).img) : ""}</div>`;
}
