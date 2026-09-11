---
rol: map
kapsam: api
guncelleme: 2026-09-11
durum: guncel
---

# API Mimarisi

`DailyCruising.Back-End/` → repo `mertagralii/DailyCruising.API`

> ⚠️ **Bu dosya 2026-08-24'ten 2026-08-26'ya kadar bayat kaldı** ve arada 10
> commit geçti. Sebebi disiplin değil kuraldı: `api-mimari.md`'nin ne okuma ne
> yazma tetikleyicisi vardı, yani bayatlamaktan başka yapabileceği bir şey
> yoktu. Kural 2026-08-26'da kapatıldı ve `dogrula.py` artık ölçüyor
> → [[genel-desenler]] "Tetikleyicisi olmayan dosya çürür"
>
> **Buradaki her sayı ölçülerek yazıldı, hatırlanarak değil.**


## Yasal metinler — 2026-09-11

| Metot | Yol | Yetki | Not |
|---|---|---|---|
| GET | `/api/legal` · `/{consentType}` | **kimliksiz** | Yürürlükteki metin; yoksa `404`, boş gövde değil |
| GET · POST | `/api/platform/legal-documents` · `/{id}` | `platform.settings` | Liste pasifleri de gösteriyor; yeni sürüm pasif doğuyor |
| POST | `.../{id}/activate` | `platform.settings` | Eskiyi **aynı işlemde** düşürüyor |
| DELETE | `.../{id}` | `platform.settings` | Yalnız yürürlükte olmayan **ve onaylanmamış** taslak |

⚠️ Güncelleme ucu YOK: gövde değişmez, sürüm eklenir. Onay kaydı metnin
kimliğini değil **sürüm etiketini** saklıyor → [[api-kararlar]]

---

## Platform ayarları — 2026-09-11

| Metot | Yol | Yetki | Not |
|---|---|---|---|
| GET | `/api/platform/settings` | `platform.settings` | Tutma süresi · tahsilat penceresi · biniş belgesi ömrü · iade kademeleri |

Değerler **motorun kendi sabitlerinden** okunuyor (`ReservationService`,
`RefundPolicy.Tiers`), yeniden yazılmıyor. İade kademeleri `switch`'ten
listeye taşındı ve **hesap o listeden yürüyor**.

⚠️ **`PUT` yok.** Süreler derleme zamanı sabiti; iptal kademeleri ise
yazılabilir **olmamalı** (`S-02`, müşteriye verilmiş söz). Cevapta bölüm
başına `editable` alanı var, bugün ikisi de `false` → [[api-kararlar]]

---

## Reklam ve istek günlüğü — 2026-09-11

| Metot | Yol | Yetki | Not |
|---|---|---|---|
| GET · POST · PUT · DELETE | `/api/platform/adverts` · `/{id}` | `platform.settings` | Panel listesi süresi geçmişleri ve kapalıları da gösteriyor; `isLive` ayrı alan |
| POST | `/api/platform/adverts/{id}/image` | `platform.settings` | WebP'ye yeniden kodlanıyor; içerik türü **imzadan** doğrulanıyor |
| POST | `/api/platform/adverts/{id}/activate` · `/deactivate` | `platform.settings` | Yayın anahtarı tarih aralığından AYRI |
| GET | `/api/adverts?placement=` | **kimliksiz** | Yayın = açık + başlamış + bitmemiş + **görseli var** |
| GET | `/api/platform/logs` · `/{id}` | `eventlog.read` | HTTP künyesi; **gövde yok**, yol ve sorgu maskeli |

Yeni tablolar: `Adverts` (`A132`), `RequestLogs` (`A133`). Yeni iş:
`istek-gunlugu-budama` (günde bir, varsayılan 30 gün).

⚠️ İstek günlüğü `EventLogs`'tan **ayrı** ve ayrı kalmalı: olay günlüğü
*"ne oldu"* sorusunu iş dilinde, istek günlüğü *"sunucuya ne geldi"*
sorusunu HTTP dilinde cevaplıyor. Birleştirilseydi iş olaylarının arasına
saniyede onlarca teknik satır karışırdı.

⚠️ Yazma isteğin yolunda değil: sınırlı sıra (`RequestLogQueue`) + arka plan
yazıcısı (`RequestLogWriter`). Ara katman **kimlik doğrulamadan sonra**
çalışıyor → [[api-kararlar]]

---

