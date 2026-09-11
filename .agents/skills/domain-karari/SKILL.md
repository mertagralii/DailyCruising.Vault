---
name: domain-karari
description: Use when Mert answers a domain/business-rule question or a blocker gets resolved for DailyCruising — iş kuralı netleşti, domain sorusu cevaplandı, blocker çözüldü, şema kararı verildi. Keeps domain-gereksinimler, api-kararlar, durum.md and the task boards from drifting apart.
---

# Domain Kararı

Bir iş kuralı netleştiğinde **dört dosya birden** güncellenir. Biri atlanırsa vault
kendi kendiyle çelişir ve altı ay sonra hangisinin doğru olduğu bilinmez.

## Önce: cevap gerçekten net mi

Net değilse **çıkarım yapıp şema kurma.** `02-API/api-desenler.md` kuralı:
"Çıkarımla şema kurulmaz — kurulursa altı ay sonra 'Mert böyle demişti' diye anılır."

Cevap yarımsa: yazılanı `*(çıkarım)*` etiketiyle işaretle ve eksik parçayı
"Cevap bekleyenler" tablosunda **bırak**. Yarım cevabı tam gibi kaydetme.

## Dört adım — sırayla

### 1. `01-Genel/domain-gereksinimler.md`

- Kuralı tarihli başlık altına yaz (`### YYYY-AA-GG — <konu>`)
- Mert'in söylediği ile senin çıkarımın **ayrı** yazılır; çıkarım `*(çıkarım)*` etiketli
- Karşılanan soruyu "Cevap bekleyenler" tablosundan **düş**

### 2. `02-API/api-kararlar.md` — yalnız şemayı/kodu etkiliyorsa

Append-only. Eski giriş **silinmez**; karar değiştiyse yeni giriş açılır ve
"<tarih> kararını iptal eder" yazılır.

Zorunlu alanlar:

```
## YYYY-AA-GG — <karar başlığı>

**Karar:** ...

**Neden:** ...            <- boş bırakılırsa dogrula.py hata verir

**Alternatifler:** ... — neden elendiği
```

Kararı Mert verdiyse **"Karar (Mert)"** yaz. Sen önerdiysen bunu açıkça belirt —
`api-kararlar.md`'deki CORS girişi bunun örneği.

### 3. `01-Genel/durum.md`

- Blocker tablosundan çözülen satırı düş
- `guncelleme:` tarihini bugüne çek (7 günden eskiyse `dogrula.py` uyarır)
- **Tek otorite burasıdır.** "Nerede kaldık"ın cevabı oturum notunda değil burada yaşar

### 4. Görev panosu

Karar bir işi serbest bıraktıysa ilgili panoda görevi aç:
`02-API/api-gorevler.md` (`A-`) · `03-Web/web-gorevler.md` (`W-`) · `01-Genel/genel-gorevler.md` (`G-`)

- Kimlik numarası **geri kullanılmaz** — panodaki en büyük numaranın bir fazlası
- Bloke olan görevin `Bağımlı:` satırı varsa temizle
- Kabul ölçütü yaz; ölçütsüz görev "bitti" kararını yine bana bırakır

## Sonra

```
python3 DailyCruising.Vault/_araclar/dogrula.py
```

TEMIZ dönmeden iş bitmiş sayılmaz.

Sonra tek satır bildir: `📝 not: <ne kaydedildi> → <dosyalar>`

## Postgres taahhüdü

2026-08-22'de verilen söz: **Mert PostgreSQL'i hiç kullanmadı.** Kararın Postgres'e
özgü bir sonucu varsa (tırnak davranışı, `EXCLUDE` kısıtı, `DateTime` Kind zorunluluğu,
`daterange`) sessizce geçme — açıkla.
