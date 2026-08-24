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

- [ ] **A-10** Uygulama için ayrı, en az ayrıcalıklı veritabanı rolü · öncelik: orta
      Bugün uygulama rolü `dailycruising` **tabloların sahibi**. 6. bölümdeki "para
      defteri tetikleyiciyle değişmez" iddiası ancak sahip OLMAYAN bir rolle geçerli —
      sahip `ALTER TABLE ... DISABLE TRIGGER` diyebilir
      Bağımlı: 6. bölüm migration'ından ÖNCE · Kabul: uygulama rolü tetikleyiciyi
      devre dışı bırakamıyor, migration ayrı rolle çalışıyor
- [ ] **A-09** Kalan yedi bölümün entity'leri ve migration'ları · öncelik: yüksek
      Bağımlı: A-02 · Bölüm bölüm ilerlenecek, hepsi tek migration'da değil
      Sıra: 2 katalog · 3 fiyat · 4 takvim+sefer · 5 rezervasyon · 6 para ·
      7 teklif+mesajlaşma · 8 yan sistemler
      4. bölümde `EXCLUDE USING gist` kısıtı EF ile kurulamaz, **elle SQL** gerekir
      Kabul: her bölüm ayrı migration, `dotnet ef database update` temiz
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
- [ ] **A-08** Olay günlüğü (event log) · öncelik: yüksek
      Bağımlı: A-01 · **Ertelenemez** — analiz sonra yapılır ama veri geçmişe dönük
      üretilemez. Değişmez ve append-only, para defteriyle aynı mantık
      Kaydedilecek: arama · tekne görüntüleme · terk edilen ödeme · mesaj · destek
      talebi · yorum · iptal · kupon · teklif
      Kabul: zaman aralığı + tür ile sorgulanabilir, kararlı kimlik taşır (n8n
      dışarıdan tüketebilsin) -> [[domain-gereksinimler]] "veri önce, entegrasyon sonra"
- [ ] **A-07** OpenAPI'den frontend tip üretimi
      Bağımlı: A-01 · Kabul: web tarafı elle tip yazmaz

## 🟡 Yapılıyor

_(boş)_

## 🟢 Tamamlandı

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
