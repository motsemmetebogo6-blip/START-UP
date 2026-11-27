// build_deck.js – SAF uprate presentation: all visuals and how the optimisation was achieved.
// Every number comes from results/model/*.csv (model outputs); nothing is typed from memory.
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const SKILL = process.env.PPTX_SKILL;
const { applyTheme } = require(path.join(SKILL, "scripts/apply_theme.js"));

const ROOT = path.resolve(__dirname, "..");
const FIG = (f) => path.join(ROOT, "report/figures", f);
const OUT = path.join(ROOT, "deliverables/SAF_Uprate_Optimisation_Presentation.pptx");

const THEME = {
  name: "SAF Furnace",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1F2328", lt1: "FFFFFF", dk2: "23272E", lt2: "F0F1F3",
    accent1: "D9541E", accent2: "3E6E8E", accent3: "2E8B57", accent4: "C0392B",
    accent5: "E8A33D", accent6: "7A8691", hlink: "3E6E8E", folHlink: "6D5A8E",
  },
};
const HEX = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Closed ferrochrome SAF uprate 55 → 60 MW: model results and optimisation";
pres.author = "MPG 118S project team";
const C = pres.SchemeColor;

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "TITLE_DARK",
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.7, y: 2.0, w: 11.9, h: 1.9, fontSize: 40, bold: true, color: C.background1, valign: "bottom", align: "left" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.7, y: 4.1, w: 11.9, h: 1.6, fontSize: 18, color: C.background2, valign: "top" }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "SECTION",
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.7, y: 2.6, w: 11.9, h: 1.2, fontSize: 40, bold: true, color: C.background1, valign: "bottom", align: "left" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.7, y: 3.95, w: 11.9, h: 1.2, fontSize: 18, color: C.background2, valign: "top" }, text: "" } },
  ],
  slideNumber: { x: 12.3, y: 6.95, w: 0.6, h: 0.35, fontSize: 10, color: C.background2 },
});
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: C.background1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.9, fontSize: 28, bold: true, color: C.text1, valign: "middle", align: "left", margin: 0 }, text: "" } },
    { text: { text: "Ferrochrome SAF uprate · MPG 118S · values from verified model (Python, cross-checked in MATLAB/Octave)", options: { x: 0.6, y: 6.95, w: 10.5, h: 0.35, fontSize: 10, color: C.accent6, margin: 0 } } },
  ],
  slideNumber: { x: 12.3, y: 6.95, w: 0.6, h: 0.35, fontSize: 10, color: C.accent6 },
});