## Referans kataloglarının yönetimi — 2026-09-11

| Metot | Yol | Not |
|---|---|---|
| GET | `/api/platform/lookups/{katalog}` | **Pasifler dahil** — modülün açılma koşulu |
| POST · PUT | `/api/platform/lookups/{katalog}` · `/{id}` | Anahtar değişmez; çeviri kümesi değiştirilir, birleştirilmez |
| POST | `.../{id}/activate` · `/deactivate` | Silme YOK — pasifleştirme kayıtları bozmuyor |

Kataloglar: `regions` · `boat-types` · `amenities` · `rules`. **Kiralama tipi
YOK**: alanları paranın nasıl hesaplandığını belirliyor.

---

## Platform paneli — yönetim modülleri, 2026-09-11

`A-165`'in dört modülü aynı gün açıldı. Dördü de **okuma ağırlıklı** ve
dördü de var olan kayıtları okuyor; hiçbiri yeni bir kayıt kaynağı açmıyor.

| Metot | Yol | Yetki | Not |
|---|---|---|---|
| GET | `/api/platform/documents` | `partner.approve` | İşletme + tekne belgeleri **tek kuyrukta**, en eskisi başta. Ayrım cevaptaki `scope` alanında |
| POST | `/api/platform/documents/{scope}/{id}/approve` · `/reject` | `partner.approve` | Redde sebep zorunlu ve sözlükten. `Pending` şartıyla tek ifade; yarışta ikinci `409` |
| GET | `/api/platform/finance/summary` · `/entries` · `/payouts` | `ledger.read` | Özet **defter bakiyelerinden** okunuyor, formülden değil. İade satırı **müşteri** hesabından |
| GET | `/api/platform/notification-templates` | `platform.settings` | Katalog **koddan** geliyor (`NotificationTemplateCatalog`); `NotificationTemplates` tablosu boş ve boş olması doğru |
| GET | `/api/platform/activity` · `/{id}` | `eventlog.read` | Personel işlem geçmişinin **genelleştirilmiş hâli** — aynı `EventLogs`, aynı `EventTitles`, aynı etiket çözücü |

⚠️ **Etkinlik akışı ile personel geçmişi arasındaki tek fark süzgeç.**
`staff/{id}/activity` tek kişiye ve `ActorType == Platform`'a kilitli; akış
müşteriyi, işletmeyi ve arka plan işlerini de gösteriyor. Süzgeçler: tarih
aralığı, aktör türü, olay sınıfı (`Read`/`Write`/`Denied`), kişi, konu
(tür + kimlik) — hepsi SQL'de, çünkü `totalCount` da süzülmeli.

⚠️ Konu etiketi çözümü `EventSubjectLabels` (Infrastructure) içinde ve **iki
okuyucu paylaşıyor** → [[api-kararlar]]

---

## Telefonla rezervasyon — 2026-09-11

| Yöntem | Yol | Not |
|---|---|---|
| POST | `/api/platform/reservations` | Personel adına açma. **Tutar katalogdan**, istekten değil |
| POST | `/api/platform/reservations/{kod}/collect` | Elle tahsilat; gerçek bir `Payment` satırı açıyor (`Provider = manual`) |
| POST | `/api/platform/reservations/{kod}/payment-link` | E-posta/SMS ile jetonlu bağlantı; geçerlilik `HoldExpiresAt` ile aynı |
| GET · POST | `/api/reservation-payments/{jeton}` · `/pay` | **Kimliksiz** müşteri tarafı |

Yeni durum `AwaitingCollection` (`A124`) · elle tahsilat alanları `Payments`
üzerinde (`A125`) · ödeme bağlantısı jetonu `Reservations` üzerinde (`A126`) ·
`RescheduleRequests.Status` 32 karaktere genişledi (`A127`).

`Reservations.CreatedByStaffId` — kanal buradan türetiliyor
(`?channel=web|phone`), ayrı kolon yok.

## Taşıma farkının tahsilatı — 2026-09-11

Müşteriye giden jetonlu bağlantı ve onun iki açık ucu:

| Yöntem | Yol | Not |
|---|---|---|
| GET | `/api/reschedule-requests/{jeton}` | **Kimliksiz.** Yetki yerine jeton; jeton yalnız bu talebin ödeme sayfasını açıyor. Süresi dolmuş talep de 200 döner, durumuyla |
| POST | `/api/reschedule-requests/{jeton}/pay` | Fark ödemesini başlatır. **Tutar istekten değil talepten** okunuyor |

