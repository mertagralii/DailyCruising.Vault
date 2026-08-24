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

**Sekiz bölümün tamamı 2026-08-24'te onaylandı.** 1–5 tek tek konuşuldu; 6–8'i
Claude tasarlayıp açık soruları toplu sordu, Mert hepsini cevapladı
→ [[api-kararlar]] 2026-08-24.

| # | Bölüm | Durum |
|---|---|---|
| 1 | Kimlik ve yetki | ✅ onaylandı 2026-08-24 |
| 2 | Katalog | ✅ onaylandı 2026-08-24 |
| 3 | Kiralama tipleri ve fiyat | ✅ onaylandı 2026-08-24 |
| 4 | Takvim ve sefer | ✅ onaylandı 2026-08-24 |
| 5 | Rezervasyon | ✅ onaylandı 2026-08-24 |
| 6 | Para | ✅ onaylandı 2026-08-24 |
| 7 | Teklif ve mesajlaşma | ✅ onaylandı 2026-08-24 |
| 8 | Yan sistemler + olay günlüğü | ✅ onaylandı 2026-08-24 |

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
| Id | uuid | PK, **v7** — `DEFAULT uuidv7()`, PostgreSQL 18 yerleşiği |
| Email | citext | **benzersiz** |
| EmailVerifiedAt | timestamptz? | null = doğrulanmamış |
| **PendingEmail** | citext? | doğrulanmamış YENİ adres burada bekler |
| **AnonymizedAt** | timestamptz? | KVKK: hesap silinemiyor, anonimleştiriliyor |
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

Kısıt: `PartnerId` dolu bir rol, yalnız `IsPartnerAssignable = true` yetkiler
alabilir. **Bu kural plpgsql tetikleyiciyle veritabanında zorlanıyor** — CHECK
başka tabloya bakamadığı için başka yolu yok.

#### `RolePermissions` · `UserRoles`

`RolePermissions`: (RoleId, PermissionId) bileşik PK.
`UserRoles`: yalnız **platform** rolleri için. İşletme içi rol
`PartnerMembers.RoleId` üzerinden gelir; iki yol karışmaz.

### Üç tetikleyici — yetki modelinin gerçek kilidi

2026-08-24 denetiminde bu üç kuralın **yalnız yorum satırında** yazdığı, veritabanında
karşılığı olmadığı bulundu. Üçü birleşince bir çalışan başka bir işletmenin verisini
görebiliyordu. Artık `Bolum1_GuvenlikTetikleyicileri` migration'ında:

| Tetikleyici | Engellediği |
|---|---|
| `trg_partner_member_role_scope` | Çalışana başka işletmenin veya platformun rolünü atamak |
| `trg_role_permission_assignable` | İşletme roluna `IsPartnerAssignable = false` yetki bağlamak |
| `trg_user_role_is_platform` | `UserRoles`'a işletme rolü koymak |

Yabancı anahtar bunları ifade edemiyor: FK "bu satır var mı" der, **"bu satır doğru
satır mı" demez**.

`Roles` üzerinde ayrıca **iki ayrı** kısmi benzersiz indeks var, tek bileşik indeks
değil: Postgres'te NULL başka bir NULL'a eşit sayılmadığı için `(PartnerId, Key)`
benzersizliği platform rollerinde hiçbir şey engellemiyordu — iki tane
`platform.admin` açılabiliyordu.

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

`RefreshTokens`: oturum sürdürme. **`TokenSha256`** saklanır, düz metin değil.
`RevokedAt`, `ReplacedById` ile zincir izlenir.
`UserTokens`: e-posta doğrulama, parola sıfırlama ve **e-posta değiştirme**.
`Purpose`, `ExpiresAt`, `ConsumedAt` — tek kullanımlık; `CreatedIp`/`UserAgent`
oran sınırlama ve adli iz için.

⚠️ **Kolon adı bilerek `TokenSha256`.** Parolalarda kullanılan bcrypt/argon2 buraya
UYMAZ — her çağrıda farklı çıktı verdikleri için `WHERE TokenSha256 = @hash` hiç
eşleşmez. Jeton zaten yüksek entropili; yavaş hash değil **deterministik** hash gerekiyor.