// ---------- helpers ----------
const X0 = 0.6, W = 12.13, Y0 = 1.45, YMAX = 6.75;
let current = "";
function section(title, sub) {
  current = title;
  pres.addSection({ title });
  const s = pres.addSlide({ masterName: "SECTION", sectionTitle: title });
  s.addText(title, { placeholder: "title" });
  s.addText(sub, { placeholder: "body" });
  return s;
}
function content(title) {
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: current });
  s.addText(title, { placeholder: "title" });
  return s;
}
function bullets(s, items, opt) {
  // pptxgenjs splits a paragraph at every run that carries bullet options, so each item is one run;
  // an item given as parts is joined and takes the emphasis of its emphasised part.
  const runs = items.map((t, i) => {
    const parts = Array.isArray(t) ? t : [{ text: t }];
    const emph = parts.find((p) => p.bold || p.color) || {};
    return {
      text: parts.map((p) => p.text).join(""),
      options: Object.assign({ bold: !!emph.bold && parts.length === 1 || parts.every((p) => p.bold), color: emph.color || C.text1,
        bullet: { indent: 15 }, paraSpaceAfter: 8 }, i < items.length - 1 ? { breakLine: true } : {}),
    };
  });
  s.addText(runs, Object.assign({ fontSize: 15, valign: "top", isTextBox: true, margin: 0.12 }, opt));
}
function fit(aspect, maxW, maxH) {
  let w = maxW, h = w / aspect;
  if (h > maxH) { h = maxH; w = h * aspect; }
  return { w, h };
}
// Figure on the left, takeaway panel on the right
function figSide(title, img, aspect, items, notes, panelTitle = "What it shows") {
  const s = content(title);
  const { w, h } = fit(aspect, 7.9, YMAX - Y0);
  s.addImage({ path: FIG(img), x: X0, y: Y0 + (YMAX - Y0 - h) / 2, w, h, altText: title, objectName: "figure" });
  const px = 8.85, pw = X0 + W - px;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: px, y: Y0, w: pw, h: YMAX - Y0, fill: { color: C.background2 }, line: { type: "none" }, rectRadius: 0.08, objectName: "takeaway panel" });
  s.addText(panelTitle, { x: px + 0.2, y: Y0 + 0.15, w: pw - 0.4, h: 0.45, fontSize: 18, bold: true, color: C.accent1, fontFace: THEME.headFontFace, isTextBox: true, margin: 0 });
  bullets(s, items, { x: px + 0.1, y: Y0 + 0.7, w: pw - 0.2, h: YMAX - Y0 - 0.85 });
  if (notes) s.addNotes(notes);
  return s;
}
// Wide figure on top, numbered takeaway cards below
function figWide(title, img, aspect, cards, notes, maxH = 3.55) {
  const s = content(title);
  const { w, h } = fit(aspect, W, maxH);
  s.addImage({ path: FIG(img), x: X0 + (W - w) / 2, y: Y0, w, h, altText: title, objectName: "figure" });
  const cy = Y0 + h + 0.3, ch = YMAX - cy, n = cards.length, gap = 0.3, cw = (W - gap * (n - 1)) / n;
  cards.forEach((c, i) => {
    const cx = X0 + i * (cw + gap);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: cx, y: cy, w: cw, h: ch, fill: { color: C.background2 }, line: { type: "none" }, rectRadius: 0.08, objectName: `card ${i + 1}` });
    s.addShape(pres.shapes.OVAL, { x: cx + 0.2, y: cy + 0.2, w: 0.45, h: 0.45, fill: { color: C.accent1 }, line: { type: "none" }, objectName: `marker ${i + 1}` });
    s.addText(String(i + 1), { x: cx + 0.2, y: cy + 0.2, w: 0.45, h: 0.45, fontSize: 15, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText(c[0], { x: cx + 0.8, y: cy + 0.18, w: cw - 1.0, h: 0.5, fontSize: 16, bold: true, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
    s.addText(c[1], { x: cx + 0.2, y: cy + 0.8, w: cw - 0.4, h: ch - 0.9, fontSize: 14, color: C.text1, valign: "top", margin: 0, isTextBox: true });
  });
  if (notes) s.addNotes(notes);
  return s;
}
function stat(s, x, y, w, h, value, label, color) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: C.background2 }, line: { type: "none" }, rectRadius: 0.08, objectName: "stat card" });
  s.addText(value, { x: x + 0.2, y: y + 0.15, w: w - 0.4, h: h * 0.52, fontSize: 40, bold: true, color: color || C.accent1, fontFace: THEME.headFontFace, valign: "bottom", margin: 0, isTextBox: true });
  s.addText(label, { x: x + 0.2, y: y + 0.2 + h * 0.52, w: w - 0.4, h: h * 0.48 - 0.35, fontSize: 14, color: C.text1, valign: "top", margin: 0, isTextBox: true });
}
const tbl = (rows, header) => [header.map((t) => ({ text: t, options: { bold: true, color: HEX.lt1, fill: { color: HEX.dk2 } } })), ...rows];

// ---------- 1. Title ----------
pres.addSection({ title: "Opening" });
current = "Opening";
let s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Opening" });
s.addText("Uprating a closed ferrochrome SAF from 55 to 60 MW", { placeholder: "title" });
s.addText([
  { text: "Model results, mass balance, optimisation and sensitivity", options: { breakLine: true } },
  { text: "MPG 118S · BEngTech Metallurgical Engineering · Tshwane University of Technology", options: { fontSize: 14 } },
], { placeholder: "body" });
s.addNotes("This deck presents every visual produced by the project model and explains, step by step, how the optimised design (C1) was reached and checked.");

