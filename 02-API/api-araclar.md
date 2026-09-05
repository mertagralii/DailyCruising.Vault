---
rol: map
kapsam: api
guncelleme: 2026-09-05
durum: guncel
---

# API Araçları

`DailyCruising.Back-End/` altında çalışırken **hangi durumda hangi aracı** kullanacağım.

Gerekçesiz araç satırı eklenmez.

| Tetikleyici | Araç | Neden |
|---|---|---|
| C# kodu yazdım veya değiştirdim | `ecc:csharp-reviewer` ajanı | async doğruluğu, nullable referans tipleri, .NET konvansiyonları |
| Şema, migration veya sorgu yazılacak | `ecc:database-reviewer` ajanı | İndeks, kısıt ve performans hataları en pahalı düzeltilen hatalar |
| PostgreSQL'e özgü bir şey yapılacak | `ecc:postgres-patterns` skill'i | PascalCase tırnak davranışı gibi Postgres'e özgü tuzaklar var -> [[api-desenler]] |
| Kimlik doğrulama, yetki veya ödeme kodu yazıldı | `ecc:security-reviewer` ajanı | Satır bazlı yetki ve fiyat doğrulaması bu projenin iki bilinen güvenlik riski -> [[durum]] |
| Build hatası aldım | `ecc:build-error-resolver` ajanı | Dar kapsamlı, mimariye dokunmayan düzeltme |
| EF Core / .NET 10 API'si soruldu | `context7` MCP | .NET 10 ve `.slnx` yeni; eğitim verim bayat olabilir -> [[api-slnx-formati]] |
| Test yazılacak | `ecc:csharp-testing` skill'i | xUnit projesi henüz yok; kurulunca biçim buradan |
| Domain modeli tasarlanacak | `superpowers:brainstorming` | A-01 çıkarımla değil konuşularak tasarlanacak -> [[api-gorevler]] |
| Bir kuralın/tipin kaç yerde kullanıldığı sorulacak | `Explore` ajanı | Katman sayısı arttıkça elle tarama bağlamı doldurur → [[genel-araclar]] |
| Şema sekiz bölümü bitince bütünsel tutarlılık denetimi | `Workflow` | Tablolar arası ilişki, kısıt bütünlüğü ve güvenlik ayrı gözlerle taranmalı → [[genel-araclar]] |

## Dikkat

- **Rider MCP kurulu.** IDE üzerinden çalışma gerekirse mevcut; ama derleme ve test
  için `dotnet` CLI yeterli, önce o denenir
- Domain soruları cevaplanmadan şema kuran araç yok — eksik olan bilgi, araç değil

## ECC — API tarafında hangi komut ne zaman

ECC v2.2.0 küresel kurulu. **Komutlar `/ecc:<ad>`**, skill'ler `Skill` aracıyla
`ecc:<ad>`.

### ⚠️ Önce bilinmesi gereken boşluk

**.NET / C# / PostgreSQL için özel slash komut YOK.** `/ecc:dotnet-build`,
`/ecc:csharp-review`, `/ecc:csharp-test` **mevcut değildir** — aranırsa bulunmaz.
Frontend tarafı (`/ecc:react-*`) tam desteklidir, backend tarafı değildir.

Karşılığı şu üçlüdür:
- Jenerik komutlar: `/ecc:build-fix`, `/ecc:code-review`, `/ecc:test-coverage`
- **Doğrudan ajan çağrısı** — asıl güç burada
- Skill'ler — .NET ve Postgres için zengin

### Zincir — bir uç nokta veya entity yazılırken

Web tarafındaki zincirin API karşılığı. **Sıra rastgele değil**: her adım bir
öncekinin yakalayamadığını yakalar.