`RescheduleRequests.TokenSha256` (`A123`) — düz jeton saklanmıyor.
`LedgerEntry.PaymentId` (`A122`) ve `LedgerEntry.RefundId` (`A121`) — defter
satırı hangi para hareketinden doğduğunu söylemek zorunda.

Yeni zamanlanmış iş: `ProcessRescheduleRequestsJob` (5 dk) — ödenmiş ama
taşınmamış talepleri tamamlar, süresi dolmuş bağlantıları kapatır.

Yeni geliştirme ucu: `POST /api/dev/jobs/{name}/run` — **yalnız Development**,
başka ortamda 404; arayüz belgesine çıkmıyor.

Yeni ortak sınıflar: `ScheduledJobExecutor` (işi çalıştırıp `JobRun` yazan tek
kopya, hem çalıştırıcı hem elle tetikleme kullanıyor) · `RefundRetryPolicy`
(deneme sınırı; hem iş hem panel ayrıntısı oradan okuyor) ·
`IReschedulePaymentFollowUp` (ödeme akışını taşıma kurallarından ayıran kanca).

## Platform vekâlet uçları — 2026-09-06

Platform personeli bir işletme ADINA tekne yönetiyor. Kapsam **adresten**
geliyor (`/api/platform/partners/{partnerId}/boats/...`), oturumdan değil.

| Uç ailesi | Fiiller |
|---|---|
| `platform/boats` | genel liste: `q`, `partnerId`, `regionId`, `status`, sayfalı |
| `platform/partners/{p}/boats` | POST · `{boatId}` GET/PUT |
| `.../boats/{b}/rental-types` | GET POST · `{id}` PUT DELETE |
| `.../rental-types/{id}/prices` | GET POST · `{priceId}` PUT DELETE |
| `.../rental-types/{id}/extras` | GET POST · `{extraId}` PUT DELETE |
| `.../boats/{b}/media` | GET POST · `order` PUT · `{id}` DELETE |
| `.../boats/{b}/documents` | GET POST · `{id}` DELETE |

**İzin `partner.boat.manage`** (`A104` göçü, yalnız platform rollerinde).
⚠️ `boat.write` KULLANILAMAZ: o izin işletme rollerinde de var, yani kapı
işletme hesabını durdurmuyor — ölçüldü, 403 yerine 400 dönüyordu.

**Servisler ÇOĞALTILMADI.** `BoatCatalogService`, `PricingCatalogService`,
`BoatMediaService` ve `BoatDocumentService`'te kapsam çözümü tek bir
noktadan geçiyordu; o noktaya isteğe bağlı bir vekâlet kimliği eklendi.
Kimlik verildiğinde servis ayrıca `IsPlatformStaff` denetliyor — kapsam
istekten geldiği için tek savunma uç özniteliği olamaz.

⚠️ **Belge yolları iki kökte:** okuma `platform/boats/{id}/documents`,
yazma `platform/partners/{p}/boats/{b}/documents`. Yazma hangi işletme
adına yapıldığını adresten söylemeli; okuma belge kimliğiyle tekil.
Birleştirme bilinçli olarak ERTELENDİ (kırıcı değişiklik) → [[api-durum]]

## Sınırlar tek kaynaktan okunuyor — 2026-09-06

`GET /api/lookups` yanıtına `limits` eklendi: `boatPhotoMax`,
`boatPhotoMaxBytes`, `boatDocumentMaxBytes`. Sayılar servis sabitlerinden
okunuyor, uçta tekrar yazılmıyor.

⚠️ Sebep ölçülmüş bir ayrışma: sunucu 24 görsele izin verirken arayüz
20'de duruyordu ve ekran, sunucunun kabul edeceği dört görseli reddedip
işletmeye "sınıra ulaştın" diyordu. **Bu ayrışmayı hiçbir kapı
yakalamıyor** — alan adı doğru, tip doğru, yalnız sayı farklı;
`UnmappedMemberHandling` bunu göremez ve iki taraf da kendi içinde
tutarlı olduğu için test kırmızı yanmaz.

## Katmanlar

Clean Architecture, dört proje. Bağımlılık **tek yönlü, içe doğru**:

```
Domain  ←  Application  ←  Infrastructure  ←  Api
  (bağımsız)                                   ↑
                                        Api ayrıca Application'a da bağlı
```

