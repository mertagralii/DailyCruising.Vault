---
rol: map
kapsam: api
guncelleme: 2026-08-24
durum: guncel
---

# Veritabanı Şeması

`A-01` çıktısı. Sekiz bölüm; her bölüm Mert'in onayından geçer, **onaysız kod
yazılmaz**. İş kuralının kaynağı [[domain-gereksinimler]]; burada yalnız o
kuralların tabloya dönüşmüş hali var. Çelişirlerse domain dosyası doğrudur.

İsimlendirme: tablo **PascalCase çoğul**, kolon PascalCase, tümü İngilizce
→ [[api-desenler]].

| # | Bölüm | Durum |
|---|---|---|
| 1 | Kimlik ve yetki | ✅ onaylandı 2026-08-24 |
| 2 | Katalog | ✅ onaylandı 2026-08-24 |
| 3 | Kiralama tipleri ve fiyat | ✅ onaylandı 2026-08-24 |
| 4 | Takvim ve sefer | ✅ onaylandı 2026-08-24 |
| 5 | Rezervasyon | sırada |
| 6 | Para | — |
| 7 | Teklif ve mesajlaşma | — |
| 8 | Yan sistemler + olay günlüğü | — |

---

## Bölüm 1 — Kimlik ve Yetki

### Kurucu üç ilke

**Tek `Users` tablosu.** Müşteri, platform personeli, tekne sahibi ve çalışan aynı
tabloda. Ayrı tablolara bölünürse müşteriyken tekne sahibi olan kişinin iki hesabı
olur ve e-posta benzersizliği çakışır.

**Yetkinin iki boyutu ayrı yerde durur.** *Ne yapabilir* → `Roles` + `Permissions`.
*Kimin verisinde* → `PartnerMembers`. İkincisi elle atanmaz, **üyelikten türer** —
"rezervasyonları görebilir" hiçbir zaman "tüm rezervasyonları" demez.

**`Roles.PartnerId` nullable.** `NULL` = platform rolü, dolu = o işletmenin kendi
tanımladığı rol. Devredilmiş yönetim (tekne sahibinin kendi çalışan rolünü açması)
ayrı tablo istemeden bu tek kolonla çözülür.

### Tablolar

#### `Users`

| Kolon | Tip | Not |
|---|---|---|
| Id | uuid | PK, v7 |
| Email | citext | **benzersiz** |
| EmailVerifiedAt | timestamptz? | null = doğrulanmamış |
| PasswordHash | text | |
| FullName | text | |
| Phone | text | SMS zorunlu olduğu için boş geçilmez |
| PhoneVerifiedAt | timestamptz? | |
| PreferredLanguage | text | varsayılan `tr` |
| Status | text | Aktif / Askıda / Kapatıldı |
| LastLoginAt | timestamptz? | |
| CreatedAt, UpdatedAt | timestamptz | |

TCKN / pasaport **burada yok** — 5. bölümde yolcu kaydında. Aracılık fatura modeli
gereği platform müşteriye fatura kesmiyor, dolayısıyla kimlik bilgisine ihtiyacı
yok; yolcu listesi ise tekne sahibinin yasal yükümlülüğü.

#### `Partners` — işletme

| Kolon | Tip | Not |
|---|---|---|
| Id | uuid | PK |
| LegalName, DisplayName | text | ticari unvan / görünen ad |
| TaxNumber, TaxOffice | text | |
| Email, Phone, Address, City | text | |
| Status | text | BasvuruAlindi → Inceleniyor → SozlesmeGonderildi → Aktif · yan dal Reddedildi |
| RejectionReason | text? | red kaydı silinmez |
| AppliedAt, ApprovedAt | timestamptz? | |

Başvuru ayrı tablo değil; aynı kayıt durum değiştirerek ilerler. "Hesap var ama
paneli yok" ara durumu `Status <> Aktif` demektir.

#### `PartnerMembers` — satır bazlı yetkinin tek kaynağı

| Kolon | Tip |
|---|---|
| Id, PartnerId, UserId, RoleId | uuid |
| IsOwner | bool |
| Status | Aktif / Pasif |
| InvitedByUserId, CreatedAt | |

