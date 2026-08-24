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

- [ ] **A-20** Testleri Testcontainers'a taşı · öncelik: düşük
      Bugün yerel PostgreSQL'de `dailycruising_test` veritabanı kuruluyor;
      Docker daemon kapalı olduğu için Testcontainers kullanılamadı
      Bağımlı: CI kurulumu (`G-05`). Bağlantı dizesi ortam değişkeninden
      geldiği için geçiş tek noktada
      Not: `dailycruising` rolüne test için `CREATEDB` verildi; `A-10`'da
      uygulama rolü ayrılırken bu yetki uygulama rolüne VERİLMEYECEK
- [ ] **A-19** `UseForwardedHeaders` yapılandırması · öncelik: **dağıtımdan önce**
      Ters vekil arkasında `RemoteIpAddress` proxy'nin IP'sini döner. Sonuç:
      `CreatedIp` adli izi bozuk, IP bazlı hız sınırı işlevsiz
      ⚠️ `KnownProxies`/`KnownNetworks` doğru verilmezse saldırgan
      `X-Forwarded-For` uydurup istediği IP'yi bildirebilir — iki yönde kırılgan
      Bağımlı: dağıtım mimarisinin belli olması (`G-05`)
      Kabul: ters vekil arkasında gerçek istemci IP'si görülüyor ve sahte
      başlık kabul edilmiyor
- [ ] **A-18** Periyodik hakediş üretimi · öncelik: orta
      `Contracts.PayoutPeriodDays` (varsayılan 14) uyarınca `Payouts` üretip
      `LedgerEntries.PayoutId` bağlayacak iş. **Para kararı** olduğu için
      `A-15`'ten ayrıldı; yanlış çalışması yanlış ödeme demek
      Bağımlı: `G-03` sanal POS seçimi (bölüştürme talimatı oraya gidecek)
      Kabul: dönem kapanınca hakediş oluşuyor, defter toplamı sıfır kalıyor
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
- [ ] **A-22** Rezervasyon oluşturma uç noktası · öncelik: yüksek
      Bağımlı: A-04 · `PricingService` hazır ama onu çağıran bir uç yok
      Kabul: tutar `QuoteAsync` ile YENİDEN hesaplanır, fiyat sorgusunun cevabı
      saklanıp kullanılmaz; `Quote` alanları rezervasyona tek bir üretici
      metotla kopyalanır ki hesap ile saklanan ayrışamasın
      Sefer `Quote.StartsAt`/`EndsAt` ile açılır — çakışmayı EXCLUDE yakalar
      ⚠️ `CountCouponRedemptionsAsync` sayıp karşılaştırıyor, kilit yok. Salt
      okunan fiyat sorgusunda zararsız; BURADA olduğu gibi kullanılırsa iki
      eşzamanlı rezervasyon `MaxRedemptions`'ı aşar -> [[api-kararlar]] 2026-08-24
- [ ] **A-05** QR biniş doğrulama uç noktası
      Kabul: kod kameradan da klavyeden de gelebilir; istemci detayı uca sızmaz
- [ ] **A-21** Kalan olay türlerinin bağlanması · öncelik: orta
      `A-08`'de altyapı ve kimlik olayları bağlandı. Henüz yazılmayanlar:
      arama · tekne görüntüleme · rezervasyon oluşturma · biniş okutma ·
      kupon uygulama ve reddi · yorum · destek talebi · **platform personelinin
      işletme verisine erişimi**
      Çoğu ilgili uç nokta yazılmadığı için bekliyor (`A-04`, `A-05`)
      Kabul: her olay türü için en az bir gerçek çağrı `EventLogs`'a düşüyor
- [ ] **A-07** OpenAPI'den frontend tip üretimi
      Bağımlı: A-01 · Kabul: web tarafı elle tip yazmaz

## 🟡 Yapılıyor

_(boş)_

## 🟢 Tamamlandı

- [x] **A-04** Rezervasyon toplamının sunucuda yeniden hesaplanması · bitti: 2026-08-24
      Kanıt: `POST /api/pricing/quote` canlı çağrıldı. **İstemci `grandTotalTry:1`
      ve `discountAmountTry:9999` gönderdi, sunucu 1000.00 ve 0 döndü** — alanlar
      reddedilmedi, hiç okunmadı çünkü `QuoteRequest`'te yoklar.
      2 yetişkin + 1 çocuk + 1 bebek → 1300.00 TL · %15 komisyonda %10 kupon →
      900 TL, %20 kupon → indirim 0 · 12 kişilik teknede 13 yetişkin → 400
      Denetim dört gerçek açık buldu, dördü de CANLI üretildi ve kapatıldı:
      `int` taşması kapasite kontrolünü atlıyordu (1,6 trilyon TL, HTTP 200) ·
      iki ayrı yoldan HTTP 500 · 200.000 satırlık ek hizmet 26 MB cevap ve
      2 yolcuya 40 milyon TL · kupon aramam `citext` indeksini öldürüyordu.
      Hepsi yeniden denendi → 400. Hız sınırı 61. istekte 429. Production
      kipinde yığın izi sızmıyor. **42 test, 42'si geçiyor**
      Kupon reddinin sebebi artık söylenmiyor -> [[api-kararlar]] 2026-08-24
      `MinPassengers` bilerek kontrol edilmiyor — o sınır sefere ait
