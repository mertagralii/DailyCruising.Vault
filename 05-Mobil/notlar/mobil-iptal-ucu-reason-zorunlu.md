---
rol: not
kapsam: mobil
guncelleme: 2026-09-10
durum: guncel
---

# İptal ucu `reason` zorunlu istiyor — `openapi.json` bunu söylemiyor

`POST /api/reservations/{code}/cancel` gövdesi 2026-09-10'da (backend commit
`b07da48`) değişti. Mobilde **bugün iptal ekranı yok** — bu not bir arıza kaydı
değil, `M-05` ile API istemcisi yazıldığında **düşülecek tuzağın** kaydı.

## Tuzak

`openapi.json`'da `reason` **nullable** görünür ve `required` dizisi `None`'dır.
Şemadan üretilen tip alanı **opsiyonel** gösterir. Zorunluluk belgede değil,
C# tarafında `ReservationService.CancelAsync` içinde ve ayrıca veritabanı
kısıtında yaşıyor.

Sonuç: **derleyici uyarmaz, uç çalışma zamanında reddeder.** Web tarafı tam bu
yüzden sessizce kırıldı. "Üretilen tip yeşil, demek ki sözleşmeye uyuyorum"
çıkarımı bu uçta yanlıştır → [[web-elle-yazilan-tip-yalan-soyler]]

Aynı şeyin ikinci yüzü: `reason` bir enum ama şemada `enum` dizisi yok, değerler
belgeden üretilemez; elle yazılacak → [[web-enum-uretilemez]]

## Sözleşme

```json
{ "contactEmail": "...", "contactPhone": "...",
  "reason": "PlansChanged"|"Weather"|"Health"|"WrongBooking"|"FoundAlternative"|"Other",
  "note": "serbest metin, en çok 500 karakter" }
```

- `reason` **zorunlu**. Yoksa 400: `İptal gerekçesi seçilmeli.`
- `reason === "Other"` ise `note` **zorunlu**. Boşsa 400:
  `"Diğer" seçtiyseniz kısa bir açıklama yazın.`
- Boş/boşluk `note` gönderilmez: `trim()` edilir, boşsa alan **hiç konmaz**.
- `note` **en çok 500 karakter** ve bu sınırı **istemci uygulamak zorunda** —
  aşağıdaki bölüm.

Hata gövdeleri hazır Türkçe cümle döner; mobilde çeviri tablosu gerekmez.

## 500 karakter sınırını istemci kesmek zorunda — uç 400 değil **500** dönüyor

Kendim ölçtüm (2026-09-10, back-end reposu):

| Nerede | Ne var |
|---|---|
| `ReservationContracts.cs:137` | `record CancelReservationRequest(...)` — dört alan da çıplak nullable, **`[MaxLength]`/`[StringLength]` yok** |
| `ReservationService.cs:212` | yalnız `Trim()` + `Other`→boş denetimi; **uzunluk denetimi yok** |
| `ReservationConfigurations.cs:73` | `CancellationNote` → `HasMaxLength(500)` |
| `ReservationsController.cs:252` | eylemin **tek** `catch`'i `ReservationException` |
| `Program.cs:1278` | yakalanmayan her şeyi ayrıntısız 500'e çeviren genel ağ |

Zincir: 501 karakter → Postgres 22001 → `DbUpdateException` → denetleyicinin
`catch`'ine uymaz → genel işleyici → **HTTP 500**, gövde
`{"error":"Beklenmeyen bir hata oluştu."}`.

**Bu yüzden iki katman gerekir, biri yetmez:**
1. `TextInput` üzerinde `maxLength={500}` — yazmayı ve yapıştırmayı engeller
2. Gönderimden önce `note.trim().slice(0, 500)`

Tek katman bırakılamaz çünkü **hata hâli 400 değil 500**: kullanıcı "bir şeyler
ters gitti" görür ve doğru eylem (kısalt) hiçbir yerde önerilmez. Doğrulanamayan
girdi burada okunabilir bir hataya değil, **sessiz bir çökmeye** dönüşüyor.

⚠️ **Bu bir back-end boşluğu ve düzeltilmesi bekleniyor.** WEB oturumu Mert'e
bildirdi: sınır denetimi serviste olmalı ve 400 dönmeli. Düzeltilirse istemci
katmanları **yine kalır** — sadece aşım hâli okunabilir bir 400'e döner.

## Anahtar listesi büyüyebilir — sözlük `?? ham` ile yazılır

Değer Postgres enum'u **değil**, `varchar(32)` metin — ama sayan bir kısıt var:
`CK_Reservations_CancellationReason_Enum`, migration
`20260910175534_A115_IptalGerekcesi`, altı değeri tek tek listeliyor. Yanına
`CK_Reservations_CancellationOtherNote` de eklenmiş, yani `Other`+açıklama kuralı
hem serviste hem veritabanında. **Liste kazara büyümez**: yeni değer C# enum üyesi
+ yeni migration ister.

Buna rağmen sözlük dayanıklı yazılır ve sebep enum değil **dağıtım gecikmesi**:
mobil uygulama mağazada eski sürüm olarak kalır; API yeni bir değer döndürdüğünde
o değeri bilmeyen istemci **boş hücre** basar. Kural web'den geliyor
(`enum.ts` başında yazılı): sözlük dışa `Record<string, string>` açılır, çağıran
`IPTAL_SEBEBI[ham] ?? ham` basar — tip "bu değer imkânsız" dese bile ekran o gün
ham anahtarı göstermeli.

⚠️ **Mobilde web'de olan kapı yok.** Web sözlüğü
`satisfies Record<CancellationReason, string>` ile üretilen enum'a bağlı, değer
eklenince **derleme hatası** veriyor. Elle yazılan mobil sözlükte o kapı yoktur:
eksik anahtar sessizce ham değer basar ve kimse fark etmez. Bu, `openapi.json`'dan
tip üretmeyi `M-05`'te tercih değil **gereklilik** yapan ikinci sebeptir →
[[mobil-gorevler]] · [[web-elle-yazilan-tip-yalan-soyler]]

## Türkçe etiketler

**Kanonik kaynak:** web reposu `src/lib/api/types/reservation.ts` → `IPTAL_SEBEBI`.
Aşağıdaki tablo oradan kopyalandı (2026-09-10); ayrışırsa **kaynak odur**, bu
tablo değil. Şemadan üretilemiyor → [[web-enum-uretilemez]]

| Anahtar | Etiket |
|---|---|
| `PlansChanged` | Planım değişti |
| `Weather` | Hava durumu uygun değil |
| `Health` | Sağlık sorunu |
| `WrongBooking` | Yanlış rezervasyon yaptım |
| `FoundAlternative` | Başka bir seçenek buldum |
| `Other` | Diğer |

## Web'in ödediği bedel — mobilde tekrarlanmasın

Onay penceresi küçük bir forma dönüştü (zorunlu sebep + isteğe bağlı açıklama,
`Other`'da zorunlu). **Hata hâlinde pencere kapatılmadı:** kapanınca kullanıcının
yazdığı açıklama siliniyordu. Mobilde modal/sheet için aynı kural geçerli —
400 dönen istek kullanıcının girdisini yok etmemeli.

Kaynak: DailyCruising.WEB oturumu, 2026-09-10 oturumlar arası bildirim.
Sözleşme ve 500 zinciri back-end reposunda **bu oturumda ayrıca doğrulandı**;
dosya/satır atıfları yukarıda.

İlgili: [[mobil-notlar]] · [[mobil-desenler]] · [[mobil-gorevler]] · [[web-elle-yazilan-tip-yalan-soyler]] · [[web-enum-uretilemez]]
