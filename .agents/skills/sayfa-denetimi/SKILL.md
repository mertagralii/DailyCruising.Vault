---
name: sayfa-denetimi
description: Use when verifying a DailyCruising.Front-End page/screen against the design before calling it done — piksel denetimi, sayfa uygulandı mı, ekran kontrolü, W-01 tipi görev. Enforces the measure-desktop-then-mobile-then-count-sections order and blocks evidence-free "bitti" claims.
---

# Sayfa Denetimi

Bir ekranın "bitti" sayılabilmesi için izlenecek sıra. **Adım atlanmaz** —
2026-08-21'de "19/19 sayfa tamamlandı" denip 106 bölüm eksik çıkmasının sebebi
tam olarak bu sıranın atlanmasıydı.

## Ön koşul

1. `03-Web/web-desenler.md` + `03-Web/web-araclar.md` okundu mu? Okunmadıysa **önce oku.**
2. Görev panoda mı? `03-Web/web-gorevler.md` içinde ilgili görevi **Yapılıyor**'a taşı.
   Yapılıyor'da 3'ten fazla görev olamaz — varsa önce birini kapat.

## Adımlar

### 1. Tasarım kaynağını aç — yerel dosyadan

`r-ht-m-temeller-sayfas/project/` altındaki yerel dosya okunur.
**`DesignSync` MCP `get_file` kullanılmaz** — dosyanın yalnız %19,6'sını veriyor
(256 KiB kesme), eksik veriyle yapılan denetim yalan söyler.

### 2. Bölümleri say — ekranı değil

"Sayfa uygulandı" ölçütü **ekran sayısı değil bölüm sayısıdır.**
Tasarımdaki bölüm sayısını yaz, koddaki bölüm sayısını yaz, farkı yaz.
Sayılar eşit değilse sayfa **bitmemiştir**, ne kadar iyi görünürse görünsün.

### 3. Dev sunucusu

Körlemesine `npm run dev` açma — 3000 zaten dolu olabilir. `run` skill'i ya da
`lsof -i :3000` ile bak.

### 4. Masaüstü ölçüm — 1280

`chrome-devtools` MCP: `resize_page` → `take_snapshot` → `evaluate_script`.

⚠️ **`resize_page` sessizce başarısız olabiliyor.** Ölçüm almadan önce gerçek
genişliği `evaluate_script` ile doğrula (`window.innerWidth`). Doğrulanmamış
boyutta alınan ölçüm çöptür.

### 5. Mobil ölçüm — 390 (ve gerekirse 834)

`playwright` MCP `browser_resize`. **`chrome-devtools` 390px'e inemiyor** —
2026-08-23 mobil taraması bu yüzden Playwright ile yapıldı.

Bakılacaklar: yatay taşma, kırpılan metin, dokunma hedefi boyutu, sabit
genişlikli kutular.

### 6. Desen ihlali taraması

- Sabit renk kodu var mı? (`#`, `rgb(`) → token okunmalı: `bg-action`, `text-fg-secondary`, `border-line`
- Rota elle mi yazılmış? → `lib/routes.ts`
- Marka metni elle mi yazılmış? → `lib/brand.ts`
- `globals.css`'e element stili eklendiyse `@layer base` içinde mi?
- `slug` ile `label` karıştırılmış mı?

### 7. Build

`npm run build` + `npm run lint`.

⚠️ **Build temiz olması sayfanın doğru olduğunu göstermez.** 2026-08-23'te 6 görsel
tuzağı build kaçırdı, hata yalnız tarayıcıda görüldü. Build gerekli koşul, yeterli değil.

### 8. Panoya kanıt yaz

`03-Web/web-gorevler.md` içinde görevi Tamamlandı'ya taşı. `Kanıt:` satırı
**şu üçünü birden** içermeli:

- ölçülen genişlikler (1280 / 390)
- bölüm sayısı karşılaştırması (tasarım N / kod N)
- build ve lint sonucu

Bu üçünden biri eksikse görev kapanmaz. Kanıtsız görev `dogrula.py` hatası verir.

## Bitirmeden

Bu denetimde yeni bir tuzak gördüysem `03-Web/notlar/` altına `web-` önekli not aç,
`web-notlar.md` hub'ından linkle ve nottan en az bir başka nota link ver.
İki bağ da yoksa `dogrula.py` hata verir.
