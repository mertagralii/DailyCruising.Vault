---
rol: map
kapsam: api
guncelleme: 2026-09-11
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
  ayrışması mümkün değil.
  ⚠️ Bu **İÇERİ** doğru geçerli. `Quote` dışarı VERİLMEZ → aşağıda
- Fiyat sorgulama ucunun döndürdüğü tutar **bağlayıcı değildir**; rezervasyon
  oluşturulurken aynı servisle yeniden hesaplanır. Sorgunun cevabını saklayıp
  rezervasyonda kullanmak, kapıyı bir adım geriye taşımaktan ibaret olurdu
- Para daima **iki haneye** yuvarlanır (`MidpointRounding.AwayFromZero`). Ara
  sonuçta yuvarlanmazsa toplam `CK_Reservations_GrandTotal` kısıtına takılır —
  kısıt tam eşitlik istiyor

## Oku-değiştir-yaz yarışında kararı veritabanına bırak

İki istek aynı satırı okuyup ikisi de "ben ilkim" diyebiliyorsa, koşulu
`WHERE`'e taşı ve **etkilenen satır sayısına** bak:

```csharp
var etkilenen = await db.Reservations
    .Where(r => r.Id == id && r.Status == ReservationStatus.Paid)
    .ExecuteUpdateAsync(u => u.SetProperty(r => r.Status, ReservationStatus.Boarded), ct);
// 1 -> ilk biziz · 0 -> başkası önce davrandı
```

Koşulu veritabanı değerlendirdiği için kilit ya da eşzamanlılık jetonu
gerekmiyor, ve "ikinci istek" bir HATA değil bilgi olarak dönüyor — tekrar
okutma gibi meşru senaryolarda hata fırlatmak istemiyoruz.

⚠️ `ExecuteUpdateAsync` değişiklik takipçisini ATLIYOR: elindeki nesne hâlâ eski
durumu söyler. `ReloadAsync` şart.

⚠️ Koşullu UPDATE ile ona bağlı kayıtlar (durum geçmişi, okutma satırı) **aynı
işlemde** gitmeli; ayrı olsalardı araya giren bir hata "binmiş görünen ama
okutma kaydı olmayan" bir rezervasyon bırakırdı.

Alternatifi `FOR UPDATE` (projede `ReservationRepository` böyle yapıyor) ve o
da doğru — ama kilit alıyor, kilit sırası sorusu doğuruyor ve aynı sonucu daha
pahalıya veriyor → [[api-kararlar]] 2026-08-25.

## Paralel çalıştırmak yarışı ÜRETMEZ

`Task.WhenAll` ile iki istek başlatmak, o ikisinin gerçekten çakıştığını
göstermez: veritabanı gidiş-dönüşleri hızlıysa istekler pratikte sıralanır ve
ikincisi çakışmaya hiç girmez. Böyle bir test, yarışı üreten kod geri
getirilse bile **yeşil kalır**.

Yarışı ölçmek için çakışmanın anını ELLE kur: iki ayrı bağlam da eski durumu
okusun, sonra ikisi de yazmayı denesin. Paralel test silinmesin ama **kanıt
sayılmasın** — servisin bütününün tutarlı kaldığını gösteren bir duman testidir.

Bir kez yaşandı: koşul kaldırıldığında paralel test yeşil kaldı, elle kurulan
test `Expected 0, Actual 1` ile kırmızıya döndü.

## Denetim kaydının hatası, denetlenen hatanın yerine geçmemeli

Bir reddi kaydedip sonra istisna fırlatan kodda, KAYIT düşerse istisna onun
yerine geçer: çağıran anlamsız bir 500 görür ve reddin sebebi hiçbir yere
yazılmaz. Yani denetim izini korumak için konan kayıt, denetim izini yok eder.

Kayıt yazımı **kendi try/catch'inde** olmalı. "Kayıt işlemi bozmamalı" bir yorum
değil, kod olmalı — bir kez yorum olarak yazıldı ve yalan söylüyordu.

## Kolon adı içeriğiyle uyuşmalı

`FailureReason` alanına başarılı bir okutmanın notunu yazmak kodda çalışır ama
`BoardingScans`'i doğrudan sorgulayan biri (denetim, raporlama) kolonun adına
bakıp yanlış sonuca varır. Ayrı `Note` kolonu açıldı.

