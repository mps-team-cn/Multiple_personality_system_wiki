const test = require("node:test");
const assert = require("node:assert/strict");

const {
  SECTIONS,
  dominantAxis,
  determineAlignmentDetails,
  determineAlignment,
  boundarySummary
} = require("../docs/assets/dnd-alignment-test.js");

function totals(lx, nx, cx, xg, xn, xe) {
  return { lx, nx, cx, xg, xn, xe };
}

test("Q1–Q36 的 144 个选项与经典原始计分表一致", () => {
  const expected = [
    "xg2,xg1,xe1,xe2",
    "xg2,xg1,xn1,xn2",
    "xe2,xe1,xn1,xn2",
    "lx2,lx1,cx1,cx2",
    "lx2,lx1,nx1,nx2",
    "cx1,cx2,nx1,nx2",
    "xe2,xe1,xg1,xg2",
    "xg2,xg1,xn1,xn2",
    "xe2,xe1,xn1,xn2",
    "lx2,lx1,cx1,cx2",
    "lx2,lx1,nx1,nx2",
    "nx2,nx1,cx1,cx2",
    "xg2,xg1,xn1,xn2",
    "xg2,xg1,xe1,xe2",
    "xn2,xn1,xe1,xe2",
    "lx2,lx1,cx1,cx2",
    "cx2,cx1,nx1,nx2",
    "lx2,lx1,nx1,nx2",
    "xg2,xg1,xe1,xe2",
    "xe2,xe1,xn1,xn2",
    "xg2,xg1,xn1,xn2",
    "lx2,lx1,cx1,cx2",
    "cx2,cx1,nx1,nx2",
    "lx2,lx1,nx1,nx2",
    "xe2,xe1,xn1,xn2",
    "xn2,xn1,xg1,xg2",
    "xg2,xg1,xe1,xe2",
    "lx2,lx1,nx1,nx2",
    "cx2,cx1,nx1,nx2",
    "cx2,cx1,lx1,lx2",
    "xg2,xg1,xe1,xe2",
    "xg2,xg1,xn1,xn1",
    "xe2,xe1,xn1,xn2",
    "nx2,nx1,lx1,lx2",
    "cx2,cx1,lx1,lx2",
    "nx2,nx1,cx1,cx2"
  ];
  const actual = SECTIONS.flatMap((section) => section.questions).map((question) =>
    question[1].map((option) => option[1] + option[2]).join(",")
  );

  assert.equal(actual.length, 36);
  assert.deepEqual(actual, expected);
});

test("第三部分使用集体与归属语境且保留六题结构", () => {
  const section = SECTIONS[2];
  const prompts = section.questions.map((question) => question[0]);

  assert.equal(section.title, "第三部分：集体与归属");
  assert.deepEqual(prompts, [
    "你会投入时间和金钱来改善自己所属的集体吗？",
    "你所属的集体面临严重的外部威胁，甚至可能因此解散或覆灭。你会：",
    "如果你受伤并需要立即帮助，集体中的其他人会愿意帮助你吗？",
    "你尊重所属集体的规则和管理者吗？",
    "集体中的其他人会排斥、躲避或嘲笑你吗？",
    "你会担任管理或代表性的职责，为集体成员的利益发声吗？"
  ]);

  assert.deepEqual(section.questions[1][1], [
    ["不惜重大个人代价，全力保护这个集体", "xg", 2],
    ["与其他成员一起尽力应对危机", "xg", 1],
    ["局势一变得严峻就选择离开", "xe", 1],
    ["与对立方达成交易，并暗中为其提供帮助", "xe", 2]
  ]);
});

test("单独最高分保持 dominant 状态并正常组合为 LG", () => {
  const result = determineAlignmentDetails(totals(12, 8, 4, 11, 6, 2));

  assert.equal(determineAlignment(totals(12, 8, 4, 11, 6, 2)), "lg");
  assert.equal(result.order.state, "dominant");
  assert.equal(result.moral.state, "dominant");
  assert.deepEqual(result.candidates, ["lg"]);
  assert.deepEqual(boundarySummary(result), []);
});

test("唯一中立最高分可正常组合为 NG 与 NN", () => {
  assert.equal(determineAlignment(totals(4, 10, 3, 11, 5, 2)), "ng");
  assert.equal(determineAlignment(totals(4, 10, 3, 5, 9, 2)), "nn");
});