**`UserId` benzersiz** — bir kullanıcı en fazla bir işletmede çalışır (Mert,
2026-08-24). **`RoleId` tekil** — üyelik başına tek rol.

#### `Roles`

| Kolon | Not |
|---|---|
| Id, Name | |
| Key | `platform.admin`, `partner.owner` |
| PartnerId | **nullable** — dolu = işletmeye özel rol |
| IsSystem | bool, silinemez |

#### `Permissions`

| Kolon | Not |
|---|---|
| Id, Key, Name, Category | `reservation.read`, `boat.edit` |
| **IsPartnerAssignable** | bool — güvenlik kilidi |

`IsPartnerAssignable = false` olan yetki, işletme sahibinin çalışanına yetki
verdiği ekranda **listelenmez bile**. Bu kolon olmazsa yetki yükseltme açığı doğar:
tekne sahibi kendi çalışanına komisyon değiştirme veya başka işletmeyi görme
yetkisi verebilir.

Kısıt: `PartnerId` dolu bir rol, yalnız `IsPartnerAssignable = true` yetkiler alabilir.

#### `RolePermissions` · `UserRoles`

`RolePermissions`: (RoleId, PermissionId) bileşik PK.
`UserRoles`: yalnız **platform** rolleri için. İşletme içi rol
`PartnerMembers.RoleId` üzerinden gelir; iki yol karışmaz.

#### `ContractTemplates` · `Contracts`

`Contracts` kritik kolonları:

| Kolon | Not |
|---|---|
| PartnerId, TemplateId | |
| **BodyHtmlSnapshot** | onaylanan metnin o günkü hali |
| **CommissionRate** | numeric(5,2) |
| Status | Taslak / Gönderildi / Onaylandı / İptal |
| ApprovedAt, ApprovedByUserId, **ApprovedIp**, UserAgent | anlaşmazlıkta tek kanıt |
| ValidFrom, ValidTo | |

Zincir: **sözleşme → komisyon oranı → rezervasyona kopya → hakediş.** Oran
`Partners` üzerinde durmaz; işletmenin geçerli oranı aktif sözleşmesindeki orandır.
Oranı değiştirmek yeni sözleşme ve yeni onay gerektirir.

Kısmi benzersiz indeks: bir işletmenin aynı anda tek `Onaylandı` sözleşmesi olur.

#### `ConsentRecords`

`UserId, ConsentType, DocumentVersion, AcceptedAt, Ip, UserAgent`.
KVKK'da onay aldığını söylemek yetmez, ispatı gerekir.

#### `RefreshTokens` · `UserTokens`

`RefreshTokens`: oturum sürdürme. `TokenHash` saklanır, düz metin değil.
`RevokedAt`, `ReplacedById` ile zincir izlenir.
`UserTokens`: e-posta doğrulama ve parola sıfırlama. `Purpose`, `ExpiresAt`,
`ConsumedAt` — tek kullanımlık.

#### `PartnerDocuments`

Başvuru evrakları: `PartnerId, DocumentType, FileKey, UploadedAt`.

### Bu bölümde hangi olaylar kaydediliyor

8. bölümdeki olay günlüğüne yazılacaklar: giriş · başarısız giriş · parola sıfırlama ·
e-posta doğrulama · rol/yetki değişikliği · çalışan ekleme-çıkarma · sözleşme
gönderimi ve onayı · başvuru durumu değişikliği · **platform personelinin işletme
verisine erişimi**.

Sonuncusu bir karardır, teknik ayrıntı değil: platform yetkisi taşıyan kullanıcıda
kapsam filtresi devre dışı kalır, karşılığında her erişim iz bırakır.

---

## Bölüm 2 — Katalog

Ayrım: **tekneye ait olan bir kez girilir**, `tekne × kiralama tipi` ikilisine ait
olan her tip için ayrı (3. bölüm). Karıştırılırsa aynı veri tekrar girilir.

### `Boats`