Ölçüt: **tabloyu koda bakmadan okuyan biri yanılır mı?**

## Aynı kolona ikinci indeks: adı `HasIndex`'e parametre ver

EF Core indeksleri **property kümesine göre** anahtarlıyor. Aynı kolon üzerinde
iki `HasIndex` çağrısı yaparsan ikincisi birincisini **sessizce eziyor** ve
üretilen şemada tek indeks oluyor.

```csharp
b.HasIndex(x => x.PartnerId);                              // ❌ eziliyor
b.HasIndex(x => x.PartnerId).HasDatabaseName("IX_...");    // ❌ hâlâ eziliyor
b.HasIndex(x => x.PartnerId, "IX_PartnerMembers_PartnerId"); // ✅ ayrı indeks
```

`HasDatabaseName` yalnız birleşmiş indeksin **adını** değiştirir. Bu tuzak
`PartnerMembers`'ta bir kez yaşandı: düz indeks kısmi benzersiz indeks
tarafından eziliyordu, yorum satırı olmayan bir indeksi anlatıyordu ve panelin
en sık sorgusu seq scan yapıyordu → [[api-kararlar]] 2026-08-25.

**Kontrol yolu:** migration üretildikten sonra `psql`'de `\d "Tablo"`. Modelde
yazan indeks orada yoksa ezilmiştir.

## Büyük/küçük harf duyarsız benzersizlik `citext` ile kurulur

Uygulama `ToLower()` ile karşılaştırıp veritabanı düz `text` ile benzersizlik
uyguluyorsa **ikisi farklı kural işletir** ve sessizce ayrışır: uygulama "bu
isim var" derken veritabanında iki satır durur.

Kolon `citext` olduğunda ikisi de aynı semantiği kullanır, `ToLower()`
gereksizleşir ve indeks kullanılabilir kalır. Şemada e-posta, kupon kodu ve
işletme rol adı bu yüzden `citext`.

## Çağırana giden mesaj ile günlüğe giden sebep ayrıdır

`EventLogs` temizlenemiyor. Bir istisnanın mesajı çağıranın gönderdiği veriyi
içerebilir — ona kendi yazdığını geri söylemek sızıntı değil — ama aynı metnin
günlüğe yazılması o veriyi **kalıcı** yapar.

Bu yüzden `PartnerStaffException` iki metin taşıyor: `Message` (ayrıntılı,
çağırana) ve `LogReason` (sabit etiket, günlüğe). Yeni bir ret dalı yazan kişi
`LogReason` vermek zorunda — derleyici hatırlatıyor.

⚠️ "Mesajı temizlemeyi hatırla" bir kural değil, bir umuttur. Bir kez unutuldu
ve kodun kendi yorumu unutmanın imkânsız olduğunu iddia ediyordu
→ [[api-kararlar]] 2026-08-25.

## Mutasyon testinde mutasyonu DOĞRU YERE koy

Enum kısıtlarının testini kanıtlamak için kısıtları veritabanından elle
düşürdüm ve testler **yeşil kaldı**. Sebep: `PostgresFixture.InitializeAsync`
her koşuda `RecreateDatabaseAsync` çağırıyor — veritabanı sıfırdan kuruluyor
ve elle yapılan her değişiklik testler başlamadan siliniyor.

Ölçülen şey "kısıt yokken test ne yapar" değil, **hiçbir şey** oldu.

Kural: mutasyon, test edilen davranışı ÜRETEN kaynağa uygulanır.
Veritabanı şemasını migration üretiyorsa mutasyon **migration dosyasında**
olmalı — canlı şemada değil. Aynısı tetikleyiciler ve indeksler için de
geçerli (2026-08-26).

## Bir testin ADI, ölçtüğü şeyin kanıtı değildir

`Rezervasyonu_olan_kiralama_tipi_silinemiyor` **rezervasyon kurmuyordu**. Yalnız
"rezervasyon yok" halini ölçüyor, sonra silmenin çalıştığını doğruluyordu — yani
adının söylediği yasağı bir kez bile denemedi. Yeşildi, 14 testin arasındaydı ve
yasak tamamen kaldırılsa yine yeşil kalırdı.