// ---------- 2. Answer first ----------
s = content("C1 meets 450 t/d, but only at its operating limits");
stat(s, X0, Y0, 3.85, 1.75, "455 t/d", "C1 production (60 MW mean + hot charging), from 394 t/d today", C.accent1);
stat(s, X0, Y0 + 2.0, 3.85, 1.75, "R1 479 M", "NPV over 15 years at 12 %; IRR 68.7 %, payback 1.5 years", C.accent3);
stat(s, X0, Y0 + 4.0, 3.85, 1.3, "86.9 %", "Cr recovery from reconciled mass balance (not the 78 % assumed)", C.accent2);
s.addChart(pres.charts.BAR, [{ name: "Production (t/d)", labels: ["A existing", "E1 PF 0.95", "S-B 60 MW", "P1 hot charge", "C1 selected"], values: [393.8, 402.3, 411.4, 435.1, 454.6] }], {
  x: 4.75, y: Y0, w: 7.98, h: 4.75, barDir: "col",
  chartColors: [HEX.accent6], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0", dataLabelFontSize: 12, dataLabelColor: HEX.dk1, dataLabelFontFace: "+mn-lt",
  showTitle: true, title: "Daily production by scenario (target 450 t/d)", titleFontSize: 15, titleColor: HEX.dk1, titleFontFace: "+mn-lt",
  valAxisMinVal: 350, valAxisMaxVal: 470, valAxisMajorUnit: 20, valAxisLabelFontSize: 12, catAxisLabelFontSize: 12,
  valAxisLabelColor: HEX.accent6, catAxisLabelColor: HEX.dk1, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
  valGridLine: { color: "D9DCE0", size: 0.5 }, catGridLine: { style: "none" }, showLegend: false,
  invertedColors: [HEX.accent6],
});
s.addText("Only C1 clears 450 t/d; every other single measure falls short.", { x: 5.0, y: 6.35, w: 7.5, h: 0.4, fontSize: 14, italic: true, color: C.accent6, margin: 0, isTextBox: true });
s.addNotes("Headline: C1 = PF raised to 0.95, load factor 0.972, 60 MW mean, plus hot charging of pellets at about 500 °C. Production 454.6 t/d in the technical model (454.8 t/d in the economic model, which uses 60.02 MW).");

// ---------- 3. Roadmap ----------
s = content("How the optimisation was achieved: five steps");
const steps = [
  ["Audit", "Recalculated 52 team numbers; found three meanings of \"60 MW\""],
  ["Electrical model", "8 scenarios on one 65 MVA basis; Westly current estimate"],
  ["Mass balance", "7 element balances reconciled by weighted NNLS"],
  ["Optimise", "Least preheat T for 450 t/d; then Monte Carlo and robust design"],
  ["Sensitivity", "NPV tornado, electrical and auxiliary response"],
];
const sw = (W - 0.3 * 4) / 5;
steps.forEach((st, i) => {
  const x = X0 + i * (sw + 0.3);
  s.addShape(pres.shapes.OVAL, { x: x + sw / 2 - 0.55, y: 1.9, w: 1.1, h: 1.1, fill: { color: i === 3 ? C.accent1 : C.text2 }, line: { type: "none" }, objectName: `step ${i + 1}` });
  s.addText(String(i + 1), { x: x + sw / 2 - 0.55, y: 1.9, w: 1.1, h: 1.1, fontSize: 32, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true, fontFace: THEME.headFontFace });
  if (i < 4) s.addShape(pres.shapes.LINE, { x: x + sw / 2 + 0.65, y: 2.45, w: sw + 0.3 - 1.3, h: 0, line: { color: C.accent6, width: 1.5, endArrowType: "triangle" }, objectName: `arrow ${i + 1}` });
  s.addText(st[0], { x, y: 3.25, w: sw, h: 0.5, fontSize: 18, bold: true, color: C.text1, align: "center", margin: 0, isTextBox: true });
  s.addText(st[1], { x, y: 3.8, w: sw, h: 1.3, fontSize: 14, color: C.text1, align: "center", valign: "top", margin: 0, isTextBox: true });
});
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: X0, y: 5.35, w: W, h: 1.3, fill: { color: C.background2 }, line: { type: "none" }, rectRadius: 0.08, objectName: "rule box" });
s.addText([
  { text: "Rules applied throughout: ", options: { bold: true } },
  { text: "no invented plant data; every input tagged by provenance (measured, supplied, assumed, literature); every result verified in Python and cross-validated in MATLAB/Octave." },
], { x: X0 + 0.25, y: 5.45, w: W - 0.5, h: 1.1, fontSize: 15, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
s.addNotes("Step 4 (orange) is the optimisation proper. It rests on steps 1–3 and is stress-tested in step 5.");

// ---------- Section A: audit and electrical ----------
section("Audit and electrical model", "Putting every scenario on one transformer basis");

s = content("The audit found three different meanings of \"60 MW\"");
[["S-B: 60 MW mean", "PF 0.95, LF 0.972. On-load 64.98 MVA = 100 % of rating. Recommended definition.", C.accent3],
 ["S-N60: 60 MW continuous", "LF = 1 at PF 0.93. Assumes no outages; not achievable in practice.", C.accent4],
 ["S-O60: 60 MW on load", "Mean only 57 MW, so production falls to 391 t/d, below today.", C.accent4]].forEach((c, i) => {
  const y = Y0 + i * 1.8;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: X0, y, w: 4.6, h: 1.55, fill: { color: C.background2 }, line: { type: "none" }, rectRadius: 0.08, objectName: `meaning ${i + 1}` });
  s.addShape(pres.shapes.OVAL, { x: X0 + 0.2, y: y + 0.22, w: 0.32, h: 0.32, fill: { color: c[2] }, line: { type: "none" }, objectName: "status dot" });
  s.addText(c[0], { x: X0 + 0.65, y: y + 0.12, w: 3.8, h: 0.5, fontSize: 16, bold: true, color: C.text1, margin: 0, valign: "middle", isTextBox: true });
  s.addText(c[1], { x: X0 + 0.2, y: y + 0.65, w: 4.2, h: 0.85, fontSize: 14, color: C.text1, margin: 0, valign: "top", isTextBox: true });
});
{ const { w, h } = fit(2.04, 7.25, 5.3); s.addImage({ path: FIG("F2_transformer_loading.png"), x: X0 + W - w, y: Y0 + (YMAX - Y0 - h) / 2, w, h, altText: "Transformer loading by scenario", objectName: "figure" }); }
s.addNotes("Audit findings AF-01 to AF-03. The load factor is an uptime fraction, not a 95 % loading cap. The baseline is 393.65 t/d actual production, not a 55 MW continuous furnace.");

