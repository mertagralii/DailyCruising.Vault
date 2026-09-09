---
rol: not
kapsam: web
guncelleme: 2026-09-08
durum: guncel
---

# Enum sözlüğü şemadan üretilemiyordu — ölçüldü, bildirildi, düzeldi

Uç anahtarı → Türkçe etiket sözlükleri (`Open → Açık`, `Paid → Ödeme alındı`)
elle yazılıyor ve bu **doğru olan**. "Elle yazılan her tablo bir gün ayrışır,
şemadan üret" önerisi makul duruyor ama ölçüldüğünde iki ayrı sebeple çöküyor.

## Ölçüm (2026-09-07)

```
components.schemas içinde `enum` taşıyan şema sayısı: 0
SupportTicketStatus -> {"type": "integer"}
SupportPriority     -> {"type": "integer"}
ReservationStatus   -> {"type": "integer"}
ReviewStatus        -> {"type": "integer"}
```

**1. Üretilecek değer yok.** Hiçbir şemada `enum` dizisi yok; belge
`Open`/`Answered` gibi değerlerin varlığından habersiz. Üreteç çalıştırılsa
boş bir sözlük çıkardı.

**2. Daha kötüsü: şema `integer` diyor, tel `string` gönderiyor.**
Sunucu enum'ları `JsonStringEnumConverter` ile yazıyor (`"status":"Answered"`)
ama OpenAPI belgesi dönüşümü yansıtmıyor. `uretilen.ts` bu yüzden
`ReservationStatus: number` yazıyor — telde hiçbir zaman görülmeyen bir tip.

Yani şemadan üretmek yalnız işe yaramamakla kalmaz, **çalışan elle yazılmış
`string` tiplerini yanlış olanla değiştirirdi.**

## Bugün bizi ne kurtardı

`uretilen.ts` başlığındaki kural: *"Yanıt tipleri BURADA YOK; elle yazılanlar
`src/lib/api/types/` altında."* Üretilen dosyadan yalnız **istek** tipleri
alınıyor (`booking.ts:12-13`), yanıt tipleri hiç. Kural konurken sebebi
"şemada yanıt yok" idi -> [[web-elle-yazilan-tip-yalan-soyler]]; bugün ikinci
bir sebebi olduğu görüldü — şemada olan enum bilgisi de yanlış.

## Doğru kaynak

Anahtarlar **backend kaynak kodundan** ölçülüyor, `openapi.json`'dan değil:
`Domain/Support/Support.cs`, `Domain/Reservations/Enums.cs`,
`Application/Support/SupportService.Categories`.

⚠️ Sözlükte olmayan anahtar `?? ham` ile ham geçiyor, gizlenmiyor:
**uydurma anahtar sessiz, eksik anahtar görünür.** Eksik anahtar ekrana
İngilizce basılır ve ilk bakan fark eder; uydurulan anahtar ise hiçbir zaman
ekrana uğramaz -> [[web-mock-hatayi-gizler]] ile aynı aile: görünmeyen kusur,
görünen kusurdan pahalıdır.

## Düzeldi — aynı gün (2026-09-07)

Ölçüm backend'e iletildi, kusur kabul edildi ve kapatıldı (`1865dbe`).
Değerler `Enum.GetNames`'ten yazdırılıyor, elle listelenmiyor:

```
enum dizisi taşıyan şema: 0 → 29
ReservationStatus: {"type":"integer"}
  → {"enum":["Pending","Paid",...,"Refunded"],"type":"string"}
```

**Notun iki gerekçesi de artık geçersiz** ve bu, notun yanlış olduğu anlamına
gelmiyor: ölçüm doğruydu, ölçülen şey değişti. Not duruyor çünkü asıl değeri
sonucu değil, **öneriyi ölçmeden kabul etmemenin** kaydı.

## Bugünkü kural

Anahtarlar üretilen belgeden **sınanıyor**, metinler elle yazılıyor:

```ts
export const TEKNE_DURUMU = {
  Draft: "Taslak", Published: "Yayında", Inactive: "Pasif",
} satisfies Record<BoatStatus, string> as Sozluk;
```

`satisfies` eksik **ve** uydurma anahtarı derleme hatası yapıyor; `as Sozluk`
çağıran tarafı gevşek bırakıyor, yani `?? ham` çalışma zamanı koruması
duruyor. Sunucu bir gün tipin imkânsız dediği bir değer gönderirse ekran boş
hücre değil ham anahtar basmalı.

