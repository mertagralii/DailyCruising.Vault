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

## EF Core

- **Entity `Domain`'de, yapılandırma `Infrastructure`'da.** Entity sınıfı sade POCO;
  `[Table]`, `[Column]` gibi öznitelik yazılmaz. Kısıt ve indeks
  `IEntityTypeConfiguration<T>` içinde durur — yoksa Domain veri erişimini tanır ve
  bağımlılık yönü sessizce delinir
- **Tablo adı `DbSet` adından gelir.** `DbSet<User> Users` -> `"Users"`. PascalCase
  çoğul kuralı böylece kendiliğinden sağlanıyor, ek yapılandırma yok
- **Enum'lar metin olarak saklanır.** `OnModelCreating` içindeki tek döngü tüm enum
  property'lerini `string`'e çeviriyor; yeni enum eklenince bir şey yazmaya gerek yok
- **Para daima `numeric`**, asla `float`/`double`. `HasColumnType("numeric(12,2)")`
- **Tarih daima `DateTimeOffset`.** Npgsql `DateTime`'ın `Kind`'ının UTC olmasını
  zorunlu tutuyor; `DateTimeOffset` bu tuzağı baştan kapatıyor
- **Parola ve bağlantı dizesi `appsettings.json`'a yazılmaz** — geliştirmede
  user-secrets, sunucuda ortam değişkeni. Commit'lenen parola git geçmişinden
  pratikte silinemez
- **Migration bölüm bölüm alınır**, hepsi tek seferde değil. İlk hatanın nerede
  olduğu ancak böyle görülür

## Kısıtlar veritabanında durur, kodda değil

Bir kural veritabanı kısıtıyla ifade edilebiliyorsa **orada durur**. Uygulama
kodundaki kontrol, o kontrolü atlayan bir yazma yolu yazıldığında sessizce delinir.

| Kural | Nasıl |
|---|---|
| Tekil ama koşullu ("tek onaylı sözleşme") | Kısmi benzersiz indeks: `HasFilter(...)` |
| Aralık ("komisyon 0-100") | `t.HasCheckConstraint(...)` |
| Çakışmama ("iki sefer aynı anda olamaz") | `EXCLUDE USING gist` — **EF üretemez, elle SQL** |

⚠️ `HasFilter` ve `HasCheckConstraint` içindeki kolon adları **çift tırnaklı**
yazılır: `"\"Status\" = 'Approved'"`. PascalCase kararının bedeli burada ödeniyor.

## HTTP katmanı

- **Controller tabanlı**, Minimal API değil
- CORS izinli origin'ler koda gömülmez → `appsettings.json` içindeki
  `Cors:AllowedOrigins` dizisinden okunur. Yeni ortam eklenince kod değil
  yapılandırma değişir
- OpenAPI yalnız Development ortamında açık (`/openapi/v1.json`)
- **Enum'lar JSON'da metin**, sayı değil (`JsonStringEnumConverter`). Sayı
  dönerse arayüz `listCurrency: 0` görür ve enum sırası değiştiğinde sessizce
  başka bir para birimi gösterir; veritabanında da metin saklanıyor

## Para istemciden gelmez

Tutar taşıyan hiçbir istek gövdesinde **tutar alanı bulunmaz**.

"İstemcinin tutarını al, sonra karşılaştır" güvenlik değildir: karşılaştırma
bir kod yolunda atlanabilir, yeni bir uçta unutulabilir, yuvarlama farkıyla
gevşetilebilir. **Alan hiç var olmazsa atlanacak bir şey de olmaz** —
`QuoteRequest` bu yüzden tutar alanı taşımıyor.

- Hesabın çıktısı (`Quote`) **aynı zamanda** rezervasyona dondurulacak alanların
  tamamıdır. Hesap ile saklanan arasında ikinci bir dönüşüm yok, yani ikisinin
  ayrışması mümkün değil
- Fiyat sorgulama ucunun döndürdüğü tutar **bağlayıcı değildir**; rezervasyon
  oluşturulurken aynı servisle yeniden hesaplanır. Sorgunun cevabını saklayıp
  rezervasyonda kullanmak, kapıyı bir adım geriye taşımaktan ibaret olurdu
- Para daima **iki haneye** yuvarlanır (`MidpointRounding.AwayFromZero`). Ara
  sonuçta yuvarlanmazsa toplam `CK_Reservations_GrandTotal` kısıtına takılır —
  kısıt tam eşitlik istiyor

## Veritabanı

- **PostgreSQL** → [[api-kararlar]] 2026-08-22
- Erişim EF Core üzerinden; elle SQL istisnadır ve yazıldığında tırnak kuralı geçerlidir

## Yazmadan önce sor

Yeni bir uç nokta veya entity eklemeden önce: bu iş kuralı [[domain-gereksinimler]]'de
tanımlı mı? Değilse önce orada netleşmeli. **Çıkarımla şema kurulmaz** — kurulursa
altı ay sonra "Mert böyle demişti" diye anılır. Cevabı olmayan sorular o dosyanın
"Cevap bekleyenler" tablosunda.

## "Bitti" demeden önce — uç nokta gerçekten çağrılır

`dotnet build` temiz olması uç noktanın doğru yanıt verdiğini **göstermez**.
Derleyicinin göremedikleri:

- Yanlış status kodu · boş veya eksik alanlı gövde
- Yetkisiz erişimin açık kalması
- `DateTime` `Kind` hatası — Npgsql UTC ister, belirsiz `Kind` **çalışma anında** fırlar
- Migration'ın veritabanına gerçekten uygulanmamış olması

**Asgari:** uç noktaya istek at, status kodunu ve gövdeyi gör. Yetki gerektiren bir
uç ise **yetkisiz istekle de** dene — 401 dönmüyorsa iş bitmemiştir.

Panoda `Kanıt:` satırı bu çıktıyı içerir; "derlendi" tek başına kanıt değildir.
Araç zinciri → [[api-araclar]]


İlgili: [[api-notlar]] · [[api-mimari]] · [[api-kararlar]] · [[api-gorevler]] · [[api-araclar]]
