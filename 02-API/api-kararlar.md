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
