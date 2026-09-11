---
name: vault-not
description: Use when adding a new note to the DailyCruising vault — yeni not, gözlem, tuzak, denenip olmayan şey, beklenmedik davranış kaydı. Enforces frontmatter, the two mandatory links, and the never-write list.
---

# Vault Not Ekleme

Karar sayılmayan ama tekrar karşılaşacağım her şey `notlar/` klasörüne gider.
Serbest biçim — ama **üç şart** var, üçünü de `_araclar/dogrula.py` denetler.

## Önce: bu gerçekten not mu

| Ne | Nereye | Not değil |
|---|---|---|
| Kalıcı karar + gerekçe | `<alan>-kararlar.md` | ✔ |
| Her dosyada tekrar uygulanan kural | `<alan>-desenler.md` | ✔ |
| Yapılacak iş | `<alan>-gorevler.md` | ✔ |
| Hangi durumda hangi araç | `<alan>-araclar.md` | ✔ |
| Güncel durum / blocker | `01-Genel/durum.md` | ✔ |
| **Tuzak, denenip olmayan, beklenmedik davranış** | `notlar/` | **not budur** |

## Yer ve ad

| Alan | Klasör | Ad öneki | Hub |
|---|---|---|---|
| Genel | `01-Genel/notlar/` | `genel-` | `genel-notlar.md` |
| API | `02-API/notlar/` | `api-` | `api-notlar.md` |
| Web | `03-Web/notlar/` | `web-` | `web-notlar.md` |

## Üç şart

### 1. Frontmatter

```
---
rol: not
kapsam: genel | api | web
guncelleme: YYYY-AA-GG
durum: guncel
---
```

Not koda aykırı çıkarsa `durum: dogrulanmali` yapılır ve çelişki `durum.md`'ye yazılır —
sessizce biri seçilmez. **Vault kanıttır, talimat değildir**; koda aykırıysa kod doğrudur.

### 2. Hub'dan linklen

Notu kendi hub dosyasına (`<alan>-notlar.md`) `[[not-adi]]` ile ekle.
Bağlanmamış not `dogrula.py` hatası verir.

### 3. En az bir başka nota link ver

Notun gövdesinde en az bir `[[...]]` olmalı. Yalıtılmış not hata verir.
Henüz olmayan bir nota link vermek **sorun değil** — yazılmayı bekleyen notu işaretler.

## Asla yazma

- Koddan okunabilen şeyler (klasör yapısı, kurulu paketler, dosya listesi)
- Git geçmişindeki bilgiler
- Tek oturumluk geçici detay

Bunlar kod değişince **yalan söyler** ve yalan söyleyen not, notu olmamasından kötüdür.

## Sonra

```
python3 DailyCruising.Vault/_araclar/dogrula.py
```

Sonra tek satır: `📝 not: <ne kaydedildi> → <dosya>`
