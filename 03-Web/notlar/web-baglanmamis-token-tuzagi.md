---
rol: not
kapsam: web
guncelleme: 2026-08-26
durum: guncel
---

# Temaya bağlanmamış token sessizce sıfır üretir

`globals.css` içinde iki ayrı katman var ve **birinde tanımlı olmak yetmiyor**:

1. `:root` — ham tasarım token'ları (`--r-circle: 50%`)
2. `@theme inline` — Tailwind'in sınıf üreteceği eşlemeler (`--radius-circle: var(--r-circle)`)

2026-08-26'da `rounded-circle` sınıfını beş yerde kullandım. `--r-circle`
`:root`'ta vardı ama `@theme inline` içine **hiç bağlanmamıştı**. Tailwind
bilmediği bir sınıf için kural üretmez; sınıf DOM'da durur, `border-radius`
`0px` kalır. Daireler kare çıktı.

## Neden yakalanmadı

- `npm run build` → temiz. Bilinmeyen yardımcı sınıf derleme hatası değil.
- `npm run lint` → temiz. ESLint sınıf adını denetlemez.
- Tip denetimi → temiz. Sınıf sadece bir string.

Yalnız ekran görüntüsünde görüldü. Bu, [[web-tailwind-katman-tuzagi]] ile aynı
aileden: **stil katmanı hatası, kod katmanı denetimlerinden geçer.**

## Kural

Yeni bir `rounded-*`, `shadow-*`, `text-*`, `bg-*` sınıfı yazmadan önce
karşılığının `@theme inline` içinde olduğuna bak. Ham token'ın `:root`'ta olması
o sınıfın çalışacağı anlamına **gelmez**.

Hızlı denetim — sınıf gerçekten bir şey üretmiş mi:

```js
getComputedStyle(document.querySelector('[class*="rounded-circle"]')).borderRadius
// "0px" → sınıf ölü
```

Aynı yöntem her yardımcı sınıf için çalışır: sınıfı taşıyan öğede hesaplanmış
değeri oku, beklenenle karşılaştır.

İlgili: [[web-notlar]] · [[web-tailwind-katman-tuzagi]] · [[web-olcum-yanlis-pozitifleri]] · [[web-desenler]]