figSide("Operating envelope: where 60 MW mean is possible", "F1_operating_envelope.png", 1.39, [
  "Mean power P = S · PF · LF, with S fixed at 65 MVA (existing transformers).",
  [{ text: "60 MW mean needs " }, { text: "PF = 0.95 and LF ≥ 0.972", bold: true }, { text: " together." }],
  "PF 0.95 is the supervisor's upper limit, so LF (uptime) is the remaining lever.",
  "No transformer replacement is needed, but there is no headroom.",
], "F1. Feasible region of power factor and load factor for the 65 MVA rating.");

figSide("Raising PF: the route chosen changes the electrode current", "F3_pf_route_current_density.png", 1.44, [
  [{ text: "Resistance route: ", bold: true }, { text: "current ratio √(sinφ₁/sinφ₀) = 0.922, which reduces current density." }],
  [{ text: "Reactance route: ", bold: true }, { text: "ratio √(PF₁/PF₀) = 1.011, a slight increase." }],
  "Current is estimated from Westly I = 8.33 · P^(2/3) (literature constant; flagged as estimate, AF-08).",
], "Audit finding AF-10: the team's documents mixed the two routes.");

// ---------- Section B: mass balance ----------
section("Mass balance", "Reconciling the supplied analyses into one consistent balance");

figSide("Seven element balances, five unknowns: a reconciled balance", "F4_mass_balance.png", 1.29, [
  "Balances on Al₂O₃, MgO, CaO, SiO₂, Cr, Fe and C per tonne of alloy.",
  "Unknowns: ore, reductant, quartz, limestone and slag rates.",
  [{ text: "Solved by weighted non-negative least squares " }, { text: "(Python bvls; MATLAB lsqnonneg)", bold: true }, { text: "." }],
  "Result: ore 2.144 t/t, reductant 0.433 t/t, flux 0.366 t/t, slag 1.188 t/t.",
], "Seven equations, five unknowns: the extra two equations test whether the data are consistent.", "Method and result");

s = content("The data are consistent, and Cr recovery is 86.9 %, not 78 %");
{ const a = fit(2.7, W, 2.35); s.addImage({ path: FIG("F5_balance_residuals.png"), x: X0 + (W - a.w) / 2, y: Y0, w: a.w, h: a.h, altText: "Balance residuals", objectName: "figure residuals" });
  const b = fit(2.39, W, 2.55); s.addImage({ path: FIG("F6_chromium_recovery.png"), x: X0 + (W - b.w) / 2, y: Y0 + a.h + 0.2, w: b.w, h: b.h, altText: "Chromium recovery", objectName: "figure recovery" }); }