⚠️ **`PendingEmail` neden var:** `EmailVerifiedAt` tek başına *hangi* adresin
doğrulandığını söylemiyor. Saldırgan kendi adresiyle doğrulayıp sonra e-postasını
kurbanınkiyle değiştirirse, değiştirme kodu `EmailVerifiedAt`'i sıfırlamayı
unuttuğu anda kurbanın geçmiş misafir rezervasyonları saldırgana bağlanır.
`PendingEmail` bunu yapısal olarak imkânsız kılıyor: `Email` ancak jeton
kullanılınca değişiyor.

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
| **Teklif** | 48 saat tarihi tutan özel teklif | 7. bölümde eklendi |

Bakım günü için ayrı tablo **bilinçli olarak yapılmadı**. Ayrı olsaydı "sefer
bakımla çakışmasın" diye ikinci bir kontrol yazmak gerekirdi ve o kontrolü atlayan
bir kod yolu er geç yazılırdı. Aynı tabloda tek kısıt ikisini birden kapsıyor.

### `Voyages`

| Kolon | Tip | Not |
|---|---|---|
| Id, BoatId | uuid | |
| BoatRentalTypeId | uuid? | Blok'ta null |
| VoyageType | text | Satış / Blok / **Teklif** |
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

---

## Bölüm 5 — Rezervasyon

Bölümün tek büyük fikri: **rezervasyon fotoğraf çeker.**

### `Reservations`

**Kimlik ve durum**

| Kolon | Not |
|---|---|
| **Code** | rastgele, **sıralı değil**, benzersiz; `0/O`, `1/I/l` kullanılmaz |
| VoyageId, BoatRentalTypeId | |
| **UserId** | **nullable** — misafir rezervasyonu birinci sınıf senaryo |
| ContactFullName, ContactEmail, ContactPhone | **kopya**, referans değil |
| ContractId | **FK, Contracts** — dondurulan oranın kaynağı |
| Status | Beklemede → Ödendi → Binildi → Tamamlandı · yan dal SüresiDoldu / İptal / İade |
| **HoldExpiresAt** | 15 dakika |
| AdultCount, ChildCount, InfantCount | |
| **BoardingTokenSha256** | QR jetonunun **SHA-256 özeti** — düz metin saklanmıyor |
| BoardingTokenExpiresAt | jeton süresiz geçerli kalmasın diye |

İletişim bilgisi profilden kopyalanır: kullanıcı altı ay sonra e-postasını
değiştirse geçmiş rezervasyonun o günkü bilgisi bozulmamalı.

**Dondurulan alanlar — bölümün asıl konusu**

| Grup | Kolonlar |
|---|---|
| Fiyat | AdultUnitPrice, ChildUnitPrice, InfantUnitPrice, BoatPrice |
| Yaş sınırı | InfantMaxAge, ChildMaxAge |
| Para birimi | ListCurrency, ListTotal, **ExchangeRate**, ExchangeRateDate, TotalTry |
| Komisyon | **CommissionRate**, ContractId |
| Kural | RequiresPassengerList |
| Toplam | ExtrasTotal, CouponId, DiscountAmount, **GrandTotalTry** |

Ortak gerekçe: tekne sahibi yarın fiyatı, yaş sınırını veya sözleşmesini
değiştirebilir. Referansla bağlansaydı geçmiş rezervasyonların tutarı ve hesaplanmış
komisyonu **geriye dönük bozulur**, hakediş yanlış çıkardı.

`ExchangeRate` özellikle kritik: €500'lük tekne 1 Temmuz'da 35 kurdan 17.500 TL
ödendi; Eylül'de kur 40 olsa da hakediş 17.500 TL üzerinden. Kur dondurulmazsa
platform tahsil etmediği parayı ödemek zorunda kalır.

### `ReservationExtras`

`ReservationId, ExtraId, ExtraType, NameSnapshot, UnitPrice, Quantity, LineTotal`

`NameSnapshot` var çünkü tekne sahibi "Menü 1"in içeriğini değiştirebilir; müşterinin
ne satın aldığı kaybolmamalı.

### `Passengers`

`ReservationId, FullName, BirthDate, IdentityType (TCKN/Pasaport/YabancıKimlik),
IdentityNumber, Nationality?, FilledByUserId, CreatedAt`

Yalnız teknenin **"yolcu listesi ister"** anahtarı açıkken doldurulur. Kimlik verisi
"lazım olur diye" değil, tekne sahibinin beyan ettiği yasal yükümlülük gerekçesiyle
toplanır — KVKK m.4'ün istediği belirli ve meşru amaç.