| # | Ne | Komut / ajan | Neden bu sırada |
|---|---|---|---|
| 1 | Plan | `/ecc:plan` | Riski değerlendirir, adım planı üretir ve **koda dokunmadan CONFIRM bekler** |
| 2 | Şema onayı | — (bu projeye özgü) | Bu projede **onaysız kod yazılmaz**. İlgili bölüm [[api-sema]]'da onaylı değilse durulur, Mert'e sorulur |
| 3 | Katman kontrolü | `Skill: ecc:hexagonal-architecture` | Kod yazılmadan **önce**: bu sınıf hangi katmana ait? Yanlış katman sonradan taşınırken bağımlılık yönü kırılır → [[api-desenler]] |
| 4 | Yazım kuralları | `Skill: ecc:dotnet-patterns` | Idiomatik C#, DI, async/await. Yazarken açık olur, sonradan düzeltilmez |
| 5 | Derleme | `dotnet build` | Sözdizimi ve tip. **Gerekli ama yeterli değil** |
| 6 | C# incelemesi | `ecc:csharp-reviewer` ajanı | Async tuzakları, **nullable reference types**, güvenlik, performans — derleyicinin görmediği sınıf |
| 7 | Veri katmanı incelemesi | `ecc:database-reviewer` ajanı | Şema, migration veya SQL değiştiyse. Postgres uzmanı: indeks, kısıt, sorgu planı |
| 8 | Güvenlik | `ecc:security-reviewer` ajanı | Kullanıcı girdisi, kimlik doğrulama, ödeme veya fiyat kodu varsa **atlanamaz** |
| 9 | **Gerçekten çalıştır** | `dotnet run` + uç noktaya istek | ⛔ **Bu adım atlanamaz** |
| 10 | Kayıt | `api-durum.md` + panoda `Kanıt:` | Kanıt satırı 5, 6 ve 9'un çıktısını içerir |

### ⛔ 9. adım neden atlanamaz

**`dotnet build` temiz olması uç noktanın doğru yanıt verdiğini göstermez.**

Web tarafında `npm run build` temizken 6 görsel tuzak tarayıcıda yakalandı. API'nin
karşılığı aynıdır ve daha sinsidir — derleyici şunların hiçbirini görmez:

- Yanlış status kodu (404 dönmesi gerekirken 200)
- Boş veya eksik alanlı JSON gövdesi
- Yetkisiz erişimin açık kalması — **panellerin herkese açık olması** tam bu sınıf
- `DateTime` `Kind` hatası — Npgsql UTC ister, belirsiz `Kind` **çalışma anında**
  fırlar → [[api-kararlar]] 2026-08-22
- Migration'ın veritabanına gerçekten uygulanmamış olması

**Asgari doğrulama:** uç noktaya istek at, **status kodunu ve gövdeyi** gör.
Yetki gerektiren bir uç ise **yetkisiz istekle de** dene — 401 dönmüyorsa iş bitmemiştir.

### Alt zincir — migration yazılırken

Migration'ın diğerlerinden farkı: **geri alması pahalıdır**, bazen imkânsızdır.

| # | Ne | Neden |
|---|---|---|
| 1 | `Skill: ecc:database-migrations` | Rollback ve sıfır kesintili deploy desenleri |
| 2 | `dotnet ef migrations add <ad>` | — |
| 3 | **Üretilen SQL'i oku** | EF'in ne ürettiği varsayılmaz. Tablo adları PascalCase olduğu için **çift tırnaklı** çıkmalı → [[api-desenler]] |
| 4 | `ecc:database-reviewer` ajanı | Kısıt, indeks ve veri kaybı riski |
| 5 | `dotnet ef database update` | — |
| 6 | **Geri alma yolunu dene** | `dotnet ef migrations remove` veya bir önceki migration'a dönüş çalışıyor mu |

⚠️ **Migration UYGULAMA rolüyle değil, `dailycruising` rolüyle çalıştırılır.**

`A-10` uygulama rolünü en az ayrıcalıklı yaptı: `dailycruising_app` DDL
çalıştıramıyor, `dotnet ef database update` `42501 permission denied for
schema public` ile düşüyor. Süper kullanıcıya geçmek de YETMİYOR — ve tehlikeli
olan tam bu:

`ALTER DEFAULT PRIVILEGES` **`dailycruising` rolüne bağlı**. Migration başka
bir rol adına koşarsa yeni tablo O rolün malı olur, varsayılan ayrıcalıklar
devreye girmez ve uygulama rolü tabloya erişemez. Sonuç `A-10`'un kendi
uyarısıdır: *"uygulama açılışta değil İLK KULLANIMDA patlar, üstelik yalnız o
özellikte."* Migration sorunsuz görünür, testler geçer, hata canlıda çıkar.

Yerelde çalışan komut:

    ConnectionStrings__Default="Host=/tmp;Port=5432;Database=dailycruising_dev;Username=mertagrali;Options=-c role=dailycruising" \
      dotnet ef database update --project DailyCruising.Infrastructure --startup-project DailyCruising.Api