s.addNotes("Top (F5): all seven residuals are within ±3 % of feed; the largest is CaO at −2.91 %. Mass closure is −0.41 %. Bottom (F6): of 579.9 kg Cr fed per tonne of alloy, 77.5 kg reports to slag, giving 86.9 % recovery. The workbook's 78 % assumption overstates ore demand.");

s = content("What the balance changed in the team's numbers");
s.addTable(tbl([
  ["Cr recovery to alloy", "78 % (assumed)", "86.9 %", "Ore and cost estimates were too high"],
  ["Ore rate", "2.13 t/t (estimate)", "2.144 t/t", "Confirmed, now traceable"],
  ["Reductant rate (dry)", "0.433 t/t", "0.433 t/t", "Confirmed by carbon balance"],
  ["Flux rate (quartz + limestone)", "0.449 t/t", "0.366 t/t", "18 % less flux"],
  ["Slag rate", "–", "1.188 t/t", "New: sizes tapping and slag handling"],
  ["Off-gas (CO + CO₂ + H₂O)", "–", "597 Nm³/t", "9 797 → 11 315 Nm³/h at C1"],
  ["Largest balance residual", "–", "2.9 % (CaO)", "Within ±3 %: data consistent"],
], ["Quantity", "Team value", "Reconciled", "Consequence"]), {
  x: X0, y: Y0, w: W, colW: [3.3, 2.4, 2.2, 4.23], fontSize: 14, color: HEX.dk1, fontFace: "Calibri",
  border: { type: "solid", pt: 0.5, color: "D9DCE0" }, rowH: 0.52, valign: "middle", margin: [0.05, 0.1, 0.05, 0.1],
  fill: { color: HEX.lt1 },
});
s.addNotes("All reconciled values from results/model/I2_mass_balance_kpis.csv.");

figSide("Every auxiliary duty rises by about 15 % at C1", "F10_daily_duties.png", 1.64, [
  "Per-tonne rates are fixed by chemistry, so duties scale with production.",
  "Ore 844 → 975 t/d; slag 468 → 540 t/d; off-gas +15.5 %.",
  "These duties feed the auxiliary check in the sensitivity analysis.",
], "F10. Daily material duties: existing operation against C1.");

// ---------- Section C: optimisation ----------
section("Optimisation", "From a single answer to a design that holds under uncertainty");

s = content("Three stages: deterministic, probabilistic, robust");
[["Deterministic", "Minimise preheat temperature T\nsubject to production ≥ 450 t/d, PF ≤ 0.95, LF ≤ LF_max.\nSolved with SLSQP; checked against the closed form below.", "T = 452 °C at LF 0.972"],
 ["Monte Carlo", "Sample the uncertain inputs (100 000 runs):\nhot-charge saving, SEC, LF, PF, T.\nAsk: how often is 450 t/d met?", "P(≥ 450 t/d) = 9.9 %"],
 ["Robust", "Find T that meets 450 t/d with 50 % and 90 % probability (chance constraint).\nCompare uncertain against plant-verified saving.", "Verified saving: 610 °C for P90"]].forEach((c, i) => {
  const cw = (W - 0.6) / 3, x = X0 + i * (cw + 0.3);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: Y0, w: cw, h: 3.55, fill: { color: C.background2 }, line: { type: "none" }, rectRadius: 0.08, objectName: `stage ${i + 1}` });
  s.addShape(pres.shapes.OVAL, { x: x + 0.25, y: Y0 + 0.25, w: 0.5, h: 0.5, fill: { color: C.accent1 }, line: { type: "none" }, objectName: "marker" });
  s.addText(String(i + 1), { x: x + 0.25, y: Y0 + 0.25, w: 0.5, h: 0.5, fontSize: 16, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addText(c[0], { x: x + 0.9, y: Y0 + 0.25, w: cw - 1.1, h: 0.5, fontSize: 20, bold: true, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
  s.addText(c[1], { x: x + 0.25, y: Y0 + 0.95, w: cw - 0.5, h: 1.75, fontSize: 14, color: C.text1, valign: "top", margin: 0, isTextBox: true });
  s.addText(c[2], { x: x + 0.25, y: Y0 + 2.8, w: cw - 0.5, h: 0.55, fontSize: 16, bold: true, color: C.accent1, valign: "middle", margin: 0, isTextBox: true });
});
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: X0, y: 5.3, w: W, h: 1.4, fill: { color: C.text2 }, line: { type: "none" }, rectRadius: 0.08, objectName: "equation box" });
s.addText([
  { text: "Closed-form check:  T* = T_ref + 100 · (SEC₀ − 24 · S · PF · LF / 450) / s", options: { bold: true, breakLine: true } },
  { text: "with SEC(T) = 3.5 − s · (T − 25)/100, s = 0.070 MWh/t per 100 °C (vendor rule), S = 65 MVA. SLSQP and closed form agree to 0.0 °C at every LF." },
], { x: X0 + 0.3, y: 5.35, w: W - 0.6, h: 1.3, fontSize: 15, color: C.background1, valign: "middle", margin: 0, isTextBox: true });
s.addNotes("Preheat referenced to ambient (25 °C), which is the conservative choice (audit AF-14). With the team's 0 °C reference the optimum is 427 °C at LF 0.972.");