`FilledByUserId`: eksik bilgiyi tekne sahibi biniş sırasında panelden girebilir;
kimin girdiği anlaşmazlıkta lazım. **Eksik yolcu bilgisi binişi ENGELLEMEZ.**

Rezervasyonu yapan mutlaka yolcu değildir; form onun bilgisiyle önden dolu gelir
ama silinebilir.

### `BoardingScans`

`ReservationId, ScannedByUserId, ScannedAt, Method (Kamera/Klavye/**Manuel**), DeviceInfo`

Her okutma ayrı satır — sadece ilki değil. İlk okutma `BoardedAt`'i set eder ve iki
şeyi tetikler: **yorum hakkı doğar**, **mesajlaşma kapanır**.

`Manuel` değeri çevrimdışı biniş için (G-12): internet yoksa tekne sahibi sonradan
panelden işaretler. Çevrimdışı kuyruk mobil uygulamayla gelecek; o zaman eklenecek
tek şey `ClientRecordedAt` ve `SyncedAt` → [[domain-gereksinimler]] 2026-08-24.

### `ReservationStatusHistory`

Her durum geçişi: kim, ne zaman, neden. Para anlaşmazlığında elde tutulacak kayıt.

### Rezervasyon DEĞİŞİKLİĞİ yok — yalnız iptal

İlk sürümde müşteri kişi sayısını veya tarihi değiştiremez; iptal edip yeniden alır.
Hava muhalefetindeki tarih değişikliği ayrıdır ve durur. `ReservationAmendments`
gelecek sürümde → [[domain-gereksinimler]] 2026-08-24.

### Kapasite ve 15 dakika — asıl mühendislik

Rezervasyon `Beklemede` açıldığı anda `Voyages.SoldSeats` artar. Üç katman:

```sql
CHECK ("SoldSeats" <= "Capacity")                              -- 1. gerçek garanti
SELECT * FROM "Voyages" WHERE "Id" = @id FOR UPDATE;           -- 2. satır kilidi
CREATE INDEX ... ON "Reservations" ("HoldExpiresAt")
  WHERE "Status" = 'Beklemede';                                -- 3. temizlik işi
```

Asıl garanti **1**; kilit yalnız oku-değiştir-yaz döngüsünün doğruluğu için. Son iki
koltuk için aynı anda ödeyen iki müşteri olursa biri `CHECK` ihlaliyle geri döner.
**Yük meselesi değil, doğruluk meselesi** — 100 kullanıcıyla da olur.

### Misafir → üye bağlama

Aynı e-postayla üye olan geçmiş misafir rezervasyonlarını görür. Tek `UPDATE`, ama
şartı kritik: **yalnızca e-posta doğrulandıktan sonra**. Doğrulanmamış e-postayla
üye olmak başkasının rezervasyonlarını devralmak demek olurdu — 1. bölümdeki
`EmailVerifiedAt` bunun için var.

### Kod ile sorgulama

**Kod + e-posta** veya **kod + telefon**; kod tek başına yetmez. Sorgulama ucu hız
sınırlı olmalı, yoksa kod denemesi otomatikleştirilir.

### Postgres'e özgü

**`SELECT ... FOR UPDATE`** — MSSQL'deki `UPDLOCK` ipucunun karşılığı.

**Kısmi indeks** — süresi dolanları arayan iş, tabloda milyon satır olsa bile yalnız
`Beklemede` olanların indeksini tarar; o indeks 20 satır büyüklüğünde kalır.

**`SERIALIZABLE` kullanılmıyor** — Postgres destekliyor ama çakışan işlemi iptal edip
yeniden denemeyi istiyor. `CHECK` + satır kilidi bu iş için daha basit ve öngörülebilir.

### Bu bölümde hangi olaylar kaydediliyor

Rezervasyon açılması · **terk edilen ödeme** (süresi dolan hold — AI analizi için
değerli) · ödeme başarısı/başarısızlığı · yolcu bilgisi doldurma · biniş okutma ·
**başarısız biniş denemesi** · iptal · durum geçişleri.

---

## Bölüm 6 — Para

Tek kural: **hiçbir para kaydı güncellenmez, sadece eklenir.**

### `LedgerEntries` — defter