Aynı tuzak 2026-08-25'te de kuruldu: `Assert.DoesNotContain("partner.owner",
rol.Key[8..])` — `[8..]` aranan öneki kırpıyordu, iddia her zaman doğruydu.

**İkisinin ortak yanı: kurulum, testin adının söylediği durumu HİÇ yaratmıyordu.**
Mutasyon testi ikisini de yakalar (kuralı kaldır, test yeşil kalıyorsa test
boştur) — ama daha ucuz bir kontrol var: *bu testin kurulumunda, adındaki
koşulun gerçekleştiğini gösteren satır hangisi?* Gösterilemiyorsa test boştur.

## Bir doğrulamanın kırmızıya dönebildiğini görmeden ona güvenme

```csharp
Assert.DoesNotContain("partner.owner", rol.Key[8..]);   // hep geçer
```

`[8..]` tam olarak `"partner."` önekini kesiyor, aranan metin de o önekle
başlıyor. Bu doğrulama **kurulum gereği** hep yeşildi; üretim kodu tam tersini
yapsa bile yeşil kalırdı.

Yeni bir doğrulama yazarken: ölçtüğü şeyi bir an için bozup **kırmızıya
döndüğünü gör**. Dönmüyorsa test değil, süstür.

## İç hesap nesnesi HTTP yanıtı değildir

`Quote` hesabın sonucudur ve rezervasyona dondurulacak her alanı taşır —
`CommissionRate`, `ContractId` dahil. **Müşteriye giden şey `QuoteResponse`**,
alanları tek tek seçilmiş ayrı bir tip.

Neden ayrı tip, `[JsonIgnore]` değil: `[JsonIgnore]` "unutulursa sızar"
davranışıdır, ayrı tip "unutulursa görünmez". Bir uç kimliksizse ve nesne para
taşıyorsa varsayılanın hangi yöne baktığı, tek tek alanların doğruluğundan
önemlidir.

Bu kural bir bulgudan doğdu: `commissionRate` kimliksiz fiyat yanıtında düz sayı
olarak dönüyordu — üstelik tam da onu gizlemek için `A-26` yapılırken
→ [[api-kararlar]] 2026-08-25.

Yeni bir uç yazarken sorulacak: *"döndürdüğüm nesne yalnız bu uç için mi
yazıldı?"* Hayırsa, o uca ait bir yanıt tipi gerekir.

## Bir kısıt eklerken tabloyu kilitleme

EF'in `AddCheckConstraint`'i düz `ALTER TABLE ... ADD CONSTRAINT` üretir; bu
komut **tüm mevcut satırları tararken ACCESS EXCLUSIVE kilidi tutar** — tarama
boyunca tabloya ne okuma ne yazma girer. Büyük ve sıcak bir tabloda (örn.
`Reservations`) bu, satır sayısıyla orantılı bir kesinti penceresidir.

Elle yazılacak desen:

```sql
ALTER TABLE "X" ADD CONSTRAINT "CK_..." CHECK (...) NOT VALID;
ALTER TABLE "X" VALIDATE CONSTRAINT "CK_...";
```

`NOT VALID` kısıtı anında ekler ve **yeni satırlar hemen denetlenir**;
`VALIDATE` eski satırları SHARE UPDATE EXCLUSIVE altında tarar, okuma ve yazma
devam eder.

⚠️ Kısıt adı EF modelindekiyle **birebir aynı** olmalı. Ayrışırsa bir sonraki
migration kısıtı "eksik" sanıp bir kez daha ekler.

## Kolon varsayılanı geçiciyse migration içinde düşürülür

`AddColumn(..., defaultValue: "X")` Postgres'te **kalıcı** bir `DEFAULT` bırakır.
Varsayılan yalnız mevcut satırları doldurmak içinse aynı migration içinde
`ALTER COLUMN ... DROP DEFAULT` gelmeli.

Yoksa model ile veritabanı sessizce ayrışır ve bir sonraki `migrations add`,
konuyla alakasız görünen bir `DROP DEFAULT` migration'ı üretir — kimse nedenini
bilmeden uygular.

## Devredilmiş yönetimin üç duvarı

İşletme sahibi kendi rollerini tanımlayıp çalışanlarını yönetiyor. Bunu güvenli
kılan **üç ayrı duvar** var ve hiçbiri diğerinin yerine geçmiyor:

| # | Duvar | Nerede | Kaldırılırsa |
|---|---|---|---|
| 1 | **Kapsam** — yalnız kendi işletmesi | Depo katmanı, her sorgu `partnerId` alır | Başkasının çalışanını yönetir |
| 2 | **Katalog** — `IsPartnerAssignable` | `Permissions` tablosu + tetikleyici + depo filtresi | Çalışanına komisyon değiştirme yetkisi verir |
| 3 | **Yükselme** — kendinde olmayanı veremez | Servis katmanı, `ICurrentUser.Has` | Yetkisi kısılmış çalışan kendine tam yetki yazar |

Üçüncü duvar en kolay unutulanı ve tek başına en kritiği: ilk ikisi **çağıranın
kim olduğuna bakmaz**. `staff.manage` verilmiş kısıtlı bir çalışan, sahibin
yarattığı tam yetkili rolü kendine atayarak yükselebilirdi — bu yüzden duvar
hem rol YARATMADA hem de rol ATAMADA çalışıyor. Yalnız yaratmada olsaydı iki
adımda aşılırdı.

Canlı doğrulandı (2026-08-25): `staff.manage` + `role.manage` verilmiş ama
`boat.write` verilmemiş bir çalışanın üç yükselme denemesi de reddedildi.

### Kapsam filtresi depo katmanında durur, serviste değil

Her sorgu `partnerId` parametresi alıyor ve `WHERE`'e koyuyor. Servis "bu benim
mi" diye kontrol etmiyor. Sebep: kontrolü unutan yeni bir çağrı yolu, başka
işletmenin verisini **sessizce** döndürürdü. Parametresiz bir "hepsini getir"
metodu bilerek yok.

### Kapsam ihlali 404 döner, 403 değil

403 ("var ama senin değil") bir oracle'dır: çağıran rastgele kimlik deneyerek
rakip işletmelerin rol ve çalışan kimliklerini haritalayabilir. "Yok" ile
"senin değil" ayırt EDİLMİYOR.

Aynı gerekçe hata mesajlarında da geçerli: başka işletmede çalışan biri
eklenmeye çalışıldığında **hangi işletmede olduğu söylenmiyor** — söylenseydi
e-posta deneyerek rakip çalışan listesi çıkarılırdı.

### Sahip rolü sabit anahtardan değil üyelikten tanınır

`Roles.Key == "partner.owner"` karşılaştırması kırılgan: tohumlama değişirse ya
da rol elle yeniden adlandırılırsa sahip koruması **sessizce** devre dışı kalır
ve sahip rolü o an atanabilir hale gelir. Doğrusu `PartnerMembers.IsOwner`
üzerinden okumak.

### "Kaç kişi kullanıyor" ile "silinebilir mi" AYNI soru değil

Çıkarılmış çalışanın satırı duruyor ve `RoleId`'si hâlâ rolü gösteriyor;
`PartnerMembers.RoleId` RESTRICT. Yani:

- panelde gösterilecek sayı → **yalnız aktif** üyeler
- rol silinebilir mi → **hepsi**, `Status` fark etmez

İkisi tek sayımla cevaplanınca "çalışanı çıkar, sonra rolü sil" akışı veritabanı
hatasıyla patlıyordu. Testi yazınca çıktı.

### Çıkarılan çalışanın erişimi ANINDA kesilmez

Kapsam ve yetkiler erişim jetonunun içinde; jeton dolana kadar (en fazla 15 dk)
çalışır. Yenileme yolu kapsamı veritabanından tekrar okuduğu için ondan sonra
kesilir. Bilinen ve kabul edilmiş denge — anında kesmek her istekte veritabanına
gitmeyi ya da iptal listesi tutmayı gerektirir. Acil durumda kullanıcının TÜM
oturumları `Users.Status` üzerinden kapatılabiliyor.

### Reddedilen yetki değişikliği MUTLAKA loglanır

Reddedilen işlem hiçbir satırı değiştirmiyor — yani `EventLogs` dışında hiçbir
yerde izi kalmaz. Yükselme duvarına çarpan bir çağrı ya arayüz hatasıdır ya
kasıtlı denemedir; ikisi de görünmeli.

## Olay günlüğü uca nasıl bağlanır

Mert (2026-08-24): olay günlüğü **ayrıntılı** tutulacak — sezonluk AI raporlarının
besleneceği veri bu. Yeni bir uç yazılırken sorulacak soru: *"bu isteğin izi başka
bir tabloda kalıyor mu?"* Kalmıyorsa olay yazılır.

- **Yazma yeri controller**, servis değil. IP ve `User-Agent` yalnız orada var;
  `Application` katmanı HTTP'yi tanımıyor
- **Başarısız istek de yazılır.** `pricing.quote.failed` kaçırılan satışın doğrudan
  ölçüsü; başarılıyı yazıp başarısızı atlamak veriyi sistematik olarak yanıltır
- **Payload'a ne girebileceği `EventPayloadPolicy` içinde tanımlı.** Olay türü
  başına izin verilen anahtar listesi var; listede olmayan anahtar, iç içe değer
  ve **listesi olmayan olay türü** düşüyor, 512 karakteri aşan metin kırpılıyor,
  4 KB'ı aşan payload tamamen düşüyor. Yeni olay türü eklerken listeye de
  eklenmeli — unutulursa payload sessizce düşer, testi var
  (`Her_olay_turunun_payload_listesi_var`)
- **Kişisel veri listeye ancak AÇIK BİR KARARLA girer.** Bugün tek örnek
  `auth.login.failed` → `email` (Mert, 2026-08-24). Giren her alan `A-12`
  kapsamında ayrıca ele alınır
- **Exception mesajı payload'a yalnız sabit metinse konur.** `PricingException`
  metinlerinin tamamı `PricingService` içinde sabit; yeni bir tane yazılırken bu
  geçerli kalmalı, yoksa kullanıcı girdisi kalıcı tabloya sızar
- **Olay yazımı isteği bozmaz.** `IEventLogger` istisna fırlatmıyor ve iş işleminden
  ayrı kapsamda çalışıyor

## Müşteriye dönen hata: sebep söylenir, oran söylenmez

Kupon reddi bunun örneği. Müşteri **neden** olmadığını görür ("süresi dolmuş",
"bu teknede geçerli değil"); göremediği tek şey **platformun kendi sayısı** —
komisyon dalı "bu turda kullanılamıyor" der, oranı yazmaz.

Ayrım şu: ret sebeplerinin birbirinden **ayırt edilebilmesi** zaten bir miktar bilgi
sızdırır (kodun gerçek olduğu gibi) ve bu bilinçli olarak kabul edildi. Ama iç bir
parametrenin **değerini** yazmak, kaba bir eşiği kesin bir sayıya çevirir — o çizgi
geçilmiyor → [[api-kararlar]] 2026-08-24.

Metnin yanında **makine okunur bir kod** da döner (`CouponRejectionCode`). Arayüz
metne göre dallanmamalı: metin değiştiğinde koşul sessizce bozulur.

## Takvimi işgal eden her yol, bırakan yolu da yazar

`Voyage` satırı yaratan bir kod yolu varsa, onu `Cancelled`'a çeken bir yol da
olmak zorunda. Kısıt `Reservation`'a değil **`Voyage.Status`'a** bakıyor:

```sql
EXCLUDE ... WHERE ("Status" <> 'İptal')   -- Voyage.Status
```

Rezervasyon ölse de sefer takvimi işgal etmeye devam eder. Bu hata iki kez
yapıldı (teklif akışında, sonra A-22'de) → [[api-terk-edilen-sefer-kilidi]].

Sefer YALNIZ canlı rezervasyonu kalmadığında bırakılır — paylaşımlı seferde bir
kişinin vazgeçmesi diğerlerinin turunu iptal etmemeli.

## Müsaitlik tanımı arama ile rezervasyonda AYNI olmak zorunda

Arama "bu tekne o gün satılabilir mi" diye soruyor; rezervasyon aynı soruyu
tekrar soruyor. İki cevap ayrışırsa iki tür zarar var ve **ikincisi sinsi**:

| Ayrışma | Belirti |
|---|---|
| Arama "yer var" der, rezervasyon reddeder | Müşteri huninin sonunda düşer — **şikâyet üretir**, görülür |
| Arama gizler, aslında yer vardır | Tekne sessizce boş gider — **hiçbir hata, hiçbir şikâyet** |

Üç kural rezervasyon yolundan (`ReservationRepository.FindOrCreateVoyageAsync`)
birebir alınmak zorunda:

1. `VoyageType.Block` → tekne o gün hiç satılamaz
2. `IsExclusive` sefer → gün tamamen kapalı (`EX_Voyages_NoOverlapPerBoat`)
3. `Status = Cancelled` sefer → takvimi **BIRAKIR**, koltukları geri verir

Üçüncüsü en kolay kaçırılanı: filtre unutulursa iptal edilmiş bir sefer tekneyi
sonsuza kadar dolu gösterir ve kimse fark etmez → `A-34` mutasyon testi.

**Bebek koltuk tutmuyor** — `Adults + Children`. Bu da iki yerde aynı olmalı.

## "Canlı satış" listesi tek ve aynı

Dört yer aynı soruyu soruyor ve **aynı listeyi** kullanmak zorunda:

    Pending · Paid · Boarded · Completed

C# tarafında tek kaynak: **`ReservationStatuses.Live`**. Yeni bir yerde bu
soruyu soruyorsan diziyi elle yazma, oradan oku.

| Nerede | Dil | Ne için |
|---|---|---|
| `trg_reservation_sync_seats` | SQL | koltuk sayacı |
| `count_live_coupon_redemptions` | SQL | kupon kullanım hakkı |
| `VoyageRelease` (iş + iptal ucu) | C# | seferin bırakılıp bırakılmayacağı |
| `PricingRepository` | C# | kupon sayımının uygulama tarafı |

SQL ile C#'ın eşit kaldığı **teste bağlı**: `Canli_durum_listesi_sql_ile_ayni`
`pg_get_functiondef` okuyup karşılaştırıyor. Derleyici iki dildeki iki sabitin
ayrıştığını göremez.

Biri kayarsa diğerleriyle **sessizce** çelişir. Bir kez oldu: uygulama tüm kupon
kullanımlarını sayarken tetikleyici yalnız canlı olanları sayıyordu — süresi
dolan bir rezervasyondan sonra veritabanı kuponu kabul ederken uygulama
reddediyordu, hiçbir yerde hata görünmeden.

`SoldSeats`'e bakarak "sefer boş mu" sorulamaz: bebek koltuk tüketmiyor, yalnız
bebekli bir rezervasyonda sayaç 0'dır ama rezervasyon canlıdır.

## Kapsam ile bedeli birbirinden türetme

`Coupon.PartnerId` kuponun **nerede geçerli** olduğunu söyler (kapsam).
`Coupon.FundedBy` **bedelini kimin ödediğini** söyler. İkisi bağımsız:

| PartnerId | FundedBy | Anlamı |
|---|---|---|
| null | Platform | Platform kampanyası, her yerde geçerli |
| dolu | Platform | Platformun **tek bir işletmeye özel** kampanyası |
| dolu | Partner | İşletmenin kendi kampanyası |
| null | Partner | **İmkânsız** — `CK_Coupons_FundedBy` engelliyor |

`PartnerId` dolu diye "demek ki işletme karşılıyor" diye yazan kod üçüncü satırı
yanlış tarafa yazar ve bunu kimse fark etmez: iki tarafın da defteri denk
görünür, yalnız yanlış taraftan düşülmüştür.

## Para alanı hangi tabloda yaşarsa oradan okunur

`Reservation.CouponFundedBy` var iken `Coupon.FundedBy`'a bakan bir hakediş
hesabı YANLIŞTIR. Kupon satırı değişebilir; rezervasyon satırı o anın
fotoğrafıdır → "Rezervasyon satın alma anının fotoğrafını çeker" kuralının
devamı. Canlı doğrulandı (2026-08-25): kuponun `FundedBy`'ı `Partner`'dan
`Platform`'a çevrildi, rezervasyon `Partner` kaldı.

Aynı gerekçe `AdultUnitPrice`, `CommissionRate`, `ExchangeRate` için de geçerli;
yeni bir para alanı eklenirken sorulacak soru: *"bu değerin kaynağı sonradan
değişebilir mi?"* Değişebiliyorsa rezervasyona kopyalanır.

## Bir kuralı kaldırırken: neyi dolaylı garanti ediyordu

`trg_coupon_within_commission` görünürde "kupon oranı komisyonu aşamaz" diyordu.
**Dolaylı olarak** garanti ettiği başka bir şey vardı: hakediş negatife düşemez.
Kural kalkınca (Mert / S-10) o ikinci garanti de sessizce gitti — kimse
kaldırmaya karar vermemişti.

Bir kısıt veya tetikleyici kaldırılırken sorulacak: *"bu kural, adının söylediği
şeyin DIŞINDA neyi imkânsız kılıyordu?"* Cevabı yazılı bırakılmazsa altı ay
sonra ortaya çıkan hata, kaldıran değişiklikle ilişkilendirilemez → `S-15`.

## Kilit sırası: `Voyages` → `Coupons`, asla tersi

Rezervasyon yazma yolu sefer satırını kilitliyor, sonra kupon satırını (kupon
tetikleyicisi içinde). Bugün `Coupons`'a başka yazan yok, bu yüzden döngü
imkânsız — canlı doğrulandı, iki oturumda bekleme var deadlock yok.

⚠️ Kupon düzenleme ucu yazılırken bu sıra korunmalı. Önce `Coupons` kilitleyip
sonra `Voyages`'a dokunan bir yol gerçek bir deadlock açar.

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

⚠️ **Testlerin yeşil olması da kanıt değildir — yazılmamış testin yakalayacağı
şey yoktur.** `ListExtrasAsync` çevirileri EF projeksiyonunun İÇİNDE
`ToDictionary` ile topluyordu: derleme temiz, 215 test yeşil, canlı istek
**500** (`The LINQ expression 't => t.LanguageCode' could not be translated`).
Sebep basit — o ucun testi yoktu. **Yazılan her ucun en az bir testi olmalı,
özellikle LİSTE uçlarının**: onlar en çok projeksiyon içerir ve projeksiyon
hataları yalnız çalışma anında görünür (2026-08-26).

Panoda `Kanıt:` satırı bu çıktıyı içerir; "derlendi" tek başına kanıt değildir.
Araç zinciri → [[api-araclar]]


## Yorumun iddiası da ölçülmek zorunda

Kapsam süzgecini iki dala böldüm ve yanına şunu yazdım: *"tek bir
`x == param` yazılsaydı, parametre boşken SQL'de `= NULL`'a çevrilir ve hiçbir
satır dönmezdi."* İddia inandırıcıydı, bilinen bir EF tuzağının adıydı ve
**yanlıştı**: EF Core boş parametreyi `IS NULL`'a çeviriyor.

Nasıl anlaşıldı: mutasyon. Kodu tek dala indirdim, testin kırmızıya dönmesini
bekledim, **yeşil kaldı**. Yani iki dal bir koruma değil fazladan koddu ve
yorum, olmayan bir tehlikeyi anlatıyordu.

⚠️ **Yanlış yorumun bedeli yanlış koddan farklı ama küçük değil:** koda
dokunacak bir sonraki kişi o iddiayı ölçmez, doğru kabul eder ve aynı deseni
gerekmediği yerlere taşır. Yorum "neden" anlatıyorsa, o "neden" bir ÖLÇÜM
olmak zorunda — hatırlanan bir kural değil.

Kural: **bir yorum bir tehlikeyi adlandırıyorsa, o tehlikenin gerçekten var
olduğunu gösteren mutasyon yapılmış olmalı.** Yapılmadıysa yorum "şunu
düşünüyorum" diye yazılır, "şu olur" diye değil (2026-09-04, `A-76`).

## Sıralı kimlik kısaltılırsa çakışır

`Guid.CreateVersion7()` zaman sıralı: ilk **on iki altılık hanesi milisaniye
damgasıdır**. Test verisinde `$"kategori-{Guid.CreateVersion7():N}"[..20]`
yazılmıştı — önek 9 hane yiyor, geriye kimliğin yalnız 11 hanesi kalıyor ve o
11 hanenin tamamı damga. Aynı milisaniyede kurulan iki kategori **aynı
anahtarı** aldı.

Belirtisi kötü: test bir koşuda kırmızı, aynı kodla bir sonraki koşuda yeşil.
Rastgele kırılan bir test, olmayan bir testten kötüdür — insan onu "yine
takıldı" diye geçmeyi öğrenir ve gerçek bir kırılma da aynı yerden geçer.

Kural: **kısaltılacak kimlik rastgele üretilir** (`Guid.NewGuid()`), sıralı
değil. Sıralı kimlik kısaltılmadan kullanılır (2026-09-04).

İlgili: [[api-notlar]] · [[api-mimari]] · [[api-kararlar]] · [[api-gorevler]] · [[api-araclar]]

## Bir kusuru düzeltince İKİNCİ kopyasını ara

Bir kusur bulunduğunda düzeltmek yetmiyor; aynı varsayımın **başka nerede**
durduğunu aramak gerekiyor. 2026-09-11'de bu üç kez ödendi:

| Kusur | İlk kopya | İkinci kopya | Nasıl bulundu |
|---|---|---|---|
| Defter para hareketinden değil rezervasyondan sürülüyor | iade tarafı | tahsilat tarafı | **arandı** — kusur doğmadan kapandı |
| Taşımada seferden türeyen pencere yenilenmiyor | `Reservations.BoardingTokenExpiresAt` | `BoardingTickets.ExpiresAt` | **aranmadı** — web tarayıcıda buldu, müşterinin karekodu çözülmüyordu |
| Sabit tekillik anahtarı tekrar denemeyi engelliyor | taşıma farkı ödemesi | rezervasyonun ilk ödemesi | **arandı** |

⚠️ Ortadaki satır farkı anlatıyor: aranmayan kopya, **kullanıcıya ulaşan**
tek kusur oldu.

**Arama biçimi ucuz ve somut:** kusurun cümlesini kur ("seferden türeyen her
şey taşımada yenilenmeli"), sonra o cümlenin geçtiği bütün alanları listele.
Burada `grep -n "reservation\.\|quote\." RescheduleRepository.cs` ve
`grep -rln "ExpiresAt" Domain/` yetti; ikisi birlikte **üçüncü bir kopya
olmadığını** da gösterdi (`ReviewInvitation.ExpiresAt` gönderim anına bağlı,
sefere değil).

⚠️ **"Üçüncü kopya yok" bir ölçüm olmalı, bir his değil.** Aramadan
"herhalde kalmadı" demek, kusurun ikinci kopyasını bulmayı web'e bırakmakla
aynı şey.

⚠️ **Kopyalar aynı sınıftan olur ama aynı bedeli taşımaz** — web'in aynı gün
kendi tarafında ölçtüğü incelik. Bir sınıfın üç kopyası sırasıyla *sessizce
sıfır gösterme*, *yanlış liste gösterme* ve *yanlış kayıt açma* üretebiliyor.
Bu yüzden "üç kopya buldum" cümlesi bir sayı değil: **her kopyanın bedeli ayrı
ölçülmeli**, yoksa en ucuzuna bakıp hepsini önemsiz sanma riski var. Bugünkü
kendi örneğimde ikinci kopyanın bedeli en ağırdı — müşterinin karekodu
iskelede çözülmüyordu.

İlgili: [[api-kararlar]] · [[api-notlar]]

## Gizli dal: çalışmayan kod ölçülmüyor, ölçülmeyen kod yanlış

Web'in ölçtüğü bir sınıf, aynı gece bende de çıktı: **var olan ama hiç
çalışmayan bir dal**, kusur taşısa bile hiçbir yerde görünmüyor.

Bendeki örnek: `RescheduleStatus.DroppedOnCancellation` değeri enum'da,
veritabanı kısıtında ve **ekranın sözlüğünde** vardı — yani üç yerde
"destekleniyor" görünüyordu. **Hiçbir kod onu yazmıyordu.**

İki katmanlı gizlilik:

1. İptal, bekleyen taşıma talebini düşürmüyordu → müşterinin elindeki ödeme
   bağlantısı **iptal edilmiş bir rezervasyon için çalışmaya devam ediyordu**;
   fark tahsil edilir, rezervasyon yeni sefere taşınırdı.
2. Kod yazmayı **deneseydi bile** olmayacaktı: kolon `varchar(16)`, değer
   22 karakter.

⚠️ **Aramanın biçimi:** bir enum değeri, durum ya da dal eklendiğinde
*"bunu kim YAZIYOR"* diye sor — okunduğu yerleri değil, **üretildiği** yeri
ara. `grep -rn "DroppedOnCancellation" src/` bunu tek komutta gösterdi:
sonuçların hepsi kısıt ve göç dosyasıydı, tek bir atama yoktu.

⚠️ **Bedeli ertelenmiş kusurlar en sinsisi.** Web'in aynı gece bulduğu
kardeş örnek: henüz ucu olmayan bir ekranın satır eşleştirmesi yanlıştı;
kusur uç geldiği gün doğacaktı ve o gün kimse *"acaba eşleştirme doğru mu"*
diye bakmayacaktı, çünkü ekran yeni çalışmaya başlamış olacaktı.

İlgili: [[api-kararlar]] · [[api-notlar]]
