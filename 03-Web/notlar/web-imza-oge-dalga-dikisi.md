---
rol: not
kapsam: web
guncelleme: 2026-08-22
durum: guncel
---

# İmza öğe atlanmıştı: dalga dikişi

Tasarım projesinde `Rihtim.dc.html` dışında **ikinci bir dosya** var:
`Rihtim Foundations.dc.html`. Hedefte adı geçmediği için uzun süre okunmadı.
İçinde markanın **imza öğesi** tanımlıydı ve uygulamada hiç yoktu.

## Öğe

"Dalga dikişi" — dolu dalga kesimi yerine iki sıra kaydırmalı ince kavis.
18px adımda tekrarlayan yay dizisi:

```css
height: 16px;
background:
  radial-gradient(circle at 50% 100%, transparent 7px, RENK 7px, RENK 9px, transparent 9.5px)
    0 100%/18px 12px repeat-x,
  radial-gradient(circle at 50% 100%, transparent 7px, SOLUK 7px, SOLUK 9px, transparent 9.5px)
    9px 100%/18px 12px repeat-x;
```

Bölüm sınırlarında kullanılır: hero altı, kampanya bandı altı, footer üstü.
Tasarımın kendi ifadesi: *"Denizin ritmini veriyor, yüzeyi kapatmıyor."*

`src/components/ui/wave-stitch.tsx` olarak uygulandı.

## Nasıl kaçırıldı

Ana tasarım dosyasında desen **4 kez** geçiyordu ama inline `radial-gradient`
olarak; sayfa yapısını çıkarırken `style` niteliklerini attığım için görünmedi.
Yalnızca Temeller dosyası okununca fark edildi.

## Aynı dosyadan çıkan iki sapma daha

| Konu | Bendeki | Doğrusu |
|---|---|---|
| `--brand-ink-800` | `#22403A` | `#17302A` |
| `--brand-ink-700` | `#345048` | `#22403A` |
| Odak durumu | `outline` | Kenarlık `#D8366B` + `0 0 0 3px rgba(216,54,107,.16)` |

## Ders

Bir tasarım projesinde **hedefte adı geçmeyen dosya da olabilir.** `list_files`
çıktısındaki her dosyaya bakılmalı; "Foundations", "tokens", "README" gibi adlar
uygulamayı doğrudan etkileyen kural taşıyabiliyor.

Ayrıca: yapı çıkarmak için `style` niteliklerini atmak hızlı ama **görsel imzayı
görünmez kılıyor**. Dekoratif öğeler için stilleri de taramak gerek.

İlgili: [[web-notlar]] · [[web-mimari]] · [[web-yuzde-yukseklik-grafik]]
