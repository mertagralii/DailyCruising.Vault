---
rol: not
kapsam: web
guncelleme: 2026-08-22
durum: guncel
---

# Ölçüm karşılaştırmasında gerçek olmayan farklar

Tasarımla uygulamayı yan yana ölçerken ([[web-tasarimi-tarayicida-acmak]]) her fark
gerçek fark değil. Aşağıdakiler **tekrar tekrar** çıkıyor; her sayfada yeniden
araştırmamak için burada.

## 1. `position:fixed` tasarımda sayfa dibinde görünür

Çerez bandı tasarımda `position:fixed;bottom:0`. Ölçümde `y=2327` çıkıyor
(sayfa dibi), uygulamada `y=681` (görüntü alanı dibi). **Uygulama doğru olan.**

Sebep: tasarım tuvali içeriği `transform`'lu bir kapsayıcıda basıyor; `transform`
`fixed` için yeni bir içerme bloğu kuruyor, öğe görüntü alanına değil kapsayıcıya
sabitleniyor. Bandın dört metni de (`Kabul et`, `Reddet`, …) bu yüzden kayık çıkar.

## 2. `{{ }}` ara değeri kendi blok span'ine sarılıyor

`{{ b.discount }} indirim` tasarımda şuna dönüşüyor:

```html
<span style="font-size:13px">%</span><span class="sc-interp">15</span> indirim
```

`sc-interp` **`display:block`** → esnek kutuda ayrı bir öğe → `%` ile sayı arasında
**ve** sayı ile "indirim" arasında ayrı 6px boşluk. React'te `{x} indirim` yazılırsa
sayı ile metin tek anonim öğe olur ve rozet **3px dar** çıkar.

Karşılığı: sayıyı `<span className="block">` içine almak.

## 3. Marka adı genişliği başlık hizasını kaydırıyor

"Rıhtım" 62px, "Daily Cruising" 131px. Header esnek yerleşim olduğu için menü
bağlantıları ~6px, arama kutusu ~69px kayıyor ve kutu 300px yerine ~225px kalıyor.
**Kabul edilen fark** — marka adı bilinçli olarak farklı.

## 4. Gerçek form alanları metin düğümü üretmez

`<select>` / `<input>` kullanıldığı için tasarımın statik kutularındaki yazılar
(`22.08.2026`, `gg.aa.yyyy`, `₺4.500`, `Tekne veya bölge ara`) ölçümde **eksik**
görünür. Değerler `fields` dizisinde ayrıca toplanıyor; oradan doğrulanmalı.

## 5. Tarayıcı varsayılanları

| Ölçümde | Gerçek |
|---|---|
| Buton dolgusu `1px 6px` → `0` | Tailwind preflight sıfırlıyor, kutu ölçüsü aynı |
| `border-radius: 50%` → `16777216px` | `rounded-full`; kare öğede görsel olarak aynı. Yine de `rounded-[50%]` yazmak farkı bitirir |
| Gölge zinciri saydam parçalar | Tailwind `--tw-shadow` zinciri; saydamlar atılıp karşılaştırılmalı |

Ayrıca **aynı metin sayfada birden çok geçiyorsa** eşleştirici yanlış çifti kurar;
"fark" demeden önce tek tek doğrula.

İlgili: [[web-notlar]] · [[web-tasarimi-tarayicida-acmak]] · [[web-kararlar]]

## Marka adı uzunluğu satır sardırıyor (2026-08-23)

Hesabım ekranında istatistik kartındaki **"Daily Cruising puanı"** iki satıra
sarıyor; tasarımdaki **"Rıhtım puanı"** tek satır. Sayfa yüksekliği tam **18px**
fazla çıkıyor ve düzen hatası gibi görünüyor. Değil — marka adı daha uzun,
kart da dar. Metin düğümünün yüksekliğine bakmak yeter: 35 (iki satır) / 17.

Aynı sebeple footer telif satırı ve header marka bağlantısı da farklı genişlikte.

## Gövde satır yüksekliği: tekrar eden kök neden (2026-08-24)

`globals.css` gövdeye **26px sabit** satır yüksekliği veriyor, tasarım `normal`
kullanıyor. Açık `leading-` verilmeyen her küçük metin bizde şişiyor. Bugüne
kadar dört ayrı yerde aynı hata çıktı:

- tekne kartı satırları (13px) — satır başına 9px
- takvim gün başlığı (12px) ve hücre gün numarası (13px)
- yönetim tablosunda rozet hücresi (sınıfsız kalmıştı)

**Yeni bir metin öğesi yazarken:** tasarımda `line-height` yoksa bizde
`leading-[normal]` yazılmalı; boş bırakmak 26px miras almak demektir.
Global değeri değiştirmek tüm sayfaları etkilediği için yapılmadı → [[durum]]

