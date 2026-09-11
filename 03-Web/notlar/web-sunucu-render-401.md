---
rol: not
kapsam: web
guncelleme: 2026-09-12
durum: dogrulanmali
---

# Sunucu render'ında `401`: üç liste sessizce boşalıyor

⚠️ **Bu not bir ölçüm + bir hipotez taşıyor ve hipotez doğrulanmadı.**
Belirti ölçüldü, sebep ölçülmedi. `durum: dogrulanmali` tam bu yüzden.

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