| Proje | Bağımlılıkları | Durum |
|---|---|---|
| `DailyCruising.Domain` | **hiçbiri** | 17 klasör, **84 entity** (DbSet sayısı) |
| `DailyCruising.Application` | Domain | **hiçbir NuGet paketi yok** — kasıtlı |
| `DailyCruising.Infrastructure` | Application | EF Core, **21 yapılandırma dosyası** (84 entity eşlemesi), **83 migration**, **11 zamanlanmış iş**, JWT, MailKit, **AWS S3 + SkiaSharp**, ödeme sağlayıcıları **Paratika (yürürlükte) + İyzico (eski ödemelerin iadesi için)** |
| `DailyCruising.Api` | Application + Infrastructure | **62 controller, 195 yol / 248 operasyon**; API arayüzü **Scalar** (`/scalar/v1`, yalnız Development); `Program` `public partial` (`A-43`) |

**İki değişmez kural:**

1. **Domain hiçbir projeye referans vermez.** Bu yön bozulursa Clean
   Architecture'ın anlamı kalmaz.
2. **Application hiçbir NuGet paketine bağlı değildir.** `AppUrlOptions`'ın
   `IOptions<>` yerine düz sınıf olmasının ve `ReservationNotifier`'ın
   Infrastructure'da durmasının sebebi bu — ikisi de `ILogger`/`IOptions`
   isteseydi kural bir yerde delinirdi.

Solution dosyası `DailyCruising.slnx` — .NET 10'un yeni XML formatı.

Infrastructure paketleri: `Npgsql.EntityFrameworkCore.PostgreSQL` ·
`Microsoft.Extensions.Identity.Core` · `System.IdentityModel.Tokens.Jwt` ·
`Microsoft.Extensions.Hosting.Abstractions` · `MailKit` · `HtmlSanitizer`

## Uç noktalar

**Kimlik ve hesap**

| Metot | Yol |
|---|---|
| POST | `/api/auth/register` · `/login` · `/refresh` · `/logout` |
| GET | `/api/auth/me` |
| POST | `/api/account/forgot-password` · `/reset-password` |
| POST | `/api/account/send-verification` · `/verify-email` |
| POST | `/api/account/change-email` · `/confirm-email-change` |

**Satış akışı** — üçü de `[AllowAnonymous]`, müşteri üye olmadan tur alabiliyor

| Metot | Yol | Not |
|---|---|---|
| POST | `/api/partners/apply` | **kimliksiz** — "Tekneni Ekle". IBAN zorunlu; panel `Active` olana kadar KAPALI |
| POST | `/api/pricing/quote` | Dönen tutar **bağlayıcı değil**; rezervasyonda yeniden hesaplanıyor |
| POST | `/api/reservations` | Koltukları 15 dk tutuyor, onay e-postası + SMS gönderiyor |
| POST | `/api/reservations/{code}/cancel` | Kod + e-posta/telefon eşleşmesi |
| POST | `/api/reservations/{code}/boarding-ticket` | **kimliksiz**, kimlik teyidi sorgulamayla AYNI. Biniş belgesi için süreli bilet üretir; **yenisi eskisini iptal eder**. Karekod görseli değil taşıyacağı METİN döner. Ömür kalkıştan 12 saat sonrası → `A-84` |
| POST | `/api/reservations/{code}/lookup` | **Misafirin TEK görüntüleme yolu.** Okuma ama gövdeli: kimlik sorgu dizesinde gitseydi erişim günlüklerine düz metin yazılırdı. Hız sınırı `rezervasyonSorgu` — koda göre, `iptal` kovasından AYRI (paylaşsalardı bakan müşteri iptal hakkını tüketirdi) |
| GET | `/api/reservations` | `[Authorize]`, üyenin kendi listesi. Misafir kaydı burada **görünmez** — kullanıcı alanı boş |
| GET | `/api/lookups` | Kimliksiz referans listeleri (bölge, tekne tipi, kiralama tipi, olanak, kural) + çeviri. Arayüz süzgeç menülerini bununla dolduruyor. `A63` ile tohumlandı 2026-08-28 |
| GET/POST | `/api/partner/boats/{id}/media` | Galeri. Yükleme `boat.write`, okuma `boat.read`. Görsel yeniden kodlanıyor (gömülü konum/cihaz verisi düşüyor), **en büyük varyant saklanıyor** — arayüz yeniden boyutlandırıyor |
| DELETE | `/api/partner/boats/{id}/media/{mediaId}` | Kapak silinirse sıradaki devralır |
| PUT | `/api/partner/boats/{id}/media/order` | Sıra + kapak TEK istekte. `IX_BoatMedia_SingleCover` ertelenebilir değil → kapak temizleme ve yazma ayrı `SaveChanges`, tek işlem |
| POST | `/api/payments/start` · `/callback` | Sonuç istemciden DEĞİL sağlayıcıdan teyit ediliyor |

