---
rol: history
kapsam: api
guncelleme: 2026-09-10
durum: guncel
---

# API Kararları

**Append-only.** Karar değişirse eskisi silinmez; yeni giriş eskisini iptal eder.

---

## 2026-08-21 — .NET 10 + Controller tabanlı Web API

**Karar:** Hedef çerçeve `net10.0`, controller tabanlı (`--use-controllers`).

**Neden:** .NET 10 SDK zaten kurulu (10.0.400) ve LTS. Controller'lar büyüyen projede
routing ve katman ayrımını Minimal API'ye göre daha net tutuyor.

**Alternatifler:** Minimal API — daha az boilerplate ama büyüdükçe organizasyon
disiplini gerektiriyor, elendi. .NET 8 (8.0.424 de kurulu) — daha olgun ekosistem
ama 10 zaten LTS, elendi.

---

## 2026-08-21 — Clean Architecture, dört katman

**Karar:** `Domain` / `Application` / `Infrastructure` / `Api` projeleri, `src/` altında.
Bağımlılık yönü içe doğru; Domain hiçbir şeye bağlı değil.

**Neden:** Mert katmanlı yapı istedi.

**Alternatifler:** Tek Api projesi (YAGNI gerekçesiyle önerilmişti) — reddedildi.
Api + test projesi — seçilmedi, test altyapısı hâlâ yok → [[durum]].

**Risk:** Domain tanımlı olmadığı için üç katman şu an boş. Katmanlar dolmadan bu
yapının faydası görünmez; yanlış domain modeliyle doldurulursa maliyeti yüksek olur.

---

## 2026-08-21 — CORS yapılandırmadan okunuyor

**Karar:** İzinli origin'ler `Cors:AllowedOrigins` yapılandırma bölümünden okunur,
koda gömülmez. `FrontendCorsPolicy` adlı tek politika.

**Neden:** Frontend ayrı origin'de (`localhost:3000`) çalışıyor; ortam değiştikçe
(staging, production) kod değişmemeli.

**Not:** Bu kararı Claude önerdi, Mert talep etmedi — istenmezse kaldırılabilir.

İlgili: [[api-mimari]] · [[durum]] · [[00-Index]]

---

## 2026-08-22 — Backend sıfırdan tasarlanıyor, PRD'ye bağlı değil

**Karar:** Tersine mühendislikle çıkarılmış şartname (PRD) backend tasarımının
dayanağı **değildir**. Domain modeli ve veritabanı şeması sıfırdan, Mert'le
konuşularak tasarlanacak.

**Neden:** Mert'in talebi. Ayrıca belge diskte bulunamadı — `~/Desktop`,
`~/Documents`, `~/Downloads` ve proje klasörü tarandı, sonuç yok. Ulaşılamayan
bir belgeye atıf yapan kararlar doğrulanamaz.

**Alternatifler:** Canlı `dailycruising.com.tr` sitesinden davranış çıkarmak —
admin ve panel tarafı görünmediği için eksik kalırdı, elendi. PRD'yi beklemek —
işi bloke ederdi, elendi.

**Sonuç:** [[proje]] içindeki iş tanımı (tur tipleri, roller, komisyon modeli)
geçerli kalır; ama "mevcut sistemin davranışı şuydu" türü her atıf artık
**doğrulanmamış** sayılır. `durum.md`'deki "PRD 14. kural" atfı dayanaksızdır —
sunucu taraflı fiyat doğrulaması yine de yapılacak, gerekçesi PRD değil
güvenliktir.

İlgili: [[api-mimari]] · [[proje]] · [[durum]]

---

## 2026-08-22 — Veritabanı: PostgreSQL

**Karar:** PostgreSQL. EF Core sağlayıcısı Npgsql.

**Neden — asıl sebep:** Sistemin bel kemiği kuralı *"aynı teknede iki sefer zaman
olarak çakışamaz"*. PostgreSQL bunu `EXCLUDE` + GIST kısıtıyla **veritabanı
seviyesinde garanti eder**; ihlal edilmesi imkânsız hale gelir. MSSQL'de aynı
güvence ancak uygulama kilidi veya serializable transaction ile sağlanır — yani
her yazma yolunda doğru kilidi almayı hatırlamaya bağlı kalır. Aynı kısıt fiyat
tarih aralıklarının çakışmasını da engeller.

**Yan sebepler:** `numeric` (para), `daterange`/`tstzrange`, JSONB, lisans maliyeti
yok, Npgsql + EF Core olgun.

**Performans GEREKÇE DEĞİL.** Mert "Postgres daha performanslı" diye duymuştu;
bu ölçekte (bugün 35 tekne, hedef birkaç bin) iki veritabanı arasındaki fark
alâkasız. Karar doğruluk garantisi ve maliyet üzerinden verildi.

**Alternatif:** MSSQL — Mert'in bildiği sistem, ciddi bir argümandı. Elendi çünkü
çakışma kısıtı yok ve lisans maliyeti büyümeyle geliyor.

**Kapsam dışı bırakılanlar:** Redis, Elasticsearch, mesaj kuyruğu, mikroservis.
Bu ölçekte tek bir PostgreSQL + tek API sunucusu yeterli. Redis bir veritabanı
alternatifi değil, önbellektir; sırası arama sorgusu ölçülebilir şekilde
yavaşladığında gelir.

**Bilinen tuzak:** Npgsql `DateTime` değerlerinin UTC `Kind` taşımasını ister;
belirsiz `Kind` hata fırlatır. "UTC sakla" kararı bunu zaten karşılıyor.

**⚠️ Taahhüt:** Mert PostgreSQL'i hiç kullanmadı. Kurulum, bağlantı, migration ve
Postgres'e özgü her konuda **açıklama yapılacak** — sessizce geçilmeyecek.

İlgili: [[api-mimari]] · [[domain-gereksinimler]] · [[durum]]

---

## 2026-08-23 — Veritabanı isimlendirmesi: İngilizce ve standartlara uygun

**Karar (Mert):** Tüm veritabanı tabloları ve kolonları **İngilizce** adlandırılır
ve yaygın standartlara uyar. Türkçe tablo/kolon adı kullanılmaz.

**Claude'un önerdiği somut kural** — onay bekliyor:

| Katman | Biçim | Örnek |
|---|---|---|
| C# entity adı | PascalCase, **tekil** | `Boat`, `ReservationItem` |
| C# property adı | PascalCase | `DepartureTime` |
| PostgreSQL tablo adı | snake_case, **çoğul** | `boats`, `reservation_items` |
| PostgreSQL kolon adı | snake_case | `departure_time` |

**Neden snake_case:** PostgreSQL tırnaksız tanımlayıcıları küçük harfe çevirir.
PascalCase tablo adı kullanılırsa her sorguda çift tırnak gerekir (`"Boats"`) —
elle SQL yazarken sürekli hata kaynağı olur. snake_case Postgres dünyasının fiili
standardıdır.

**Nasıl:** `EFCore.NamingConventions` paketi C# tarafındaki PascalCase adları
otomatik snake_case'e çevirir; entity sınıflarına öznitelik yazmaya gerek kalmaz.

⚠️ **Mert'e açıklanacak** — PostgreSQL'e özgü bir davranış, MSSQL'de bu sorun yok.
2026-08-22 Postgres kararındaki öğretme taahhüdü kapsamında.

İlgili: [[domain-gereksinimler]] · [[api-mimari]]

---

## 2026-08-23 — İsimlendirme: PascalCase (aynı gün verilen snake_case önerisini iptal eder)

**Karar (Mert):** Veritabanı tablo ve kolon adları **PascalCase** olacak.
`Boats`, `Reservations`, `DepartureTime`. Adlar İngilizce kalır.

**Neden:** Mert'in tercihi — C# tarafındaki yazımla veritabanı yazımının aynı
kalması. Claude snake_case önerdi ve Postgres'in tırnak davranışını açıkladı;
Mert dinleyip PascalCase'i seçti. Karar Mert'indir.

**Alternatifler:** snake_case — aynı gün Claude önerdi, elle yazılan SQL'de tırnak
gerektirmemesi avantajıydı; elendi.

**Sonuçları — bilinerek kabul edildi:**
- PostgreSQL tırnaksız tanımlayıcıları küçük harfe indirger. PascalCase adlar bu
  yüzden **her elle yazılan SQL'de çift tırnak ister**: `SELECT * FROM "Boats"`.
  psql, pgAdmin, DBeaver ve elle yazılan migration betikleri bundan etkilenir.
- **EF Core tarafında hiçbir sorun yok** — EF her tanımlayıcıyı zaten tırnaklar.
  Bu aynı zamanda Npgsql'in **varsayılan** davranışıdır, yani
  `EFCore.NamingConventions` paketine **gerek kalmaz**, ek yapılandırma yoktur.

**Pratikte:** günlük işin tamamı EF Core üzerinden yürüyeceği için etki sınırlı;
bedel yalnız veritabanına elle bağlanıp SQL yazıldığında ödenir.

İlgili: [[domain-gereksinimler]] · [[api-mimari]]

---

## 2026-08-24 — Şema bölüm 1: kimlik ve yetki (Mert onayladı)

**Karar:** Tek `Users` tablosu; yetki iki ayrı boyutta modellenir — *ne yapabilir*
(`Roles`/`Permissions`) ve *kimin verisinde* (`PartnerMembers`). İkincisi elle
atanmaz, üyelikten türer. Tam şema → [[api-sema]].

**Neden:** Mert *"daha sonrasında farklı farklı roller ve farklı farklı yetkiler
verebilirim"* dedi; rol kodda `enum` olamaz. İşletme sahibi kendi çalışanını
tanımladığı için yetki yönetimi devredilmiş olmalı, ama devredilen yetki platformun
kendi yetkilerine uzanmamalı.

**Mert'in üç cevabı (2026-08-24):**
1. **Üyelik başına tek rol.** İşletme sahibi zaten kendi rolünü tanımlayabildiği
   için "hem rezervasyoncu hem muhasebeci" ayrı bir rol olarak açılır. Rol birleşimi
   hesaplama karmaşası ve yetki sızıntısı riski getirirdi.
2. **Bir kullanıcı yalnız BİR işletmede çalışabilir.** `PartnerMembers.UserId`
   benzersiz. Kooperatif senaryosunda çok üyelik gerekirse bu kısıt kaldırılacak —
   ama bugün kapalı, çünkü açık kapsam hatası veri sızdırır.
3. **Platform personelinde kapsam filtresi devre dışı, karşılığında her erişim
   olay günlüğüne yazılır.** Yoksa admin hiçbir şey göremezdi.

**Güvenlik kilidi:** `Permissions.IsPartnerAssignable`. `false` olan yetki, işletme
sahibinin çalışanına yetki verdiği ekranda listelenmez. Bu kolon olmadan tekne
sahibi kendi çalışanına komisyon değiştirme yetkisi verebilirdi.

**Komisyon oranı `Partners` üzerinde DEĞİL, `Contracts` üzerinde.** İşletmenin
geçerli oranı = aktif sözleşmesindeki oran. Oran değişikliği yeni sözleşme ve yeni
onay ister. Gerekçe: [[domain-gereksinimler]] "komisyon oranı sözleşmede yazar".

**Alternatifler:** Rol için `enum` — Mert'in talebiyle elendi. Ayrı `Customers` /
`PartnerUsers` tabloları — müşteriyken tekne sahibi olan kişide e-posta çakışması
yaratırdı, elendi. Kapsamı `UserRoles` üzerinde taşımak — elle atanabilir olurdu,
yani unutulabilir; `PartnerMembers`'tan türetmek yapısal olarak güvenli.

**Postgres'e özgü — Mert'e açıklandı:** `citext` (Postgres metinde büyük/küçük harf
duyarlıdır, MSSQL değildir — eklentisiz aynı e-postayla iki hesap açılır) ·
`timestamptz` + Npgsql'in UTC zorunluluğu · kısmi benzersiz indeks (MSSQL'de
"filtered index") · uuid v7 (`Guid.CreateVersion7()`) · durum kolonları `text` +
CHECK, Postgres `ENUM` tipi değil (değer eklemek migration'da acı veriyor).

İlgili: [[api-sema]] · [[api-desenler]] · [[domain-gereksinimler]]

---

## 2026-08-24 — Şema bölüm 2: katalog (Mert onayladı)

**Karar:** 13 tablo. Tekneye ait bilgi `Boats` ve bağlantı tablolarında; kiralama
tipine ait bilgi 3. bölümde. Tam şema → [[api-sema]].

**Neden ayrı çeviri tabloları:** genel `Translations(EntityType, EntityId, ...)`
tablosunda foreign key kurulamaz ve tip güvenliği yoktur. Varlık başına ayrı tablo
daha çok dosya demek ama veritabanı bütünlüğü koruyor.

**Neden `BoatCrewLanguages` ve `BoatRules` ayrı tablo:** serbest metin olsalardı
filtrelenemezlerdi. "İngilizce bilen mürettebat" ve "evcil hayvan kabul eden tekne"
aramaları ancak yapılandırılmış veriyle çalışır.

**Mert'in iki cevabı (2026-08-24):**
1. **Belge süresi dolunca tekne yayında kalır, uyarı gider** (b seçeneği). Otomatik
   pasife düşürmek sezon ortasında tekne sahibinin haberi olmadan satışını
   durdurur — uyarı, sessiz kesintiden iyidir.
2. **Şimdilik tek slug**, dile göre slug ilerideki sürümde. Mert: *"sonrasında SEO
   için kesinlikle dile göre ayrım yapacağız."* Sonradan `BoatTranslations.Slug`
   eklenip eskisi 301 yönlendirmeye dönüşür; mevcut veri bozulmaz
   → [[domain-gereksinimler]] 🔮 GELECEK SÜRÜM.

**İki kapasite kolonu ayrı tutuldu** (`CommercialCapacity` / `LegalCapacity`): tek
kolon olsaydı ticari sınır yükseltilirken yasal sınır da sessizce yükselirdi → D2.

**Postgres'e özgü — Mert'e açıklandı:** `unaccent` + `pg_trgm` (Postgres'te `Çeşme`
ile `Cesme` farklı metindir, MSSQL collation'ı bunu kendiliğinden çözüyordu) ·
kısmi benzersiz indeks ile "tekne başına tek kapak fotoğrafı" · koordinat için
`double precision`, PostGIS erken eklenmiyor.

İlgili: [[api-sema]] · [[domain-gereksinimler]]

---

## 2026-08-24 — Şema bölüm 3: kiralama tipleri ve fiyat (Mert onayladı)

**Karar:** `RentalTypes` (8 tip, platform tanımlı) → `BoatRentalTypes` (teknenin o
tipi satma biçimi) → `Prices` (temel + sezon istisnası) → `Extras` (menü ve ek
hizmet). Tam şema → [[api-sema]].

**"+1 gün" kuralı kolon oldu, kod olmadı.** `RentalTypes.ExtraDayCount`.
**Neden:** fiyat ve takvim aynı sayıyı okumalı. Kodda `if (tip == konaklamalı)`
yazılsaydı, ikinci bir çok günlü tip eklendiğinde o `if` aranacaktı.

**Temel fiyat ayrı tablo değil, `ValidRange IS NULL` satırı.**
**Neden:** fiyat sorgusu sistemin en sık çalışan sorgusu; tek yerden okumalı.
Çakışan sezon aralığı `EXCLUDE USING gist` ile veritabanı seviyesinde imkânsız.

**Menü ayrı tablo DEĞİL, `Extras.ExtraType = Menü`.**
**Neden:** Mert "menü dışında ekstra satılan bir şey olabilir" dedi. Transfer,
ekipman, fotoğraf paketi şema değiştirmeden eklenebilmeli.

**Mert'in iki cevabı (2026-08-24):**
1. **Aynı teknede aynı kiralama tipinden birden çok satır olabilir** — sabah ve
   öğleden sonra turu gibi. `(BoatId, RentalTypeId)` benzersiz değil; ayırt edici
   `Name` çeviri tablosunda. Mert bunu genel ilkeye bağladı: *"bazı böyle durumları
   biz tekne sahibine bırakalım, o panelden kendisi yapsın"*
   → [[domain-gereksinimler]] TASARIM İLKESİ 2026-08-24.
2. **Menü ve ek hizmette sezonluk fiyat YOK.** Yemek maliyeti tur fiyatı kadar
   oynamıyor; tekne sahibine gereksiz iş çıkarırdı.

**Postgres'e özgü — Mert'e açıklandı:** `daterange` + `EXCLUDE USING gist` (MSSQL'de
karşılığı yok) · **`btree_gist` eklentisi şart**, yoksa kısıt reddedilir ve hata
mesajı sebebi söylemez · para daima `numeric`, `float` kuruş kaçırır.

İlgili: [[api-sema]] · [[domain-gereksinimler]]

---

## 2026-08-24 — Şema bölüm 4: takvim ve sefer (Mert onayladı)

**Karar:** `Voyages` tek tablo; her satış ve her blok teknenin takviminde bir
`tstzrange` işgal eder. Tam şema → [[api-sema]].

**Tek kısıt her şeyi taşıyor:**
`EXCLUDE USING gist (BoatId WITH =, TimeRange WITH &&) WHERE (Status <> 'İptal')`

**Neden blok ayrı tablo DEĞİL:** ayrı olsaydı "sefer bakımla çakışmasın" diye ikinci
bir kontrol gerekirdi; o kontrolü atlayan kod yolu er geç yazılır. Aynı tabloda tek
kısıt ikisini birden kapsıyor.

**Neden yarı açık aralık `[)`:** sabah `[09:00,13:00)` ve öğleden sonra
`[13:00,17:00)` turları çakışmasın diye. Kapalı aralıkta 13:00 ikisine de ait olur
ve 3. bölümde açılan "günde iki tur" özelliği çalışmazdı.

**Mert'in iki cevabı (2026-08-24):**
1. **`Boats.DefaultCalendarMode`** — tekne eklenirken varsayılan takvim modu
   sorulur. "Mod tanımlanmamış tarih" boşluğu hiç oluşmaz; karar tekne sahibinde
   kalır.
2. **`AvailabilityDays` özet tablosu ERTELENDİ.** Claude kendi eski çıkarımına
   itiraz etti, Mert kabul etti. Geri dönüş eşiği ölçüme bağlandı: arama p95
   > 300 ms veya 300+ tekne → [[domain-gereksinimler]].

**Postgres'e özgü — Mert'e açıklandı:** `tstzrange` + yarı açık aralık `[)` ·
kısmi `EXCLUDE` ile iptal edilen seferin takvimi bırakması · UTC saklama ama
`Europe/Istanbul` gün sınırı, `tstzrange` yaz saatinde kaymaz (MSSQL `datetime2`
ile elle yönetilirdi).

İlgili: [[api-sema]] · [[domain-gereksinimler]] · [[api-durum]]

---

## 2026-08-24 — Şema bölüm 5: rezervasyon (Mert onayladı)

**Karar:** Rezervasyon satın alma anının fotoğrafını çeker — fiyat, yaş sınırı, kur,
komisyon oranı ve kurallar **kopyalanır**, referansla bağlanmaz. Tam şema
→ [[api-sema]].

**Neden dondurma:** tekne sahibi yarın fiyatını, yaş sınırlarını veya sözleşmesini
değiştirebilir. Referans olsaydı geçmiş rezervasyonların tutarı ve hesaplanmış
komisyonu geriye dönük bozulur, hakediş yanlış çıkardı.

**Kapasite koruması üç katmanlı:** `CHECK (SoldSeats <= Capacity)` gerçek garanti ·
`SELECT ... FOR UPDATE` oku-değiştir-yaz doğruluğu için · `HoldExpiresAt` üzerinde
kısmi indeks temizlik işi için. `SERIALIZABLE` bilinçli olarak seçilmedi —
çakışmada yeniden deneme mantığı gerektiriyor, bu iş için gereksiz karmaşık.

**Mert'in iki cevabı (2026-08-24):**
1. **Çevrimdışı biniş (G-12 KAPANDI): c seçeneği** — internet yoksa tekne sahibi
   sonradan panelden işaretler, `BoardingScans.Method = Manuel`. **a seçeneği
   (çevrimdışı kuyruk) gelecek sürümde**, mobil uygulamayla: *"ilerde yaparız, bunu
   da kesinlikle ekle."*
2. **Rezervasyon değişikliği YOK, yalnız iptal.** `ReservationAmendments` gelecek
   sürümde — değişiklik para farkı ve yeni komisyon üretir, 6. bölümdeki para defteri
   oturmadan kurmak erken.

Her ikisi de → [[domain-gereksinimler]] 2026-08-24.

İlgili: [[api-sema]] · [[domain-gereksinimler]] · [[api-durum]]

---

## 2026-08-24 — Şema bölüm 6-7-8: TASARLANDI, onay bekliyor

⚠️ **Bu üç bölüm Mert'in tek tek onayından geçmedi.** Mert *"sen hepsini yap, en son
bana cevaplamam gereken soruları yaz"* dedi. Aşağıdakiler **Claude'un kararlarıdır**;
onay gelmeden bu bölümlerden kod yazılmaz. Tam şema → [[api-sema]].

**Bölüm 6 — Para.** Değişmez, append-only defter (`LedgerEntries`). Bir rezervasyonun
tüm satırlarının toplamı her zaman 0; sapma varsa hesap hatası var demektir.
Düzeltme `UPDATE` değil **ters kayıt**.
**Neden:** para kaydı güncellenirse "bu tutar neden böyle" sorusu üç ay sonra
cevaplanamaz. Aynı mantık olay günlüğüne de uygulandı.

**Fatura numarasında `SEQUENCE` kullanılmayacak** — Postgres dizileri geri alınan
işlemde boşluk bırakır, Türk vergi mevzuatı kesintisiz numara ister. Ayrı sayaç
tablosu + `FOR UPDATE`. Sonradan fark edilirse düzeltmesi çok pahalı.

**Bölüm 7 — Teklif ve mesajlaşma.** Teklif tarihi tutmak için ayrı mekanizma
yazılmadı: `Voyages` tablosuna **`VoyageType = Teklif`** eklendi.
**Neden:** aynı `EXCLUDE` kısıtı üç senaryoyu birden taşıyor (satış, blok, teklif).
Ayrı mekanizma ikinci bir çakışma kontrolü gerektirirdi. Bu, 4. bölümün onaylanmış
haline yapılan **tek ekleme**.

`Messages` hem `Body` (orijinal) hem `MaskedBody` tutuyor. **Neden:** anlaşmazlıkta
platformun elinde kayıt kalmalı, ama API asla orijinali döndürmemeli.
`MaskedItemCount` platform dışına kaçış girişiminin sinyali.

**Bölüm 8 — Yan sistemler ve olay günlüğü.** `EventLog` değişmez ve append-only;
`Payload jsonb` sayesinde yeni olay türü şema değişikliği istemiyor. Arama sorguları
için ayrı tablo açılmadı, `search.performed` olayının içinde duruyor.
**Neden `Seq` kolonu:** n8n gibi dış tüketiciler `WHERE Seq > sonOkunan` ile ilerler.
Dizi boşluk bırakır ama sıra bozulmaz — imleç için yeterli, faturada yetersizdi.

`SupportTickets.FirstResponseAt` ve `ResolvedAt` süs değil: destek personeli sezon
raporunun tek veri kaynağı. Bugün açılmazsa o rapor hiç üretilemez.

**Claude'un onay bekleyen iki kararı:**
- **S6-1** Kuponlu rezervasyonda kısmi iade → **(b)**: hakediş liste üzerinden
  orantılı, indirimi platform karşılamaya devam eder. Bedeli: platformun payı düşer.
- **S6-2** Hakediş periyodu → **iki haftada bir, sözleşmede yazılı**
  (`Contracts.PayoutPeriodDays`).

**Postgres'e özgü — Mert'e açıklandı:** `jsonb` + GIN (sağlayıcı seçilmeden şema
kurulabilmesinin sebebi) · tetikleyiciyle gerçekten değişmez tablo · `EventLog` için
aylık **declarative partitioning** (eski ayı silmek `DROP TABLE` kadar ucuz) ·
zaman sıralı devasa tabloda **BRIN** indeksi, MSSQL'de karşılığı yok.

İlgili: [[api-sema]] · [[domain-gereksinimler]] · [[api-durum]]

---

## 2026-08-24 — Şema bölüm 6-7-8 ONAYLANDI (Mert'in toplu cevabı)

Mert altı sorunun tamamını cevapladı; şema sekiz bölümde tamamlandı.

**Onaylananlar:**
- **A1 → (b)** Kuponlu rezervasyonda kısmi iade: hakediş liste fiyatı üzerinden
  orantılı, indirimi platform karşılamaya devam eder. 1000/%15/%10'da yarı iade →
  tekne sahibi 425, platform 25.
- **A2 → iki haftada bir**, sözleşmede yazılı (`Contracts.PayoutPeriodDays`).
- **B3 → mesajlaşma için giriş ZORUNLU.** Rezervasyon misafir olarak yapılabilir ama
  mesaj atmak için hesap gerekir. **Neden:** cevabın kime gideceği belli olmalı ve
  giriş olmadan spam yönetilemez.
- **C5 → tekne sahibinin blog yazısı platform onayından geçer.** `BlogPosts` üzerine
  `ApprovedByUserId` + `ApprovedAt`. Platform yönetiminin kendi yazısı onay beklemez.

**Değişiklik gerektiren tek cevap — C4: yorumda ALT PUANLAR da olacak.**

`Reviews.Rating` (genel, zorunlu) korundu; üstüne `ReviewCriteria` +
`ReviewCriterionTranslations` + `ReviewScores` eklendi. Kriterler: temizlik,
mürettebat, yemek, fiyat/değer, güvenlik, tekne durumu.

**Neden kolon değil ayrı tablo:** yeni kriter eklemek şema değişikliği
gerektirmemeli ve **eski yorumları bozmamalı**. Kolon olsaydı her yeni kriterde
geçmiş yorumların tamamı `NULL` ile dolar, ortalama yanlış çıkardı.

**Alt puanlar opsiyonel, genel puan zorunlu.** Menü almamış müşteri "yemek" puanı
veremez; zorunlu olsaydı ya rastgele puan verirdi ya yorumu hiç yazmazdı.

**Kriterleri platform tanımlar, tekne sahibi değil** — teknelerin karşılaştırılabilir
kalması için. "Kararı tekne sahibi verir" ilkesinin sınırı: ayarlanabilir olan
işletme tarzıdır, platformun ölçüsü değil → [[domain-gereksinimler]].

**C6 → olay günlüğü saklama süresi ERTELENDİ.** Mert: *"şimdilik hep saklayalım,
bunu düzelteceğiz zaten, süre vermeyelim ŞİMDİLİK."* Aylık bölümlendirme sayesinde
karar sonradan verildiğinde uygulaması tek `DROP` komutu — satır satır `DELETE`
gerekmeyecek. Karar ertelendi ama **uygulaması ucuz kalacak şekilde kuruldu**.

İlgili: [[api-sema]] · [[domain-gereksinimler]] · [[api-durum]]

---

## 2026-08-24 — PostgreSQL 18 Homebrew ile kuruldu, migration bölüm bölüm

**Karar:** PostgreSQL 18.6, `brew install postgresql@18`. Mert üç seçenek arasından
Homebrew'ü seçti (Docker ve Postgres.app elendi).

**Neden Homebrew:** `psql` doğrudan PATH'te (`/opt/homebrew/bin/psql`), sunucuda
görülecek deneyimin aynısı, eklenti kurmak kolay. Docker'da `psql` konteynerin içinde
kalıyor ve öğrenme aşamasında kafa karıştırıyor; Postgres.app'i Mert'in elle indirmesi
gerekiyordu.

**Kurulan yapı:**
- Veritabanı `dailycruising_dev`, sahibi `dailycruising` rolü (superuser DEĞİL)
- Eklentiler: `citext`, `btree_gist`, `unaccent`, `pg_trgm`
- Servis: `brew services start postgresql@18` (girişte otomatik başlar)

**Bağlantı dizesi `appsettings.json`'a YAZILMADI.** Parola .NET user-secrets'ta
(`~/.microsoft/usersecrets/`), yani repo dışında. **Neden:** parola commit'lenirse
git geçmişinden silinmesi pratikte imkânsız.

**Eklentiler `HasPostgresExtension` ile modele bağlandı** — migration'ın parçası
oldular. Yeni bir makinede `dotnet ef database update` tek başına yeterli, elle
`CREATE EXTENSION` gerekmiyor.

**Enum'lar metin olarak saklanıyor**, Postgres `ENUM` tipi olarak değil. `OnModelCreating`
içinde tek döngüyle tüm enum property'leri `string`'e çevriliyor.
**Neden:** Postgres ENUM'una değer eklemek migration'da acı veriyor; metin + `CHECK`
aynı güvenceyi esneklikle veriyor.

**Migration stratejisi: bölüm bölüm, hepsi tek seferde değil.**
İlk migration `Bolum1_KimlikVeYetki` — 13 tablo. Kalan yedi bölüm ayrı migration'lar
olacak (`A-09`).
**Neden:** 55 tabloyu tek seferde yazmak, ilk hatanın nerede olduğunu gizler. Bölüm
bölüm gidince her adım ayrı doğrulanıyor ve geri alınabiliyor.

**Kanıtlanan kısıtlar** (geri alınan bir işlem içinde denendi):
- `citext`: `Mert@Ornek.com` varken `mert@ornek.com` **reddedildi**
- `CK_Contracts_CommissionRate`: %150 komisyon **reddedildi**
- Kısmi benzersiz indeksler kuruldu: işletme başına tek onaylı sözleşme, tek sahip

İlgili: [[api-sema]] · [[api-desenler]] · [[api-durum]]

---

## 2026-08-24 — Üç ajan denetimi: 1. bölümde 17 kusur bulundu ve düzeltildi

Mert *"aç bunu ve api araçlarını kullan"* dedi; [[api-araclar]]'ın üç tetikleyicisi de
oluşmuştu. `database-reviewer`, `csharp-reviewer` ve `security-reviewer` paralel
çalıştı. Üçü de kusur buldu; `csharp-reviewer` birleştirmeyi **engelledi**.

### ⚠️ Bu bir vault ↔ kod çelişkisiydi

Bulguların çoğu **[[api-sema]]'da doğru yazılmış ama koda geçmemiş** kurallardı.
Şemada "işletme rolü yalnız IsPartnerAssignable=true yetkiler alabilir" yazıyordu;
veritabanında böyle bir kısıt yoktu. Yani belge ile gerçek ayrışmıştı ve
**`dogrula.py` bunu yakalayamaz** — semantik çelişki, kırık link değil.

### Güvenlik: üç eksik birleşince gerçek yetki yükseltme zinciri

1. `PartnerMembers.RoleId` herhangi bir role bağlanabiliyordu — FK "bu rol var mı"
   der, "bu rol bu işletmenin mi" demez. `platform.admin`'in id'si yazılırsa çalışan
   platform yetkilerini devralıyordu
2. `Roles.PartnerId` null'a çekilebiliyordu → sahte "platform rolü" üretilebiliyordu
3. `UserRoles`'a işletme rolü eklenebiliyordu — kural yalnız yorum satırındaydı

Üçü birlikte: **bir çalışan başka bir işletmenin verisini görebiliyordu.**

**Çözüm: üç plpgsql tetikleyici** (`Bolum1_GuvenlikTetikleyicileri` migration'ı).
FK ve CHECK bu kuralları ifade edemiyor — FK doğru satırı değil var olan satırı
kontrol eder, CHECK başka tabloya bakamaz.

**Neden kodda değil veritabanında:** şemanın kendi ilkesi. 3. bölümde fiyat
çakışması için *"uygulama kodundaki kontrol, o kontrolü atlayan bir yazma yolu
yazıldığında sessizce bozulur"* denip `EXCLUDE` kısıtı konmuştu. En kritik güvenlik
kuralında aynı ilkeyi terk etmek tutarsızlıktı.

**Kanıt:** dört saldırı senaryosu canlı denendi, dördü de reddedildi; meşru işlem
geçti (bkz. `A-02` görev kanıtı).

### Diğer düzeltmeler

| Bulgu | Düzeltme |
|---|---|
| `(PartnerId, Key)` benzersizliği platform rollerinde çalışmıyordu — Postgres'te NULL, NULL'a eşit değil, iki `platform.admin` açılabiliyordu | İki ayrı **kısmi** benzersiz indeks: `PartnerId IS NULL` ve `IS NOT NULL` |
| `EmailVerifiedAt` mutable `Email`'e bağlıydı → hesap devralma | **`User.PendingEmail`** eklendi + `UserTokenPurpose.EmailChange` |
| `TokenHash` adı bcrypt tuzağı kuruyordu (bcrypt her çağrıda farklı çıktı verir, `WHERE` hiç eşleşmez) | **`TokenSha256`** olarak yeniden adlandırıldı, gerekçe koda yazıldı |
| `uuid v7` kararı şemada vardı, kodda yoktu | `HasDefaultValueSql("uuidv7()")` — PostgreSQL 18 yerleşik fonksiyonu |
| Enum→string dönüşümü `OnModelCreating`'de refleksiyonla, yapılandırmalardan SONRA çalışıyordu; ileride yazılacak `.HasConversion<int>()`'ı sessizce eziyordu | `ConfigureConventions` + `Properties<Enum>().HaveConversion<string>()` — yapılandırmalardan ÖNCE çalışır, ezilebilir |
| `UseNpgsql(null)` hata vermiyor; uygulama açılıp ilk istekte anlamsız hatayla düşüyordu | Başlangıçta hemen patlıyor, mesaj user-secrets komutunu veriyor |
| `Roles.PartnerId` yabancı anahtarsızdı | FK → `Partners`, `Restrict` |
| Kanıt kolonları (`ApprovedByUserId`, `SentByUserId`, `GrantedByUserId`, `InvitedByUserId`, `CreatedByUserId`) çıplak uuid'di — "anlaşmazlıkta tek kanıt" dediğimiz alanın ucu kopabiliyordu | Hepsine FK → `Users`, `Restrict` |
| `ConsentRecords` → `User` **Cascade**'di; kullanıcı silinince KVKK onay ispatı da siliniyordu | **`Restrict`** — silme isteği geldiğinde karar vermek zorunda kalınır |
| `PartnerId` üzerinde yalnız kısmi indeks vardı; "işletmenin tüm sözleşmeleri" sorgusu filtreyi içermediği için tablo taramasına düşüyordu | Ayrıca düz indeks |
| Partner çocuklarında `OnDelete` tutarsızdı (sözleşme `Restrict`, evrak `Cascade`) | Hepsi `Restrict` — "red kaydı silinmez" kuralıyla uyumlu |
| `Status='Approved'` iken `ApprovedAt`/`ApprovedByUserId` boş kalabiliyordu | `CK_Contracts_ApprovedEvidence` |
| Reddedilen başvuruda sebep boş kalabiliyordu | `CK_Partners_RejectionReason` |
| Kısmi indeks filtresi `'Approved'` düz metindi; enum adı değişse sessizce bozulurdu | `nameof(ContractStatus.Approved)` |
| Entity ve yapılandırma sınıfları `sealed` değildi | Hepsi `sealed` |

### İleriye taşınan iki uyarı (henüz açık)

- **`AllowedHosts: "*"`** duruyor. Parola sıfırlama linkleri `Request.Host`'tan
  kurulursa Host header injection ile sahte link üretilebilir. Linkler sabit
  yapılandırılmış base URL'den kurulacak → `A-03`
- **Uygulama rolü tabloların sahibi.** 6. bölümdeki "para defteri tetikleyiciyle
  değişmez" iddiası ancak uygulama rolü tablo sahibi DEĞİLSE geçerli — sahip
  `ALTER TABLE ... DISABLE TRIGGER` diyebilir. Ayrı, en az ayrıcalıklı bir rol
  gerekiyor → `A-10`

İlgili: [[api-sema]] · [[api-desenler]] · [[api-durum]] · [[api-araclar]]

---

## 2026-08-24 — 2-8. bölüm entity'leri ve migration'ları

**Karar:** Sekiz bölümün tamamı koda döküldü. **75 tablo**, 3 EXCLUDE kısıtı,
5 tetikleyici. Migration'lar bölüm bölüm alındı, hepsi tek seferde değil.

**Domain katmanı bağımsız kaldı — bunun bir bedeli var.**
`daterange` ve `tstzrange` Npgsql tipleridir (`NpgsqlTypes`); Domain'de kullanmak
oraya paket bağımlılığı sokardı ve Clean Architecture kuralını delerdi. Bu yüzden
aralıklar **iki ayrı kolon** olarak duruyor (`StartsAt`/`EndsAt`,
`ValidFrom`/`ValidTo`) ve kısıtlar migration'da **ifade tabanlı** kuruluyor:

```sql
EXCLUDE USING gist ("BoatId" WITH =, tstzrange("StartsAt","EndsAt",'[)') WITH &&)
  WHERE ("Status" <> 'Cancelled')
```

Garanti birebir aynı; [[api-sema]]'daki "ValidRange daterange" ifadesi bu yüzden
kolon adı değil **kavram** olarak okunmalı.

**Üç EXCLUDE kısıtı:**

| Kısıt | Engellediği |
|---|---|
| `EX_Voyages_NoOverlapPerBoat` | Aynı teknede zaman olarak çakışan iki sefer |
| `EX_Prices_NoOverlappingSeasons` | Çakışan sezon fiyat aralığı |
| `EX_CalendarModeRules_NoOverlapPerLayer` | Aynı öncelik katmanında çakışan takvim modu |

Fiyat kısıtı `WHERE ValidFrom IS NOT NULL` ile sınırlı: temel fiyat satırı
sınırsız aralık sayılıp her sezonla çakışırdı.

**İki değişmez tablo:** `LedgerEntries` ve `EventLogs` üzerinde `forbid_mutation()`
tetikleyicisi. UPDATE ve DELETE reddediliyor; düzeltme ters kayıt.

**`EventLogs` aylık bölümlendirme ŞİMDİLİK YAPILMADI.** Tek tablo + BRIN indeksi.
**Neden:** bölümlendirme ilk satır yazılmadan önce kurulmalı ama bugün hiç veri
yok ve hacim bilinmiyor. BRIN indeksi bu ölçekte aynı işi görüyor. Saklama süresi
kararı verildiğinde (Mert erteledi) bölümlendirme onunla birlikte gelecek — ikisi
aynı işin parçası.

**Doğrulama — sekiz senaryo canlı denendi, sekizi de doğru davrandı:**
- Mehmet 15 Eylül günlük tur aldı; Cemil'in aynı gün konaklamalı seferi **reddedildi**
- Aynı teknenin aynı günkü 17:00-21:00 turu **kabul edildi** (yarı açık aralık çalışıyor)
- 12 kişilik tekneye 13 koltuk **reddedildi**
- Çakışan sezon fiyatı **reddedildi**
- İkinci temel fiyat **reddedildi**
- Defterde UPDATE **reddedildi**, DELETE **reddedildi**
- Ticari kapasite yasal kapasiteyi aşamadı
- Test işlemi geri alındı, veritabanı temiz kaldı

**Migration zinciri (ecc:database-migrations skill'i uyarınca):**
1. Üretilen SQL okundu — **veri kaybı riski 0** (kolon silme, tip daraltma, tablo
   düşürme yok; hepsi yeni tablo), 56 `uuidv7()` varsayılanı, 44 CHECK, 12 kısmi
   indeks, BRIN + GIN yerinde, tüm tanımlayıcılar çift tırnaklı
2. **Geri alma denendi:** 75 tablo, 14'e indi, tekrar 75'e çıktı; kısıtlar geri geldi
3. `ecc:postgres-patterns` indekssiz yabancı anahtar sorgusu **0 satır** döndü

**Skill'in iki tavsiyesi bilinçli reddedildi:** `bigint` yerine `uuid` (v7, rastgele
değil; pazar yerinde id tahmin edilememeli) · `text` yerine `varchar(n)`
(Postgres'te performans farkı yok, uzunluk doğrulama görevi görüyor).

İlgili: [[api-sema]] · [[api-desenler]] · [[api-durum]]

---

## 2026-08-24 — 2-8. bölüm üç ajan denetimi: 20 bulgu, 13'ü düzeltildi

**Karar:** Üç denetçinin bulduğu 20 boşluktan 13'ü aynı oturumda kapatıldı; kalan
7'si görev olarak açıldı. Kapatılanların tamamı **veritabanı kısıtı veya
tetikleyici** olarak yazıldı, uygulama koduna bırakılmadı.

**Neden:** Denetçinin yakaladığı tutarsızlık şuydu — 3. bölümde fiyat çakışması
için *"uygulama kodundaki kontrol, o kontrolü atlayan bir yazma yolu yazıldığında
sessizce bozulur"* deyip EXCLUDE kısıtı konmuştu; ama komisyon oranı, kupon sınırı
ve koltuk sayacı gibi **para doğuran** kurallarda aynı ilke terk edilmişti. Bu üçü
bozulduğunda zarar sessizce oluşur ve ancak defter toplamı sıfırdan sapınca fark
edilir. Kural veritabanında ifade edilebiliyorsa orada durmalı.

`database-reviewer`, `csharp-reviewer` ve `security-reviewer` paralel çalıştı.
C# denetimi "onay (küçük düzeltmelerle)" verdi, diğer ikisi ciddi boşluklar buldu.

### EN ÖNEMLİSİ: kendi yazdığım gerekçe yanlıştı

Bu dosyaya *"EventLogs aylık bölümlendirme yapılmadı, BRIN indeksi aynı işi
görüyor"* yazmıştım. `database-reviewer` haklı olarak şunu gösterdi: [[api-sema]]
8. bölümde saklama süresi kararının ertelenebilme gerekçesi **"bölümlendirme
sayesinde eski ayı silmek DROP TABLE kadar ucuz olacak"** idi. Bölümlendirme
yoksa o öncül geçersiz; silme kararı geldiğinde milyonlarca satırlık DELETE ve
VACUUM gerekecek, yani tam da kaçınmak için kurduğum senaryo.

**BRIN sorgu hızını çözüyor, SİLME maliyetini çözmüyor.** İkisini karıştırmışım.

Bugün bölümlendirme yapılmadı çünkü EF Core bölümlenmiş tabloyu modellemiyor ve
birincil anahtarın bölümleme anahtarını içermesi gerekiyor; model ile veritabanı
ayrışırdı. Görev `A-11` olarak açıldı ve **ilk ciddi veri girmeden önce**
yapılmalı, sonradan yapmak veri kopyalama demek.

### Düzeltilen 13 bulgu

| Bulgu | Düzeltme |
|---|---|
| **TRUNCATE değişmezlik tetikleyicisini atlıyor** — canlı doğrulandı, defter tek komutla boşaldı | `BEFORE TRUNCATE ... FOR EACH STATEMENT` tetikleyicisi iki tabloya |
| Rezervasyonun kopyaladığı komisyon oranının **doğru** olduğunu kimse doğrulamıyordu | `trg_reservation_commission` — orana ve sözleşmenin işletmesine bakıyor |
| **`Reservation.ContractId` yabancı anahtarsızdı** | FK, `Contracts`, `Restrict` |
| Aritmetik tutarsızlık girebiliyordu (ListTotal 1000, GrandTotalTry 1) | `CK_Reservations_GrandTotal` + `CK_Reservations_TotalTry` + `CK_Reservations_DiscountBound` |
| **Kupon oranı komisyonu aşabiliyordu** — platform zarar ederdi | `trg_coupon_within_commission` |
| **`Voyages.SoldSeats` gerçek rezervasyonlarla bağlı değildi** — iptalde azaltmayı unutan kod sayacı kalıcı saptırırdı | `trg_reservation_sync_seats`; sayaç artık türetilmiş veri |
| Başarısız hakediş `LedgerEntries.PayoutId`'yi serbest bırakmıyordu; ortağın parası askıda kalırdı | `trg_payout_failed_releases_ledger` |
| **`BoardingToken` düz metin saklanıyordu** — diğer tüm jetonlar hash'li | `BoardingTokenSha256` + `BoardingTokenExpiresAt` |
| `Coupon.PartnerId` ve `Invoice.IssuerPartnerId` yabancı anahtarsızdı | İkisine de FK ve indeks |
| `Payouts`'ta tutar ve tamamlanma kontrolü yoktu | `CK_Payouts_Amount`, `CK_Payouts_Settled` |
| `CouponRedemptions.DiscountAmountTry` negatif olabiliyordu | `CK_CouponRedemptions_Amount` |
| `Boats.AverageRating` indekssizdi ama arama filtresinde var | `IX_Boats_Search` (bölge, durum, puan) |
| **`User`'da anonimleştirme alanı yoktu** — "hesabımı sil" talebinin teknik karşılığı yoktu | `User.AnonymizedAt` ve kısmi indeks |

### Kanıt — sekiz senaryo canlı denendi

Yanlış komisyon oranı **reddedildi** · başka işletmenin sözleşmesi **reddedildi** ·
aritmetik tutarsızlık **reddedildi** · geçerli rezervasyonda `SoldSeats` otomatik
**5** oldu (bebek sayılmadı) · iptalde **0**'a düştü · yüzde 20 kupon yüzde 15
komisyonda **reddedildi**, yüzde 10 **geçti** · TRUNCATE iki tabloda da
**reddedildi**. Test işlemi geri alındı, veritabanı temiz kaldı.

### Neden hepsi veritabanında, kodda değil

Denetçinin yakaladığı asıl tutarsızlık şuydu: 3. bölümde fiyat çakışması için
*"uygulama kodundaki kontrol, o kontrolü atlayan bir yazma yolu yazıldığında
sessizce bozulur"* deyip EXCLUDE kısıtı konmuştu; komisyon, kupon ve sayaç
kurallarında aynı ilke terk edilmişti. Artık üçü de veritabanında.

### Açık bırakılanlar — görev olarak kaydedildi

`A-11` EventLogs bölümlendirme · `A-12` KVKK saklama ve anonimleştirme akışı ·
`A-13` `EventLogs.Payload` içeriğine sınır · `A-10` genişletildi (ayrı rol ve
TRUNCATE yetkisi olmaması) · `A-03`'e eklendi: `Message.Body` asla API'den
dönmeyecek, `Reservation.Code` sorgusu hız sınırlı olacak.

İlgili: [[api-sema]] · [[api-desenler]] · [[api-durum]] · [[api-araclar]]

---

## 2026-08-24 — A-11: EventLogs aylık bölümlendirmeye çevrildi

**Karar:** `EventLogs` artık `PARTITION BY RANGE ("OccurredAt")`. Birincil anahtar
`("Id","OccurredAt")` bileşik, `Seq` benzersizliği `("Seq","OccurredAt")`.
26 parça: 25 ay peşinen açıldı, bir de varsayılan parça var.

**Neden:** saklama süresi kararının ertelenebilmesi bölümlendirmeye dayanıyordu —
eski ayı silmek tek komut olsun diye. Bölümlendirme olmadan o gerekçe geçersizdi.

**Neden şimdi:** tablo boştu. Veri girdikten sonra bölümlendirmek satır kopyalama
demek; migration bunu bildiği için tabloyu boş bulmazsa **durup hata fırlatıyor**.

**Neden bileşik anahtar:** Postgres, bölümlenmiş tabloda birincil anahtarın ve her
benzersizlik kısıtının bölümleme anahtarını içermesini şart koşuyor. Bedeli yok —
`EventLogs`'a işaret eden yabancı anahtar ve navigasyon zaten hiç yok.

### Bölümlendirme dünkü bir korumada DELİK AÇTI

Prototipte ölçüldü — ayrı bir deneme veritabanı kuruldu, varsayımla ilerlenmedi:

| Davranış | Sonuç |
|---|---|
| Satır bazlı tetikleyici üst tablodan parçalara yayılıyor mu | evet |
| Deyim bazlı boşaltma tetikleyicisi yayılıyor mu | **HAYIR** |

Bir ay parçasına doğrudan boşaltma komutu **hiçbir hata vermeden geçti**. Dün
kapatılan açık, bölümlendirmeyle yeniden açılmış olacaktı.

**Çözüm:** tetikleyici hem üst tabloya hem **her parçaya ayrı** kuruluyor;
`ensure_event_log_partition()` yeni parça açarken tetikleyiciyi de kuruyor, yani
unutulması mümkün değil.

### Parça bitmesi bir kesinti riskidir — iki katmanlı koruma

1. Peşinen 24 ay açık
2. Kapsanmayan tarih gelirse **varsayılan parçaya** düşüyor, yazma başarısız olmuyor

Varsayılan parçanın bedeli: o aralık için sonradan gerçek parça eklenemez, önce
satırların taşınması gerekir.

⚠️ **`ensure_event_log_partitions(24)` düzenli çağrılmalı.** Zamanlanmış iş yok;
`A-14` olarak açıldı. Çağrılmazsa 24 ay sonra her olay varsayılan parçaya yığılır
ve bölümlendirmenin faydası kaybolur.

### Ölçülen bedel: tarihsiz sorgu 26 parçayı da tarıyor

Payload içinde arama, tarih filtresi olmadan tüm parçalara yayılıyor (sorgu planıyla
görüldü). Sezonluk AI raporları zaten tarih sınırlı olacağı için uyumlu, ama
**olay günlüğü sorguları tarih aralığı içermeli** — yoksa bölümlendirme fayda değil
maliyet olur.

### Kanıt

10 senaryo canlı denendi: doğru parçaya yönlendirme · `Seq` parçalar arası artıyor ·
güncelleme ve silme hem üst tablodan hem parçadan **reddedildi** · boşaltma üst
tabloda, ay parçasında ve varsayılan parçada **reddedildi** · tarih aralığı sorgusu
**tek parça** tarıyor · `Seq` imleci çalışıyor.

Migration **geri alınıp tekrar uygulandı**: bölümlenmiş, sıradan, tekrar bölümlenmiş.
`dotnet build` 0 uyarı 0 hata. Toplam 101 tablo (75 tablo + 26 parça).

**EF Core sapması yok:** EF tabloyu sıradan bir tablo olarak modelliyor;
bölümlendirmeyi bilmiyor ama kolonlar, anahtar ve indeksler birebir örtüştüğü için
bir sonraki `migrations add` fark üretmiyor.

İlgili: [[api-sema]] · [[api-durum]] · [[domain-gereksinimler]]

---

## 2026-08-24 — A-15: zamanlanmış iş katmanı, Hangfire'sız

**Karar:** Tek bir `BackgroundService` (`ScheduledJobRunner`) ve `IScheduledJob`
arayüzü. Hangfire, Quartz veya benzeri **eklenmedi**.

**Neden eklenmedi:** bu ölçekte beş iş var ve hiçbiri dakikadan sık çalışmıyor.
Hangfire ek bağımlılık, ek tablolar, ek panel ve ek yapılandırma demek. Sırası
geldiğinde (birden çok sunucu, yeniden deneme politikası, iş kuyruğu) arayüz
korunarak değiştirilebilir — Redis'i eleme gerekçesiyle aynı.

**Neden ertelenemezdi:** bu katman olmadan **veritabanı kısıtları sistemi
kilitliyordu**. Canlı üretildi ve ölçüldü:

| Adım | Sonuç |
|---|---|
| Terk edilmiş ödeme 12 koltuk tutuyor | `SoldSeats = 12` |
| Aynı sefere yeni rezervasyon | `CK_Voyages_SoldSeats` ile **reddedildi** |
| İş çalıştı | `SoldSeats` **12 -> 0** |
| Aynı sefere yeni rezervasyon | **kabul edildi** |

**Şemanın en güçlü iki garantisi, iş katmanı yokken sistemi kilitleyen
mekanizmalara dönüşüyordu.** Kısıtlar yanlış değildi; eksik olan onları serbest
bırakacak katmandı. Bu, "kuralı veritabanına koy" ilkesinin bedeli: kural
uygulanır ama serbest bırakma da uygulanmak zorunda.

### Beş iş

| İş | Aralık | Çalışmazsa |
|---|---|---|
| `rezervasyon-tutma-suresi` | 1 dk | Koltuklar **kalıcı kilitlenir**, sefer satılamaz |
| `teklif-suresi` | 5 dk | Tarih **sonsuza kadar kapalı** kalır (EXCLUDE kısıtı) |
| `konusma-kapatma` | 1 saat | Konuşma süresiz açık kalır (kilitlenme değil, sessiz yanlış) |
| `sefer-tamamlama` | 1 saat | Hakediş hesabı seferi "gerçekleşmemiş" sayar, para ödenmez |
| `olay-gunlugu-parcalari` | 24 saat | 24 ay sonra olaylar varsayılan parçaya yığılır (`A-14`) |

**Koltuk sayacı elle azaltılmıyor:** rezervasyon durumu `Expired`'a çekiliyor,
`trg_reservation_sync_seats` sayacı kendisi yeniden hesaplıyor. Sayaç tek yerden
yönetildiği için işteki bir hata onu bozamıyor.

**Teklif seferi silinmiyor, `Cancelled`'a çekiliyor:** `EXCLUDE` kısıtı iptal
edilmiş seferleri zaten dışlıyor, ve kaydı silmek geçmişi yok etmek olurdu.

### "Çalışmadığında görülüyor" — kabul ölçütünün ikinci yarısı

`JobRuns` tablosu her çalışmayı kaydediyor, **başarısız olanı da**. Yalnız
başarılıyı kaydetmek, hata anında hiç iz bırakmamak olurdu.

`GET /api/health/jobs` — her iş için son çalışma, geçen süre, işlenen kayıt ve
hata. `platform.settings` yetkisi gerektiriyor: hangi işlerin çalıştığı ve hata
mesajları operasyonel bilgi. Yetkisiz istekte **401** doğrulandı.

**Kayıt yazımı ayrı bir kapsamda yapılıyor:** işin kendi `DbContext`'i hatalı
duruma düşmüş olabilir ve o zaman kaydı da yazamazdı — yani hata anında hiç iz
kalmazdı. Tam da en çok ize ihtiyaç duyulan an.

**Her iş kendi kapsamında çalışıyor:** `DbContext` scoped, arka plan servisi
singleton. Doğrudan enjekte edilseydi tek bir `DbContext` uygulama ömrü boyunca
yaşar, değişiklik izleyicisi büyür ve bir işin hatası diğerlerinin durumunu
kirletirdi.

### Henüz yapılmayan iki iş

`ExchangeRates` günlük TCMB çekimi ve periyodik hakediş üretimi bu dilimde YOK.
İkisi de dış sisteme veya para kararına bağlı; ayrı görev olarak açılacak.
⚠️ Kur tablosu boş kaldığı sürece **dövizli tekne satılamaz**.

İlgili: [[api-sema]] · [[api-durum]] · [[api-gorevler]]

---

## 2026-08-24 — A-15 denetimi: bir DI hatası tüm API'yi düşürüyordu

**Karar:** `ScheduledJobRunner` baştan sona sarmalandı, işler somut tiple
çözülüyor, kapanış iptali hata sayılmıyor.

**Neden:** `csharp-reviewer` denetimi üç gerçek kusur buldu ve **ikisini ayrı bir
host kurarak deneyerek** doğruladı — okuyarak değil.

### 🔴 En ağırı: sınıf kendi yorumunu yalanlıyordu

`ScheduledJobRunner`'ın yorumunda *"bir işin hatası diğerlerini durdurmaz"*
yazıyordu. Gerçekte yalnız `job.RunAsync` sarmalanmıştı; DI çözümlemesi
(`CreateScope`, `GetRequiredService`, `First(j => j.Name == ...)`) korumasızdı.

.NET'te `BackgroundService` içinden çıkan istisna varsayılan olarak
**tüm host'u durduruyor** (`BackgroundServiceExceptionBehavior.StopHost`).
Yani bir iş adı yanlış yazılsa **web API'sinin tamamı düşecekti** — arka plan
işi değil, sitenin kendisi.

**Bu, en sinsi hata türü:** kod doğru görünüyordu, yorum güvence veriyordu ve
tetikleyici koşul (isim uyuşmazlığı) bugün oluşmuyordu. Yarın bir iş yeniden
adlandırılsa üretimde ortaya çıkardı.

### 🔴 İkincisi: izleme sisteminin kendisi yanlış alarm üretiyordu

Kapanış sırasında iptal, genel `catch` tarafından **başarısızlık** sayılıyordu.
Üstelik başarısızlık kaydı **aynı iptal edilmiş jetonla** yazılmaya çalışılıyordu,
yani o da başarısız oluyordu.

Sonuç: her düzgün yeniden başlatma `JobRuns`'a sahte bir arıza yazacaktı ve
sağlık ucu (`basarisiz` sayacı) gerçek olmayan bir sorun gösterecekti — tam da
gerçek arızayı görünür kılmak için kurulan mekanizma, güveni bozan bir gürültü
kaynağına dönüyordu.

**Düzeltme:** kapanış iptali `catch (OperationCanceledException) when
(ct.IsCancellationRequested)` ile ayrıldı ve kayıt yazımı **ayrı, iptal edilmemiş**
bir jeton kullanıyor.

### 🟡 Üçüncüsü: her çalıştırmada altı işin altısı da inşa ediliyordu

İş adıyla aranıyordu (`GetServices<IScheduledJob>().First(...)`), bu da kayıtlı
bütün işleri — her birinin `DbContext` ve `HttpClient` bağımlılıklarıyla —
yaratıp beşini atmak demekti. Artık somut tiple çözülüyor
(`AddScheduledJob<T>()` hem tipi hem arayüzü kaydediyor).

### Belgelenen kör nokta

Kayıt yazımının ayrı kapsamda olması yalnız `DbContext` bozulmasına karşı işe
yarıyor. İşin hatası **veritabanına erişememekten** kaynaklanıyorsa kayıt da
yazılamıyor ve `JobRuns`'a hiç satır düşmüyor. Denetim bunu haklı olarak
"yorumun fazla söz verdiği" bir nokta diye işaretledi; yorum düzeltildi ve
izlemenin ayrıca günlük hata oranına bakması gerektiği yazıldı.

### Kanıt

Altı iş de çalıştı ve kaydedildi · uygulama **iş çalışırken** durduruldu ·
kapanış sonrası `JobRuns`'ta **0 başarısız kayıt** · uygulama günlüğünde
**0 kritik hata**, host düzgün kapandı.

**Doğrulanan ama hata olmayanlar** (denetim somut olarak ölçtü): `CloseConversationsJob`
sorgusu tam SQL'e çevriliyor, istemci tarafında değerlendirme yok ·
`AddHttpClient` typed client kaydı doğru · 15 saniyelik tur aralığı en kısa iş
aralığından küçük, işler seyrek çalışmıyor.

İlgili: [[api-durum]] · [[api-gorevler]]

---

## 2026-08-24 — A-03 ikinci dilim: parola sıfırlama, e-posta doğrulama ve değiştirme

**Karar:** Üç akış da aynı kalıpta — tek kullanımlık, süreli, özet olarak
saklanan jeton. E-posta ve SMS **sağlayıcıdan bağımsız arayüz** arkasında;
geliştirmede linkler günlüğe yazılıyor.

**Neden arayüz:** e-posta sağlayıcısı hiç seçilmedi, SMS'te eski sistemin
Verimor'u canlıda IP whitelist hatası veriyordu (`G-04`). Ödeme sağlayıcısında
yapılanın aynısı: seçim beklenmeden akış uçtan uca çalışıyor, seçim geldiğinde
yalnız bir uygulama ekleniyor ve çağıran hiçbir yer değişmiyor.

### Linkler yapılandırılmış adresten kuruluyor

`Request.Host`'tan **değil**. `AllowedHosts` gevşekken saldırgan sahte bir Host
başlığı gönderip kendi sunucusuna işaret eden bir sıfırlama linki ürettirebilir;
kullanıcı tıkladığında jeton saldırgana gider.

**Canlı denendi:** `Host: kotu-site.com` başlığıyla istek atıldı, üretilen linkte
o adres **geçmedi**.

### Parola değişince bütün oturumlar kapanıyor

Parola sızdığı için sıfırlanıyorsa, saldırganın elindeki yenileme jetonu geçerli
kalırsa sıfırlama hiçbir işe yaramaz. `RevokeAllRefreshTokensAsync` ile
kapatılıyor; **sıfırlama öncesi alınan jeton canlı testte 401 aldı**.

### E-posta değiştirme: `PendingEmail` hesap devralmayı yapısal olarak kapatıyor

Yeni adres `PendingEmail`'e yazılıyor, `Email` **değişmiyor**. Taşıma ancak
**yeni adrese giden** jeton kullanılınca oluyor — adresin sahibi olduğunu
kanıtlayan tek şey bu.

Doğrulama linki yeni adrese, **uyarı eski adrese** gidiyor: hesabı ele geçirilen
kullanıcı durumu ancak böyle fark eder.

Bu ayrım olmadan şu saldırı mümkündü: saldırgan kendi adresiyle kayıt olup
doğrular, sonra e-postasını kurbanınkiyle değiştirir; değiştirme kodu doğrulama
damgasını sıfırlamayı unutursa satır "doğrulanmış" görünür ve kurbanın geçmiş
misafir rezervasyonları saldırgana bağlanır. Artık unutmak mümkün değil, çünkü
`Email` hiç değişmiyor.

### Kullanıcı numaralandırma her yerde kapalı

`forgot-password` **her zaman 204** dönüyor: e-posta kayıtlı olsa da olmasa da,
oran sınırına takılsa da. "Çok fazla denediniz" demek bile o adresin kayıtlı
olduğunu doğrulamak olurdu.

Oran sınırı: saatte en fazla üç sıfırlama isteği (e-posta bombalamaya karşı).

### Kanıt — 12 senaryo canlı denendi

Var olan ve olmayan e-posta **aynı cevabı** verdi · sahte Host başlığı linke
sızmadı · jeton ikinci kullanımda **400** · eski parola **401**, yeni parola
**200** · sıfırlama öncesi yenileme jetonu **401** · e-posta değiştirmede `Email`
değişmedi ve `PendingEmail` doldu · zaten kayıtlı adrese değiştirme **409** ·
onaydan sonra `Email` değişti, `PendingEmail` boşaldı, doğrulama damgası yenilendi.

**Application katmanı hâlâ hiçbir pakete bağlı değil:** `IOptions<>` yerine düz
sınıf kullanıldı, değeri `Program.cs` yapılandırmadan okuyup tekil örnek olarak
kaydediyor.

İlgili: [[api-sema]] · [[api-durum]] · [[api-gorevler]]

---

## 2026-08-24 — A-03 güvenlik denetimi: hesap ele geçirme zinciri kırıldı

**Karar:** Jeton tüketimi atomik yapıldı, e-posta değiştirmede mevcut parola
zorunlu oldu, parola kuralı ve IP bazlı hız sınırı eklendi.

**Neden:** `security-reviewer` denetimi **tek çalıntı erişim jetonundan kalıcı
hesap ele geçirmeye** giden somut bir zincir gösterdi:

1. Saldırgan 15 dakikalık bir erişim jetonu çalıyor
2. `change-email` çağırıp adresi kendi adresiyle değiştiriyor — uç yalnız
   `[Authorize]` istiyordu, **parola sormuyordu**
3. Doğrulama linki saldırgana gidiyor, kurbana yalnız uyarı
4. Kurban uyarıyı görmezse saldırgan 24 saat içinde adresi devralıyor
5. Sonra sıradan parola sıfırlama akışıyla parolayı da alıyor
   — **kurbanın parolasını hiç bilmeden**

**Kırılan halka:** mevcut parola teyidi. Çalıntı jeton parolayı vermiyor.
**Canlı doğrulandı:** çalıntı jeton + yanlış parola → **401**, doğru parola → 204.

### Yorumum yine yalan söylüyordu

`ConsumeTokenAsync`'in yorumunda *"tek kullanımlık olması burada garanti
ediliyor"* yazıyordu. Gerçekte oku-kontrol-et-yaz yarışına açıktı: iki eşzamanlı
istek aynı jetonu "kullanılmamış" görebiliyordu, çünkü `ConsumedAt` bellekte
damgalanıp `SaveChanges` çağırana bırakılıyordu.

**Bugün ikinci kez** bir yorumun kodun yapmadığı bir şeyi vaat ettiği yakalandı
(ilki `ScheduledJobRunner`). Desen aynı: güvence yorumda, uygulama eksik.

**Düzeltme:** `TryConsumeUserTokenAsync` — koşul (`ConsumedAt IS NULL`) SQL'in
içinde, tek güncellemede. Etkilenen satır 1 değilse reddediyor. İleride
eklenecek her jeton akışı (sihirli link, davet, 2FA yedek kodu) bunu kullanacak.

### Diğer düzeltmeler

| Bulgu | Düzeltme |
|---|---|
| **Parola kuralı hiç yoktu** — `"1"` kabul ediliyor, PBKDF2'nin 100.000 turu anlamsızlaşıyordu | En az 10 karakter, **Application katmanında** (yalnız API doğrulaması başka istemciyle atlanabilirdi) |
| İptal + kayıt **ayrı** kalıcılaşıyordu; parola değişikliği başarısız olsa oturumlar kapanmış ama parola değişmemiş kalırdı | `ExecuteUpdate` yerine izlenen güncelleme, tek `SaveChanges` |
| Hız sınırı yalnız kullanıcı bazlı; saldırgan **farklı adreslerle** sınırsız istek atabiliyordu | IP başına 15 dakikada 10 istek. **Canlı denendi:** 8 istek geçti, sonrakiler **429** |
| Jeton standart base64 (`+ / =`) — WAF, CDN veya e-posta tarayıcısı yanlış çözerse sessizce bozulur | URL güvenli base64 (RFC 4648 §5). Doğrulandı: üretilen jetonda yalnız `-` ve `_` |
| Zayıf parola **409** dönüyordu ("çakışma"), oysa geçersiz istek | `ValidationFailedException` ayrıldı → **400**. Çakışma 409 kaldı |

### Denetimin doğruladığı ama sorun olmayan

Amaç kontrolü (`Purpose != expected`) çalışıyor — parola sıfırlama jetonu
doğrulama ucunda kullanılamıyor.

### Açık kalan

⚠️ **`UseForwardedHeaders` yok.** Ters vekil arkasında `RemoteIpAddress` proxy'nin
IP'sini döner: hem `CreatedIp` adli izi bozuk olur hem IP bazlı hız sınırı
işlevsiz kalır. Yanlış yapılandırılırsa saldırgan `X-Forwarded-For` uydurabilir.
Vekil kurulumu bilinmediği için tahmin edilmedi → görev `A-19`.

İlgili: [[api-durum]] · [[api-gorevler]]

---

## 2026-08-24 — A-06: testler gerçek PostgreSQL'e karşı çalışıyor

**Karar:** xUnit + gerçek PostgreSQL. Bellek içi sağlayıcı **reddedildi**.

**Neden:** bu şemanın değeri Postgres'e özgü kısıtlarda — `EXCLUDE USING gist`
sefer çakışmasını, tetikleyiciler komisyon tutarlılığını ve defter
değişmezliğini, `citext` e-posta benzersizliğini garanti ediyor. Bellek içi
sağlayıcı bunların **hiçbirini** uygulamaz: testler geçer ve hiçbir şey
kanıtlamaz. **Yanlış güven, güvensizlikten kötüdür.**

Şema `EnsureCreated` ile değil **migration'lardan** kuruluyor: EXCLUDE kısıtları
ve tetikleyiciler yalnız elle yazılmış migration'larda var, `EnsureCreated`
onları atlar ve testler gerçekte olmayan bir şemayı sınardı.

### İddialar mesaja değil HATA KODUNA bakıyor

İlk yazımda tetikleyici mesajlarını arıyordum ve 6 test kırıldı — mesajlar
Türkçe karakter içeriyor, testler ASCII arıyordu. Mesaj düzeltilse test yine
kırılırdı: **gerçek bir sorun olmadan kırmızıya dönen test güven kaybettirir.**
Artık SQLSTATE koduna (`23001`, `23514`) ve kısıt adına bakılıyor — ikisi de
dilden bağımsız ve kararlı.

### Test kendi hatasını gösterdi

Sefer çakışma testi başta yanlıştı: iki seferi de aynı kiralama tipiyle
kuruyordum, bu yüzden `EXCLUDE` yerine `IX_Voyages_SharedVoyagePerDay`
indeksine takılıyordu.

Bu bir kusur değil, **tasarımın doğrulanması**: aynı günde iki tur satmak,
tasarım gereği iki AYRI `BoatRentalType` satırı demek — Mert'in "sabah ve
öğleden sonra turu" kararının şemadaki karşılığı. Test senaryoya sadık hale
getirildi (Mehmet günlük tur, Cemil konaklamalı).

### Kanıt

**14 test, 14'ü geçiyor, 0 uyarı.** Kapsananlar: sefer çakışması · aynı gün
peş peşe tur · iptal edilen seferin tarihi bırakması · kapasite aşımı · defter
güncelleme, silme ve boşaltma · olay günlüğü parçasının doğrudan
boşaltılamaması · üç yetki tetikleyicisi · citext e-posta benzersizliği.

⚠️ **Testcontainers tercih edilirdi**, Docker daemon kapalıydı. Yerel sunucuda
ayrı test veritabanı kuruluyor; bağlantı dizesi ortam değişkeninden geldiği
için CI'a geçiş tek noktada → `A-20`.

⚠️ `dailycruising` rolüne test için **`CREATEDB`** verildi. `A-10`'da uygulama
rolü ayrılırken bu yetki **uygulama rolüne verilmeyecek** — yalnız geliştirme
ve migration rolünde kalacak.

İlgili: [[api-durum]] · [[api-gorevler]]

---

## 2026-08-24 — A-10: uygulama artık tabloların sahibi değil

**Karar:** İki rol. `dailycruising` sahip ve migration çalıştırır;
`dailycruising_app` uygulamanın çalışma anı rolü — veri okur ve yazar, başka
hiçbir şey yapamaz.

**Neden:** uygulama tabloların SAHİBİ olarak bağlanıyordu. Sahip
`ALTER TABLE ... DISABLE TRIGGER` diyebilir, yani *"para defteri değişmezdir"*
iddiası uygulamanın kendi kendini durdurmamasına bağlıydı.

**Bir güvence, ancak onu ihlal edebilecek olanın elinde değilse güvencedir.**
`A-15` ve `A-11`'de kurulan bütün değişmezlik korumaları bu adıma kadar
yarım kalmıştı.

**TRUNCATE bilerek verilmedi.** PostgreSQL'de ayrı bir ayrıcalık; okuma ve yazma
yetkisi onu kapsamıyor. Tetikleyicinin ötesinde ikinci katman.

**`ALTER DEFAULT PRIVILEGES` şart.** Onsuz bir sonraki migration'ın yarattığı
tabloya uygulama erişemez ve hata açılışta değil **ilk kullanımda**, üstelik
yalnız o özellikte ortaya çıkar — bulması en zor türden.

**Parola migration'a gömülmedi.** `DC_APP_ROLE_PASSWORD` ortam değişkeninden
okunuyor; yoksa migration duruyor. Sessizce zayıf bir parola kullanmaktansa
açıkça çalışmaması iyidir.

**Rol `Down`'da düşürülmüyor:** başka veritabanlarında kullanılıyor olabilir ve
düşürmek geri alınamaz. Yalnız bu veritabanındaki yetkiler geri alınıyor.

### Kanıt — yedi senaryo

Okuma ✓ · yazma ✓ · tetikleyici kapatma **"must be owner"** · tablo boşaltma
**"permission denied"** · tablo düşürme **reddedildi** · kolon ekleme
**reddedildi** · defter güncelleme tetikleyiciyle **reddedildi**.

Uygulama bu role geçirildi: sağlık ucu 200, giriş 200, altı zamanlanmış iş
çalıştı, 0 hata.

⚠️ `dailycruising` rolüne bu iş için `CREATEROLE`, `A-06` için `CREATEDB`
verildi. İkisi de **yalnız sahip/migration rolünde**; uygulama rolünde yok.

İlgili: [[api-durum]] · [[api-gorevler]]

---

## 2026-08-24 — A-08: olay günlüğü artık fiilen yazılıyor

**Karar:** `IEventLogger` arayüzü + `EventLogger` uygulaması. Kimlik olayları ve
terk edilen ödeme bağlandı.

**Neden şimdi:** tablo, bölümlendirme ve değişmezlik hazırdı ama **hiçbir olay
yazılmıyordu.** Boş bir tabloyu bölümlemek, kimsenin gelmeyeceği bir salona
sandalye dizmek gibiydi. Analiz ertelenebilir; **veri toplama ertelenemez** —
geçen sezonun olayları kaydedilmediyse sonsuza kadar yoktur.

### Üç tasarım kararı

**1. Olay yazımı ASLA istisna fırlatmıyor.** Günlük analiz içindir, işin
doğruluğu için değil: bir olayı kaybetmek kabul edilebilir, müşterinin girişini
bozmak değil. Hata yutuluyor ama uygulama günlüğüne yazılıyor.

**2. Yazma iş işleminden AYRI kapsamda.** Aynı işlemde olsaydı iki yönde de
yanlış olurdu: olay yazımındaki hata rezervasyonu geri alırdı, ya da rezervasyon
geri alındığında olay da kaybolurdu — oysa **"denendi ve başarısız oldu" tam
olarak kaydetmek istediğimiz şey**.

**3. IP tuzlu hash'leniyor.** Ham IP'nin **tuzsuz** SHA-256'sı koruma değildir:
IPv4 uzayı yaklaşık 4 milyar adres, tamamının özeti kısa sürede hesaplanıp
eşleştirilebilir. Tuz olmadan "hash'ledik" demek ham IP saklamakla neredeyse
aynı şey. Tuz yapılandırmadan geliyor; yoksa uygulama **açılmıyor**.

### Kişisel veri payload'a konmuyor

Başarısız giriş olayında e-posta adresi **yazılmıyor**, yalnız sebep
(`unknown_user` / `bad_password`). Tablo değişmez ve süresiz saklanıyor —
buraya bir kez giren kişisel veri **asla silinemez**. Kullanıcı varsa kimliği
`ActorUserId`'de zaten duruyor.

### Test iki gerçek şey buldu

**`Seq` EF tarafından geri okunmuyor.** Veritabanında doğru artıyor ama
bölümlenmiş tabloda EF `RETURNING` uygulamıyor, bellekteki nesnede sıfır
kalıyor. Sorun değil çünkü hiçbir kod ekleme sonrası o değeri kullanmıyor —
ama biri kullanmaya kalkarsa **sessizce sıfır alır**, o yüzden testte açıkça
belgelendi.

**`A-10` testlere sürtünme getirmişti:** migration uygulama rolü parolasını
ortam değişkeninden istiyor ve test çalıştıran kişiye ikinci bir değişken
sordurmak gereksizdi. Fixture tek kullanımlık bir değer veriyor.

### Kanıt

Dört kimlik olayı canlı yazıldı, IP hepsinde hash'li. **Terk edilen ödeme
yakalandı:** tutar 3000, 2 yetişkin 1 çocuk, **745 saniye sonra vazgeçilmiş** —
son alan, 15 dakikalık tutma süresinin doğru olup olmadığını ölçmenin tek yolu.

**18 test, 18'i geçiyor**, `dotnet build` 0 uyarı.

## 2026-08-24 — Fiyat sunucuda hesaplanır, istemciden tutar HİÇ alınmaz

`QuoteRequest` içinde tutar alanı **yok** ve olmayacak.

**Neden:** "İstemcinin tutarını al, sonra doğrula" güvenlik değildir.
Doğrulama bir kod yolunda atlanabilir, yeni bir uçta unutulabilir, yuvarlama
farkıyla gevşetilebilir. **Alan hiç var olmazsa atlanacak bir şey de olmaz.**
Canlı denendi: istek `grandTotalTry: 1` ve `discountAmountTry: 9999` gönderdi,
sunucu 1000.00 ve 0 döndü — alanlar reddedilmedi, hiç okunmadı.

### Kuponun matrahı: tur + ek hizmet

**Neden:** komisyon matrahı da tur + menü + ek hizmet. İki oran ayrı tabana
uygulansaydı "kupon komisyonu aşamaz" kuralı farklı şeyleri karşılaştırdığı
için anlamını yitirirdi. Mert'e soruldu -> [[api-durum]] S-7.

### Kupon reddinin sebebi SÖYLENMİYOR

Altı ayrı ret mesajı vardı; hepsi tek metne indirildi.

**Neden:** ayrıntılı mesaj kimliksiz çağırana keşif aracı veriyordu. "Bu
kupon bu işletmede geçerli değil" cevabı kodun GERÇEK olduğunu ve başka bir
işletmeye ait olduğunu söylüyordu. Daha kötüsü "komisyonu aşıyor" cevabı,
bilinen oranlı kuponlar denenerek işletmenin **komisyon oranının** ikili
aramayla bulunmasına izin veriyordu — komisyon oranı sözleşme verisidir.
Bedeli: gerçekten süresi dolmuş bir kuponu getiren müşteri artık sebebi
göremiyor. Takas bilinçli.

### `MinPassengers` fiyat sorgusunda kontrol EDİLMİYOR

Denetim "kontrol edilmiyor" diye işaretledi; **uygulanmadı**.

**Neden:** o sınır sefere kopyalanıyor, rezervasyona değil. Paylaşımlı seferde
asgari 8 kişilik tura 2 kişilik rezervasyon meşrudur; sefer dolmazsa iptal
edilir. Fiyat sorgusunda kontrol edilseydi geçerli bir satış reddedilirdi.
Denetim bulgusunun kendisi doğru, önerdiği düzeltme yanlıştı.

### Denetim dört gerçek açık buldu — hepsi CANLI üretildi

Hiçbiri okumayla kabul edilmedi; her biri istek atılarak doğrulandı, düzeltildi
ve yeniden denendi.

**`int` taşması kapasite kontrolünü atlıyordu.** 2 milyar yetişkin + 2 milyar
çocuk toplamda `-294.967.296` oluyor, 12 kişilik teknenin kontrolünü geçiyor ve
**1,6 trilyon TL**'lik teklif HTTP 200 dönüyordu. Sayılar artık toplanmadan
önce tek tek sınırlanıyor — sıra önemli, sonra sınırlamak işe yaramaz.

**İki ayrı yoldan HTTP 500.** `Nights = int.MaxValue` taşıp negatife düşüyor;
9999-12-20 kalkışlı konaklamalı tur ise taşma olmadan takvimin sonunu aşıyor.
İkisi de `DateOnly.AddDays` içinde yakalanmamış hata veriyordu.

**Ek hizmet satırı sınırsızdı.** 200.000 satırlık tek bir kimliksiz istek
26 MB cevap ürettiriyordu. Dahası aynı menü 200.000 kez sayıldığı için
**2 yolcuya 40 milyon TL**'lik ek hizmet çıkıyordu: satır başına yapılan "adet
yolcu sayısını aşamaz" kontrolü, satır sayısı sınırsız olduğu için hiçbir şey
engellemiyordu. Sınır + aynı hizmetin tekrarının reddi birlikte kapatıyor.

**Kupon aramam indeksi öldürüyordu.** `c.Code.ToUpper() == code.ToUpper()`
yazmıştım. Kolon zaten `citext`, yani harf duyarsızlığı bedava geliyordu;
`upper()` sarmalaması `IX_Coupons_Code`'u kullanılamaz kılıp her fiyat
sorgusunda tabloyu baştan sona taratıyordu. Ölçüldü: `upper()` ile `Seq Scan`,
düz eşitlikle `Index Only Scan`. **Kendi eklediğim satır hem gereksiz hem
zararlıydı.**

### Sözleşme seçiminde kesin sıralama

`ORDER BY ApprovedAt DESC` tek başına kesin değil.

**Neden:** yönetici birkaç sözleşmeyi tek `UPDATE` ile onaylarsa damgalar
eşitlenir. Aynı ifade içindeki üç ayrı alt sorgu o zaman farklı satır
seçebilir — komisyon oranı bir sözleşmeden, kimliği başkasından gelir.
`ThenByDescending(Id)` eklendi. **Tek sorguda okumak tek başına yetmiyormuş;**
sınıfın yorumu bunu güvence diye anlatıyordu, düzeltildi.

### Yazdığım iki yorum fazlasını iddia ediyordu

`Quote` için "ikisinin ayrışması mümkün değil", controller için "rezervasyon
oluşturulurken AYNI servisle yeniden hesaplanır" yazmıştım. İkisi de bu
dosyaların sağlayamayacağı, üstelik rezervasyon oluşturma ucu **henüz
yazılmadığı** için bugün doğrulanamaz iddialar. Niyet olarak yeniden yazıldı.

**Neden:** bu depo yorumun yalan söylemesinden iki kez zarar gördü. Güvence
diye yazılan şey güvence değilse, sonraki okuyan ona güvenip kontrol koymaz.

### Kanıt

`POST /api/pricing/quote` canlı çağrıldı. Doğru hesap: 2 yetişkin + 1 çocuk +
1 bebek → 1300.00 TL. Kupon: %15 komisyonda %10 kupon → 900 TL, %20 kupon →
indirim 0. Kapasite: 12 kişilik teknede 13 yetişkin → 400. Dört açık kapandı,
dördü de yeniden denendi → 400. Hız sınırı → 61. istekte 429. Production
kipinde beklenmeyen hata → yığın izi yok. **42 test, 42'si geçiyor.**

## 2026-08-24 — Veritabanı denetimi: iki indeks hiç yaratılmamış

`database-reviewer` canlı veritabanında `EXPLAIN` çalıştırdı. Üç bulgu, üçü de
doğrulandı.

### `Prices.BoatRentalTypeId` ve `Contracts.PartnerId` indeksleri YOKTU

Yapılandırma ikisini de istiyordu; EF aynı kolona yapılan ikinci `HasIndex`
çağrısını birincinin yerine koyduğu için hiç yaratılmamışlardı.
`Contracts` tarafında yanlarında **"bu sorgu kısmi indeksi kullanamaz"**
yorumu duruyordu — yorum ihtiyacı doğru anlatıyor, indeks yok.

**Neden fark edilmedi:** derleme temiz, testler geçiyor, sorgular doğru sonuç
veriyor. Yalnız yavaş. Bunu ancak `pg_indexes`'e bakmak gösteriyor.
`HasDatabaseName` eklemek de yetmedi; ad ikinci parametre olarak verilmeli
-> [[api-hasindex-yutulmasi]]

### `ExchangeRates` indeksinin sırası fiyat sorgusuna ters

Tek indeks `(Date, CurrencyCode)`. Fiyat hesabı ise
`WHERE CurrencyCode = x ORDER BY Date DESC LIMIT 1` sorguyor — para birimi
baştaki kolon olmadığı için Postgres indeksi tarihe göre GERİ YÜRÜYEREK
tarıyor, eşleşen satıra varana kadar diğer para birimlerinin satırlarını
geçiyor.

**Neden mevcut indeks silinmedi:** TCMB işi `WHERE "Date" = @date` sorguyor,
onun için sıra Date-önce kalmalı. İkinci indeks eklendi.
Ölçüldü: geri yürüyüşle 19.32, yeni indeksle 8.15.

### Fiyat sorgusu iki gidiş-dönüşten bire indi

Önce "sezon var mı", yoksa "temel fiyat" diye iki sorgu atılıyordu — ve
YAYGIN durum olan "sezon tanımlı değil" her seferinde ikisini birden
yapıyordu. Tek sorguya indi; sıralama sezonu öne alıyor.

**Neden güvenli:** `EX_Prices_NoOverlappingSeasons` en fazla bir sezonun,
`IX_Prices_SingleBasePrice` en fazla bir temel fiyatın eşleşmesini garanti
ediyor. Yani "hangisi kazanır" belirsizliği yok.

### Doğrulanan bir şey: sezon koşulunda boşluk YOK

`ValidFrom` dolu ama `ValidTo` boş bir satır koşulu sessizce atlardı.
`CK_Prices_RangeComplete` böyle bir satırı imkânsız kılıyor — kontrol edildi,
düzeltme gerekmedi.

### Sonraya bırakılan: kupon kullanım sayımı yarış açık

`CountCouponRedemptionsAsync` sayıp karşılaştırıyor; arada kilit yok. Bugün
sömürülemez çünkü yazan bir yol yok — fiyat sorgusu salt okuma. Rezervasyon
oluşturma ucunda (`A-22`) aynı kontrol olduğu gibi kullanılırsa iki eşzamanlı
rezervasyon `MaxRedemptions`'ı aşabilir. `CK_Coupons_Redemptions` bunu
kapatmıyor: o yalnız `UsedCount` kolonunu sınırlıyor, bu kod ise o kolona
bilerek güvenmiyor.

### Kanıt

Üç indeks migration'la yaratıldı ve `pg_indexes`'te görüldü. Tekleştirilmiş
sorgunun planı yeni `IX_Prices_BoatRentalTypeId` üzerinden tek tarama.
Canlı: eylül kalkışı 1800 TL (sezon), kasım kalkışı 1000 TL (temel) —
sezon önceliği bozulmadı. **42 test, 42'si geçiyor.**

İlgili: [[api-sema]] · [[api-durum]] · [[domain-gereksinimler]]

---

## 2026-08-24 — Mert sekiz bekleyen soruyu cevapladı (S-1…S-9)

**Karar:** `api-durum.md` "Mert'e sorulacaklar" tablosundaki sekiz soru ve denetimden
çıkan dokuzuncusu cevaplandı. Üçü kod değişikliği gerektirdi, altısı mevcut varsayımı
onayladı.

| # | Soru | Cevap | Kod değişti mi |
|---|---|---|---|
| S-1 | TCMB hangi kuru | *"Sana bırakıyorum"* → **`ForexSelling`** korundu | hayır |
| S-2 | Parola kuralı | *"Çok karmaşık olmasın, hızlı kayıt olabilsinler"* → asgari **8**, karmaşıklık yok | **evet** |
| S-3 | Hesap uçlarında hız sınırı | IP başına 15 dk'da 10 istek **onaylandı** | hayır |
| S-4 | E-posta değişiminde mevcut parola | **Sorulsun** — onaylandı | hayır |
| S-5 | Başarısız girişte denenen adres | **Loglansın** | **evet** |
| S-6 | Olay günlüğü ayrıntısı | *"Ayrıntılı olursa AI'a vereceğimiz veri daha iyi olur"* | **evet** |
| S-7 | Kuponun matrahı | Tur + ek hizmet — **olduğu gibi kalsın** | hayır |
| S-8 | Fiyat ucunda hız sınırı | Dakikada 60 — **onaylandı** | hayır |
| S-9 | Kupon reddinde sebep | **Müşteri sebebini görsün** | **evet** |

**Neden (S-1, Claude'a bırakıldı):** Dört TCMB değeri arasından **döviz satış**
(`ForexSelling`). Yabancı para cinsinden bir borcu TL'ye çevirmenin ticari standardı
bu ve platform lehine ihtiyatlı olan da bu — efektif kurlar nakit işlemler için,
bizim işlemimiz nakit değil. Alış kuru seçilseydi platform her yabancı para turunda
kur farkını üstlenirdi. Değiştirmek `TcmbExchangeRateSource` içinde tek satır.

**Neden (S-2, 10 → 8):** Mert'in isteği karmaşıklık değil **hız**. Karmaşıklık şartı
zaten yoktu; kayıt akışını yavaşlatan şey uzunluktu. 8, NIST SP 800-63B'nin
kompozisyon kuralsız tabanı — altına inilmedi. Kaba kuvvetin asıl freni burada değil:
PBKDF2 100.000 tur + IP başına 15 dakikada 10 istek. 10'da tutmak, güvenliği
artırdığından daha çok kaydı yavaşlatıyordu.

**Neden (S-5, adres loglanıyor):** Kaba kuvvet ve kimlik-doldurma analizinde "hangi
adres denendi" en değerli sinyal ve başka hiçbir tablo tutmuyor. Adres normalize
ediliyor (trim + küçük harf) ki aynı hedefe yapılan denemeler `Ali@X`/`ali@x` diye
ikiye bölünmesin, ve **254 karakterde kesiliyor** (RFC 5321 üst sınırı) — giriş
formuna megabaytlık metin yapıştırılabilir.

⚠️ **Bedeli geri alınamaz ve bilinerek kabul edildi.** `EventLogs` append-only;
UPDATE/DELETE tetikleyiciyle reddediliyor, TRUNCATE yetkisi uygulama rolünde yok.
Buraya giren adres **silinemez**. Hesabı olmayan birinin adresi de düşüyor: biri
e-postasını yanlış yazdığında ÜÇÜNCÜ bir kişinin adresi kalıcı olarak kaydedilir.
`A-12` (KVKK) bu satırı ayrıca ele almak zorunda.

**Neden (S-6, olay günlüğü genişletildi):** *"Analiz ertelenir, VERİ TOPLAMA
ertelenemez"* ilkesinin devamı. Bugün bağlanabilen tek uç fiyat sorgulama olduğu için
oradan başlandı: `pricing.quoted`, `pricing.quote.failed`, `coupon.applied`,
`coupon.rejected`. Fiyat sorgusu **rezervasyona dönüşmeyen talebin tek izi** — hangi
tekneye, hangi tarihe, kaç kişiyle bakıldığı başka hiçbir tabloda yok.
`pricing.quote.failed` ise kaçırılan satışın doğrudan ölçüsü ("o tarihte fiyat yok").
Arama, tekne görüntüleme ve oturum takibi ilgili uçlar yazılmadığı için hâlâ `A-21`'de.

**Neden (S-9, ret sebebi ayrıştırıldı — aynı günün sabahındaki kararı İPTAL EDER):**
2026-08-24 sabahı güvenlik denetimi üzerine altı ayrı mesaj tek metne indirilmişti
("Kupon geçerli değil."). Mert aynı gün geri istedi: *"kupon reddedilince müşteri
sebebini görsün"*. Gerçekten süresi dolmuş bir kuponu olan müşterinin nedenini
görememesi, teorik bir keşif riskinden ağır basıyor.

Bedeli ölçüldü ve kabul edildi: **sızıntı mesajın metninde değil, cevapların
birbirinden ayırt edilebilmesinde.** Kimliksiz çağıran "bu işletmede geçerli değil"
cevabından kodun gerçek olduğunu anlar. Bu yüzden komisyon dalına muğlak bir metin
yazmak hiçbir şey kazandırmazdı — o dal da açıkça yazılıyor ("bu turda
kullanılamıyor"), yalnız komisyondan söz etmiyor: oranı yazmak, ayrıştırılabilirliğin
verdiği kaba eşiği kesin değere çevirirdi.

Pratikteki sınır: **kupon üretmek işletmeye ya da platforma ait.** Saldırgan
istediği oranda kupon üretip ikili arama yapamaz, yalnız var olan kuponları
deneyebilir; oranı bilinen genel kuponlar komisyon için kaba bir eşik verir.

**Alternatifler:** Ret sebebini yalnız giriş yapmış kullanıcıya göstermek — kimliksiz
çağıranı korurdu ama fiyat ucunun kimliksiz kalması bilinçli bir karar
(müşteri üye olmadan fiyat görmeli), iki modlu cevap ise arayüzde ikinci bir yol
demekti; elendi. Komisyon dalını tek metinde bırakıp diğerlerini ayrıştırmak —
ayrıştırılabilirlik zaten sızdırdığı için hiçbir şey kazandırmıyordu; elendi.

**Ayrıştırılan sebepler:** `NotFound` · `Inactive` · `NotStarted` · `Expired` ·
`OtherPartner` · `OtherBoat` · `LimitReached` · `ExceedsCommission`. Metnin yanında
**makine okunur** bir kod da dönüyor (`Quote.CouponRejectionCode`) — arayüz metne
göre dallanmasın (metin değişince koşul sessizce bozulur) ve olay günlüğüne serbest
metin yerine sabit bir değer düşsün diye.

İlgili: [[api-durum]] · [[api-desenler]] · [[api-gorevler]]

---

## 2026-08-24 — S-1…S-9 denetimi: üç ajan, dört bulgu, üçü düzeltildi

**Karar:** Cevapların uygulanmasından sonra `csharp-reviewer`, `security-reviewer`
ve `database-reviewer` çalıştırıldı. Dört gerçek bulgu çıktı; üçü düzeltildi, biri
Mert'e soruldu (`S-10`), ikisi ortam görevine dönüştü (`A-23`).

### 1. Denetim kaydını saldırganın kendisi sildiriyordu — DÜZELTİLDİ

`IEventLogger.LogAsync` bir `CancellationToken` alıyordu ve **13 çağrı yerinin
hepsi** isteğin kendi jetonunu geçiyordu, yani `HttpContext.RequestAborted`'ı.
Bağlantısını koparan istemcide `SaveChangesAsync` iptal oluyor, `EventLogger`'ın
genel `catch`'i istisnayı yutuyor ve kayıt hiç yazılmıyordu.

**Neden ciddi:** kaba kuvvet ve kupon deneme betikleri cevabı beklemez. Yani
`auth.login.failed` ve `coupon.rejected` — S-5'in ve S-6'nın tam amacı olan iz —
saldırgan tarafından silinebiliyordu.

**Ölçüldü:** 30 ms'de kesilen 3 istek → eski davranışta **0 kayıt**, yeni
davranışta **3 kayıt**. Ayrıntı ve 10 ms tuzağı → [[api-olay-gunlugu-iptal-jetonu]]

**Neden parametre kaldırıldı, "None geçin" denmedi:** 13 çağrının 13'ü de yanlış
geçiyordu; yanlış kullanım istisna değil kuraldı. Bu projede tekrarlanan ilke —
yanlış geçilebilen alan er ya da geç yanlış geçilir, var olmayan alan geçilemez.
`QuoteRequest`'te tutar alanının bulunmaması da aynı ilke.

### 2. `/api/auth/login` hiçbir hız sınırına tabi değildi — DÜZELTİLDİ

`AccountController` ve `PricingController` sınırlıydı, **`AuthController` değildi**.
Canlı doğrulandı: 40 ardışık başarısız giriş, 40 kez 401, tek bir 429 yok.

⚠️ **Bu, aynı gün alınan S-2 kararının dayanağını çürütüyordu.** Asgari parolayı
8'e indirmenin gerekçesi "kaba kuvvetin freni PBKDF2 + 15 dakikada 10 istek"
diye yazılmıştı; o fren giriş ucunda fiilen yoktu.

`login` ve `register` mevcut `hesap` politikasına bağlandı (Mert'in S-3'te
onayladığı sayı). **Sınıfa toptan uygulanmadı:** `refresh` ve `logout` yüksek
frekanslı, tek IP arkasındaki bir ofiste 15 dakikada 10 tazeleme normaldir ve
meşru kullanıcılar kilitlenirdi. Tazeleme jetonu 256 bit ve karma üzerinden
karşılaştırılıyor, denenerek bulunamaz — kaba kuvvet yüzeyi değil.

**Alternatif:** giriş için ayrı ve daha gevşek bir politika — sayı uydurmak
olurdu, elendi. Sınır darlık yaparsa görünür ve tek satırda genişler; sınırsızlık
sessizdi.

### 3. Olay günlüğüne serbest metin girebiliyordu — DÜZELTİLDİ

`NormalizeEmailForLog` yalnız kırpıp kesiyordu, **biçim doğrulamıyordu**. Giriş
kutusuna yazılan her şey — yanlışlıkla yapıştırılmış bir parola, bir not, üçüncü
birinin verisi — 254 karaktere kadar değişmez tabloya düşüyordu.

Artık e-postaya benzemeyen girdi, girdinin kendisi yerine `(e-posta bicimi degil)`
işaretiyle kaydediliyor: deneme sayısı ve IP korelasyonu korunuyor, içerik
saklanmıyor. Canlı denendi — `<script>alert(1)</script>` ve serbest metin
işaretle, gerçek adres kendisiyle kaydedildi.

**Neden hash'lenmedi:** denetim adresi tuzlu SHA-256 ile saklamayı önerdi. Mert
açıkça *"loglansın"* dedi; adresi göremezse suistimal analizi yapamaz. Karar
Mert'in, öneri uygulanmadı.

`IEventLogger.Payload` belgesindeki "kişisel veri KONMAZ" cümlesi **artık yalandı**,
yeniden yazıldı: kişisel veri ancak açık kararla girer, serbest metin hiç girmez.

### 4. Kupon oracle'ı — DÜZELTİLMEDİ, `S-10` olarak Mert'e soruldu

Denetim, platform geneli kuponlarda `ExceedsCommission` ret sebebini gizlemeyi
önerdi. **Uygulanmadı ve gerekçesi şu:** sızıntı mesajda değil. Kuponun uygulanıp
uygulanmadığı (`discountAmountTry` 180 mi 0 mı) zaten aynı eşiği veriyor; mesajı
gizlemek hiçbir kanalı kapatmaz, yalnız kapatmış gibi görünürdü.

Gerçekten kapatmak için ya "kupon komisyonu aşamaz" kuralını kaldırıp indirimi
kırpmak ya da kupon değerlendirmesini kimliğe bağlamak gerekir — ikisi de iş
kararı, tahmin edilmedi → [[api-durum]] `S-10`.

### 5. Ortam kaynaklı iki risk → `A-23`

Npgsql havuz tavanı verilmemiş (varsayılan 100 = Postgres'in tamamı) ve
`ensure_event_log_partition()` sunucunun `TimeZone` GUC'una bağlı. İkisi de kodda
değil ortamda; dağıtımdan önce doğrulanacak.

Ayrıca: `Payload` üzerindeki GIN indeksi `->>` sorgularını hızlandırmıyor →
[[api-jsonb-gin-opclass]]

İlgili: [[api-durum]] · [[api-gorevler]] · [[api-notlar]] · [[api-desenler]]

---

## 2026-08-24 — A-22: rezervasyon oluşturma uç noktası

**Karar:** `POST /api/reservations` yazıldı. Kimliksiz çağrılabiliyor, tutarı
sunucu sıfırdan hesaplıyor, kapasite/çakışma/kupon kararlarını veritabanı
kısıtları veriyor.

**Neden istek TUTAR DA `Quote` DA TAŞIMIYOR:** A-04'te fiyat sorgusu için verilen
kararın devamı. Fiyat sorgusunun cevabını istemciden geri almak, "istemcinin
tutarı belirlemesi"ni bir adım geriye taşımaktan ibaret olurdu — cevap istemcinin
elinden geçmiş demektir. İstek fiyat sorgusuyla AYNI girdileri taşıyor ve tutar
`PricingService.QuoteAsync` ile yeniden hesaplanıyor.

Bunun kabul edilen bedeli: müşteri fiyatı gördükten sonra tekne sahibi fiyatı
değiştirirse rezervasyon YENİ tutarla oluşur. Alternatif (sorgunun cevabını
imzalayıp bağlayıcı saymak) düşünüldü ve elendi — imzalı da olsa istemcinin
taşıdığı bir tutarı bağlayıcı yapmak aynı kapı.

**Neden `ReservationFactory` var:** A-04'te *"hesabın çıktısı aynı zamanda
rezervasyona dondurulacak alanların tamamıdır"* yazılmıştı ama bu bir NİYETTİ.
Alanlar iki ayrı yerde tek tek kopyalansaydı biri unutulduğunda hiçbir şey
uyarmazdı: derleme temiz geçer, testler geçer, yalnız hesap ile saklanan sessizce
ayrışırdı. Dönüşüm tek bir yerde; yeni dondurulan alan eklendiğinde eklenecek tek
yer orası.

**Neden depoda `if` yok:** kapasite `CK_Voyages_SoldSeats`, çakışma
`EX_Voyages_NoOverlapPerBoat`, paylaşımlı sefer yarışı
`IX_Voyages_SharedVoyagePerDay`, kupon hakkı `trg_coupon_redemption_limit`
tarafından reddediliyor. Uygulama kodu yalnız reddi anlamlı bir mesaja çeviriyor.
Buraya bir kontrol yazmak, onu atlayan ikinci bir kod yolunun er geç yazılması
demekti.

**Kupon hakkı artık veritabanı garantisi.** `CountCouponRedemptionsAsync` sayıp
karşılaştırıyordu, kilit yoktu — panoda TOCTOU uyarısı olarak duruyordu. Yeni
`trg_coupon_redemption_limit` önce kupon satırını `FOR UPDATE` kilitliyor, sonra
sayıyor. `Coupons.UsedCount` de artık türetiliyor; eskiden hiçbir şey onu
güncellemiyordu, yani her zaman 0 gösteren sessiz yanlış bir kolondu.

**Sayım CANLI rezervasyonlara göre.** Süresi dolan ya da iptal edilen
rezervasyonun kuponu serbest kalıyor — aksi halde ödeme ekranını terk eden her
müşteri sınırlı bir kampanya kuponunu kalıcı yakardı. `CouponRedemptions` satırı
silinmiyor, yalnız sayıma girmiyor.

### Denetim: üç ajan, üç gerçek hata (biri kritik), iki yanlış bulgu

**1. KRİTİK — terk edilen çarter takvimi kalıcı kilitliyordu.** Rezervasyon
`Expired`'a düşüyor ama açtığı `Voyage` `Planned` kalıyordu; `EXCLUDE` kısıtı
`Voyage.Status`'a baktığı için tekne TURUN BİTİŞİNE KADAR satılamıyordu.
Kimliksiz, ödemesiz, tek istekle kurulan bir takvim kilidi. Canlı üretildi ve
düzeltildi → [[api-terk-edilen-sefer-kilidi]]

⚠️ Bu hata sınıfı `ExpireOffersJob`'da ZATEN çözülmüştü ve o dosyanın başındaki
yorum sorunu birebir tarif ediyor. A-22 yazılırken o desen aranmadı.

**2. Çakışma sonrası bağlam kirli kalıyordu.** İşlem geri alınıyordu ama
reddedilen varlıklar `Added` durumunda takılı kalıyor, aynı bağlamla yapılan
sonraki kayıt onları hayalet olarak yazmaya kalkıyordu. Uygulamada `DbContext`
istek başına atıldığı için canlıda görünmüyordu; **denetimin istediği eşzamanlılık
testi yazılınca çıktı.** Testin değeri tam olarak buydu.

**3. Döngü sınırı örtüktü.** `for (;;)` idi; üst sınırı yalnız bir istisna
filtresinin `deneme < SeferDenemeSayisi` parçası sağlıyordu. Koşula taşındı.

**Yanlış çıkan iki bulgu (ölçüldü):** negatif yolcu sayısı 409 değil **400**
dönüyor — `PricingService.ValidateCounts` zaten sınırlıyor. `CreatedAtAction`
`Location` başlığını sorunsuz üretiyor (`?code=...`).

**Kilit sırası temiz — canlı kanıtlandı.** İki psql oturumuyla denendi: aynı
sefer + aynı kupon, farklı sefer + aynı kupon. İkisinde de BEKLEME var, deadlock
yok. `FromSql` + `FOR UPDATE` gerçekten kilitliyor (`pg_locks` ile doğrulandı);
EF'in alt sorguya sarması sorun çıkarmıyor.

**`IX_Reservations_Canli` eklendi.** Kupon sayımı, kupon satırı KİLİTLİYKEN
çalışıyor; orada yavaşlamak aynı kuponu kullanan bütün eşzamanlı rezervasyonları
bekletir. Kısmi indeks canlı satış sayısınca büyüyor, tablo boyunca değil.

⚠️ **Dürüstlük notu:** denetimin ölçtüğü `Seq Scan` planını kendi veri
dağılımımda YENİDEN ÜRETEMEDİM (100.000 sentetik satırda planlayıcı zaten doğru
planı seçti). Doğrulanan şey şu: indeks eklendiğinde sorgu `Index Only Scan`'e
geçiyor, heap'e hiç gitmiyor. İndeks bu yüzden "ölçülmüş bir yavaşlığın çözümü"
değil, kilit altındaki bir sorgu için ucuz sigorta olarak eklendi.

İlgili: [[api-gorevler]] · [[api-desenler]] · [[api-durum]] · [[api-sema]]

---

## 2026-08-25 — A-24: rezervasyon iptal ucu, seferi bırakma mantığı ortaklaştı

**Karar:** `POST /api/reservations/{code}/cancel`. Kimliksiz çağrılabiliyor;
koltuğu, seferi ve kuponu bırakıyor. **İade hesabı YOK.**

**Neden iade yok:** müşteri iptalinde iade oranı karara bağlanmadı — domain
dosyasında yalnız **hava iptali** için %100 kuralı var. Uydurmak yerine soru
kuyruğuna alındı (`S-12`). Bugün zaten sanal POS seçilmedi (`G-03`), yani iade
fiziken yapılamıyor; politika netleşince defter ters kaydıyla birlikte `A-18`
kapsamında yazılacak. Cevapta `refundNote` alanı var, tutar yok.

**Neden kod tek başına yetmiyor:** kod 8 karakter (~39 bit) ve misafir
rezervasyonunda müşterinin elindeki tek anahtar. Yalnız kodla iptale izin
vermek, kod deneyen birinin başkasının turunu iptal etmesi demekti. Şemanın
"kod + e-posta veya kod + telefon" kuralı burada uygulanıyor. Jetonla çağıran
sahibi için ikisi de gerekmiyor.

**Neden "kod yok" ile "kimlik tutmuyor" AYNI cevap:** ayrışsalardı kimliksiz bir
çağıran, geçerli kodları ayıklayan bir araç elde ederdi. Kupon ret sebebinde
ayrıştırılabilirliği bilerek kabul etmiştik — orada müşteriye bir şey
kazandırıyordu; burada kazandırmıyor, o yüzden kapalı. **Kimlik doğrulandıktan
SONRAKİ** mesajlar ayrışıyor ("zaten iptal edilmiş", "süresi dolmuş", "tur
gerçekleşti") — çağıran zaten sahibi olduğunu kanıtladı, oracle değil.

### Seferi bırakma mantığı ORTAKLAŞTI — asıl kazanç bu

Görev panosundaki uyarı şuydu: *"`Voyage` yaratan iki yer var ve bırakan iki
ayrı kod; iptal ucu üçüncüsü olacak, aynı hata üçüncü kez doğmasın."*

Üçüncü kopya yazılmadı. `VoyageRelease.ReleaseEmptyAsync` tek yer; hem
`ExpireReservationHoldsJob` hem iptal ucu onu çağırıyor.

Ayrıca **"canlı satış" durum listesi** tek kaynağa taşındı
(`ReservationStatuses.Live`). Bu liste dört yerde kullanılıyor — ikisi SQL,
ikisi C#:

| Nerede | Ne için |
|---|---|
| `trg_reservation_sync_seats` (SQL) | koltuk sayacı |
| `count_live_coupon_redemptions` (SQL) | kupon kullanım hakkı |
| `ExpireReservationHoldsJob` / `VoyageRelease` (C#) | seferin bırakılması |
| `PricingRepository` (C#) | kupon sayımının uygulama tarafı |

⚠️ **Bu listenin kayması hiçbir yerde hata vermez.** Bir kez kaydı: uygulama
bütün kupon kullanımlarını sayarken tetikleyici yalnız canlıları sayıyordu; iki
taraf da kendi içinde tutarlı çalışıyor, cevap yanlış oluyordu. C# tarafı artık
tek yerden okuyor; SQL tarafıyla eşleştiği **teste bağlandı**
(`Canli_durum_listesi_sql_ile_ayni` — `pg_get_functiondef` okuyup karşılaştırıyor).
Derleyici bunu göremez, o yüzden test şart.

**Kupon için ayrıca kod yazılmadı:** `Cancelled` canlı listesinde olmadığı için
hem tetikleyici hem uygulama sayımı kuponu kendiliğinden serbest bırakıyor.
Tek kaynak kuralının doğrudan getirisi.

İlgili: [[api-gorevler]] · [[api-desenler]] · [[api-durum]] · [[api-terk-edilen-sefer-kilidi]]

---

## 2026-08-25 — A-13: `EventLogs.Payload` içeriğine sınır

**Karar:** Payload artık serbest değil. Olay türü başına **izin verilen anahtar
listesi** (`EventPayloadPolicy.AllowedKeys`) var ve `EventLogger` her yazmada
uyguluyor.

**Neden:** `EventLogs` değişmez ve temizlenemez — `UPDATE`/`DELETE`
tetikleyiciyle reddediliyor, `TRUNCATE` yetkisi uygulama rolünde yok. Bir kez
giren asla silinemez. jsonb serbest olduğu sürece payload'a yanlışlıkla bir
isim, telefon ya da arama kutusuna yazılmış bir metin koyan **tek bir satır**
kalıcı bir KVKK sorunu üretiyordu.

Nokta çözümler zaten vardı — `NormalizeEmailForLog`, `Kisalt`, `KodBicimi` — ama
**kural yoktu**: yeni bir olay yazan birinin hiçbirini bilmesi gerekmiyordu.
Artık kural tek yerde ve uygulaması çağıranın dikkatine bağlı değil.

**Beş kural, hepsi fail-closed:**

| Durum | Ne oluyor |
|---|---|
| Olay türünün listesi yok | Payload **düşer**, olay yazılır, uygulama günlüğüne ERROR |
| Listede olmayan anahtar | Anahtar düşer, uyarı |
| İç içe nesne/dizi | Düşer — kesme derinlemesine yapılamıyor, payload'lar düz kalmalı |
| 512 karakterden uzun metin | **Kırpılır**, atılmaz: "bir şey yazılmıştı" bilgisi analiz için değerli |
| 4096 bayttan büyük payload | Tamamen düşer — kırpmak jsonb'yi bozardı |

**Neden fail-closed:** açık bırakılsaydı yeni bir olay türü eklemek sessizce
sınırların dışına çıkmak olurdu. `EventTypes` içindeki her sabitin listede
karşılığı olduğu **testle** sabitleniyor
(`Her_olay_turunun_payload_listesi_var`, iki yönlü: eksik ve fazla). Derleyici
bunu göremez.

**Neden olay düşmüyor, yalnız payload:** olayın kendisi (tür, aktör, zaman, IP
özeti) sınırın dışında değil ve analiz için değerli. Listesi unutulmuş bir olay
türünde her şeyi atmak, düzeltilebilir bir eksikliği veri kaybına çevirirdi.

**Kırpma surrogate çiftini bölmüyor.** `metin[..512]` bir emojinin ortasında
kesebilir; geriye yarım surrogate kalır ve JSON yazıcısı onu U+FFFD ile
değiştirir — veri **sessizce** bozulur. Bir karakter erken kesiliyor.

**Yan karar: `payment.abandoned` anahtarları İngilizceye çevrildi.**
`tutar`/`yetiskin`/`cocuk`/`bebek`/`tutmaSuresiSaniye` →
`totalTry`/`adults`/`children`/`infants`/`holdSeconds`. Diğer bütün olaylar
İngilizce; iki ad kümesi kalıcı olurdu çünkü tablo temizlenemiyor. Üretim
verisi yokken düzeltildi.

**Kanıt:** sekiz olay türü canlı üretildi, payload anahtarları birebir korundu,
**düşürülen/kırpılan anahtar 0** — yani liste gerçekten yazılanla eşleşiyor.

İlgili: [[api-gorevler]] · [[api-desenler]] · [[api-durum]]

---

## 2026-08-25 — Mert beş bekleyen soruyu cevapladı (S-10…S-14)

Sorular ve gerekçeleri [[api-durum]] içindeki tabloda; burada yalnız **karar ve
neden**.

### S-10 → "kupon komisyonu aşabilir" — kural KALDIRILIYOR

Bugüne kadar hem `PricingService` hem `trg_coupon_within_commission` indirimi
komisyon tutarında kırpıyordu. Kaldırılıyor.

**Neden:** Kural bir *sızıntı* üretiyordu — aynı kuponun bir teknede geçip
diğerinde geçmemesi, çağırana o iki işletmenin komisyon oranını sıralatıyordu ve
uç kimliksiz. Mert kuralı kaldırmayı seçti; böylece kupon her teknede aynı
davranır, ayrım kalmaz, sızıntı kaynağı kurur.

**Bedeli açıkça yazılıyor:** garanti veritabanından uygulamaya iniyor. Tetikleyici
"hak ediş negatif olamaz"ı *dolaylı* olarak sağlıyordu; kalkınca bunu doğrudan
garanti eden bir kısıt gerekiyor → `A-26`.

### S-14 → kupon açığını kuponu OLUŞTURAN taraf karşılar

10.000 TL tur, %15 komisyon (1.500 TL), 2.000 TL kupon → 500 TL açık.
İşletmenin kuponuysa açık işletmeden, platformun kuponuysa platformdan düşer.
Ayrım `Coupon.PartnerId`: dolu ise işletme kuponu, boş ise platform kuponu.

**Neden:** Kimse başkasının kampanyasını ödemez. "Her zaman platform" platformu
işletmenin agresif kuponuna açık bırakırdı; "her zaman işletme" işletmeyi haberi
olmayan bir platform kampanyasından zarara sokardı. Kuponu kim yazdıysa bedelini
o üstlenir — hem adil hem defterde tek satırla ifade edilebilir.

### S-12 → müşteri iptalinde KADEMELİ iade

| Kalkışa kalan süre | İade |
|---|---|
| 48 saat ve üzeri | %100 |
| 24 – 48 saat | %50 |
| 24 saatten az | yok |

**Neden:** Tek oran ya işletmeyi son dakika boşluğuna açık bırakır ya müşteriyi
erken iptalde cezalandırır. Kademeli oran, iptalin işletmeye maliyeti zamanla
arttığı için maliyetle orantılı — koltuk 48 saat kala yeniden satılabilir,
6 saat kala satılamaz.

**⚠️ Cevaplanmamış yan soru:** kademe **komisyona da** uygulanıyor mu? %50
iadede platform kendi payının yarısını da geri veriyor mu? Sorulmadı, tahmin
EDİLMEYECEK → `A-27` bunu Mert'e sormadan kapanamaz.

### S-11 → rezervasyon ucu KİMLİKSİZ kalıyor

**Neden:** Misafir rezervasyonu şemada zaten karara bağlıydı; giriş zorunluluğu
o kararı bozardı ve satın alma hunisinde en pahalı adımı ekler. Koruma hız
sınırında kalıyor (IP / 15 dk / 10). ⚠️ Bu sınır `A-19` yapılmadan ters vekil
arkasında **çalışmaz** — bugünkü güvenlik, yarınki dağıtımın ön koşuluna bağlı.

### S-13 → iptalde onay linki YOK

**Neden:** Şemanın "kod + e-posta veya kod + telefon" kuralı Mert'in kararıydı
ve değişmiyor. Sıkılaştırma model içinde yapıldı (telefon tam eşleşme, başarısız
denemelerin loglanması, koda göre saatte 5 deneme). E-posta linki `G-04`'e
(e-posta sağlayıcısı) bağımlı olurdu; o seçilmeden söz vermek anlamsız.

---

## 2026-08-25 — A-26 denetimi: komisyon oranı zaten açıkta duruyormuş

`A-26` "kupon davranışından komisyon oranını çıkarsama" sızıntısını kapatmak
içindi. Denetim, kapatılmaya çalışılan şeyin **gereksiz** olduğunu gösterdi:

    curl -X POST /api/pricing/quote   →   "commissionRate": 15.0

Kimlik yok, kupon yok, çıkarım yok. Herkese açık bir `boatRentalTypeId` ile tek
bir istek, o işletmenin komisyon oranını **kesin sayı** olarak veriyordu.
Canlı doğrulandı, sonra düzeltildi.

**Sebep bir hata değil, bir TASARIM tercihiydi:** `Quote` iki iş birden
yapıyordu — hem fiyat hesabının sonucu, hem HTTP yanıtı. `[[api-desenler]]`
bunu bir erdem olarak yazıyordu ("hesabın çıktısı aynı zamanda rezervasyona
dondurulacak alanların tamamıdır, ikinci bir dönüşüm yok"). O gerekçe **iç
taraf için hâlâ doğru**; yanlış olan, aynı nesnenin dışarı da verilmesiydi.
İç ihtiyaç için eklenen her alan (`CommissionRate`, `ContractId`) sessizce
müşteriye gidiyordu.

**Karar:** `QuoteResponse` adında ayrı bir yanıt tipi. `Quote` iç nesne kalıyor.

**Neden ayrı tip, `[JsonIgnore]` değil:** `[JsonIgnore]` "unutulursa sızar"
davranışıdır — yeni alan eklendiğinde varsayılan olarak dışarı çıkar. Ayrı tip
"unutulursa görünmez" davranışıdır. Para ve ticari şart taşıyan bir nesnede
varsayılanın hangi yöne baktığı, tek tek alanların doğruluğundan daha önemli.

Üç testle sabitlendi: yasak alan adları, serileştirilmiş gövdede arama, ve
`QuoteResponse`'a **yeni alan eklenirse** patlayan bir liste. Sonuncusu sayıyı
sabitlemek için değil; ekleyen kişiyi durdurup "bu müşteriye gitmeli mi?"
sorusunu sordurmak için.

⚠️ **Aynı denetim iki şeyi daha yakaladı ve ikisi de düzeltildi:**

1. **Dondurulan değer, donduğu anda doğru olmak zorunda.** `CouponFundedBy`
   ile `Coupons.FundedBy` arasında hiçbir veritabanı bağı yoktu.
   `ReservationFactory` içindeki bir hata her rezervasyona `Platform` yazsa,
   kupon `Partner` olsa bile veritabanı kabul ederdi ve sonuç **sessiz**
   olurdu: iki tarafın da defteri denk görünür, yalnız yanlış cepten
   düşülmüştür. `trg_reservation_coupon_funder` eklendi — **yalnız INSERT**,
   çünkü sonradan ayrışmak dondurmanın ta kendisi.

2. **`AddCheckConstraint` üretim tablosunu kilitler.** EF düz
   `ALTER TABLE ... ADD CONSTRAINT` üretiyor; tüm satırlar taranırken
   ACCESS EXCLUSIVE kilidi duruyor ve `Reservations`'a ne okuma ne yazma
   giriyor. `NOT VALID` + ayrı `VALIDATE CONSTRAINT` desenine geçildi.
   **Neden:** kesinti penceresi satır sayısıyla orantılı büyür, yani bugün
   fark edilmeyip yarın büyür — ve o gün nedeni bu migration'a bağlanamaz.

**Denetimin bir bulgusu REDDEDİLDİ.** C# denetimi `KuponRetMesaji` içindeki
`_ =>` dalının artık ulaşılamaz olduğunu söyledi. Ölçüldü: yanlış. C# enum'ları
tanımlı üyelerle sınırlı değil (`(CouponRejection)99` geçerli bir değerdir) ve
dal kalkarsa derleyici CS8509 verir. Proje 0 uyarıyla derleniyor, dal duruyor.

**Bir bulgu düzeltilmedi, bilerek:** "kaldırılan tetikleyicinin yerine bir üst
sınır konmalı" — hangi sınır olacağı **iş kararı**, `S-15` olarak Mert'e
soruldu → [[api-durum]]

---

## 2026-08-25 — A-03 devredilmiş yönetim ve denetiminin altı bulgusu

İşletme sahibi kendi rollerini tanımlayıp çalışanlarını yönetiyor. Tasarım ve
üç duvarın gerekçesi [[api-desenler]]'de; burada **denetimin bulduğu ve
düzeltilen** şeyler.

### 1. Olay günlüğüne çağıranın yazdığı serbest metin giriyordu

`PartnerStaffException.Message` doğrudan `EventLogs`'a yazılıyordu ve
`YetkileriCozAsync` tanınmayan yetki anahtarlarını mesaja **olduğu gibi**
koyuyordu. `role.manage` yetkisi olan biri `permissions` dizisine ne yazarsa
temizlenemeyen tabloya kalıcı olarak düşüyordu.

**Kodun kendi yorumu bunun imkânsız olduğunu iddia ediyordu.** Yorum yanlıştı.

**Karar:** istisna iki metin taşıyor — `Message` çağırana (kendi yazdığını geri
görmesi sızıntı değil), `LogReason` günlüğe ve **sabit**.

**Neden ayrı alan, "mesajı temizle" değil:** temizleme her yeni ret dalında
tekrar hatırlanmak zorunda. Ayrı alan, unutan kişiyi derleyiciyle durduruyor.

### 2. E-posta varlık oracle'ı

`AddMemberAsync` üç ayrı cevap veriyordu: "kullanıcı yok", "başka işletmede",
"zaten çalışanın". İlk ikisi birleştirildi.

**Neden:** `staff.manage` işletme sahibinin güvendiği kişiye verilir ama
**platformun tamamına** değil. Ayrı cevaplar, rastgele e-posta deneyerek
platformdaki kimin kayıtlı olduğunu ve kimin bir işletmede çalıştığını
öğrenmeye yarıyordu. Üçüncü dal ayrı kaldı: kendi çalışanı olduğu bilgisi zaten
çalışan listesinde görünüyor.

Ek olarak iki hız sınırı kondu: `panel` (kullanıcı başına dakikada 120) ve
`personelEkle` (kullanıcı başına saatte 20). **Bölümleme IP'ye değil
KULLANICIYA göre** — bir işletmenin bütün çalışanları aynı ofis IP'sinden çıkar.

### 3. `IX_PartnerMembers_PartnerId` hiç yoktu

`PartnerConfigurations` iki kez `HasIndex(x => x.PartnerId)` çağırıyordu: biri
düz, biri `IsUnique` + `WHERE "IsOwner" = true`. **EF indeksleri property
kümesine göre anahtarlıyor**, ikincisi birincisini sessizce eziyordu. Üretilen
şemada düz indeks yoktu ve panelin en sık sorgusu seq scan yapıyordu.

Yorum satırı ("düz indeks şart") olmayan bir indeksi anlatıyordu — kod
doğruymuş gibi görünüyordu.

⚠️ **`HasDatabaseName` YETMİYOR** — o yalnız birleşmiş indeksin adını
değiştirir. İkinci indeks için ad `HasIndex`'e **parametre** olarak verilmeli:
`HasIndex(x => x.PartnerId, "IX_PartnerMembers_PartnerId")`.

### 4. Rol adı benzersizliği hiçbir kısıta bağlı değildi

`RoleNameExistsAsync` "önce bak sonra yaz". İki eşzamanlı istek aynı ismi
kontrol edip ikisi de "yok" cevabını alıp ikisi de yazabiliyordu. `Roles.Key`
benzersizliği yakalamıyor çünkü `Key` her zaman biricik üretiliyor.

`IX_Roles_PartnerName` eklendi ve **`Roles.Name` `citext`'e çevrildi**.

**Neden citext:** kısıt büyük/küçük harf duyarsız olmalı, çünkü uygulama
öyleydi. Düz `text` olsaydı uygulama "Personel" ile "personel"i aynı sayarken
veritabanı farklı sayardı — **aynı sessiz ayrışma deseni**, `A-22`'de kupon
sayımında bir kez yaşandı.

### 5. Rol yaratma atomik değildi

`Role.Id` veritabanında üretiliyor, yani yetkileri bağlamadan önce bir
gidiş-dönüş şart. İki `SaveChangesAsync` ayrı işlemdeydi: araya giren bir hata
geriye **yetkisiz bir rol** bırakırdı — panelde görünen, işe yaramayan, adı
kullanımda olduğu için aynı isimle yeniden yaratılamayan bir kayıt. İşleme
alındı.

### 6. `Role.Key` kesmesi rastgeleliğin çoğunu atıyordu

`$"partner.{partnerId:N}.{Guid.CreateVersion7():N}"[..64]` — tam uzunluk 73,
kolon `HasMaxLength(100)`. Kesmeye hiç gerek yoktu ve bedeli görünmezdi:
**uuid v7 zaman sıralı**, ilk 12 onaltılık karakteri milisaniye damgası. 64'e
kesmek kuyruktaki gerçek rastgeleliği kırpıyordu. Kesme kaldırıldı.

### Denetimin bir bulgusu değerlendirildi ve GEREK GÖRÜLMEDİ

`ReplaceRolePermissions`'ta eşzamanlı iki güncellemede "son yazan kazanır"
riski. Doğru ama projede hiçbir yerde eşzamanlılık jetonu (`xmin`/`RowVersion`)
yok; yalnız buraya koymak tutarsız olurdu. Not olarak duruyor.

### Testin biri HİÇBİR ŞEY ÖLÇMÜYORDU

`Assert.DoesNotContain("partner.owner", rol.Key[8..])` — `[8..]` tam olarak
`"partner."` önekini kesiyor, aranan metin de o önekle başlıyor. **Kurulum
gereği hep geçiyordu**; üretim kodu anahtara göre karar verse bile yeşil
kalırdı. Kurulum artık anahtarda "owner" geçirmiyor, doğrulama tüm anahtara
bakıyor.

**Ders:** bir doğrulamanın kırmızıya dönebildiğini görmeden yeşil olmasına
güvenmemek.

---

## 2026-08-25 — A-05 QR biniş ve denetiminin beş bulgusu

İki uç: `scan` (jetonla, kamera/klavye) ve `manual` (rezervasyon koduyla,
`G-12` seçenek c). Tasarım ve kurallar [[api-desenler]]'de; burada denetimin
bulduğu ve düzeltilenler.

### 1. Eşzamanlı okutma yarışı — İKİ denetim de bağımsız olarak buldu

Aynı jeton iki cihazda aynı anda okutulduğunda iki istek de satırı `Paid`
okuyup **ikisi de durum geçişi kaydı** yazıyordu, ve son yazan `BoardedAt`'i
belirliyordu. Oysa "ilk biniş anı" gerçek biniş anıdır: yorum hakkının doğması
ve mesajlaşmanın kapanması ona bağlı.

**Karar:** koşullu UPDATE — `WHERE "Status" = 'Paid'`, etkilenen satır sayısına
bakılıyor. 1 ise bu çağrı ilk binişi yaptı, 0 ise başkası önce davrandı.

**Neden `FOR UPDATE` değil:** denetim projedeki mevcut `FOR UPDATE` desenini
(`ReservationRepository`) önerdi. Koşullu UPDATE tercih edildi çünkü kilit
almıyor, kilit sırası sorusu doğurmuyor ve kararı tek bir SQL cümlesinde
veritabanına bırakıyor. `FOR UPDATE` burada aynı sonucu daha pahalıya verirdi.

**Neden eşzamanlılık jetonu (`xmin`) değil:** projede hiçbir yerde yok; yalnız
buraya koymak tutarsız olurdu ve zaten çakışma hatası fırlatmak istemiyoruz —
tekrar okutma **hata değil**, normal.

### 2. Testim yanlış sebeple geçiyormuş

Yarışı `Task.WhenAll` ile paralel iki okutma olarak yazmıştım. Koşullu
UPDATE'in koşulunu kaldırdığımda **test yine yeşil kaldı** — yani hiçbir şey
ölçmüyordu: veritabanı gidiş-dönüşleri hızlı olduğu için iki istek pratikte
sıralanıyor, ikincisi durumu zaten `Boarded` okuyup çakışmaya hiç girmiyordu.

Yerine çakışmanın tam anı **elle** kuruldu: iki bağlam da `Paid` görüyor, sonra
ikisi de işaretlemeye çalışıyor. Bu test koşul kalkınca `Expected 0, Actual 1`
ile kırmızıya dönüyor — ölçüldü.

Paralel test silinmedi, **kanıt olmaktan çıkarıldı**: servisin bütününün o karar
altında tutarlı kaldığını gösteren bir duman testi olarak duruyor ve yorumunda
tek başına kanıt olmadığı yazılı.

### 3. Başarılı yazma sonrası okuma hatası, başarıyı başarısız gösteriyordu

Yolcu listesi `SaveChangesAsync`'ten SONRA okunuyordu. O sorgu düşerse istisna
`BoardingException` olmadığı için 500'e dönüşüyordu: müşteri iskelede "biniş
başarısız" duyuyor, oysa veritabanında binmiş görünüyordu.

Sorgu yazılan hiçbir şeye bağlı değil (`Passengers` bu akışta değişmiyor), sıra
bedelsiz değiştirildi.

### 4. Denetim kaydının hatası, denetlenen hatanın yerine geçiyordu

`BasarisizYazAsync` reddi kaydedip sonra `BoardingException` fırlatıyordu.
Kayıt kendisi düşerse istisna **onun yerine** geçiyordu: okutan kişi anlamsız
bir 500 görüyor ve reddin sebebi hiçbir yere yazılmıyordu. Yani denetim izini
korumak için konan kayıt, denetim izini yok ediyordu.

Kodun üstündeki yorum "kaydın kendisi işlemi bozmamalı" diyordu — **yorum
yalan söylüyordu**. Artık try/catch ile kod haline getirildi.

### 5. `FailureReason` başarılı satırlarda dolu görünüyordu

Elle binişte okutan kişinin notu `FailureReason`'a yazılıyordu ve
`Succeeded = true` olan satırlarda "başarısızlık sebebi" adlı bir alan dolu
duruyordu. `BoardingScans`'i doğrudan sorgulayan biri kolonun adına bakıp
yanlış sonuca varırdı.

Ayrı `Note` kolonu eklendi. ⚠️ Geriye dönük veri taşınmadı; migration'da
taşıma sorgusu yorum olarak duruyor.

### Güvenlik denetiminde kritik bulgu ÇIKMADI

Jeton 256 bit, yalnız SHA-256 özeti saklanıyor, kapsam filtresi tek yerde ve
"jeton yok" ile "başka işletmenin" ayırt edilmiyor. Denetim ayrıca şunu
doğruladı: payload politikası süslü yorum değil, `EventLogger` içinde fiilen
uygulanan bir filtre — controller yanlışlıkla jeton eklese bile düşer.

⚠️ **Web tarafına devredilen bir not:** `DeviceInfo` ve `Note` istemciden gelen
serbest metin; sunucu yalnız uzunlukla kırpıyor. Panelde gösterilirken kaçış
(escaping) uygulanmazsa depolanan XSS potansiyeli var → `03-Web` tarafına
bildirilmeli.

---

## 2026-08-25 — A-21 kimlik dilimi: kodun iddia ettiği zincir yokmuş

34 olay türünden 9'u bağlanmamıştı. Altısı henüz yazılmamış uçlara ait; **üçünün
ucu vardı ama loglamıyordu** ve üçü de hesap güvenliğiyle ilgiliydi:
`auth.token.refreshed`, `auth.logout`, `account.email_change.requested`.

Bunları bağlarken daha ciddi bir şey çıktı.

### Kodun yorumu iki şey iddia ediyordu, ikisi de yanlıştı

> *"Aynı jeton ikinci kez kullanılırsa çalınmış demektir; zincir `ReplacedById`
> üzerinden izlenebiliyor."*

1. **`ReplacedById` hiçbir yerde atanmıyordu.** Kolon ve yabancı anahtar baştan
   beri vardı, yazan yoktu — her satırda `NULL`.
2. **Yeniden kullanım "jeton yok" ile aynı koda düşüyordu.** Döndürme (rotation)
   sayesinde her jeton bir kez kullanılabiliyor, yani ikinci kullanım
   hırsızlığın en güçlü sinyali — ve hiçbir iz bırakmıyordu.

**Karar:** `auth.token.reused` diye ayrı bir olay türü. Zincir kuruluyor.

**Neden:** Döndürme kullanan bir sistemde jetonun ikinci kez sunulması,
elde edilebilecek EN GÜÇLÜ hırsızlık sinyalidir — ve tek görünme yeri
günlüktür, çünkü reddedilen istek hiçbir satırı değiştirmiyor. "Süresi
dolmuş" ile aynı kovaya atmak, o sinyali kalıcı olarak yok ediyordu.
Zincir ise sinyalin işe yarar hâle gelmesi için şart: hangi oturumdan
türediği bilinmeden hangi jetonların iptal edileceği de bilinemez.

**Müşteriye dönen cevap DEĞİŞMEDİ** ("Oturum süresi dolmuş", 401). Ayrım yalnız
günlükte — aksi halde saldırgana jetonun gerçek olduğunu söylemiş olurduk.

### Yarış: tespit atlatılabiliyordu

Denetim yakaladı: aynı jetonla iki istek AYNI ANDA gelirse ikisi de satırı
`RevokedAt = NULL` okuyup ikisi de döndürmeyi tamamlayabiliyordu. Jetonu çalan
biri, gerçek kullanıcıyla aynı anda yenileyerek kendi zincirini **sessizce**
kurardı ve `auth.token.reused` hiç yazılmazdı.

**Karar:** koşullu UPDATE — `WHERE "RevokedAt" IS NULL`, etkilenen satır
sayısına bakılıyor. 0 ise yarışı kaybettik ve bu **tam olarak yeniden kullanım
durumudur**; kendi ürettiğimiz jeton iptal ediliyor ve olay yazılıyor.

Aynı desen `A-05`'te biniş için de kullanıldı → [[api-desenler]].

**Sıra ters çevrilemez:** önce yeni jeton yazılıyor, sonra eskisi bağlanıyor.
`ReplacedById` yabancı anahtar, var olmayan satıra işaret edemez. Ara pencerede
süreç ölürse "hiç kimseye verilmemiş" bir jeton kalır — zararsız, çünkü düz
metni yalnız o isteğin cevabında dönecekti ve cevap hiç dönmedi.

### Ara düzeltmede DÜZELTTİĞİM HATAYI YENİDEN YARATMIŞIM

İlk denemede zinciri iki ayrı `SaveChangesAsync` ile kuruyordum: yeni jeton
yazılıyor, sonra `ReplacedById` bağlanıyordu. C# denetimi şunu gösterdi: araya
bir hata girerse geriye **eski jeton iptal, yeni jeton geçerli, `ReplacedById`
NULL** kalıyordu — yani düzeltmeye çalıştığım durumun ta kendisi, dar bir
pencerede.

`RefreshToken.Id` artık **kodda** üretiliyor (`Guid.CreateVersion7()`), yani
kimlik önceden biliniyor ve ikinci kayda gerek kalmıyor. `uuidv7()` varsayılanı
tabloda duruyor; elle atılan `INSERT`'lerde hâlâ çalışıyor.

### Bilerek düzeltilmeyen: zamanlama yan kanalı

Denetim haklı olarak şunu buldu: yeniden kullanım dalında fazladan bir
`LogAsync` var ve `EventLogger` ayrı bir kapsam açıp veritabanına yazıyor — yani
o dal ölçülebilir biçimde daha yavaş. Aynı durum `logout`ta da var.

**Düzeltilmedi**, gerekçesi:
- İstismar için jetonu ELDE TUTMAK gerekiyor, ve sunmak jetonu yakıyor. Yani
  "sessiz prob" olarak kullanılamıyor.
- Ayırt ettiği şey iki ÖLÜ jeton durumu: "zaten döndürülmüş" ile "hiç yok".
- Eşitlemenin yolu başarısız denemeleri de loglamak olurdu; `refresh` ucu
  bilerek hız sınırsız (yüksek frekans) ve `EventLogs` **temizlenemiyor** —
  kimliksiz bir uçtan sınırsız satır yazmak daha büyük bir sorun.

⚠️ Bu bir kabul, çözüm değil. `S-17` cevaplandığında yeniden bakılmalı.

### Tespit var, EYLEM yok — `S-17`

Yeniden kullanım saptanıyor ama oturumlar kapatılmıyor. OWASP/OAuth önerisi tüm
zinciri iptal etmek; seçilmedi çünkü **yanlış pozitif riski gerçek**: kötü
bağlantıda istemcinin aynı isteği iki kez göndermesi meşru kullanıcıyı her
yerden atardı. UX/güvenlik dengesi, teknik karar değil → [[api-durum]]

---

## 2026-08-25 — G-04 bildirim sağlayıcıları ve denetiminin altı bulgusu

Mert seçti: e-posta **Postmark**, SMS **Netgsm**, yerel test **Mailpit**.
Sağlayıcı seçimi yapılandırmadan geliyor.

**Neden:** Postmark işlemsel postada teslimat kalitesi için — rezervasyon onayı
spam'e düşerse müşteri kodunu hiç görmez ve destek talebi olarak geri döner.
Netgsm ise Türkiye'ye özgü iki kısıt yüzünden: gönderici başlığı operatörden
önceden onaylı olmalı ve İYS kayıt zorunluluğu var; yurt dışı sağlayıcıları
eleyen şey bunlar. Verimor önerilmedi — eski sistemde canlıda IP whitelist
hatası veriyordu.

### Bağlarken çıkan asıl şey: kural yazılıydı, kod yoktu

`SendSmsAsync` kod tabanında **hiçbir yerden çağrılmıyordu** ve rezervasyon
onayı yalnız HTTP cevabında dönüyordu. Oysa domain kuralı net: *"Rezervasyon
tamamlanınca müşteriye hem e-posta hem SMS gider… Sonuç: telefon zorunlu
alan."* Telefonu zorunlu yapmışız ama hiç kullanmamışız.

### ⚠️ Bunu bağlamak YENİ BİR AÇIK AÇTI

`POST /api/reservations` kimliksiz ve `contactPhone` sahipliğini
doğrulamıyor. Gönderim bağlanmadan önce oraya üçüncü bir kişinin numarasını
yazmanın hiçbir etkisi yoktu. Bağlandığı an aynı alan şuna dönüştü:
**istediğin numaraya, bizim paramızla, ücretli SMS gönderten bir uç.**

**Karar:** hedef bazlı sınır (`INotificationThrottle`) — aynı e-posta ya da
telefona son bir saatte 5'ten fazla rezervasyon açılmışsa gönderim durur.

**Neden IP sınırı yetmiyor:** mevcut sınır IP başına ve vekil havuzuyla
aşılıyor. Aşılamayan tek şey KURBANIN NUMARASI.

**Neden e-posta ve telefon AYRI sayılıyor:** birlikte sayılsaydı saldırgan her
istekte e-postayı değiştirip aynı numaraya sınırsız SMS gönderirdi — çift her
seferinde yeni olurdu. Canlı doğrulandı: 8 rezervasyon, 8 farklı e-posta, aynı
telefon → 5 bildirim gitti, 3'ü durduruldu.

**Neden rezervasyon engellenmiyor:** meşru müşteri arka arkaya üç tur
alabilmeli ve kod HTTP cevabında zaten dönüyor. Sınır gönderime, işleme değil.

### Kendi kuralımı bir sınıf sonra çiğnemişim

`PostmarkEmailSender` alıcı adresini bilerek loglamıyor ve gerekçesini de
yazıyor. `SmtpEmailSender` ise aynı adresi `Information` seviyesinde
yazıyordu. Uygulama günlükleri `EventLogs` kadar korumalı değil.

### Geliştirmede GÖRÜNMEYEN bir tuzak

`CompositeNotificationSender` singleton'dı. `AddHttpClient` typed istemcileri
**transient** kaydediyor, yani singleton composite onları uygulamanın ömrü
boyunca içine hapsediyordu (captive dependency) ve `IHttpClientFactory`'nin
handler yenilemesi hiç çalışmıyordu.

**Neden fark edilmiyordu:** geliştirmede iki sağlayıcı da singleton (Mailpit +
günlük), yani singleton singleton'ı tüketiyordu ve hiçbir şey yanlış
görünmüyordu. Yalnız üretim yapılandırmasında ortaya çıkıyordu. Scoped'a
çekildi.

### İsteğin iptal jetonu gönderime bağlanmamalı

Gönderim `HttpContext.RequestAborted`'a bağlıydı: müşteri sayfayı kapatınca —
rezervasyon zaten oluşmuşken — gönderim yarıda kesiliyor ve kesilme gerçek
sağlayıcı hatasıyla aynı kulvarda `LogError`'lanıyordu. İki zarar birden:
müşteri kodunu almıyor, ve izlemede yanlış alarm.

`CancellationToken.None` kullanılıyor; aynı gerekçe `EventLogger`'da da yazılı.

### Ölçülen ama ÇÖZÜLMEYEN: cevap hâlâ gönderimi bekliyor

E-posta ve SMS artık paralel ve istemci zaman aşımı 5 sn'ye indirildi (en kötü
durum 30 sn'den ~5 sn'ye). Ama HTTP cevabı hâlâ sağlayıcının hızına bağlı ve
**yeniden deneme yok**. Asıl çözüm arka plan kuyruğu → `A-28`.

---

## 2026-08-26 — İade, iptalden AYRI bir iş

**Karar:** `ReservationService.CancelAsync` iade oranını hesaplayıp donduruyor ama
sağlayıcıya HİÇBİR ŞEY göndermiyor. Para hareketi ayrı bir uçtan geçiyor:
`POST /api/payments/refund` → `RefundService`.

**Neden:** İptalin içine gömülseydi, sağlayıcıya giden HTTP çağrısı müşterinin iptal
isteğini bekletirdi. Çağrı zaman aşımına uğradığında müşteri *"iptal başarısız"*
görürdü, oysa rezervasyon iptal edilmiş olurdu. Aynı tuzağın bildirim tarafındaki
hâli `A-28` olarak yaşandı ve giden kutusuyla çözüldü. Ayrılınca iade **tekrar
denenebilir** bir iş oluyor — sağlayıcı reddettiğinde iptal geri alınmıyor.

**Alternatifler:** İptalin içinde senkron iade — yukarıdaki sebeple elendi.
Giden kutusu deseniyle tam otomatik iade — `A-28` altyapısı var ama para hareketini
insan onayından geçirmemek ilk sürümde fazla iddialı bulundu; kayda alındı →
[[api-benim-kararlarim]]

---

## 2026-08-26 — `refund.manage`, `reservation.cancel`'dan ayrı yetki

**Karar:** İade talimatı göndermek için ayrı bir yetki (`refund.manage`,
`IsPartnerAssignable = false`). `platform.admin` rolüne migration'da elle bağlandı,
`platform.support` rolüne **bağlanmadı**.

**Neden:** İptal, tutarı hesaplayıp donduruyor; asıl para hareketi iadede oluyor.
Tek yetkide toplansaydı, müşteri iptalini yapabilen destek personeli aynı anda
platform kasasından para çıkarabilirdi. `IsPartnerAssignable = false` olması,
`trg_role_permission_assignable` tetikleyicisi sayesinde tekne sahibinin kendi
çalışanına bu yetkiyi vermesini **veritabanı seviyesinde** imkânsız kılıyor.

⚠️ **`A03_YetkiKatalogu`'ndaki `CROSS JOIN` sonradan eklenen yetkileri kapsamıyor.**
O migration `platform.admin`'e o gün var olan yetkileri bağladı; yeni yetki oraya
kendiliğinden girmiyor. Bağlama satırı unutulsaydı uç yazılır, derlenir, testten
geçer ve **hiç kimse çağıramazdı**.

---

## 2026-08-26 — Niyet, etkiden önce yazılır

**Karar:** `RefundService` sağlayıcıyı çağırmadan ÖNCE `Refunds` satırını yazıp
commit ediyor; sonra `Sent`'e alıp yine commit ediyor; ancak ondan sonra HTTP
çağrısı yapıyor.

**Neden:** Önce sağlayıcı çağrılıp sonra kayıt atılsaydı, arada düşen bir süreç
**parası gitmiş ama kaydı olmayan** bir iade bırakırdı — mutabakatta görünmez.
Tersi güvenli: kaydı olup gönderilmemiş iade görülebilir ve tekrar denenebilir.

`Requested` ile `Sent`'in ayrı olması da bu yüzden: süreç `Sent`'te düşerse
*"gönderilmiş olabilir, sağlayıcıdan teyit et"*, `Requested`'ta düşerse
*"kesinlikle gönderilmedi"* demektir. Ayrım olmasaydı operatör, parayı ikinci kez
göndermek ile müşteriyi bekletmek arasında **kanıtsız** seçim yapardı.

---

## 2026-08-26 — Çift iade kapısı veritabanında

**Karar:** `UX_Refunds_ReservationId_Aktif` — `Refunds("ReservationId")` üzerinde
kısmi benzersiz indeks, filtresi `"Status" <> 'Failed'`.

**Neden:** Servisteki durum kontrolü yarışta yetmiyor: eşzamanlı iki istek de
rezervasyonu `Cancelled` görür, ikisi de sağlayıcıya talimat gönderir ve **para iki
kez çıkar**. `Failed` satırların filtre dışında bırakılması zorunlu — aksi halde
başarısız bir iade o rezervasyonu sonsuza kadar kilitler, müşterinin parası bizde
kalır ve elle müdahale gerekirdi.

**Ölçüldü:** indeks migration'dan çıkarıldığında eşzamanlılık testi YEŞİL kalıyor
(iki görev pratikte sırayla koşuyor), yalnız doğrudan indeksi hedefleyen test
kırmızıya dönüyor → [[api-eszamanlilik-testi-yarismayabilir]]

---

## 2026-08-26 — Sandbox adresi üretimde açılmıyor

**Karar:** `Payments:Iyzico:BaseUrl` üretimde `sandbox` içeriyorsa uygulama
açılmıyor. Anahtarlar boşsa da açılmıyor.

**Neden:** Sahte sağlayıcı yasağının kılık değiştirmiş hâli. Sandbox gerçek kart
çekmez: uygulama sorunsuz çalışır, müşteri *"ödedim"* der, defter kaydı yazılır ve
**hiçbir para tahsil edilmez**. Sağlayıcı adı `iyzico` olduğu için mevcut
`fake` yasağı bunu yakalamazdı.

Anahtarlar `appsettings.json`'a YAZILMIYOR — `dotnet user-secrets` / ortam değişkeni.
`BaseUrl` sır olmadığı için `appsettings`'te: Development → sandbox, üretim → gerçek.

---

## 2026-08-26 — İyzico'da Checkout Form, doğrudan ödeme ucu DEĞİL

**Karar:** `/payment/iyzipos/checkoutform/initialize/auth/ecom` kullanılıyor.
Müşteri kart bilgisini İyzico'nun barındırdığı sayfaya giriyor; biz yalnız dönen
`paymentPageUrl`'e yönlendiriyoruz.

**Neden:** Alternatif olan `/payment/auth` ucu kart numarasını, son kullanma
tarihini ve CVC'yi **bizim sunucumuzdan geçirirdi** ve PCI DSS kapsamına
girerdik. `PaymentStartRequest` içinde kart alanı olmaması zaten bu tercihi
söylüyordu — arayüz baştan barındırılan sayfa için tasarlanmıştı.

`IyzicoTests.Kart_alani_istege_hic_girmiyor` bu tercihin sessizce değişmesini
engelliyor: istekte `cardNumber`, `paymentCard` veya `cvc` geçerse test kırmızı.

**Alternatifler:** `/payment/3dsecure/initialize` — HTML içeriği döndürüyor,
adres değil; arayüzümüzdeki `RedirectUrl` kavramına oturmuyordu, elendi.

---

## 2026-08-26 — Ödemede TUTAR da sağlayıcıdan teyit ediliyor

**Karar:** `IPaymentProvider.CompleteAsync` artık `expectedAmountTry` alıyor.
İyzico'nun döndürdüğü `price` beklenen tutara eşit değilse ödeme **başarısız**
sayılıyor.

**Neden:** "Ödendi mi" sorusunun cevabı tek başına yetmiyordu. Beklenenden düşük
bir tahsilat `Succeeded` sayılsaydı rezervasyon `Paid` olur ve defter **tahsil
edilmemiş parayı gerçek gösterirdi** — `A-18`'in tam olarak engellemeye
çalıştığı şey.

⚠️ `paidPrice` DEĞİL `price` karşılaştırılıyor: taksitli ödemede `paidPrice`
faizle birlikte daha yüksek oluyor. `paidPrice` karşılaştırılsaydı **her
taksitli ödeme reddedilirdi**.

---

## 2026-08-26 — İyzico'ya `ip` alanı gönderilmiyor, TCKN yer tutucu gidiyor

**Karar (ip):** İade isteğinde `ip` alanı yok. **Ölçüldü:** alansız iade
`success` dönüyor, yani zorunlu değil.

**Neden:** Elimizdeki tek IP iadeyi yapan personelinki olurdu, müşterininki
değil. Uydurma bir IP göndermek sahtekârlık skorlamasını kirletirdi.

**Karar (TCKN + adres):** `identityNumber` ve `registrationAddress` **zorunlu**
(ölçüldü: `errorCode 8` ve `5026`), biz ikisini de toplamıyoruz. Geçici olarak
yer tutucu gidiyor.

TCKN yer tutucusu `11111111111` **bilerek geçersiz**: son basamak TCKN doğrulama
kuralını tutmuyor, yani hiçbir gerçek kişiye ait olamaz. Rastgele geçerli bir
numara üretmek, var olan birinin kimlik numarasını gerçek bir ödemeye bağlamak
olurdu. Adres yer tutucusu da uydurma bir adres değil, ne olduğunu **söyleyen**
bir metin: `"Adres bilgisi alınmıyor"`.

**Mert'in kararı bekleniyor** → [[api-benim-kararlarim]]

---

## 2026-08-26 — Alıcı kimliği ayrı tabloda, sağlayıcı başına bir kayıt

**Karar:** `PartnerPayeeAccounts (PartnerId, Provider, ExternalKey, Status)`,
`UX_PartnerPayeeAccounts_PartnerProvider` benzersiz.

**Neden:** `Payments.Provider` kararının aynısı. İyzico'nun verdiği
`subMerchantKey` yalnız İyzico'da geçerli; `Partners` üzerinde tek kolon olsaydı
PayTR'ye geçildiği gün her ödeme **var olmayan bir alıcıya** bölüştürülmeye
çalışılır ve sessizce başarısız olurdu. Eski sağlayıcının satırı silinmiyor:
geçmiş ödemelerin iadesi ve mutabakatı hâlâ oradan geçiyor.

Sağlayıcı başına ikinci kayıt yasak — hangisine para gideceği belirsiz kalırdı.

---

## 2026-08-26 — Bölüştürme alanları sağlayıcıdan BAĞIMSIZ adlandırıldı

**Karar:** `PaymentStartRequest.PayeeKey` + `PayeeAmountTry`. `SubMerchantKey`
DEĞİL.

**Neden:** `IPaymentProvider`'ın ilk satırındaki uyarının aynısı — arayüz
İyzico'nun şekline göre yazılsaydı PayTR'de kırılırdı. "Alıcı" ve "alıcının
payı" bizim domain kavramlarımız; `subMerchantKey` İyzico'nun kelimesi ve
yalnız `IyzicoPaymentProvider` içinde geçiyor.

İyzico'da bu alanlar **sepet kalemine** yazılıyor, isteğin köküne değil: çok
kalemli bir sepette her kalem farklı satıcıya ait olabiliyor.

---

## 2026-08-26 — Hakediş formülü TEK YERDE

**Karar:** `EarningCalculator.PartnerEarning(Reservation)`. `LedgerService`'in
iki kopyası (ödeme ve iade) buraya bağlandı; ödeme akışı da aynı fonksiyonu
çağırıyor.

**Neden:** Sağlayıcıya "bu paranın şu kadarı işletmenin" derken kullanılan sayı
ile defterin yazdığı sayı **aynı olmak zorunda**. İki ayrı hesap bugün aynı
sonucu verirdi; komisyon ya da kupon kuralı değiştiği gün ayrışırdı — ve
ayrıştığında belirti "defter tutmuyor" değil, **işletmeye yanlış tutar
ödenmesi** olurdu.

Test hem defterle karşılaştırıyor hem elle yazılmış sayıyla: yalnız "defterle
aynı" demek, **ikisi birden yanlış olduğunda** yeşil kalırdı.

---

## 2026-08-26 — Alıcı kaydı yoksa ödeme yine de alınıyor

**Karar:** İşletmenin alıcı kaydı yoksa bölüştürme yapılmıyor, ödeme reddedilmiyor.

**Neden:** Reddetmek, alıcı kaydı henüz açılmamış **her** işletmenin satışını
durdururdu — bugün bu tüm işletmeler demek. Bedeli: para platformda kalıyor,
hakediş yalnız defterde duruyor, transfer elle yapılıyor.

⚠️ Bedelin **görünür** olması için bölüştürme bilgisi `Payments.RawResponse`
içine yazılıyor: `payeeKey` boşsa o ödemede bölüştürme olmamıştır. Görünmeseydi
"hangi ödemeler elle transfer bekliyor" sorusu cevapsız kalırdı.

Kalıcı olup olmayacağı Mert'in kararı → [[api-benim-kararlarim]]

---

## 2026-08-26 — IBAN biçimi veritabanında doğrulanıyor

**Karar:** `CK_Partners_Iban` — `"Iban" IS NULL OR "Iban" ~ '^TR[0-9]{24}$'`.

**Neden:** Yanlış biçimli bir IBAN uygulama katmanında sessizce geçseydi, hatayı
ancak ödeme sağlayıcısı alıcı kaydını reddettiğinde — yani **işletme parasını
beklerken** — görürdük.

Boşluklu yazım (`TR18 0006 …`) bilerek REDDEDİLİYOR: normalleştirme uygulama
katmanının işi ve veritabanı iki farklı biçimi eşit saymamalı, yoksa aynı hesap
iki ayrı değer olarak durur.

⚠️ Bu kısıt IBAN'ın **biçimini** doğruluyor, **var olduğunu** değil. Mod-97
sağlaması yapılmıyor: geçerli biçimde ama var olmayan bir IBAN hâlâ girilebilir.
Onu ancak sağlayıcı yakalar.

---

## 2026-08-26 — İşletme paneli, işletme `Active` değilse KAPALI

**Karar:** `PermissionAuthorizationHandler`, `partner_id` taşıyan her istekte
işletmenin `Status = Active` olduğunu **veritabanından** doğruluyor. Değilse
yetki reddediliyor (403).

**Neden:** Domain akışı hesabı 3. adımda (başvuru) açıyor ama panele erişimi
9. adıma (sözleşme onayı) kadar kapalı tutuyor. `Partner` kaydında da yazılıydı
— *"'Hesap var ama paneli yok' ara durumu `Status <> Active` demek"* — ama
**hiçbir yer uygulamıyordu.**

`A-42` yazılana kadar bu teorikti: sisteme işletme girmiyordu. Başvuru ucuyla
birlikte canlı bir açığa dönüştü — başvuran anında tekne ekleyip fiyat
girebiliyordu, yani platformun onaylamadığı bir işletme satışa hazırlanabilirdi.

Aynı boşluk `A-38`'i de kesiyordu: askıya alma yalnız `Status`'ü değiştiriyor,
jetonu iptal etmiyordu. Askıdaki işletme panelde çalışmaya devam ediyordu.

⚠️ **Kontrol jetondan DEĞİL veritabanından.** Jetona bir `partner_active`
talebi konsaydı, askıya alınan işletme jetonu dolana kadar (15 dk) çalışmaya
devam ederdi. Bedeli istek başına bir sorgu; askı için 15 dakikalık pencere
bırakmaktan ucuz.

Kanıt: aynı jetonla `ApplicationReceived` → 403, `Active` → 200,
`Suspended` → 403. Platform personeli (`partner_id` yok) etkilenmiyor.

⚠️ **Otomatik testi YOK** — test projesi HTTP barındırmıyor → `A-43`.

---

## 2026-08-26 — IBAN iki katmanda doğrulanıyor

**Karar:** Veritabanı `CK_Partners_Iban` ile BİÇİMİ (`TR` + 24 rakam),
uygulama `IbanNormalizer` ile MOD-97 SAĞLAMASINI denetliyor.

**Neden:** İkisi farklı hatayı yakalıyor. Biçim kısıtı, uygulama atlansa bile
tabloya bozuk veri girmesini engelliyor. Mod-97 ise **tipoyu** yakalıyor:
biçimi kusursuz ama bir hanesi yanlış yazılmış bir IBAN kısıttan geçer ve onu
ancak sağlayıcı alıcı kaydını reddettiğinde — yani işletme parasını beklerken —
görürdük.

Ölçüldü: `TR180006200119000006672316` (son hanesi bozuk) biçim kısıtından
GEÇİYOR, mod-97'den geçmiyor.

⚠️ Mod-97 IBAN'ın **var olduğunu** kanıtlamıyor, yalnız yazım hatasız
olduğunu. Var olmayan ama sağlaması tutan bir IBAN'ı ancak banka yakalar.

---

## 2026-08-26 — Onay metninin sürümü SUNUCUDA sabit

**Karar:** `ConsentRecord.DocumentVersion` sunucudaki bir sabitten geliyor
(`OnayMetniSurumu`), istekten değil.

**Neden:** İstemciden alınsaydı, kullanıcının hangi metni onayladığını istemci
belirlerdi ve KVKK ispatı değersizleşirdi — anlaşmazlıkta elde tutulacak tek
kanıt bu kayıt.

⚠️ Geçici: metinler bir tabloda sürümlenmiyor. Sürüm elle güncellenmesi gereken
bir sabit ve güncellenmezse yeni metin eski sürümle kaydedilir →
[[api-benim-kararlarim]]

---

## 2026-08-26 — Test sunucusunda zamanlanmış işler ve hız sınırı kapalı

**Karar:** İki yapılandırma anahtarı — `ScheduledJobs:Enabled` ve
`RateLimiting:Enabled`, ikisi de varsayılan **açık**, yalnız `ApiFixture`
kapatıyor.

**Neden (işler):** Test barındırıcısında çalışsalardı TCMB kur işi gerçek bir
dış isteğe çıkardı ve diğer işler **başka testlerin satırlarını** değiştirirdi.
İş global çalışıyor, testin kurduğu veriyle sınırlı değil — bu tuzak vault'ta
iki kez kayıtlı (giden kutusu ve yorum daveti testleri).

**Neden (hız sınırı):** Kovalar `RemoteIpAddress`'e göre bölünüyor ve test
sunucusunda o adres **boş**: bütün testler tek kovayı paylaşıyor (15 dk / 10).
Ölçüldüğünde paket zaten 7 istekteydi; iki HTTP testi daha eklenince `429` ile
kırılacaktı — ve o kırılma **gerçek bir hata gibi okunurdu**.

**Varsayılan neden açık:** Kapatmayı unutan bir ortam korumasını kaybetmez;
açmayı unutan bir ortam sessizce kaybederdi.

⚠️ **Her iki anahtar da ÜRETİMDE kapatılamıyor** — `Program.cs` açılışta
reddediyor. Bu, sahte ödeme sağlayıcısı ve sandbox adresi yasaklarıyla aynı
desen: yanlış yapılandırma uygulamayı açtırmamalı, çünkü açılırsa hiçbir hata
vermez ve yalnız hiçbir şey OLMAZ.

**Her iki anahtar da İKİ YÖNDE test edildi.** Yalnız "kapalıyken kapalı"
denetlenseydi, varsayılanın yanlışlıkla `false` olması hiçbir şeyi kırmazdı.

---

## 2026-08-26 — Testte jeton elle üretilmiyor, giriş ucundan alınıyor

**Karar:** `ApiFixture.LoginAsync` gerçek `POST /api/auth/login` çağırıyor.

**Neden:** Elle üretilen bir jeton, jeton üretiminin kendisi bozulduğunda
testleri yeşil bırakırdı — talep adları değişse, imza yanlış hesaplansa ya da
yetkiler jetona hiç konmasa test bunu göremezdi. Kurulum yolu ile üretim yolu
ayrışmamalı; aynı sebeple `ApiTestData.ApplyAsync` da işletmeyi doğrudan
`DbContext`'e yazmak yerine **başvuru ucundan** açıyor.

---

## 2026-08-26 — Testler tek kullanımlık konteynerde (`A-20`)

**Karar:** `PostgresFixture` yerel sunucu yerine `postgres:18.6-alpine`
konteyneri açıyor. `DC_TEST_PASSWORD` ortam değişkeni kaldırıldı.

**Neden:** Önceki hâli iki bedel taşıyordu — testler makinede kurulu bir
PostgreSQL istiyordu ve **CI'da hiç koşamazdı**. Bu, `A-20`'nin varlık
sebebiydi ve bağımlılık başlangıçta ters yazılmıştı: Testcontainers CI'ı
beklemiyordu, CI'ın çalışabilmesi için Testcontainers gerekiyordu.

⚠️ **İmaj etiketi SABİT, `latest` değil.** Şema `EXCLUDE USING gist`,
`citext`, bölümleme ve `uuidv7()` kullanıyor; `latest` sessizce değişirse
testler makineden makineye farklı davranır ve sebebi görünmez. Sürüm
geliştirme sunucusuyla aynı: 18.6. İki test bu sabitlemeyi denetliyor —
kural yazılı olmakla kalmıyor, ölçülüyor.

⚠️ **Konteyner kullanıcısı süper kullanıcı olmak zorunda:** `A-10`
migration'ı `dailycruising_app` rolünü yaratıyor ve bu `CREATEROLE` istiyor.
Resmî imajın `postgres` kullanıcısı süper kullanıcı — ölçüldü, varsayılmadı.

**Bedel:** paket süresi 8 sn'den 11–15 sn'ye çıktı. Karşılığı, testlerin
herhangi bir makinede ve CI'da kurulumsuz koşabilmesi.

Bu karar 2026-08-26 sabahki "Docker Hub erişilemiyor, geri alındı" kaydını
İPTAL EDER — engel aynı gün öğleden sonra yeniden ölçüldüğünde kalkmıştı.

---

## 2026-08-26 — Otomatik iade: sorgu, servisin ön koşullarını aynen yansıtıyor

**Karar:** `ProcessRefundsJob`'un aday sorgusu `RefundService`'in reddettiği
her durumu **baştan dışarıda bırakıyor**: ödemesi olmayan, iade tutarı sıfır
olan, aktif iadesi bulunan, denemeleri tükenmiş ve son denemesi bir saatten
yeni olan rezervasyonlar.

**Neden — ve bu bir üslup tercihi değil:** Servis, ön koşulu tutmayan bir
rezervasyonda **istisna atıyor ve `Refunds` satırı YAZILMADAN dönüyor**. Satır
yazılmadığı için deneme sayacı ilerlemiyor. Sorgu o kayıtları dışarıda
bırakmasaydı iş onları her 15 dakikada bir tekrar dener, her seferinde patlar
ve sayaç hiç ilerlemezdi — **sonsuz döngü**.

⚠️ **Bu koruma başlangıçta ÖLÇÜLEMİYORDU.** Test yalnız `Refunds` satır
sayısına bakıyordu; kayıt seçilse bile satır yazılmadığı için ödeme koşulunu
sorgudan söktüğümde test **yeşil kaldı**. Uyarı günlüğünü yakalayan bir
günlükçü eklenince mutasyon kırmızıya gitti. Ders: **yan etkisi olmayan bir
hatanın tek izi günlüktür; ölçüm oraya bakmalı.**

⚠️ **Deneme sayacı ayrı bir kolon değil.** Her başarısız deneme geriye bir
`Failed` satırı bırakıyor ve kısmi benzersiz indeks yalnız `Failed` olmayanı
tekilleştiriyor — yani satır sayısı **deneme sayısının kendisi**. Ayrı bir
sayaç ikinci bir gerçek kaynağı olurdu ve ikisi ayrışabilirdi.

⚠️ **Denemeler tükendiğinde `payment.refund.abandoned` yazılıyor.** Bu olmadan
iş, beşinci denemeden sonra rezervasyonu sorgudan düşürür ve bir daha hiç
bakmazdı: müşteri parasını bekler, sistem "iptal edildi" der ve hiçbir yerde
"bu iade yapılamadı" yazmazdı. **Sessiz bırakma, başarısızlığın kendisinden
pahalı.**

---

## 2026-08-26 — Güvenlik damgası: yetki değişince jeton ANINDA geçersiz

**Karar:** `Users.SecurityStamp`; jetona `sstamp` talebi olarak gömülüyor ve
`OnTokenValidated` içinde veritabanındakiyle karşılaştırılıyor. Uyuşmazsa `401`.

**Neden:** Yetkiler erişim jetonuna gömülü ve jeton 15 dakika yaşıyor. Devir,
rol değişimi ve üyelik pasifleştirmesinde veritabanı doğru oluyordu ama ELDEKİ
JETON donmuş kalıyordu. Canlı ölçüm: devirden sonra eski sahip `staff.manage`
gerektiren uca **403 değil 400** aldı — yetki süzgecinden geçmişti.

⚠️ **BU KARAR, 2026-08-25'teki "erişim anında kesilmiyor, kabul edilmiş denge"
kaydını İPTAL EDER.** O gün gerekçe şuydu: *"anında kesmek her istekte
veritabanına gitmeyi gerektirir; bu ölçekte ödenmeyecek bir bedel."* Gerekçe
`A-43`'te geçersizleşti — işletme aktiflik kapısı eklenirken istek başına okuma
zaten başlamıştı. Damga o okumaya bir kolon ekliyor.

⚠️ **Doğrulama `OnTokenValidated`'da, `[HasPermission]` işleyicisinde DEĞİL.**
İşleyici yalnız yetki isteyen uçlarda çalışıyor; düz `[Authorize]` olan uçlar
(konuşmalar, destek, hesap) kapsam dışında kalırdı.

⚠️ **`401` — `403` değil.** "Kim olduğunu biliyorum, iznin yok" değil, "bu
jeton artık geçerli değil" diyoruz; istemci yenileme akışına girmeli. İşletme
aktiflik kapısı (`A-42`) ise `403` veriyor ve bu ayrım bilerek korunuyor.

**Bedel dürüstçe:** `[HasPermission]` uçlarında sorgu sayısı değişmedi
(`A-43`'ün sorgusu buraya taşındı), ama düz `[Authorize]` uçlarında istek
başına bir okuma eklendi — eskiden hiç yoktu.

⚠️ **Dağıtımda tüm açık oturumlar bir kez düşecek**: dağıtımdan önce üretilmiş
jetonlarda `sstamp` talebi HİÇ YOK ve doğrulama onları reddediyor. Alternatif
("talep yoksa geçir") korumayı ilk günden delik bırakırdı.

⚠️ **Yükseltmeyi unutulan bir yol, korumayı O YOLDA sessizce kaldırır.** Bugün
dört nokta var: rol yetkisi değişimi (o role bağlı herkes), üye rolü değişimi,
üye pasife alma, sahiplik devri (iki taraf). Yeni bir yetki değiştiren yol
eklenirse buraya da eklenmeli.

---

## 2026-08-26 — Yeniden başvuru: e-posta VE parola, ve hepsi aynı cevap

**Karar:** Reddedilmiş bir işletmeye yeniden başvuru yalnız şu üçü birden
tutarsa kabul ediliyor: kayıt `Rejected`, başvuru e-postası kaydın SAHİBİNİN
e-postasıyla aynı, ve parola doğru.

**Neden — ve bu teorik bir risk değil:** Vergi numarası yarı-kamusal bir bilgi
(fatura, web sitesi, ticaret sicili). Yalnız ona bakan bir kural, numarayı
bilen herkese reddedilmiş bir kaydı **kendi hesabına açtırma** imkânı verirdi:
saldırgan kendi e-postasıyla başvurur, kayıt onun olur, platform onaylarsa
başka birinin işletme kimliğiyle satış yapmaya başlar.

⚠️ **Üç başarısızlık da AYNI cevabı veriyor** (`TaxNumberTaken`): kayıt yok,
e-posta tutmuyor, parola yanlış. Ayrışsalardı bu uç, **hangi vergi
numarasının reddedilmiş bir kayda ait olduğunu ele veren bir sorgulama aracına**
dönerdi. Aynı ilke rezervasyon iptalinde de uygulanmıştı: *"kod yok"* ile
*"kod var ama kimlik tutmuyor"* aynı cevabı veriyor.

⚠️ **`RejectionReason` yeniden başvuruda TEMİZLENİYOR.** Kalsaydı, incelemeyi
bekleyen bir başvuruda panelde eski red sebebi görünürdü — askı sebebinin
`ReinstateAsync`'te temizlenmesiyle aynı gerekçe (kolon adı içeriğiyle
uyuşmalı). Sebep yine de kaybolmuyor: reddi yazan olay `EventLogs`'ta ve o
tablo append-only.

⚠️ **Aktif işletme REDDEDİLEMEZ.** Durdurmanın yolu askıya almak. Ayrılmasaydı
"reddedilmiş" bir işletmenin satılmış turları olur ve `RejectionReason`
başvuruyla ilgisiz bir metin taşırdı.

⚠️ **Yeniden başvuru YENİ onay kaydı yazıyor.** Eski `ConsentRecord`'lar
önceki başvuruya ait ve o başvuru reddedildi; eskisine yaslanmak kullanıcının
BUGÜN onayladığını ispatlamazdı.

---

## 2026-08-26 — İyimser eşzamanlılık: proje geneli, beş tablo hariç

**Karar:** `xmin` jetonu `OnModelCreating` içinde DÖNGÜYLE tüm entity'lere
uygulanıyor; beşi hariç: `Voyages`, `Boats`, `Coupons`, `LedgerEntries`,
`EventLogs`.

**Neden döngü:** Tek tek eklenseydi yeni bir entity eklendiğinde koruma
unutulurdu. Döngü, korumanın **kendiliğinden gelmesi** demek.

**Neden bu beşi hariç — ve bu tercih değil, zorunluluk:**

İlk dördünün satırlarını veritabanı **tetikleyicileri** güncelliyor
(`sync_voyage_sold_seats`, `sync_boat_rating`, `sync_coupon_used_count`,
`release_ledger_on_failed_payout`). Tetikleyici çalıştığı anda satırın `xmin`'i
değişiyor ama bağlamda takip edilen kopya eski değeri taşımaya devam ediyor;
o kopyayla yapılan `SaveChanges` çakışma istisnasıyla düşüyor. **Ölçüldü: 39
test kırıldı**, hepsi iptal akışında — sebep yarış değil, kendi
tetikleyicimizin kendi işlemimizi çarpması.

`EventLogs` bölümlenmiş ve append-only: jetonun değeri sıfır
(`forbid_mutation` `UPDATE`'i zaten reddediyor) ama bölümlenmiş tabloya
`INSERT`'te EF `xmin`'i geri okuyamıyor — **9 test kırıldı.**

⚠️ **BU BİR KORUMA BOŞLUĞU VE GİZLENMİYOR.** Bu beş tabloda kayıp güncelleme
hâlâ mümkün. Boşluk `Tetikleyici_yazan_tablolarda_jeton_yok` testiyle
SABİTLENDİ: birileri "her yerde koruma var" sanmasın, ve kapatılmaya
çalışılırsa test kırmızıya dönüp kararı bilinçli hale getirsin.

⚠️ **`ExecuteUpdate` / `ExecuteDelete` de kapsam dışı** — değişiklik
izleyicisinden geçmiyorlar, `WHERE xmin = ...` üretmiyorlar. Projede yarış
güvenliği gereken yerler zaten koşullu UPDATE + etkilenen satır sayısı
deseniyle yazılı; oradaki güvence kısıtlardan geliyor.

**İki teknik tuzak, ikisi de ölçülerek bulundu:**

1. **Migration gövdesi BOŞ olmalı.** `xmin` PostgreSQL sistem kolonu; EF onu
   yeni kolon sanıp 75 `AddColumn` üretti. Çalıştırılsaydı ilk tabloda
   *"column name xmin conflicts with a system column name"* ile reddedilirdi.
2. **`FromSql` ile yazılan ham sorguda `SELECT *` YETMİYOR.** Sistem kolonları
   `*` ile gelmiyor; EF ham sorguyu alt sorgu yapıp `d.xmin` isteyince
   `42703: column d.xmin does not exist` çıkıyor. **132 test birden** bu
   yüzden kırılmıştı; `SELECT *, xmin` ile çözüldü.

**Çakışma API'de `409`**, `500` değil: bu düzenli oluşacak bir durum ve
istemcinin doğru eylemi (yeniden okuyup denemek) ancak böyle anlaşılır.
`500` dönseydi günlükler gerçek hatalarla dolardı.

---

## 2026-08-26 — Tekne adresi: geçmiş ve dil tek tabloda

**Karar:** `BoatSlugs (BoatId, LanguageCode, Slug, IsCanonical)`. Ad değişince
yeni slug yürürlüğe geçiyor, eskisi geçmişe düşüyor ve `301` ile yenisine
yönlendiriyor.

**Neden tek tablo:** İki karar aynı yapıyı istiyordu — eski adreslerin
yönlendirilmesi (soru 4) ve dile göre ayrı slug ([[domain-gereksinimler]]
2026-08-24, Mert: *"kesinlikle yapacağız"*). Ayrı ayrı yapılsaydı tablo iki
kez tasarlanır ve ikincisi birincisini bozardı.

⚠️ **`302` değil `301`.** Geçici yönlendirme SEO değerini taşımaz ve arama
motoru eski adresi indekste tutmaya devam eder. Adres değişimi kalıcı bir
karar; cevabı da kalıcı olmalı.

⚠️ **Yönlendirme kontrolü içerikten ÖNCE.** Eski adresle gelen isteğe önce
içerik verip sonra yönlendirmek, aynı içeriğin iki adreste yayınlanması
(yinelenen içerik) demekti.

⚠️ Slug yalnız ad GERÇEKTEN değiştiğinde dönüyor. Her güncellemede dönseydi
kapasiteyi düzelten bir işletme farkında olmadan adresini değiştirir ve eski
bağlantılar gereksiz yere yönlendirmeye düşerdi.

⚠️ `Boats.Slug` kaldı ve yürürlükteki adresin kopyasını taşıyor. İki yerde
tutmak ayrışma riski; ad güncellemesi ikisini de aynı akışta yazıyor.
Kaldırmak `Slug`'ı okuyan her sorguyu değiştirmek olurdu.

---

## 2026-08-26 — Dosya depolama S3, resimler WebP + üç boyut

**Karar (Mert):** Dosyalar **S3**'te. **Karar (benim, onaya açık):** kabul
edilen format kullanıcıya bırakılıyor (JPG/PNG/HEIC), **saklanan ve sunulan
format tek: WebP**, ve her görselden **üç genişlik** üretiliyor
(400 / 800 / 1600).

**Neden WebP:** Aynı görsel kalitede JPEG'den ~%25-35 küçük. PNG fotoğrafta
kayıpsız olduğu için 5-10 kat büyüyor — PNG yalnız logo/ikon için. AVIF daha
da küçük ama kodlaması yavaş ve WebP'ye göre kazanç marjinal; sonraki sürüm.

⚠️ **Asıl kazanç formattan değil BOYUTTAN geliyor.** 4000 piksellik bir
fotoğrafı 400 piksellik kutuda göstermek, kullanıcıya gereksiz megabaytlar
indirtiyor. "Geç yükleme" şikayetinin en büyük tek sebebi bu.

⚠️ **Anahtar İÇERİK ÖZETİNDEN türüyor.** Sonucu: adres, içerik değişmedikçe
değişmiyor; değiştiğinde de içerik kesinlikle değişmiş oluyor. Bu, CDN'e
`max-age=31536000, immutable` verilebilmesinin şartı. Rastgele anahtar
üretilseydi her yükleme yeni bir adres yaratır, önbellek hiç ısınmaz ve aynı
resim defalarca depolanırdı.

**Zincirin kalan iki halkası bizde değil:** CDN (altyapı, `G-07`) ve
`srcset` + `loading="lazy"` (frontend). Backend üçünden ikisini yapıyor.

⚠️ **SkiaSharp seçildi, ImageSharp DEĞİL — ve bu bir lisans kararı.**
ImageSharp'ın "Six Labors Split License"ı belirli gelir eşiğinin üzerindeki
ticari kullanımı **ücretli** kılıyor. DailyCruising ticari bir platform;
sessizce ücretli bir lisansa bağlanmak, fark edildiğinde geri alması pahalı
bir borç olurdu. SkiaSharp MIT ve WebP kodluyor. **Mert bilmeli.**

⚠️ **Uygulama S3'e değil S3 API'sine bağlı.** `ServiceUrl` verilerek MinIO,
Cloudflare R2 ya da DigitalOcean Spaces kullanılabiliyor — ve testler tam
olarak bunu yapıyor: **gerçek bir MinIO konteynerine karşı** koşuyorlar.
Sahte bir `IAmazonS3` ile yazılsaydı imzalama, başlıklar ve anahtar biçimi
hiç sınanmaz, "çalışıyor" sanılan kod ilk gerçek yüklemede patlardı — `A-20`
gerekçesinin aynısı.

**İki tuzak ölçülerek bulundu:**
1. `PutObjectAsync` girdi akışını **kapatıyor**; boyut yüklemeden ÖNCE
   okunmalı, yoksa `ObjectDisposedException`.
2. `DisablePayloadSigning` **yalnız HTTPS'te** çalışıyor. HTTP bir uç
   noktada açık bırakılırsa her yükleme düşer.

---

## 2026-08-26 — `A-41` beklerken süreç akar tutuluyor

**Karar (Mert):** *"Şu anki süreçte bu çalışıyormuş gibi olsun."*

**Neden:** İyzico hesabında pazaryeri özelliği kapalı ve bu bir HESAP
ayarı — kodla çözülemiyor, Mert'in İyzico ile görüşmesini bekliyor. O süre
boyunca alıcı kaydı akışını hiç yazmamak, özellik açıldığında sıfırdan
başlamak demekti; akışı yazıp yalnız sağlayıcı gövdesini boş bırakmak
bekleme süresini kayıp olmaktan çıkarıyor.

`IPaymentProvider.RegisterPayeeAsync` eklendi. Sahte sağlayıcı gerçek bir
anahtar üretiyor; bölüştürme akışı uçtan uca çalışıyor ve geliştirme
durmuyor. İyzico sağlayıcısı çağrıldığında **engeli açıkça söylüyor** —
sessizce başarılı dönmüyor.

⚠️ **"Çalışıyormuş gibi" ile "çalışıyor sanmak" arasındaki fark korundu:**
sahte sağlayıcı zaten üretimde açılmıyor, ve `Payments.RawResponse` içinde
`payeeKey` boşsa bölüştürme olmadığı görülüyor.

🔔 **HATIRLATMA MEKANİZMASI:** uygulama her açılışta, hiçbir işletmenin alıcı
kaydı yoksa `A-41 BEKLİYOR` uyarısı yazıyor. Bu bir kod eksiği değil hesap
ayarı olduğu için hiçbir test kırmızıya dönmez ve sessizce unutulabilirdi.

Uyarı **kendiliğinden susuyor**: kayıt açıldığında çıkmıyor. Elle
kaldırılması gereken, unutulduğunda gürültüye dönüşecek bir şey bırakmıyor.
Ölçüldü: kayıt varken 0, yokken 1.

---

## 2026-08-27 — Dosya beyanı doğrulanıyor, anahtar dışarı verilmiyor

**Karar:** Yüklenen her dosyanın **ilk baytlarına** bakılıp beyan edilen
`Content-Type` ile uyuştuğu doğrulanıyor. Depolama anahtarı (`FileKey`)
hiçbir cevapta dönmüyor; indirme ayrı ve yetkili uçlardan geçiyor.

**Neden (imza):** `A-60`'ta yalnız izin listesi vardı ve bu eksikti. Liste
*"hangi türü kabul ediyoruz"* sorusunu cevaplıyordu, *"gelen şey gerçekten o
mu"* sorusunu değil. `Content-Type` **istemcinin yazdığı bir metin**: `.pdf`
diye gönderilen bir dosya bir betik, HTML ya da çalıştırılabilir olabilir.

⚠️ **Tanınmayan tür REDDEDİLİYOR.** `true` dönseydi, izin listesine yeni bir
tür eklendiği an imza doğrulaması o tür için **sessizce devre dışı** kalırdı —
korumanın en sinsi kaybolma biçimi.

⚠️ **Bu bir virüs taraması değil.** Amaç beyanla içeriğin uyuşmasını
zorlamak; kötü niyetli ama geçerli bir PDF yine geçer. Depolamanın
çalıştırılabilir olmaması ve kovanın genel okumaya kapalı olması ayrı
katmanlar ve ikincisi **kodla garanti edilemiyor** — altyapı ayarı.

**Neden (anahtar gizli):** Anahtar depolama adresinin parçası. Cevapta
dönseydi doğrudan erişim denemesine davetiye olurdu ve kova ayarı yanlışsa
bütün evraklar açılırdı. İki katman birbirini yedekliyor.

⚠️ **İndirme `attachment`, `inline` DEĞİL:** tarayıcı dosyayı göstermek
yerine indiriyor. Gömülü betik taşıyan bir PDF ya da SVG böyle çalışmıyor.

⚠️ **Platform indirmesinde erişim ÖNCE yazılıyor, dosya SONRA veriliyor.**
Ters sırada, yarıda kesilen bir indirme hiç kaydedilmezdi — oysa bakılmış
olurdu. `A-38`'in "muafiyetin bedeli okumada da ödenir" kuralının devamı.

⚠️ **Akış başa sarılıyor.** İmza için okunan baytlar geri verilmeseydi
yükleme, eksik bir akışla devam eder ve dosya **bozuk yazılırdı**.

---

## 2026-08-27 — API arayüzü: Scalar, Swagger değil

**Karar (Mert):** Tarayıcıdan tıklanabilir bir API arayüzü. **Scalar** seçildi.

**Neden Swagger/Swashbuckle değil:** Belgeyi zaten .NET 10'un yerleşik
`Microsoft.AspNetCore.OpenApi`'si üretiyor. Swashbuckle'a dönmek, aynı işi
yapan ikinci bir üretici, ek bağımlılık ve ek bakım demekti. Scalar yalnız
GÖRÜNTÜLEYİCİ: mevcut belgeyi okuyor, üretimine karışmıyor.

**Lisans doğrulandı:** MIT — paketin kendi `nuspec`'inden okundu, tahmin
edilmedi. ImageSharp'ta bu adım atlansaydı ücretli bir lisansa bağlanmış
olacaktık; aynı kontrolü burada da yaptım.

⚠️ **`AddOpenApi()` GÜVENLİK ŞEMASINI KENDİLİĞİNDEN EKLEMİYOR.**
`BearerSecurityTransformer` yazmak zorunlu oldu. Onsuz Scalar'ın jeton alanı
hiç çıkmaz, uçların çoğu yetki istediği için her istek 401 döner ve arayüz
**sessizce işe yaramaz** olurdu — hiç arayüz olmamasından kötü bir durum.

⚠️ **Şema belgeye ekleniyor, uçlara ZORUNLU işaretlenmiyor.** Kimliksiz uçlar
(arama, tekne detayı, rezervasyon, ödeme) gerçekten kimliksiz; hepsine "jeton
gerekli" damgası vurmak belgeyi yalancı yapar ve frontend gereksiz yere jeton
beklerdi.

⚠️ **İKİ KATMAN, çünkü ortam değişkenine güvenilmiyor.** `IsDevelopment()`
koşulu tek başına yeterli değil: yanlış ayarlanmış bir sunucu kendini
Development sanabilir. `ApiReference:Enabled` üretimde açıksa uygulama HİÇ
AÇILMIYOR. Üretime sızan bir arayüz, yetki isteyen 85 işlemin **tam
haritasını** herkese verir — saldırgana keşif işini hazır sunmak olurdu.

⚠️ `Microsoft.OpenApi` v2.7.5'te tipler kök ad alanına taşındı;
`Microsoft.OpenApi.Models` her yerdeki örneklerde geçtiği için kolayca yanlış
yazılıyor. Assembly'den doğrulandı.

## 2026-08-27 — Test kodu İngilizce isimlendirme, yorumlar Türkçe

**Karar (Mert):** Test projesindeki **isimlendirmeler** İngilizce.
`FiyatTests` → `PricingTests`, `FiyatEkleAsync` → `SeedPriceAsync`,
`Kisi_basi_fiyat_yas_kirilimiyla_hesaplanir` →
`Per_person_price_is_computed_by_age_band`. 46 dosya, 330 tanımlayıcı,
~250 test metodu. Dosya adları sınıf adlarına uyduruldu (`git mv`).

**Yorumlar Türkçe KALDI** — Mert'in açık talebi: *"Olm yorum satırları
falan türkçe kalabilir ben genel olarak isimlendirmelerin ingilizce
olmasını istemiştim."* Dokuz dosyanın yorumu çevrilmişti, geri alındı ve
yorumların HEAD ile birebir aynı olduğu programatik olarak doğrulandı.

**Neden:** Gerekçe metni `src/` ile aynı dilde kalıyor; kod içi isimler
ise dilden bağımsız okunuyor.

⚠️ **Hata mesajı dizgileri de Türkçe kaldı.** Üretim kodu Türkçe mesaj
döndürüyor; `Assert.Contains("zaten", error.Message)` gibi doğrulamalar
çevrilseydi testler geçer ama **hiçbir şey ölçmezdi**. Çeviri betiği bu
yüzden dizgileri ve yorumları maskeleyip yalnız kod bölgesine dokundu.

⚠️ **C# ayrılmış sözcükleri tuzağı.** `olay → event` ve `ozel → private`
derlemeyi patlattı (`event` ve `private` ayrılmış). `add`, `remove`,
`value`, `record` bağlamsal olduğu için sorun çıkarmadı. Toplu yeniden
adlandırmada hedef adlar **önce anahtar sözcük listesine karşı**
süzülmeli → [[api-notlar]]

⚠️ **Üretim üyesi adını test haritasına koymak.** `ManualAsync`,
`MaskelemeEsigi`, `Gecerlilik`, `Maske`, `ContactMasker.Mask` `src/`
içinde yaşıyor; haritaya girdikleri için test tarafında var olmayan
adlara çevrildiler ve derleme kırıldı. Ders: harita hedefleri `src/`
tanımlayıcı kümesinden **düşülmeli**.

⚠️ **Enterpolasyon delikleri ilk geçişte atlandı.** `$"...{ilk}..."`
içindeki kimlikler dizgi sayıldığı için çevrilmedi; bildirim yeniden
adlandı, kullanım kalmadı → 40+ `CS0103`. İkinci geçiş `{...}`
deliklerini de çeviriyor. Delik içinde tırnak varsa
(`{string.Join(", ", x)}`) regex hâlâ erken kesiyor — kalan 7 yer elle
düzeltildi.

**Kanıt:** `dotnet test` → 441/441 yeşil (28 s). Yorumların
değişmediği, HEAD'deki yorum listesiyle karşılaştırılarak doğrulandı:
0 fark. Commit `f36f5ce`, push edildi.

## 2026-08-27 — `src/` tanımlayıcıları da İngilizce

**Karar (Mert):** Test tarafındaki kural üretim koduna da uygulandı:
**isimler İngilizce, yorumlar Türkçe.** 104 dosya, ~410 tanımlayıcı.
`Calistir` → `ExecuteAsync`, `YazAsync` → `WriteEventAsync`,
`MaskelemeEsigi` → `MaskingThreshold`, `IlkIsim` → `FirstNameOf`.

**Neden:** Test tarafı İngilizce isimlendirmeye geçince kod tabanı iki
dile bölünmüştü; aynı kavram iki adla yaşıyordu (`Calistir` /
`ExecuteAsync`). Gerekçe metni Türkçe kalıyor çünkü kararın *niçin*'i
Mert'in dilinde daha doğru anlatılıyor; kod içi isimler ise dilden
bağımsız okunuyor ve dış kütüphanelerle aynı sözlüğü paylaşıyor.

**Riskli bölgeler ÖNCE ölçüldü, sonra dokunuldu:**

1. **`Domain/` içinde tek bir Türkçe tanımlayıcı yoktu.** Entity
   property'lerinin hepsi zaten İngilizceydi → **hiçbir DB kolonu
   yeniden adlandırılmadı, migration gerekmedi.** Bu ölçülmeden
   başlansaydı 39 migration'lık şemayı kırma riski vardı.
2. **Dışa dönen DTO'larda Türkçe alan adı yoktu.** Public üye taraması
   yalnız dört Türkçe sabit buldu (`Gecerlilik`, `Kategoriler`,
   `Maske`, `MaskelemeEsigi`) ve hiçbiri serileşmiyor.
3. **`Migrations/` klasörü kapsam dışı bırakıldı** — migration sınıf
   adı `__EFMigrationsHistory` kimliğine bağlı.
4. **Olay payload anahtarları dizgi.** `EventPayloadPolicy` izin
   listesinde Türkçe anahtar olmadığı doğrulandı; anonim üye adı
   değişen tek yer `JobHealthController`.

⚠️ **DİZGİ İÇİNDEKİ AD SESSİZCE KIRILIR.** `FakePaymentProvider`
yönlendirme adresini `$"?islem={operationId}"` diye **dizgi** olarak
kuruyordu. Controller parametresi `islem` → `operation` olunca dizgi
Türkçe kaldı ve iki uç birbirini bulamaz hâle geldi. **Testler bunu
yakalamadı** — testler `CompleteAsync`'i doğrudan çağırıyor, sorgu
dizesinden geçmiyor. Yakalayan şey `openapi.json`'un yeniden üretilip
**eskisiyle diff'lenmesi** oldu. Ders: toplu yeniden adlandırmadan
sonra sözleşme dosyasını üret ve diff'le; derleyici dizgi görmez.

**Bilinçli iki sözleşme değişikliği:**
- `POST /api/payments/callback` sorgu parametresi `islem` → `operation`
- `GET /api/health/jobs` yanıt alanları (`sonCalisma` → `lastRun`,
  `gecenSure` → `elapsed`, `basarili` → `succeeded`, `islenen` →
  `processed`, `isSayisi` → `jobCount`, `basarisiz` → `failed`,
  `isler` → `jobs`). Anonim tip olduğu için `openapi.json`'da şeması
  yok; front-end henüz başlamadığı için tüketen kimse yok →
  [[web-durum]] için not gerekiyor.

**Kanıt:** `dotnet build` temiz · `dotnet test` 441/441 · 310 dosyada
yorum farkı **0** · uygulama ayağa kaldırılıp ölçüldü:
`/api/health/jobs` kimliksiz **401**, `/api/boats/olmayan-tekne`
**404** + Türkçe gövde, `/api/partners/apply` boş gövde **400** ·
`openapi.json` yeniden üretildi, tek fark yukarıdaki parametre adı.
Commit `689869b`, push edildi.

## 2026-08-27 (3) — İfade gövdeli üye (`=>`) kullanılmıyor

**Karar (Mert):** Üye gövdeleri `=>` ile YAZILMAZ, blok gövde kullanılır.
567 yer çevrildi (metot, property, ctor).

**Neden:** Mert'in kendi ifadesiyle *"böyle olduğunda ben kod okumakta
zorlanıyorum."* Kod okunmak için var; okuyanı zorlayan bir kısaltma,
kazandırdığı satırdan daha pahalı.

**Kapsam üç yapıdan yalnız birini içeriyor** — bu ayrım kararın kendisi
kadar önemli:

| Yapı | Örnek | Karar |
|---|---|---|
| Üye gövdesi | `public string Name => "x";` | **Bloğa çevrildi** |
| Lambda | `.Where(b => b.PartnerId == id)` | **Dokunulmadı** |
| `switch` kolu | `{ SqlState: "23505" } => "..."` | **Dokunulmadı** |

Lambda'yı bloğa çevirmek LINQ zincirlerini okunmaz hâle getirirdi —
yani aynı gerekçe ters yönde çalışıyor. `=>` sayısı 1736 → 1169;
kalan 1169 bu iki kategoriden.

⚠️ **DÖNÜŞÜM REGEX'LE YAPILMADI.** `=>` üç ayrı dil yapısında geçiyor ve
ifadenin nerede bittiğini (çok satırlı, iç içe lambda, dizgi içinde `;`)
metin işleme ile bulmak güvenilir değil. Roslyn'in kendi düzeltmesi
kullanıldı: `dotnet format style --diagnostics IDE0021 IDE0022 IDE0023
IDE0024 IDE0025 IDE0026 IDE0027 IDE0061 --severity info`.

⚠️ ~~**KURAL `.editorconfig`'E YAZILDI.**~~ **İPTAL — aşağıdaki
2026-08-27 (4) girişine bak.** Dosya aynı gün Mert'in isteğiyle
kaldırıldı; kural yazılı ama **otomatik denetlenmiyor**.

**Roslyn çıktısı iki yerde elle düzeltildi:**
1. `=> ` (3 karakter) → `return ` (7 karakter) olunca Roslyn devam
   satırlarını **4 boşluk sağa kaydırıyor**. 67 dosyada 1151 satırın
   girintisi, HEAD'deki metinle satır-satır eşleştirilerek orijinaline
   geri çekildi (`difflib`, yalnız boşluk farkı olan satırlar).
2. Erişimciler yedi satıra açılıyordu
   (`get` / `{` / `return x;` / `}`). Mert'in seçtiği biçim tek satır:
   177 erişimci `get { return x; }` hâline indirildi.

**Kanıt:** `dotnet build` temiz · `dotnet test` **441/441** · 116 değişen
dosyada **yorum farkı 0** · `openapi.json` yeniden üretildi, **fark yok**
(imzalar değişmedi) · canlı: `/api/health/jobs` kimliksiz **401**,
olmayan tekne **404**, boş gövdeyle apply **400**, `/api/search` **200**.
Commit `0a59632`, push edildi.


## 2026-08-27 (4) — `.editorconfig` kaldırıldı

**Karar (Mert):** *"istemiyorum onu kaldır."* Bir önceki girişteki
`.editorconfig` silindi (`c3062dc`).

**Neden:** Mert deponun kök dizininde araç zincirine kural dayatan bir
dosya istemiyor. Karar onun; gerekçesini sormadım.

**İPTAL EDİLEN:** Yalnız DAYATMA mekanizması. `=>` üye gövdesi
kullanmama kararı (2026-08-27 (3)) **yürürlükte** ve koddaki 567
dönüşüm yerinde duruyor.

⚠️ **KURAL ARTIK KORUNMUYOR.** IDE uyarı vermiyor, `dotnet format`
denetleyemiyor. Yeni yazılan kodda `=>` üye gövdesi geri gelirse
kimse fark etmez — bunu yakalayacak tek şey bu notu okumak.
Bu, [[api-mimari]]'deki *"bir dosyayı vault'a koymak onu canlı tutmaz;
onu canlı tutan tetikleyicisidir"* dersinin bilinçli olarak kabul
edilmiş hâli: tetikleyici kaldırıldı, kural notta kaldı.

**Kanıt:** `dotnet build` temiz, `dotnet test` **441/441** — dosya
silindikten sonra ölçüldü. Commit `c3062dc`, push edildi.

---

## 2026-08-28 — Tekne görselinde tek varyant saklanıyor, üçü değil

`IImageProcessor` üç genişlik üretiyor (400/800/1600) ama `BoatMedia` satırında
**tek** `FileKey` alanı var. Yükleme en büyük varyantı saklıyor, diğer ikisi
atılıyor. `PublicBoatDetail.Media` ve `SearchResultItem.CoverUrl` tek adres
döndürüyor.

**Neden:** Üç varyantı saklamanın iki yolu vardı ve ikisi de kötüydü.

1. **Ada göre türetme** (`{anahtar}-400.webp`) — örtük sözleşme. `TargetWidths`
   ileride değişirse eski satırların türetilmiş adresleri **sessizce** kırılır;
   kimse fark etmez çünkü satır sağlam görünür. Kırık görsel, biraz büyük
   görselden kötüdür.
2. **Şemaya varyant alanı eklemek** — sonradan eklenirse yüklenmiş bütün
   görsellerin yeniden işlenmesi gerekir.

Arayüz `next/image` kullanıyor ve yeniden boyutlandırmayı kendi yapıyor; web
oturumu bundan vazgeçme ihtimali olmadığını yazılı olarak teyit etti
(2026-08-28). Yeniden boyutlandırmayı istemci katmanında tutmak, genişlik
listesi değiştiğinde şemayı kırmıyor.

**Bedeli kabul edildi:** yükleme başına iki varyantın işlem maliyeti boşa
gidiyor. Yükleme seyrek bir işlem, bu maliyet ölçülebilir değil.

**Değişirse:** arayüz `next/image`'tan vazgeçerse bu karar iptal edilmeli ve
şemaya varyant alanı eklenmeli — o noktada mevcut görsellerin yeniden
işlenmesi de gerekir.

`Width`/`Height` **saklanan** dosyanın ölçüleridir, yüklenenin değil. Arayüz
en-boy oranını bunlardan hesaplayıp görsel inmeden yer ayırıyor; orijinalin
ölçüsü yazılsaydı oran yanlış çıkar ve yerleşim sıçraması düzelmezdi.

İlgili: [[api-mimari]] · [[api-durum]]

---

## 2026-08-28 (2) — Şablon metni taşır, ticari koşulları taşımaz

`ContractTemplates` yalnız `Name`, `BodyHtml`, `Version` taşır. Komisyon oranı ve
hakediş periyodu **`Contracts` satırındadır**, sözleşme başına. Şablona varsayılan
komisyon/periyot alanı **eklenmeyecek**.

**Neden:** Mert'in cümlesi — *"Komisyon ve periyot alanı sitemizde sabit değil, her
bir işletmeciye farklı periyotlar ve farklı komisyonlar tanımlayabiliriz."* Oran ve
periyot pazarlık konusu. Şablona varsayılan konsaydı pazarlık gizli bir sayıya
sabitlenir, personel değiştirmeyi unuttuğunda işletme yanlış oranla bağlanır ve bu
**imzalanmış bir belgede** kalırdı. Boş alan durdurur, yanlış varsayılan durdurmaz.

Şemaya dokunurken bu ayrım korunacak.

## 2026-08-28 (3) — Sözleşme metni sunucuda temizlenmiyor

`GET /api/platform/contracts/{id}` `bodyHtmlSnapshot` alanını **ham HTML** olarak
döndürüyor. Sunucu tarafında sanitize edilmiyor.

**Neden:** Metin gönderim anında dondurulmuş bir belgedir. Temizlemek onu
**değiştirmek** olurdu; işletmenin onayladığı belge ile panelde görünen belge
ayrışırsa bir uyuşmazlıkta hangisinin geçerli olduğu tartışmalı hale gelir.

Risk kabul edildi ve **gösteren tarafa** devredildi: şablonu platform personeli
yazıyor, ama bir şablon bir kez kötü yazılır ya da dışarıdan içe aktarılırsa metni
basan her ekranda o personelin oturumunda çalışır. Web oturumu metni `sandbox`
özniteliği boş bir `<iframe srcdoc>` içinde basıyor — betik çalışmaz, üst pencereye
erişemez (2026-08-28'de kararlaştırıldı).

Alan adları ayrımı taşıyor: sözleşmede `bodyHtmlSnapshot` (gönderim anının kopyası),
şablonda `bodyHtml` (yaşayan hâli). **Yeni bir uç metin döndürecekse aynı ayrımı ve
aynı yalıtma yükümlülüğünü taşımalı.**

İlgili: [[api-mimari]] · [[api-durum]]

---

## 2026-08-28 (4) — Depo görünürlüğü nesne izniyle değil önek politikasıyla

`IFileStorage.PutAsync` `publiclyReadable` parametresi alıyor ama
`S3FileStorage` onu **isteğe yansıtmıyor** ve yansıtılmayacak. Dosya
görünürlüğünü **kova politikası** belirliyor; kural: açık okuma **yalnız
`boat-media/*`** önekine verilir, diğer bütün önekler kapalıdır ve yalnız
yetkili uçlardan iner.

**Neden nesne izni eklenmedi:** kova politikası `s3:GetObject` iznini herkese
veriyorsa nesne izni ne olursa olsun dosya iner. Parametreye bir izin
konsaydı kod korunuyormuş gibi görünür ama korunmazdı — **yanlış güven,
korumasızlıktan kötüdür.** Bayrak yine de anlamlı: hangi dosyanın hangi
önekte durması ve dağıtımın hangi öneki açması gerektiğini söylüyor.

**Nasıl bulundu:** tekne belgesi ucu yazıldıktan sonra depo adresi kimliksiz
denendi ve `200` döndü. Geliştirme kovası bütün nesnelere açık okuma
veriyordu. Aynı açık, aylardır yayında olan **işletme evrakını** da
kapsıyordu — vergi levhası ve kimlik fotokopisi. Dosyayı koruyan tek şey
anahtarın içerikten türetilmiş olmasıydı, yani tahmin edilemezlik; erişim
denetimi değil.

Geliştirme politikası daraltıldı ve ölçüldü: belge `403`, galeri `200`,
yetkili indirme uçları `200`. **Üretim kovasının politikası ayrıca
doğrulanmalı** → [[api-durum]] S-24.

İlgili: [[api-mimari]] · [[api-durum]]

## 2026-08-28 (5) — Ödeme geri çağrısı özeti, üye listesiyle aynı satır tipini döndürür

`POST /api/payments/callback` yanıtı `{succeeded, reservation}` oldu.
`reservation`, üye listesinin ve misafir sorgusunun döndürdüğü
`MyReservationItem`'ın ta kendisi — geri çağrıya özel yeni bir tip
yazılmadı.

**Neden:** Uç yalnız `succeeded` döndürüyordu. Ödeme sağlayıcısından
dönen misafirin elinde oturum da yok, rezervasyon kodu da yok — yalnız
işlem kimliği var. Dönüş sayfasının gösterecek gerçek verisi olmadığı
için **aylarca sabit veriden okudu**: ödemesini yapan müşteri ekranda
BAŞKASININ rezervasyon kodunu ve tutarını gördü. Bu, tek bir eksik alanın
kullanıcıya kadar taşınmasının en pahalı örneği.

Yeni bir tip yerine mevcut satır tipi seçildi çünkü arayüz aynı
rezervasyonu üç yerde gösteriyor; üçü ayrı şekilde dönseydi arayüz üç ayrı
eşleme yazardı ve biri değişince diğer ikisi sessizce eskirdi.

**Özet iletişim bilgisi ve biniş jetonu taşımaz.** Bu uç kimlik
doğrulamıyor ve `AllowAnonymous`; elindeki tek kanıt sağlayıcının işlem
kimliği. Alınmayan alan sızdırılamaz → [[api-desenler]]

Ödeme zaten başarılıyken erken dönen dal da özeti dolduruyor. Doldurmasaydı
sayfayı yenileyen misafir dolu ekrandan boş ekrana düşerdi — parası
alınmış birinin göreceği en kötü şey.

`succeeded` alanı korundu; mevcut çağıranlar kırılmasın diye.

## 2026-08-28 (6) — Biniş QR ucu YAZILMADI, jetonun tek seferlik olması korundu

Frontend'in birinci önceliği `qrImageUrl` idi. Yazılmadı.

**Neden:** `CreateReservationResult.BoardingToken` düz metni **yalnız
oluşturma yanıtında ve yalnız bir kez** dönüyor; veritabanında yalnız özeti
saklanıyor ve kaybolursa yeniden üretilemez. Bu, koda sonradan sızmış bir
eksiklik değil, XML belgesinde yazılı kasıtlı bir özellik: jetonu
sonradan okuyabilen bir uç, veritabanını okuyabilen herkesin biniş
jetonunu okuyabilmesi demek.

QR ucu açmak için jetonun düz metninin saklanması gerekirdi. Karar Mert'in
→ `S-25` [[api-durum]]. Ara çözüm önerim: QR'ı **oluşturma yanıtından
istemcide üretmek** — jeton zaten orada bir kez geçiyor, sunucuda hiçbir
şey değişmiyor.

**Yapmadığımı yaptım sanmamak için not:** bu karar ölçülerek değil
belgeden okunarak verildi; jetonun geri üretilemezliği kodda `Hash`
karşılaştırmasıyla doğrulandı.

## 2026-08-28 (7) — QR'ın istemcide üretilmesi önerisi GERİ ÇEKİLDİ

`2026-08-28 (6)`'da ara çözüm olarak "QR'ı oluşturma yanıtındaki jetondan
istemcide üret" önerilmişti. Frontend oturumu uygulamadı ve gerekçesi
öneriden güçlü çıktı; öneri geri çekiliyor.

**Neden:** Ödeme arada dış sağlayıcıya tam sayfa yönlendirmesi yapıyor.
Jetonu başarı ekranına taşımak için tarayıcı depolamasına yazmak gerekir —
geri üretilemeyen bir doğrulama sırrını diske yazmak. Ama asıl sebep bu
değil: **QR yalnız ödemeden hemen sonraki sekmede olurdu.** Müşteri sayfayı
kapatırsa, telefonundan açarsa, belgeyi ertesi gün yazdırırsa QR bir daha
hiç olmazdı.

"Bazı müşteride var, bazısında yok" bir biniş belgesi, hiç QR olmamasından
kötüdür: destek hattı "benim QR'ım nerede" çağrısıyla dolar ve sebebi kimse
bulamaz, çünkü sebep müşterinin sekmeyi kapatıp kapatmadığıdır.

Bugünkü hâl: QR yerine yer tutucu, kod büyük ve kopyalanabilir, kaptan elle
okutuyor. **Eksik ama tutarlı** — her müşteride aynı.

Ders, QR'dan bağımsız olarak geçerli: **yalnız bir yoldan gelene çalışan bir
özellik, hiç olmayan özellikten kötü olabilir.** Tutarlılık burada
tamlıktan önce geliyor.

`S-25` buna göre yeniden yazıldı → [[api-durum]]

## 2026-08-28 (8) — Bir alan iki soruya cevap veremez: `memberCount` yanında `canDelete`

Rol listesi `memberCount` döndürüyordu ve arayüz bunu iki şey için
kullanıyordu: "kaç kişi çalışıyor" ve "silinebilir mi". İkincisi için
yanlış sayıydı ve panel "0 kişi" gösterip silme isteği reddediliyordu.

**Neden sayı düzeltilmedi:** ikisi de doğru, ama ayrı sorular.
`memberCount` yalnız aktif çalışanı sayıyor ve "bu rolde kaç kişi
çalışıyor" sorusunun doğru cevabı bu. Silinebilirlik ise çıkarılmış
çalışanın duran satırını da hesaba katmak zorunda, çünkü veritabanındaki
kısıtlayıcı yabancı anahtar onu sayıyor — silmeyi gevşetmek uygulamanın
elinde değil.

Sayıya pasifleri eklemek "kaç kişi çalışıyor" cevabını bozardı;
silmeyi gevşetmek mümkün değildi. Üçüncü yol: **eksik olan soruyu ayrı
alan olarak vermek.** `canDelete`, silmenin reddettiği iki koşulun tam
tersinden hesaplanıyor ve kaynağı silmenin kullandığı koşulun aynısı
(`RolesInUseAsync` ≡ `RoleInUseAsync`). İki ayrı yazım olsaydı biri
değişince diğeri sessizce eskirdi — zaten olan buydu.

**Genel kural:** bir alanın iki soruya birden cevap verdiği her yer, o iki
sorunun ayrışacağı bir durum bekliyor demektir. Ayrışma ortaya çıkana kadar
alan "çalışıyor" görünür.

**Ölçüm notu:** alan her zaman `false` dönseydi bütün olumsuz sınamalardan
geçerdi. Bu yüzden kullanılmayan bir rolün `canDelete=true` dönüp gerçekten
`204` ile silindiği ayrıca ölçüldü → [[api-durum]] "olumlu durum" kuralı.

## 2026-08-28 (9) — Hız sınırı kimlik doğrulamadan SONRA uygulanır

`UseRateLimiter` artık `UseAuthentication` ve `UseAuthorization`'dan
sonra çağrılıyor.

**Neden:** önceki sırada `context.User` bölümleme anahtarı hesaplanırken
henüz doldurulmamış oluyordu. `FindFirst(ClaimTypes.NameIdentifier)`
daima `null` dönüyor, yani `panel`, `rezervasyonSorgu` ve `personelEkle`
politikalarının "kullanıcıya göre böl" niyeti hiçbir zaman
gerçekleşmiyordu — hepsi IP'ye göre bölünüyordu.

Yayında bunun bedeli: NAT ya da mobil operatör CGNAT'ı arkasındaki
kullanıcılar tek IP olarak görünür. Tek bir gürültülü istemci, aynı çıkış
adresini paylaşan herkesin panelini dakikada 120 istekte kilitlerdi.

**Kabul edilen bedel:** kimlik doğrulama artık sınırdan önce çalışıyor,
yani bir sel jeton doğrulama işi yaptırabiliyor. Jetonsuz istekte bu iş
neredeyse sıfır (doğrulanacak jeton yok) ve kimliksiz çağıran hâlâ IP
kovasına düşüyor. Kimliksiz uçların sınırlı kaldığı ayrıca ölçüldü.

**Bu kusurun sınıfı `publiclyReadable` ile aynı:** kontrol yazılmış, hiç
uygulanmamış, testler geçmiş. Ortak sebep de aynı — **tek kullanıcıyla
iki bölümleme aynı görünür**, tıpkı tek kovayla iki politika gibi. Bir
ayrımı sınamak için ayrımın iki tarafını da üretmek gerekiyor.

**Testin kendisi doğrulandı:** yeni test eski sıra geri getirilerek
çalıştırıldı ve BAŞARISIZ oldu. Geçen bir test, geçmemesi gereken durumda
da geçiyorsa hiçbir şey ölçmüyor demektir → [[api-durum]]

## 2026-08-30 — İşletme rezervasyon listesi iletişim bilgisi taşır, kimlik bilgisi taşımaz

`GET /api/partner/reservations` satırları müşterinin adı, e-postası ve
telefonunu döndürüyor; yolcuların kimlik bilgisini (TCKN, pasaport)
döndürmüyor.

**Neden taşıyor:** işletme turu yapan taraftır. Hava muhalefetinde iptal,
kalkış gecikmesi, buluşma noktası değişikliği — hepsinde müşteriye
ulaşması gerekir. Ulaşamayan bir işletme müşteriyi iskelede bekletir.

**Neden kimlik bilgisi taşımıyor:** yetki kataloğu bu ayrımı ZATEN
yapıyor — `reservation.read` ve `passenger.read` ayrı yetkiler. Yani
"rezervasyonu yapana ulaşmak" ile "yolcuların kimliğini görmek" projenin
kendi tasarımında farklı sorular. Bu uç yalnız birincisini istiyor.

**Ölçüldü, varsayılmadı:** bugüne kadar işletme yalnız müşterinin ADINI
görüyordu (biniş ekranı `ContactFullName` döndürüyor). E-posta ve telefon
YENİ bir açılım, mevcut bir davranışın tekrarı değil — bu yüzden `S-27`
olarak Mert'e teyit sorusu açıldı ve engelleyici sayılmadı: panel bu
bilgiler olmadan çalışmıyor ve gerekçe sözleşmenin ifası.

Sayfa boyutu tavanı (50) burada ayrıca bir koruma: sınırsız sayfa boyutu,
bütün müşteri listesini tek istekte dışarı almanın yolu olurdu.

`includeCancelled` AYRI bir alan, `status` içine gizlenmiş varsayılan
değil. Gizli olsaydı "3 turum var" diyen bir ekranda iptallerin neden
sayılmadığı hiçbir yerde görünmezdi; ayrı alan olunca davranış OpenAPI
belgesinde de okunuyor → [[api-durum]] `S-27`

## 2026-08-31 — İşletme ayarları: sınır bir `if` değil, isteğin tipi

`PUT /api/partner/profile` yalnız beş alan yazıyor: `displayName`,
`email`, `phone`, `address`, `city`.

**Neden yasal kimlik yazılamıyor:** unvan, vergi numarası, vergi dairesi
ve iş yeri türü başvuruda doğrulandı, imzalı sözleşmede yazılı ve ödeme
sağlayıcısındaki alıcı kaydına gönderildi (`RegisterPayeeAsync`). Tek
taraflı değişmeleri kaydı sözleşmeyle çelişkiye düşürürdü; vergi
numarasının ayrıca tekil indeksi var.

**Neden IBAN yazılamıyor:** paranın gideceği hesap. Hesabı ele geçiren
biri IBAN'ı değiştirip bütün gelecek hakedişleri yönlendirebilirdi. Bu
değişiklik kendi akışını hak ediyor — parola teyidi, olay günlüğü ve
bildirim ile, tıpkı sahiplik devrinde olduğu gibi. Kataloğun
`payout.manage` yetkisini platforma kapalı tutması da bu yönü destekliyor.

**Sınırın biçimi:** yasaklı alanlar `UpdatePartnerProfileRequest`
kaydında BULUNMUYOR, yani bağlanamıyorlar. Kod içinde bir süzgeç olsaydı
bir gün biri kaydı genişletip süzgeci güncellemeyi unuturdu. Canlıda
denendi: gövdeye `legalName`, `taxNumber`, `iban`, `status` eklendi,
hiçbiri değişmedi.

**Okuma yazmadan fazla alan döndürüyor** ve bu kasıtlı: işletme vergi
numarasının yanlış girildiğini GÖRMELİ, düzeltmeyi platformdan
isteyebilmeli. Yalnız yazılabilenler dönseydi hatayı fark edemezdi.
IBAN'ın son dört hanesi dönüyor — "doğru hesap mı" sorusuna yetiyor,
tamamını okutmuyor.

**Yeni yetkinin geri doldurulması zorunluydu.** Sahip rolü bütün
atanabilir yetkileri BAŞVURU ANINDA topluca alıyor
(`GetAssignablePermissionIdsAsync`). Sonradan eklenen bir yetki, o
tarihten önce kaydolmuş hiçbir sahibe düşmez: uç açılır, mevcut
işletmelerin hepsi `403` alır ve sebebi hiçbir ekranda görünmez.
Migration 11 sahip rolünü doldurdu. **Yeni yetki eklerken bu adım her
seferinde gerekli** → [[api-desenler]]

## 2026-08-31 (2) — Olay günlüğü yükü dizi kabul etmiyor

`changedFields` önce `List<string>` olarak gönderildi. Satır yazıldı,
uç `200` döndü, **yük BOŞ kaldı.**

**Neden:** `EventPayloadPolicy` iç içe değerleri (dizi ve nesne) kasten
düşürüyor ve düşürürken uyarı yazıyor. Yani sistem doğru davrandı ve
sebebini de söyledi; hata bendeydi — politikayı okumadan liste gönderdim.

**Yanıta bakarak görünmezdi.** `200` dönüyordu ve satır da yazılıyordu;
eksik olan yalnız yükün içeriğiydi. Veritabanı satırına bakınca görüldü.

Çözüm: virgülle birleştirilmiş metin → `{"changedFields": "phone"}`.

**Kural:** olay günlüğüne yalnız SKALER değer gönderilir. Birden çok
değer taşınacaksa birleştirilmiş metin kullanılır → [[api-desenler]] ·
[[api-yazilmis-ama-uygulanmamis-kontrol]]

## 2026-08-31 (3) — Yolcu listesi bayrağı yalnız teknenin anahtarından okunur

Fiyat bağlamı bu bayrağı `DurationKind == MultiDay` ifadesinden
hesaplıyordu; artık `Boat.RequiresPassengerList`'ten okuyor.

**Neden:** kural 2026-08-22'de belgelenmişti — yolcu tablosu her
rezervasyonda değil, **teknenin "yolcu listesi ister" anahtarı açıkken**
dolar. KVKK gerekçesi de buna dayanıyor: kimlik verisi "lazım olur diye"
değil, **tekne sahibinin beyan ettiği yasal yükümlülük** gerekçesiyle
toplanıyor (KVKK m.4). Süreden türetmek, anahtarı kapalı bir teknenin
müşterisinden **beyansız** kimlik verisi istemek olurdu — yani yalnız
yanlış değil, gerekçeyi çürüten bir hata.

**Zarar neden ekranla sınırlı değildi:** `ReservationFactory` bayrağı
teklifin sonucundan kopyalayıp rezervasyona DONDURUYOR. Yanlış yazılan
değer sonradan düzeltilemez; o rezervasyon ömrü boyunca "yolcu listesi
istemiyor" der. Canlıda ölçüldü: tekne `t`, rezervasyon `f`.

**Aynı işi yapan iki yol ayrışmıştı:** teklif akışı
(`OfferRepository`) bayrağı zaten `brt.Boat.RequiresPassengerList`
üzerinden okuyordu. Biri tekneye, diğeri süreye bakıyordu ve ikisi de
rezervasyon üretiyordu.

**Bir test kusuru iddia ediyordu.** `Overnight_rental_charges_one_extra_day`
içinde `Assert.True(offer.RequiresPassengerList)` vardı ve düzeltme onu
kırdı. Hangisinin doğru olduğuna vault'taki karara bakılarak karar
verildi, teste bakılarak değil.

**Ders:** kırılan bir test her zaman değişikliğin yanlış olduğu anlamına
gelmez. Test de bir iddiadır ve iddianın kaynağı sorulmalı — bu testinki
koddan okunmuş bir gözlemdi, karardan değil → [[api-desenler]] ·
[[api-yazilmis-ama-uygulanmamis-kontrol]]

---

## 2026-09-04 — Blog: yayındaki işletme yazısı düzenlenirse onaya geri düşer

**Karar:** `AuthorPartnerId` dolu bir yazı `Published` iken güncellenirse aşama
`UnderReview`'a çekilir, `ApprovedByUserId` ve `ApprovedAt` temizlenir, yazı
herkese açık sorgulardan çıkar. Platformun kendi yazısı (`AuthorPartnerId`
boş) yayında kalır.

**Neden:** Düşmeseydi onay tiyatro olurdu. İşletme sade bir yazı onaylatır,
onaydan sonra gövdesini istediği gibi değiştirirdi ve platform bunu hiçbir
yerde görmezdi — hata da çıkmazdı, çünkü kural yoksa ihlal de yok. Onayın tek
somut anlamı bu kuralda.

**Alternatifler:** (a) düzenleme yayını bozmasın — onayı anlamsız kılıyor,
elendi. (b) düzenleme tamamen yasaklansın — yazım hatası düzeltilemez hale
gelirdi, elendi.

**Bedeli açık:** yazar bir virgül düzeltmek için de onay bekliyor. Kabul
edildi; alternatifi denetlenmeyen içerik.

**`PublishedAt` temizlenmiyor** — yazının İLK yayın tarihidir ve yeniden
onaylanınca korunur. Veritabanı kısıtı yalnız aşama `Published` iken dolu
olmasını istiyor, tersini yasaklamıyor.

**Kanıt:** canlı ölçüldü — yayındaki yazı güncellendi, `status` `UnderReview`,
`approvedAt` `null`, `publishedAt` korundu, herkese açık detay `404`. Platform
yazısında aynı akış `Published` kaldı (test). Kural koddan çıkarıldığında
`Yayindaki_isletme_yazisi_duzenlenince_onaya_geri_dusuyor` kırmızıya döndü.

---

## 2026-09-04 (2) — `BlogPosts`'a `RejectionReason` kolonu eklendi

**Karar:** Nullable `character varying(500)`. Moderatörün ret gerekçesi bu
kolonda yaşıyor ve yazara `GET /api/blog/posts/{id}` ile dönüyor.

**Neden:** Gerekçenin gidebileceği başka yer YOK. `EventPayloadPolicy` serbest
metni yasaklıyor (olay günlüğü temizlenemiyor), yani günlüğe yazılamaz.
Kolonsuz bir ret, yazara "bir şey yanlış" demekten ibaret kalırdı ve aynı yazı
aynı hatayla tekrar gönderilirdi — moderatör aynı işi iki kez yapar.

**Alternatifler:** (a) gerekçe hiç saklanmasın — yukarıdaki döngü, elendi.
(b) mesajlaşma üzerinden bildirilsin — konuşma kapsamı müşteri-işletme
ekseninde, platform-yazar ekseni yok; yeni bir kavram açardı, elendi.

**Şema çıkarımla kurulmaz kuralına göre:** bu bir çıkarım ve `[makul]` damgalı.
Mert'e soruldu (2026-09-04 soru listesi). Geri alma bedeli düşük: nullable
kolon düşürmek, veri kaybı yok.

**Migration:** `20260904191507_A76_BlogRetGerekcesi` — nullable, varsayılansız,
tablo yeniden yazılmıyor.

---

## 2026-09-04 (3) — Blog kategorisi yönetimi `blog.approve` yetkisinde

**Karar:** `POST/PUT/DELETE /api/blog/categories` yalnız `blog.approve` ile.
Okuma (`GET`) herkese açık.

**Neden:** Kategori listesi bütün işletmelerin yazılarını gruplayan ORTAK bir
taksonomi. Her işletme kendi kategorisini açabilseydi liste birkaç ayda
birbirinin eşanlamlısı otuz satıra çıkar ve süzgeç işe yaramaz hale gelirdi.
`blog.approve` katalogda `IsPartnerAssignable = false`, yani işletme sahibi bu
yetkiyi çalışanına veremiyor — ayrım kendiliğinden korunuyor.

**Neden hiç yazılmadan bırakılmadı:** `BlogCategories` tablosu şema
kurulduğundan beri BOŞ ve kategori yaratacak hiçbir yol yoktu.
`BlogPosts.BlogCategoryId` ölü bir kolondu.

---

## 2026-09-04 (4) — Yazının altında kişi adı değil işletmenin görünen adı durur

**Karar:** Herkese açık blog yanıtları `authorPartnerName` taşıyor;
`AuthorUserId`'nin arkasındaki kişinin adı soyadı HİÇBİR yanıtta yok.

**Neden:** İşletmenin görünen adı zaten herkese açık bir ticari isim. Panelde
yazan çalışanın adı soyadı değil — o kişi işten ayrıldığında bile yazının
altında kalıcı olarak yayında dururdu ve silinmesini isteyeceği yer belli
değil. Yazar kimliği `AuthorUserId` kolonunda duruyor, denetim için yeterli.

**Kanıt:** `Herkese_acik_yanit_isletme_adini_tasiyor_kisi_adini_tasimiyor`.

---

## 2026-09-04 (5) — `posts`, `categories`, `moderation` kısa ad olarak yasak

**Karar:** Bu üç değer `BlogService.ReservedSlugs` içinde ve yazma anında
reddediliyor (`ReservedSlug`).

**Neden:** Üçü de `/api/blog/` altında gerçek yol parçası. Bir yazı bunlardan
birini kısa ad olarak alsaydı `GET /api/blog/{slug}` ona HİÇ ulaşamazdı:
yönlendirme sabit yol parçasını değişkene tercih eder. Yazı kaydedilir,
yayınlanır, listede görünür ve adresinden açılmaz — hiçbir yerde hata çıkmaz.

**Alternatifler:** yazarlık uçlarını `/api/blog/` dışına taşımak — dört
controller yerine üç ayrı önek doğururdu ve aynı kaynağın uçları dağılırdı,
elendi.

**Bakım kuralı:** `/api/blog/` altına yeni bir SABİT yol parçası eklenirse
`ReservedSlugs` da genişletilmeli. Unutulursa o adı taşıyan mevcut yazı
sessizce erişilemez olur.

**Kanıt:** liste boşaltıldığında `Ayrilmis_kisa_ad_reddediliyor` üç dalında da
kırmızıya döndü.

---

## 2026-09-04 (6) — Kapak görseli `blog-media/` önekine yazılıyor, kova politikası genişletildi

**Karar:** Blog kapağı `blog-media/{postId}/...webp`. Geliştirme kovasının
anonim okuma politikası `boat-media/*` yanına `blog-media/*` eklenerek
genişletildi; `boat-documents/*` ve `partner-documents/*` kapalı kaldı.

**Neden:** `S3FileStorage` `publiclyReadable` parametresini kullanmıyor —
görünürlüğü YALNIZ kova politikası belirliyor (`S-24`). Politika
genişletilmeseydi yazı yayında görünür, kapağı kırık çıkardı.

⚠️ **`S-24` bu yüzden büyüdü:** üretim kovasında açık okuma artık İKİ öneke
verilmeli. Tek önek yazılırsa blog kapakları üretimde sessizce kırılır —
uygulama tarafında hiçbir hata olmaz, çünkü hata tarayıcıda ve nesne
deposunda.

**Kanıt:** politika öncesi kapak `403`, sonrası `200 image/webp`; aynı ölçümde
`boat-documents/*` ve `partner-documents/*` `403` kaldı.

---

## 2026-09-04 (7) — Favoriler ayrı tabloda, hesap kapatmada SİLİNİYOR

**Karar:** `FavoriteBoats` (`UserId`, `BoatId`, `CreatedAt`), `(UserId, BoatId)`
benzersiz. Ekleme ve çıkarma idempotent. Hesap kapatılınca satırlar
`AnonymizationRepository` içinde **siliniyor**.

**Neden ayrı tablo:** "bu kullanıcı neleri beğendi" ve "bu tekneyi kaç kişi
beğendi" iki ayrı soru; ikisi de indeksle cevaplanabilmeli. Kullanıcı satırına
gömülü bir liste ikinciyi tüm tabloyu taramadan cevaplayamazdı.

**Neden ÜZERİNE YAZILMIYOR, siliniyor:** rezervasyon ve mesajda satır duruyor,
kişisel alanlar temizleniyor — çünkü kaydın kendisi ticari bir belge. Favori
satırının kişisel veriden başka bir içeriği YOK: temizlenecek alanı yok, geriye
anlamsız bir bağ kalırdı.

⚠️ **Yabancı anahtar CASCADE bunu YAPMIYOR.** CASCADE yalnız kullanıcı SATIRI
silinseydi çalışırdı; anonimleştirme satırı silmiyor, üzerine yazıyor. Silme
satırı olmasaydı kapatılmış bir hesabın beğeni listesi veritabanında olduğu
gibi kalır ve bunu hiçbir ekran göstermezdi.
**Kanıt:** silme satırı koddan çıkarıldığında
`Closing_the_account_deletes_favorite_boats` kırmızıya döndü.

**Yayından kalkan tekne listeden ÇIKARILMIYOR, `isAvailable = false` ile
işaretleniyor.** Sessizce çıkarılsaydı kullanıcının listesi sebebi görünmeden
kısalır ve "ben bunu kaydetmiştim" sorusunun cevabı hiçbir yerde olmazdı.
Eklemede ise yayın şartı VAR: müşteri o tekneyi zaten hiçbir ekranda göremiyor,
eklenebilseydi kimlik denenerek yayınlanmamış teknelerin varlığı öğrenilirdi.

**Favori hareketleri olay günlüğüne YAZILMIYOR** — "izi başka tabloda kalmayan
istek günlüğe yazılır" kuralına bilerek açılan istisna. Beğeni listesi kişisel
veri, olay günlüğü temizlenemez; favoriyi ÇIKARMAK o veriyi silme hakkını
kullanmaktır ve çıkarmayı kalıcı bir tabloya yazmak tam olarak o hakkı
geçersiz kılardı.

**`PUT` seçildi, `POST` değil:** işlem idempotent, aynı adrese ikinci istek
aynı durumu bırakıyor. Kalp simgesine iki kez dokunan kullanıcı hata görmemeli.

**Fiyat kartta YOK:** fiyat tarihe, kişi sayısına ve satış biçimine göre
değişiyor, favoride üçü de belli değil. Bağlayıcı olmayan bir "başlangıç
fiyatı", favoriden tıklayan müşteriye ilk ekranda farklı bir tutar göstermek
olurdu.

---

## 2026-09-04 (8) — Bildirim tercihi: bildirim değil KANAL kapatılır

**Karar:** `NotificationPreferences` tablosu üç alan taşıyor —
`EmailEnabled`, `SmsEnabled`, `ReviewInvitationsEnabled`. Rezervasyon onayı ve
iptal bildirimi için **alan yok ve olmayacak**.

**Neden:** Biniş kodu onay mesajında, iade tutarı iptal mesajında. Bunlar
kapatılabilir bildirim değil. Kullanıcının onlar üzerindeki tek denetimi hangi
KANALDAN alacağı.

**Alan hiç var olmazsa kapatılacak bir şey de olmaz** — "istemciden tutar
alınmaz" kuralıyla aynı akıl: bir denetim eklemektense, denetlenecek durumu
imkânsız kılmak.

**En az bir kanal açık kalmak zorunda ve kural VERİTABANINDA**
(`CK_NotificationPreferences_AtLeastOneChannel`). Yalnız uygulama kodunda
olsaydı, denetimi atlayan yeni bir yazma yolu müşteriyi rezervasyon kodunu hiç
alamayacak hâle getirirdi — ve bu iskeleye varana kadar hiçbir yerde
görünmezdi.
**Kanıt:** canlıda `psql` ile doğrudan `UPDATE` denendi, veritabanı reddetti.

**Bugün TAMAMEN kapatılabilen tek bildirim yorum daveti.** Liste bilerek kısa:
her satırın karşılığında onu GÖNDEREN yerde bir denetim var. Denetimi olmayan
bir satır, açılıp kapanan ama hiçbir şey yapmayan bir düğme olurdu — bu
projede beş kez tekrarlanan hata sınıfı.

**Tercih ALICI adresine göre okunuyor, isteği yapana göre değil.** Üye biri
arkadaşı adına rezervasyon yaptığında bildirim arkadaşına gidiyor;
rezervasyonu yapanın "bana SMS gelmesin" tercihine bakmak arkadaşının biniş
kodunu susturmak olurdu.
Telefonla arama YAPILMIYOR: `Users.Phone` benzersiz değil, aynı numarayı
taşıyan iki hesapta hangisinin tercihi geçerli olurdu belirsiz kalırdı.
Rezervasyon bildiriminde e-posta ve telefon aynı iletişim satırından geldiği
için e-postadan bulunan tercih ikisini de yönetiyor.

**Satır yalnız kullanıcı bir şey DEĞİŞTİRDİĞİNDE yazılıyor**; olmayan satır
"hepsi açık" demek. Kayıt anında herkese satır açılsaydı tablo kullanıcı
sayısı kadar büyür ve satırların ezici çoğunluğu varsayılanı tekrar ederdi.

**Yorum daveti işinde: e-posta gitmese bile davet satırı YAZILIYOR.** İki
sebep, ikisi de sessiz:
1. Yazılmasaydı aday her koşuda yeniden seçilir, iş sonsuza kadar aynı
   rezervasyonları tarardı.
2. Kullanıcı tercihini sonradan açtığında aylar öncesinin turları için toplu
   davet giderdi.

**Kanıt:** iki mutasyon, ikisi de yakalandı — kanal kapısı etkisiz hâle
getirildi (2 kırmızı), yorum daveti vazgeçme kapısı kaldırıldı (1 kırmızı).

---

## 2026-09-04 (9) — `S-27`: işletme müşterinin e-postasını ve telefonunu GÖRMEZ

**Karar (Mert):** `GET /api/partner/reservations` yanıtından `contactEmail` ve
`contactPhone` **kaldırıldı**. `contactFullName` kalıyor.

**Neden — ve gerekçe bizim düşündüğümüz değil.** Ben soruyu KVKK sorusu olarak
sormuştum ve karşı gerekçem "hava muhalefetinde işletme müşteriye ulaşamazsa
onu iskelede bekletir" idi. Mert'in sebebi başka:

> *"işletme müşterinin e-posta ve telefonunu görüp kendisi başka yerden
> rezervasyon yaptırabilir"*

Yani mesele gizlilik değil **aracıdan kaçış**. İşletme müşteriye doğrudan
ulaşabilirse ikinci turu platform dışında satar ve komisyonun tamamı kaybolur.
Bu, ürünün gelir modelinin merkezinde duran bir risk ve teknik bir soru olarak
sorulduğunda görünmüyordu.

**Yerine konan akış:** işletme destek talebi açar, durumu anlatır, müşteriye
platform haber verir. Yani ihtiyaç inkâr edilmiyor, ARACIYA bağlanıyor.

**`2026-08-30` kararını iptal eder** — o gün uç bu alanlarla yazılmıştı.

**Testi alan üzerinden değil SERİLEŞTİRİLMİŞ GÖVDE üzerinden yazıldı.**
Kaldırılmış bir özelliğe başvuran test derlenmez, yani yasağı koruyan hiçbir
şey kalmazdı. Gövdeyi okuyan test alanlar geri eklendiğinde kırmızıya dönüyor
ve kurulumda değerler GERÇEKTEN var — kurulum boş bıraksaydı test, alanlar geri
eklense bile yeşil kalırdı.

**Kanıt:** alanlar geri eklenerek mutasyon denendi, test kırmızıya döndü.
Canlı yanıtta 16 alan var, `contactEmail` ve `contactPhone` yok, gövdenin
tamamında tek bir `@` işareti bile geçmiyor.

---

## 2026-09-04 (10) — Mert'in 29 cevabı: API tarafını bağlayanlar

Cevaplar `migrate-design-to-frontend` oturumu üzerinden toplu olarak geldi.
Buraya yalnız **API'yi bağlayanlar** ve **gerekçesi bizim varsaydığımızdan
farklı olanlar** yazılıyor; tam liste [[domain-gereksinimler]] 2026-09-04.

### Para ve vergi

**`S-21` — komisyon matrahı DEĞİŞMİYOR ama çerçeve yanlıştı.**
Ben soruyu *"platform, işletmenin devlete borçlu olduğu vergiden de komisyon
alıyor, kasıtlı mı?"* diye sormuştum. Mert:

> *"İşletmeler teknelerinin fiyatlarını kendileri belirler (KDV dahil ederek
> fiyatlarını koyarlar), biz sadece aracı olduğumuz için ücreti alacağız"*

**Neden çerçevem yanlıştı:** liste fiyatı platformun hesapladığı bir tutar
değil, **işletmenin koyduğu KDV dahil fiyat**. Platform o fiyatın yüzdesini
alıyor. Yani "verginin üzerinden komisyon" diye bir şey yok; komisyon
işletmenin kendi belirlediği rakamın yüzdesi. Bugünkü `grandTotal` üzerinden
hesap **doğru**, kod değişmiyor.

**`S-20` + `57` — KDV oranı rezervasyona DONDURULACAK.**
**Neden:** diğer beş para alanı (birim fiyat, komisyon oranı, kur, kupon payı,
kupon finansörü) zaten donduruluyor. Oran sonradan eklenirse geçmiş satırların
o günkü oranı **geriye dönük üretilemez** — vergi oranı devlet kararıyla
değişen bir sayı ve değiştiği gün eski satırlar sessizce yanlış okunur.

**`59` — TEK ORAN, kalem başına ayrı oran YOK.**
> *"günün sonunda ne kadar ücret çıkarsa ona göre bir KDV oranı, her birisi
> için ayrı ayrı KDV oranları olmayacak"*

**Neden önemli:** ek hizmet/menü satırına ayrı oran kolonu AÇILMAYACAK. Şema
kalem bazlı oranı ifade edebilir hâle getirilirse, kimse istemediği hâlde
ileride iki farklı hesabın yan yana yaşadığı bir tablo doğar.

**`S-12` açık ucu — kademeli iadede komisyon TAM alınır.**
**Neden:** iptal maliyeti işletmede kalıyor; platform aracılık hizmetini
vermiş oluyor. `A-27` artık tahmin etmeden yazılabilir.

### Altyapı

**`S-19` — `KnownProxies` = `127.0.0.1`.** API ve Next **aynı makinede**
koşacak. **Neden yayın engelleyiciydi:** liste boşken uygulama Production'da
hiç açılmıyor; guard gevşetilseydi daha kötü olurdu — hız sınırı bütün
trafiği tek istemci sayardı.

**E-posta ve SMS — Postmark + Netgsm.** İkisi de açılış guard'ının beklediği
değerler; yapılandırma işi, kod değişmiyor.

**`S-24` — S3 ya da DigitalOcean Spaces, başlangıçta ücretsiz katman.**
Açık okuma **iki öneke**: `boat-media/*` ve `blog-media/*`.
⚠️ Tek önek yazılırsa blog kapakları üretimde **sessizce** kırılır — uygulama
tarafında hiçbir hata olmaz → 2026-09-04 (6).

**`A-41` — İYZİCO DEĞİL, PARATİKA.**
> *"Paratikaya geçelim onda pazar yeri özelliği vardı."*

**Neden:** İyzico hesabında pazaryeri özelliği açılamadı ve ölçüldü
(`POST /onboarding/submerchant` → `2000`). Paratika'yı eski sistem zaten
kullanıyordu, alt üye iş yeri desteği var.
**Bedeli:** `IyzicoPaymentProvider` çöpe gitmiyor ama **kullanılmayacak**;
`IPaymentProvider` arayüzü sağlayıcının yapılandırmadan seçilmesini zaten
sağlıyor, yani değişen tek şey yeni bir uygulama sınıfı → 2026-08-25 kararı
burada işe yarıyor.
⚠️ Sandbox'ta uçtan uca doğrulanan İyzico akışı artık **kanıt değil**;
Paratika için baştan ölçülmeli.

**`A-42` — belgeler BAŞVURUDA toplanacak ve IBAN ZORUNLU.**
**Neden:** alıcı kaydı açılamayan işletmelerin birikmesi, satışa açılamayan
işletme demek. Sürtünme artıyor, kabul edildi.

### Ürün

**`13` — front-end'deki 7 statik blog yazısı veritabanına GİRMEYECEK.**
Blog gerçek yazılarla sıfırdan dolacak. **Neden API'yi ilgilendiriyor:**
kategori adları o yazılardan türetilmeyecek; göç işi yok.

**`14` — reddedilen işletme başvurusu yeniden başvurabilir.**
**Neden not düşülüyor:** `TaxNumber` benzersiz, yani "yeniden başvuru" mevcut
kaydın yeniden açılması demek, ikinci satır değil. Ret ucu bunu bilerek
yazılmalı.

**`15` — yorum daveti tur BİTER BİTMEZ, hatırlatma AÇIK.**
Bugünkü 3 saatlik gecikme benim tahminimdi, kalkıyor.

**`S-28` — 10 kayıt DÜZELTİLSİN.** Yolcu listesi bayrağı teknenin bugünkü
anahtarına göre geriye dönük düzeltilecek.
**Neden ilkeye aykırı görünmesine rağmen:** "rezervasyon satın alma anının
fotoğrafıdır" kuralı, o fotoğrafın DOĞRU çekildiği varsayımına dayanıyor.
Burada fotoğraf hatalıydı (`A-74`); düzeltmek fotoğrafı değiştirmek değil,
hiç çekilmemiş olanı çekmek.

**`S-22` — `a04-*` tohum satırları SİLİNSİN**, bağlı test teknesi başka tipe
taşınsın.

**`A-07` — yanıt şeması HEPSİNE yazılacak.** 114 uç, mekanik iş.

**`S-18` — 10 mavi tur bölgesi ONAYLANDI.**

**`28` — 26 Ağustos'ta aldığım geçici kararların tamamı TOPLU ONAYLANDI**
→ [[api-benim-kararlarim]].

**`24` — testlerdeki iki ad değişikliği KALSIN**, demo aşaması.

**Veri göçü ERTELENDİ** — önce site ayağa kalkacak.

### Hâlâ cevapsız

**`S-25`** (biniş jetonu geri üretilebilir olsun mu) — Mert *"anlamadım"*
dedi, soru ürün diliyle yeniden soruluyor. `W-66` QR işi buna bağlı.
**`S-31`** (blog gövdesi düz metin mi zengin metin mi) — bugün açıldı.
**`G-13`** mali müşavir teyidi — henüz sorulmadı.

---

## 2026-09-04 (11) — `S-20`: KDV ORANI rezervasyona donduruluyor, tutar değil

**Karar:** `Reservations.VatRate numeric(5,2) NOT NULL`, kısıt `0..100`.
Değer `Quote` üzerinden akıyor — yani rezervasyona donan diğer beş para
alanıyla aynı yoldan. Vergi TUTARI saklanmıyor.

**Neden tutar değil oran:** tutar toplamdan türetilebiliyor
(`GrandTotalTry × VatRate / (100 + VatRate)` — fiyat KDV DAHİL, çünkü işletme
kendi fiyatını vergiyi içine katarak koyuyor → 2026-09-04 (10) `S-21`).
İkisini birden saklamak, yuvarlamada birinin diğerinden kaymasına açık kapı
bırakırdı ve o an hangisinin doğru olduğu belirsiz kalırdı.

**Neden dondurulması geri alınamaz bir iş:** oran devlet kararıyla değişiyor.
Kolon sonradan eklenseydi, eklendiği andan ÖNCEKİ her rezervasyonun o günkü
oranı **geriye dönük üretilemezdi** — tahmin edilerek okunurdu ve tahmin
hiçbir yerde görünmezdi.

**Oranın KAYNAĞI bugün yapılandırma** (`Billing:VatRate`), `TaxOptions` düz
sınıfı üzerinden. `Application` katmanının NuGet bağımsızlığı korunuyor —
`AppUrlOptions` ile aynı desen.
⚠️ **Kaynak sorusu AÇIK** → `S-32`: oran tarihli bir tabloya taşınmalı mı?
Taşınırsa değişen tek şey bu değerin nereden okunduğu; rezervasyondaki kolon
aynı kalıyor. Yani pahalı olan iş bugün yapıldı, ucuz olan ertelendi.

**Üretimde oran AÇIKÇA verilmek zorunda** (15. açılış kapısı). Geliştirmede
%20'ye düşüyor; üretimde de düşseydi, oranın değiştiği gün yapılandırmayı
güncellemeyi unutan bir dağıtım **kesilen her faturayı** yanlış oranla
üretirdi ve hiçbir hata çıkmazdı. Belirti aylar sonra mali müşavirden gelirdi
— ve oran rezervasyona dondurulduğu için yanlış satırlar kalıcı olurdu.
Kapı bildirim kapısından ÖNCE duruyor.

**`vatRate` müşteriye AÇIK dönüyor**, komisyon oranı gibi gizlenmiyor.
Ayrım: komisyon platform ile işletme arasındaki ticari şart, KDV devletin
ilan ettiği bir sayı ve fiyat KDV dahil ilan ediliyor — müşteri ödediğinin ne
kadarının vergi olduğunu görebilmeli.
`A_new_field_cannot_silently_widen_the_response` testi tam da amacına uygun
davranıp durdurdu ve soruyu sordurdu; cevap yazılıp listeye eklendi.

**Migration ELLE düzeltildi, üretilen hâliyle bırakılmadı:**
1. Varsayılan `0` yerine `20` — EF'in ürettiği sıfır mevcut her rezervasyonu
   "KDV'siz" damgalardı ve o satırlar kalıcı.
2. Varsayılan aynı işlemde `DROP DEFAULT` — kalıcı bir `DEFAULT` model ile
   veritabanını sessizce ayrıştırır → [[api-desenler]]
3. Kısıt `NOT VALID` + `VALIDATE` — EF'in düz `ADD CONSTRAINT`'i tüm satırları
   tararken ACCESS EXCLUSIVE tutuyor ve `Reservations` bu şemanın en sıcak
   tablosu.

**Kanıt:** dondurma satırı kaldırılarak mutasyon denendi, iki test kırmızıya
döndü. Canlı: fiyat sorgusunda `vatRate: 20`, komisyon sızmıyor, türetilen
vergi `1000 × 20/120 = 166.67`. Canlı rezervasyon `AZ6QSV9B` satırında
`VatRate = 20.00` dondu. Veritabanında `column_default` boş, kısıt
`convalidated = t`, 80 eski satır 20 ile dolduruldu.

---

## 2026-09-04 (12) — `S-28` ve `S-22`: iki veri düzeltmesi, ikisi de migration

**Karar:** İkisi de elle SQL değil **migration** olarak yazıldı.
**Neden:** elle çalıştırılan bir düzeltme hiçbir yerde kayıtlı olmaz; hangi
veritabanına uygulandığı, ne zaman ve neyi değiştirdiği yalnız o an bilinir.
Migration sürümlü, tekrarlanabilir ve gerekçesi kodun içinde.

### `S-28` — yolcu listesi bayrağı (`A-81`)

**Kapsam TARİHLE sınırlı**, koşulsuz değil. Düzeltmeden (`c33feed`,
2026-08-31 02:07:33 UTC) SONRA yazılan satırlar doğru ve bir teknenin bayrağı
meşru olarak değişmiş olabilir; tarihsiz bir güncelleme o meşru farkları da
sessizce ezerdi.
**Ölçüldü:** o andan sonra yazılmış ayrışık satır **sıfır** — yani `A-74`
gerçekten çalışıyor ve migration yalnız geçmişe dokunuyor.

⚠️ **Mert'e sorulan sayı 10'du, gerçek sayı 15.** Ters yönde 5 satır daha
vardı (rezervasyon `true`, tekne `false`): eski kural çok günlü turları
yanlışlıkla işaretliyordu. Soruyu ben tek yönü ölçerek yazmıştım. Kural
"teknenin bugünkü anahtarına göre düzelt" olduğu için ikisi de kapsamda;
tek yön düzeltilseydi ayrışıklık yerinde kalırdı.

### `S-22` — `a04-` tohum satırları (`A-82`)

⚠️ **"Temizlik" kelimesi işin küçüklüğünü ima ediyordu, ölçüm öyle olmadığını
gösterdi: bu satırlara 38 REZERVASYON bağlıydı.** Doğrudan silme yabancı
anahtara takılır ya da daha kötüsü, farklı bir sırayla veri götürürdü.

Sıra: önce TAŞI, sonra sil. Rezervasyonlar `RentalTypes`'a değil
`BoatRentalTypes`'a bağlı olduğu için satış biçiminin işaret ettiği kiralama
tipini değiştirmek rezervasyonlara dokunmuyor.

Hedefler **anlam olarak birebir eş** seçildi, benzer değil:

| Kaynak | Hedef | Neden bu |
|---|---|---|
| `a04-gulet` | `gulet` | aynı tip, çevirisi var |
| `a04-bodrum` | `bodrum` | aynı bölge |
| `a04-gunluk-tekne` | `gunluk-tekne` | `WithinDay` / `PerPerson` — birebir |
| `a04-konaklamali` | `konaklamali` | `MultiDay` / `PerBoat` — birebir |

Son ikisi kritik: `DurationKind` ve `PricingStrategy` fiyatın hangi alanlara
yazıldığını belirliyor. Farklı süre biçimindeki bir tipe taşımak, mevcut 38
rezervasyonun anlamını **sessizce** değiştirirdi.

`IX_BoatRentalTypes_BoatRental` benzersiz; taşınan teknenin hedef tiplere
sahip OLMADIĞI önceden ölçüldü. Olsaydı migration benzersizlik hatasıyla
düşerdi — sessiz bozulma değil.

**Kanıt:** uygulama öncesi 15 ayrışık rezervasyon / 4 `a04-` satırı / teknenin
38 rezervasyonu; sonrası **0 / 0 / 38**. Yani düzeltmeler yapıldı ve hiçbir
rezervasyon kaybolmadı. Canlı: arama sonucundaki tip adları yalnız `Gulet`,
`lookups` gövdesinde `a04-` geçmiyor.

**İkisinin de `Down()`'ı bilerek BOŞ.** Eski hatalı değerler hiçbir yerde
saklanmıyor; "önceki hâle dön" diye bir hâl yok. Yanlış bir düzeltme yapılırsa
çözüm geri almak değil, YENİ bir düzeltme migration'ı yazmaktır.

---

## 2026-09-04 (13) — `S-31`: blog gövdesi zengin metin, temizleme YAZMA yolunda

**Karar (Mert):** *"b olabilir ya da CKEditör de olabilir"* — seçim teknik
tarafa bırakıldı, web oturumu **CKEditor** seçti. Gerekçesi benim Markdown
önerimi çürüttü ve haklıydı: yazarlar tekne işletmecisi ve kaptan;
`**kalın**` yazmayı öğrenmek gerçek bir engel ve blogun amacı işletmeyi
yazmaya TEŞVİK etmek. Benim "temizleme yüzeyi en dar olan" gerekçem
geliştiriciyi koruyordu, kullanıcıyı değil.

**Uygulama:** `HtmlSanitizer` (paket `HtmlSanitizer` 9.2.1039, ad alanı
`Ganss.Xss`) `Infrastructure`'a eklendi. Arayüz `IHtmlContentSanitizer`
`Application`'da — o katman hiçbir NuGet paketine bağlı değil, `IImageProcessor`
ile aynı ayrım.

**Temizleme YAZMA yolunda, okuma yolunda DEĞİL.** Okumada temizlenseydi
veritabanında kirli metin durur ve yarın başka bir istemci (mobil, e-posta
özeti, dışa aktarma) onu ham basardı. Kirli veriyi hiç saklamamak, her
okuyucunun temizlemeyi hatırlamasını ummaktan güvenli.
**Kanıt:** canlıda gönderilen betik veritabanı satırında da yok.

**Politika izin listesi, yasak listesi DEĞİL.** Yasak listesi "aklıma gelen
tehlikeli şeyler" demektir ve aklına gelmeyen her şey geçer. Kütüphanenin
varsayılan listeleri önce BOŞALTILIYOR — boşaltılmasaydı bizim listemiz
varsayılana EKLENİR ve "yalnız şunlar" niyeti sessizce "şunlar da" olurdu.
**Kanıt:** boşaltma satırı kaldırılınca üç test kırmızıya döndü.

**Neden burası tek savunma hattı:** yazıyı platform onaylıyor ama onaylayan
kişi METNE bakıyor, kaynak koda değil. Onay bir `script` etiketini yakalamaz.

### Ölçerek öğrenilen iki şey — ikisi de kütüphane varsayımıydı

**1. Boş izin listesi metni de siliyor.** Başlık ve özetten etiketleri düşürmek
için boş listeli ikinci bir temizleyici kuruldu; `<h1>Gökova</h1>` tamamen
kayboldu. Yani "etiketi düşür" niyeti "yazıyı da sil" olarak çalışıyordu.
Çözüm `KeepChildNodes = true`.
Test yazılmasaydı bütün başlıklar sessizce boşalır ve doğrulama "başlık boş
olamaz" derdi — belirti, yazarın hiçbir başlığı kaydedememesi olurdu.

**2. Betik gövdesi başlıkta düz metne dönüyor.** `<script>alert(1)</script>`
bir başlıkta `alert(1)` olarak kalıyor. Bunu engellemek için başlığı önce
zengin temizleyiciden geçirmek denendi ve o yol `<h1>` içindeki gerçek
başlığı da siliyordu — düzeltme, çözdüğünden büyüğünü bozuyordu.
**Kalan durum kabul edildi ve TESTE YAZILDI:** başlık düz metin olarak
saklanıp kaçışlanarak gösteriliyor, hiçbir yerde HTML basılmıyor. Saçma bir
başlık, kaybolan bir başlıktan iyidir. Test bu gerçeği yazıyor çünkü
yazılmazsa bir sonraki okuyan kişi bunu hata sanıp "düzeltir" ve başlıkları
yeniden kaybeder.

**Kanıt (canlı, uçtan uca):** gönderilen gövde
`<h2>` + `<strong>` + `<script>` + `onclick` + `javascript:` bağlantı +
`<iframe>` + `<style>` içeriyordu. Saklanan hâli:
`<h2>Koylar</h2><p><strong>Kalın</strong> metin</p><p>tıkla</p><a>kötü</a><a href="https://ornek.test">iyi</a>`
— tehlikeli olanların hepsi düştü, biçimlendirme ve geçerli bağlantı kaldı.
Başlık `<h1>Gökova</h1> rehberi` → `Gökova rehberi`.

---

## 2026-09-04 (14) — `S-25`: ayrı biniş bileti, asıl jetona dokunulmuyor

**Karar (Mert):** (b) — biniş belgesi açıldığında **ayrı, süreli bir bilet**
üretilir. Rezervasyonun asıl biniş jetonu olduğu gibi kalır.

**Neden (a) elendi:** jetonun düz metnini saklamak belgeyi her zaman yeniden
bastırırdı ama veritabanını gören herkes başkasının biniş anahtarını okurdu.

**Ne yapıldı:** `BoardingTickets` tablosu — `ReservationId`, `TokenSha256`,
`IssuedAt`, `ExpiresAt`, `RevokedAt`. Uç:
`POST /api/reservations/{code}/boarding-ticket`, gövdesi ve kimlik teyidi
sorgulama ucuyla **aynı**. İkinci bir kimlik yolu yazılmadı — yazılsaydı
birinin sıkılaştırılması diğerini açık bırakırdı.

**Karekod GÖRSELİ değil taşıyacağı METİN dönüyor.** Görsel üretmek sunucuya
çizim kütüphanesi ve depolama sorusu getirirdi; arayüz karekodu zaten çiziyor.
Ayrıca metin, karekod okunamadığında elle girilebilecek tek şey.

**Yeni bilet eskisini İPTAL EDER** ve kural veritabanında: `RevokedAt IS NULL`
koşullu benzersiz indeks, rezervasyon başına tek geçerli bilet bırakıyor.
Uygulama kodunda kalsaydı iptali unutan bir yazma yolu iki geçerli bilet
bırakırdı ve bu hiçbir yerde hata üretmezdi. "Telefonumu kaybettim" isteğinin
asıl karşılığı bu.

**Ömür kalkıştan 12 saat sonrası**, tur bitişi DEĞİL — Mert'e ilettiğim uyarı
karara girdi. Bitişte ölen bilet, geç kalkan ya da uzayan turda kaptanın
elinde ölür ve o an kimse destek hattı arayacak durumda olmaz. Sayı ölçülmüş
değil seçilmiş; tek sabit, değiştirmesi ucuz.

**Okutma İKİ jetonu da tanıyor:** asıl jeton ve geçerli bilet. Bilet asıl
jetonun yerine geçmiyor, yanına ekleniyor — yoksa bilet basılmamış eski
rezervasyonların hepsi sessizce okutulamaz hâle gelirdi.

**Ödenmemiş rezervasyona bilet verilmiyor:** koltuklar tutmada ve süre dolunca
serbest bırakılıyor; verilseydi müşteri birazdan kaybolacak bir rezervasyonun
belgesini eline alırdı.

### ⚠️ Testlerimden biri doğru sonucu YANLIŞ SEBEPTEN veriyordu

Süre testini önce "biletin bitişinden sonra okut" diye kurmuştum. O anda tur
da bitmiş oluyor, yani okutma zaten başka bir sebeple reddediliyordu — süre
şartı koddan tamamen çıkarıldığında **test yeşil kalıyordu.**

Mutasyon bunu yakaladı. Kurulum tersine çevrildi: biletin bitişi geçmişe
çekiliyor ve okutma her şeyin geçerli olduğu normal anda deneniyor, yani tek
değişken biletin süresi. Yanına olumlu ikizi de yazıldı.

**Kanıt:** iki mutasyon, ikisi de yakalandı — iptal satırı kaldırıldı (2
kırmızı), süre şartı kaldırıldı (1 kırmızı, düzeltilmiş testle).
**Kanıt (canlı):** yanlış e-posta `400 "Rezervasyon bulunamadı."`; doğru
e-posta jeton + `expiresAt` döndürdü; ikinci bilet basıldığında veritabanında
**2 bilet, 1 geçerli**.

---

## 2026-09-05 — İade önizlemesi: yeni alan, ve hesap TEK yerde

**Karar:** Sorgulama ve liste yanıtlarına `refundPreviewRate` /
`refundPreviewTry` eklendi — yalnız **iptal edilebilir** rezervasyonda dolu.

**Neden mevcut alanlar doldurulmadı:** `cancellationRefundRate` ve
`refundDueTry` bir KAYIT — *"iptal edilirken şu oran uygulandı"* — ve yalnız
iptal edilmiş satırda dolu. Önizleme bir TAHMİN. Aynı ada iki anlam yüklemek,
okuyanın hangisini gördüğünü satırdan satıra değiştirirdi.

**Bulguyu web oturumu getirdi ve kendi varsayımını düzelterek getirdi:** o iki
alanı önizleme sanıp ekrana bağlamaya başlamış, ölçünce kayıt olduklarını
görmüş. Bugün müşteri, geri alınamaz bir işlemi sonucunu görmeden onaylıyordu
ve `S-12` ile birlikte bunun somut bedeli var: kalkışa 24 saatten az kala
**iade sıfır**.

**Hesap `RefundPolicy` içine ÇIKARILDI ve iptal ucu da oradan çağırıyor.**
Kritik olan kuralın kendisi değil tekliği: iki kopya olsaydı biri ekranda
gösterilir diğeri iptalde uygulanırdı ve ayrıştıklarında **ikisi de kendi
kodunda doğru** görünürdü. Müşteri ekranda %50 görüp hesabına %0 geçtiğinde
bunu kimse hata olarak göremezdi.

**Önizleme SQL'de değil bellekte hesaplanıyor:** SQL'e taşınsaydı kademe
eşikleri ikinci bir yerde daha yazılır ve politika değiştiğinde biri sessizce
eskide kalırdı.

**Yalnız `CanCancel` doğruyken dolduruluyor.** Her satırda doldurulsaydı,
iptal edilemeyen bir rezervasyonda "iade edilecek tutar" gibi okunan bir sayı
dururdu ve müşteri onu bir vaat sanardı.

**Kanıt:** mutasyon — önizleme yanıta bağlanmayınca test kırmızıya döndü.
Sınır anları ayrı ayrı ölçüldü (72/48/47.99/24/23.99/0/−1 saat); tam 48:00 ve
tam 24:00 müşteri lehine üst kademede.
**Kanıt (canlı):** `canCancel: true`, `refundPreviewRate: 100`,
`refundPreviewTry: 1500.0`, `cancellationRefundRate: null` — tahmin dolu,
kayıt boş.

---

## 2026-09-05 (2) — `S-32`: KDV oranı tarihli tabloya taşındı

**Karar (Mert):** oranın kaynağı yapılandırma değil **tarihli tablo** olsun.

**Neden:** yapılandırmadaki tek bir sayı, oranın NE ZAMAN değiştiğini ifade
edemiyor. Devlet oranı bir tarihten geçerli olmak üzere değiştiriyor; tek
alanlı bir kaynakta yeni oranı ancak o gün, elle ve dağıtımla yazmak mümkün
ve yazmayı unutan bir sabah bütün faturalar eski oranla kesiliyor. Tarihli
tabloda değişiklik önceden girilebiliyor ve kimsenin o sabah bir şey
yapmasına gerek kalmıyor.

**Ne yapıldı:** `TaxRates` (`Rate`, `EffectiveFrom`, `Note`, `CreatedAt`).
Yürürlükteki oran, `EffectiveFrom` şu andan küçük ya da eşit satırların **en
yenisi**. `TaxOptions` düz sınıfı, DI kaydı, `Billing:VatRate` yapılandırması
ve 15. açılış kapısı **kaldırıldı** — hepsi tek bir tabloyla değişti.

**Kazanç, "yapılandırma yerine tablo"dan büyük:** ileri tarihli bir satır
bugünden girilebiliyor ve tarihi gelene kadar hiçbir etkisi olmuyor. Oranın
1 Ocak'ta değişeceğini bilmek artık işe yarıyor; önceki hâlde yeni oranı
ancak o gün, elle, dağıtımla yazmak mümkündü ve yazmayı unutan bir sabah
bütün faturaları eski oranla keserdi.

**Oran `PricingContext` üzerinden taşınıyor**, komisyon oranıyla aynı
sorgudan. Ayrı bir yoldan gelseydi bir gün biri güncellenip diğeri
unutulurdu. `PricingService` artık vergi için hiçbir bağımlılık almıyor.

**Tohum satırı migration'ın PARÇASI.** Yürürlükteki oran bulunamazsa hesap
sıfır oran taşır; boş bir tablo bütün satışı sessizce vergisiz yapardı.
Satır `2000-01-01`'den geçerli, yani mevcut rezervasyonların kesildiği dönemi
de kapsıyor. Değer %20 — kaldırılan yapılandırmanın taşıdığı değerin aynısı,
yani bu migration onu **devralıyor**.

**`EffectiveFrom` benzersiz.** Aynı ana iki oran yazılabilseydi "o an hangi
oran yürürlükteydi" sorusunun cevabı sorgunun sıralamasına kalırdı ve iki
farklı kod yolu iki farklı cevap verebilirdi.

**Kaldırılan açılış kapısı yerine ne kondu:** hiçbir şey — ve bu bilinçli.
Kapının işi "oran yapılandırmada tanımsız kalmasın"dı; artık oran
yapılandırmada değil ve tablo migration'la doluyor. Kapı korunsaydı, olmayan
bir ayarın varlığını kontrol ediyor olurdu.
⚠️ İkisinin de yakalamadığı şey aynı: **YANLIŞ** bir oran. Onu ne kapı ne
tablo görür; gören tek şey mali müşavir teyididir (`G-13`).

**Kanıt:** mutasyon — yürürlük tarihi şartı kaldırılınca
`Ileri_tarihli_oran_tarihi_gelene_kadar_etkisiz` kırmızıya döndü.
**Kanıt (canlı):** fiyat sorgusu `vatRate: 20.0`, tabloda tek satır
(`2000-01-01`, devralınan not). **573 test yeşil.**

### ⚠️ Testim paylaşılan veritabanında başka testin satırını taşıdı

İleri tarihli oranı geçmişe çekerken `Where(t => t.Rate == 21m)` yazmıştım.
Testler aynı veritabanını paylaşıyor ve başka bir test de %21 yazıyordu; sorgu
onun satırını da taşıdı ve benzersizlik kısıtı patladı.

Ders `A-78`'deki ile aynı ailede: **paylaşılan veritabanında bir satırı
ÖZELLİĞİNE göre bulmak, başkasının satırını bulmaktır.** Kimlikle bulunmalı.
Bu hafta iki kez oldu — ilkinde sabit e-posta, ikincisinde oran.

---

## 2026-09-05 (3) — Slug üretiminde noktalı `İ` kusuru

**Karar:** `Slugify` iki katmanlı düzeltildi ve mevcut bozuk adres
yönlendirmeyle korunarak küçültüldü (`A-87`).

**Neden — kusur sessizdi.** `ToLowerInvariant()` noktalı büyük `İ`'yi
(U+0130) **küçültmüyor**, değişmeden bırakıyor. Ardından gelen `FormD`
ayrıştırması onu `I` + birleşen noktaya bölüyor, nokta atılıyor ve geriye
**BÜYÜK `I`** kalıyor. "Akdeniz İncisi" teknesi `akdeniz-Incisi` adresini
almıştı:

    /api/boats/akdeniz-Incisi  -> 200
    /api/boats/akdeniz-incisi  -> 404   <- insanın yazacağı hâl

Hiçbir yerde hata yok; yalnız paylaşılan bağlantı ölü. Bulguyu web oturumu
getirdi.

**İki katman, ve ikincisi asıl olan:**
1. Büyük Türkçe harfler küçültmeden ÖNCE açık listeye eklendi.
2. ASCII harf eklenirken **her zaman küçültülüyor**.

Birincisi yalnız bilinen harfleri kapatır. İkincisi, ayrıştırmadan büyük
ASCII harf çıkaran **bütün** durumları kapatır — hangileri olduğunu
bilmesek de. Tek bir harfi düzeltmek, sınıfı açık bırakmak olurdu.

**Test de KURALI tutuyor, harfi değil:** `A_generated_slug_never_contains_an_uppercase_letter`
üretilen adresin tamamen küçük harf olduğunu doğruluyor.

### ⚠️ Mutasyon ölçümünde kendi hatam

İki katmanı **ayrı ayrı** kaldırdım ve ikisinde de test yeşil kaldı; "testim
yolu geçmiyor" diye düşündüm. Gerçek sebep başkaydı: her katman diğerini
örtüyordu. Kusuru üretmek için **ikisini birlikte** kaldırmak gerekiyordu ve
öyle yapınca iki test de kırmızıya döndü.

Ders: **savunması katmanlı bir kodda mutasyon tek katmanı kaldırarak
ölçülemez.** Tek katman kaldırıldığında yeşil kalan test, "test boş" demek
değil; "diğer katman çalışıyor" demek olabilir. Ayrımı yapmanın tek yolu
kusuru gerçekten üretmek.

### ⚠️ Yönlendirme ilk yazımda SESSİZCE yazılmadı

Migration'ı `BoatSlugs` üzerinden yazmıştım — o tablo yalnız tekne YENİDEN
ADLANDIRILDIĞINDA doluyor, kuruluşta değil. Kaynak yanlış olduğu için hiçbir
satır bulunmadı ve yönlendirme **sessizce** yazılmadı; migration başarıyla
tamamlandı. Ölçtüğümde `BoatSlugs` boştu.

Düzeltildi: kaynak `Boats` oldu. Ders yine aynı — **varsayımı ölçmeden
yazmak.** Bu kez varsayım "her teknenin bir slug geçmişi vardır" idi.

**Kanıt (canlı):** `akdeniz-incisi` → `200`; `akdeniz-Incisi` → **`301`**,
`Location: /api/boats/akdeniz-incisi`, izlenince `200`. Yeni tekne
"İZMİR Ünlü Çağrı Deneme" → `izmir-unlu-cagri-deneme`.
**575 test yeşil.**

**Blog etkilenmiyor:** blog kısa adı kullanıcıdan geliyor ve doğrulama
büyük harfi **reddediyor** (`400 InvalidSlug`), sessizce bozmuyor. Canlı
ölçüldü: `İzmir-rehberi` → *"Kısa ad yalnız küçük harf, rakam ve tire
içerebilir."*

---

## 2026-09-05 (4) — Kuponlar: üç tür, üç ayrı mekanizma

**Karar (Mert, soru 61):** üç kupon türü olacak — kullandığım kuponlar, bana
özel kuponlar, sitede listelenen genel kampanyalar.

**Neden `Coupons.UserId` EKLENMEDİ:** kolon konsaydı aynı tablo iki anlam
taşırdı — boş kolon "herkese açık kampanya", dolu kolon "kişiye özel". Kupon
denetimi yazan her yeni kod yolu bu ayrımı hatırlamak zorunda kalır ve unutan
biri kişisel kuponu herkese açar; hata sessizdir, kimse şikâyet etmez.
Ayrı tablonun ikinci kazancı: bir kupon **birden çok** kişiye tanımlanabiliyor.
Kolonla "on kişiye özel kampanya" için on ayrı kupon üretmek gerekirdi.

| Tür | Mekanizma | Uç |
|---|---|---|
| Kullandıklarım | `CouponRedemptions` → rezervasyon → kullanıcı | `GET /api/coupons/mine` |
| Bana özel | `CouponAssignments` (yeni tablo) | `GET /api/coupons/mine` |
| Genel kampanya | `Coupons.IsPubliclyListed` (yeni kolon) | `GET /api/coupons` |

**"Kodu bilene açık" dördüncü bir tür zaten vardı** ve dokunulmadı: ne
listelenen ne tanımlı olan kupon. Amacı görünmemek.

### Tanım FİYAT HESABINDA uygulanıyor

Yeni red sebebi `CouponRejection.NotYours`. Tanımı olan kuponu yalnız tanımlı
kullanıcılar kullanabiliyor; **giriş yapmamış çağıran da reddediliyor** —
kimin olduğu bilinmeden "senin" denemez.

Ayrı bir "önce giriş yap" sebebi AÇILMADI: açılsaydı, bir kodun kişiye özel
olduğu bilgisi kimliksiz istekle öğrenilebilirdi.

⚠️ Bu, `QuoteAsync`'e **çağıranın kimliğini** eklemeyi gerektirdi
(`QuoteAsync(request, userId, ct)`, 36 çağrı yeri). İsteğe koymak mümkün
değildi: istemciden gelen kimlik kimlik değildir.

**Doğrulama hesap anında, yalnız rezervasyonda değil.** Yalnız rezervasyonda
denetlenseydi müşteri fiyat ekranında indirimi görür, ödeme adımında
reddedilirdi — "huninin sonunda düşen müşteri" → [[api-desenler]]

### Son tanım kaldırılınca kupon PASİFE alınıyor

Tanımı olmayan kupon kısıtsızdır. Bu kural olmasaydı kişiye özel bir kupon,
tanımları silinince **sessizce** herkesin kullanabileceği bir kupona
dönüşürdü.

### Listelenen kupona kişi tanımlanamıyor

İkisi bir arada olsaydı kupon hem sitede herkese görünür hem yalnız tanımlı
kişiler kullanabilir olurdu: müşteri kodu ekranda görüp reddedilirdi ve sebebi
hiçbir yerde yazmazdı. Aynı sebeple tanımlı kuponlar herkese açık listeden de
**çıkarılıyor** — "listelensin" işareti taşısalar bile.

### Yönetim yanıtı ayrı tip

`Coupon` varlığı döndürülmedi: tanımların arkasındaki kullanıcı nesneleri,
oluşturanın kimliği ve ileride eklenecek her alan kendiliğinden dışarı
çıkardı → [[api-desenler]] "İç hesap nesnesi HTTP yanıtı değildir".
Kullanım hakkı sayısı herkese açık listede YOK: "son 3 hak kaldı" platformun
iç sayacını dışarı verirdi.

**`coupon.read` / `coupon.write` katalogda 2026-08-24'ten beri duruyordu ve
hiçbir uç kullanmıyordu** — verilebilen ama hiçbir şey açmayan iki yetki daha.
İkisi de `IsPartnerAssignable = false`, yani duvar katalogda.

**Kanıt:** iki mutasyon, ikisi de yakalandı — tanım denetimi kaldırıldı
(1 kırmızı), son tanımda pasife alma kaldırıldı (1 kırmızı).
**Kanıt (canlı):** `AYSEYE20` kuponu → Ayşe `indirim 580`, Can
`0 + "size tanımlı değil"`, kimliksiz `0 + aynı mesaj`. Herkese açık listede
yalnız `YAZ2026` görünüyor, `AYSEYE20` yok. **581 test yeşil.**

⚠️ **Açık kalan:** `Coupon.PartnerId` ve `FundedBy = Partner` var, yani
işletmenin karşıladığı kupon şemada ifade edilebiliyor — ama `coupon.write`
işletmeye verilemiyor, yani işletme kendi kuponunu **yönetemiyor**. Bugün
kuponu platform açıyor. Tutarsızlık gerçek; Mert'e sorulacak.

## 2026-09-05 (5) — İşletme kendi kuponunu kendisi açar; `FundedBy` isteğe ASLA girmez

`A-89`. Mert **(a)** dedi: *"işletme kendi kampanyasını kendisi açabilecek."*
`coupon.read` / `coupon.write` artık `IsPartnerAssignable = true`; migration
yetkileri **mevcut sahip rollerine geri doldurdu** (20 rol), çünkü sahip rolü
verilebilir yetkileri yalnız **rol oluşturma anında** alıyor — yeni yetki eski
rollere kendiliğinden inmiyor → [[api-desenler]].

Uçlar `api/partner/coupons` altında ayrı bir controller'da; platform ucu
(`api/admin/coupons`) olduğu gibi kaldı. **İki ucun sözleşmesi kasıtlı olarak
farklı:** `SavePartnerCouponRequest` üç alanı **taşımıyor** — `FundedBy`,
`PartnerId`, `IsPubliclyListed`.

**Neden:** bir yetkiyi açmak, o yetkinin kapsamını da açmak demek değildir.
İşletme isteğinde `FundedBy` seçilebilseydi işletme kendi kuponunun bedelini
`Platform` yazabilirdi — ve bu **sessiz** bir zarar: kupon çalışır, indirim
uygulanır, hata dönmez, fark yalnız ay sonu hakedişinde ortaya çıkar. Aynı
biçimde `PartnerId` istekten gelseydi işletme **başkasının teknesine** kupon
açabilirdi. Üçü de sunucuda sabitlendi: `FundedBy = Partner`, `PartnerId =`
jetondaki işletme, `IsPubliclyListed = false`. Tekne verilirse teknenin o
işletmeye ait olduğu ayrıca doğrulanıyor.

`IsPubliclyListed = false` sabiti bir **kısıt değil, varsayılan** — herkese açık
kampanya vitrini bugün platformun editoryal alanı. İşletme oraya kendi kuponunu
koyabilmeli mi, ayrı bir karar → `S-33`.

**Kanıt (mutasyon):** üçü de yakalandı — `FundedBy` → `Platform` (2 kırmızı),
tekne sahipliği denetimi kaldırıldı (1 kırmızı), pasife almadan işletme kapsamı
kaldırıldı (1 kırmızı).
**Kanıt (canlı):** Mavi Yolculuk kendi jetonuyla `MAVI10` açtı → `201`, kendi
listesinde `bedel=Partner listelenen=False kullanim=0`; herkese açık
`/api/coupons` listesinde yalnız `YAZ2026` var, `MAVI10` sızmıyor.
**Kanıt (migration):** `coupon.read`/`coupon.write` → `IsPartnerAssignable = t`;
`coupon.write` tutan rol sayısı **20**. **586 test yeşil.**

## 2026-09-05 (6) — `KnownProxies` dolu olması doğru olduğu anlamına gelmiyor: IPv6 loopback tuzağı

Üretim kapısı `ForwardedHeaders:KnownProxies` **boş mu** diye bakıyor. Boş
değilse geçiyor. Ama vekil aynı makinedeyse bağlantı çoğu kurulumda `::1`
üzerinden geliyor ve listede yalnız `127.0.0.1` yazıyorsa ASP.NET Core başlığı
**sessizce yok sayıyor** — hata yok, günlük yok, sadece bütün istekler tek IP'ye
düşüyor.

**Neden önemli:** hız sınırı ve `EventLogs.IpHash` istemciyi IP'den ayırıyor.
Bütün trafik tek IP görünürse `hesap` kovası (15 dakikada 10) **tüm kullanıcılar
için ortak** olur; bir kişinin başarısız denemeleri herkesi kilitler. Kapı bunu
yakalamaz çünkü liste dolu.

**Kanıt (ölçüm, 2026-09-05):** aynı API'ye iki farklı `X-Forwarded-For`
(`198.51.100.1`, `198.51.100.2`) ile başarısız giriş atıldı.
`KnownProxies = 127.0.0.1` iken `EventLogs` iki satıra **aynı** `IpHash`
(`45f986b7ce1e`) yazdı. Listeye `::1` eklenince aynı deneme **iki farklı** özet
verdi (`61a9986e0195`, `bba4a18638c0`). Kapının hata metni bu ölçümle genişletildi.

Yani `S-19`'un cevabı (*"vekil aynı makinede, 127.0.0.1"*) **eksik**: üretimde
`KnownProxies` **hem `127.0.0.1` hem `::1`** içermeli. Aynı tuzak SMTP
sunucusunda da yaşanmıştı → [[api-notlar]].

## 2026-09-05 (7) — Gövdedeki tarih UTC'ye ÇEVRİLİR, saat dilimsiz tarih REDDEDİLİR

`A-90`. Web oturumu ölçtü: `POST /api/partner/coupons` `"2026-09-05"` ve
`"2026-09-05T00:00:00+03:00"` gövdelerinde **`500`** dönüyordu, yalnız
`"...Z"` `201` veriyordu. Kök neden Npgsql:

> `Cannot write DateTimeOffset with Offset=03:00:00 to PostgreSQL type
> 'timestamp with time zone', only offset 0 (UTC) is supported.`

Yani sözleşmeye uyan bir istek model bağlamayı geçiyor, doğrulamayı geçiyor
ve **veritabanına yazarken** patlıyordu. `500` "sunucuda beklenmeyen bir şey
oldu" demek; oysa olan şey beklenmedik değildi.

Çözüm tek noktada: `UtcDateTimeOffsetConverter` bütün controller'lara
kayıtlı. İki davranışı var ve ikisi ayrı kararlar:

1. **Ofsetli değer kabul edilir, UTC'ye çevrilir.** `00:00+03:00` →
   `21:00Z` (önceki gün). Bilgi kaybı yok: kolon zaten yalnız ANI saklıyor.
   İstemcinin saat dilimi bilmesi gerekmiyor.
2. **Saat dilimi taşımayan değer `400` ile reddedilir.** `"2026-09-07"` ya da
   `"2026-09-07T00:00:00"` kabul EDİLMİYOR.

**Neden ikincisi — tahmin etmek reddetmekten pahalı:** .NET saat dilimsiz
değeri SUNUCUNUN yerel saatiyle yorumluyor. Aynı istek, sunucu UTC'deyken
7 Eylül'ü, Türkiye saatindeyken 6 Eylül'ü kaydeder. Hata yok, günlük yok,
yalnız yanlış gün. Kabul etmek `500`'ü `200`'e çevirirdi ama kusuru
görünmezden gelinene dönüştürürdü. Mesaj da düzeltmeyi söylüyor:
*"sonuna 'Z' ya da '+03:00' ekleyin"* ve `$.validFrom` alanına bağlanıyor.

Ayrım ham METİNDEN yapılıyor, ayrıştırılmış değerden değil: .NET saat
dilimsiz değere sunucunun ofsetini koyduğu için ayrıştırılmış değer her
zaman bir ofset taşır. `-` araması `T` ayıracından sonra yapılıyor, tarih
kısmındaki tirelerle karışmasın diye.

**Etki alanı ölçüldü:** gövdesinde `DateTimeOffset` taşıyan **yalnız iki**
istek tipi var (`SaveCouponRequest`, `SavePartnerCouponRequest`). Rezervasyon
`DateOnly` alıyor, müsaitlik sorgu dizesinden `DateOnly` alıyor — ikisi de bu
yoldan geçmiyor.

**Kanıt (canlı):** `+03:00` → `201` ve veritabanında `2026-09-06 21:00 UTC`;
`Z` → `201`; `"2026-09-07"` → `400` + mesaj; `"2026-09-07T00:00:00"` → `400`.
`/api/search`, `/api/lookups`, `/api/coupons`, `{slug}/availability` `200`.
**Kanıt (mutasyon):** üçü de yakalandı — `ToUniversalTime()` kaldırıldı
(1 kırmızı), saat dilimi şartı kaldırıldı (1 kırmızı), dönüştürücü
`Program.cs`'ten çıkarıldı (2 kırmızı). **589 test yeşil.**

## 2026-09-05 (8) — `S-23` bayattı: uçlar vardı, ATAMA yoktu

Not *"tekne detayında donanım/kural ataması yok, aramada `AmenityIds`
süzgeci yok"* diyordu. Ölçüm ikisini de yalanladı: kayıt gövdesi
`amenityIds` ve `rules` alıyor, depo yazıyor, müşteriye açık detay çeviriyle
birlikte döndürüyor, `SearchRepository` **VE** anlamlı süzgeç uyguluyor.

Eksik olan **veriydi**: katalogda 9 donanım, 3 kural vardı ve **yayındaki
sekiz teknenin hiçbirinde tek atama yoktu.** Sonuç kullanıcıya kusur olarak
görünürdü — donanım bölümü boş, "klimalı tekneler" süzgeci her seçimde sıfır
sonuç. Hata yok, boş sonuç var.

**Neden buraya yazılıyor:** bu, bu projede tekrarlayan sınıfın veri
tarafındaki hâli — *yazılmış ama hiç uygulanmamış kontrol*'ün ikizi:
**yazılmış ama hiç beslenmemiş yol.** Kod incelemesi bunu bulamaz; yalnız
ürünü çalıştırmak bulur.

Ayrıca **ilk ölçümüm yanlıştı**: donanımı olan tekneyi seçip detayında
`amenities` alanını göremeyince "uç döndürmüyor" sandım. Gerçekte o tekne
YAYINDA DEĞİLDİ ve dönen gövde `{"error": ...}` idi — yani doğru cevabı
yanlış sebeple okudum. Ölçümün kendisi de kontrol edilmek zorunda
→ [[api-desenler]] "Yorumun iddiası da ölçülmek zorunda".

**Kanıt (canlı):** sekiz tekneye ayrışan donanım atandı; arama süzgeci
8 → klima 6 → şnorkel 4 → mikrofon 1, `klima+şnorkel` 3, `klima+mikrofon+wifi`
1 döndü. Akdeniz İncisi detayında 7 donanım, 3 kural (`Evcil hayvan` yasak,
`Sigara` serbest) çeviriyle geldi.
**Kanıt (mutasyon):** detay projeksiyonunda donanım listesi boşaltıldı
(1 kırmızı), kural `IsAllowed` sabitlendi (1 kırmızı).

## 2026-09-05 (9) — Yanıt şemaları: iddia eden değil, DERLENEN sözleşme

`A-07`. Başlangıç durumu ölçüldü: **146 operasyonun 146'sı** belgede yalnız
**şemasız bir `200`** bildiriyordu. Belge dolu görünüyordu ama hiçbir şey
söylemiyordu — ne gerçek durum kodunu (`201`, `204`, `404` hiç yoktu) ne de
gövde tipini. Web oturumu bu yüzden yanıt tiplerini elle yazıyordu ve bir
oturumda **üçü gerçekten yanlış çıktı** (blog liste satırı, iade oranı,
favori kartı); üçünü de tarayıcı yakaladı, derleyici değil.

Üç ayrı iş yapıldı ve sıraları önemliydi:

**1. Anonim gövdeler isimlendirildi.** 24 uç `Ok(new { ... })` döndürüyordu.
İsimsiz nesnenin OpenAPI'de adı olmaz. `ApiError`, `IdResponse`,
`IdsResponse`, `HealthResponse`, `JobHealthResponse`, `JobRunSummary`,
`AccountDeletionResponse`, `OfferAcceptedResponse`, `PaymentStartResponse`,
`PaymentCallbackResponse`, `RefundResponse`, `PayeeRegistrationResponse`,
`ReviewPageResponse`, `TicketCreatedResponse` yazıldı ve uçlar **bu tipleri
döndürecek şekilde değiştirildi**.

**Neden yalnız işaretlemek yetmedi:** `ProducesResponseType` bir İDDİADIR.
Kod isimsiz nesne döndürmeye devam etseydi belge bir şekli anlatır, uç başka
bir şey döndürürdü ve ikisi ayrıştığında hiçbir şey kırılmazdı. Tip
döndürülünce **derleyici** sözleşmeyi tutuyor. Alan adları birebir korundu,
JSON değişmedi (canlı doğrulandı).

**2. İşaretler eklendi** — 146 eylemin tamamına, gerçek kodlarıyla.

**3. Ölçüm iki kusur buldu ve ikisi de "eksik iddia"ydı.**
`POST /api/partner/coupons` yalnız `201` bildiriyordu ama canlıda `400`
dönüyordu: 14 controller hataları ortak bir `ExecuteAsync` yardımcısında
yakalıyor ve kodu üreten satır eylemin gövdesinde GÖRÜNMÜYOR. Yardımcının
ürettiği kodlar 66 eyleme eklendi. Aynı biçimde `[Authorize]` /
`[HasPermission]` taşıyan 113 eyleme `401` / `403` eklendi — kimliksiz istek
canlıda `401` dönüyor, belge bunu hiç söylemiyordu.

**Aşırı iddia da denetlendi:** kimliksiz uçlarda (`/api/search`,
`/api/lookups`, `/api/boats/{slug}`, `/api/coupons`, `/api/blog`,
`/api/health`, `/api/pricing/quote`) `401` iddiası OLMADIĞI ayrıca ölçüldü.
Yanlış yönde bir şema, eksik şemadan daha zararlı olurdu.

**Kural denetleniyor, yazılı kalmıyor:** `OpenApiDocumentTests`'e iki test
eklendi — her eylem bir yanıt tipi bildiriyor mu, her başarı yanıtı ya şema
taşıyor ya gövdesiz mi. İkincisi yazıldığı anda **beş gerçek boşluk** buldu:
dört belge indirme ucu (`File(...)` — `application/octet-stream` olarak
bildirildi) ve `POST /api/reservations` (`CreateReservationResult`).

`HealthController` rotası `api/[controller]` idi ve belgede `/api/Health`
diye çıkıyordu; `api/health` olarak sabitlendi — yönlendirme büyük/küçük
harfe duyarsız olduğu için çalışıyordu ama belge tek başına okunduğunda
tutarsızdı.

**Kanıt (öncesi/sonrası):** şema taşıyan operasyon **0 → 145/146**; bileşen
şeması **0 → 181**; bildirilen kodlar `{200:146}` → `{200:88, 201:16,
204:42, 301:1, 400:120, 401:120, 403:91, 404:85, 409:3}`.
**Kanıt (canlı):** yedi uçta şema alanları gövdeyle **birebir** eşleşti
(`health`, `lookups`, `coupons`, `search`, `blog`, `partner/coupons`,
`boats/{slug}`). `404` → `{error}`, `400` → `{error, code}`, `201` → `{id}`
— üçü de `ApiError`/`IdResponse` şemasıyla aynı. **591 test yeşil.**

## 2026-09-05 (10) — Bütün tablolar dolduruldu; doldurma iki gerçek kusur buldu

Mert: *"Bizim bütün veritabanı tablolarımızı uygun bir şekilde doldurmanı
istiyorum. Sen doldurduktan sonra front-end'i birde öyle test edeceğim."*

Başlangıç ölçümü: 82 tablodan **16'sı tamamen boş**. `pg_stat_user_tables`
ile bakmakla başlamıştım ve o **yalan söyledi** — `Amenities` için 0 dedi,
gerçekte 9 vardı. `n_live_tup` bir tahmindir; `count(*)` ile sayıldı.

**Neden:** demoyu elle SQL'le doldurmak daha hızlı olurdu ama yalnız
tabloları doldururdu — akışları değil. Uçtan geçen veri, veriyi üreten
yolun çalıştığını da kanıtlıyor; kısıtlar, doğrulamalar ve yetki kapıları
aynı anda sınanıyor. Ayrıca elle yazılan satır, uygulamanın asla
üretmeyeceği bir birleşim olabilir ve arayüz onu gerçek sanır.

**Yöntem: uç varsa uçtan.** Doldurma aynı zamanda uçları sınadığı için
**iki gerçek kusur** ortaya çıktı ve ikisi de yalnız veri yazarken görüldü:
ekstralı teklif kabulü `500` dönüyordu, konuşma–rezervasyon bağını hiçbir
kod yazmıyordu → 2026-09-05 (11) ve (12).

**Bulgu 1 — sekiz tabloyu uygulama kodu HİÇ kullanmıyor.** Ne okuyan ne
yazan bir satır var; yalnız migration ve `DbSet` içinde duruyorlar:
`Invoices`, `InvoiceCounters`, `NotificationTemplates`,
`NotificationDeliveries`, `WeatherCancellations`, `CalendarModeRules`,
`BoatCrewLanguages`, `OfferItems`(*).

Bunlar boş tablo değil, **yazılmamış özellik**: faturalama yok, hava
muhalefeti iptali yok, sezona göre takvim modu yok, bildirim şablonları
koda gömülü. Şemanın vaat ettiği ile kodun yaptığı ayrışmış.

(*) `OfferItems`'ın yazanı vardı ama hiç çalışmamıştı — ekstralı teklif
kabul edilemediği için. Kusur düzeltilince kendiliğinden doldu.

**Bulgu 2 — `Passengers` okunuyor, yazan uç yok.** Biniş ekranı yolcu
adlarını buradan alıyor, teknede `RequiresPassengerList` işareti var,
hatırlatma işi çalışıyor — ama listeyi doldurabilecek hiçbir uç yok. Yani
işaret açık bir teknede sistem sürekli olmayan bir listeyi bekliyor.
Mert'e sorulacak → `S-34`.

**Bulgu 3 — defter kendini savundu.** Geçmiş kurarken `LedgerEntries`
tarihlerini geriye almayı denedim; veritabanı reddetti:
*"LedgerEntries degismezdir; yalnizca PayoutId bir kez damgalanabilir."*
İşlem tamamen geri alındı. Koruma tam olması gerektiği gibi çalıştı ve
**gevşetilmedi**; hakediş dönemi bunun yerine sözleşmeden ayarlandı
(`PayoutPeriodDays`, kısıt: `> 0`).

**Kanıt (sonuç):** 82 tablonun 81'i dolu. Tek boş kalan
`NotificationOutbox` ve o bir **kuyruk** — gönderim işi boşalttığı için
boş; dolu olması gönderimin bozuk olduğu anlamına gelirdi.
**Kanıt (canlı):** dört rolde uç taraması — kimliksiz müşteri (arama 8,
kampanya 5, blog 8), girişli müşteri (rezervasyon 8, favori 3, konuşma 6,
destek 3), iki işletme (tekne 4+4, rezervasyon 20+20, yorum 12+6, belge
3+3, hakediş 2+2), platform (işletme 20, yorum 37, destek 10, kupon 13,
blog moderasyon kuyruğu 1). Sekiz teknenin sekizinde de puan var
(2,00–4,67 arası, tetikleyiciden hesaplanmış).

Betikler `araclar/demo-doldur/` altında, sıralı ve gerekçeli.

## 2026-09-05 (11) — Ekstralı teklif kabul EDİLEMİYORDU; tutar iki kez sayılıyordu

Belirti `500`. Kök neden Npgsql değil anlam çakışmasıydı:
`Offer.TotalAmount` = `BaseAmount + ekstralar` yani ekstrayı **içeriyor**;
rezervasyondaki `TotalTry` ise **ekstrasız** tur bedeli ve
`CK_Reservations_GrandTotal` şunu şart koşuyor:
`GrandTotal = Total + Extras - Discount`.

`OfferReservationFactory` teklif tutarını olduğu gibi `TotalTry`'a yazıyor,
ayrıca `ExtrasTotalTry`'ı da dolduruyordu → ekstra iki kez sayılıyor, kısıt
satırı reddediyordu. Ekstrasız teklifte `ExtrasTotalTry = 0` olduğu için
kısıt hiç zorlanmıyor ve kusur görünmüyordu.

**Neden bugüne kadar yaşadı:** kabul yolunu sınayan tek test ekstrasız bir
teklif kuruyordu. Kusur kodda değil **test kümesindeydi** — sınanmayan dal
kusuru saklıyordu.

Düzeltme: taban tutar geri çıkarılıyor, `TotalTry` ekstrasız yazılıyor,
`GrandTotalTry = TotalTry + ExtrasTotalTry`.

**Kanıt (test):** `An_offer_with_extras_can_be_accepted` üç alanı ayrı ayrı
ölçüyor — ekstra sessizce atılsaydı kabul yine başarılı olur, müşteri
ödemediği hizmeti alırdı. **Kanıt (mutasyon):** eski hesaba dönüldü, test
kırmızı. **Kanıt (canlı):** 4 ekstralı teklif kabul edildi, `OfferItems`
0 → 16.

## 2026-09-05 (12) — `CloseConversationsJob` hiçbir zaman iş yapamıyordu

`ConversationReservations` tablosunu **hiçbir kod yazmıyordu**, oysa
`CloseConversationsJob` kapatılacak konuşmayı YALNIZ oradan buluyor. Yani
iş her turda sıfır satır işliyordu: hata yok, günlük yok, uyarı yok —
tarihi geçmiş konuşmalar sonsuza kadar açık kalıyordu.

Bağ artık teklif kabulünde kuruluyor. Bağ ilk kaydetmeden SONRA ekleniyor
(rezervasyon kimliği ancak orada doğuyor) ve **ayrı bir kaydetme** gerekiyor:
sonraki iki adım doğrudan SQL yazıyor ve değişiklik izleyicisini boşaltmıyor.
İlk denemede bu unutuldu, satır yazılmadı, test yakaladı.

**Neden bu ailenin bir üyesi:** bu, projede tekrarlayan *"yazılmış ama hiç
uygulanmamış kontrol"* deseninin veri tarafındaki hâli — **okuyanı olan ama
yazanı olmayan tablo.** Kod incelemesi bulamaz; yalnız veriyi doldurmaya
çalışmak bulur.

**Kanıt:** test bağın varlığını değil, işin konuşmayı **kapatabilmesini**
ölçüyor (`RunAsync` çağrılıyor, `Status = Closed` doğrulanıyor) — yorumun
iddiası testten fazlasını söylemesin diye. Mutasyon: çağrı kaldırıldı,
kırmızı. Canlı: `ConversationReservations` 0 → 4.

## 2026-09-05 (13) — Ödeme sağlayıcısı Paratika; İyzico kaldırılmadı

Mert: *"Ödeme sistemi iyzico değil paratika olucak."*

`ParatikaPaymentProvider` yazıldı, `Payments:Provider` varsayılanı `paratika`
oldu. **İyzico sınıfı ve ayarları SİLİNMEDİ.**

**Neden silinmedi:** `PaymentProviderResolver` iadeyi ödemenin KENDİ
sağlayıcısından geçiriyor. İyzico kaydı kaldırılsaydı o sağlayıcıdan geçmiş
eski bir rezervasyonun iadesi çalışma anında "sağlayıcı bulunamadı" hatasına
düşerdi — ve bu ancak aylar sonra, ilk eski iade denendiğinde görülürdü.
Sağlayıcı seçimi ayarla yapılıyor, sınıfın varlığıyla değil.

### Paratika'nın İyzico'dan iki yapısal farkı

**1. İstek biçimi.** JSON değil `application/x-www-form-urlencoded`; tek uç
adresi var ve işlemi `ACTION` alanı belirliyor. Kimlik her istekte gövdede
(`MERCHANT`, `MERCHANTUSER`, `MERCHANTPASSWORD`), ayrı imza başlığı yok.

**2. İşlemin kalıcı anahtarı bizim ürettiğimiz `MERCHANTPAYMENTID`.**
Sorgulama (`QUERYTRANSACTION`) ve iade (`REFUND`) bu alandan gidiyor, oturum
jetonundan değil. Bu yüzden `ProviderTransactionId` olarak **oturum jetonu
değil sipariş anahtarı** saklanıyor. Jeton saklansaydı ödeme çalışır, ay
sonra yapılacak iade elde tutulan anahtarla çalışmazdı.

Anahtar rezervasyon kodu + rezervasyon kimliğinden kuruluyor ve 32 karakterde
kesiliyor; kod baştan yer aldığı için bir destek kaydında hangi rezervasyona
ait olduğu okunabiliyor. Rastgele değil: aynı rezervasyon için her zaman aynı
anahtar üretiliyor.

### Pazaryeri modeli — `A-41`'in şekli değişti

Paratika'nın pazaryeri modeli belgeli ve satıcı kaydı bir API aksiyonu:
`SELLERADD` (ayrıca `SELLEREDIT`, `QUERYSELLER`). Yani İyzico'daki
*"bu servis yalnız pazaryeri müşterilerine açık"* duvarının Paratika
karşılığı **kod tarafında yok** — `RegisterPayeeAsync` gerçekten yazıldı.

Bölüştürme sepet kalemine yazılıyor (`sellerId`, `sellerCommissionAmount`),
isteğin köküne toplamı (`TOTALSELLERCOMMISSIONAMOUNT`). Üçü birlikte gitmek
zorunda.

Satıcı anahtarını **sağlayıcı üretmiyor, biz veriyoruz**: `SELLERID` isteğin
zorunlu alanı ve işletmenin kendi kimliği yazılıyor. Böylece iki tarafta iki
ayrı numara taşımak gerekmiyor.

Vergi kimliği işletme türüne göre AYRI alana gidiyor: vergi mükellefi olmayan
şahıs `TCKN`, şirketler `VKN`. Hesap sahibi adı yalnız arkasında gerçek kişi
olan türlerde gönderiliyor — limited/anonimde hesap tüzel kişiye ait ve oraya
kişi adı yazmak IBAN sahibiyle uyuşmazlık üretirdi.

### Doğrulanamayan cevap ÖDENDİ sayılmıyor

`QUERYTRANSACTION` cevabında işlem kaydının hangi düzeyde durduğu (kökte mi,
listede mi) **gerçek hesap olmadan doğrulanamadı**. Kod bu belirsizliği
"muhtemelen ödendi" diye çözmüyor: tutarı okuyamazsa ödemeyi BAŞARISIZ
sayıyor.

**Neden bu yön:** yanlış tarafa düşen bir teyit ödenmemiş rezervasyonu
ödenmiş gösterir, koltuk tutulur ve tekne boş kalkar — bu **görülmez**. Bu
yönde düşen bir teyit ise ödemiş müşteriyi bekletir ve destek talebi açtırır
— bu **görülür**. Belirsizlik görünür tarafa yıkıldı.

**Kanıt (test):** 7 test, ağa çıkmadan sahte taşıyıcıyla. **Beş mutasyon da
yakalandı** — bölüştürme alanları kaldırıldı (1 kırmızı), doğrulanamayan
cevap "ödendi" yapıldı (1), tutar doğrulaması kaldırıldı (1), vergi kimliği
hep `VKN`'ye yazıldı (1), tutar biçimi kültüre bırakıldı (3).
**Kanıt (açılış kapısı, canlı):** üretim ortamında dört durum ölçüldü —
kimlik bilgisi yok → reddetti; API adresi deneme → reddetti; API üretim ama
ödeme sayfası deneme → **ayrıca** reddetti; hepsi üretim → açıldı.
İki adres ayrı denetleniyor: yalnız biri üretime alınırsa müşteri deneme
sayfasında kart girer ve para yine tahsil edilmez. **600 test yeşil.**

## 2026-09-05 (14) — Depolama Amazon S3; yol-tarzı adresleme yalnız AWS DIŞINDA

Mert: *"S3 olarak da Amazon S3 bucket'i kullanacağız."*

Ölçüm: kod **zaten** gerçek AWS'ye bakıyordu — `AWSSDK.S3`, `IAmazonS3`,
bölge `eu-central-1`, `ServiceUrl` boş. Kararın gerektirdiği bir kod
değişikliği yoktu. `S-24`'teki *"S3 / DO Spaces"* belirsizliği kapandı.

Tek düzeltme `ForcePathStyle`: koşulsuz `true` idi ve yorumu *"gerçek AWS
ikisini de kabul ediyor"* diyordu. Bu bugün doğru ama AWS yol-tarzı
adreslemeyi kullanımdan kaldırma yolunda ve yeni bölge/özelliklerin bir kısmı
yalnız alt alan adı biçiminde çalışıyor.

**Neden:** "bugün çalışıyor" ile "doğru" aynı şey değil. Sağlayıcı artık
kesinleştiğine göre varsayılan da kesinleşmeli; koşulsuz bırakmak sessizce
eskiyen bir seçim olurdu. Ayrım `ServiceUrl` ile yapılıyor — dolu olması
zaten "AWS değil" demek, geliştirme ve testler MinIO'ya karşı koşuyor.

**Kanıt:** 600 test yeşil; MinIO'ya karşı koşan depolama testleri etkilenmedi
(`ServiceUrl` dolu olduğu için onlarda yol-tarzı hâlâ açık).

## 2026-09-05 (15) — İşletmenin ilçesi ayrı alan; şehirle birleştirilmedi

Web oturumu: `/add-boat` başvuru formunda Mert "Şehir" yerine **"İl" ve
"İlçe"** istiyor. Şemada yalnız `city` vardı.

`Partner.District` eklendi (boş bırakılabilir, 120 karakter). İki uçta
görünüyor: `POST /api/partners/apply` gövdesinde ve
`GET/PUT /api/partner/profile` yazılabilir alanları arasında.

**Neden `"Muğla / Bodrum"` diye tek alana yazılmadı** — en kolay yol buydu ve
hiç backend işi gerektirmezdi: **ayrıştırma bir daha yapılamaz.** Bugün
birleştirilen veri, yarın "Muğla'daki bütün işletmeler" sorgusunda ayrılmak
zorunda kalır ve o ayırma kullanıcının nasıl yazdığına bağlı bir TAHMİNE
döner. Bu, `Coupons.UserId` itirazının aynısı: iki anlamı tek alana koymak.
Alanı bugün açmak ucuz, veri girildikten sonra bölmek pahalı.

**Neden zorunlu değil:** mevcut kayıtlarda ilçe yok ve zorunlu yapmak onları
geçersiz kılardı; ayrıca merkez ilçedeki bir işletme yazmak istemeyebilir.
`city` zorunluluğu değişmedi.

İl listesi `lookups`'a KONMADI. 81 il değişmiyor ve bir uç çağrısı daha
eklemek bu alan için orantısız; liste ekranda sabit duruyor. İlçe serbest
metin: ~970 ilçelik doğrulanmamış bir liste, serbest metinden **daha kötü**
olurdu — kullanıcı kendi ilçesini bulamayınca yanlışını seçer.

**Kanıt (migration):** `A97_IsletmeIlcesi` — boş bırakılabilir kolon, tablo
yeniden yazılmıyor, `Down` çalışıyor. `dailycruising` rolüyle uygulandı;
`Partners` sahibi `dailycruising`, uygulama rolünün yeni kolonda `SELECT` ve
`UPDATE` yetkisi **kolon bazında** doğrulandı.
**Kanıt (canlı):** başvuru `city=Muğla, district=Bodrum` yazdı; profil ucu
alanı döndürdü ve `PUT` ile `Yalıkavak` olarak değiştirildi, tekrar okundu.
Olay yükü izin listesine `district` eklendi — eklenmeseydi alan olay
günlüğüne sessizce düşerdi. **600 test yeşil.**

## 2026-09-05 (16) — En çok linklenen dosya en bayat dosyaydı; üretilebilen kısım artık üretiliyor

Vault oturumu ölçtü: `api-sema.md` **40 yerden linkli**, `durum: guncel`
diyor, **24 Ağustos'tan beri yazılmamış**. Ben de ölçtüm: veritabanındaki
**84 tablonun 16'sı o belgede hiç geçmiyor** — `BoardingTickets`,
`FavoriteBoats`, `NotificationPreferences`, `CouponAssignments`, `TaxRates`,
`PartnerPayeeAccounts` ve on tane daha.

**Neden bu şaşırtıcı değil:** çok linklenmek bir dosyayı güncel TUTMAZ,
yalnız güncel SANILMASINI sağlar. Güven arttıkça doğrulama azalıyor. Bu
`api-mimari` olayının aynısı ve aynı dersin ikinci kanıtı: bir dosyayı
canlı tutan şey linki değil tetikleyicisidir.

**Çözüm elle güncellemek DEĞİL.** Elle güncellemek aynı çürümeyi geri
getirirdi — belge 994 satır ve her migration'da elle dokunulması gereken bir
şey, ilk yoğun günde atlanır. Bunun yerine dosya İKİYE ayrıldı:

| Dosya | Ne taşır | Nasıl güncellenir |
|---|---|---|
| `api-sema.md` | 24 Ağustos'ta onaylanan tasarım ve **gerekçesi** | elle; zaten değişmiyor, arşiv |
| `api-sema-guncel.md` | bugün veritabanında ne var | `araclar/sema-cikar.py` **üretir** |

`api-sema.md` artık `durum: tasarim-kaydi` ve başında ne OLMADIĞI yazıyor.

**Neden ayrım burada:** envanter üretilebilir, gerekçe üretilemez. "Neden bu
kısıt var" sorusunun cevabı hiçbir sorguda yok ve elle yazılmaya devam
etmeli. Karışık tutmak, üretilemeyeni de çürütüyordu.

Bu, aynı gün `demo-doldur/ozet.py` ile verilen kararın ikizi: **bayatlayan
belge yazmak yerine belgeyi üretmek.** İkisinde de tetikleyici "hatırla"
değil "betiği çalıştır" oldu.

**Kanıt:** üretilen belgede 84 tablonun 84'ünün başlığı var (0 eksik),
`Partners.District` kolonu ve `CK_Reservations_GrandTotal` kısıtı dahil.

## 2026-09-05 (17) — Paratika kapıları testle bağlandı; `ForcePathStyle` testi YAZILMADI

İki iş, ikisi de aynı dersin uygulaması.

**Yapıldı:** Paratika'nın üç açılış kapısı `ProductionGuardTests` zincirine
eklendi. Kapılar canlıda ölçülmüştü ama teste bağlı DEĞİLDİ — yani biri
kapıyı kaldırsa hiçbir şey kırılmazdı. Zincirin son adımı da düzeltildi:
`Assert.Contains("")` yazmıştım, **her zaman geçen** bir iddia. Gerçek
mesaja bağlandı.

**Kanıt:** iki mutasyon da yakalandı — kimlik kapısı kaldırıldı (kırmızı),
ödeme sayfası adresi denetimi kaldırıldı (kırmızı).

**YAPILMADI ve sebebi:** `ForcePathStyle` dalı için test yazmayı denedim.
Yazdığım test `!string.IsNullOrWhiteSpace(ServiceUrl)` ifadesini **kopyalıyordu**;
`Program.cs` bozulsa kırmızıya dönmezdi. Yani yeşil bir test, sıfır ölçüm.

Sildim. Gerçeğini yazmak uygulamayı ayağa kaldırıp kapsayıcıdan `IAmazonS3`
çözmeyi gerektiriyor ve ölçeceği tek şey bir boole; `Y-14` zaten ilk gerçek
yüklemede kapanıyor. **Sahte testin maliyeti testsizlikten yüksek:** testsiz
bir dal "doğrulanmadı" diye durur, sahte testli bir dal "doğrulandı" diye
durur.

**Neden buraya yazıldı:** yapılmayan işin gerekçesi de karardır. Yazılmasa,
altı ay sonra biri "burada test eksik" der ve ya boşuna yazar ya da aynı
sahte testi kurar → [[genel-desenler]] *"Testler yeşil demeden önce
değiştirdiğin satırın koştuğunu ölç"*.

## 2026-09-05 (18) — Katılım akışının kopuk halkası: sözleşme kabul ucu

Web oturumu bildirdi, ben de baştan ürettim: sözleşme gönderilmiş bir işletme
giriş yapıyor, `GET /api/partner/contracts` **404**, panelin her bölümü
**403**. Yani sözleşmesini ne görebiliyor ne kabul edebiliyordu — ve **hiçbir
yeni işletme sisteme giremiyordu.**

**Kusurun şekli, bu projede tekrarlayan desenin en pahalı hâli:** panelin
`Active` olmayan işletmeye kapalı olması DOĞRU bir kural. Ama işletmeyi
`Active` yapacak tek eylem de o kapının ardındaydı. Kapı doğru, arkasında
çıkış yok.

Ayrıca `Contract` varlığında `ApprovedAt`, `ApprovedByUserId`, `ApprovedIp`,
`ApprovedUserAgent` **zaten vardı** — şema kabulü öngörmüş, uç yazılmamıştı.
`ConversationReservations` ile aynı aile: yazanı olmayan alan.

### Kararlar

**Neden bu uçlar kapının dışına alındı:** kuralı gevşetmek yerine kapıyı
korumak da mümkündü — örneğin işletme aktifleşene kadar sözleşmeyi
e-postayla göndermek. Seçilmedi çünkü ticari bir taahhüdün kabulü,
kimliği doğrulanmış bir oturumda ve delili kaydedilebilir biçimde
olmalı; e-posta bağlantısı ikisini de zayıflatırdı. Kapı korunacaksa
arkasında bir çıkış olmak zorunda, yoksa kural değil tuzak olur.

**Uçlar yetki kapısına DEĞİL yalnız kimliğe bağlı.** İstisna dar tutuldu: iki
uç, yalnız kendi sözleşmesi, kapsam sorgunun İÇİNDE. Panelin başka hiçbir ucu
açılmadı — kapı tek tek gevşetilerek erir.

**Parola isteniyor.** Sahiplik devriyle aynı gerekçe ve ondan güçlüsü: bu
tıklama işletmeyi komisyon oranına ve hakediş dönemine BAĞLIYOR. Açık bırakılan
bir oturumda yanlışlıkla basılabilecek bir düğmenin arkasına ticari taahhüt
konulmaz.

**Ayrı "okudum" onay kutusu YOK.** Kabul isteğinin kendisi zaten olumlu
eylemdir; ikinci bir boole yalnız istemcinin gönderdiği bir iddia olurdu ve
sunucu onu doğrulayamaz. Delil değeri taşıyan üç şey — an, adres, tarayıcı —
**sunucuda** üretiliyor. İmzalayanın kendi beyanı, imzanın kanıtı değildir.

**Durum yalnız `ContractSent`'ten `Active`'e geçiyor.** Koşulsuz yazılsaydı
askıya alınmış bir işletme, elinde gönderilmiş sözleşme kaldıysa kendi askısını
kaldırabilirdi. Askıyı kaldırmak platformun işi.

**Kabul ile aktifleşme AYNI işlem.** Ayrı adımlara bölünseydi "kabul etmiş ama
hâlâ giremeyen işletme" oluşurdu — düzeltilen kusurun bir adım ileri hâli.

**Kanıt (canlı):** başvuru → inceleme → sözleşme gönderimi → işletme girişi.
Sözleşme listesi `200` (unvan, %18 komisyon, 21 gün, metin), panel hâlâ `403`;
yanlış parola `400 InvalidPassword`; **başka işletmenin sözleşmesi `404`**
(varlık sızdırmıyor); doğru parola `204` → işletme `Active`, dört delil alanı
da dolu; kabul sonrası panel `200`.
**Kanıt (mutasyon):** dördü de yakalandı — parola denetimi kaldırıldı, kapsam
sorgudan çıkarıldı, durum koşulsuz `Active` yapıldı, sözleşme metni
döndürülmedi. **605 test yeşil.**

⚠️ İki test bu değişiklikte **kendiliğinden** kırıldı ve ikisi de doğru
davrandı: `openapi.json` bayat kaldı, yeni olay türünün yük izin listesi
yoktu. Kapılar işini yaptı.

## 2026-09-05 (19) — Sözleşme reddi: reddedilen SÖZLEŞMEDİR, işletme değil

Mert: *"Reddetme özelliği de olsun."* — `S-36` kapandı.

Ret önerisine itirazım şuydu: ayrı bir "reddedildi" durumu, ileri yolu olmayan
ölü bir işletme kaydı üretebilir. Mert özelliği istedi; itiraz **tasarımda**
karşılandı, özellik kısılarak değil.

**Neden:** ret ile işletmenin reddedilmesi iki ayrı şey. Sözleşme reddedilince
`Contracts.Status = Rejected` oluyor ama **işletme `ContractSent` kalıyor**.
Böylece platform düzeltilmiş bir sözleşme gönderebiliyor ve pazarlık döngüsü
kapanıyor. İşletmeyi de reddedilmiş saymak, tam olarak itiraz ettiğim ölü
kaydı üretirdi.

Mevcut kodun iki yeri bu tasarımı zaten destekliyordu ve değiştirilmedi:
`HasPendingContractAsync` yalnız `Sent` sayıyor (reddedilmiş sözleşme yeni
gönderimi engellemiyor) ve `CancelPendingContractsAsync` yalnız `Sent`
iptal ediyor (ret kaydı geçmişte duruyor).

### `Rejected`, `Cancelled`'dan ayrı bir durum

İptali **platform** yapar (yerine yenisi gönderildiği için), reddi **işletme**
yapar (şartları kabul etmediği için). Tek değerde toplansaydı *"bu sözleşme
neden yürürlükte değil"* sorusunun cevabı kaybolurdu.

### Gerekçe zorunlu, parola değil — asimetri bilinçli

**Gerekçe ZORUNLU.** Gerekçesiz bir ret platforma neyi düzelteceğini söylemez;
ret o zaman akışı ilerletmeyen bir düğmeye dönerdi. Boşluk kırpılıyor: yalnız
boşluktan oluşan gerekçe, gerekçesizliğin kılık değiştirmiş hâli.

**Parola İSTENMİYOR** — kabulde isteniyor. Kabul işletmeyi komisyon oranına ve
hakediş dönemine BAĞLIYOR, geri alınamaz. Ret bağlamıyor ve geri alınabilir:
platform yeni sözleşme gönderir. Geri alınabilir bir eylemin önüne geri
alınamaz olanın sürtünmesini koymak koruma değil yalnız engel olurdu.

### Kural veritabanında da var

`CK_Contracts_RejectedEvidence`: `Status <> 'Rejected' OR (RejectedAt IS NOT
NULL AND RejectedByUserId IS NOT NULL AND RejectionReason IS NOT NULL)`.
Onay tarafındaki `CK_Contracts_ApprovedEvidence` ile aynı güçte, üstüne
gerekçeyi de istiyor. Uygulama yolu atlansa bile gerekçesiz satır yazılamıyor.
Durum listesi kısıtı da `Rejected`'ı kapsayacak şekilde `NOT VALID` + `VALIDATE`
deseniyle güncellendi.

**Kanıt (canlı, pazarlık döngüsünün tamamı):** %25 komisyonlu sözleşme
gönderildi → gerekçesiz ret `400 ReasonRequired` → gerekçeli ret `204`,
sözleşme `Rejected`, **işletme `ContractSent` kaldı** → reddedilen sözleşmeyi
kabul denemesi `404` → platform %15'lik yeni sözleşme gönderdi `201` → liste
ikisini de gösteriyor (biri `Sent`, biri gerekçesiyle `Rejected`) → kabul
`204` → işletme `Active` → panel `200`.
**Kanıt (mutasyon):** üçü de yakalandı — ret işletmeyi de kapattı (2 kırmızı),
gerekçe zorunluluğu kaldırıldı (2 kırmızı), gerekçe kırpılmadı (1 kırmızı).
**609 test yeşil.**

## 2026-09-06 — Dalışçı sayısı yolcuların alt kümesidir ve kontenjan sefer düzeyinde denetlenir

Mert: *"rezervasyon formunu da değiştir, dalışçı sayısı sorulsun"*

### Karar 1 — dalışçı ek yolcu değil, yolcuların alt kümesi

`DiverCount <= AdultCount + ChildCount`. Dalan kişi zaten koltuk tutuyor.

**Neden:** ayrı bir sayı olsaydı kapasite iki kez sayılırdı — 4 yolcu + 3
dalışçı 7 koltuk gibi görünür, tekne dolmadan dolu görünürdü. Bu tür bir
hata ekranda hata olarak da görünmez: yalnız satılmayan koltuk olarak.

Bebekler üst sınırın dışında: bebek dalmaz ve koltuk da tutmuyor.

### Karar 2 — kontenjan SEFERİN tamamı için denetlenir

`Voyages.SoldDivers` sayacı + `CK_Voyages_SoldDivers`.

**Neden:** `dalis-turu` paylaşımlı bir tur (`PerPerson` / `Shared`). Yalnız
gelen isteği kontenjanla karşılaştıran bir denetim "koruma var, kapsamı
yanlış"tır: kontenjan 8 iken beş ayrı rezervasyonun her biri 8 dalışçı
yazabilir, hepsi tek tek geçer ve tekne 40 dalışçıyla kalkar.

Fiyat servisindeki tek-istek denetimi KALDI ama işi başka: erken ve
anlaşılır bir hata vermek (`400`, "en fazla 6 dalışçı yeri var"). Sınırın
gerçekten aşılamaz olduğu yer veritabanı kısıtı (`409`, "kontenjan doldu").

### Karar 3 — sayaç `SoldSeats` ile AYNI işlevin içinde

`sync_voyage_sold_seats()` artık iki sayacı birlikte yazıyor.

**Neden:** iki sayaç iki ayrı tetikleyiciden güncellenseydi, birini
güncelleyip diğerini unutan ilk kod yolu ikisini KALICI olarak ayrıştırırdı
ve kısıtlar bunu yakalayamazdı — sayılar hâlâ sınır içinde kalabilir, yalnız
yanlış. Durum süzgeci de aynı: ayrışsaydı iptal edilen bir rezervasyonun
dalışçısı, koltuğu boşalmışken yerini tutmaya devam ederdi.

`UPDATE OF` listesine `"DiverCount"` eklenmesi işin yarısı değil tamamı:
liste eksik kalsaydı yalnız dalışçı sayısını değiştiren bir güncelleme
tetikleyiciyi hiç çalıştırmaz, sayaç eski değerde kalırdı.

### Karar 4 — `supportsDivers` tekne detayına eklendi

**Neden:** cephe "dalışçı sayısı sorayım mı" sorusunu `diverCapacity != null`
ile cevaplamak zorunda kalırdı ve bu, **kontenjanı sınırsız olan bir dalış
turunu dalış yapılmayan turdan ayırt edemezdi.** Çıkarımın doğru olduğu
durum yaygın, yanlış olduğu durum sessiz: o turda dalışçı alanı hiç
görünmez ve kimse hata görmez.

Aynı sınıf: `?? 24` ve `?? false` istemci varsayılanları → [[api-desenler]]

**Kanıt:** 640 test yeşil · üç mutasyon üç doğru kırmızı · canlı ölçümün
tamamı → [[api-gorevler]] `A-108`

### Karar 5 — bayrak teklife de kondu (aynı gün, cephenin ölçümüyle)

`QuoteResponse.supportsDivers`.

**Neden:** cephe somut bir ÜÇÜNCÜ hâl bildirdi. Rezervasyon formu bayrağı
tekne detayından okuyor ve adres çubuğunda `boat` parametresi yokken bayrağı
**bilmiyor**. Bilinmeyeni `false` saymak, dalış turunda alanı sessizce hiç
sormak olurdu — Karar 4'ün kapattığı tuzağın aynısı, bir adım sonra.

Teklif zaten her hâlde çağrılıyor. Bayrak oraya konunca "bilinmiyor" hâli
hiç doğmuyor: kapı ile sınır aynı cevapta, yan yana.

**Ders bunun kendisi:** bir bayrağı TEK bir uca koymak, o ucu okumayan her
akış için bayrağın yokluğu demek. Soru "alan bir yerde var mı" değil, **"onu
kullanacak akış onu okuyor mu"**.

**Kanıt:** 642 test · bayrak iki durumda da ölçüldü · mutasyon (`true`
sabitlendi) doğru testi kırdı · canlı: dalış turu `true`/6, dalış olmayan tur
`false`/`null` → commit `7f58ced`

## 2026-09-06 — Sözleşme şablonu: yetki, sürüm ve pasife alma

Mert: *"Sözleşme oluşturma şablonunu da yap o zaman hadi"*

### Karar 1 — yetki `contract.write`, `contract.send` degil

**Neden:** hazır bir metinden sözleşme göndermek ile platformun sözleşme
METNİNİ yazmak aynı ağırlıkta iş değil. `contract.write` katalogda zaten
"Sözleşme şablonu düzenleme" olarak tanımlıydı ve hiçbir uç kullanmıyordu —
tanımlanmış ama bağlanmamış bir yetki, verilmiş gibi görünüp hiçbir şey
yapmaz.

⚠️ **Gerekçemin ilk hâli yanlıştı ve düzeltildi.** "`contract.send`
platform-destek rolünde de var" diye ölçmüştüm; o rol GELİŞTİRME
veritabanındaki demo verisinden geliyordu. Temiz kurulumda `platform-destek`
yok, `platform.support` var ve onda `contract.send` yok. Karar değişmedi,
gerekçesi değişti — ve testi katalogdaki bir role dayandırmaktan vazgeçtim:
test yalnız `contract.send` taşıyan bir rolü KENDİ kuruyor. Katalog yarın
değişse bile ölçülen sınır aynı kalıyor.

### Karar 2 — metin değişirse sürüm artar, ad ya da yürürlük değişirse artmaz

**Neden:** gönderilmiş her sözleşme `TemplateVersion` alanında bir numara
saklıyor. Numara artmadan metin değişseydi aynı (şablon, sürüm) çiftinin
altında iki farklı metin bulunurdu ve o kayıt hangi metnin onaylandığını
söylemekten çıkardı. Tersi de doğru: her düzenlemede artan bir sayaç sürümü
"kaç kez dokunuldu" sayısına çevirir ve künyedeki numaranın anlamını
boşaltırdı.

Gönderilmiş sözleşmeler zaten etkilenmiyor — `BodyHtmlSnapshot` gönderim
anında kopyalanıyor. Ama bu güvence test yazılana kadar yalnız bir varsayımdı.

### Karar 3 — şablon silinmiyor, pasife alınıyor

**Neden:** silmek, o şablondan üretilmiş sözleşmelerin künyesindeki bağı
koparırdı. Liste `includeInactive` süzgeciyle iki soruya birden cevap
veriyor: gönderme formu yalnız aktifleri, yönetim ekranı hepsini görüyor.
Pasif şablon her yerden kaybolsaydı geri açmanın yolu kalmaz, panelden
yapılan bir tıklama geri alınamaz olurdu.

### Kusur — aynı bulucu iki işi göremez

İlk yazımda düzenleme, gönderme yolunun bulucusunu kullanıyordu:
`AsNoTracking` + `IsActive` süzgeci. İkisi de o yolun DOĞRU davranışı, ama
düzenlemede birincisi değişikliği sessizce yutuyor, ikincisi pasif şablonu
düzenlenemez yapıyordu.

**Uç `200` dönüyordu ve gövde yeni değerleri gösteriyordu** — cevap sunucunun
elindeki nesneden kuruluyordu, veritabanından değil. Sürüm testi cevaba
baktığı için YEŞİLDİ. Pasife alma testi listeyi geri okuduğu için kırmızı
verdi.

**Ders:** *ürettiğim bir iddia ölçüm değildir.* Yazma ucunun testi, yazılan
değeri BAŞKA bir yoldan geri okumak zorunda. Sürüm testi de geri okumaya
çevrildi.

**Kanıt:** 652 test · üç mutasyon üç doğru kırmızı → [[api-gorevler]] `A-109`

## 2026-09-06 — Kupon: kimlik listede, düzenleme yok, geri açma yok

Web oturumunun ölçümüyle doğdu.

### Karar 1 — atama listesi kimliği taşır, silme ucu e-posta kabul etmez

**Neden:** e-posta değişebilir bir alan, kimlik değişmez. Silme yolu
değişebilen bir anahtara bağlansaydı, adresini değiştiren bir kullanıcının
ataması kaldırılamaz hâle gelirdi. Eksik olan ucun anahtarı değil, listenin
taşıdığı bilgiydi.

### Karar 2 — kupon düzenlenmez

**Neden:** müşteri kodu görüp planını ona göre yapıyor. Yüzdesi sonradan
değişen bir kupon, aynı kodu kullanan iki müşteriye iki farklı indirim
verirdi. Yanlış açılan kupon kapatılır, yerine yenisi açılır — ve yeni
kuponun kendi sayacı, kendi tarihi olur.

### Karar 3 — pasife alınan kupon geri açılmaz

**Neden:** pasife alınmış bir kupon, müşterinin "kod geçersiz" cevabı aldığı
kupondur. Aynı kodu sessizce geri açmak reddedilen müşteriye hiçbir şey
söylemez; o müşteri kampanyayı çoktan kaybetmiştir.

### Ortak desen — beşinci kez

Bugünün tekrar eden kusuru: **veri var, onu kullanacak akış ona ulaşamıyor.**
`supportsDivers` tekne detayındaydı, rezervasyon formu ulaşamıyordu; kupon
atamasının kimliği veritabanındaydı, ekran ulaşamıyordu; sözleşme şablonu
tablosu vardı, yaratacak uç yoktu.

Soru artık "alan bir yerde var mı" değil: **onu kullanacak akış onu okuyor
mu.**

**Kanıt:** 655 test · canlı ölçümün tamamı → [[api-gorevler]] `A-110`

## 2026-09-06 — "Müşteri" kimdir: temiz kural, yanlış kapsam

Mert'in ilk tanımı: *"burada sadece bizim sitemizde kayıtlı olan müşteriler
yer alacak. İşletmeci, destek ekibi, site sahibi vesayre barınmayacak."*

Karşılığı basitti: personel değil VE işletme üyesi değil.

**Neden değişti:** o kural, tur satın almış bir işletme sahibini hiçbir
listede müşteri saymıyordu. Parası ödenmiş, rezervasyonu duruyor, ama
"kaç müşterim var" sayısında yok. Mert bunu görünce kuralı genişletti:

> (personel değil VE işletme üyesi değil) VEYA (en az bir rezervasyonu var)

İkinci koşulla girenler `alsoRole` ile işaretleniyor — listede görünüyorlar
ama sıradan müşteri gibi görünmüyorlar. Bu ayrım işlevsel: toplu müşteri
e-postası gönderilirken o satırların ayırt edilebilmesi gerekiyor.

**Ders — bugünün tekrar eden dersinin bir başka yüzü:** temiz bir kural,
kapsamı dışında kalanı YOK SAYDIĞI için yanlış olabilir. Süzgeç doğru
görünür çünkü dışarıda bıraktığı şey süzgece bakarak görülmez; ancak
"kim eksik" diye sorulduğunda ortaya çıkar.

Aynı sebeple `topRatedBoats`'a asgari yorum eşiği KONMADI: eşik de listeyi
okuyanın göremediği bir süzgeç olurdu.

**Kanıt:** 672 test · iki mutasyon iki doğru kırmızı · canlı ölçümün tamamı
→ [[api-gorevler]] `A-117`

## 2026-09-07 — Belge, telde görüneni bildirmek zorunda

`JsonStringEnumConverter` serileştirmede uygulanıyordu ama OpenAPI belgesine
yansımıyordu: tel `"Paid"` gönderiyor, belge `integer` diyordu.

**Neden bu bir kusur, biçim tercihi değil:** belgeden üretilen her istemci
tipi yanlış olur. Web tarafı `ReservationStatus: number` üretiyordu — telde
hiçbir zaman görülmeyen bir tip. Yanlış belge, elle yazmayı ZORUNLU kılıyor;
yani belge yanlış olduğu sürece "belgeden üret" kuralı hiç kurulamıyor.

**İkinci ders — sessizliğin ikinci katmanı:** belgede `enum` dizisi hiç
yoktu. Yani yalnız tür yanlış değildi, değerlerin VARLIĞI da yazılı değildi.
Cephe çeviri tablolarını elle yazmak zorundaydı ve aynı gün iki kez ayrıştı.

**Ders:** *bir sözleşmenin yanlış olması, onu kullanmayı imkânsız kılar ve
bu, kullanılmadığı için de fark edilmez.* Belge kimse ona güvenmediği için
sessizce yanlış kaldı; ancak biri "buradan üretelim" dediğinde ölçüldü.

⚠️ **Kusuru bulan şey benim yanlış önerimdi.** "Enum'ları belgeden üretin"
dedim; web oturumu ölçtü, üretilecek bir şey olmadığını gösterdi. Yanlış
öneri, ölçüldüğü için işe yaradı — ölçülmeden kabul edilseydi çalışan elle
yazılmış tipleri yanlış olanlarla değiştirecekti.

**Kanıt:** enum şeması 0 → 29 · 678 test · mutasyon doğru kırmızı
→ [[api-gorevler]] `A-121`

## 2026-09-07 — Testin yeşil olması, doğru şeyi ölçtüğü anlamına gelmiyor

`A-123`'te belgedeki `number|string` birleşimini düzelttim ve bunu ölçen bir
test yazdım. Test yeşil verdi. Ama **242 alan hâlâ bozuktu**: test yalnız
`number` + `string` arıyordu, `integer` + `string` aramıyordu; ve yalnız
`components.schemas` içine bakıyordu, sorgu parametrelerine bakmıyordu.

**Neden:** testi, düzelttiğim kusurun ŞEKLİNE göre yazdım — kusurun
SINIFINA göre değil. Elimdeki altı örneğin hepsi `decimal`di, ben de
`number` aradım.

**Bu, bugün başkalarında altı kez bulduğum kusurun testimdeki hâli:**
koruma var, kapsamı yanlış. Ve testler için özellikle tehlikeli, çünkü
yeşil bir test aktif olarak güven üretiyor — korumasız kalmaktan farkı,
korumalı olduğunu SANMAK.

**Kural:** bir koruma yazarken sorulacak soru "elimdeki örnekleri yakalıyor
mu" değil, **"bu sınıftan başka ne var ve onu da yakalıyor mu"**.

Sorunu web oturumu ölçüp bildirdi. İki oturum aynı kusur sınıfını gün boyu
birbirine gösterdi; bu sonuncusunda gösteren onlardı.

**Kanıt:** 215 → 0 · 27 → 0 · mutasyon 242 ihlal sayarak kırmızı
→ [[api-gorevler]] `A-124`

## 2026-09-07 — Biniş jetonu artık saklanıyor: bilinerek verilmiş bir güvenlik ödünü

**Önceki tasarım:** jetonun yalnız SHA-256 özeti saklanıyordu. Düz metin
müşteriye bir kez veriliyor, bir daha hiçbir yerden okunamıyordu.
Veritabanını ele geçiren biri geçerli bilet üretemezdi.

**Mert'in kararı (web oturumu üzerinden, riski yazılı olarak önündeyken):**
panelde mevcut karekod görünsün. Aktarılan cümle: *"veritabanı sızarsa
saldırgan geçerli biniş bileti üretebilir hâle gelir."*

Üç seçenek sunulmuştu: (A) bugünkü hâl — karekod yok · (B) personel yeni
bilet üretir, eskisi iptal olur · (C) jetonu sakla. **C seçildi.**

**Neden bu bir ürün kararı, teknik bir hata değil:** karekodun panelde
görünmesi iskelede gerçek bir işi çözüyor ve müşterinin belgesini
bozmuyor. Güvenlik tarafı zayıflıyor; hangisinin ağır bastığı ürün
sahibinin kararı.

### Ödünün maliyetini düşüren üç şey

1. **Şifreli, düz metin değil.** AES-GCM, anahtar **veritabanının
   dışında** (yapılandırmada). Yalnız veritabanı sızarsa jetonlar okunamaz.
   ⚠️ Bu "hiç saklamamak" kadar güvenli DEĞİL ve öyle anlatılmamalı: iki
   farklı sırrın birden sızmasını gerektiriyor, o kadar.

2. **Uygulama anahtarsız açılmıyor.** Varsayılan anahtar konsaydı, onu
   değiştirmeyi unutan kurulum "şifreli" görünüp herkesin bildiği bir
   anahtarla korunurdu — şifrelemenin en kötü hâli, çünkü koruma sanılıyor.

3. **Görüntüleme kayda geçiyor** (`boarding.ticket.viewed`). Sızıntı
   riskini kaldırmıyor, kötüye kullanımı görünür yapıyor: panelde bir
   personel misafirin biniş kodunu izsiz alabilir hâle geliyordu.
   Jetonun KENDİSİ günlüğe yazılmıyor — erişimi kaydeden mekanizma ikinci
   bir sızıntı yüzeyi olmamalı ve olay günlüğü temizlenemiyor.

### AES-GCM neden

Hem gizliyor hem **bütünlüğü doğruluyor**. Yalnız gizleyen bir kip (CBC)
kullanılsaydı, veritabanına yazma erişimi olan biri jetonu sessizce
değiştirebilir ve kimse fark etmezdi.

Özet KALDI: okutma doğrulaması hâlâ onun üstünden çalışıyor, çünkü şifreli
metin her seferinde farklı çıkıyor ve aramaya elverişsiz.

**Geri doldurma imkânsız:** bu karardan önce üretilmiş biletlerin düz metni
hiçbir yerde yok. O rezervasyonlarda `token: null`.

**Kanıt:** 688 test · 7 şifreleme testi · canlı: müşteriye verilen jeton ile
panelde görünen AYNI, veritabanında düz metin YOK, görüntüleme günlüğe
yazıldı → [[api-gorevler]] `A-127`

## 2026-09-07 — Günün üç kusur sınıfı

Bugün iki oturum birbirine sekiz kusur gösterdi ve **hiçbiri gözle
görülmedi, hepsi ölçümden çıktı** — panel hâlâ tarayıcıda gezilmedi.
Üçü tekrar eden sınıf:

### 1. Boş ya da tek çeşit veri, kusuru gizler

· Destek sekmesi boşken durum sütunu hiç sınanmamıştı; veri gelince ham
  İngilizce çıktı.
· Dört kuponun dördü de listeliydi; "listelenene kişi atanamaz" dalı hiç
  çalışmamış, ekranda ölü bir düğme duruyordu.
· Müşteri listesindeki "işletme üyesi" işareti, rezervasyon yapan bir
  işletme sahibi olmadığı için canlıda hiç görünmemişti.
· Ekstra tablosu boştu, "yok" ile "bozuk" ayırt edilemiyordu.

⚠️ Tersi de doğru ve daha ince: **tablo dolsun diye doldurmak** da yanlış —
kimsenin okumadığı veri, kimsenin fark etmediği yanlış demek. Ölçüt
"tablo dolu mu" değil, **"bu ekranın dalları çalıştı mı"**.

### 2. Aracın ne ölçtüğünü sormadan sayısına güvenmek

· `pg_stat_user_tables.n_live_tup` bayat: kuponlar yazılmışken 0 gösterdi.
· Web'in üreteci "183/184 yanıt şeması" diyordu; 400'ün `ApiError`'ını
  sayıyordu, gerçek sayı 129.
· `grep -c` satır sayar, eşleşme değil.
· Benim `contract.send` ölçümüm demo verisindendi, temiz kurulumda o rol
  yok.

Ortak hâl: sayı doğru görünüyor ve kimse **neyi saydığını** sormuyor.

### 3. Korumanın kendi kapsamını ölçmemek

· `number|string` testim 242 alanı kaçırdı: kusurun ŞEKLİNE göre yazılmıştı,
  SINIFINA göre değil.
· Web'in `TEKNE_DURUMU`'u üç kopyaydı ve yalnız birinde ayrışmıştı.

En tehlikelisi bu, çünkü yeşil bir test **aktif olarak güven üretiyor**.
Korumasız olmaktan farkı: korumalı olduğunu sanmak.

**Kural:** bir koruma yazarken sorulacak soru *"elimdeki örnekleri
yakalıyor mu"* değil, **"bu sınıftan başka ne var ve onu da yakalıyor
mu"**.

**Neden:** bu üç sınıf bugün sekiz kusurun tamamını üretti ve hiçbiri
gözle görülmedi. Kaydedilmeselerdi, yarın aynı sınıftan dokuzuncusu yine
ölçümle bulunacaktı — üstelik her seferinde farklı bir kılıkta, yani
"aynı hatayı yapıyoruz" cümlesi hiç kurulmayacaktı. Sınıfın adı olmadan
tekrar görünmüyor.


## 2026-09-07 · Karekod üretimi ödemeyi düşüremez

Ödeme tamamlandığında biniş karekodu kendiliğinden üretiliyor
(`PaymentService.EnsureBoardingTicketAsync`). Üretim bloğu **bilerek**
`catch (Exception) when (!ct.IsCancellationRequested)` ile yutuluyor.

**Neden:** İki iş aynı çağrıda ama ağırlıkları aynı değil. Ödeme
kaydedildiğinde para çoktan çekilmiş, defter satırı atılmış olur;
o noktada fırlatılan bir istisna müşteriye "ödeme başarısız" der ve
kayıtla gerçek ayrışır. Karekod ise **sonradan elle de üretilebilir**
(uç nokta zaten var), ödeme üretilemez. Ucuz olanı feda ediyoruz.

⚠️ Bunun bedeli: karekod üretimi sessizce başarısız olabilir. Kabul
edildi çünkü alternatifi — başarılı bir ödemeyi başarısız göstermek —
kıyaslanamaz derecede kötü.

## 2026-09-07 · Aynı gerçeği iki alanda tutmak, tutarsızlığı görünmez yapar

`Voyages` hem `DepartureDate` hem `StartsAt` taşıyor. Demo betiği yıllardır
yalnız `StartsAt`'i kaydırıyordu; 68 seferin 4'ünde iki alan **farklı gün**
söylüyordu ve hiçbir ekran şikâyet etmedi.

**Neden görünmedi:** iki alan farklı yerlerde okunuyor — ekranlar
`DepartureDate`, biniş penceresi ve iade dilimleri `StartsAt`. Her okuyucu
kendi alanını tutarlı buluyor. Tutarsızlık ancak **ikisini aynı anda
kullanan** bir iş çıkınca (bilet üretimi) ortaya çıktı.

**Ders:** türetilebilir bir alanı ayrıca saklıyorsak, onu yazan **her**
yolun ikisini birden yazdığını denetlemek gerekir; "kim güncellemeyi
unutur" sorusu değil, "unutulduğunda ne bağırır" sorusu önemli. Burada
hiçbir şey bağırmıyordu. → [[api-desenler]]

## 2026-09-08 · Okutma bileti iptal etmiyor — "okutuldu" biletten okunamaz

Başarılı okutmadan sonra `BoardingTickets.RevokedAt` **null kalıyor** ve
`isUsable` **true** dönmeye devam ediyor. Ölçüldü: `6UGJC9S4` okutuldu,
bilet hâlâ geçerli görünüyor.

**Neden:** `BoardingService` `Boarded` durumundaki rezervasyonun tekrar
okutulmasını kabul ediyor ve `AlreadyBoarded: true` dönüyor. Kaptan aynı
kodu ikinci kez okuttuğunda korkutucu bir hata değil, "zaten binildi"
görmeli — iskelede tereddüt, yanlış kabulden pahalı.

**Bedeli:** ön yüz "okutuldu" hâlini `boardingTicket`'tan **türetemez**.
Bugün tek doğru yol `boardingScans.some(s => s.succeeded)`.

⚠️ **`succeeded` süzgeci zorunlu.** `boardingScans` başarısız denemeleri de
taşıyor (bilerek — iskelede çalışmayan kodun sebebi yalnız orada yazılı).
`length > 0` yazan bir ön yüz, yalnızca başarısız denemesi olan GEÇERLİ bir
bileti "okutuldu" diye soluklaştırır.

`status === 'Boarded'` daha zayıf bir vekil: biniş elle de işaretlenebiliyor
(`2A2UA3HS` öyle kurulmuş), o zaman okutma yokken "okutuldu" denir.

**`usedAt` alanı YAZILDI ve GERİ ALINDI.** Ön yüz — tek tüketicisi —
istemedi: türetmeyi tek satırla ve `succeeded` süzgeciyle doğru yapıyor,
alan eklemek sözleşme yüzeyini tüketicisi olmayan bir şeyle büyütürdü.
Gerekçe kabul edildi.

**Yeniden istenmesinin koşulu yazılı:** müşterinin kendi ekranı bu bilgiyi
isterse. `MyReservationItem`'da bilet alanı **hiç yok**, dolayısıyla orada
türetilecek `boardingScans` de olmayacak — o gün `usedAt` doğru cevap olur.

Bu turun kazancı alan değil, **ölçüm**: ön yüz "okutuldu" hâlini
`boardedAt`ten türetiyordu ve `2A2UA3HS` gibi ELLE işaretlenmiş bir binişte
ortada hiç okutma yokken "bu kod okutuldu" diyordu. Ölçüm o kusuru açtı,
alan değil.

## 2026-09-08 · Tekrar okutma "başarısız" yazılmaz

Web oturumu, ikinci okutmanın denetim kaydına `Succeeded = false` +
`FailureReason = "AlreadyBoarded"` yazılmasını önerdi. **Reddedildi.**

**Neden:** `Succeeded` "biniş oldu mu" demiyor, **"okutma kabul edildi mi"**
diyor. Ölçüldü — `false` yazılan bütün hâller (`TokenExpired`, `NotPaid`,
`Cancelled`, `Refunded`, `Expired`, `AlreadyCompleted`, `NotBoardable`)
`BoardingException` fırlatıyor: istek reddedilmiş, kaptan hata görmüş,
misafir binememiş. Tekrar okutma bunların hiçbiri değil — `BoardingResult`
dönüyor ve kaptan yolcu listesini görüyor.

İki somut bedeli olurdu:

1. `IX_BoardingScans_ScannedAt WHERE Succeeded = false` kısmi dizini
   iskelede **çalışmayan** kodları bulmak için var. Zararsız tekrarlar
   oraya dolarsa işletmesel değeri olan tek sorgu seyrelir.

2. ⚠️ **Ön yüzün "elle işaretlendi, kod okutulmadı" hâlini yalancı
   çıkarırdı.** Sıra: biniş elle işaretlenir (`Boarded`, okutma yok), sonra
   kaptan gerçek karekodu okutur. O okutma `Succeeded = false` yazılırsa
   rezervasyonun TEK okutması "başarısız" olur ve ekran "bu kod okutulmadı"
   der — okutulduğu hâlde. `2A2UA3HS` tam olarak bu şekil.

**Gerçek problem ekrandaydı, kayıtta değil:** iki "Okutuldu" satırı insana
iki biniş gibi okunuyordu. Biniş sayısı okutma sayısı değil;
`ReservationStatusHistory`'de `Paid → Boarded` bir kez var. Çözüm ön yüzde
tek satır: **ilk** başarılı okutma binişi yapandır, sonrakiler yeniden
okumadır.

**Ders:** bir alanın adı ("Succeeded") ne ölçtüğünü söylemiyor; ne zaman
`false` yazıldığına bakmadan anlamı bilinemez. Ekranı düzeltmek için
kaydın anlamını kaydırmak, ekranı düzeltir ve kaydı bozar.
→ [[api-gorevler]] `A-134`

## 2026-09-08 · Ekranda toplanacak sayılar, tek tek değil TOPLAMI korunarak üretilir

Ödeme dökümü tur/ek hizmet/indirim/KDV satırlarını alt alta gösteriyor.
Her satır kendi "doğru" formülüyle yuvarlansaydı dört ayrı yuvarlama
birbirini bir kuruş ıskalayabilir ve **ekranda toplamayan bir döküm**
çıkardı.

**Karar:** üç kalem netleştirilip yuvarlanıyor, **KDV artakalan olarak**
bulunuyor (`GrandTotal − net`). Kalem satırlarında da **son kalem
yuvarlama artığını üstleniyor**.

**Neden:** hangi satırın kuruşu üstleneceği bir seçimdir ve vergi satırı,
kalem fiyatlarından daha esnektir. Kullanıcı "kahvaltı 533,33 yazıyor ama
toplamı 533,34 olmalı" demez; "üç sayı toplanmıyor" der.

⚠️ **`MidpointRounding.AwayFromZero` açıkça veriliyor.** .NET'in varsayılanı
bankacı yuvarlaması, Postgres'in `numeric` `round`'u yarımı yukarı yuvarlar;
varsayılan bırakılsaydı aynı rezervasyonun KDV'si SQL'de bir, ekranda başka
bir kuruş çıkardı.

## 2026-09-08 · "Toplam şu artı bu" cümlesi tahsilatı da gösterimi de tarif edebilir

Mert *"tur bedeli + ek hizmet + KDV = genel toplam"* dedi. Bunu **tahsilat
modeli** olarak okudum: ilan fiyatları KDV hariç olacak, müşteri %20 fazla
ödeyecek. `PricingService` değiştirilmeye, `CK_Reservations_GrandTotal` için
migration planlanmaya başlandı. Kastı **yalnız o ekrandaki gösterimdi.**

**Neden yanılttı:** iki farklı şey aynı cümleyle söyleniyor ve aradaki fark
kelimede değil BEDELDE — biri CSS kadar ucuz, diğeri fiyat, ödeme, fatura,
komisyon ve hakediş demek.

**Kural:** bir cümle para AKIŞINI mı yoksa para GÖSTERİMİNİ mi değiştiriyor,
koda dokunmadan önce sorulur. Ayırt edici soru şu: *"müşterinin ödediği tutar
değişiyor mu?"* — cevabı hayırsa bu bir ekran işidir.

Yanılgının ucuz kapanmasının sebebi, değişikliği yapmadan önce **kapsamı
ölçüp yazmış olmam**: "müşteri ilan fiyatının %20 fazlasını öder" cümlesini
görünce Mert hemen düzeltti. Ölçüm, yanlış anlamayı koda dönüşmeden yakaladı.

## 2026-09-08 · Bir alanın süzgeçte olması, izdüşümde olduğu anlamına gelmez

`SupportTicketMessage.IsInternal` sorguda **süzüyordu**
(`isPlatformStaff || !m.IsInternal`) ama izdüşüme hiç girmiyordu. Yani
kural işliyordu, **sonucu görünmüyordu**: personelin ekranında iç not ile
müşteriye gitmiş yanıt birebir aynıydı.

**Neden fark edilmedi:** süzgecin testi vardı ve yeşildi — "müşteri iç notu
görmüyor, personel görüyor" doğru ölçülüyordu. Eksik olan şey görünürlük
değil **ayırt edilebilirlikti**, ve onu ölçen hiçbir test yoktu.

**Ders:** bir bayrak sorguda kullanılıyorsa, o bayrağın **dışarı da
dönmesi gerekip gerekmediği** ayrı bir sorudur. "Süzüyoruz" ile
"gösteriyoruz" farklı işler; birincisinin testi ikincisini kapsamıyor.

⚠️ Testin doğru kurulması da ayrı bir iş: yalnız iç notun `true` döndüğünü
ölçmek yetmez, aynı talepte müşteriye GİDEN bir personel yanıtının `false`
döndüğü de ölçülmeli — yoksa her personel mesajına `true` yazan kod da
geçer. → [[api-gorevler]] `A-137`

## 2026-09-08 · Demo veri "var" olmakla sınamaz, ARTIK üretmesi gerekir

Ön yüz "ek hizmetli bir rezervasyon" istedi. Ayşe'nin her zamanki teknesinin
ek hizmet fiyatları 150/450/1200 ve **üçü de 1,2'ye tam bölünüyor** — o
teknede hangi kalem seçilirse seçilsin kuruş yuvarlaması hiç sınanmıyor.

Tekne, artık üreten fiyatı olan Deniz Kızı ile değiştirildi (280×1 → 233,33
ve 320×2 → 533,33, ama toplamın neti 766,67).

**Neden:** demo verinin işi ekranı DOLDURMAK değil, korumayı **çalıştırmak**.
"Ek hizmet var" bir varlık ölçüsü; "yuvarlama artığı var" bir davranış
ölçüsü. Birincisiyle yetinen demo veri, ikinci sınıf kusurları sessizce
gizler — bu, günün ilk kararının (*"boş ya da tek çeşit veri kusuru gizler"*)
bir adım incelmiş hâli: **tek çeşit olmayan ama hepsi aynı köşeye düşen**
veri de gizler.

## 2026-09-08 · Sayfa zarfı `totalCount`; istisna kendi ucumdu

Ön yüz ölçtü: panelin sayfalı şemalarının **12'si `totalCount`**, **2'si
`total`** — ve ikincilerden biri aynı gün yazdığım `PlatformStaffPage`'ti.
Ayrışmayı ekleyen bendim. Çoğunluğa çekildi (`c7da3b3`).

**Neden önemliydi:** bedeli sessiz. Alışkanlıkla `totalCount` yazan bir ekran
`undefined` okur, toplamı 0 sanır, sayfa sayısını **hep 1** hesaplar ve
sayfalama hiç görünmeden kaybolur. Dört kayıtlık bir listede fark bile
edilmezdi — kusur ancak liste büyüdüğünde, yani en kötü anda çıkardı.

⚠️ Kalan tek istisna `BlogListResponse` (`total`); daha eski ve
dokunulmadı. **Bilerek bırakıldı**, çünkü onu değiştirmek çalışan bir ekranı
kırar; ama ayrışma yazılı olmalı ki bir sonraki uç yanlış tarafa
kopyalanmasın.

**Ders:** ad tutarlılığı kozmetik değil. Aynı kavramın iki adı olduğunda,
yanlış olanı yazan istemci **hata almaz** — sessizce yanlış davranır.

## 2026-09-08 · Demo veri ekranın DALLARINI dolaşmalı, satırlarını değil

Personel ekranının üç dalı vardı ve **üçü de hiç çalışmıyordu**, çünkü dört
demo personelin dördü de yönetici ve hepsi tek rollüydü:

| Dal | Görünmüyordu çünkü |
|---|---|
| `support` dolu | kimsede destek rolü yoktu |
| ortalama `null` ama nesne dolu | yanıtsız talebi olan destek personeli yoktu |
| `roleNames` çoğul | kimsenin ikinci rolü yoktu |

Üç personel eklendi (Selin, Kerem, Deniz) ve her biri **bir dalı** açıyor.

**Neden:** demo verinin işi ekranı doldurmak değil, **kodun her yolundan bir
kez geçmek**. "Personel listesi dolu" bir satır ölçüsü; "üç dalın üçü de
çalıştı" bir yol ölçüsü.

Bu, günün en çok tekrarlayan dersinin beşinci hâli — ve her seferinde biraz
daha inceldi: önce *boş tablo*, sonra *tek çeşit veri*, sonra *hepsi aynı
köşeye düşen veri* (`A-136`, ek hizmet fiyatlarının hepsinin 1,2'ye tam
bölünmesi), şimdi *kodun bir dalına hiç uğramayan veri*.

## 2026-09-08 · Çalıştırılmış migration düzenlenmez, yenisi yazılır

`A03_YetkiKatalogu`'nun tohum verisi ASCII'ye indirgenmişti. Düzeltme, o
dosyayı değiştirerek DEĞİL yeni bir migration (`A111`) ile yapıldı.

**Neden:** çalıştırılmış bir migration'ı düzenlemek, onu zaten uygulamış
veritabanlarında **hiçbir şey yapmaz** — `__EFMigrationsHistory` o kaydı
görür ve atlar. Geliştirici kendi veritabanını sıfırdan kurduğu için
"düzeldi" sanır; üretim bozuk kalır ve bu ancak aylar sonra fark edilir.

Uyarı web oturumundan geldi ve doğruydu.

⚠️ **`Down` bilerek boş.** Geri alma, doğru yazılmış isimleri bozuk
hâllerine döndürmek olurdu. Şema değişmediği için teknik bir gerekçesi de
yok — iskeletin **boş üretilmiş olması** bunun kanıtı: EF hiçbir şema farkı
bulamadı, dosya yalnız veri düzeltiyor.

## 2026-09-08 · Yazılan ama okunmayan veri bayatlar ve kimse duymaz

Yetki adları 24 Ağustos'ta yazıldı, 8 Eylül'e kadar **hiçbir ekran onları
basmadı** ve iki hafta boyunca bozuk durdular. Hata vermediler, test
düşürmediler, kimse şikâyet etmedi — çünkü okuyan yoktu.

Aynı gün ikinci örneği: `Voyages.DepartureDate` ile `StartsAt`, 68 seferin
4'ünde farklı gün söylüyordu ve **farklı ekranlar farklı alanı okuduğu**
için tutarsızlık ancak ikisini birden kullanan bir iş çıkınca göründü.

**Neden:** bir alanın doğruluğu, onu okuyan bir yol olduğunda ölçülür.
Yazılıp okunmayan alanda "doğru" ile "bozuk" ayırt edilemez — hiçbir kanal
farkı bildirmez. Bu yüzden yeni bir ekran eski bir alanı ilk kez bastığında
**o alan doğrulanmamış sayılmalı**, çalışıyor varsayılmamalı.

**Ders:** bir alanın doğruluğu, onu okuyan bir yol olduğunda ölçülür.
Yazılıp okunmayan alan için "doğru" ile "bozuk" ayırt edilemez hâldedir;
ilk okuyucu geldiğinde bulduğu şey veridir, kusur değil — kusur zaten
oradaydı. → [[api-gorevler]] `A-139`

## 2026-09-08 · Derleyici koruyamıyorsa test korur — sözlük sunucuda kalır

77 olay türünün okunur karşılığı **sunucuda** tutuluyor, ön yüzde değil.

**Neden:** ön yüzdeki bir çeviri tablosunu hiçbir şey koruyamaz — olay
türleri belgede enum değil, düz dize. 78. tür eklendiği gün ekranda ham
İngilizce belirir ve **kimse fark etmez**. Aynı gerekçe yetki adlarında da
işlemişti (`A-139`): sözlük yerine `name` göndermek sorunu kökten kaldırdı.

⚠️ **Ama sunucuda da derleyici koruyamıyor:** `EventTypes` bir
`const string` sınıfı, `switch` bütünlüğü zorlanamıyor. Koruma bu yüzden
bir **teste** taşındı: bütün sabitler yansımayla okunuyor, her birinin
başlığı olduğu doğrulanıyor, ve **ters yön** de ölçülüyor — sözlükte
`EventTypes`'ta karşılığı olmayan anahtar kalamaz.

**Ders:** "derleyici zorlayamıyor" ile "koruma yok" aynı şey değil.
Yansımalı bir test, enum'un verdiği garantinin çalışma zamanı karşılığını
üretir; tek koşulu, testin **kaynağı koddan okuması** — elle yazılmış bir
liste ile karşılaştırsaydı ikinci bir bakım noktası olurdu.

## 2026-09-08 · Denetim kaydında `read | write` yetmez, üçüncüsü `denied`

Web oturumu olayları `read | write` diye ikiye ayırmamı istedi. Üçe
ayrıldı: `Read` · `Write` · `Denied`.

**Neden:** red ve başarısızlık olayları (`PlatformDenied`, `LoginFailed`,
`BoardingFailed`) ikisinden de değil — hiçbir şeyi değiştirmiyorlar ama
"bakma" da değiller. `Write` sayılsalardı ekran "bu personel şunu
değiştirdi" derdi; `Read` sayılsalardı "yalnızca baktı" derdi. İkisi de
yanlış, ve **reddedilen deneme denetimde en çok bakılası satırdır.**

⚠️ Tanınmayan tür `Write` sayılıyor, `Read` değil: ekranın varsayılan
süzgeci "yalnız değişiklikler" olacak ve bilinmeyen bir olayı okuma saymak
onu o süzgeçten **sessizce** düşürürdü. Yanlış tarafa düşecekse görünen
tarafa düşsün.

## 2026-09-09 · Denetim ekranına giden gövde İZİN listesinden geçer

Personel işlem ayrıntısı olay gövdesini ham göndermiyor; anahtarlar bir
**izin listesinden** geçiyor ve listede olmayan her alan düşüyor.

**Neden:** yasak listesi ("şunları gizle, kalanı göster") gövdeye **yarın
eklenecek** bir alanı kendiliğinden ekrana düşürür ve kimse fark etmez.
Denetim ekranı, sızıntının en pahalı olacağı yer — orada varsayılan
"gizle" olmalı, "göster" değil.

⚠️ Gerekçe tahmin değil ölçüm: `AuthService` başarısız girişte kullanıcının
**tam e-postasını** gövdeye yazıyor. `NormalizeEmailForLog` biçim
doğruluyor, **maskelemiyor**. Yasak listesi kurulsaydı bu alanı tek tek
hatırlamak gerekirdi; izin listesinde adı geçmediği için zaten düşüyor.

Kimlik taşıyan alanlar (`boatId`, `voyageId`, `onBehalfOf`) da dışarıda —
GUID ekranda hiçbir şey söylemiyor; `subjectLabel` kararının aynısı.

⚠️ **Bu, 2026-09-08'in "payload gönderme" kararını iptal ETMİYOR**, kapsamını
değiştiriyor: ham JSON hâlâ dönmüyor. Dönen şey gövdeden **seçilmiş**,
etiketlenmiş, biçimlenmiş alanlar.

## 2026-09-09 · Aralık verilince sayacın SAYISI değil ANLAMI değişir

Destek sayaçları `from`/`to` ile süzülebiliyor ama **hepsi değil**:

| Sayaç | Aralıktan etkilenir mi |
|---|---|
| `openTickets` | **Hayır** — anlık durum |
| `resolvedTotal` | **Hayır** — tanımı gereği ömür boyu |
| `resolvedInRange` | Evet |
| ortalama ilk yanıt | Evet, aralıkta **AÇILAN** talepler üzerinden |

**Neden:** "açık talep" bir dönemin olayı değil, bir andır — bugün açık
duran talep hangi aralığa bakılırsa bakılsın bugün açıktır. Aralığa göre
süzülseydi sayı doğru, **anlamı yalan** olurdu: "geçen ay kaç talep açıktı"
gibi cevaplanamayan bir soruyu cevaplıyormuş gibi görünürdü.

Ortalamanın aralıkta **açılan** taleplerden alınmasının sebebi ayrı: "ilk
yanıt süresi" açılıştan ölçülüyor; aralık dışında açılmış bir talebi içeri
almak, süreyi aralığa ait olmayan bir başlangıçtan hesaplamak olurdu.

⚠️ Bu ayrımı **testin ölçtüğünden emin olmak ayrı bir iş oldu:** ilk sürümde
açık taleplerin hepsi aralığın içindeydi, dolayısıyla sayacı aralığa göre
süzen bir mutasyon testten geçti. Aralığın DIŞINDA açılmış, hâlâ açık bir
talep eklenince koruma gerçekten ölçmeye başladı.

## 2026-09-09 · Etiketi çevirip değeri bırakmak yarım çeviridir

Olay ayrıntısında alan **etiketleri** Türkçeleştirilmişti ama **değerler**
ham geçiyordu. Ekranda şöyle görünüyordu:

    İşlem     moderation.publish          ← ham
    Sebep     İnceleme aşamasında değil   ← çevrilmiş

**Neden önemli:** yarım çeviri, okuyanı etiketin hiç çevrilmemiş olması
kadar yanıltır — üstelik daha sinsi, çünkü satırın yarısı Türkçe olduğu
için "çevrilmiş" görünür ve gözden kaçar.

`action`, `stage` ve `resource` için de sözlük eklendi.

⚠️ **Bu kümeler de kapalı DEĞİL ve ölçüldü:** veritabanındaki 17 `action`
değeri ile kodda literal olarak bulunan 16 değer **aynı küme değil** —
bazıları değişkenden geliyor. `reason` gibi, tanınmayan değer ham geçiyor
ve `EventTitles`'daki bütünlük testinin karşılığı burada kurulamıyor.

⚠️ **Kusuru ne derleme, ne test, ne uçtan bakmak yakaladı** — hepsinde
`moderation.publish` geçerli bir dizeydi. Ekranda, bir cümlenin ortasında
göründü. Web oturumu 401 aldığı için ekranı göremiyor; bu sınıf kusuru
yalnız tarayıcıya bakan taraf bulabiliyor.

## 2026-09-09 · Çelişkili iki parametre reddedilir, biri sessizce seçilmez

`period` ile `from`/`to` birlikte gelirse uç `400 PeriodAndRange` veriyor.
Web oturumu "aralık kazansın, dönem yok sayılsın" önerdi.

**Neden reddedildi:** sessiz seçim, istemcinin **gönderdiği ama
uygulanmayan** bir parametre bırakır. Ekranda "bu ay" çipi seçili
görünürken veri başka aralıktan gelir; hata yok, uyarı yok, fark eden yok.

Ayrıca bu kod tabanının deseni zaten reddetmek: `UnknownStatus`,
`UnknownPeriod`, `InvalidRange` — hepsi hata veriyor, varsayılana
düşmüyor. Burada sessiz seçmek, deseni tam da en çok gerektiği yerde
delerdi.

⚠️ Serbest aralıkta dönem adı **`custom`** dönüyor, `null` değil: `null`
"hiç seçim yok" ile karışırdı ve ekran hangi seçimin uygulandığını
bilemezdi.

## 2026-09-09 · Aynı kavramın iki adı, ekranda iki okuma yolu demektir

Müşteri ayrıntısı `periodStart`/`periodEnd`, personel ayrıntısı
`rangeStart`/`rangeEnd` diyordu — **aynı işi yapan iki ad**. Personel ucu
bir günlüktü, o değiştirildi.

**Neden:** ön yüzün iki uçtan aynı bilgiyi iki farklı adla okuması, her
yeni ekranda "bu uç hangisini kullanıyordu" sorusunu doğurur ve o soru
derlemede sorulmaz. `totalCount`/`total` ayrışmasının (2026-09-08) aynısı;
orada da bedeli sessizdi.

⚠️ Ama **varsayılanlar bilerek farklı bırakıldı**: müşteride `all`,
personelde `month`. Birleştirme adların birleştirilmesidir, davranışların
değil — ekranların soruları farklı ("bu müşteri toplam ne harcadı" ile "bu
personel bu ay ne yaptı") ve tek varsayılan birini anlamsız yapardı.

## 2026-09-09 · Yöneticinin belirlediği parolayı iki kişi bilir

`POST /api/platform/staff` yeni hesabı yönetici tarafından belirlenen bir
parolayla açıyor. Sistemde **"ilk girişte değiştirmeye zorla" diye bir
kavram yok** ve bu uç onu icat etmedi.

**Neden icat edilmedi:** böyle bir bayrak, giriş akışını, parola değiştirme
ekranını ve jeton üretimini birlikte ilgilendirir — uçtan tek başına
eklenen bir alan, hiçbir yerde uygulanmayan bir söz olurdu. Yarım bir
koruma, olmayandan kötü: ekranda "değiştirmesi istenecek" yazarken
değiştirilmezse kimse fark etmez.

⚠️ **Risk yazılı olarak duruyor** (sözleşme ve uç belgesinde): personel
parolasını değiştirmezse, hesabına erişebilen ikinci bir kişi kalıcı olarak
var olur. Web oturumu bayrağı önerdi; karar Mert'te.

## 2026-09-09 · "Kimsenin dokunmadığı yıl" ölçülür, varsayılmaz

Paylaşılan Testcontainers veritabanında yeni testlerin yarattığı
kullanıcılar `OverviewTests`'in dönem sayacını bozdu (beklenen 2, görülen 4).

İlk düzeltme sabit saati 2031'e taşıdı ve **durumu kötüleştirdi** (4 → 20):
`OverviewTests` de 2031'i kullanıyor ve YIL penceresi hepsini yuttu.
Takımdaki yıllar sayıldı — 2026 (27 yer), 2031 (11), 2027 (1) — ve boş olan
2034 seçildi.

**Neden iki kez yanlış:** "başka test bu yılı kullanmıyor" bir varsayımdı ve
iki kez ölçülmeden yapıldı. Üstelik ikinci kez, düzeltmenin kendisi kusuru
büyüttü.

⚠️ İkinci ders daha ince: **üretim yolundan yazılan kayıt da sahte saati
taşıyor.** Testin elle kurduğu satırların tarihini değiştirmek yetmedi,
çünkü asıl kullanıcılar servisin `clock.UtcNow`'undan doğuyordu.

## 2026-09-09 · `Closed` paneleden yazılmaz — aynı kelime iki anlam taşıyamaz

Personel durum ucu yalnız `Active` ↔ `Suspended` kabul ediyor; `Closed`
hiç alınmıyor.

**Neden:** `Closed` bugün hesap silme akışının (`AnonymizationRepository`)
çıktısı ve o yol kişisel veriyi **anonimleştiriyor**. O yoldan kapanmış bir
hesabı `Active` yapmak, içi boşaltılmış bir hesabı diriltmek olurdu.
Panelden yazılan `Closed` ise geri dönüşlü olurdu — yani aynı enum değeri
biri geri alınamaz, diğeri alınabilir **iki farklı şey** demeye başlardı ve
ekranda ayırt edilemezdi.

Web oturumu bunu sordu ("geri dönüşlü mü, değilse onay diyaloğu göstermem
gerek") ve soru cevabı üretti: ayırt edilemeyecek bir değeri hiç kabul
etmemek, onay diyaloğu göstermekten temiz.

## 2026-09-09 · Küresel bir değişmez, paylaşılan veritabanında yalıtılmadan ölçülemez

"Sistemde `staff.manage` taşıyan son kişi" bir **küresel** değişmez.
İlk yazdığım test onu ölçmüyordu ve **yeşildi**: paylaşılan Testcontainers
veritabanında başka testlerin bıraktığı yöneticiler sayıyı hep 1'in üstünde
tutuyor, kapı hiç ateşlenmiyordu.

**Neden tehlikeli:** test yeşil, koruma yazılı, mutasyon yapılmasa kimse
fark etmez. Kapının kaldırıldığı mutasyon da yeşil kalırdı — yani testin
kendisi bir koruma değil, koruma **görüntüsüydü**.

**Çözüm:** ölçümden önce testin dışındaki bütün aktif yetki sahiplerini
askıya almak. Küresel değişmezin testi, ölçüm penceresini kendisi
kurmak zorunda.

⚠️ Bu, "ölçüm penceresini boş yıla taşımak" (2026-09-09, `A-145`) ile aynı
ailenin üçüncü örneği: paylaşılan veritabanı, testin ölçtüğünü sandığı şeyi
sessizce değiştiriyor.

## 2026-09-09 · Sistem rolleri panelden hiç düzenlenemez — adları bile

`platform.admin` ve `platform.support` için `PUT` ve `DELETE`
`SystemRoleImmutable` dönüyor. Yalnız yetkileri değil, **adı** da kilitli.

**Neden:** ölçüldü. Beş migration bu rolleri `Key` üzerinden bulup yeni
yetki bağlıyor (`WHERE r."Key" = 'platform.admin'`), ve `A111` (2026-09-08)
rollerin **adlarını migration'dan yeniden yazdı**. Panelden düzenlenebilseydi
aynı alanın iki yazarı olurdu ve çakışmayı migration **sessizce** kazanırdı:
yönetici adı değiştirir, bir sonraki migration geri alır, kimse sebebini
bilmez. Yetkilerde de aynısı — panelden kaldırılan bir yetkiyi sonraki
migration geri bağlar.

Web oturumu "adı değişebilir, yetkileri değişmemeli" önerdi; ölçüm daha
katı bir cevap verdi. Ad da üretilen bir alan; üretilen alan elle
yazılmaz → [[genel-desenler]]

⚠️ Kısıtın bedeli var ve kabul edildi: farklı yetkili bir yönetim rolü
isteyen, **yeni rol tanımlıyor**. Zaten tasarım o.

## 2026-09-09 · Ateşlenemeyen kapı hiç yazılmaz

Rol düzenlemede `LastAdmin` kapısı **bilerek yok**. Çağıranın `staff.manage`
yetkisi kesin var (uçtaki süzgeçten geçti). Rolden o yetki kalkarken iki
ihtimal var: çağıran yetkiyi başka bir rolden de alıyor — o hâlde sistemde
en az bir yönetici kalıyor; ya da almıyor — o hâlde `CannotModifySelf`
ateşleniyor. Üçüncü ihtimal yok, yani `LastAdmin` bu yolda **hiç
çalışamazdı**.

**Neden:** `A-150`'de küresel bir değişmezi yalıtmayı öğrendik. Bir adım
sonrası bu: hiçbir mutasyonun kırmızıya döndüremeyeceği bir dal yazmak,
korumayı artırmıyor — **ölçülemeyen kod ekliyor**. Aynı gerekçeyle rol
silmede de ayrı bir yönetim kapısı yok: `RoleInUse` dolu rolü zaten
engelliyor ve boş bir rolün silinmesi kimseden yetki almıyor.

Simetri bir gerekçe değildir. `A-150`'de iki kapı vardı diye buraya da iki
kapı koymak, ikincisini süse çevirirdi.

## 2026-09-09 · Ekrana basılan sayı ile silme kapısının sayısı ayrı — ve ayrı kalmalı

Rol ayrıntısındaki `assignedStaffCount` **görünür** personeli sayıyor
(anonimleştirilmiş hesap hariç); silmeyi engelleyen `RoleInUseAsync` ise
**her** `UserRoles` satırına bakıyor.

**Neden:** iki sorunun cevabı gerçekten farklı ve tek sayıya indirmek
ikisinden birini bozar.

- Ekrandaki sayı **listeyle** aynı kişileri saymalı. Saymasaydı "3
  personelde kullanılıyor" yazarken `?roleId=` süzgeci 2 satır döndürürdü
  ve okuyan listenin bozuk olduğunu sanardı. Web oturumu tam bu soruyu
  sordu ve cevabı ilk hâlinde HAYIR'dı — soru kusuru buldu.
- Silme kapısı **yabancı anahtarla** aynı şeye bakmalı. Kapatılmış hesabın
  `UserRoles` satırı duruyor; görünür sayıya bakan bir kapı o rolü
  silmeye kalkar ve kullanıcıya anlaşılır bir hata yerine ham Postgres
  hatası döner.

⚠️ İkincisi işletme tarafında **yaşanmış** bir kusur: orası önce yalnız
aktif çalışanları sayıyordu ve "çalışanı çıkar, sonra rolü sil" akışı
veritabanı hatasıyla patlıyordu → [[api-gerekce-arsivi-application]]

Mesaj da ayrı: görünür personel sıfırken "önce onların rolünü değiştirin"
demek, yöneticiyi var olmayan bir personeli aramaya gönderirdi.

⚠️ **Genel kural:** bir sayı ekrana basılıyorsa **yanındaki listeyle**
aynı ölçütü kullanmalı; bir sayı kapı olarak kullanılıyorsa **arkasındaki
kısıtla** aynı ölçütü kullanmalı. Aynı isimle iki iş yaptırmak, ikisinden
birinin sessizce yanlış olması demek.

## 2026-09-09 · "Rolün personeli" ayrı uç değil, personel listesinin süzgeci

`GET /api/platform/staff?roleId=…` yazıldı; `GET /roles/{id}/staff`
**açılmadı**.

**Neden:** ayrı uç ikinci bir personel listesi demek. Sayfalama, arama ve
durum süzgeci zaten birinde var; ikincisi bunları ya kopyalar ya kaybeder,
ve zamanla ikisi ayrışır — biri askıdakini gösterir, diğeri göstermez.
Süzgeç olunca satır şekli (`PlatformStaffItem`) tek kalıyor ve ön yüz aynı
bileşeni ikinci kez basıyor.

Gerekçe web oturumundan geldi ve ekrandaki karşılığı ölçülmüştü:
`TEKNE_DURUMU`'nun üç, `TALEP_DURUMU`'nun iki kopyası. Bu, o kusurun uç
tarafındaki hâli olurdu.

⚠️ Tanınmayan `roleId` **hata veriyor** (`UnknownRole`), boş liste değil —
tanınmayan `status` ile aynı gerekçe: boş liste "bu rolde kimse yok" diye
okunur, oysa rol hiç yok.

## 2026-09-10 · Çeviri okunan her sorguda dil süzgeci ZORUNLU

`*Translations` tablolarından okuyan her sorgu
`LanguageCode == ContentLanguage.Default` süzgecini taşır.

**Neden:** süzgeçsiz `FirstOrDefault` iki ayrı şeyi birden bozuyor.

- **Yanlış dil:** `en` alfabetik olarak `tr`'den önce geliyor, yani Türkçe
  panelde İngilizce ad görünüyordu (`Day cruise`). Çeviriler vardı — 8 `tr`,
  8 `en` — yazılmış ama okunmamıştı.
- **Kararsızlık:** sırasız bir `FirstOrDefault`'ın hangi satırı döndüreceği
  garanti değil; aynı sorgu başka bir planla başka dili döndürebilir.

Dört platform sorgusu bu hâldeydi: genel bakış tür dağılımı, müşterinin
rezervasyonları, rezervasyon ayrıntısı, platform rezervasyon listesi.
Katalog tarafındaki sorgular (`BoatCatalogRepository`, `FavoriteRepository`)
süzgeci zaten taşıyordu — yani desen vardı, platform tarafı ondan kopmuştu.

⚠️ **Testi iki dilli veri ister.** Tek dilli veriyle süzgeci tamamen kaldıran
kod da geçer: seçilecek tek satır zaten doğru dildedir. Üretimde iki dil var,
testte de olmalı → [[api-desenler]]

## 2026-09-10 · Tur türü süzgeci katalog türüne bakar, teknenin satış kaydına değil

`?rentalTypeId=` süzgeci `Reservations.BoatRentalType.RentalTypeId`
üzerinden çalışır, `Reservations.BoatRentalTypeId` üzerinden değil.

**Neden:** `BoatRentalType` tekne **başına** bir satır — "şu tekne bu türü
şu para biriminden satıyor" demek. Süzgeç ona baksaydı "Günlük tekne turu"
seçildiğinde yalnız tek teknenin turları gelirdi ve yönetici eksik listeyi
tam sanırdı; hiçbir yerde hata görünmezdi.

⚠️ Kusur **ancak paylaşılan türle** ölçülebiliyor. `TestData.CreateBoatAsync`
her çağrıda yeni bir katalog türü üretiyor; o veriyle iki yanlış kod da aynı
sonucu verir. Test bu yüzden aynı türü satan ikinci bir tekne kuruyor.
Üretim verisi de öyle: `Günlük tekne turu` üç teknede, iki işletmede.

Aynı aile: "her kişinin tek rolü olduğu veri, çoklu rol dalını hiç
sınamıyordu" (2026-09-08).

## 2026-09-10 · Platform panelinin çeviri sorguları dil parametresi ALMIYOR — bilinen sınır

Bugün düzeltilen dört sorgu `ContentLanguage.Default`'a **sabit**. İstek
dilini kabul eden `LookupRepository` deseni (istenen dil → bulunamazsa
varsayılan) buraya uygulanmadı.

**Neden:** platform paneli için dil parametresi bugün **hiçbir uçta yok**.
Sabitlemek, olmayan bir kavramı dört sorguda icat etmekten temiz; parametre
eklenseydi hiçbir çağıran onu göndermez ve varsayılana düşerdi — yani aynı
davranış, üstüne kullanılmayan bir parametre.

⚠️ **Ne pahasına:** panel bir gün İngilizce desteklerse bu dört ekran Türkçe
kalır, `GET /api/lookups` İngilizceye geçer ve **kutu ile tablo ayrışır**.
Kusur o gün ekranda görünür; bugün görünmez.

Sınır yazılı olsun diye burada: panelde dil seçimi gündeme geldiğinde
yapılacak iş, dördünü `LookupRepository` desenine çevirmek.
→ [[api-kararlar]] 2026-09-10 (dil süzgeci zorunlu)

## 2026-09-10 · Yukarıdaki sınırın tetikleyicisi düzeltildi — ölçüm web oturumundan

Az önceki girişte tetikleyiciyi *"panel bir gün İngilizce desteklerse"* diye
yazmıştım. Web oturumu ön yüzü ölçtü ve tetikleyici bundan **bir adım
öncesi** çıktı: **ön yüzün `lang` göndermeye başlaması.**

Ölçüm (2026-09-10): uçta 9 işlem dil parametresi kabul ediyor; ön yüz bunu
yalnız iki yerde ve **sabit `"tr"`** olarak kullanıyor. `lookups` iki yerden
çağrılıyor ve **hiçbirinde `lang` gönderilmiyor**; `dcFetch` de
`Accept-Language` eklemiyor.

**Sonucu, benim yazdığımdan daha güçlü:** bugün ayrışma "olası değil" değil,
**mümkün değil**. İki taraf da soruyu sormadığı için ikisi de aynı sunucu
varsayılanında buluşuyor. Ayrışma ancak bir taraf sormaya başlayınca doğar.

**Neden önemli:** yanlış tetikleyici, sınırı yanlış kişiye havale ediyordu.
"Panel İngilizce desteklesin" büyük ve uzak bir iş gibi duruyor; "ön yüz
`lang` göndersin" ise **tek satır** ve yarın olabilir. Sınırın ne zaman
patlayacağını yanlış tahmin etmek, sınırı yazmamakla neredeyse aynı.

Yayın koşulu olarak `Y-15` (web oturumu yazdı), kabul ölçütü iki parçalı:
dört sorgu parametreli hâle gelmeli **ve** ön yüzdeki iki sabit `"tr"`
seçili dile bağlanmalı. Biri eksikse ekran sessizce iki dilli olur.

⚠️ Ders: bir sınır yazarken *"ne zaman patlar"* sorusunun cevabı da
ölçülmeli. Ben kendi tarafımdan bakıp tahmin ettim; doğru cevap **karşı
tarafın kodundaydı**.