test("L = N > C 记录相邻边界并自动生成 LG / NG", () => {
  const result = determineAlignmentDetails(totals(12, 12, 5, 13, 6, 2));

  assert.equal(result.code, "ng");
  assert.deepEqual(result.order, { code: "n", state: "boundary", winners: ["l", "n"] });
  assert.deepEqual(result.candidates, ["lg", "ng"]);
  assert.match(boundarySummary(result).join(" "), /边界倾向：守序善良 ↔ 中立善良/);
});

test("N = C > L 记录相邻边界并自动生成 NG / CG", () => {
  const result = determineAlignmentDetails(totals(5, 12, 12, 13, 6, 2));

  assert.equal(result.code, "ng");
  assert.deepEqual(result.order, { code: "n", state: "boundary", winners: ["n", "c"] });
  assert.deepEqual(result.candidates, ["ng", "cg"]);
});

test("G = N > E 记录道德轴相邻边界并自动生成 LG / LN", () => {
  const result = determineAlignmentDetails(totals(12, 6, 2, 13, 13, 5));

  assert.equal(result.code, "ln");
  assert.deepEqual(result.moral, { code: "n", state: "boundary", winners: ["g", "n"] });
  assert.deepEqual(result.candidates, ["lg", "ln"]);
});

test("N = E > G 记录道德轴相邻边界并自动生成 LN / LE", () => {
  const result = determineAlignmentDetails(totals(12, 6, 2, 4, 11, 11));

  assert.equal(result.code, "ln");
  assert.deepEqual(result.moral, { code: "n", state: "boundary", winners: ["n", "e"] });
  assert.deepEqual(result.candidates, ["ln", "le"]);
});

test("L = C > N 记录 extreme_tie，canonical 为 NG，候选为 LG / CG", () => {
  const result = determineAlignmentDetails(totals(12, 5, 12, 13, 6, 2));

  assert.equal(result.code, "ng");
  assert.deepEqual(result.order, { code: "n", state: "extreme_tie", winners: ["l", "c"] });
  assert.deepEqual(result.candidates, ["lg", "cg"]);
  assert.match(boundarySummary(result).join(" "), /特殊平局/);
});

test("G = E > N 记录 extreme_tie，canonical 为 LN，候选为 LG / LE", () => {
  const result = determineAlignmentDetails(totals(12, 6, 2, 11, 4, 11));

  assert.equal(result.code, "ln");
  assert.deepEqual(result.moral, { code: "n", state: "extreme_tie", winners: ["g", "e"] });
  assert.deepEqual(result.candidates, ["lg", "le"]);
  assert.match(boundarySummary(result).join(" "), /不能据此解释为普通中立倾向/);
});

test("L = N = C 记录 full_tie", () => {
  assert.deepEqual(
    dominantAxis(
      { code: "l", value: 10 },
      { code: "n", value: 10 },
      { code: "c", value: 10 }
    ),
    { code: "n", state: "full_tie", winners: ["l", "n", "c"] }
  );
});

test("G = N = E 记录 full_tie", () => {
  assert.deepEqual(
    dominantAxis(
      { code: "g", value: 10 },
      { code: "n", value: 10 },
      { code: "e", value: 10 }
    ),
    { code: "n", state: "full_tie", winners: ["g", "n", "e"] }
  );
});

test("双轴相邻平局自动生成四个候选阵营", () => {
  const result = determineAlignmentDetails(totals(12, 12, 5, 13, 13, 5));

  assert.equal(result.code, "nn");
  assert.deepEqual(result.candidates, ["lg", "ln", "ng", "nn"]);
  assert.match(boundarySummary(result).join(" "), /双轴边界/);
});

test("单轴全平且另一轴明确时保留三个候选阵营", () => {
  const result = determineAlignmentDetails(totals(10, 10, 10, 13, 6, 2));

  assert.equal(result.code, "ng");
  assert.deepEqual(result.candidates, ["lg", "ng", "cg"]);
  assert.match(boundarySummary(result).join(" "), /道德倾向明确：善良/);
});

test("两轴全部同分时 canonical 为 NN，并保留全部九个候选阵营", () => {
  const result = determineAlignmentDetails(totals(10, 10, 10, 9, 9, 9));

  assert.equal(result.code, "nn");
  assert.deepEqual(result.candidates, ["lg", "ln", "le", "ng", "nn", "ne", "cg", "cn", "ce"]);
  assert.match(boundarySummary(result).join(" "), /本次测试没有形成明显的阵营倾向/);
});
