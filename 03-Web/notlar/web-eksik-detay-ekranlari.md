---
rol: not
kapsam: web
guncelleme: 2026-08-22
durum: guncel
---

# Eksik detay ekranları — "rota açılıyor" ≠ "sayfa bitti"

Tasarımdaki her liste tablosunun son sütununda **"Detay"** bağlantısı var ve bu
bağlantı ayrı bir ekran açıyor. İlk uygulamada yalnızca liste tabloları yazıldı,
detay ekranları atlandı. Kimse fark etmedi çünkü rota 200 dönüyordu.

## Ölçüm (2026-08-22)

| Ekran | Tasarım başlığı | Kodda | Eksik |
|---|---|---|---|
| `isAdmin` | 132 | 44 | **88** |
| `isOwnerPanelScreen` | 18 | 9 | 9 |
| `isAccount` | 13 | 10 | 3 |
| `isSupportPanel` | 4 | 2 | 2 |
| `isDetail` | 3 | 0 | 3 |

## Nasıl ölçülür

Tasarımda bölüm başlıkları `font-size:20px` (ve detay başlıkları `26px`) ile
yazılmış. Başlıkları çıkarıp `src/` içinde aramak yeterli:

```
grep -o 'font-size:2[0-9]px[^"]*"[^>]*>[^<]\{3,60\}' Rihtim.dc.html | sed 's/.*>//'
```

Marka değişikliğinden gelen yanlış pozitiflere dikkat: tasarımda "Rıhtım" geçen
metinler kodda "Daily Cruising" → [[web-kararlar]]

## Filtre çubukları da atlanmıştı

Tasarımda her tablonun üstünde arama + açılır seçim + "Filtrele" / "Temizle" var.
Kodda panellerde **sıfır** `input` vardı; bu da aynı sebeple görülmemişti.

İlgili: [[web-notlar]] · [[web-kararlar]] · [[durum]]