| Kolon | Tip | Not |
|---|---|---|
| Id | uuid | PK |
| PartnerId | uuid | FK |
| Name, Slug | text | Slug benzersiz, **şimdilik dilden bağımsız tek slug** |
| BoatTypeId, RegionId | uuid | FK |
| MarinaName | text | kalkış noktası |
| Latitude, Longitude | double precision | |
| **CommercialCapacity** | int | satışa açık azami yolcu |
| **LegalCapacity** | int | ruhsattaki kapasite (D2) |
| CabinCount, BedCount, BathroomCount | int | |
| LengthMeters, WidthMeters | numeric(5,2) | |
| BuildYear, LastRefitYear | int? | |
| EngineInfo | text | |
| CaptainName, CrewCount | | |
| Status | text | Taslak / Yayında / Pasif |
| AverageRating, ReviewCount | | sıralama için önden hesaplı |
| CreatedAt, UpdatedAt | timestamptz | |

İki kapasite bilinçli olarak ayrı: satışta `CommercialCapacity`, denetimde
`LegalCapacity`. Tek kolon olsaydı ticari sınır yükseltilirken yasal sınır da
sessizce yükselirdi.

Açıklama metinleri burada değil, çeviri tablosunda.

### Lookup tabloları — hepsi çevrili

`BoatTypes` (gulet, katamaran, yelkenli, motoryat, sürat teknesi…) · `Regions`
(**düz liste, il/ilçe hiyerarşisi yok**) · `Amenities` (klima, şnorkel, wifi…) ·
`Rules` (evcil hayvan, sigara, müzik saati)

### Bağlantı tabloları

| Tablo | İçerik |
|---|---|
| `BoatAmenities` | BoatId + AmenityId |
| `BoatRules` | BoatId + RuleId + `IsAllowed` + Note |
| `BoatCrewLanguages` | BoatId + LanguageCode |

`BoatCrewLanguages` ve `BoatRules` **bilinçli olarak yapılandırılmış, serbest metin
değil** — ancak böyle filtre olurlar. Müşteri kitlesi ağırlıklı yabancı turist;
"mürettebat İngilizce biliyor mu" satın alma kararını doğrudan etkiliyor. Serbest
metin olsalardı aranamazlardı.

### `BoatMedia`

`BoatId, MediaType (Foto/Video), FileKey, SortOrder, IsCover, Width, Height`

Kısmi benzersiz indeks: **tekne başına tek kapak fotoğrafı.**

### `BoatDocuments`

`BoatId, DocumentType (Ruhsat/Sigorta/TurizmBelgesi), FileKey, DocumentNumber,
IssuedAt, ExpiresAt, VerifiedAt, VerifiedByUserId, Status`

**`ExpiresAt` dolduğunda tekne yayında KALIR; tekne sahibine ve platforma uyarı
gider** (Mert, 2026-08-24). Otomatik pasife düşürmek sezon ortasında tekne
sahibinin haberi olmadan satışını durdurur — daha büyük zarar.

### Çeviri tabloları

`BoatTranslations`, `BoatTypeTranslations`, `RegionTranslations`,
`AmenityTranslations`, `RuleTranslations` — hepsi aynı kalıpta:

| Kolon | Not |
|---|---|
| ParentId, LanguageCode | `(ParentId, LanguageCode)` benzersiz |
| çevrilen alanlar | ad, açıklama, kalkış tarifi… |
| **Source** | Manuel / Otomatik |
| **SourceHash** | kaynak (Türkçe) metnin özeti |
| UpdatedAt | |

`Source = Manuel` olan çeviri bir sonraki otomatik çeviriyle **ezilmez**.
`SourceHash` Türkçe metin değişince çevirinin bayatladığını söyler.
İlk sürümde yalnız `tr` satırları dolar.

**Genel `Translations(EntityType, EntityId, Field, Value)` tablosu bilinçli olarak
REDDEDİLDİ:** foreign key kurulamaz, tip güvenliği yoktur, EF Core'da her okuma
elle join olur. Varlık başına ayrı tablo sıkıcı ama doğru.

### Postgres'e özgü

**`unaccent` + `pg_trgm`** — Postgres'te `Çeşme` ile `Cesme` farklı metindir; MSSQL'de
collation bunu kendiliğinden çözüyordu. Bu iki eklenti olmadan müşteri `cesme`
yazınca sıfır sonuç alır. `pg_trgm` ayrıca yazım hatası toleransı verir.

