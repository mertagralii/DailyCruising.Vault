---
rol: map
kapsam: api
guncelleme: 2026-08-24
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

### Sırayla çalıştırılacaklar — bir uç nokta veya entity yazıldığında

| Sıra | Ne | Ne zaman | Neden |
|---|---|---|---|
| 1 | `/ecc:plan` | Koda dokunmadan **önce** | Riski değerlendirir, adım planı üretir, **CONFIRM bekler**. Bu projede şema onaysız kod yazılmıyor → [[api-sema]] |
| 2 | `Skill: ecc:dotnet-patterns` | C# yazarken | Idiomatik C#, DI, async/await konvansiyonları |
| 3 | `/ecc:build-fix` | `dotnet build` kırılınca | Dil-agnostik; build sistemini tespit edip minimum değişiklikle düzeltir |
| 4 | `ecc:csharp-reviewer` ajanı | C# değişen **her işten sonra** | .NET konvansiyonları, async desenleri, **nullable reference types**, güvenlik, performans |
| 5 | `ecc:database-reviewer` ajanı | Şema, migration veya SQL yazıldığında | PostgreSQL uzmanı: sorgu optimizasyonu, şema tasarımı, indeksleme, güvenlik |

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
