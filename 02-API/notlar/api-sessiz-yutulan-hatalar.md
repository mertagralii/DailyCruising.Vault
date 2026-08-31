---
rol: not
kapsam: api
guncelleme: 2026-08-28
durum: guncel
---

# Sessiz yutulan hatalar — API'de denetim (2026-08-28)

Arayüz oturumu kendi kodunda şu kusuru buldu: `catch` bloğu listeyi boş
bırakıyordu ve ekran "kayıt yok" diyordu. Yani **okuma başarısızlığı ile
gerçekten boş sonuç aynı değerle temsil ediliyordu.** Kuralı şöyle koydu:

> Boş liste bir cevap, hata bir cevapsızlık. İkisi aynı değerle temsil
> edilirse ayırt edilemez.

Aynı kusur API'de var mı diye bakıldı.

## Sonuç: bu kusur API'de YOK

95 `catch` bloğunun tamamı tarandı.

| Aranan | Bulunan |
|---|---|
| `catch` içinde `Ok()` / 200 dönen | **0** |
| `catch` içinde boş koleksiyon ya da `null` dönen | 3, üçü de meşru |

Meşru üçü:
- `S3FileStorage.OpenAsync` — yalnız `AmazonS3Exception` **ve**
  `StatusCode == NotFound` yakalıyor. "Dosya yok" gerçekten boş sonuçtur.
- `EventLogger` (iki yer) — `LogError` ile günlüğe yazıp olayı yine
  kaydediyor, düşürülen yalnız payload.

Sebebi yapısal: API hatayı **HTTP durum koduna** çeviriyor, boş listeye
değil. Arayüzdeki kusur, durum kodunu veri şekline çevirirken doğuyor.

## Yan bulgu: iki tamamen boş `catch`

`BoardingService.WriteFailureEventAsync` ve `AuthService.SendWarningEmailAsync`.
İkisi de bilerek yutuyor ve yutması doğru — ana işlem yan kanal yüzünden
düşmemeli. Ama ikisi de **tamamen sessizdi**.

Düzeltmeye girişildi (`ILogger` eklemek) ve **geri alındı**:
`DailyCruising.Application` katmanının **hiçbir NuGet bağımlılığı yok**,
yalnız `Domain`'e bakıyor. Eklenecek şey o katmanın ilk paket bağımlılığı
olurdu. "Günlük eklemek" diye başlayan bir değişikliğin mimari bir sınırı
yan etki olarak delmesi kabul edilmedi — bu Mert'in kararı.

Geri aldıktan sonra ölçüldü ve ikisi de sanıldığı kadar kör değil:
- `BoardingService` — denetleyici `EventTypes.BoardingFailed` ile olayı
  **ayrı yoldan** günlüğe yazıyor
- `AuthService` — `EventTypes.TokenReused` e-posta DENENMEDEN önce
  yazılıyor; XML belgesi bunu zaten söylüyor

Görünmeyen tek şey yan etkinin tutup tutmadığı, olayın kendisi değil.

## Geriye kalan gerçek boşluk

Uyarı e-postası **herkeste** sessizce başarısız olsa kimse fark etmez — ve
üretim e-posta sağlayıcısı henüz yapılandırılmadı. Jetonu çalınan ilk
gerçek kullanıcı uyarı almayacak ve bu hiçbir yerde görünmeyecek. Yeni soru
açılmadı; mevcut "üretim e-posta sağlayıcısı" sorusuna bu sonuç eklendi
→ [[api-durum]]

## Ders

Bir kuralın işe yaraması, aradığı şeyi bulmasıyla ölçülmez. Bu denetim
aradığı kusuru bulamadı ama iki şey ortaya çıkardı: bir mimari sınır ve bir
üretim boşluğu → [[api-notlar]] · [[api-kararlar]]