figSide("Optimisation map: least preheat temperature against uptime", "F7_optimisation_map.png", 1.33, [
  "At PF 0.95, each extra 1 % of load factor saves about 25 °C of preheat.",
  "LF 0.972 → T = 452 °C; LF 0.95 → 556 °C (ambient reference).",
  [{ text: "Optimiser and closed form agree exactly", bold: true }, { text: ", which verifies the solution." }],
], "F7. Minimum hot-charge temperature for 450 t/d against achievable load factor.");

figSide("Monte Carlo: the point design meets 450 t/d 1 time in 10", "F8_montecarlo.png", 1.81, [
  "100 000 samples of the uncertain inputs.",
  "Median 438 t/d; 5th–95th percentile 424–453 t/d.",
  [{ text: "P(≥ 450 t/d) = 9.9 %", bold: true, color: C.accent4 }, { text: ": the point design is fragile." }],
  "Main cause: the hot-charge saving is a vendor rule, not a plant measurement.",
], "F8. Distribution of C1 production under input uncertainty.");

figWide("Which input drives production the most", "F9_tornado.png", 2.5, [
  ["Hot-charge saving", "Halving it costs 23 t/d (432 → 455 t/d). The largest single uncertainty."],
  ["SEC and load factor", "±2 % on SEC swings 20 t/d; LF 0.95–0.98 swings 14 t/d."],
  ["Power factor", "Staying at 0.93 gives 445 t/d: the target fails."],
], "F9. Tornado of C1 production. Source: results/model/I2_tornado.csv.");

s = content("Robust design: verify the saving, then preheat to ≈ 610 °C");
{ const { w, h } = fit(1.61, 7.6, YMAX - Y0); s.addImage({ path: FIG("F11_robust_optimisation.png"), x: X0, y: Y0 + (YMAX - Y0 - h) / 2, w, h, altText: "Robust optimisation", objectName: "figure" }); }
s.addTable(tbl([
  ["Saving uncertain (0.035–0.070)", "670", "925", "9.8 %"],
  ["Verified ≈ 0.070 by plant trial", "520", "610", "38.7 %"],
  ["Verified ≈ 0.0525 (75 %)", "670", "780", "2.6 %"],
], ["Case", "T for P50 (°C)", "T for P90 (°C)", "P at 500 °C"]), {
  x: 8.4, y: Y0, w: 4.33, colW: [1.69, 0.88, 0.88, 0.88], fontSize: 12, color: HEX.dk1, fontFace: "Calibri",
  border: { type: "solid", pt: 0.5, color: "D9DCE0" }, valign: "middle", margin: [0.04, 0.06, 0.04, 0.06], fill: { color: HEX.lt1 },
});
bullets(s, [
  "With the saving uncertain, no practical preheat temperature is robust.",
  [{ text: "A plant trial that confirms the vendor saving makes C1 robust at ≈ 610 °C.", bold: true }],
], { x: 8.3, y: 4.4, w: 4.43, h: 2.3, fontSize: 14 });
s.addNotes("Chance-constrained optimisation. Source: results/model/I2_robust_optimisation.csv.");

// ---------- Section D: sensitivity ----------
section("Sensitivity analysis", "Chapter 16: effect of each assumption on NPV and on the plant systems");

figWide("Tornado: which assumptions move the NPV", "F12_npv_tornado.png", 2.05, [
  ["Alloy price", "Swing R1 159 M; NPV stays positive down to US$734/t."],
  ["Hot-charge saving", "Swing R761 M. Also fails the 450 t/d target when halved."],
  ["Capital and electricity", "Weak effects: capex must reach about R1 620 M for NPV = 0."],
], "Base NPV R1 479 M (15 years, 12 %). Octave check agrees to 2e-15.", 3.6);