**Koordinat için `double precision` yeterli** — PostGIS ancak "50 km yakınımdaki
tekneler" araması istenirse gerekir. Bölge filtresi varken erken eklemek bakım yükü.

### Bu bölümde hangi olaylar kaydediliyor

Tekne yayına alma/çıkarma · bilgi düzenleme · fotoğraf ekleme-silme · belge yükleme
ve doğrulama · **belge süresinin dolması** · tekne görüntülenmesi (AI analizi için).

---

## Bölüm 3 — Kiralama Tipleri ve Fiyat

### `RentalTypes` — sekiz tip, platform tanımlı

| Kolon | Not |
|---|---|
| Key | `gunluk-tekne`, `ozel-balik`, `konaklamali`… |
| **PricingStrategy** | KişiBaşı / TekneBazlı |
| **OccupancyMode** | Paylaşımlı / Özel |
| **DurationKind** | Günİçi / ÇokGünlü |
| **ExtraDayCount** | konaklamalı = **1**, diğerleri 0 |

"+1 gün" kuralı **kolon**, kod değil. Hem fiyat hem takvim aynı sayıyı okur; kodda
`if (tip == konaklamalı)` yazılsaydı ikinci bir çok günlü tip eklendiğinde o `if`'i
bulmak gerekirdi.

Dağılım: 2 tip kişi başı/paylaşımlı (günlük tekne, günlük dalış), 6 tip tekne
bazlı/özel. Paylaşımlı balık turu **yok**.

### `BoatRentalTypes` — bölümün merkezi

| Kolon | Not |
|---|---|
| BoatId, RentalTypeId | **benzersiz DEĞİL** — aşağıya bak |
| **Name** | çeviri tablosunda: "Sabah Turu", "Öğleden Sonra Turu" |
| StartTime, EndTime | gün içi saat aralığı |
| DurationDays | çok günlü için |
| **WeekStartDay** | haftalık turun sabit kalıbı (Cmt→Cmt) |
| **ListCurrency** | TRY / USD / EUR / GBP |
| **InfantMaxAge, ChildMaxAge** | her tekne kendi sınırını koyar |
| MinPassengers | asgari kişi, opsiyonel |
| IsActive, SortOrder | |

**Aynı teknede aynı kiralama tipinden birden çok satır olabilir** (Mert,
2026-08-24): aynı tekne "günlük tekne turu"nu hem 09:00–13:00 hem 14:00–18:00
satabilir. Kaç tane olacağına tekne sahibi panelden karar verir
→ [[domain-gereksinimler]] "kararı tekne sahibi verir" ilkesi.

Yaş sınırları burada duruyor ve **rezervasyona kopyalanacak** (5. bölüm); yoksa
tekne sahibi "çocuk 0–10" dediğinde geçmiş rezervasyonların kategorileri kayar.

`BoatRentalTypeTranslations`: ad, tur programı, uğranan koylar, dahil/hariç olanlar.

### `Prices` — temel fiyat ve sezon istisnası TEK tabloda

| Kolon | Tip |
|---|---|
| BoatRentalTypeId | uuid |
| **ValidRange** | `daterange` — **NULL = temel fiyat** |
| AdultPrice, ChildPrice, InfantPrice | numeric(12,2) |
| BoatPrice | numeric(12,2) |

Türetilmiş fiyat yok; üç fiyat bağımsız, oran kolonu tutulmaz.

Kısıtlar:

```sql
EXCLUDE USING gist ("BoatRentalTypeId" WITH =, "ValidRange" WITH &&)
UNIQUE ("BoatRentalTypeId") WHERE "ValidRange" IS NULL
```

Birincisi çakışan sezon aralığını **imkânsız** kılar. MSSQL'de karşılığı yoktur;
uygulama kodunda kontrol edilir ve o kontrolü atlayan bir yazma yolu yazıldığında
sessizce bozulur. Temel fiyatın ayrı tablo değil `NULL` aralık olması bilinçli:
fiyat sorgusu tek yerden okur.

### `Extras` — menü ve ek hizmet aynı yapıda

