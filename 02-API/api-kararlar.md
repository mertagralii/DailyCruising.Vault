---
rol: history
kapsam: api
guncelleme: 2026-08-21
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