⚠️ **Kapı takılır takılmaz üç canlı kusur çıktı** — hiçbiri `tsc`'ye
görünmüyordu: `TEKNE_DURUMU` `Inactive`'i kaçırıyordu (üç kopyadan biri
ayrışmıştı), `SATIS_MODU` `Exclusive` diyordu (`ExclusiveOpen` olacaktı),
`KUPON_RED_METNI` `NotYours`u taşımıyordu — sonuncusu panelde değil,
**müşterinin rezervasyon akışında**.

## Zincir üç halkalı, ikisi otomatik

```
enum  → belge   backend'in testi (e0c53ac) — enum'a değer eklenip belge
                üretilmezse ORADA kırılıyor, bayat belge bize hiç gelmiyor
belge → tip     `npm run build` → `tip-uret --kontrol` (5c04112)
tip   → sözlük  `satisfies Record<Enum, string>` (7d49d26)
```

### ⚠️ Zincirin dışında kalan dördüncü halka: **belge ≠ tel**

2026-09-08'de ölçüldü. Backend `isInternal` alanını commit'ledi, `openapi.json`
güncellendi, ben tipleri üretip ekranı yazdım — **ama çalışan API o commit'ten
önce başlatılmıştı ve alan telde yoktu.** Dört mesajın dördünde de anahtar hiç
dönmüyordu.

Sonuç: kod `undefined` görüp rozeti hiç basmayacaktı ve ekran **sessizce eski
hâlinde** kalacaktı. Derleme temiz, tipler doğru, kapı yeşil.

```
enum/sayı → belge : backend testi        ✅ otomatik
belge     → tip   : tip-uret --kontrol   ✅ otomatik
tip       → sözlük: satisfies            ✅ derlemede
belge     → TEL   : —                    ❌ hiçbir şey ölçmüyor
```

⚠️ **`--kontrol` belgeyi denetliyor, çalışan sunucuyu değil.** `openapi.json`
telden **ileri** olabiliyor: dosya yeniden üretildiği an güncelleniyor, uç ise
ancak süreç yeniden başlatılınca. Aradaki pencerede tip doğru, ekran yanlış.

**Bugünkü azaltma süreçsel:** backend alan eklediğinde restart'ı da yaptığını
ayrıca bildiriyor. Kod tarafında karşılığı yok ve aranmadı — zorunlu alanın
yokluğunu çalışma zamanında denetlemek her yanıtta bedel demek, üstelik
üretimde bu pencere hiç oluşmuyor (dağıtım tek adım).

⚠️ Bu, *"elle yazılan tip yalan söyler"* sınıfının **tersi**: tip doğru,
**sunucu** geride → [[web-elle-yazilan-tip-yalan-soyler]]

⚠️ **Kalan boşluk bilerek açık:** backend belgeyi ürettikten sonra biz
`tip-uret` çalıştırana kadar eski birleşimle derliyoruz. `--kontrol` bunu
`build` anında yakalıyor, yani boşluk bir derleme kadar. Tamamen kapatmanın
tek yolu her derlemede kardeş repoyu okumak olurdu ve o, iki repoyu
birbirine bağlardı. Bu aralıkta ekranı koruyan şey `?? ham`.

## Sırada: yanıt tipleri

Aynı düzeltme ikinci bir kapıyı da açtı. Not yazıldığında `openapi.json`
**hiçbir** işlem için yanıt şeması taşımıyordu; bugün **129 işlem** taşıyor.
Yani elle yazılan yanıt tiplerinin gerekçesi de büyük ölçüde ortadan kalktı
-> [[web-elle-yazilan-tip-yalan-soyler]]. Bu ayrı ve büyük bir iş; ölçüldü,
yapılmadı -> [[web-gorevler]].

⚠️ **Sayıyı iki kez yanlış söyledim, ikisi de aynı sebepten.** Üreteç
*"yanıt şeması olan işlem: 183/184"* basıyor ve ben onu aktardım — oysa kendi
ölçümüm aynı gün **129** demişti. 183, herhangi bir yanıtında şema olanı
sayıyor: `400`'ün `ApiError`'ı da dahil. **Tip üretilebilecek uç sayısı 129**;
kalan 55 `204` dönüyor ve `204` tanımı gereği gövdesiz. Ders: bir sayı ölçtükten
sonra **başka bir aracın sayısını aktarmak**, ölçümü hiç yapmamaktan kötüdür —
iki sayı da elde varken hangisinin ne saydığı sorulmadı.
