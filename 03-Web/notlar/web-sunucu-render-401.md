---
rol: not
kapsam: web
guncelleme: 2026-09-12
durum: guncel
---

# Sunucu render'ında `401`: üç liste sessizce boşalıyor

⚠️ **Hipotez yanlış çıktı.** Not, hipotezi ve onu çürüten ölçümü birlikte
taşıyor — silinmedi, çünkü yanlış hipotezin nasıl çürütüldüğü, doğru
cevaptan daha öğreticiydi. Sonuç en altta.

## Ölçülen

Yönetim paneli açıkken tarayıcı konsolunda tekrar eden üç satır:

```
[panel] /api/platform/partners okunamadı: 401 Unauthorized
[panel] /api/support/tickets okunamadı: 401 Unauthorized
[panel] /api/platform/reviews okunamadı: 401 Unauthorized
```

Üçü de `lib/api/panel.ts` içindeki `liste()`'den geliyor, yani **sunucu
bileşeni render'ından** — `api(..., { yazabilir: false })`.

⚠️ **Bir kez "bayat kayıt" diye eleyip geçmiştim ve yanlıştı.** 2026-09-11
23:45'te konsolu temizleyip sayfayı yeniden yükledim, temiz çıktı ve
"giriş öncesinden kalma" diye kapattım. 00:17'de **yeniden çıktı**. Yani
ilk ölçüm doğruydu ama **sonucu yanlış genelledim**: bir kez temiz çıkması
tekrarlamayacağı anlamına gelmiyor.

## Aynı anda çalışan şey

Aynı oturumda **istemci** çağrıları başarılı: `PUT /api/platform/settings`
00:22'de `204` döndü, aktivite listesi 1264 kayıt okudu. Yani jetonun
kendisi ölü değil.

Fark, iki yolun çerez yenileme yeteneği:

| Yol | Jeton yenileyebiliyor mu |
|---|---|
| `src/proxy.ts` (rota kapısı) | **evet** — belge gezinmesinde |
| `src/app/api/dc/[...path]` (vekil) | **evet** — rota işleyicisi çerez yazabilir |
| `lib/api/client.ts` sunucu render'ı | **hayır** — `yazabilir: false` |

Üçüncüsü tasarım gereği: Next'te render sırasında `cookies().set()` hata
fırlatıyor. Kapı bunu telafi ediyor — `istegeYaz()` tazelenen jetonu
**aynı isteğin** render'ına geçiriyor (2026-08-28'de ölçülüp düzeltilmiş).

## Hipotez — doğrulanmadı

Kapı yalnız **belge gezinmelerinde** çalışıyor. Kapıdan geçmeyen bir
sunucu render'ı olursa (geliştirmede HMR yeniden derlemesi; üretimde
kapının eşleşmediği herhangi bir RSC yeniden render'ı) erişim çerezi o
arada ölmüşse **yenilenme şansı yok** ve üç liste `null` dönüyor.

Belirtinin 00:17'deki iki kümesi benim dosya kaydetmelerimin hemen
ardına denk geliyor; bu hipotezi **destekliyor ama kanıtlamıyor** —
zamanlamayı dev sunucusunun günlüğüyle karşılaştırmadım.

## Ayırt edici deney

1. Panelde otur, hiçbir şeye dokunma, erişim jetonunun ömrü (15 dk) dolsun.
2. **Gezinme yapmadan** sayfayı RSC yeniden render'ına zorla.
3. Üç `401` çıkıyorsa hipotez doğru; çıkmıyorsa sebep başka.

Üretimde HMR yok, yani geliştirmeye özgü olabilir — **ama bu da
ölçülmedi** ve "geliştirmeye özgüdür" demek şu an bir varsayım.

## Neden önemli

Belirti sessiz: üç modül **boş** görünüyor, hata kutusu **yok**.
`liste()` yakalayıp `null` dönüyor ve ekran "kayıt yok" basıyor.
Personel için *"hiç yat işletmesi yok"* ile *"liste okunamadı"* aynı
görünüyor — bu oturumda defalarca karşılaşılan **sıfırın üç anlamı**
kalıbının aynısı → [[web-desenler]]

⚠️ Kusur bu notta duruyor çünkü kod karşılığı **henüz belirsiz**: sebep
doğrulanmadan yazılacak bir düzeltme, olmayan bir hatayı düzeltir.

İlgili: [[web-notlar]] · [[web-durum]]

---

## 2026-09-12 · hipotez çürütüldü — sebep başkaymış

Back-end (`e2104fe`) istek günlüğünde **kendi kusurunu** buldu:
`UseRequestLog()` ara katmanı `UseAuthentication`'dan **sonraydı**, yani
yetki katmanının kestiği istekler hiç kaydedilmiyordu. Günlük 258 satır
taşıyor ve `401` sayısı **sıfır** görünüyordu — çünkü hiçbir `401`
görünmüyordu. Sessizlik kanıt değil, kusurun kendisiydi.

⚠️ Bu, aynı kalıbın üçüncü yüzü: *"görünmeyen satır, olmayan satır gibi
okunur."* Dün gece ben aynı hatayı defterde yaptım, o gece kendileri
kuyrukta, şimdi günlükte.

### Ayırt edici sorgu ve sonucu

Ara katman öne alındıktan sonra panelde dolaşıp `GET /api/platform/logs
?minStatus=401&maxStatus=401` çalıştırıldı:

```
toplam: 2
api/platform/settings  401  actorType: Anonymous  00:33
api/platform/partners  401  actorType: Anonymous  00:32
```

İki şey birden söylüyor:

1. **İstek API'ye ulaşıyor** — yani `401`'i vekil ya da rota kapısı
   üretmiyor. Hipotezimin ilk yarısı burada düştü.
2. **`actorType: Anonymous`** — jeton **hiç gönderilmemiş**. Yani jetonun
   süresi dolmuş ya da imzası tutmuyor değil; ortada jeton yok.

Üstelik ölçümden hemen sonra üç modül (`isletmeler` · `yorum` · `destek`)
arka arkaya açıldı ve **yeni `401` satırı oluşmadı** — toplam 2'de kaldı.

### Gerçek sebep

İki satırın zamanı (00:32–00:33), API'nin yeniden başladığı dakikaya denk
geliyor. Zincir şu:

1. Erişim çerezi süresi dolmuş → rota kapısı yenilemeye çalışıyor.
2. **Yenileme isteği de API'ye gidiyor ve API o an ayakta değil** →
   `jetonuYenile()` `null` dönüyor.
3. İstek jetonsuz devam ediyor → sunucu tarafı okumaları `Anonymous` →
   `401`, ve sayfa **misafir gibi** render ediliyor.

Yani "HMR yeniden derlemesi kapıyı atlıyor" tahminim gereksizdi: kapı
çalışıyordu, **yenileyeceği sunucu yoktu.**

⚠️ **Eski kümeler kanıtlanamıyor.** 23:18, 23:39 ve 00:17'deki `401`'ler
günlük düzelmeden önceydi, yani kayıtları **yok**. Aynı sebepten olduklarını
söyleyemem — yalnız aynı sebebin onları da açıkladığını söyleyebilirim.

Görünen yüzü ayrı bir notta: ulaşılamayan API panelde *"çıkış yaptın"*
gibi okunuyor → [[web-ulasilamayan-api-cikis-gibi]]