- [x] **A-08** Olay günlüğünün yazılması — altyapı ve kimlik olayları · bitti: 2026-08-24
      Kanıt: canlı denendi, dört olay yazıldı — `auth.login.failed` (olmayan
      kullanıcı ve yanlış parola AYRI sebeplerle), `auth.login.succeeded`,
      `account.password_reset.requested`. IP hepsinde **hash'li**
      Kanıt-2: **terk edilen ödeme** yakalandı — süresi dolan rezervasyon
      `payment.abandoned` yazdı: tutar 3000, 2 yetişkin 1 çocuk, **745 saniye**
      sonra vazgeçilmiş. Bu veriyi başka hiçbir tablo tutmuyor
      Kanıt-3: **18 test, 18'i geçiyor** (4'ü olay günlüğü için yeni)
      Kalan olay türleri `A-21`'de; çoğu ilgili uç nokta yazılmadığı için bekliyor
- [x] **A-10** Uygulama için ayrı, en az ayrıcalıklı veritabanı rolü · bitti: 2026-08-24
      Kanıt: `dailycruising_app` rolü oluştu — superuser değil, CREATEDB yok,
      CREATEROLE yok. **Yedi senaryo canlı denendi:** okuma ✓ · yazma ✓ ·
      tetikleyici kapatma **reddedildi** ("must be owner") · tablo boşaltma
      **reddedildi** ("permission denied") · tablo düşürme **reddedildi** ·
      kolon ekleme **reddedildi** · defter güncelleme tetikleyiciyle
      **reddedildi**
      Kanıt-2: uygulama bu role geçirildi, `GET /api/health` 200, giriş 200,
      altı zamanlanmış iş çalıştı, **0 hata**
      ⚠️ `A-15`'in "para defteri değişmezdir" iddiası ancak ŞİMDİ tam geçerli
      -> [[api-kararlar]] 2026-08-24
- [x] **A-06** Test projesi (xUnit) · bitti: 2026-08-24
      Kanıt: **14 test, 14'ü geçiyor**, 0 uyarı. Bugünkü elle doğrulamalar
      kalıcı hale geldi: sefer çakışması, aynı gün peş peşe tur, iptal edilen
      seferin tarihi bırakması, kapasite aşımı, defter güncelleme/silme/boşaltma,
      olay günlüğü parçasının doğrudan boşaltılamaması, üç yetki tetikleyicisi,
      citext e-posta benzersizliği
      Testler **GERÇEK PostgreSQL'e** karşı çalışıyor; bellek içi sağlayıcı
      bilinçli reddedildi — bu şemanın değeri Postgres'e özgü kısıtlarda ve
      bellek içi sağlayıcı onları uygulamaz, testler geçer ve hiçbir şey
      kanıtlamazdı
      ⚠️ Testcontainers tercih edilirdi, Docker daemon kapalıydı -> `A-20`
- [x] **A-16** `Boats.AverageRating` tetikleyicisi · bitti: 2026-08-24
      Kanıt: beş geçiş canlı denendi — beklemede yorumlar ortalamaya **girmedi**
      (boş kaldı) · 5 puan onaylandı -> **5.00 / 1** · 4 puan onaylandı ->
      **4.50 / 2** · 3 puan reddedildi -> **değişmedi** · onaylı yorum geri
      çekildi -> **5.00 / 1**
      ⚠️ Denetimin "iki bölüm zıt söylüyor" bulgusu **yanlış çıktı**: bölüm 2
      genel puandan, bölüm 8 KRİTER bazlı alt puanlardan bahsediyordu. Çelişki
      yoktu; yine de karışmasın diye şema notu netleştirildi
- [x] **A-17** TCMB günlük kur çekme işi · bitti: 2026-08-24
      Kanıt: canlı TCMB bülteninden **3 kur** çekildi ve saklandı
      (24.08.2026 — USD 48,0788 · EUR 56,0948 · GBP 65,6556), `JobRuns`'ta
      başarılı kaydı var
      Kanıt-2: uygulama yeniden başlatıldı, iş tekrar çalıştı, **0 kayıt işledi**
      ve satır sayısı 3 kaldı — tekrar çalışması zararsız
      ⚠️ **Hangi kurun kullanılacağı Mert'e soruldu** — şimdilik `ForexSelling`
      -> [[api-durum]] "Mert'e sorulacaklar"
- [x] **A-15** Zamanlanmış iş katmanı · bitti: 2026-08-24
      Kanıt: **kilitlenme birebir üretildi ve çözüldü.** Terk edilmiş bir ödeme
      12 koltuğu tuttu, yeni rezervasyon `CK_Voyages_SoldSeats` ile reddedildi
      (sefer satılamaz), iş çalıştı, `SoldSeats` **12 -> 0** oldu, aynı sefere
      yeni rezervasyon **kabul edildi**
      Kanıt-2: beş iş de çalıştı ve `JobRuns`'a yazıldı; sağlık ucu yetkisiz
      istekte **401**, platform yöneticisinde beş işi de listeliyor
      Hangfire/Quartz **eklenmedi** — tek `BackgroundService` yeterli
      -> [[api-kararlar]] 2026-08-24
- [x] **A-14** `ensure_event_log_partitions()` zamanlanmış iş · bitti: 2026-08-24
      Kanıt: `olay-gunlugu-parcalari` işi günde bir çalışıyor, `JobRuns`'ta
      başarılı kaydı var. `A-15` kapsamında yapıldı
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
