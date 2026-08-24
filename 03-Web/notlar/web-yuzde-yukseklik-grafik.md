---
rol: not
kapsam: web
guncelleme: 2026-08-22
durum: guncel
---

# Yüzdelik yükseklikli çubuk grafik görünmez çıkıyor

Yönetim panelindeki "Aylık ciro" grafiğinde **çubuklar hiç görünmedi**; yalnızca
değer ve ay etiketleri vardı.

## Sebep

Yapı şöyleydi:

```
<div class="flex h-36 items-end">        ← sabit yükseklik BURADA
  <div class="flex flex-col">            ← sütun: otomatik yükseklik
    <span>4.82</span>                    ← etiket
    <div style="height: 100%">           ← çubuk: NEYİN %100'ü?
    <span>Ağu</span>                     ← etiket
```

Çubuğun yüzdesi, sabit yükseklikli kabın değil **otomatik boyutlanan sütunun**
yüzdesi olarak hesaplanıyor. Sütunun yüksekliği içeriğine göre belirlendiği için
yüzde çözümlenemiyor ve çubuk sıfır yükseklikte kalıyor.

## Düzeltme

Sabit yüksekliği çubuğun **doğrudan kabına** ver, etiketleri o kabın dışında bırak:

```
<div class="flex flex-col">
  <span>4.82</span>
  <div class="flex h-32 items-end">      ← sabit yükseklik ÇUBUĞUN KABINDA
    <div style="height: 100%">           ← artık çözümleniyor
  </div>
  <span>Ağu</span>
```

Ayrıca `Math.max(4, yüzde)` eklendi: çok küçük değerler tamamen kaybolmasın.

## Ders

CSS'te yüzdelik yükseklik, **en yakın belirlenmiş yükseklikli ataya** göre çözülür.
Araya otomatik yükseklikli bir kap girerse yüzde sessizce çalışmaz — hata vermez,
sadece görünmez.

Aynı hata destek panelindeki haftalık grafikte de vardı; ekran görüntüsü almadan
fark edilmemişti. İki yerde birden düzeltildi.

İlgili: [[web-notlar]] · [[web-grid-row-span-tuzagi]] · [[web-mimari]]
