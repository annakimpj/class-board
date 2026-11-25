// 우리반 보드 · 아바타 (교사 보드 index.html과 학생 화면 student.html이 같이 씀)
// 그림은 av/ 폴더의 PNG. 모든 그림이 같은 크기(238×376)라 그대로 겹치면 제자리 (av/comp.py가 원본 그림에서 잘라 맞춤)
// 겹치는 순서: 몸(피부) → 신발(나중에) → 하의 → 상의 → 머리
const AV_SKIN = [["#fce6e2"], ["#fad8cb"], ["#ebbeab"], ["#cb9a88"], ["#8b655e"]]; // 몸 그림 av/body-0~4.png 색 (고르는 동그라미)
const AV_NAMES = {
  hair: ["부스스 짧은 머리", "레이어드 단발", "일자 단발", "웨이브 단발", "짧은 스포츠머리", "뾰족 머리", "뽀글 머리", "똥머리", "긴 생머리", "양 똥머리", "양 갈래 땋은 머리", "긴 웨이브"],
  top: ["세일러 블라우스", "크림 후드티", "검정 재킷", "분홍 가디건", "고양이 후드티", "흰 셔츠", "야구 점퍼", "곰돌이 니트", "검정 프릴 블라우스", "줄무늬 티", "하얀 패딩", "빨간 망토", "카키 야상", "멜빵 원피스", "검정 후드티", "레이스 블라우스"],
  bottom: ["하늘 주름치마", "검정 주름치마", "베이지 반바지", "청반바지", "검정 카고 바지", "회색 운동복 바지", "남색 트레이닝 바지", "프릴 치마", "분홍 체크 치마", "카키 반바지", "체인 치마", "체크 바지"],
};
const AV_PRICE = { // 0이면 무료 (기본으로 입는 것)
  hair: [0, 6, 6, 7, 5, 7, 8, 8, 0, 9, 9, 8],
  top: [8, 7, 9, 7, 9, 0, 10, 8, 9, 0, 9, 10, 9, 9, 8, 10],
  bottom: [6, 6, 0, 0, 7, 6, 7, 8, 7, 6, 8, 7],
};
const AV_ITEMS = Object.entries(AV_NAMES).flatMap(([slot, names]) => names.map((name, i) => ({ id: `${slot}-${i}`, slot, name, price: AV_PRICE[slot][i], img: `av/${slot}-${i}.png` })));
const AV_REQ = { hair: "hair-0", top: "top-5", bottom: "bottom-3" }; // 늘 입고 있는 칸 (없으면 기본)
const AV_ACC = []; // 장신구 칸 (아직 없음)
const AV_TABS = [["hair", "헤어"], ["top", "상의"], ["bottom", "하의"]]; // 신발은 그림이 생기면 추가
const avItem = id => AV_ITEMS.find(x => x.id === id);
// 입은 것 중 지금 있는 물건만 (예전 픽셀 그림 물건 id는 버리고 기본으로)
const avWear = (wear = {}) => ({ ...AV_REQ, ...Object.fromEntries(Object.entries(wear).filter(([sl, id]) => avItem(id)?.slot === sl)) });
// av = { skin }, wear = { hair, top, bottom } → 겹친 그림 (div 하나)
function avPic(av, wear = {}) {
  const w = avWear(wear), skin = AV_SKIN[av?.skin] ? av.skin : 0;
  const imgs = [`av/body-${skin}.png`, ...["bottom", "top", "hair"].map(sl => avItem(w[sl]).img)];
  return `<div class="avp" aria-hidden="true">${imgs.map(s => `<img src="${s}" alt="" draggable="false">`).join("")}</div>`;
}