**İşletme paneli** — yetki gerektiriyor, kapsam `ICurrentUser.PartnerId`'den

| Metot | Yol | Yetki |
|---|---|---|
| POST | `/api/boarding/scan` · `/manual` | `boarding.scan` |
| GET | `/api/partner/permissions` · `/roles` · `/members` | `role.manage` / `staff.manage` |
| POST/PUT/DELETE | `/api/partner/roles` · `/roles/{id}` | `role.manage` |
| POST/PUT | `/api/partner/members` · `/members/{id}/role` · `/members/{id}/deactivate` | `staff.manage` |
| POST | `/api/partner/transfer-ownership` | `staff.manage` **+ mevcut sahip olmak + parola** |
| GET | `/api/partner/boats` · `/boats/{id}` | `boat.read` |
| POST/PUT | `/api/partner/boats` · `/boats/{id}` · `/boats/{id}/status` | `boat.write` |
| GET | `/api/boats/{slug}` | **kimliksiz** — yalnız `Published` |
| GET | `/api/partner/boats/{id}/rental-types` · `.../prices` | `boat.read` |
| POST/PUT/DELETE | `/api/partner/boats/{id}/rental-types` · `.../prices` | `boat.write` |
| GET/POST/PUT/DELETE | `.../rental-types/{id}/extras` | `boat.read` / `boat.write` |
| GET | `/api/search` | **kimliksiz** — canlı sorgu, özet tablo yok |
| GET/POST | `/api/reviews/invitation` · `/api/reviews` | **kimliksiz** — hak jetonda |
| GET | `/api/boats/{slug}/reviews` | **kimliksiz** — yalnız `Approved` |
| GET/POST | `/api/partner/reviews` · `/{id}/reply` | `review.reply` |
| GET/POST | `/api/conversations` · `/{id}` · `/{id}/messages` | **oturum açık** — kapsam iki taraflı, yetki YOK |
| GET/POST | `/api/conversations/{id}/offers` · `/{id}/cancel\|reject\|accept` | **oturum açık** — gönderme satıcının, kabul müşterinin |
| POST | `/api/support/tickets` | **kimliksiz** — açma serbest |
| GET/POST | `/api/support/tickets` · `/{id}` · `/{id}/messages` | **oturum açık** |
| PATCH | `/api/support/tickets/{id}` | `support.resolve` **+ platform personeli** |
| GET/POST | `/api/platform/partners` · `/{id}/review\|contracts\|reject\|suspend\|reinstate` | `partner.*` / `contract.send` **+ platform personeli** |
| GET/POST | `/api/platform/reviews` · `/{id}/moderate` | `review.moderate` **+ platform personeli** |
| POST | `/api/payments/refund` | `refund.manage` — **iptalden ayrı yetki**, kasadan para çıkarıyor |

