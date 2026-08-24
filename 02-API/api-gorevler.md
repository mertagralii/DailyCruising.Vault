---
rol: gorev
kapsam: api
guncelleme: 2026-08-24
durum: guncel
---

# API Görevleri

`DailyCruising.Back-End/` işleri. Kimlik öneki **`A-`**, numara geri kullanılmaz.

**Kurallar:** Yapılıyor'da en fazla 3 görev · Tamamlandı'ya taşımak `Kanıt:` satırı
ister · iptal edilen görev silinmez, "iptal" olarak Tamamlandı'ya taşınır.
Biçim ve gerekçe -> [[genel-desenler]]

## 🔵 Yapılacak

- [ ] **A-14** `ensure_event_log_partitions()` icin zamanlanmis is · oncelik: orta
      Bugun 24 ay pesinen acildi ama otomatik uzatma YOK. Cagrilmazsa 24 ay sonra
      her olay varsayilan parcaya yigilir ve bolumlendirmenin faydasi kaybolur
      Varsayilan parcada satir birikirse o aya gercek parca eklenemez, once
      tasinmasi gerekir — yani gecikme kendi kendini pahalilastiriyor
      Kabul: ayda bir calisan bir is var ve calismadiginda goruluyor
- [ ] **A-12** KVKK saklama ve anonimleştirme akışı · öncelik: orta
      `User.AnonymizedAt` alanı açıldı ama akış yok. Hesabın tamamen silinmesi
      **imkânsız**: rezervasyonu veya mesajı olan kullanıcıyı Restrict zinciri
      tutuyor ve tutmalı da (muhasebe ve anlaşmazlık kaydı)
      Kişisel veri şu tablolara kopyalanmış durumda: `Reservations.Contact*`,
      `Passengers.FullName/IdentityNumber`, `Messages.Body`, `EventLogs.Payload`,
      `LedgerEntries.Note` — son ikisi **değişmez**, temizlenemez
      Kabul: "hesabımı sil" talebi tek bir işlemle karşılanabiliyor
- [ ] **A-13** `EventLogs.Payload` içeriğine sınır · öncelik: orta
      Bugün jsonb serbest. Süresiz saklanan ve değişmez bir tabloya serbest metin
      girerse (arama kutusuna yazılan isim veya telefon gibi) **asla temizlenemez**
      Kabul: izin verilen anahtar listesi veya şema doğrulaması var
- [ ] **A-10** Uygulama için ayrı, en az ayrıcalıklı veritabanı rolü · öncelik: orta
      Bugün uygulama rolü `dailycruising` **tabloların sahibi**. 6. bölümdeki "para
      defteri tetikleyiciyle değişmez" iddiası ancak sahip OLMAYAN bir rolle geçerli —
      sahip `ALTER TABLE ... DISABLE TRIGGER` diyebilir
      ⚠️ **Genişletildi 2026-08-24:** boşaltma komutu da engellenmeli. Satır bazlı
      tetikleyiciler o komutta tetiklenmiyordu — canlı doğrulandı, defter tek
      komutla boşaldı. Deyim bazlı tetikleyici eklendi ama asıl çözüm uygulama
      rolünün o yetkiye hiç sahip olmaması
      Bağımlı: 6. bölüm migration'ından ÖNCE · Kabul: uygulama rolü tetikleyiciyi
      devre dışı bırakamıyor ve tabloyu boşaltamıyor, migration ayrı rolle çalışıyor
- [ ] **A-03** Kimlik doğrulama + **dinamik rol/yetki** + satır bazlı kapsam · öncelik: yüksek
      ⚠️ "6 rol" ifadesi **eskidir**. Roller kodda sabit DEĞİL, veritabanı kaydıdır —
      yeni rol açmak ve yetki eklemek kod değişikliği gerektirmez ([[domain-gereksinimler]]
      2026-08-22). Başlangıç rolleri: platform yönetimi, tekne sahibi, müşteri, destek
      İki ayrı boyut: **ne yapabilir** × **kimin verisinde**. İkincisi iş ortağından
      otomatik türer, elle atanmaz
      İş ortağı sahibi kendi çalışanlarını tanımlar ve yetkilerini kısar (devredilmiş yönetim)
      Kabul: iş ortağı yalnız kendi kayıtlarını görür; panel uçları kimliksiz 401
      Not: web tarafındaki panel rotaları şu an herkese açık -> [[durum]]
      ⚠️ **Host header injection:** `AllowedHosts` hâlâ `*`. Parola sıfırlama ve
      e-posta doğrulama linkleri `Request.Host`'tan DEĞİL, sabit yapılandırılmış
      base URL'den kurulacak — yoksa sahte sıfırlama linki üretilebilir
      ⚠️ Jeton karşılaştırması **SHA-256** ile; bcrypt kullanılırsa `WHERE` hiç
      eşleşmez -> [[api-sema]]
      ⚠️ Kapsam sorgusu `PartnerMembers.Status = Active` filtresini unutmamalı;
      benzersiz indeks Status'tan bağımsız, çıkarılmış çalışan satırı duruyor
- [ ] **A-04** Rezervasyon toplamının sunucuda yeniden hesaplanması · öncelik: yüksek
      Bağımlı: A-01 · Kabul: istemciden gelen tutar yok sayılır, sunucu tutarı esas
      Gerekçe güvenliktir; PRD atfı dayanaksız -> [[api-kararlar]] 2026-08-22
- [ ] **A-05** QR biniş doğrulama uç noktası
      Kabul: kod kameradan da klavyeden de gelebilir; istemci detayı uca sızmaz
- [ ] **A-06** Test projesi (xUnit) kurulumu
      Kabul: `dotnet test` çalışır, en az bir gerçek testi vardır
