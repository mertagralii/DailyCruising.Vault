// Sayfa parmak izi — tasarim ile uygulamayi ayni olcutlerle olcer.
// chrome-devtools MCP `evaluate_script` icine oldugu gibi yapistirilir.
async () => {
  await document.fonts.ready;
  document.getAnimations().forEach(a => { try { a.finish(); } catch (e) {} });
  window.scrollTo(0, 0);
  await new Promise(r => setTimeout(r, 400));
  const cv = document.createElement('canvas'); cv.width = cv.height = 1;
  const cx = cv.getContext('2d', { willReadFrequently: true });
  const cache = new Map();
  const norm = (c) => {
    if (!c) return c;
    if (cache.has(c)) return cache.get(c);
    cx.clearRect(0, 0, 1, 1); cx.fillStyle = c; cx.fillRect(0, 0, 1, 1);
    const d = cx.getImageData(0, 0, 1, 1).data;
    const v = `${d[0]},${d[1]},${d[2]},${d[3]}`;
    cache.set(c, v); return v;
  };
  // Tailwind saydam golge zincirini atar; kalan gercek golgeleri birlestirir
  const shadow = (v) => v === 'none' ? '' :
    v.split(/,(?![^(]*\))/).map(s => s.trim()).filter(s => !/^rgba\(0, 0, 0, 0\)/.test(s)).join(' | ');
  const texts = [], boxes = [];
  const walk = (el) => {
    for (const n of el.childNodes) {
      if (n.nodeType === 3) {
        const t = n.textContent.replace(/\s+/g, ' ').trim();
        if (!t) continue;
        const r = document.createRange(); r.selectNodeContents(n);
        const b = r.getBoundingClientRect();
        if (!b.width && !b.height) continue;
        const s = getComputedStyle(el);
        texts.push({ t, x: Math.round(b.left), y: Math.round(b.top + scrollY), w: Math.round(b.width), h: Math.round(b.height),
          fs: parseFloat(s.fontSize), fw: s.fontWeight, lh: s.lineHeight, ls: s.letterSpacing,
          tt: s.textTransform, c: norm(s.color), tag: el.tagName });
      } else if (n.nodeType === 1) {
        const s = getComputedStyle(n);
        if (s.display === 'none' || s.visibility === 'hidden') continue;
        const b = n.getBoundingClientRect();
        if (b.width || b.height) {
          const bg = s.backgroundColor, bi = s.backgroundImage;
          const bw = parseFloat(s.borderTopWidth) || 0;
          if ((bg && norm(bg) !== '0,0,0,0') || bi !== 'none' || bw > 0) {
            boxes.push({ tag: n.tagName, x: Math.round(b.left), y: Math.round(b.top + scrollY),
              w: Math.round(b.width), h: Math.round(b.height),
              bg: norm(bg), bi: bi === 'none' ? '' : bi.slice(0, 90), br: s.borderRadius,
              bd: bw ? `${bw}px ${norm(s.borderTopColor)}` : '',
              pad: `${s.paddingTop} ${s.paddingRight} ${s.paddingBottom} ${s.paddingLeft}`,
              sh: shadow(s.boxShadow) });
          }
        }
        walk(n);
      }
    }
  };
  walk(document.body);
  const fields = [...document.querySelectorAll('input,textarea,select')].map(e => { const b = e.getBoundingClientRect(); return {
    tag: e.tagName, type: e.type, ph: e.placeholder || '', val: e.value || '',
    x: Math.round(b.left), y: Math.round(b.top + scrollY), w: Math.round(b.width), h: Math.round(b.height) }; });
  return { vw: innerWidth, vh: innerHeight, pageH: document.documentElement.scrollHeight, texts, boxes, fields };
}