| Kolon | Not |
|---|---|
| ReservationId, PartnerId | |
| **AccountType** | Müşteri / Platform / İşOrtağı |
| EntryType | Tahsilat / Komisyon / Hakediş / İade / KuponGideri |
| **Amount** | numeric(12,2), **işaretli** |
| OccurredAt, CreatedAt | |
| **ReversesEntryId** | düzeltme kaydı; silme yok |
| PayoutId | hangi hakedişe girdi |

Bir rezervasyonun tüm satırlarının toplamı **her zaman 0**. Muhasebe süsü değil,
hata yakalama aracı: kod yanlış hesaplarsa toplam sıfırdan sapar ve tek sorguyla
bulunur.

1000 TL tur, %15 komisyon, %10 kupon:

| Hesap | Tutar |
|---|---|
| Müşteri (tahsilat) | +900 |
| İş ortağı (hakediş) | −850 |
| Platform | −50 |
| **Toplam** | **0** |

Kuponun 100 TL'sinin tamamı platformdan çıkar — tekne sahibinin hakedişi liste
fiyatı üzerinden.

**Düzeltme = ters kayıt.** Yanlış komisyon `UPDATE` edilmez; eksi işaretli yeni
satır atılıp doğrusu eklenir.

### `Payments` · `Refunds`

`Payments`: `ReservationId, Provider, ProviderTransactionId, Amount, Status,
RawResponse jsonb, IdempotencyKey`

Sanal POS henüz seçilmedi (`G-03`). `RawResponse` sağlayıcının ham cevabını olduğu
gibi saklar. `IdempotencyKey` şart — ödeme sağlayıcıları webhook'u iki kez gönderir;
bu varsayım değil kuraldır.

`Refunds`: `ReservationId, PaymentId, Amount, Reason (MüşteriIptali/HavaIptali/
NoShow/Platform), RequestedByUserId, ProviderRefundId, Status`

### `Payouts` — hakediş

`PartnerId, PeriodStart, PeriodEnd, TotalAmount, Status, ProviderInstructionId,
SettledAt`

Kolon adı bilinçli `ProviderInstructionId`, `PaymentId` değil: para platformun
hesabında değil **sağlayıcıda** bekler; hakediş bizim ödememiz değil, sağlayıcıya
verilen **bölüştürme talimatıdır**.

Periyodik olmasının yan etkisi: iptalde para hâlâ sağlayıcıda olduğu için tekne
sahibinden komisyon **geri istenmez**, sadece hiç kazanılmamış olur.

### `Coupons` · `CouponRedemptions`

`Coupons`: `Code, Percentage numeric(5,2), ValidFrom, ValidTo, MaxRedemptions,
UsedCount, Scope, IsActive`

**Kupon oranı komisyon oranını aşamaz** — global kontrol edilemez, çünkü komisyon iş
ortağı bazında. Doğrulama kuponun uygulandığı an, o rezervasyonun ortağının oranına
karşı yapılır. Aşan kupon o teknede **geçersiz sayılır, kırpılmaz**.

### `Invoices`

`IssuerType, IssuerPartnerId, RecipientType, RecipientPartnerId, InvoiceType, Number,
IssuedAt, Amount, TaxAmount, PayoutId, FileKey`

Aracılık modeli: hizmeti tekne sahibi verir, müşteriye faturayı o keser; platform iş
ortağına komisyon faturası keser. **Yön bir alandır** — mali müşavir (`G-13`) başka
derse şema değil veri değişir.

### Postgres'e özgü

**`jsonb`** — MSSQL'de JSON `nvarchar(max)` içinde saklanır ve üstünde arama zordur;
Postgres'te gerçek bir tiptir, GIN indeksiyle sorgulanır. Sağlayıcı seçilmeden şema
kurabilmemizin sebebi bu.

**Tablo gerçekten değişmez yapılabilir** — `LedgerEntries` üzerine `UPDATE`/`DELETE`
tetikleyiciyle engellenir. "Kimse güncellemesin" kod kuralı olarak kalmaz.

⚠️ **Satır bazlı tetikleyici tek başına YETMİYOR.** Tabloyu boşaltma komutu ayrı
bir olay sınıfıdır ve satır tetikleyicilerini hiç çalıştırmaz — 2026-08-24'te canlı
doğrulandı, değişmez sanılan defter tek komutla boşaldı. Deyim bazlı tetikleyici
ayrıca eklendi. Kalıcı çözüm, uygulama rolünün bu yetkiye hiç sahip olmaması,
görev `A-10`.

