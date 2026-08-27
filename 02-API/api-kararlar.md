---
rol: history
kapsam: api
guncelleme: 2026-08-25
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
