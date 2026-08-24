---
rol: map
kapsam: api
guncelleme: 2026-08-24
durum: guncel
---

# API Desenleri

`DailyCruising.Back-End/` altında kod yazarken uyulacak kurallar.

**Desen ≠ karar.** Karar bir kez verilir ("PostgreSQL kullanacağız"); desen her
dosyada yeniden uygulanır ("entity adı PascalCase ve tekil"). Gerekçeler tarihleriyle
[[api-kararlar]] içinde; burada yalnız **uygulama kuralı** var.

## Katmanlar

Bağımlılık **içe doğru**: `Api → Application → Domain`, `Infrastructure → Application`.

- **`Domain` hiçbir projeye referans veremez.** Bu yön bozulursa Clean Architecture'ın
  anlamı kalmaz → [[api-mimari]]
- İş kuralı `Domain`'de · kullanım senaryosu `Application`'da · dış dünya (veritabanı,
  e-posta, SMS, ödeme) `Infrastructure`'da · HTTP `Api`'de
- Yeni bir NuGet paketi eklerken hangi katmana girdiğine dikkat: veri erişim paketi
  `Domain`'e girerse kural sessizce delinir

## İsimlendirme

Tümü **İngilizce**. Türkçe tablo, kolon veya sınıf adı yazılmaz.

| Ne | Biçim | Örnek |
|---|---|---|
| Entity sınıfı | PascalCase, **tekil** | `Boat`, `ReservationItem` |
| Property | PascalCase | `DepartureTime` |
| Tablo | PascalCase, **çoğul** | `Boats`, `Reservations` |
| Kolon | PascalCase | `DepartureTime` |

PascalCase kararı 2026-08-23'te Mert tarafından verildi ve aynı gün önerilen
snake_case'i iptal etti.

⚠️ **Bedeli:** PostgreSQL tırnaksız tanımlayıcıları küçük harfe indirir, bu yüzden
**elle yazılan her SQL'de çift tırnak gerekir** — `SELECT * FROM "Boats"`. psql,
pgAdmin, DBeaver ve elle yazılan migration betikleri etkilenir. EF Core her
tanımlayıcıyı zaten tırnakladığı için orada bedel yok, ek paket de gerekmez.

## HTTP katmanı

- **Controller tabanlı**, Minimal API değil
- CORS izinli origin'ler koda gömülmez → `appsettings.json` içindeki
  `Cors:AllowedOrigins` dizisinden okunur. Yeni ortam eklenince kod değil
  yapılandırma değişir
- OpenAPI yalnız Development ortamında açık (`/openapi/v1.json`)

## Veritabanı

- **PostgreSQL** → [[api-kararlar]] 2026-08-22
- Erişim EF Core üzerinden; elle SQL istisnadır ve yazıldığında tırnak kuralı geçerlidir

## Yazmadan önce sor

Yeni bir uç nokta veya entity eklemeden önce: bu iş kuralı [[domain-gereksinimler]]'de
tanımlı mı? Değilse önce orada netleşmeli. **Çıkarımla şema kurulmaz** — kurulursa
altı ay sonra "Mert böyle demişti" diye anılır. Cevabı olmayan sorular o dosyanın
"Cevap bekleyenler" tablosunda.

İlgili: [[api-notlar]] · [[api-mimari]] · [[api-kararlar]] · [[api-gorevler]] · [[api-araclar]]
