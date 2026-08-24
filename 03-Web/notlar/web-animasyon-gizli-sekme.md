---
rol: not
kapsam: web
guncelleme: 2026-08-21
durum: guncel
---

# Gizli sekmede CSS animasyonları duraklar — yanlış hata teşhisi

Açılış perdesini (preloader) ekledikten sonra ölçtüm: 2,2 saniye beklememe rağmen
hero içeriği `opacity: 0` idi ve perde hâlâ DOM'daydı. "Animasyon bozuk" gibi görünüyordu.

## Gerçek sebep

```js
document.getAnimations()[0].playState   // "running"
document.getAnimations()[0].currentTime // 0   ← hiç ilerlememiş
document.visibilityState                // "hidden"
```

Chrome, **gizli sekmelerde CSS animasyonlarını duraklatır.** Tarayıcı otomasyonuyla
açılan sekme odakta olmadığı için animasyon başlamamıştı. Ürün hatası değil,
ölçüm ortamının etkisi.

## Doğru test yöntemi

Bitiş durumunu görmek için animasyonları zorla bitir:

```js
document.getAnimations().forEach(a => a.finish());
```

Sonra `getComputedStyle` ile son durumu kontrol et. Böyle yapınca hero `opacity: 1`,
`transform: none` çıktı — doğruydu.

## Bu arada bulunan gerçek kırılganlık

`animation-fill-mode: both` kullanan bir açılış efektinde içerik başlangıçta
`opacity: 0`. Animasyon hiç çalışmazsa içerik **kalıcı olarak görünmez** kalır.
Sekme görünür olunca Chrome animasyonu başlattığı için gerçek kullanıcıda sorun yok,
ama bu desen kullanılırken akılda tutulmalı.

Ayrıca: perdenin `onAnimationEnd` ile temizlenmesi, animasyon React hidrasyonundan
**önce** biterse hiç tetiklenmez. Bileşene 2 sn'lik `setTimeout` emniyet ağı eklendi.

İlgili: [[web-notlar]] · [[web-mimari]] · [[web-tailwind-katman-tuzagi]]