- [ ] **A-08** Olay günlüğünün YAZILMASI · öncelik: yüksek
      ✅ Şema tarafı bitti: `EventLogs` tablosu var, değişmez, aylık bölümlenmiş
      ❌ **Hiçbir olay henüz yazılmıyor** — tablo boş ve boş kalırsa amacı boşa gider
      Yazılacaklar: arama · tekne görüntüleme · **terk edilen ödeme** · mesaj ·
      destek talebi · yorum · iptal · kupon · teklif · giriş ve başarısız giriş
      **Ertelenemez** — analiz sonra yapılır ama veri geçmişe dönük üretilemez
      ⚠️ Sorgular tarih aralığı içermeli, yoksa tüm parçalar taranır -> [[api-kararlar]]
      Kabul: bir uç nokta çağrıldığında ilgili olay `EventLogs`'a düşüyor ve
      zaman aralığı + tür ile sorgulanabiliyor
- [ ] **A-07** OpenAPI'den frontend tip üretimi
      Bağımlı: A-01 · Kabul: web tarafı elle tip yazmaz

## 🟡 Yapılıyor

_(boş)_

## 🟢 Tamamlandı

- [x] **A-11** `EventLogs` aylık bölümlendirme · bitti: 2026-08-24
      Kanıt: `EventLogs` artık bölümlenmiş tablo (`relkind = p`), **26 parça**
      (25 ay + varsayılan), toplam 101 tablo. Bileşik anahtar `("Id","OccurredAt")`
      Kanıt-2: 10 senaryo canlı denendi — doğru parçaya yönlendirme, `Seq` parçalar
      arası artıyor, güncelleme/silme hem üst tablodan hem parçadan reddedildi,
      **boşaltma üç seviyede de reddedildi**, tarih aralığı sorgusu tek parça tarıyor
      Kanıt-3: migration geri alınıp tekrar uygulandı (`p` → `r` → `p`),
      `dotnet build` 0 uyarı 0 hata
      ⚠️ Prototipte bulundu: deyim bazlı tetikleyici parçalara **yayılmıyor**;
      bir ay parçası doğrudan boşaltılabiliyordu. Her parçaya ayrı tetikleyici
      kuruldu -> [[api-kararlar]] 2026-08-24
- [x] **A-09** Kalan yedi bölümün entity'leri ve migration'ları · bitti: 2026-08-24
      Kanıt: **75 tablo** veritabanında · 3 EXCLUDE kısıtı · 5 tetikleyici ·
      `dotnet build` 0 uyarı 0 hata · `GET /api/health` -> 200 `{"status":"healthy"}` ·
      olmayan uç -> 404 · `/openapi/v1.json` -> 200 · uygulama günlüğünde 0 hata
      Kanıt-2: sekiz kısıt senaryosu canlı denendi, sekizi de doğru davrandı —
      Mehmet/Cemil çakışması reddedildi, aynı günün 17:00 turu geçti (yarı açık
      aralık), kapasite aşımı reddedildi, çakışan sezon fiyatı reddedildi,
      ikinci temel fiyat reddedildi, defterde UPDATE ve DELETE reddedildi,
      ticari kapasite yasal kapasiteyi aşamadı
      Kanıt-3: migration **geri alındı ve tekrar uygulandı** (75 -> 14 -> 75) ·
      üretilen SQL okundu, veri kaybı riski 0 · indekssiz yabancı anahtar 0
      -> [[api-kararlar]] 2026-08-24
- [x] **A-02** EF Core + PostgreSQL kurulumu ve ilk migration · bitti: 2026-08-24
      Kanıt: PostgreSQL 18.6 kuruldu ve çalışıyor · `dailycruising_dev` veritabanı,
      dört eklenti (`citext`, `btree_gist`, `unaccent`, `pg_trgm`) ·
      `Bolum1_KimlikVeYetki` migration'ı uygulandı, **13 tablo** oluştu ·
      tablo adları PascalCase çoğul (`Users`, `PartnerMembers`) ·
      `dotnet build` 0 uyarı 0 hata · `GET /api/health` hâlâ `{"status":"healthy"}` ·
      kısıtlar canlı denendi: citext büyük/küçük harf çakışmasını, CHECK %150
      komisyonu **reddetti**
      **Üç ajan denetiminden geçti** (database/csharp/security-reviewer), 17 kusur
      bulundu ve düzeltildi; ikinci migration `Bolum1_GuvenlikTetikleyicileri`
      Kanıt-2: dört saldırı senaryosu canlı denendi ve **dördü de reddedildi** —
      çalışana platform.admin atama · işletme roluna yasak yetki bağlama ·
      UserRoles'a işletme rolü koyma · ikinci platform.admin açma.
      Meşru işlem (kendi rolünü kendi çalışanına verme) geçti
      -> [[api-kararlar]] 2026-08-24
- [x] **A-01** Veritabanı şemasının sekiz bölümde çıkarılması · bitti: 2026-08-24
      Kanıt: sekiz bölümün tamamı [[api-sema]] içinde, hepsi Mert onaylı.
      1-5 tek tek konuşuldu; 6-8 Claude tasarladı, altı açık soru toplu cevaplandı.
      Gerekçeler tarihli olarak [[api-kararlar]] içinde (6 giriş).
      Her bölümde "hangi olaylar kaydediliyor" sorusu cevaplandı -> A-08 girdisi hazır
- [x] **A-00** Backend iskeleti: .NET 10, Clean Architecture 4 katman, health ucu · bitti: 2026-08-21
      Kanıt: `dotnet build` 0 uyarı 0 hata · `GET /api/health` -> `{"status":"healthy"}`

İlgili: [[api-desenler]] · [[api-kararlar]] · [[api-mimari]] · [[durum]] · [[api-notlar]]