| Kolon | Not |
|---|---|
| BoatRentalTypeId | menü her kiralama tipi için ayrı girilir |
| **ExtraType** | Menü / Hizmet |
| Price | numeric(12,2), **kişi başı**, `ListCurrency`'yi miras alır |
| IsActive, SortOrder | |

**Sezonluk fiyatı YOK** (Mert, 2026-08-24) — yemek maliyeti tur fiyatı kadar
oynamıyor, tekne sahibine gereksiz iş çıkarır. Gerekirse aynı `daterange` yapısı
sonradan eklenir.

Menü ayrı tablo değil, ek hizmetin bir **türü**: "menü dışında ekstra satılan bir
şey olabilir" kararı gereği transfer, ekipman, fotoğraf paketi şema değişmeden
eklenebilsin. Menüde yaş kırılımı yok, paket fiyatı neyse odur.

`ExtraTranslations`: ad ve içerik.

### `Currencies` · `ExchangeRates`

`ExchangeRates`: `Date, CurrencyCode, RateToTry numeric(18,6), Source, FetchedAt`
— `(Date, CurrencyCode)` benzersiz.

**TL eksendir.** Euro fiyatlı tekneyi sterlin görüntüleyen müşteride euro→TL→sterlin
zinciri kurulmaz; her şey TL'ye normalize edilir. Kurlar TCMB'den günlük çekilip
saklanır — "o gün kur neydi" sorusu üç ay sonra da sorulacak.

### Postgres'e özgü

**`daterange` + `EXCLUDE USING gist`** — MSSQL'de karşılığı yok. Veritabanı
kararının asıl gerekçesi; ilk kez burada, 4. bölümde sefer çakışmasında tekrar.

**`btree_gist` eklentisi ŞART** — kısıt `uuid` eşitliğiyle aralık kesişimini aynı
indekste birleştiriyor. Eklenti olmadan Postgres reddeder ve **hata mesajı sebebi
açıkça söylemez**.

**Para daima `numeric`, asla `float`** — `float` 0.1 + 0.2'yi 0.30000000000000004
yapar, komisyonda kuruş kaçar.

### Bu bölümde hangi olaylar kaydediliyor

Fiyat değişikliği (eski→yeni) · sezon aralığı ekleme-silme · menü/ek hizmet
değişikliği · kiralama tipi açma-kapatma · **fiyatsız kalan kiralama tipi**
(satılamıyor demek, tekne sahibine uyarı).

---

## Bölüm 4 — Takvim ve Sefer

Sistemin en kritik bölümü. Altı tablo, ama asıl olan **tek bir kısıt**.

### Kurucu fikir: blok da bir seferdir

`Voyages` tek tablo, iki tür kayıt tutar:

| VoyageType | Ne | Örnek |
|---|---|---|
| **Satış** | müşteriye satılan sefer | 15 Eylül günlük tur |
| **Blok** | tekne sahibinin kapattığı zaman | bakım, kendi kullanımı, mürettebat yok |

Bakım günü için ayrı tablo **bilinçli olarak yapılmadı**. Ayrı olsaydı "sefer
bakımla çakışmasın" diye ikinci bir kontrol yazmak gerekirdi ve o kontrolü atlayan
bir kod yolu er geç yazılırdı. Aynı tabloda tek kısıt ikisini birden kapsıyor.

### `Voyages`

| Kolon | Tip | Not |
|---|---|---|
| Id, BoatId | uuid | |
| BoatRentalTypeId | uuid? | Blok'ta null |
| VoyageType | text | Satış / Blok |
| **TimeRange** | `tstzrange` | seferin işgal ettiği zaman |
| Status | text | Planlandı / İptal / Tamamlandı |
| IsExclusive | bool | kiralama tipinden kopya |
| Capacity | int | koltuk havuzu (paylaşımlı) |
| **SoldSeats** | int | `CHECK (SoldSeats <= Capacity)` |
| MinPassengers | int? | asgari kişi, kopya |
| BlockReason | text? | tekne sahibinin açıklaması |

**Sistemin bel kemiği kuralı:**

```sql
EXCLUDE USING gist ("BoatId" WITH =, "TimeRange" WITH &&)
  WHERE ("Status" <> 'İptal')
```