⚠️ **Fatura numarası için `SEQUENCE` KULLANILMAYACAK.** Postgres dizileri (MSSQL
`IDENTITY` gibi) **boşluk bırakır**: işlem geri alınırsa o numara kaybolur. Türk
vergi mevzuatı fatura numarasının kesintisiz olmasını ister. Doğrusu ayrı bir sayaç
tablosu, `FOR UPDATE` ile kilitlenip artırılır. Sonradan fark edilirse düzeltmesi
çok pahalı bir hatadır.

### 🟡 Claude'un iki kararı — Mert'in onayı bekleniyor

**S6-1 — Kuponlu rezervasyonda kısmi iade: (b).** 1000 liste, %15 komisyon, %10
kupon, yarısı iade → tekne sahibi **425**, platform **25**. (a) "komisyon =
müşteride kalmayan × oran" 382,50 / 67,50 verirdi.
**Gerekçe:** kupon kararının mantığı "indirimi platform karşılar"dı; iadede tekne
sahibine yükletmek o kararı yarıda bırakır. **Bedeli:** platformun payı 25'e düşer.

**S6-2 — Hakediş periyodu: iki haftada bir, sözleşmede yazılı**
(`Contracts.PayoutPeriodDays`). **Gerekçe:** kısa periyot döviz fiyatlı teknelerde
kur riskini azaltır, uzun periyot işlem masrafını. Komisyon oranı zaten sözleşmede;
ikisi aynı yerde dursun ve ortak bazında değişebilsin.

### Bu bölümde hangi olaylar kaydediliyor

Ödeme başlatma / başarı / başarısızlık · terk edilen ödeme · iade talebi ve sonucu ·
kupon uygulama ve **reddedilen kupon denemesi** · hakediş oluşturma ve talimat
verme · fatura kesme · defter düzeltmesi.

---

## Bölüm 7 — Teklif ve Mesajlaşma

### `Offers` — özel teklif

| Kolon | Not |
|---|---|
| ConversationId, BoatRentalTypeId | |
| **VoyageId** | tarihi tutan sefer kaydı |
| CreatedByUserId | teklifi gönderen tekne sahibi |
| **CustomerUserId** | **zorunlu** — mesajlaşma için giriş şart (Mert, 2026-08-24) |
| TotalAmount, Currency | |
| **ExpiresAt** | gönderimden **48 saat** |
| Status | Gönderildi / Kabul / Ret / SüresiDoldu / İptal |
| ReservationId? | kabul edilince doğan rezervasyon |

**Teklif tarihi nasıl tutuyor:** 4. bölümdeki `Voyages` tablosuna
**`VoyageType = Teklif`** değeri eklendi. Teklif gönderilince o sefer açılır ve
`EXCLUDE` kısıtı sayesinde başkası o tarihi satın alamaz. Süre dolunca sefer
`İptal`e çekilir, tarih serbest kalır.

Ayrı bir "tarih rezervasyonu" mekanizması yazılmadı — 15 dakikalık `Beklemede`
holdüyle aynı yapı, farklı süre. Tek kısıt üç senaryoyu birden taşır.

`OfferItems`: `OfferId, ExtraId, NameSnapshot, UnitPrice, Quantity` — teklife menü
ve ek hizmet dahil edilebilir. Komisyon normal oranla aynı; her kiralama tipinde açık.

### `Conversations` — (müşteri × tekne)

| Kolon | Not |
|---|---|
| BoatId, CustomerUserId | |
| Status | Açık / Kapalı |
| ClosedAt, **ClosedReason** | Biniş / TarihGeçti / Manuel |
| LastMessageAt | |

Konuşma **rezervasyona bağlı değil** — rezervasyondan önce açılır. Rezervasyon
konuşmaya `ConversationReservations` ile iliştirilir.

**Kapanma:** QR okutulup biniş resmileştiğinde. Biniş hiç olmazsa tur tarihi geçince
otomatik.

### `Messages`

| Kolon | Not |
|---|---|
| ConversationId, SenderUserId, SenderRole | |
| **Body** | orijinal — yalnız platform yönetimi görür |
| **MaskedBody** | herkesin gördüğü, telefon/e-posta gizli |
| **MaskedItemCount** | kaç kez maskelendi |
| ReadAt, CreatedAt | |

