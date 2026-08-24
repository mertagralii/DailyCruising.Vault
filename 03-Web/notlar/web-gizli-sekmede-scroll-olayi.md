---
rol: not
kapsam: web
guncelleme: 2026-08-22
durum: guncel
---

# Gizli sekmede scroll olayı da yayınlanmıyor

Header'ın kaydırınca beyaza dönmesini test ederken `window.scrollTo(0, 600)` çağırdım;
`scrollY` 600 oldu ama header şeffaf kaldı. "Hook bozuk" gibi göründü.

## Ölçüm

```js
let sayac = 0;
window.addEventListener('scroll', () => sayac++);
window.scrollTo(0, 600);
// sayac: 0   ← kendi dinleyicim bile tetiklenmedi
// scrollY: 600
// document.hidden: true
```

Gizli sekmede Chrome **scroll olaylarını yayınlamıyor**; konum değişiyor ama olay
gelmiyor. [[web-animasyon-gizli-sekme]] ile aynı sınıf bir ölçüm hatası.

## Doğru test yöntemi

Olayı elle tetikle:

```js
window.scrollTo(0, 600);
window.dispatchEvent(new Event('scroll'));
```

Böyle yapınca header beklendiği gibi `#FFFFFF` zemine, `#E7E6E6` kenarlığa ve üst
şerit `#10201C`'ye döndü — yani mantık doğruydu.

## Ders

Otomasyon sekmesi gizli çalışıyor. **Olay tabanlı hiçbir davranış** (scroll, resize,
animasyon, IntersectionObserver) orada kendiliğinden tetiklenmez. Bozuk sanmadan önce
`document.hidden` kontrol et.

İlgili: [[web-notlar]] · [[web-animasyon-gizli-sekme]] · [[web-mimari]]