**İşletme paneli** (2026-08-30/31'de eklenenler)

| Metot | Yol | Not |
|---|---|---|
| GET | `/api/partner/reservations` | `reservation.read`. İşletmenin KENDİ rezervasyonları; müşteri listesi `UserId`'ye bağlı olduğu için işletme oradan tek satır göremiyordu. **Müşteri iletişim bilgisi TAŞIMAZ** — `contactEmail` ve `contactPhone` 2026-09-04'te kaldırıldı (`S-27`, Mert): işletme müşteriye doğrudan ulaşabilirse ikinci turu platform dışında satar. Ad kalıyor. Yolcu kimliği de yok. `includeCancelled` ayrı alan, varsayılan `false` |
| GET/PUT | `/api/partner/profile` | `partner.settings`. Yalnız beş alan yazılabilir: `displayName, email, phone, address, city`. Yasal kimlik, IBAN, durum, komisyon **istek tipinde bulunmuyor**, yani bağlanamıyor. Okuma yazmadan fazla alan döndürür (işletme vergi numarası hatasını görebilmeli); IBAN'ın son dört hanesi |
| GET/POST/PUT/DELETE | `/api/partner/boats/{id}/media` · `/documents` · `/calendar` · `/rental-types` · `/prices` · `/extras` | Katalog, galeri, evrak ve takvim |
| GET | `/api/partner/finance/summary` · `/entries` · `/payouts` | `payout.read` — `ledger.read` platforma kapalı olduğu için değiştirildi |

**Bildirim tercihleri** (2026-09-04, `A-78`) — `NotificationPreferences` yeni

| Metot | Yol | Not |
|---|---|---|
| GET/PUT | `/api/account/notification-preferences` | **oturum açık**. Üç alan: `emailEnabled`, `smsEnabled`, `reviewInvitationsEnabled`. Kayıt yoksa varsayılan döner, `404` değil |

⚠️ **Rezervasyon onayı ve iptal bildirimi KAPATILAMAZ** — istek tipinde alanı
yok. Biniş kodu ve iade tutarı o mesajlarda; kullanıcının denetimi yalnız
kanal seçimi ve iki kanal birden kapatılamıyor
(`CK_NotificationPreferences_AtLeastOneChannel`).

**Tercihin uygulandığı üç yer:** `ReservationNotifier` (onay + iptal, kanal
kapısı) · `SendReviewInvitationsJob` (davet + hatırlatma, vazgeçme kapısı) ·
`AnonymizationRepository` (hesap kapatmada satır siliniyor). Listeye yeni bir
tercih alanı eklenirse onu OKUYAN yer de yazılmalı — okunmayan alan, açılıp
kapanan ama hiçbir şey yapmayan bir düğmedir → [[api-kararlar]] 2026-09-04 (8)

**Favoriler** (2026-09-04, `A-77`) — `FavoriteBoats` tablosu yeni

| Metot | Yol | Not |
|---|---|---|
| GET | `/api/favorites` | **oturum açık**, yetki yok. Kullanıcı kimliği parametre DEĞİL, jetondan. Yayından kalkmış tekne listeden çıkmıyor, `isAvailable: false` ile işaretleniyor |
| PUT/DELETE | `/api/favorites/{boatId}` | İdempotent — ikinci istek de `204`. Ekleme yalnız `Published` tekneye; çıkarma yayın durumuna bakmıyor |

⚠️ **Hesap kapatmada favoriler SİLİNİYOR** (`AnonymizationRepository`). Yabancı
anahtar CASCADE bunu yapmıyor: anonimleştirme kullanıcı satırını silmiyor,
üzerine yazıyor → [[api-kararlar]] 2026-09-04 (7)

**Blog** (2026-09-04, `A-76`) — dört tablo şema kurulduğundan beri boştu

| Metot | Yol | Yetki |
|---|---|---|
| GET | `/api/blog` · `/api/blog/{slug}` | **kimliksiz** — yalnız `Published`. Taslak ve onay bekleyen de `404`: "var ama yayında değil" denseydi kısa ad denenerek rakip yazıların varlığı öğrenilirdi |
| GET | `/api/blog/categories` | **kimliksiz**. Yazı sayısı yalnız yayındakileri sayıyor |
| GET/POST | `/api/blog/posts` | `blog.write`. Kapsam jetondan: işletmeli çağıran kendi yazılarını, platform personeli platformun yazılarını görür. **İşletme kimliği hiçbir uçta parametre değil** |
| GET/PUT/DELETE | `/api/blog/posts/{id}` | `blog.write`. Yazma yanıtları çeviri sözlüğünü **TAM** döndürür — tek dile çözülmüş dönseydi panel gördüğünü geri gönderdiğinde diğer dili sessizce silerdi |
| POST | `/api/blog/posts/{id}/submit` | `blog.write`. İşletme yazısı `UnderReview`, platform yazısı doğrudan `Published` |
| POST | `/api/blog/posts/{id}/cover` | `blog.write`. WebP'ye yeniden kodlanıyor, `blog-media/` önekine yazılıyor → `S-24` |
| GET | `/api/blog/moderation` · `/moderation/{id}` | `blog.approve` — **kapsamsız, kasıtlı**. En uzun bekleyen üstte |
| POST | `/api/blog/moderation/{id}/publish` · `/reject` | `blog.approve`. Ret gerekçesi `BlogPosts.RejectionReason` kolonunda (`A-76` migration); reddetme YAYINDAKİ yazıda da çalışır — platform onayladığı bir metni geri çekebilmeli |
| POST/PUT/DELETE | `/api/blog/categories` · `/categories/{id}` | `blog.approve` — kategori listesi ortak taksonomi, tek işletme genişletemez |

⚠️ `posts`, `categories` ve `moderation` **kısa ad olarak yasak**: üçü de bu
önek altında gerçek yol. `/api/blog/` altına yeni sabit yol eklenirse
`BlogService.ReservedSlugs` da genişletilmeli → [[api-kararlar]] 2026-09-04 (5)

**Sağlık**

| GET | `/api/health` · `/api/health/jobs` |
|---|---|

⚠️ **2026-08-31'de ölçülerek düzeltildi.** Bu satır "katalog, arama, yorumlar,
mesajlaşma, teklifler, destek, hakediş, platform paneli yok" diyordu ve
sayısı **69 yol**tu; ölçüldüğünde hepsi vardı ve **93 yol** çıktı. Dosya
bayatlamıştı — CLAUDE.md'deki *"tetikleyicisi olmayan dosya çürür"*
dersinin ikinci örneği.

**Gerçekten YOK olanlar** (2026-08-31 ölçümü → [[api-uc-envanteri-2026-08-30]]):

| Eksik | Durum |
|---|---|
| Yönetim panelinin 9 modülü | müşteriler, personel, kuponlar, bölgeler, reklam, e-posta, SMS, log, aktivite |
| Yorum yanıtı düzenleme/silme | yalnız `POST .../reply` — tek atış |
| IBAN değiştirme akışı | kasten yok; parola teyidi + bildirim isteyen ayrı akış olmalı |

**108 tablo, 108 yol / 136 operasyon, 48 yetki.** → [[durum]]

## Zamanlanmış işler

`IScheduledJob` (Application) + `ScheduledJobRunner` (Infrastructure,
`IHostedService`). Hangfire/Quartz eklenmedi — bu ölçekte tek bir arka plan
servisi yetiyor.

Altı iş çalışıyor: rezervasyon tutma süresi · teklif süresi · konuşma kapatma ·
sefer tamamlama · olay günlüğü bölümü açma · TCMB kur çekme.

⚠️ Bu işler olmadan **veritabanı kısıtları sistemi kilitler**: süresi dolmayan
tutmalar koltukları kalıcı tutar, süresi dolmayan teklifler tarihleri sonsuza
kadar kapatır.

## Dış servisler

| Ne | Sağlayıcı | Yerelde |
|---|---|---|
| E-posta | **Postmark** | **Mailpit** (Docker, `localhost:1025`, arayüz `:8025`) |
| SMS | **Netgsm** | günlüğe yazan uygulama |
| Döviz kuru | TCMB | gerçek servis |
| Dosya depolama | **S3 uyumlu** (`A-60`) — geliştirmede MinIO, üretimde S3/R2. Resimler **WebP**, üç genişlik | `Storage:*` · anahtarlar user-secrets |
| Sanal POS | **İyzico** — Checkout Form; sandbox'ta uçtan uca doğrulandı 2026-08-26. Bölüştürme altyapısı hazır (`PartnerPayeeAccounts`), ⚠️ alıcı kaydı AÇILAMIYOR — İyzico hesabı pazaryeri değil (`A-41`) | `Payments:Iyzico:BaseUrl` · anahtarlar user-secrets |

Sağlayıcı seçimi **yapılandırmadan** geliyor; değiştirmek kod değil ortam
değişkeni işi → [[api-kararlar]] 2026-08-25.

⚠️ Üretimde yerel/sahte sağlayıcıyla **uygulama açılmıyor** — yoksa müşteriler
rezervasyon kodlarını hiç almaz ve bu günlerce fark edilmezdi.

## Yapılandırma

CORS izinli origin'ler koda gömülü değil → `appsettings.json` içindeki
`Cors:AllowedOrigins`.

OpenAPI yalnız Development ortamında açık (`/openapi/v1.json`).

`AllowedHosts` üretimde boş ya da `*` olamaz — uygulama açılışta patlıyor.
Değer koda YAZILMADI: üretim host adı bir dağıtım kararı → `A-19`.

## Şema

Veritabanı şeması ayrı dosyada, sekiz bölüm halinde → [[api-sema]]

İlgili: [[api-kararlar]] · [[api-desenler]] · [[proje]] · [[00-Index]]