`Options=-c role=...` Npgsql'in oturuma `SET ROLE` yaptırma yolu; süper
kullanıcı parola sormadan role geçebiliyor.

**Kontrol yolu — tablo yaratan her migration'dan sonra:**

    SELECT tableowner FROM pg_tables WHERE tablename='YeniTablo';
    SELECT has_table_privilege('dailycruising_app','"YeniTablo"','SELECT');

Sahibi `dailycruising` değilse ayrıcalıklar da yoktur. `A-77`'de ölçüldü:
sahip `dailycruising`, `SELECT/INSERT/DELETE` var, **`TRUNCATE` yok**
(2026-09-04).

⚠️ **Veri kaybettiren migration sessizce geçer.** Kolon silme, tip daraltma ve
`NOT NULL` ekleme üçü de derlenir, uygulanır ve veriyi götürür. 4. adım bu yüzden var.

### Alt zincir — kimlik doğrulama ve fiyat doğrulama (`A-03`, `A-05`)

Bu ikisi projenin **1 ve 3 numaralı blocker'ı** → [[durum]]. Normal zincire ek olarak:

| Ne | Neden |
|---|---|
| `Skill: ecc:security-review` | Auth, secret, injection, güvensiz kripto |
| `ecc:security-reviewer` ajanı | Yazıldıktan sonra ikinci göz |
| `ecc:silent-failure-hunter` ajanı | Yutulmuş exception bir yetki kontrolünü sessizce atlatabilir |
| **Negatif test** | Yetkisiz istek 401 mi, başka kullanıcının verisi 403 mü, **istemciden gelen tutar yok sayılıyor mu** |

Fiyat doğrulamasının kabul ölçütü panoda yazılı: *"istemciden gelen tutar yok
sayılır, sunucu tutarı esas alınır"* → [[api-gorevler]] `A-05`. Bu, istemcinin
gönderdiği tutarla karşılaştırma yapmak **değildir** — hiç bakmamaktır.

### Şema ve veritabanı — bu projenin şu anki işi

| Tetikleyici | Ne | Neden |
|---|---|---|
| Şema bölümü tasarlanıyor | `Skill: ecc:postgres-patterns` | Postgres'e özgü şema, indeksleme, güvenlik. `EXCLUDE`/GIST kısıtı bu projenin Postgres kararının **asıl gerekçesi** → [[api-kararlar]] 2026-08-22 |
| Migration yazılacak | `Skill: ecc:database-migrations` | Rollback ve **sıfır kesintili deploy**; migration geri alınamazsa üretimde pahalıya patlar |
| Uç nokta tasarlanacak | `Skill: ecc:api-design` | Kaynak adlandırma, status kodları, sayfalama, filtreleme, hata yanıtı, versiyonlama |
| Katman sınırı sorusu | `Skill: ecc:hexagonal-architecture` | Ports & Adapters, domain sınırı, bağımlılık tersine çevirme. Bu projenin Clean Architecture kararıyla aynı ailede → [[api-mimari]] |
| İstemci–sunucu sözleşmesi değişiyor | `Skill: ecc:contract-first` | `A-07`'nin tam konusu: frontend elle tip yazmasın, alan kayması olmasın |
| Tip tasarımı doğru mu | `ecc:type-design-analyzer` ajanı | Kapsülleme, invariant ifadesi, zorlama. Domain modelinde değerli |

### Güvenlik — ertelenmeyecek olanlar

| Tetikleyici | Ne | Neden |
|---|---|---|
| Kimlik doğrulama kodu yazılıyor (`A-03`) | `ecc:security-reviewer` ajanı + `Skill: ecc:security-review` | Panellerin herkese açık olması **1 numaralı blocker** → [[durum]] |
| Ödeme / fiyat doğrulama kodu (`A-05`) | Aynı ikili | Fiyat istemcide hesaplanıyor; sunucu doğrulaması yazılırken atlanacak yer değil |
| Hata yutuluyor olabilir | `ecc:silent-failure-hunter` ajanı | Sessiz hata, yutulmuş exception, kötü fallback |

### Test — bu projede hiç yok

xUnit projesi kurulmadı. Kurulduğunda:

| Ne | Neden |
|---|---|
| `Skill: ecc:csharp-testing` | xUnit, FluentAssertions, mocking, integration test organizasyonu |
| `/ecc:test-coverage` | Kapsam boşluklarını bulup eksik testleri üretir |
| `ecc:tdd-guide` ajanı | Test-önce disiplinini zorlar |

### ⚠️ GateGuard — ilk yazmada bloklar

`pre:edit-write:gateguard-fact-force` hook'u **her dosyaya ilk `Edit`/`Write`'ı
bloklar** ve önce somut araştırma ister (importer'lar, veri şemaları, kullanıcı
talimatı). Aynısı oturumun ilk `Bash` komutu için de geçerli.

Bu bir arıza değil, kasıtlı kapıdır — körlemesine yazmayı engeller. Yapılacak:
istenen olguları sun ve **aynı işlemi tekrar dene**. Kurulum veya onarım işini
tıkıyorsa `ECC_GATEGUARD=off` ya da
`ECC_DISABLED_HOOKS=pre:edit-write:gateguard-fact-force`
→ [[genel-gateguard-davranisi]]

Birden çok dosya oluşturulacaksa tek bir `Bash` heredoc çağrısında toplamak kapı
sayısını azaltır.

### Hangi komutları hangi sırayla — emin olunamazsa

`Skill: ecc:ecc-recipes` — tarif edilen iş akışını doğru ECC komut **grubuna**,
sırasıyla ve durma koşuluyla eşler. `/ecc:ecc-guide` ise ECC'de ne olduğunu listeler.

İlgili: [[api-notlar]] · [[api-desenler]] · [[api-mimari]] · [[api-gorevler]] · [[genel-araclar]]

## Tohum mu demo mu — ikisi ayrı iş

| Betik | Ne için | İçerik |
|---|---|---|
| `araclar/tohum-veri.sh` | **Akış çalışıyor mu** | Asgari fikstür: iki tekne, üç rezervasyon, bir konuşma, bir yorum |
| `araclar/demo-veri.sh` | **Ürün nasıl görünüyor** | Sekiz tekne, beş tip, sekiz bölge, fiyat + fotoğraf, iki işletme, blog, üç iade dilimi |

**Neden ikisi ayrı:** tohum hızlı ve dar; demo yavaş ve geniş. Tek betikte
birleştirilseydi, akış testi için her seferinde sekiz tekne ve altı görsel
üretilirdi.

### Demo betiğinde ölçerek öğrenilenler

**Fiyatlama biçimi TABLODAN yazılmaz, referans listesinden okunur.**
`lookups` her kiralama tipiyle birlikte `pricingStrategy` ve `durationKind`
döndürüyor. İlk yazımda tabloya elle yazılmıştı ve tekne bazlı fiyatlanan bir
tipe kişi başı fiyat gönderen tek satır demoyu durdurdu.

**İade dilimi betiğin çalışma SAATİNE bırakılamaz.** Kalkış tarihi gün
hassasiyetinde, saat kiralama tipinden geliyor; aynı tarih sabah çalıştırılınca
%50, akşam çalıştırılınca %0 dilimine düşüyor. Sefer anı yerleştirilmezse demo
"üç dilim de görünsün" sözünü tutamıyor.

**Üç dilim üç AYRI teknede kurulmak zorunda:** `EX_Voyages_NoOverlapPerBoat`
aynı tekneye üst üste sefer yazdırmıyor.

**Kategori anahtarı damgasız olmalı.** Damgalıyken ikinci koşu aynı adı
taşıyan ikinci bir kategori açıyordu; iki "Rotalar" süzgeci demoda hatadan
ayırt edilemez.

**Hız sınırı demoyu durduruyor.** Hesap uçları adres başına 15 dakikada 10
istek; betik birkaç kayıt ve giriş yapıyor ve başarısız bir koşudan sonra
tekrar denemek kovayı tüketiyor. Betik `429`'da ne yapılacağını yazıyor:

    RateLimiting__Enabled=false ASPNETCORE_ENVIRONMENT=Development \
      dotnet run --project src/DailyCruising.Api --no-launch-profile

**Tekne fotoğrafı UYDURULMAZ.** Her tekneye ayırt edilebilir, üstünde DEMO
yazan bir yer tutucu üretiliyor; gerçek fotoğrafları işletmeler yükleyecek
(Mert, soru 27).