figSide("Spider plot: market inputs dominate, operating inputs matter", "F13_npv_spider.png", 1.52, [
  "Steepest lines: alloy price and exchange rate.",
  "Load factor and power factor together swing NPV by more than R550 M.",
  [{ text: "NPV is positive in every case tested.", bold: true, color: C.accent3 }],
], "F13. NPV against percentage change in each input.");

figWide("Electrical response: no headroom below PF 0.95", "F14_electrical_sensitivity.png", 2.44, [
  ["Transformer loading", "60 MW mean reaches 65 MVA exactly at PF 0.95; PF 0.92 gives 103 %."],
  ["Mean power", "At PF 0.93 even LF 0.99 does not reach 60 MW mean."],
  ["Implication", "PF correction and uptime are both design requirements, not options."],
], "F14. Left: on-load MVA against PF. Right: mean power against LF.", 3.6);

figWide("Auxiliary response: upgrade unless spare capacity ≥ 28 %", "F15_auxiliary_sensitivity.png", 2.44, [
  ["Utilisation", "At a 10 % design margin, auxiliaries run at 105 % for C1."],
  ["Threshold", "Only a margin of 28 % or more keeps utilisation ≤ 90 %."],
  ["Action", "Survey actual capacities; the R30 M allowance is essential."],
], "F15. Left: utilisation against production. Right: off-gas and slag duty.", 3.6);

s = content("Comparison: economically robust, technically at the limit");
const yes = { text: "Yes", options: { color: HEX.accent3, bold: true } }, no = { text: "No", options: { color: HEX.accent4, bold: true } };
s.addTable(tbl([
  ["Base case C1", "454.8", yes, "105 %", "1 479", "68.7 %", "1.46"],
  ["Hot-charge saving halved", "432.1", no, "100 %", "718", "40.7 %", "2.44"],
  ["Load factor stays 0.95", "444.5", no, "103 %", "1 231", "59.6 %", "1.68"],
  ["Power factor stays 0.93", "445.2", no, "103 %", "1 249", "60.2 %", "1.66"],
  ["Alloy price US$1 200/t", "454.8", yes, "105 %", "900", "47.4 %", "2.10"],
  ["Capital cost +40 %", "454.8", yes, "105 %", "1 339", "50.3 %", "1.98"],
  ["Ore rate 2.39 t/t (78 % recovery)", "454.8", yes, "105 %", "1 403", "65.9 %", "1.52"],
], ["Case", "Production (t/d)", "≥ 450 t/d", "Aux. use", "NPV (R M)", "IRR", "Payback (y)"]), {
  x: X0, y: Y0, w: W, colW: [3.9, 1.5, 1.2, 1.2, 1.5, 1.33, 1.5], fontSize: 14, color: HEX.dk1, fontFace: "Calibri",
  border: { type: "solid", pt: 0.5, color: "D9DCE0" }, rowH: 0.5, valign: "middle", margin: [0.05, 0.1, 0.05, 0.1], fill: { color: HEX.lt1 },
});
s.addText("Three single deviations each fail the 450 t/d target, while NPV stays positive: the production target, not the economics, binds the design.", { x: X0, y: 5.75, w: W, h: 0.8, fontSize: 16, bold: true, color: C.accent1, margin: 0, isTextBox: true, valign: "middle" });
s.addNotes("Source: results/model/CH16_comparison.csv. Auxiliary utilisation assumes a 10 % design margin (A-22).");

// ---------- Section E: verification and dashboard ----------
section("Verification and dashboard", "How we know the numbers are right, and how they are presented");

s = content("Every result was reproduced independently");
stat(s, X0, Y0, 2.85, 2.3, "104/104", "Increment 1 electrical values match MATLAB/Octave", C.accent3);
stat(s, X0 + 3.09, Y0, 2.85, 2.3, "18/18", "Mass balance and optimum match MATLAB/Octave", C.accent3);
stat(s, X0 + 6.18, Y0, 2.85, 2.3, "47/52", "Team numbers reproduced; 5 traced to audit findings", C.accent5);
stat(s, X0 + 9.27, Y0, 2.86, 2.3, "2e-15", "Relative NPV difference, Python against Octave", C.accent3);
bullets(s, [
  "157 model inputs, each tagged with its provenance (measured, supplied, assumed, literature, proposed).",
  "7 automated tests on the model package; all pass.",
  "The 5 unreproduced numbers come from the 60 MW on-load reading (S-O60), not from arithmetic errors.",
  "Estimates (electrode current, voltage, current density) are flagged wherever shown (AF-08).",
], { x: X0, y: 4.2, w: W, h: 2.5, fontSize: 18 });
s.addNotes("Sources: results/model/I1_crossval.csv, I2_crossval.csv, I1_verification.csv, CH16_python_npv.csv and CH16_octave_npv.csv.");