Orijinal saklanır çünkü anlaşmazlıkta platformun elinde kayıt kalmalı; ama API asla
`Body` döndürmez.

`MaskedItemCount` suistimal sinyalidir: ısrarla numara paylaşmaya çalışmak platform
dışına kaçış girişimidir.

### Destek talepleri AYRI

Mesajlaşma (müşteri ↔ tekne sahibi) ile destek (müşteri ↔ platform) birleştirilmedi —
Mert'in açık tercihi. Destek 8. bölümde.

---

## Bölüm 8 — Yan Sistemler ve Olay Günlüğü

### `Reviews` · `ReviewScores` · `ReviewCriteria` · `ReviewReplies` · `ReviewInvitations`

`Reviews`: `ReservationId (**benzersiz**), BoatId, **Rating 1–5 (genel)**, Body,
Status (Beklemede/Onaylandı/Reddedildi), ModeratedByUserId, ModeratedAt`

**Alt puanlar da var** (Mert, 2026-08-24):

| Tablo | İçerik |
|---|---|
| `ReviewCriteria` | `Key, SortOrder, IsActive` — temizlik, mürettebat, yemek, fiyat/değer, güvenlik, tekne durumu |
| `ReviewCriterionTranslations` | başlıkların çevirisi |
| `ReviewScores` | `ReviewId, CriterionId, Score 1–5` — `(ReviewId, CriterionId)` benzersiz |

**Alt puanlar OPSİYONEL, genel puan zorunlu.** Gerekçe: menü almamış müşteri "yemek"
puanı veremez; zorunlu olsaydı ya boş yere puan verirdi ya yorumu hiç yazmazdı.

**Kriterler ayrı tabloda, kolon değil.** Yeni kriter eklemek şema değişikliği
gerektirmez ve **eski yorumlar bozulmaz** — yalnız o kriterde puanları olmaz.
Kolon olsaydı her yeni kriterde tüm geçmiş yorumlar `NULL` ile dolar ve ortalama
yanlış çıkardı.

Kriterleri **platform** tanımlar, tekne sahibi değil — teknelerin karşılaştırılabilir
kalması için. Bu, "kararı tekne sahibi verir" ilkesinin sınırına giren bir konu:
ayarlanabilir olan işletme tarzıdır, platformun ölçüsü değil.

Tekne başına kriter ortalamaları **canlı hesaplanır**, önden tutulmaz —
`AvailabilityDays` ile aynı gerekçe.

Yorum hakkı rezervasyon yapmakla değil **QR okutulmakla** doğar; yorum yayına
girmeden **platform onayından** geçer. Tekne sahibi cevap yazabilir.

`ReviewInvitations`: `ReservationId, TokenHash, SentAt, ExpiresAt, UsedAt` — tek
kullanımlık ve süreli jeton. Üyelik gerekmez; hak rezervasyona bağlıdır.

### `BlogPosts` · `BlogPostTranslations` · `BlogCategories`

`AuthorUserId, AuthorPartnerId?, Slug, Status (Taslak/İncelemede/Yayında),
PublishedAt, **ApprovedByUserId**, **ApprovedAt**, CoverFileKey, ViewCount`

Hem platform hem tekne sahipleri yazabilir. **Tekne sahibinin yazısı platform
onayından geçer** (Mert, 2026-08-24) — yazı platformun adı altında yayınlanıyor.
Platform yönetiminin kendi yazısı onay beklemez.

### `SupportTickets` · `SupportMessages`

`SupportTickets`: `Code, UserId?, ContactEmail, Subject, Category, Priority, Status,
AssignedToUserId, ReservationId?, CreatedAt, **FirstResponseAt**, **ResolvedAt**`

Son iki kolon süs değil: destek personeli sezon raporunun ("ilk cevap süresi",
"çözüm süresi") tek veri kaynağı. Bugün açılmazsa o rapor hiç üretilemez.

`SupportMessages`: `TicketId, SenderUserId, Body, **IsInternal**, CreatedAt` —
`IsInternal` personelin kendi arasındaki not, müşteri görmez.

### `NotificationTemplates` · `Notifications` · `NotificationDeliveries`