Mehmet/Cemil senaryosunu çözen şey budur. Cemil'in konaklamalı seferi Mehmet'in
günlük seferiyle kesişiyorsa veritabanı INSERT'i **reddeder** — uygulama kodunda
kontrol yok, unutulacak yer yok, yarış durumu yok.

`WHERE Status <> 'İptal'`: iptal edilmiş sefer takvimi işgal etmemeli.

**Konaklamalının +1 günü ayrı kural değil** — `TimeRange` iki günü kapsayacak
şekilde üretilir (`RentalTypes.ExtraDayCount`), kısıt gerisini halleder. D3'ün
kendiliğinden çözülmesi budur.

**Paylaşımlı sefer tembel oluşur:** ilk rezervasyonda `(BoatId, BoatRentalTypeId,
tarih)` için sefer aranır, yoksa açılır. İki müşteri aynı anda alırsa ikisi de
sefer açmasın diye o üçlüde benzersiz indeks var.

### `CalendarModeRules` — mod bazlı takvim

| Kolon | Not |
|---|---|
| BoatId | |
| **ValidRange** | `daterange` |
| **Mode** | Paylaşımlı / ÖzeleAçık |
| **Priority** | int — büyük olan kazanır |
| Note | |

`Priority`, "istisna günler tek tek işaretlenebilir" isteğini karşılar: tekne sahibi
"1 Haziran–30 Eylül paylaşımlı" (öncelik 0) der, sonra "15 Eylül özel'e açık"
(öncelik 1) ekler — aralığı üçe bölmesi gerekmez.

Kısıt: `EXCLUDE ... ("BoatId" WITH =, "Priority" WITH =, "ValidRange" WITH &&)` —
aynı katmanda çakışma yasak, farklı katmanda serbest.

**`Boats.DefaultCalendarMode`** (Mert, 2026-08-24): tekne eklenirken varsayılan mod
sorulur. Böylece "mod tanımlanmamış tarih" boşluğu hiç oluşmaz ve karar tekne
sahibinin panelinde kalır → [[domain-gereksinimler]] TASARIM İLKESİ.

### `VoyageStatusHistory` · `WeatherCancellations`

`VoyageStatusHistory`: durum geçişleri — kim, ne zaman, neden.
`WeatherCancellations`: `VoyageId, DeclaredByUserId, DeclaredAt, Reason`. D5'te
"şimdilik sadece ölçelim" denildi; **ölçmek için tablo bugün gerekiyor**.

### `AvailabilityDays` — YAPILMADI

Özet/önbellek tablosu bilinçli olarak kurulmadı; arama canlı sorguyla çalışıyor.
Gerekçe ve geri dönüş eşiği (p95 > 300 ms veya 300+ tekne)
→ [[domain-gereksinimler]] 2026-08-24.

### Postgres'e özgü

**`tstzrange` ve yarı açık aralık `[)`** — bu bölümün en önemli teknik detayı.
Başlangıç dahil, bitiş hariç. Sabah turu `[09:00, 13:00)` ile öğleden sonra turu
`[13:00, 17:00)` **çakışmaz**. Kapalı aralık kullanılsaydı 13:00 ikisine de ait
olurdu ve tekne sahibi günde iki tur satamazdı — 3. bölümde açtığımız özellik
çalışmazdı.

**Kısmi `EXCLUDE`** (`WHERE Status <> 'İptal'`) — iptal edilen seferin takvimi
bırakması bu tek satırla olur.

**Saat dilimi:** her şey UTC saklanır, "gün" kavramı `Europe/Istanbul`'a göre
yorumlanır. `tstzrange` saat dilimi taşıdığı için yaz saati geçişinde kayma olmaz;
MSSQL'de `datetime2` ile bu elle yönetilirdi.

### Bu bölümde hangi olaylar kaydediliyor

Sefer açılması · sefer dolması · **asgari kişi dolmadığı için iptal** · blok
ekleme-kaldırma · takvim modu değişikliği · hava iptali ilanı · sefer tamamlanması.

İlgili: [[api-desenler]] · [[api-kararlar]] · [[api-mimari]] · [[api-gorevler]] · [[domain-gereksinimler]] · [[durum]]