s = content("Power BI dashboard: five pages, one per engineering question");
const pages = [["PBI_page1_overview.png", "1 Baseline vs C1"], ["PBI_page2_electrical.png", "2 Electrical loading"], ["PBI_page3_massbalance.png", "3 Mass balance"], ["PBI_page4_optimisation.png", "4 Optimisation"], ["PBI_page5_verification.png", "5 Verification"]];
const pw3 = (W - 0.6) / 3, ph3 = pw3 / 1.78;
pages.forEach((p, i) => {
  const row = i < 3 ? 0 : 1, col = i < 3 ? i : i - 3;
  const x = row === 0 ? X0 + col * (pw3 + 0.3) : X0 + (pw3 + 0.3) / 2 + col * (pw3 + 0.3);
  const y = Y0 + row * (ph3 + 0.55);
  s.addImage({ path: FIG(p[0]), x, y, w: pw3, h: ph3, altText: `Power BI page ${p[1]}`, objectName: `pbi ${i + 1}` });
  s.addText(p[1], { x, y: y + ph3 + 0.05, w: pw3, h: 0.35, fontSize: 13, bold: true, color: C.text1, align: "center", margin: 0, isTextBox: true });
});
s.addNotes("Mock-ups rendered from SAF_PowerBI_Dataset.xlsx (15 tables). The build guide gives the visuals, fields and DAX measures for each page.");

// ---------- Conclusions ----------
pres.addSection({ title: "Conclusions" });
current = "Conclusions";
s = pres.addSlide({ masterName: "SECTION", sectionTitle: "Conclusions" });
s.addText("Conclusions and next steps", { x: 0.7, y: 0.5, w: 11.9, h: 0.9, fontSize: 36, bold: true, color: C.background1, fontFace: THEME.headFontFace, margin: 0, isTextBox: true });
[["C1 is the right design", "60 MW mean (PF 0.95, LF 0.972) on the existing 65 MVA transformers, plus hot charging, gives 455 t/d."],
 ["It is worth doing", "NPV R1 479 M, IRR 68.7 %; positive in every sensitivity case."],
 ["It is not yet robust", "P(≥ 450 t/d) is only 9.9 % while the hot-charge saving is unverified."]].forEach((c, i) => {
  const y = 1.7 + i * 1.15;
  s.addShape(pres.shapes.OVAL, { x: 0.7, y: y + 0.05, w: 0.5, h: 0.5, fill: { color: C.accent1 }, line: { type: "none" }, objectName: "marker" });
  s.addText(String(i + 1), { x: 0.7, y: y + 0.05, w: 0.5, h: 0.5, fontSize: 16, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addText([{ text: c[0], options: { bold: true, breakLine: true, fontSize: 18 } }, { text: c[1], options: { fontSize: 15 } }], { x: 1.45, y, w: 5.2, h: 1.05, color: C.background1, valign: "top", margin: 0, isTextBox: true });
});
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.0, y: 1.6, w: 5.73, h: 3.25, fill: { color: C.text1 }, line: { color: C.accent1, width: 1.5 }, rectRadius: 0.08, objectName: "next steps" });
s.addText("Before capital release", { x: 7.3, y: 1.75, w: 5.2, h: 0.5, fontSize: 18, bold: true, color: C.accent1, margin: 0, isTextBox: true });
s.addText([
  { text: "Plant trial to measure the hot-charge saving", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
  { text: "Power-quality metering to confirm PF 0.95", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
  { text: "Availability plan to reach LF ≥ 0.972", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
  { text: "Survey of actual auxiliary capacities", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
  { text: "Design the preheater for about 610 °C", options: { bullet: true } },
], { x: 7.3, y: 2.35, w: 5.2, h: 2.75, fontSize: 15, color: C.background1, valign: "top", margin: 0, isTextBox: true });
s.addNotes("Close on the decision: approve C1 subject to the plant trial on hot charging.");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