Üç tablo, çünkü aynı bildirim hem e-posta hem SMS olarak gider ve her kanalın kaderi
ayrıdır: e-posta gitti, SMS başarısız olabilir.

`NotificationDeliveries`: `NotificationId, Channel, Provider, ProviderMessageId,
Status, SentAt, FailedAt, Error`

Şablonlar çevrili — i18n ertelendi ama şema ertelenmedi.

### `EventLog` — bölümün asıl sebebi

| Kolon | Not |
|---|---|
| Id | uuid **v7**, zaman sıralı |
| **Seq** | bigint identity — dışarıdan tüketim için imleç |
| OccurredAt | timestamptz |
| EventType | `search.performed`, `boat.viewed`, `payment.abandoned`… |
| ActorUserId?, ActorType | Müşteri/TekneSahibi/Platform/Sistem/Anonim |
| SessionId? | giriş yapmamış ziyaretçiyi oturum içinde izlemek için |
| SubjectType, SubjectId | neyle ilgili |
| PartnerId?, BoatId? | rapor kırılımları |
| **Payload jsonb** | olaya özgü alanlar |
| IpHash?, UserAgent? | ham IP değil, **özet** |

**Değişmez ve append-only** — para defteriyle aynı mantık.

Arama sorguları için ayrı tablo **açılmadı**; `search.performed` olayının
`Payload`'ında filtreler ve sonuç sayısı durur. Yeni olay türü eklemek şema
değişikliği gerektirmez — "veri önce, entegrasyon sonra" ilkesinin karşılığı bu.

`Seq` neden var: n8n gibi dış tüketiciler `WHERE Seq > sonOkunan` ile ilerler.
Diziler boşluk bırakır ama **sıra bozulmaz** — imleç için yeterli, faturada
yetersizdi.

⚠️ **KVKK:** ham IP değil `IpHash` saklanır. Rapor üretmek ile pazarlama amaçlı
profilleme farklı hukuki dayanaklardır; kayıt altyapısı ortak olsa da izin ayrı
yönetilir → 1. bölüm `ConsentRecords`.

**Saklama süresi: ŞİMDİLİK sınırsız** (Mert, 2026-08-24 — *"şimdilik hep saklayalım,
bunu düzelteceğiz zaten"*) → [[domain-gereksinimler]].

⚠️ **Bu kararın ucuz olma gerekçesi bölümlendirmeye dayanıyordu ve bölümlendirme
henüz yok** (`A-11`). Süre kararı bölümlendirmeden önce gelirse temizlik pahalı olur.

### Postgres'e özgü

**Aylık bölümlendirme — ⚠️ HENÜZ YAPILMADI, görev `A-11`.**
`EventLog` sistemin açık ara en büyük tablosu olacak. `PARTITION BY RANGE
(OccurredAt)` ile aylık parçalara ayrılırsa eski ayı silmek tek komut olur.

Bugün yapılamadı: EF Core bölümlenmiş tabloyu modellemiyor ve birincil anahtarın
bölümleme anahtarını içermesi gerekiyor — model ile veritabanı ayrışırdı.

⚠️ **Bir kararın dayanağı bu.** BRIN indeksi sorgu hızını çözüyor, **silme
maliyetini çözmüyor**. İlk ciddi veri girmeden önce yapılmalı; sonradan yapmak
veri kopyalama demek.

**Buna dayananlar:** [[domain-gereksinimler]] — olay günlüğü saklama süresinin
ertelenmesi. Bölümlendirme yapılmazsa o erteleme ucuz olmaktan çıkar.

**BRIN indeksi** — zaman sıralı devasa tablolarda B-tree yerine BRIN; binlerce kat az
yer kaplar, tarih aralığı sorgusunda aynı işi görür. MSSQL'de karşılığı yok.

**GIN indeksi `Payload` üzerinde** — jsonb içindeki alana göre sorgulama.

### Bu bölümde hangi olaylar kaydediliyor

Yorum yazma / onay / ret · tekne sahibinin cevabı · blog yayını · destek talebi
açılış, ilk cevap, çözüm · bildirim gönderimi ve başarısızlığı · **ve olay günlüğü
diğer yedi bölümün olaylarını taşır.**

İlgili: [[api-desenler]] · [[api-kararlar]] · [[api-mimari]] · [[api-gorevler]] · [[domain-gereksinimler]] · [[durum]]
