---
rol: not
kapsam: web
guncelleme: 2026-08-21
durum: guncel
---

# `row-span` + `justify-end` = kartın üstünde beyaz boşluk

Tur kategorileri ızgarasında geniş kart `lg:col-span-2 lg:row-span-2` ile iki satır
kaplıyordu. Kart içi `flex flex-col justify-end` idi ve görsel alanına sabit
yükseklik (`h-64`) verilmişti.

**Sonuç:** kartın içeriği iki satırlık yüksekliği doldurmadığı için üstte belirgin
bir beyaz boşluk kaldı. Kart "bozuk" göründü.

**Düzeltme:** sabit yükseklik yerine esneme —

```
<div className={c.wide ? "min-h-64 flex-1" : "h-28 flex-none"}>
```

## Ders

Bir ızgara öğesi `row-span` ile uzatılıyorsa, içindeki bloklardan **biri**
`flex-1` olmalı; yoksa artan yükseklik boşluk olarak kalır. `justify-end`
boşluğu yok etmez, sadece yerini değiştirir.

**Nasıl yakalandı:** derleme ve lint temiz geçti; yalnızca ekran görüntüsünde
görüldü. Bölüm yüksekliklerini DOM'dan ölçmek (`getBoundingClientRect`) hangi
bölümün şiştiğini bulmayı hızlandırdı.

İlgili: [[web-notlar]] · [[web-mimari]] · [[web-tailwind-katman-tuzagi]]
