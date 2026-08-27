---
rol: map
kapsam: api
guncelleme: 2026-08-27
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

## Katmanlar

Clean Architecture, dört proje. Bağımlılık **tek yönlü, içe doğru**:

```
Domain  ←  Application  ←  Infrastructure  ←  Api
  (bağımsız)                                   ↑
                                        Api ayrıca Application'a da bağlı
```

| Proje | Bağımlılıkları | Durum |
|---|---|---|
| `DailyCruising.Domain` | **hiçbiri** | 17 klasör, **79 entity** (DbSet sayısı) |
| `DailyCruising.Application` | Domain | **hiçbir NuGet paketi yok** — kasıtlı |
| `DailyCruising.Infrastructure` | Application | EF Core, **22 yapılandırma**, **39 migration**, **13 zamanlanmış iş**, JWT, MailKit, **AWS S3 + SkiaSharp** |
| `DailyCruising.Api` | Application + Infrastructure | **21 controller, 69 yol / 85 işlem**; API arayüzü **Scalar** (`/scalar/v1`, yalnız Development); `Program` `public partial` (`A-43`) |

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
`Microsoft.Extensions.Hosting.Abstractions` · `MailKit`

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

**Sağlık**

| GET | `/api/health` · `/api/health/jobs` |
|---|---|

⚠️ **HÂLÂ YOK ve ürün bunlarsız çalışmıyor:** katalog (tekne / kiralama tipi /
fiyat / ek hizmet girişi), arama ve listeleme, yorumlar, mesajlaşma ve
teklifler, destek talepleri, hakediş ve fatura, bildirim tercihleri, blog,
platform yönetim paneli. **106 tablo var, 69 yol / 85 işlem.** → [[durum]]

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
