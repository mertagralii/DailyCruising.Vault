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

- [ ] **A-02** EF Core + PostgreSQL kurulumu ve ilk migration · öncelik: yüksek
      Bağımlı: A-01 · Kabul: `dotnet ef database update` temiz, tablo adları
      PascalCase çoğul -> [[api-desenler]]
- [ ] **A-03** Kimlik doğrulama + **dinamik rol/yetki** + satır bazlı kapsam · öncelik: yüksek
      ⚠️ "6 rol" ifadesi **eskidir**. Roller kodda sabit DEĞİL, veritabanı kaydıdır —
      yeni rol açmak ve yetki eklemek kod değişikliği gerektirmez ([[domain-gereksinimler]]
      2026-08-22). Başlangıç rolleri: platform yönetimi, tekne sahibi, müşteri, destek
      İki ayrı boyut: **ne yapabilir** × **kimin verisinde**. İkincisi iş ortağından
      otomatik türer, elle atanmaz
      İş ortağı sahibi kendi çalışanlarını tanımlar ve yetkilerini kısar (devredilmiş yönetim)
      Kabul: iş ortağı yalnız kendi kayıtlarını görür; panel uçları kimliksiz 401
      Not: web tarafındaki panel rotaları şu an herkese açık -> [[durum]]
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

- [ ] **A-01** Veritabanı şemasının sekiz bölümde çıkarılması · öncelik: yüksek
      **Başlandı 2026-08-24** — 8/8 bölüm çıkarıldı; 1-5 Mert onaylı, 6-8 toplu onay bekliyor -> [[api-sema]]
      Bağımlılık **kalktı** — G-01 tamamlandı, şemayı bloke eden madde yok
      Bölümler: 1 kimlik/yetki · 2 katalog · 3 kiralama tipi+fiyat · 4 takvim+sefer
      (en kritik) · 5 rezervasyon · 6 para · 7 teklif+mesajlaşma · 8 yan sistemler
      Her bölüm Mert'in onayından geçer; **onaysız kod yazılmaz**
      Kabul: entity ve ilişkiler [[domain-gereksinimler]] ile birebir örtüşür,
      çıkarım kalmaz; her varlık için "hangi olaylar kaydediliyor" sorusu cevaplanır

## 🟢 Tamamlandı

- [x] **A-00** Backend iskeleti: .NET 10, Clean Architecture 4 katman, health ucu · bitti: 2026-08-21
      Kanıt: `dotnet build` 0 uyarı 0 hata · `GET /api/health` -> `{"status":"healthy"}`

İlgili: [[api-desenler]] · [[api-kararlar]] · [[api-mimari]] · [[durum]] · [[api-notlar]]
