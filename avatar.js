// 우리반 보드 · 픽셀 아바타 (교사 보드 index.html과 학생 화면 student.html이 같이 씀)
// ───── 픽셀 아바타 (24×32, 사람 모양). 그림은 "글자x0,y0,x1,y1" 네모 칠하기로 적음. ~ 는 좌우 대칭도 함께 칠함
const AV_SKIN = [["#ffe3cf", "#f2c4a6"], ["#f8cfa5", "#e3ad7f"], ["#d9a074", "#bd8156"], ["#a26a45", "#82512f"]];
const AV_HAIR = [["#2e2b36", "#1a1820", "#55516a"], ["#5b3a29", "#3d2619", "#86604a"], ["#9a6532", "#74491f", "#c08a52"], ["#ecc45c", "#c99c33", "#f8e3a0"], ["#c9463c", "#972f28", "#ec7a6f"], ["#3f63c8", "#2a4590", "#7393ea"], ["#ec8fb8", "#cc6795", "#f8c2da"], ["#e9ecef", "#bfc5cc", "#ffffff"]];
const AV_FIX = { k: "#2b2430", e: "#2b2430", w: "#ffffff", c: "#ffb1b5", m: "#b8504a", g: "#ffd43b", G: "#f08c00", r: "#e03131", R: "#a61e1e", d: "#343a40", D: "#868e96", l: "#a5d8ff", n: "#ffffff" };
const AV_BODY = "s6,4,17,4 s5,5,18,5 s4,6,19,14 s5,15,18,15 s6,16,17,16 ~s3,10,3,12 ~S3,11 ~e7,10,8,12 w8,10 w16,10 ~c5,13,6,13 m11,14,12,14 S10,17,13,17 s7,18,16,23 ~s5,18,6,25 ~s8,25,10,28";
// 슬롯 그리는 순서: 뒷머리 → 몸 → 하의 → 신발 → 상의 → 목 → 앞머리 → 얼굴 → 머리 장신구
const AV_ITEMS = [
  // 헤어 (b: 뒷머리, f: 앞머리)
  { id: "h-short", slot: "hair", name: "짧은 머리", price: 0, f: "h8,2,15,2 h6,3,17,3 ~h4,4,5,4 h5,4,18,4 h4,5,19,7 h4,8,19,8 H5,8,8,8 H15,8,18,8 s10,8 s13,8 ~h3,6,3,10 ~H4,9,4,10 j9,3,11,3 j7,4,8,4" },
  { id: "h-bob", slot: "hair", name: "단발", price: 0, b: "h3,5,20,17", f: "h8,2,15,2 h6,3,17,3 h5,4,18,4 h4,5,19,8 h4,9,19,9 s8,9 s12,9 s15,9 ~H5,9,6,9 ~h2,7,4,16 ~H3,16,5,17 ~h5,10,5,15 ~H2,12,2,16 j9,3,11,3 j7,4,8,5" },
  { id: "h-long", slot: "hair", name: "긴 머리", price: 7, b: "h3,5,20,23 ~H2,9,2,22 ~H3,23,5,24", f: "h8,2,15,2 h6,3,17,3 h5,4,18,4 h4,5,19,8 h4,9,19,9 s9,9 s14,9 ~H5,9,6,9 ~h2,7,4,18 ~h5,10,5,13 ~H2,14,3,18 j9,3,11,3 j7,4,8,5" },
  { id: "h-pony", slot: "hair", name: "포니테일", price: 6, b: "h19,6,22,8 h20,9,22,15 h19,16,21,18 H21,10,22,16 r19,6,20,7", f: "h8,2,15,2 h6,3,17,3 h5,4,18,4 h4,5,19,8 h4,9,8,9 h15,9,19,9 h10,9,13,9 s11,9 ~H4,9,5,9 ~h3,6,3,11 j9,3,11,3 j7,4,8,5" },
  { id: "h-twin", slot: "hair", name: "양갈래", price: 8, b: "~h0,7,3,9 ~h0,10,2,19 ~H0,15,1,20 ~r2,6,3,7", f: "h8,2,15,2 h6,3,17,3 h5,4,18,4 h4,5,19,8 h4,9,19,9 s8,9 s11,9,12,9 s15,9 ~H4,9,5,9 ~h3,6,3,11 j9,3,11,3 j7,4,8,5" },
  { id: "h-bun", slot: "hair", name: "똥머리", price: 8, f: "h9,0,14,0 h8,1,15,1 H9,2,14,2 j10,0,11,0 h7,3,16,3 h5,4,18,4 h4,5,19,8 h4,9,19,9 s9,9 s14,9 ~H5,9,6,9 ~h3,6,3,11 j8,4,10,4" },
  { id: "h-spiky", slot: "hair", name: "뾰족 머리", price: 7, f: "h7,0 h11,0 h15,0 h6,1,8,1 h10,1,12,1 h14,1,16,1 h5,2,18,2 h4,3,19,7 ~h3,2 ~h3,4,3,9 h4,8,19,8 ~H5,8,7,8 H11,8,12,8 s9,8 s14,8 j8,2,9,2 j6,3,7,3" },
  { id: "h-curly", slot: "hair", name: "곱슬 머리", price: 9, b: "~h2,6,4,15 ~H2,14,4,15", f: "h7,1,9,1 h11,1,12,1 h14,1,16,1 h5,2,18,2 h4,3,19,7 ~h3,3,3,10 ~h2,5,2,13 h4,8,19,8 ~H4,8,5,8 H9,8 H14,8 s7,8 s11,8,12,8 s16,8 ~j6,3,7,3 j11,2,12,2" },
  // 상의 (full: 하의를 덮음)
  { id: "t-tee", slot: "top", name: "티셔츠", price: 0, c: { t: "#f8f9fa", T: "#d5dbe1" }, p: "t7,18,16,23 s10,18,13,18 ~t5,18,6,20 ~T7,19,7,23 T8,23,15,23 ~T5,20,6,20" },
  { id: "t-stripe", slot: "top", name: "줄무늬 티", price: 5, c: { t: "#ffffff", T: "#dee2e6", u: "#4c6ef5" }, p: "t7,18,16,23 s10,18,13,18 ~t5,18,6,20 u7,19,16,19 u7,21,16,21 ~u5,19,6,19 u8,23,15,23 ~T7,20 ~T7,22" },
  { id: "t-hood", slot: "top", name: "후드티", price: 7, c: { t: "#74c0fc", T: "#4dabf7", u: "#a5d8ff" }, p: "T8,17,15,17 t7,18,16,23 T10,18,13,18 ~t5,18,6,23 ~T5,23,6,23 u9,21,14,22 n10,19 n13,19 n10,20 n13,20 ~T7,19,7,23" },
  { id: "t-jacket", slot: "top", name: "노란 재킷", price: 8, c: { t: "#fcc419", T: "#e0a800", u: "#ffc9d6" }, p: "t7,18,16,23 u10,18,13,23 ~T9,18,9,20 ~t5,18,6,23 ~T5,23,6,23 ~T7,22,8,23 ~T7,19,7,21" },
  { id: "t-uniform", slot: "top", name: "교복", price: 9, c: { t: "#364fc7", T: "#2b3f9e", u: "#ffffff" }, p: "t7,18,16,23 u10,18,13,19 ~u9,18 r11,19,12,22 ~t5,18,6,23 ~T5,23,6,23 ~T7,19,7,23 T8,23,15,23 g9,20 g9,22" },
  { id: "t-dress", slot: "top", name: "원피스", price: 10, full: 1, c: { t: "#ff8fab", T: "#e0607e", u: "#ffffff" }, p: "t7,18,16,21 s10,18,13,18 u10,18,13,18 ~t5,18,6,19 t7,22,16,23 t6,24,17,25 t5,26,18,27 T5,27,18,27 ~T8,24 ~T11,25 u7,21,16,21" },
  // 하의
  { id: "b-jeans", slot: "bottom", name: "청바지", price: 0, c: { p: "#4f6fb3", P: "#3a5592" }, p: "p7,24,16,24 ~p8,25,10,28 ~P10,25,10,28 ~P8,28,10,28" },
  { id: "b-shorts", slot: "bottom", name: "반바지", price: 5, c: { p: "#8b6b4a", P: "#6b5034" }, p: "p7,24,16,24 ~p8,25,10,26 ~P8,26,10,26" },
  { id: "b-skirt", slot: "bottom", name: "치마", price: 6, c: { p: "#e8590c", P: "#c2410c" }, p: "p7,24,16,24 p7,25,16,25 p6,26,17,26 P6,26 P9,26 P12,26 P15,26 P17,26" },
  { id: "b-pants", slot: "bottom", name: "체크 바지", price: 7, c: { p: "#6c757d", P: "#495057", u: "#868e96" }, p: "p7,24,16,24 ~p8,25,10,28 ~u8,26,10,26 ~u9,25,9,28 ~P8,28,10,28" },
  // 신발
  { id: "s-sneak", slot: "shoes", name: "운동화", price: 0, c: { o: "#ffffff", O: "#adb5bd" }, p: "~o7,29,10,29 ~O7,30,10,30" },
  { id: "s-red", slot: "shoes", name: "빨간 구두", price: 5, c: { o: "#e03131", O: "#a61e1e" }, p: "~o7,29,10,29 ~O7,30,10,30 ~n8,29" },
  { id: "s-boot", slot: "shoes", name: "장화", price: 6, c: { o: "#fab005", O: "#e67700" }, p: "~o8,27,10,29 ~o7,29 ~O7,30,10,30" },
  { id: "s-brown", slot: "shoes", name: "갈색 구두", price: 6, c: { o: "#7a4b2a", O: "#4f2e17" }, p: "~o7,29,10,29 ~O7,30,10,30" },
  // 장신구 (예전 장신구 이름 그대로: 이미 산 것은 그대로 가짐)
  { id: "ribbon", slot: "head", name: "리본", price: 5, p: "r15,3 r17,3 r15,5 r17,5 R16,4 r14,4 r18,4" },
  { id: "clip", slot: "head", name: "꽃핀", price: 5, p: "n16,5 n18,5 n17,4 n17,6 g17,5" },
  { id: "bowtie", slot: "neck", name: "나비넥타이", price: 5, p: "~r9,18,10,18 ~r9,19 R11,18,12,18" },
  { id: "glasses", slot: "face", name: "안경", price: 6, p: "~k6,9,9,9 ~k6,13,9,13 ~k6,10,6,12 ~k9,10,9,12 k10,10,13,10" },
  { id: "scarf", slot: "neck", name: "목도리", price: 7, p: "r8,17,15,18 n9,17 n11,17 n13,17 R14,19,15,22 n14,20" },
  { id: "hat", slot: "head", name: "모자", price: 7, p: "l6,1,17,1 l5,2,18,4 d5,4,18,4 d4,5,21,5 n10,2,12,3" },
  { id: "sunglasses", slot: "face", name: "선글라스", price: 8, p: "~k6,9,9,9 ~k6,10,9,12 ~D7,10 k10,10,13,10" },
  { id: "headphones", slot: "head", name: "헤드폰", price: 9, p: "D6,1,17,1 ~D4,2,5,3 ~D3,4,3,8 ~r2,9,4,12 ~R2,12,4,12" },
  { id: "crown", slot: "head", name: "왕관", price: 10, p: "g7,0 g11,0,12,0 g16,0 g7,1,8,1 g10,1,13,1 g15,1,16,1 g7,2,16,3 G7,3,16,3 r9,2 l12,2 r14,2" },
  // 배경
  { id: "bg-none", slot: "bg", name: "없음", price: 0, p: "" },
  { id: "bg-sky", slot: "bg", name: "하늘", price: 5, c: { a: "#a5d8ff", A: "#d0ebff", b: "#69db7c", B: "#40c057" }, p: "a0,0,23,15 A0,16,23,25 n3,5,7,6 n2,6 n16,9,20,10 n15,10 b0,26,23,31 B0,26,23,26 B4,29 B12,28 B19,30" },
  { id: "bg-class", slot: "bg", name: "교실", price: 6, c: { a: "#fff4d6", A: "#2f6e4f", b: "#c08a52", B: "#9a6532" }, p: "a0,0,23,23 B1,3,22,15 A2,4,21,14 n4,6,7,6 n4,8,9,8 n13,11,18,11 n20,13 b0,24,23,31 B0,24,23,24 B0,28,23,28 B6,25,6,27 B17,29,17,31" },
  { id: "bg-park", slot: "bg", name: "공원", price: 6, c: { a: "#c5f6fa", A: "#2b8a3e", b: "#8ce99a", B: "#7a4b2a" }, p: "a0,0,23,31 A0,6,4,13 A1,4,3,5 B2,14,2,22 A19,8,23,15 A20,6,22,7 B21,16,21,22 b0,23,23,31 A0,23,23,23 g11,2 g10,3,12,3 g11,4" },
  { id: "bg-night", slot: "bg", name: "밤하늘", price: 8, c: { a: "#1c2541", A: "#3a506b" }, p: "a0,0,23,31 A0,24,23,31 g18,2,20,4 a17,2 a17,3 g3,3 g8,6 g21,9 g2,12 g14,1 g6,17 g22,15 n12,4 n4,8" },
  { id: "bg-beach", slot: "bg", name: "바다", price: 8, c: { a: "#d0ebff", A: "#339af0", b: "#ffe8a3", B: "#1c7ed6" }, p: "a0,0,23,17 g19,2,21,4 A0,18,23,24 B0,20,23,20 B3,23,8,23 B15,22,20,22 n5,19 n17,21 b0,25,23,31 G4,28 G18,29" },
  { id: "bg-street", slot: "bg", name: "거리", price: 10, c: { a: "#e7f5ff", A: "#f3c6c6", b: "#ced4da", B: "#868e96" }, p: "a0,0,23,31 A0,2,5,24 A18,4,23,24 B1,5,3,8 B1,12,3,15 B19,7,22,10 B19,13,22,16 n2,6 n20,8 b0,25,23,31 B0,25,23,25 n10,28,13,28 n4,29,7,29 n16,29,19,29" },
];
const AV_REQ = { hair: "h-short", top: "t-tee", bottom: "b-jeans", shoes: "s-sneak", bg: "bg-none" }; // 늘 입고 있는 슬롯 (없으면 기본)
const avItem = id => AV_ITEMS.find(x => x.id === id);
function avPaint(spec, set) {
  if (spec) spec.split(" ").forEach(tok => {
    const mir = tok[0] === "~", ch = tok[mir ? 1 : 0], [x0, y0, x1 = x0, y1 = y0] = tok.slice(mir ? 2 : 1).split(",").map(Number);
    for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) { set(x, y, ch); if (mir) set(23 - x, y, ch); }
  });
}
// av = { skin, hair }, wear = { hair, top, bottom, shoes, neck, face, head, bg }
function avSvg(av, wear = {}) {
  const w = { ...AV_REQ, ...wear }, [s, S] = AV_SKIN[av.skin] || AV_SKIN[0], [hc, H, j] = AV_HAIR[av.hair] || AV_HAIR[0];
  const base = { ...AV_FIX, s, S, h: hc, H, j };
  const it = sl => avItem(w[sl]) || avItem(AV_REQ[sl]);
  const bg = [], ch = [];
  const lay = (grid, spec, c) => { const pal = { ...base, ...c }; avPaint(spec, (x, y, k) => { if (x >= 0 && x < 24 && y >= 0 && y < 32 && pal[k]) (grid[y] ||= [])[x] = pal[k]; }); };
  const bgI = it("bg"); lay(bg, bgI?.p, bgI?.c);
  const hair = it("hair"), top = it("top");
  lay(ch, hair.b); lay(ch, AV_BODY);
  if (!top.full) lay(ch, it("bottom").p, it("bottom").c);
  lay(ch, it("shoes").p, it("shoes").c); lay(ch, top.p, top.c);
  for (const sl of ["neck"]) { const x = avItem(w[sl]); x && lay(ch, x.p, x.c); }
  lay(ch, hair.f);
  for (const sl of ["face", "head"]) { const x = avItem(w[sl]); x && lay(ch, x.p, x.c); }
  const has = (x, y) => !!ch[y]?.[x];
  const out = {}; // 바깥 테두리는 그림 밖(-1, 24, 32)까지 그려서 잘리지 않게
  for (let y = -1; y <= 32; y++) for (let x = -1; x <= 24; x++) if (!has(x, y) && (has(x - 1, y) || has(x + 1, y) || has(x, y - 1) || has(x, y + 1))) (out[y] ||= {})[x] = AV_FIX.k;
  let r = "";
  const run = (row, y, x0, x1, grow) => { for (let x = x0; x <= x1;) { const c = row[x]; if (!c) { x++; continue; } let n = 1; while (x + n <= x1 && row[x + n] === c) n++; const a = grow && x === 0 ? -1 : x, b = grow && x + n === 24 ? 25 : x + n; r += `<rect x="${a}" y="${y}" width="${b - a}" height="1" fill="${c}"/>`; x += n; } };
  bg.forEach((row, y) => { if (!row) return; run(row, y, 0, 23, 1); if (y === 0) run(row, -1, 0, 23, 1); if (y === 31) run(row, 32, 0, 23, 1); });
  for (const y in out) run(out[y], +y, -1, 24);
  ch.forEach((row, y) => row && run(row, y, 0, 23));
  return `<svg viewBox="-1 -1 26 34" shape-rendering="crispEdges" aria-hidden="true">${r}</svg>`;
}
const AV_TABS = [["hair", "헤어"], ["top", "상의"], ["bottom", "하의"], ["shoes", "신발"], ["acc", "장신구"], ["bg", "배경"]];
