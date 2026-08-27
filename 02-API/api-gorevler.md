---
rol: gorev
kapsam: api
guncelleme: 2026-08-26
durum: guncel
---

# API Görevleri

`DailyCruising.Back-End/` işleri. Kimlik öneki **`A-`**, numara geri kullanılmaz.

**Kurallar:** Yapılıyor'da en fazla 3 görev · Tamamlandı'ya taşımak `Kanıt:` satırı
ister · iptal edilen görev silinmez, "iptal" olarak Tamamlandı'ya taşınır.
Biçim ve gerekçe -> [[genel-desenler]]

> 📌 **MERT'İN CEVAP VERECEĞİ KARARLAR → [[api-benim-kararlarim]]**
>
> `/goal` koşusunda kendi aldığım her geçici karar oraya, gerekçesi ve
> **geri alma bedeliyle** yazılıyor. Damgalar: `[kesin]` ölçüldü ·
> `[makul]` gerekçesi sağlam · `[tahmin]` Mert'in kararı gerekiyor.
> `Mert'e sorulacak:` satırları toplu cevap için bekleyen sorulardır.
> Koşu bitince o dosya baştan sona okunup düzenlemeler yapılacak.

## 🔵 Yapılacak

### Yazılmamış uç grupları — ürün bunlarsız uçtan uca çalışmıyor

> **102 tablo, 27 uç nokta.** 14 domain alanının 4'ünde uç var. Bugün sisteme
> hiçbir tekne girilemiyor ve hiçbir müşteri tekne arayamıyor.
>
> `A-21`'in kalan altı olay türü buraya dağıtıldı — her biri ilgili ucun kabul
> ölçütü. Olay türü tek başına bir görev olamaz, çünkü yazacak bir çağrı yeri
> yok → [[api-benim-kararlarim]]

### Panodaki diğer işler

### Mert'in 2026-08-26 kararlarından doğan işler

> 23 sorunun hepsi cevaplandı; 6'sı onaylandı (kod değişmiyor), **17'si iş
> çıkardı**. Gerekçeler → [[api-benim-kararlarim]]

- [ ] **A-58** Alıcı kaydı olmayan işletmeyi satışa kapat · 🔴 **`A-41`'e BAĞLI** (soru 21)
      ⚠️ Bugün açılamaz: hiçbir işletmenin alıcı kaydı yok, katılaştırma
      **tüm satışı durdururdu**. İyzico pazaryeri özelliği açılıp işletmeler
      onboard edildikten SONRA

- [ ] **A-41** Alt üye iş yeri ve hakediş transferi · 🔴 **MERT'TE** ·
      öncelik: **yüksek**

      🔔 **MERT'E HATIRLATILACAK — İYZİCO GÖRÜŞMESİ**
      İyzico'dan hesaba **pazaryeri (marketplace) özelliğinin açılması**
      istenecek. Sandbox ve üretim hesabı için ayrı ayrı sorulmalı.
      Ölçüm: `POST /onboarding/submerchant` → `2000 — Bu servis sadece
      pazaryeri müşterilerine açıktır`; `/detail` → `2001` (okuma açık,
      yaratma kapalı). Üç farklı gövdede aynı hata → kapı hesapta

      **2026-08-26: SÜREÇ AKAR HÂLE GETİRİLDİ** (Mert: *"şu anki süreçte
      çalışıyormuş gibi olsun"*)
      `IPaymentProvider.RegisterPayeeAsync` + `POST /api/platform/partners/{id}/payee`
      Sahte sağlayıcı gerçek bir anahtar üretiyor → bölüştürme akışı uçtan
      uca çalışıyor, geliştirme ve test durmuyor
      İyzico sağlayıcısı çağrıldığında **engeli açıkça söylüyor**, sessizce
      başarılı dönmüyor
      Kanıt: alıcı kaydı canlıda açıldı (`fake-payee-…`), ikinci kez
      `400 PayeeAlreadyRegistered`

      🔔 **UYGULAMA HER AÇILIŞTA HATIRLATIYOR:** hiçbir işletmenin alıcı
      kaydı yoksa `A-41 BEKLİYOR` uyarısı düşüyor. Kanıt: kayıt varken
      **0**, yokken **1** kez yazıldı — uyarı kendiliğinden susuyor,
      elle kaldırılacak bir şey bırakmıyor

      ⚠️ **Bugün para hâlâ işletmeye gitmiyor.** Tahsilat platform
      hesabında, hakediş defterde; transfer ELLE. Pazaryeri açıldığında
      değişecek TEK şey `IyzicoPaymentProvider.RegisterPayeeAsync` gövdesi
      Kabul: sandbox'ta gerçek bir alıcı kaydı açılıyor, ödeme ona bölünüyor

- [ ] **A-07** OpenAPI'den frontend tip üretimi · **kapsam daraldı**
      API yarısı bitti (`A-07a`): `openapi.json` repoda, bayatlaması test edilir.
      **KALAN, ve bu oturumun işi DEĞİL:** web tarafında `openapi-typescript`
      ile tip üretimi + `npm` betiği. `03-Web/` başka bir oturumun yazma
      alanında (`migrate-design-to-frontend` açıktı, 2026-08-26) — backend
      oturumu oraya yazmıyor
      Kabul: web tarafı elle tip yazmaz

## 🟡 Yapılıyor

_(boş)_

## 🟢 Tamamlandı

- [x] **A-62** Dosya erişimi ve içerik doğrulama · bitti: 2026-08-27
      `FileSignature` (magic bytes) + iki indirme ucu:
      `GET /api/partner/documents/{id}/content` (kendi evrakı) ve
      `GET /api/platform/partner-documents/{id}/content` (inceleme)
      Kanıt: **`.pdf` diye gönderilen bir betik reddediliyor**
      (`ContentTypeMismatch`) ve geriye HİÇBİR kayıt kalmıyor
      Kanıt: PNG içerik `image/jpeg` diye beyan edilirse de reddediliyor —
      iki taraf da izin listesinde olsa bile beyan doğru olmak zorunda
      Kanıt: doğru beyan edilen JPEG/PNG geçiyor — koruma aşırı değil
      Kanıt: **başka işletmenin evrakı indirilemiyor** (`NotFound`) ve
      listesine de düşmüyor
      Kanıt: platform personeli her evrakı indirebiliyor; personel OLMAYAN
      o yolu kullanamıyor (`NotPlatformStaff`)
      Kanıt: PNG'nin satır sonu kısmı bozulmuşsa reddediliyor; `RIFF` var
      ama `WEBP` yoksa (örn. WAV) reddediliyor; **tanınmayan tür
      reddediliyor** — `true` dönseydi izin listesine yeni bir tür
      eklendiği an imza doğrulaması o tür için sessizce kalkardı
      Kanıt: **iki mutasyon kırmızıya gitti** — imza doğrulaması ve kapsam
      filtresi
      Kanıt: 441 test geçiyor, 69 yol

      ⚠️ **`FileKey` hiçbir yerde dışarı verilmiyor.** İndirme uçtan geçiyor;
      anahtar verilseydi depolama adresine doğrudan erişim denemesine
      davetiye olurdu. İki katman: anahtar gizli VE kova genel okumaya
      kapalı olmalı
      ⚠️ İndirme `attachment` ile dönüyor, `inline` DEĞİL: tarayıcı dosyayı
      göstermek yerine indiriyor, gömülü betik çalışmıyor
      ⚠️ Platform indirmesinde erişim ÖNCE yazılıyor, dosya SONRA veriliyor —
      ters sırada, yarıda kesilen bir indirme hiç kaydedilmezdi
      ⚠️ **Bu bir virüs taraması DEĞİL.** Amaç beyanla içeriğin uyuşmasını
      zorlamak; kötü niyetli ama geçerli bir PDF yine geçer
      🔴 **Kova genel okumaya KAPALI olmalı** — bu bir altyapı ayarı,
      kodla garanti edilemiyor. `G-07` ile doğrulanmalı
- [x] **A-29** İyzico gövdesi · bitti: 2026-08-26
      `IyzicoPaymentProvider` — **Checkout Form** akışı. Mert sandbox
      anahtarlarını `user-secrets`'a koydu, gövde yazıldı ve **gerçek sandbox'a
      karşı** doğrulandı
      Kanıt: **uçtan uca canlı, gerçek İyzico** — rezervasyon `ZCC34BEQ` →
      `POST /api/payments/start` gerçek `sandbox-cpp.iyzipay.com` adresi döndü →
      tarayıcıda sandbox test kartıyla ödendi → İyzico geri dönüşü uca POST etti
      → rezervasyon **`Paid`**, `Payments.Provider = 'iyzico'`, dört defter
      kaydı **toplam 0.00**
      Kanıt: **gerçek İyzico iadesi** — iptal (%100) → `POST /api/payments/refund`
      → `200 {"refunded":1500.00,"providerRefundId":"mock00001iyzihostrfn-02"}`;
      rezervasyon `Refunded`, iade kaydı `Completed`, defter 7 kayıt **0.00**
      Kanıt: **üretim kapıları ateşliyor** (ölçüldü, `--no-launch-profile` ile) —
      `BaseUrl` sandbox ise ve anahtar boşsa uygulama AÇILMIYOR; ikisi de
      doğruyken açılıyor
      Kanıt: 325 test geçiyor; 8 yeni İyzico testi **ağa çıkmadan** imzayı,
      para biçimini ve kart alanının isteğe girmediğini ölçüyor
      ⚠️ **TCKN ve adres yer tutucu gönderiliyor** — İyzico zorunlu tutuyor,
      biz toplamıyoruz → [[api-benim-kararlarim]]
      ⚠️ **Alt üye iş yeri (submerchant) YAZILMADI.** Bugün tahsilat platform
      hesabına yapılıyor, hakediş defterde duruyor ama işletmeye **para
      transferi yok** — `A-18`'in bıraktığı boşluk aynen duruyor → `A-41`

- [x] **A-56** İadeyi otomatik gönderen iş · bitti: 2026-08-26 (soru 17)
      `ProcessRefundsJob` — 15 dakikada bir, iptal edilmiş ve iadesi
      bekleyen rezervasyonları `RefundService`'e veriyor
      Kanıt: **uçtan uca canlı** — `6PY3ETG4` iptal edildi (%100, 1500 TL),
      iş kaydı buldu, `ItemsProcessed = 1`, rezervasyon `Refunded`, ödeme
      `Refunded`, iade `Completed` + sağlayıcı kimliği, defter 7 kayıt
      **toplam 0.00**
      Kanıt: iş ikinci kez çalıştığında aynı rezervasyona DOKUNMUYOR
      Kanıt: başarısız denemeden sonra bir saat geçmeden tekrar denemiyor
      Kanıt: beş denemeden sonra duruyor ve `payment.refund.abandoned`
      olayını **tam bir kez** yazıyor — sessiz bırakmıyor
      Kanıt: 373 test geçiyor

      **İki sonsuz döngü koruması ve ikisi de mutasyonla ölçüldü:**
      1. Sorgu, servisin ön koşullarını aynen yansıtıyor. Ödeme koşulu
         söküldüğünde ödemesiz kayıt seçiliyor, servis istisna atıyor,
         `Refunds` satırı YAZILMADAN dönüyor → sayaç ilerlemiyor, iş her
         15 dakikada aynı kaydı deniyor
      2. Deneme sınırı (`5`) söküldüğünde başarısız iade sonsuza kadar
         deneniyor
      ⚠️ **Birinci koruma önce ÖLÇÜLEMİYORDU.** Yalnız `Refunds` satır
      sayısına bakıyordum; kayıt seçilse bile satır yazılmadığı için test
      yeşil kalıyordu. Uyarı günlüğünü yakalayan bir günlükçü eklenince
      mutasyon kırmızıya gitti → [[api-eszamanlilik-testi-yarismayabilir]]

      ⚠️ Deneme sayacı ayrı kolon DEĞİL: her başarısız deneme bir `Failed`
      satırı bırakıyor, satır sayısı sayacın kendisi. Ayrı bir sayaç ikinci
      bir gerçek kaynağı olurdu

- [x] **A-44** Yetki damgası — jeton anında geçersizleşiyor · bitti: 2026-08-26 (soru 1)
      `Users.SecurityStamp` + jetonda `sstamp` talebi + `OnTokenValidated`
      doğrulaması. Migration `A44_GuvenlikDamgasi`
      Kanıt: damga değişince AYNI jeton **401** alıyor (`403` değil — jetonun
      kendisi geçersiz, izin sorunu yok); yeniden giriş çalışan jeton üretiyor
      Kanıt: **devir senaryosu kapandı** — bu görevi doğuran ölçüm buydu.
      Devirden sonra eski sahibin AYNI jetonu `401`, yeni sahip girince `200`
      Kanıt: çalışan pasife alınınca erişim **anında** kesiliyor; koddaki
      *"anında kesilmiyor, 15 dakika devam eder"* yorumu artık yanlış ve
      düzeltildi
      Kanıt: damgası değişmeyen kullanıcı ETKİLENMİYOR — koruma herkesi kesmiyor
      Kanıt: **üç mutasyon kırmızıya gitti** — damga karşılaştırması, pasife
      alma yükseltmesi, devir yükseltmesi
      Kanıt: 378 test geçiyor

      **Yükseltme noktaları:** rol yetkisi değişimi (o role bağlı HERKES),
      üye rolü değişimi, üye pasife alma, sahiplik devri (İKİ taraf birden)

      ⚠️ **`A-43`'ün sorgusu buraya taşındı.** İşletme aktiflik kontrolü
      kendi sorgusunu atıyordu; damga ikinci bir sorgu daha ekleyecekti.
      İkisi `OnTokenValidated` içinde TEK okumada birleşti, sonuç
      `HttpContext.Items` üzerinden işleyiciye geçiyor
      ⚠️ **Bedel dürüstçe:** `[HasPermission]` uçlarında sorgu sayısı aynı
      kaldı, ama düz `[Authorize]` uçlarında (konuşmalar, destek, hesap)
      istek başına BİR okuma eklendi — eskiden hiç yoktu
      ⚠️ **Dağıtımda tüm oturumlar bir kez düşecek**: eski jetonlarda
      `sstamp` talebi yok ve doğrulama onları reddediyor. Bilerek — "talep
      yoksa geçir" korumayı ilk günden delik bırakırdı

- [x] **A-48** İyimser eşzamanlılık (`xmin`) — proje geneli · bitti: 2026-08-26 (soru 6)
      `OnModelCreating` içinde DÖNGÜYLE, tek tek değil: yeni entity
      eklendiğinde koruma kendiliğinden geliyor
      Kanıt: aynı fiyatı iki bağlam düzenleyince ikincisi
      `DbUpdateConcurrencyException` alıyor ve **birincinin yazdığı duruyor**
      Kanıt: yeniden okuyup yazmak çalışıyor — koruma kilitlemiyor
      Kanıt: işletme kaydında da çalışıyor (fiyata özel değil)
      Kanıt: API çakışmayı **409** olarak dönüyor, `500` değil
      Kanıt: 414 test geçiyor

      🔴 **BEŞ TABLO KAPSAM DIŞI ve bu bir KORUMA BOŞLUĞU:**
      `Voyages` · `Boats` · `Coupons` · `LedgerEntries` — satırlarını
      **tetikleyiciler** güncelliyor (`sync_voyage_sold_seats`,
      `sync_boat_rating`, `sync_coupon_used_count`,
      `release_ledger_on_failed_payout`). Tetikleyici çalışınca `xmin`
      değişiyor, bağlamdaki kopya bayatlıyor ve jeton **kendi işlemimizi**
      çarpıyor. Ölçüldü: **39 test kırıldı**, hepsi iptal akışında
      `EventLogs` — bölümlenmiş ve append-only. Jetonun değeri sıfır
      (`forbid_mutation` `UPDATE`'i zaten reddediyor) ama bölümlenmiş
      tabloya `INSERT`'te `xmin` geri okunamıyor ve **9 test kırıldı**
      ⚠️ Boşluk BİR TESTLE SABİTLENDİ (`Tetikleyici_yazan_tablolarda_jeton_yok`):
      birileri "her yerde koruma var" sanmasın. Kapatılırsa test kırmızıya
      döner ve o zaman bilinçli bir karar verilmiş olur

      ⚠️ **`ExecuteUpdate`/`ExecuteDelete` de kapsam dışı** — değişiklik
      izleyicisinden geçmiyorlar
      ⚠️ Migration gövdesi **boş**: `xmin` sistem kolonu, EF onu yeni kolon
      sanıp 75 `AddColumn` üretti; çalıştırılsaydı PostgreSQL reddederdi
      ⚠️ `FromSql` ile yazılan ham sorguda `SELECT *` yetmiyor, `xmin`
      açıkça seçilmeli — **132 test birden** bu yüzden kırılmıştı

- [x] **A-55** İşletme reddetme ucu + yeniden başvuru · bitti: 2026-08-26 (soru 16)
      `POST /api/platform/partners/{id}/reject` (`partner.approve` yetkisi)
      Reddedilen, aynı vergi numarasıyla yeniden başvurunca kayıt
      `ApplicationReceived`'a dönüyor — YENİ kayıt açılmıyor
      Kanıt: ret sonrası `Rejected` + sebep + `RejectedAt`; sebepsiz ret
      **400**; **aktif işletme reddedilemiyor** (durdurmanın yolu askı)
      Kanıt: yeniden başvuruda AYNI `partnerId` dönüyor, `RejectionReason`
      ve `RejectedAt` temizleniyor, tek işletme + tek üyelik kalıyor
      Kanıt: yeni başvuru YENİ onay kaydı yazıyor (2 → 4) — eskisine
      yaslanmak, kullanıcının BUGÜN onayladığını ispatlamazdı
      Kanıt: **iki mutasyon kırmızıya gitti** — e-posta eşleşmesi ve parola
      teyidi
      Kanıt: 385 test geçiyor, 64 yol

      🔒 **Yeniden başvuru İKİ kapıyla korunuyor ve sebebi somut:**
      vergi numarası yarı-kamusal bir bilgi. Yalnız ona bakılsaydı numarayı
      bilen herkes reddedilmiş bir kaydı kendi hesabına açtırabilirdi.
      (1) başvuru e-postası, kaydın SAHİBİNİN e-postasıyla aynı olmalı
      (2) parola teyidi
      ⚠️ Üçü de (kayıt yok · e-posta tutmuyor · parola yanlış) **AYNI**
      cevabı veriyor: `TaxNumberTaken`. Ayrışsalardı uç, hangi vergi
      numarasının reddedilmiş bir kayda ait olduğunu ele veren bir sorgulama
      aracına dönerdi
      ⚠️ Red sebebi kayıttan silinse de KAYBOLMUYOR: `platform.data.accessed`
      olayı reddi yazdı ve `EventLogs` append-only

- [x] **A-47** `price.write` ayrı yetkisi · bitti: 2026-08-26 (soru 5)
      Fiyat uçları `price.read`/`price.write`, ek hizmet yazma `extra.write`
      Kanıt: yalnız `boat.read`+`boat.write` taşıyan çalışan tekne listesine
      **200**, fiyat ve ek hizmet uçlarına **403** alıyor
      Kanıt: işletme sahibi fiyat ucuna erişebiliyor (`403` DEĞİL) — bu test
      olmasaydı `A-47` sahipleri de kilitlemiş olabilirdi
      ⚠️ Yetkiler katalogda 2026-08-24'ten beri VARDI ve hiçbir uç
      kullanmıyordu. **Tanımlanmış ama bağlanmamış bir yetki, verilmiş gibi
      görünüp hiçbir şey yapmaz**
      ⚠️ Kiralama tipleri bilerek `boat.*` kaldı: süre, kapasite ve kural
      teknenin yapılandırması, fiyatı değil
      ⚠️ Mevcut işletme rolleri `boat.write` ile fiyat düzenleyemez oldu —
      istenen bu, ama işletmeye söylenmeli

- [x] **A-57** `RefundReason`'a "işletme iptali" · bitti: 2026-08-26 (soru 18)
      `PartnerCancellation` eklendi; migration `A57_IsletmeIptaliSebebi`
      Kanıt: yeni değer veritabanına yazılabiliyor, uydurma bir değer HÂLÂ
      `CK_Refunds_Reason_Enum` ile reddediliyor — kısıt gevşetilmedi,
      genişletildi
      ⚠️ **Enum'a değer eklemek migration istiyor**: `A-39` her enum kolonuna
      izin listesi koydu. Yalnız C# enum'una satır eklenseydi kod derlenir,
      test geçer ve İLK GERÇEK KAYIT kısıta takılırdı — üstelik iade
      akışının, yani para hareketinin ortasında

- [x] **A-49** Reddedilen yorumlar işletmeden gizlensin · bitti: 2026-08-26 (soru 7)
      `ListForPartnerAsync` artık `Rejected` yorumları döndürmüyor
      Kanıt: üç durumlu veri kuruldu, panel listesi 2 döndürdü; reddedilen
      yorumun METNİ de sızmıyor
      Kanıt: mutasyon (filtre söküldü) kırmızıya gitti
      ⚠️ Filtre SORGUDA, servis katmanında değil — yeni bir okuma yolu
      (dışa aktarma, rapor, bildirim) filtreyi unutabilirdi

- [x] **A-45** Yayından kaldırırken satılmış sefer uyarısı · bitti: 2026-08-26 (soru 3)
      `GET /api/partner/boats/{id}/status-impact` — gelecek satılmış sefer
      sayısı, toplam yolcu, en yakın kalkış
      Kanıt: ödenmiş sefer sayılıyor, **ödenmemiş sayılmıyor** (`Pending`
      tutma süresi dolunca düşüyor; onu saymak işletmeyi olmayan bir
      yükümlülükle korkuturdu)
      Kanıt: başka işletmenin teknesi sorgulanınca sıfır dönüyor — kapsam
      filtresi olmasaydı rakip doluluğu öğrenilebilirdi
      ⚠️ AYRI bir okuma ucu, durum cevabına eklenmiş alan değil: uyarı
      işlemden ÖNCE gösterilmeli. Cevaba konsaydı işletme "40 yolcunuz vardı"
      yazısını tekne çoktan yayından kalktıktan sonra okurdu
      ⚠️ İşlem ENGELLENMİYOR — tekne arızalandığında işletme kilitlenmemeli

- [x] **A-53** Destek personelinin ilk ismi müşteriye · bitti: 2026-08-26 (soru 14)
      `TicketMessageItem.StaffFirstName` — yalnız ilk isim
      Kanıt: "Ayşe Demir Kaya" → `"Ayşe"`; **soyadı hiç çıkmıyor**;
      müşterinin kendi mesajında alan `null`
      Kanıt: mutasyon (ayrıştırma söküldü, tam ad döndü) kırmızıya gitti
      ⚠️ Tam ad ARA TİPTE kalıyor, DTO'ya hiç girmiyor: doğrudan
      `TicketMessageItem` içine yazılsaydı bir an için dışarıya
      dönebilecek bir nesnede dururdu

- [x] **A-51** Kapanan konuşmadan sonra yeni konuşma · bitti: 2026-08-26 (soru 9)
      `(BoatId, CustomerUserId)` benzersiz indeksi **kısmi** yapıldı:
      `UX_Conversations_AcikTekil`, filtresi `Status = 'Open'`
      Kanıt: kapanan konuşmadan sonra yenisi açılıyor, geçmişler AYRI duruyor
      (her konuşmada kendi mesajı), eskisi `Closed` kalıyor
      Kanıt: ikinci AÇIK konuşma `23505` ile kesiliyor — hangisine yazılacağı
      belirsiz kalmasın
      Kanıt: açık konuşma varken `StartAsync` yenisini açmıyor, mevcuda yazıyor
      ⚠️ "Konuşmayı yeniden aç" seçeneği elendi: kapanmanın anlamını yitirir
      ve QR ile kapanma kuralını (`A-36a`) zayıflatırdı

- [x] **A-54** Askıya alırken turları iptal seçeneği · bitti: 2026-08-26 (soru 15)
      `SuspendPartnerRequest.CancelUpcomingTours` — **varsayılan `false`**
      Kanıt: iptal edilen tur **%100** iade alıyor, sebep `PartnerCancellation`
      Kanıt: **iade zincirine gerçekten bağlanıyor** — `ProcessRefundsJob`
      onu topluyor, iade `Completed`, rezervasyon `Refunded`, defter 0.00.
      Bu bağ olmadan müşterinin turu iptal olur, parası iade edilmezdi
      Kanıt: geçmiş turlar iptal edilmiyor
      ⚠️ Kademeli iade MÜŞTERİNİN KENDİ vazgeçmesi için; burada müşterinin
      kusuru yok, ceza kesmek yanlış olurdu

      🔍 **Yolda bir eksik çıktı ve kapatıldı:** iptalin SEBEBİ rezervasyonda
      kayıtlı değildi. `A-57` `RefundReason`'a `PartnerCancellation` eklemişti
      ama **kaydedilecek yer yoktu** — otomatik iade işi HER iptali
      `CustomerCancellation` sayıyordu. `Reservations.RefundReason` eklendi
      (migration `A54_IptalSebebi`, enum kısıtıyla)

- [x] **A-59** Onay metinleri tablosu · bitti: 2026-08-26 (soru 22)
      `ConsentDocuments` — `ContractTemplates` deseni. Tür başına tek
      yürürlükteki metin (`UX_ConsentDocuments_Yururlukte`)
      Kanıt: yürürlükteki sürüm değiştirilince sonraki başvurunun onay kaydı
      YENİ sürümü taşıyor
      Kanıt: yürürlükteki metin yoksa başvuru **reddediliyor**
      (`ConsentDocumentMissing`) — sürümsüz bir onay kaydı anlaşmazlıkta
      hiçbir şey kanıtlamaz
      ⚠️ İlk sürümler migration'da ve gövdeleri YER TUTUCU olduğunu SÖYLÜYOR.
      **Gerçek hukuki metinler Mert'ten gelecek ve YENİ SÜRÜM olarak
      eklenecek** — yürürlükteki gövdenin üzerine yazılırsa geçmişte onay
      verenlerin neyi onayladığı geriye dönük değişir
      ⚠️ `EnumKisitlariTests` yeni enum kolonunu kısıtsız görüp kırmızıya
      döndü; kısıt eklendi. Kural yazılı olmakla kalmıyor, ölçülüyor

- [x] **A-50** Yorum daveti hatırlatması · bitti: 2026-08-26 (soru 8)
      `ReviewInvitations.ReminderSentAt` + `SendReviewInvitationsJob` içinde
      hatırlatma turu; 7 gün sonra, **yalnız bir kez**
      Kanıt: 6. günde hatırlatma YOK, 8. günde var, 20. günde İKİNCİ hatırlatma
      YOK; yorum yazılmışsa gitmiyor; süresi dolmuş davete gitmiyor
      Kanıt: mutasyon değil, **testin kendisi bir kod hatası yakaladı** —
      işin başındaki `if (adaylar.Count == 0) return 0;` hatırlatmayı HİÇ
      çalıştırmıyordu ve tam da hatırlatmanın gerektiği durum buydu
      ⚠️ Jeton hatırlatmada YENİLENİYOR: düz metin saklanmadığı için eskisi
      gönderilemezdi. Eski link geçersizleşiyor — ilk e-postadaki link
      çalışmıyorsa müşteri ikincisini kullanır

- [x] **A-52** Maskeleme eşiği bildirimi · bitti: 2026-08-26 (soru 10)
      Konuşmadaki toplam maskeleme **5**'i aştığında
      `messaging.masking.threshold` olayı yazılıyor
      Kanıt: eşik **yalnız aşıldığı mesajda** işaretleniyor — sonraki
      mesajlarda değil. Yalnız "toplam >= eşik" denseydi platform aynı
      konuşma için düzinelerce uyarı alır ve bildirim gürültüye dönerdi
      Kanıt: temiz mesajlar eşiği hiç aşmıyor
      ⚠️ Kullanıcıya HİÇBİR ŞEY söylenmiyor (Mert): uyarı caydırıcı olduğu
      kadar **nasıl kaçılacağını da öğretirdi**
      ⚠️ Payload'da SAYILAR var, maskelenen METİN yok — `EventLogs`
      temizlenemiyor
      ⚠️ **Eşik (5) bir TAHMİN.** Kaç maskelemenin "ısrar" sayılacağını
      söyleyen veri yok; gerçek rakamlar birikince gözden geçirilmeli
      ⚠️ Bildirimin YÜZEYİ olay günlüğü (`eventlog.read`). Ayrı bir destek
      paneli ekranı frontend işi

- [x] **A-46** Slug değişimi + yönlendirme · bitti: 2026-08-26 (soru 4)
      `BoatSlugs` tablosu — **iki kararı birden karşılıyor**: eski adresler
      (soru 4) ve dile göre slug ([[domain-gereksinimler]] 2026-08-24).
      Ayrı ayrı yapılsaydı tablo iki kez tasarlanırdı
      Ad değişince yeni slug yürürlüğe geçiyor, eskisi geçmişe düşüyor;
      `GET /api/boats/{slug}` eski adrese **301** dönüyor
      Kanıt: eski adres yürürlüktekine çözülüyor; iki yürürlükteki adres
      `UX_BoatSlugs_Yururlukte` ile kesiliyor; iki tekne aynı adresi
      paylaşamıyor (global benzersiz)
      Kanıt: mevcut 5 teknenin adresi migration'da taşındı — taşınmasaydı
      adres çözümlemesi tabloya geçtiği an yayındaki her tekne **404** olurdu
      ⚠️ `302` değil `301`: geçici yönlendirme SEO değerini taşımaz
      ⚠️ Slug yalnız AD GERÇEKTEN değiştiyse dönüyor — her güncellemede
      dönseydi kapasiteyi düzelten işletme farkında olmadan adresini
      değiştirirdi
      ⚠️ `Boats.Slug` kaldı ve yürürlükteki adresin kopyasını taşıyor;
      ayrışma riski var, ikisi tek işlemde yazılıyor

- [x] **A-60** Dosya depolama ve belge yükleme · bitti: 2026-08-26 (soru 23)
      Mert: *"S3'te olması gerekiyor"* · *"geç yüklenme sorunu yaşamak
      istemiyorum"*
      `IFileStorage` + `S3FileStorage` + `ImageProcessor` +
      `POST /api/partner/documents`
      Kanıt: **GERÇEK bir S3 API'sine karşı doğrulandı** — tek kullanımlık
      MinIO konteyneri. Yazma, okuma, silme, olmayan anahtar, aynı içerik
      aynı anahtar
      Kanıt: JPEG → **WebP**, üç boyut (400/800/1600), en-boy oranı
      korunuyor, `RIFF…WEBP` imzası doğrulanıyor ve **her boyut orijinalden
      küçük** — kazanç ölçüldü, iddia edilmedi
      Kanıt: küçük görsel BÜYÜTÜLMÜYOR; bozuk veri anlaşılır hata veriyor
      Kanıt: 422 test geçiyor, 67 yol
      ⚠️ **`PartnerDocuments` ölü tabloydu** (yazan yok, okuyan yok) —
      artık canlı

      **Performans kararları (Mert'in sorusuna cevap):**
      Anahtar **içerik özetinden** türüyor → adres içerik değişmedikçe
      değişmiyor → CDN'e `max-age=31536000, immutable` verilebiliyor.
      Rastgele anahtar üretilseydi her yükleme yeni adres yaratır ve
      önbellek hiç ısınmazdı
      Üç genişlik üretiliyor: 4000px fotoğrafı 400px kutuda göstermek
      "geç yükleme" şikayetinin **format değil**, en büyük tek sebebi
      ⚠️ Kalan iki parça bizde değil: **CDN** (altyapı) ve
      **`srcset` + `loading=lazy`** (frontend)

      ⚠️ **SkiaSharp seçildi, ImageSharp DEĞİL.** ImageSharp'ın "Six Labors
      Split License"ı belirli gelir eşiğinin üstünde ticari kullanımı
      ÜCRETLİ kılıyor. Sessizce ücretli bir lisansa bağlanmak, fark
      edildiğinde geri alması pahalı bir borç olurdu. SkiaSharp MIT
      ⚠️ **`DisablePayloadSigning` YALNIZ HTTPS'te çalışıyor** — HTTP bir uç
      noktada açık bırakılırsa her yükleme düşer (ölçüldü)
      ⚠️ Üretim kapıları: depolama anahtarı boşsa VE adresler `localhost`
      içeriyorsa uygulama açılmıyor

- [x] **A-42** İşletme başvuru ucu · bitti: 2026-08-26
      `POST /api/partners/apply` — tek istekte beş kayıt, TEK İŞLEMDE:
      kullanıcı → işletme → sahip rolü → rol yetkileri → sahip üyeliği,
      artı iki KVKK onay kaydı ve "başvurunuzu aldık" e-postası
      **IBAN ZORUNLU** (Mert, 2026-08-26) + mod-97 sağlaması
      Kanıt: **uçtan uca canlı** — başvuru `200`, işletme
      `ApplicationReceived`, **1 sahip, 1 rol, 25 rol yetkisi = 25
      verilebilir yetki** (tam eşleşme), 2 onay kaydı IP'siyle, e-posta
      kuyrukta `Pending`
      Kanıt: boşluklu ve küçük harfli IBAN normalleşiyor →
      `TR180006200119000006672315`
      Kanıt: **son hanesi bozuk IBAN reddediliyor** (`IbanInvalid`) — biçim
      olarak kusursuz, veritabanı kısıtından geçerdi; mod-97 yakalıyor
      Kanıt: onay kutusu işaretsiz `400 ConsentRequired`; aynı e-posta
      `400 EmailTaken`; aynı vergi no `400 TaxNumberTaken`
      Kanıt: başvuran giriş yapabiliyor, jetonunda `partner_id` ve 25 yetki var
      Kanıt: olay günlüğünde **IBAN, vergi no ve telefon YOK** — yalnız
      iş yeri türü ve şehir
      Kanıt: **iki mutasyon kırmızıya gitti** — `IsPartnerAssignable`
      filtresi söküldü (5 test), mod-97 sağlaması söküldü (2 test)
      Kanıt: 355 test geçiyor, 63 yol

      🔴 **YOLDA BİR GÜVENLİK AÇIĞI BULUNDU VE KAPATILDI.**
      Domain *"panele erişim sözleşme onaylanana kadar kapalı"* diyor,
      `Partner` kaydında da yazılıydı — ama **hiçbir yer uygulamıyordu**.
      Başvuru ucu yazılana kadar teorikti (sisteme işletme girmiyordu);
      `A-42` ile canlı bir açığa dönüştü: başvuran **anında tekne ekleyip
      fiyat girebiliyordu**. Aynı boşluk `A-38`'i de kesiyordu — askıya
      alma yalnız durumu değiştiriyor, jetonu iptal etmiyordu
      Çözüm: `PermissionAuthorizationHandler` artık `partner_id` taşıyan
      her istekte işletmenin `Active` olduğunu **veritabanından** doğruluyor
      Kanıt: aynı jetonla üç durum — `ApplicationReceived` **403**,
      `Active` **200**, `Suspended` **403**. Askı ANINDA etkili, 15 dakikalık
      jeton penceresi yok
      Kanıt: platform personeli etkilenmiyor (`/api/platform/*` **200**)
      ⚠️ **Bu kapının OTOMATİK TESTİ YOK** — kanıtı yalnız canlı ölçüm.
      Test projesi servis/veritabanı seviyesinde, HTTP barındırmıyor → `A-43`

- [x] **A-43** Test projesine HTTP katmanı · bitti: 2026-08-26
      `ApiFixture` (`WebApplicationFactory<Program>`) + gerçek giriş ucundan
      jeton alan yardımcı. `Microsoft.AspNetCore.Mvc.Testing` eklendi;
      `Program` artık `public partial`
      Kanıt: **`A-42`'nin güvenlik kapısı artık KIRMIZIYA GİDEBİLİYOR** —
      `PermissionAuthorizationHandler`'dan aktiflik kontrolü söküldüğünde
      iki test kırmızı. Kanıtı elle `curl` olmaktan çıktı
      Kanıt: aynı jetonla üç durum tek testte —
      `ApplicationReceived` 403 → `Active` 200 → `Suspended` 403
      Kanıt: jetonsuz istek **401**, yetkisiz istek **403** (ikisi ayrı
      test — karıştırılırsa istemci yenileme akışını tetikleyemez)
      Kanıt: aktif işletme sahibi `refund.manage` istemeyen uçlara giriyor
      ama **iade ucuna giremiyor** (403); panelin açık olduğu ÖNCE
      doğrulanıyor, yoksa 403'ün sebebi ayırt edilemezdi
      Kanıt: geçersiz gövde **400**, 500 değil
      Kanıt: 365 test geçiyor

      **Yolda iki anahtar açıldı ve ikisi de İKİ YÖNDE test edildi:**
      `ScheduledJobs:Enabled` — test sunucusunda işler çalışsaydı TCMB'ye
      gerçek istek atar ve başka testlerin satırlarını değiştirirdi
      `RateLimiting:Enabled` — kovalar IP'ye göre bölünüyor, test
      sunucusunda IP BOŞ, yani bütün testler tek kovayı paylaşıyordu
      (15 dk / 10). Paket 7 istekteydi; iki test daha eklenince **`429` ile
      kırılacaktı** ve bu gerçek bir hata gibi okunurdu
      Kanıt: hız sınırı AÇIKKEN 11. istek `429`; kapalıyken 12 istek geçiyor
      Kanıt: zamanlanmış iş koşucusu anahtar kapalıyken kayıtlı DEĞİL,
      açıkken kayıtlı
      ⚠️ **İkisi de üretimde kapatılamıyor** — `Program.cs` açılışta
      reddediyor. Ölçüldü (`--no-launch-profile` ile): işler kapalı →
      açılmıyor, hız sınırı kapalı → açılmıyor, ikisi açık → açılıyor

- [x] **A-20** Testleri Testcontainers'a taşı · bitti: 2026-08-26
      `PostgresFixture` artık tek kullanımlık konteyner açıyor
      (`postgres:18.6-alpine`, koleksiyon başına bir tane)

      **2026-08-26 sabah DENENDİ ve GERİ ALINDI** — `docker pull` hiçbir
      imajı indiremiyordu, `hello-world` bile 45 saniyede inmedi. Aynı gün
      öğleden sonra yeniden ölçüldü: **engel kalkmış**, `hello-world`
      2,5 sn'de, `postgres:18.6-alpine` 16 sn'de indi

      Kanıt: **`DC_TEST_PASSWORD` olmadan 367 test geçiyor** — yerel
      PostgreSQL'e hiç bağlanmıyor
      Kanıt: **yerel `dailycruising_test` veritabanı SİLİNDİ**, testler yine
      geçti ve veritabanı yeniden yaratılmadı. Yerel sunucuya bağımlılığın
      gerçekten koptuğunun kesin kanıtı bu
      Kanıt: imajın yetenekleri ölçüldü — `citext`, `btree_gist`, `unaccent`,
      `pg_trgm`, `uuidv7()`, gist `range_ops`, `postgres` kullanıcısı
      süper kullanıcı + `CREATEROLE` (`A-10` migration'ı bunu istiyor)
      Kanıt: koşu sonrası artık konteyner kalmıyor
      Kanıt: iki test imajın SABİTLENMİŞ olduğunu denetliyor —
      `latest` yasak ve ana sürüm geliştirme sunucusuyla aynı (18)
      Bedel: paket süresi **8 sn → 11-15 sn** (konteyner açılışı)

      ⚠️ **Bu görev CI'ı BEKLEMİYORDU, tam tersiydi**: CI'ın çalışabilmesi
      için Testcontainers gerekiyordu — yerel Postgres'e bağlı testler CI'da
      hiç koşamazdı. CI kurulumu ayrı iş → `G-07`
- [x] **A-40** Yorum davetini ÜRETEN iş · bitti: 2026-08-26
      `SendReviewInvitationsJob` — saatlik. Tur bittikten **3 saat** sonra,
      biniş yapmış rezervasyonlara davet üretiyor ve e-postayı outbox'a koyuyor
      ⚠️ **`A-35` akışı canlıda HİÇ ÇALIŞMIYORDU** — daveti tüketen uçlar
      vardı, üreten yoktu; davet satırını elle kurmuştum. Bunu fark eden tek
      şey "davetleri kim üretiyor" diye sormak oldu
      ⚠️ Düz metin jeton YALNIZ e-postaya giriyor; veritabanına SHA-256 özeti
      ⚠️ Davet ve e-posta AYNI kaydetmede: ayrı olsalardı ya "jetonu olan ama
      e-postası gitmeyen" ya da "e-postası giden ama jetonu olmayan" bir davet
      kalırdı — ikincisinde müşteri geçersiz link tıklardı
      ⚠️ Üç koşul birden: biniş yapılmış · tur bitmiş · daveti/yorumu yok.
      Üçüncüsü olmasaydı iş saatlik çalıştığı için müşteri **her saat** bir
      "değerlendirin" e-postası alırdı
      Kanıt: 308 test yeşil; beş mutasyon kırmızıya döndü. Test, e-postadaki
      jetonun veritabanındaki özetin karşılığı olduğunu VE o jetonla
      `GetInvitationAsync`'in gerçekten çalıştığını doğruluyor — üretim ile
      tüketim birbirini tutuyor
      ⚠️ **İki test hatası kendi kurulumumdan çıktı:** seferin bitiş anını
      sabit varsaymıştım (gerçekte 14:00 UTC, ben 17:00 sanmıştım) ve
      iddiaları işin DÖNÜŞ SAYISINA bağlamıştım — iş global çalışıyor, başka
      testlerin artıklarını da alıyor. Aynı tuzağa outbox testlerinde de
      düşülmüştü. İddialar belirli rezervasyona bağlandı

- [x] **A-38** Platform yönetim uçları · bitti: 2026-08-26
      `GET /api/platform/partners` · `POST /partners/{id}/review|contracts|
      suspend|reinstate` · `GET /reviews` · `POST /reviews/{id}/moderate`
      ⚠️ **MUAFİYETİN BEDELİ GERÇEKTEN ÖDENİYOR** — kabul ölçütü buydu.
      Platform personeli kapsam filtresinden muaf (Mert, 2026-08-24) ve
      **OKUMA DAHİL** her erişim `platform.data.accessed` olarak yazılıyor.
      Diğer controller'larda liste/detay okumaları günlüğe yazılmıyor (kendi
      verisini okumak olağan); burada yazılıyor ve fark tam olarak bu:
      **başka birinin verisine bakmak olağan değildir**
      ⚠️ İzin listesi ESKİDEN BOŞTU — bedel ödeniyor GİBİ görünüyordu ama
      kayıtta NE ERİŞİLDİĞİ yoktu. `resource`, `action`, `filter` eklendi
      ⚠️ **"Komisyon düzenleme" diye ayrı bir uç YOK**: *"Oranı değiştirmek
      yeni sözleşme (ve yeni onay) demektir"*. Oranı doğrudan güncelleyen bir
      uç, işletmeyi onaylamadığı bir orana tabi kılardı
      ⚠️ Yeni sözleşme önceki BEKLEYENİ iptal ediyor, ONAYLIYA dokunmuyor:
      yürürlükteki sözleşme iptal edilseydi işletme yenisini onaylayana kadar
      sözleşmesiz kalır, tekne ekleyemez, satış yapamazdı
      ⚠️ Gövde KOPYALANIYOR — şablon değişse işletmenin neyi onayladığı
      kaybolmamalı
      ⚠️ Askıya alma mevcut rezervasyonları İPTAL ETMİYOR
      **Yorum moderasyonu `A-35`'in eksik yarısıydı** — `ModeratedByUserId`
      yazılıyor (`CK_Reviews_Moderated` istiyor) ve `trg_review_sync_boat_rating`
      puanı yeniden hesaplıyor
      Kanıt: canlı — kimliksiz **401** · işletme kullanıcısı **403** ·
      platform personeli **200** (3 işletme) · **okuma olay sayısını 1→2
      artırdı** (`{"action":"list","resource":"partner"}`) · geçersiz geçiş
      **400** · %18 sonra %12 sözleşme → eskisi **`Cancelled`**, yenisi
      **`Sent`** · %150 komisyon **400** · sebepsiz askı **400** · askı
      **204** · tekrar askı **400** · askı kalkınca sebep **temizlendi**
      Kanıt: 303 test yeşil; sekiz mutasyon kırmızıya döndü
      ⚠️ **`SuspensionReason` kolonu EKLENDİ** (`A38_AskiSebebiKolonu`).
      Askı sebebini `RejectionReason`'a yazıyordum; kolon adı içeriğiyle
      uyuşmuyordu ([[api-desenler]]) ve `CK_Partners_RejectionReason` o kolonu
      `Rejected` durumuna bağlıyor. Migration eski kayıtları TAŞIYOR,
      kopyalamıyor — iki yerde dursa hangisi doğru sorusu doğardı
      ⚠️ Testimin kurulumu `Rejected` işletmeyi sebepsiz yaratıyordu ve kısıt
      yakaladı; kısıt haklıydı

- [x] **A-37** Destek talebi uçları · bitti: 2026-08-26
      `POST /api/support/tickets` (**kimliksiz**) · `GET` liste ve detay ·
      `POST /{id}/messages` · `PATCH /{id}` (yalnız platform personeli)
      ⚠️ Mesajlaşmadan **bilinçli olarak AYRI** — Mert: *"net sınır, birleşik
      kod değil"*. Kurallar farklı: destekte iç not, öncelik, atama var;
      maskeleme YOK (müşteri destek personeline telefonunu verebilmeli)
      **İki şey her şeyi taşıyor:**
      **İç not sızmamalı** — filtre DEPO katmanında, sorguda; serviste
      elenseydi yeni bir okuma yolu (dışa aktarma, rapor) unutabilirdi ·
      **`FirstResponseAt` doğru olmalı** — iç not SAYILMIYOR, yoksa "ilk cevap
      süresi" raporu müşterinin hiç görmediği bir nota göre hesaplanır ve
      cevapsız talepler hızlı görünür. Kolon geçmişe dönük hesaplanamıyor
      ⚠️ `ResolvedAt` yalnız İLK çözümde; yoksa gidip gelen bir talep son
      dokunuşuyla "hızlı çözüldü" görünür
      ⚠️ Öncelik istekten GELMİYOR — müşteri kendi talebini "Acil"
      işaretleyebilseydi tüm talepler acil olurdu
      ⚠️ Kategori İZİNLİ LİSTEDEN; serbest metin `EventLogs`'a taşınamazdı
      ⚠️ Rezervasyon iliştirilirken SAHİPLİK kontrol ediliyor — yoksa kimlik
      bilen biri destek personelinden başkasının rezervasyonunu öğrenirdi
      Kanıt: canlı — kimliksiz talep **201** · geçersiz kategori **400** ·
      kimliksiz okuma/liste **401** · müşteri iç not **400** · müşteri durum
      değişikliği **403** · personel iç not **204**, müşteri görüşünde
      **görünmüyor** ve `FirstResponseAt` **boş** · personel gerçek cevap
      **204** → `Answered` ve `FirstResponseAt` **dolu** · personel görüşünde
      3 mesaj, iç not **görünüyor**
      Kanıt: 290 test yeşil; yedi mutasyon kırmızıya döndü
      ⚠️ **Hız sınırı hatası canlı denemede çıktı:** tüm sınıfa `hesap`
      (15 dk / 10 istek) yazmıştım ve kendi talebini birkaç kez OKUYAN müşteri
      **429** alıyordu — giriş korumasının bütçesi destek okumaya harcanıyordu.
      Sınıf `panel`e alındı, kimliksiz talep açma ucu `hesap`ta bırakıldı

- [x] **A-36b** Özel teklif uçları · bitti: 2026-08-26
      `GET/POST /api/conversations/{id}/offers` ·
      `POST .../offers/{id}/cancel|reject|accept`
      **TEKLİF BİR VAAT DEĞİL, TAKVİMDE YER KAPLAYAN BİR REZERV.** 48 saat
      boyunca `VoyageType.Offer` bir sefer tarihi tutuyor; ret, geri çekme ya
      da süre dolması onu `Cancelled`'a çekiyor ve tarih serbest kalıyor
      ⚠️ **Kabul: ÖNCE rezervasyon, SONRA teklifin kapanışı.**
      `CK_Offers_Accepted` bir teklifin `Accepted` olabilmesi için
      `ReservationId`'sinin dolu olmasını istiyor; ters sıra aradaki anda
      kısıtı ihlal ediyordu
      ⚠️ Tutar TEKLİFTEN, **komisyon SİSTEMDEN** — satıcı komisyonunu teklifle
      değiştiremez. Birim fiyatlar `null`: teklifte kişi başı kırılım yok,
      uydurma bir birim fiyat muhasebeyi yanıltırdı
      ⚠️ Ek hizmet BİRİM FİYATLARI istekten değil `Extras` tablosundan; ad
      snapshot'lanıyor
      **Not: `ExpireOffersJob` ve `CloseConversationsJob` DAHA ÖNCEKİ
      oturumlardan zaten vardı** (`ad40559`, `61fa872`) — pano bunu
      söylemiyordu ve `ExpireOffersJob`'un üzerine yazdım, git'ten geri aldım
      Kanıt: canlı — müşteri teklif gönderemiyor **400** · satıcı **201** ·
      **tarih tutuldu** (arama o günü göstermiyor, ertesi gün gösteriyor) ·
      aynı tarihe ikinci teklif **400** `DateAlreadyHeld` · ret **204** →
      tarih **serbest** · reddedilmiş teklifi kabul **400** · satıcının kendi
      teklifini kabulü **404** · kabul **200** + rezervasyon · çift gönderim
      **aynı** kimlik · teklif `Accepted` + rezervasyon bağlı · sefer
      `Offer → Sale`
      Kanıt: 279 test yeşil; yedi mutasyon kırmızıya döndü
      ⚠️ **DÖRT hata yalnız canlı denemede çıktı, derlemede değil:**
      `CK_Voyages_RentalTypeRequired` (teklif seferinde kiralama tipi zorunlu,
      atlamıştım) · `23P01` çevrilmemişti, satıcı çıplak **500** görüyordu ·
      `Include` eksikti, kabul `NullReferenceException` veriyordu ·
      `CK_Reservations_HoldExpiry` süresiz `Pending`'i reddetti — tasarımım
      yanlıştı, veritabanı düzeltti

- [x] **A-36a** Sistem içi mesajlaşma · bitti: 2026-08-26
      `GET/POST /api/conversations` · `GET /api/conversations/{id}` ·
      `POST /api/conversations/{id}/messages`
      Mert (2026-08-23): *"bütün bu konuşmalar bizim sistemimizin içerisinde
      olsun ki hem takip edebilelim, hem kullanıcıyı hem tekne sahibini
      koruyabilelim."*
      ⚠️ **MASKELEME: telefon, e-posta VE IBAN.** IBAN kasıtlı — domain
      *"IBAN'a havale KESİNLİKLE YOK"* diyor ve platform dışına kaçışın en
      doğrudan yolu numara değil hesap numarası paylaşmak. İlk sürümde IBAN
      telefon desenine RASTLANTIYLA takılıyor ve `TR` öneki açıkta kalıyordu
      ⚠️ Maskeleme bir GÜVENLİK DUVARI değil, SÜRTÜNME katmanı: kararlı bir
      kullanıcı yazıyla geçirebilir. Amaç imkânsız kılmak değil, KOLAY olmaktan
      çıkarmak ve denemeyi ÖLÇÜLEBİLİR yapmak (`MaskedItemCount`)
      ⚠️ Orijinal metin `Messages.Body`'de duruyor (anlaşmazlık kaydı), API
      yalnız `MaskedBody` dönüyor — `MessageItem` orijinali TAŞIMIYOR
      ⚠️ Konuşma **(müşteri × tekne)** bazında, rezervasyon bazında değil
      ⚠️ Gönderen rolü İSTEKTEN değil konuşmadaki YERDEN türüyor
      **QR → KAPANMA BAĞI KURULDU.** `BoardingService` yorumunda *"mesajlaşmanın
      kapanması ona bağlı"* yazıyordu ama kapanma **hiç yazılmamıştı** — yorum
      niyeti anlatıyordu, davranışı değil. Kapatma artık biniş işleminin
      İÇİNDE: ayrı olsaydı biniş ile kapanma arasında müşteri yazmaya devam
      ederdi
      Kanıt: canlı — kimliksiz **401** · konuşma **201** · detayda numara ve
      e-posta `[gizlendi]`, veritabanında orijinal duruyor
      (`MaskedItemCount = 2`) · işletme kendi teknesinin konuşmasını görüyor ·
      işletmenin IBAN'ı maskelendi · **üçüncü kişi 404** ·
      QR okutuldu → konuşma **`Closed / Boarded`** · kapalıya mesaj **400** ·
      kapalı konuşma yine **okunabiliyor** · boş mesaj **400**
      Kanıt: 268 test yeşil; yedi mutasyon kırmızıya döndü
      ⚠️ **İki hata canlı denemede çıktı, derlemede değil:** yeni konuşmanın
      `Id`'si `SaveChanges`'e kadar boş olduğu için ilk mesaj FK ihlaliyle
      **500** veriyordu (gezinti özelliğine geçildi — `RefreshToken` zincirinde
      de aynı tuzak vardı) · `[Authorize]` yokken kimliksiz istek **400**
      alıyordu, **401** değil
      ⚠️ **Bir mutasyon yanlış metodu vurdu ve boşluk açığa çıktı:** okuma
      (`LoadDetailAsync`) ile gönderme (`FindForParticipantAsync`) AYRI
      sorgular; gönderme yolunun kapsamını hiçbir test ölçmüyordu.
      `Ucuncu_kisi_mesaj_yazamiyor` eklendi

- [x] **A-34b** Fiyatsız kiralama tipi aramada görünmüyordu · bitti: 2026-08-26
      ⚠️ **KENDİ YAZDIĞIM KURAL DOMAIN'E AYKIRIYDI.** `A-34`'te fiyatı olmayan
      kiralama tiplerini aramadan ELEDİM ve bunu doğrulayan bir test bile
      yazdım (`Fiyati_olmayan_tekne_aramada_yok`).
      [[domain-gereksinimler]] 2026-08-23: *"Fiyatsız kiralama tipi arama
      sonuçlarında görünmeli ama fiyat filtresine takılmamalı — 'fiyat sorunuz'
      olarak listelenmeli."* Tekne sahibi fiyat girmeden tip tanımlayabiliyor
      ve müşteri "fiyat için iletişime geçin" görüp **özel teklif akışını**
      başlatıyor. Eleme o satış yolunu tamamen görünmez kılıyordu
      **Yanlış kuralı yazıp testini de yazmak, kuralı iki kat kalıcı yapar** —
      test artık doğru kuralı tutuyor
      ⚠️ Fiyat FİLTRESİ verildiğinde fiyatsızlar yine düşüyor; artan sıralamada
      sona gidiyorlar. Teknenin hem fiyatlı hem fiyatsız tipi varsa listede
      fiyatlı olan görünüyor
      Kanıt: 247 test yeşil; eski elemeyi geri koyan mutasyon kırmızıya döndü
      ⚠️ İkinci mutasyon YEŞİL kaldı: `x.Fiyat != null` kontrolü taşıyıcı değil,
      C#'ın yükseltilmiş operatörü (`null >= 500m` → `false`) zaten yapıyor.
      Yorum düzeltildi — **kod ne yaptığını doğru anlatmalı**

- [x] **A-35** Yorum uçları · bitti: 2026-08-26
      `GET /api/reviews/invitation` · `POST /api/reviews` (kimliksiz) ·
      `GET /api/boats/{slug}/reviews` · `GET /api/partner/reviews` ·
      `POST /api/partner/reviews/{id}/reply`
      **İki duvar, ikisi de sessizce delinebilirdi:**
      **QR** — yorum hakkı rezervasyon yapmakla değil FİİLEN TEKNEYE BİNMEKLE
      doğuyor; delinirse tura gitmemiş biri puan verir ·
      **Moderasyon** — yorum yayına girmeden onaydan geçiyor; delinirse hakaret
      içeren yorum anında görünür VE `trg_review_sync_boat_rating` onu
      ortalamaya katar
      ⚠️ Üyelik gerekmiyor — hak REZERVASYONA bağlı, kullanıcıya değil. Jeton
      **SHA-256** özetiyle saklanıyor, düz metin veritabanında hiç durmuyor
      ⚠️ Jeton tüketimi KOŞULLU `UPDATE` (`WHERE UsedAt IS NULL`)
      ⚠️ Yorum başına en fazla BİR işletme cevabı; yalnız ONAYLI yoruma
      Kanıt: canlı — uydurma jeton **404** · geçerli davet **200** ·
      QR okutulmamışken **400** `NotBoarded` · QR sonrası **201** ·
      aynı jetonla tekrar **400** `InvitationUsed` · `Pending` yorum tekne
      sayfasında **görünmüyor**, puan **boş** · onaylandıktan sonra
      **görünüyor**, puan **5.00 / 1**
      Kanıt: olay günlüğünde `review.submitted`
      (`{rating: 5, hasBody: true, scoreCount: 0}`) ve `review.denied`
      (`NotBoarded`, `InvitationUsed`) — **metin yok**, `EventLogs`
      temizlenemediği için yorum metni oraya konmuyor
      Kanıt: 246 test yeşil; sekiz mutasyon kırmızıya döndü
      ⚠️ **Yarış korumasını hiçbir test ölçmüyordu.** `WHERE UsedAt IS NULL`
      koşulu tamamen kaldırıldığında testler **yeşil kaldı** — servisteki
      sıralı kontrol onları geçiriyordu. `Davet_ikinci_kez_tuketilemiyor`
      eklendi: koşullu `UPDATE`'i doğrudan, eşzamanlılığa güvenmeden ölçüyor
      ⚠️ `OpenApiBelgesiTests` mutlak rotayı (`/` ile başlayan `[HttpGet]`)
      tanımıyordu ve var olan bir ucu "eksik" sanıyordu — kodda değil TESTTE
      hata vardı, düzeltildi
      ⚠️ Canlı denemede iki kısıt kendini gösterdi: `CK_Reservations_PaidAt`
      (binmiş ama ödenmemiş rezervasyon yok) ve `CK_Reviews_Moderated`
      (onaylayanın KİM olduğu yazılmadan onay yok) → `A-38` bunu bilmeli

- [x] **A-39** Enum kolonlarına CHECK kısıtı · bitti: 2026-08-26
      **69 kolon, 49 tablo.** Enum'lar metin olarak saklanıyor ve veritabanı
      bugüne kadar HER metni kabul ediyordu
      ⚠️ Bu teorik değildi: `Boats.DefaultCalendarMode` kolonunda `'Open'`
      yazıyordu (geçerli değerler `Shared`/`ExclusiveOpen`). Elle yazılan bir
      seed SQL'i koymuş, aylardır oradaydı ve `A-34` araması o satıra dokununca
      **500** ile patladı. **Yazan kod EF değildi** — kontrol bu yüzden
      uygulamada değil veritabanında olmak zorundaydı
      ⚠️ `NOT VALID` + ayrı `VALIDATE`: doğrudan `ADD CONSTRAINT` tabloyu tam
      tarama boyunca ACCESS EXCLUSIVE kilitler
      ⚠️ **Ürettiğim liste BİR KOLONU KAÇIRDI.** `Domain` enum'larını tarayarak
      üretmiştim; `BoatRentalTypes.WeekStartDay` bir BCL enum'u (`DayOfWeek`)
      olduğu için listeye girmedi. Eksiği bulan şey kod taraması değil,
      **EF modelini okuyan test** oldu. Ders: model, veritabanına gerçekte
      neyin yazıldığının tek doğru kaynağı
      Kanıt: canlı — geri alındığında **0** kısıt · bozuk veri eklenip tekrar
      denendiğinde `23514: check constraint "CK_Boats_DefaultCalendarMode_Enum"
      of relation "Boats" is violated by some row` ile **DURDU** ve arkasında
      **0** kısıt bıraktı (tek işlem) · veri düzeltilince **95** (69 mantıksal
      + `EventLogs`'un 26 aylık bölümünden gelen miras)
      Kanıt: uygulama normal çalışıyor — arama **200**, tekne yaratma **201**
      (`ExclusiveOpen`), durum değiştirme **204**; elle `'Yayinda'` yazma
      denemesi **reddedildi**
      Kanıt: 234 test yeşil; dört mutasyon MIGRATION ÜZERİNDE kırmızıya döndü
      ⚠️ **İlk mutasyon denemem hiçbir şey ölçmedi**: kısıtları veritabanından
      elle düşürdüm ama `PostgresFixture` her koşuda veritabanını SIFIRDAN
      kuruyor, yani mutasyon testler başlamadan siliniyordu. Doğru mutasyon
      noktası migration kaynağıydı -> [[api-desenler]]

- [x] **A-34** Arama ve listeleme uçları · bitti: 2026-08-26
      `GET /api/search` — kimliksiz. Filtreler: bölge · tekne tipi · kiralama
      tipi · tarih · kişi sayısı · fiyat aralığı · puan · sıralama · sayfalama
      **CANLI SORGU, özet tablo yok** — `AvailabilityDays` 2026-08-24'te
      bilerek ertelenmişti; geri dönüş eşiği p95 > 300 ms ya da tekne > 300
      ⚠️ **MÜSAİTLİK TANIMI REZERVASYON YOLUYLA AYNI.** Ayrışırsa iki yönde de
      zarar var ve **ikincisi sinsi**: arama gizler, tekne boş gider, hiçbir
      hata ve şikâyet üretmez. Üç kural rezervasyondan birebir alındı —
      `Block` seferi kapatır · özel sefer günü tamamen kapatır ·
      `Status = Cancelled` sefer takvimi BIRAKIR
      ⚠️ Bebek koltuk tutmuyor (`Adults + Children`)
      ⚠️ Sezon fiyatı temel fiyatı eziyor; sıralama olmasaydı hangisinin
      döneceği sorgu planına kalırdı ve aynı arama iki farklı fiyat gösterirdi
      ⚠️ Sayfa boyutu tavanı **50** — uç kimliksiz, sınırsız bırakılsaydı tüm
      katalog tek istekte çekilebilirdi ve bunu yapanın hesabı bile olmazdı
      Kanıt: canlı — 12 koltuk boş **12** · 10 satılınca **2** · 3 kişi **YOK** ·
      12/12 dolunca **YOK** · sefer `Cancelled` olunca yine **12** ·
      bakım günü **YOK**, ertesi gün **12**
      Kanıt: 2027-09-15'te sezon fiyatı **650**, 2027-06-15'te temel **500** ·
      geçmiş tarih **400** · ters fiyat aralığı **400** · `pageSize=100000`
      sessizce **50**
      Kanıt: `search.performed` payload izin listesi BOŞTU (her arama
      payloadsız yazılıyordu, "ne arandı" sorusu cevapsızdı). 13 alan eklendi,
      **`resultCount` dahil** — sıfır sonuçlu arama kaçırılan satışın doğrudan
      ölçüsü
      Kanıt: 230 test yeşil; yedi mutasyon ayrı ayrı kırmızıya döndü
      ⚠️ **Arama yazarken canlı 500 çıktı ve sebebi ARAMA DEĞİLDİ**:
      `Boats.DefaultCalendarMode` kolonunda `'Open'` yazıyordu — enum'da böyle
      bir değer yok. Geçmiş bir seed SQL'i yazmış, kimse fark etmemiş.
      Enum kolonlarında **hiç CHECK kısıtı yok** → `A-39`

- [x] **A-33** Katalog uçları · **BİTTİ: 2026-08-26**
      Üç dilim: tekne (`A-33a`) · kiralama tipi + fiyat (`A-33c`) ·
      ek hizmet (`A-33e`). Denetim bulguları `A-33b` ve `A-33d`
      Kanıt: kabul ölçütlerinin üçü de canlı doğrulandı — `boat.viewed`
      olayı `EventLogs`'ta görüldü · başka işletmenin teknesi **404** ·
      çakışan sezon **400** (`EX_Prices_NoOverlappingSeasons`)
      Kanıt: 219 test yeşil, `openapi.json` 38 uç; alt görevlerin kanıt
      satırları `A-33a`, `A-33c`, `A-33e`
      ⚠️ `A-03`'ün 2. maddesi (satır bazlı kapsam) bu görevde uygulandı ve
      `A-34`…`A-38` için de aynı desen geçerli: kapsam DEPO katmanında,
      parametresiz "hepsini getir" metodu yok, ihlal 404
      ⚠️ Jeton karşılaştırması **SHA-256** ile; bcrypt kullanılırsa `WHERE`
      hiç eşleşmez -> [[api-sema]]

- [x] **A-33e** Ek hizmet uçları · bitti: 2026-08-26
      `GET/POST /api/partner/boats/{id}/rental-types/{rtId}/extras` ·
      `PUT/DELETE .../extras/{extraId}`
      ⚠️ **`tr` ÇEVİRİSİ ZORUNLU** ve sebebi somut:
      `PricingRepository.GetExtrasAsync` istenen dili bulamazsa `tr`'ye
      düşüyor, o da yoksa **boş metin** döndürüyor. `tr` olmadan eklenen bir ek
      hizmet satın alındığında rezervasyona **adı boş** yazılırdı ve hiçbir
      yerde hata görünmezdi
      ⚠️ Güncelleme, gövdede olmayan çeviriyi SİLİYOR; çeviriler yerinde
      güncelleniyor (topluca silinip yeniden yazılmıyor) — otomatik çeviri işi
      `ExtraTranslations` kimliklerine bakacak
      ⚠️ Satılmış ek hizmet silinmiyor (`ReservationExtras.ExtraId`)
      Kanıt: canlı — 400 `tr` yokken · 201 `tr`+`en` ile · 400 boş ad ·
      400 negatif fiyat · 200 liste (`names` sözlüğü iki dil) · 204 güncelleme ·
      200 liste (`en` gitmiş) · 404 başka işletme · 204 silme
      Kanıt: 219 test yeşil; üç mutasyon kırmızıya döndü
      ⚠️ **LİSTE UCU İLK SÜRÜMDE 500 VERİYORDU.** Çeviriler EF
      projeksiyonunun İÇİNDE `ToDictionary` ile toplanıyordu; derleme temiz,
      215 test yeşildi ama canlı istek `The LINQ expression
      't => t.LanguageCode' could not be translated` ile düştü. **O ucun testi
      yoktu** — canlı istek atmasaydım fark edilmezdi -> [[api-desenler]]

- [x] **A-33d** A-33c denetiminin bulguları · bitti: 2026-08-26
      **Düzeltilen üç gerçek bulgu:**
      1. **`CheckViolation` (23514) hiç yakalanmıyordu** — altı CHECK kısıtı var
         (canlı sayıldı) ve uygulama doğrulamasıyla bugün örtüşüyorlar; biri
         değişip diğeri unutulursa çıplak **500** dönerdi
      2. **FK yön ayrımı yanlıştı** — `ad.Contains("BoatRentalType")` hem geleni
         (`FK_BoatRentalTypes_RentalTypes_...`) hem gideni
         (`FK_Reservations_BoatRentalTypes_...`) yakalıyordu; geçersiz kiralama
         tipi "kullanımda, silinemiyor" mesajı alıyordu. `StartsWith` önekine
         çevrildi
      3. **Migration `IF NOT EXISTS` + `CONCURRENTLY` geçersiz indeksi
         maskeliyordu** — dört adıma bölündü: çakışan veri varsa dur · önceki
         denemeden kalan GEÇERSİZ indeksi düşür · indeksi kur · gerçekten
         geçerli mi diye kontrol et
      **Denetimin İKİ iddiası YANLIŞ çıktı, kendim ölçtüm:**
      - "`Boats.PartnerId` indeksi yok" → **var** (`IX_Boats_PartnerId`)
      - "`RestrictViolation` ölü kod, EF `NO ACTION` üretir, 23503 fırlar" →
        FK'ler gerçekten `RESTRICT` (`confdeltype='r'`) ve silme denemesi
        **`23001: violates RESTRICT setting`** verdi. Kol yaşıyor
      Kanıt: migration çakışan veriyle çalıştırıldı ve **durdu**
      (`Ayni kiralama tipi bir tekneye birden cok kez eklenmis`); veri
      temizlenince geçti ve `indisvalid = t`
      Kanıt: 215 test yeşil; iki mutasyon kırmızıya döndü — `CheckViolation`
      kolu silinince, FK ayrımı `Contains`'e döndürülünce (**denetimin tarif
      ettiği hatalı mesaj birebir üretildi**)
      ⚠️ Eşzamanlılık jetonu bulgusu (kayıp güncelleme) **düzeltilmedi**:
      projede hiçbir entity'de yok, yalnız buraya eklemek tutarsız davranış
      adası yaratırdı -> [[api-benim-kararlarim]]

- [x] **A-33c** Kiralama tipi ve sezonluk fiyat uçları · bitti: 2026-08-26
      `GET/POST /api/partner/boats/{id}/rental-types` · `PUT/DELETE .../{id}` ·
      `GET/POST .../{id}/prices` · `PUT/DELETE .../prices/{id}`
      **YENİ KISIT — `IX_BoatRentalTypes_BoatRental`** (`(BoatId, RentalTypeId)`
      benzersiz). Depo kodunu yazarken bu adı taşıyan bir kısıt VAR SANMIŞTIM;
      veritabanına bakınca yoktu. Yani aynı kiralama tipi bir tekneye iki kez
      eklenebiliyordu ve "bu teknenin günlük tur fiyatı ne" sorusunun iki
      cevabı olurdu. Migration `CREATE UNIQUE INDEX CONCURRENTLY` +
      `suppressTransaction: true` — EF'in ürettiği `CreateIndex` ACCESS
      EXCLUSIVE kilidi alıyordu
      **Sessiz başarısızlığı önleyen dört kural:** temel fiyat silinemez ·
      temel ↔ sezon çevrilemez · yarım açık sezon yok · fiyat alanlarını
      kiralama tipinin stratejisi belirler (kişi başı ↔ tekne başı)
      ⚠️ **Sezon sınırı KAPSAYICI** (`daterange(..., '[]')`): bir sezonun son
      gününde başlayan sezon çakışma sayılıyor, ertesi günde başlayan geçiyor.
      Açık uçlu (`[)`) olsaydı 31 Ağustos'ta biten yaz sezonunun son günü
      sonbahar fiyatından satılırdı ve kimse fark etmezdi
      ⚠️ `RentalTypeId` değiştirilemez — değişseydi kişi başı bir tipin
      fiyatları girilip tip tekne başına çevrilebilirdi
      Kanıt: canlı — 201 tip ekleme · **400 aynı tip tekrar** ·
      400 yaş sınırı çakışması · 201 temel fiyat · **400 ikinci temel fiyat** ·
      201 sezon · **400 çakışan sezon** · 201 bitişik sezon ·
      400 kişi başı tipe tekne fiyatı · 400 yarım açık sezon ·
      400 temel fiyat silme · 204 sezon silme · 404 başka işletmenin teknesi
      Kanıt: sınır testi — 2027-10-31'de başlayan **400**, 2027-11-01'de
      başlayan **201**
      Kanıt: migration ileri/geri denendi; geri alındığında indeks düştü (0),
      tekrar uygulanınca kuruldu (1)
      Kanıt: 213 test yeşil; yedi mutasyon ayrı ayrı kırmızıya döndü
      ⚠️ **Bir testim içi boştu**: `Rezervasyonu_olan_kiralama_tipi_silinemiyor`
      rezervasyon KURMUYORDU, yalnız "rezervasyon yok" halini ölçüyordu — adının
      söylediği yasağı hiç denemiyordu. Aynı tuzağa 2026-08-25'te de düşülmüştü.
      Gerçek rezervasyon kurularak düzeltildi -> [[api-desenler]]

- [x] **A-33a** Tekne katalog uçları · bitti: 2026-08-26
      `GET/POST /api/partner/boats` · `GET/PUT /api/partner/boats/{id}` ·
      `POST /api/partner/boats/{id}/status` · `GET /api/boats/{slug}` (kimliksiz)
      **Dört duvar, dördü de ayrı test edildi:**
      kapsam (depoda `partnerId`) · sözleşme (onaylı sözleşmesi olmayan tekne
      yaratamaz) · kapasite (ticari ≤ yasal) · yayın filtresi (taslak müşteriye
      görünmez)
      ⚠️ `Status` gövdede YOK, ayrı uçtan değişiyor — yayından kaldırmak bir
      düzenleme değil, satışı durduran bir karar; olay günlüğünde de ayrı
      ⚠️ `Slug` yaratılışta addan türetiliyor ve DEĞİŞMİYOR — değişseydi
      paylaşılmış her bağlantı sessizce kırılırdı
      ⚠️ `PublicBoatDetail` panel tipinden AYRI: `FlagRegistryNo`, `CaptainName`,
      `EngineInfo`, `LegalCapacity`, `Status` müşteriye gitmiyor
      Kanıt: 401 (jetonsuz) · 400 sözleşme yokken · 201 + `Published` +
      `mavi-yolculuk-guleti-sahin` · aynı ad ikinci teknede `-2` · 400 kapasite ·
      200 kimliksiz müşteri sayfası (iç alanlar yok) · 204 yayından kaldırma ·
      **404 aynı sayfa artık pasif** · 404 başka işletmenin teknesi
      Kanıt: olay günlüğünde `boat.created`, `boat.status.changed`
      (`from: Published, to: Inactive`), `boat.viewed`, `boat.catalog.denied`
      satırları görüldü
      Kanıt: 197 test yeşil; beş mutasyon ayrı ayrı kırmızıya döndü — kapsam
      filtresi, sözleşme duvarı, kapasite kuralı, yayın filtresi ve `"ı"`
      harf çevirisi kaldırıldığında
      ⚠️ **`OpenApiBelgesiTests` bu işte KENDİLİĞİNDEN ateşledi** — altı yeni uç
      `openapi.json`'da yokken test kırmızı oldu. Bayatlama koruması süs değil

- [x] **A-33b** A-33a denetiminin iki bulgusu · bitti: 2026-08-26
      1. **Sahte "değişti" olayı**: durum zaten istenendeyse servis hiçbir şey
         yazmadan dönüyordu ama controller olayı KOŞULSUZ yazıyordu — günlüğe
         `from == to` taşıyan satır düşüyordu ve "tekne ne zaman satıştan
         çekildi" sorusu güvenilmez hale geliyordu. `ChangeStatusAsync` artık
         önceki durumu döndürüyor, olay yalnız gerçek geçişte yazılıyor
      2. **Çift sorgu**: yaratma `Guid` döndürüp controller kaydı tekrar
         çekiyordu; durum değişikliğinde de aynı satır iki kez okunuyordu
         (ve iki okuma arasında durum değişirse `from` yanlış yazılabilirdi)
      Kanıt: canlı — aynı duruma geçiş **204** ama `boat.status.changed`
      sayısı `1 → 1`; gerçek geçiş **204** ve sayı `1 → 2`,
      payload `{"from": "Inactive", "to": "Published"}`
      Kanıt: 199 test yeşil; iki mutasyon kırmızıya döndü — `null` dönüşü
      kaldırılınca ve yaratma projeksiyonundan bir alan silinince

- [x] **A-07a** OpenAPI belgesi repoda ve bayatlamıyor (API yarısı) ·
      bitti: 2026-08-26
      `./araclar/openapi-uret.sh` → repo kökünde `openapi.json` (28 uç).
      Anahtarlar sıralı yazılıyor; sıralanmasaydı aynı API iki farklı diff
      üretir, "sözleşme değişti mi" sorusu git'ten okunamazdı
      ⚠️ **Derleme sırasında üretim DENENDİ ve GERİ ALINDI.**
      `Microsoft.Extensions.ApiDescription.Server` belgeyi üretiyor ama
      `Program.cs`'i gerçekten çalıştırıyor; çalışması için bağlantı dizesi,
      imzalama anahtarı ve **üretim korumalarının atlanması** gerekiyordu.
      Bu, üretim koduna ortam değişkeniyle açılan bir "korumaları atla"
      anahtarı koymak demekti — sunucuda yanlışlıkla set edilse `AllowedHosts`,
      TLS, Postmark ve vekil korumalarının HEPSİ düşerdi. Belgeyi çalışan
      uygulamadan çekmek aynı sonucu üretim kodunu hiç değiştirmeden veriyor
      Kanıt: `OpenApiBelgesiTests` — her controller eylemi belgede aranıyor ve
      ters yönde belgedeki her uç kodda aranıyor. Veritabanı gerekmiyor
      (yalnız yansıma), CI'da çalışır
      Kanıt: iki mutasyon ayrı ayrı kırmızıya döndü — belgeden
      `POST /api/partner/transfer-ownership` silinince, belgeye `GET /api/hayalet`
      eklenince. 187 test yeşil
      **Web yarısı `A-07b` olarak Web panosunda**: `openapi-typescript` ile tip
      üretimi. Bu oturum backend oturumu, `03-Web/*`'e yazmıyor -> [[durum]]

- [x] **A-03** Kimlik doğrulamanın kalan dilimleri · **kapandı: 2026-08-26**
      Üç kalan maddesinden yalnız biri kendi başına bir işti:
      1. Platform personeli uçları → `A-38`'e devroldu (aynı işi tarif ediyordu)
      2. Satır bazlı kapsamın diğer uçlara uygulanması → `A-33`…`A-38`'e
         devroldu; kapsam, ucu yazan görevin işidir — henüz var olmayan uçlar
         için ayrı görev tutulamaz
      3. İşletme sahibinin devredilmesi → `A-03e` olarak yapıldı
      Kanıt: `A-03e` kanıt satırları · `A-38` ve `A-33` bloklarına devir notu
      düşüldü, madde kaybolmadı
      **Neden kapanıyor:** açık kalan bir görev, içindeki her madde başka bir
      görevin kabul ölçütüne dönüştüğünde artık iş değil, çift kayıt olur
      -> [[api-benim-kararlarim]]

- [x] **A-03e** İşletme sahipliğinin devri · bitti: 2026-08-26
      `POST /api/partner/transfer-ownership` — sahip, aktif bir çalışanına
      sahipliği devrediyor. Bayrak ve roller **takas** oluyor: yeni sahip sahip
      rolünü, eski sahip yeninin rolünü alıyor.
      ⚠️ `staff.manage` YETMEZ, yalnız mevcut sahip devredebilir · parola teyidi
      zorunlu · pasif çalışana devredilemez
      ⚠️ Depoda sıra bilerek "önce eski sahibin bayrağı düşer" — tersi
      `IX_PartnerMembers_SingleOwner`'a takılıyor
      Kanıt: 401 (jetonsuz) · 403 (yetkisiz çalışan) · 400 `Parola hatalı.` ·
      400 `Sahiplik zaten sizde.` · 204 (devir) · devir sonrası veritabanında
      sahiplik ve roller takas edilmiş, tek sahip · 400 `Sahipliği yalnız
      işletme sahibi devredebilir.` (eski sahip tekrar denedi)
      Kanıt: 185 test yeşil; üç mutasyon ayrı ayrı kırmızıya döndü —
      sahiplik kontrolü kaldırılınca, parola kontrolü kaldırılınca, takas
      sırası ters çevrilince (`23505 IX_PartnerMembers_SingleOwner`)
      **`A-03` bununla KAPANIYOR**: 1. maddesi `A-38`'e, 2. maddesi
      `A-33`…`A-38`'e devroldu; 3. madde bu iştir -> [[api-benim-kararlarim]]

- [x] **A-29a** Ödeme akışı, sağlayıcı soyutlaması ve defter bağlantısı ·
      bitti: 2026-08-26
      Kanıt: **uçtan uca canlı** — rezervasyon → ödeme başlat → sağlayıcı
      dönüşü → `Paid` + dört defter kaydı, **toplam 0.00**
      Kanıt: başarısız ödeme rezervasyonu `Paid` yapmıyor ve defter yazmıyor
      Kanıt: mükerrer bildirim defteri ikiye katlamıyor (iki koruma katmanı)
      Kanıt: **sağlayıcı değişse bile eski ödeme kendi sağlayıcısıyla
      çözülüyor** — PayTR'ye geçince eski İyzico iadesinin sessizce
      çalışmaması bu testle engellendi
      Kanıt: üretimde sahte sağlayıcıyla uygulama açılmıyor
      Kanıt: 181 test geçiyor


- [x] **A-18** Para defteri ve periyodik hakediş üretimi · bitti: 2026-08-26
      `LedgerService` (ödeme + iade ters kaydı) ve `GeneratePayoutsJob`
      ⚠️ Defter değişmezliğini DARALTTIM → [[api-benim-kararlarim]]
      Kanıt: ödeme kayıtlarının toplamı **sıfır** (4 kayıt); iade sonrası
      toplam **yine sıfır**
      Kanıt: `S-16` uygulandı — %50 iadede müşteri 500, işletme −425,
      platform −75 (komisyonun da yarısı)
      Kanıt: mükerrer ödeme bildirimi ikinci kez yazılmıyor
      Kanıt: **tutar hâlâ güncellenemiyor**; `PayoutId` bir kez damgalanıyor
      ve geri alınamıyor
      Kanıt: 175 test geçiyor
      ⚠️ Para hareketi yok — transfer talimatı `A-29`'a bağlı
      ⚠️ Negatif hakediş ödenmiyor, sonraki döneme kalıyor; tahsilat yok


- [x] **A-28** Bildirim gönderiminin arka plana alınması · bitti: 2026-08-26
      Giden kutusu (`NotificationOutbox`) + `DispatchNotificationsJob`
      Kanıt: **uçtan uca canlı** — rezervasyon anında iki satır `Pending`,
      Mailpit sayacı `11 → 11` (HTTP cevabı gönderimi BEKLEMEDİ); iş
      çalıştıktan sonra kuyruk **0**, Mailpit `12`
      Kanıt: gönderim düşerse bildirim KAYBOLMUYOR — satır duruyor, geri
      çekilmeli yeniden deneniyor (test)
      Kanıt: beş denemeden sonra `Failed` olarak İNCELEME İÇİN duruyor ve bir
      daha denenmiyor
      Kanıt: başarılı gönderimde satır siliniyor — kişisel verinin kalıcı
      ikinci kopyası oluşmuyor
      Kanıt: 168 test geçiyor
      ⚠️ Beş denemeden sonra kimse haberdar olmuyor (yalnız uygulama günlüğü);
      uyarı kanalı `A-38` panelini bekliyor


- [x] **A-12** KVKK saklama ve anonimleştirme akışı · bitti: 2026-08-26
      `POST /api/account/delete` — parola teyidi zorunlu
      ⚠️ Beş karar bende ve hukuki sonuç doğuruyor → [[api-benim-kararlarim]]
      Kanıt: canlı — yanlış parola **400**; doğru parola ile `Email` →
      `silinmis-…@anonim.local`, `FullName`/`Phone` → `(silindi)`,
      `Status` → `Closed`
      Kanıt: **yaklaşan turu olan müşteri reddediliyor**; iptal edince geçiyor
      ve rezervasyon iletişim alanları temizleniyor
      Kanıt: rezervasyon SİLİNMİYOR — `GrandTotalTry` dokunulmadan duruyor
      Kanıt: 165 test geçiyor
      ⚠️ Otomatik saklama süresi YOK, yalnız talep üzerine — süre hukuki karar


- [x] **A-21** Kalan olay türlerinin bağlanması · bitti: 2026-08-26
      Ölçüldü: 34 olay türünün **28'i bağlı**. Kalan altısı
      (`boat.viewed`, `search.performed`, `review.submitted`, `offer.sent`,
      `support.ticket.opened`, `platform.data.accessed`) yazılmamış uçlara ait
      **Kararım:** olay türü tek başına görev olamaz — yazacak bir çağrı yeri
      yok. Altısı da ilgili uç görevinin **kabul ölçütüne** taşındı
      (`A-33`…`A-38`), böylece uç yazılırken olay unutulamıyor
      Kanıt: `auth.*`, `account.*`, `pricing.*`, `coupon.*`, `reservation.*`,
      `boarding.*`, `partner.*`, `offer.expired`, `payment.abandoned` bağlı
      Kanıt: `Her_olay_turunun_payload_listesi_var` testi iki yönlü yansımayla
      kataloğun eksiksizliğini zaten koruyor


- [x] **A-19** Gerçek istemci IP'si (`UseForwardedHeaders`) · bitti: 2026-08-26
      Karar bende (`G-07` açık) → [[api-benim-kararlarim]]
      Kanıt: üretimde `ForwardedHeaders:KnownProxies` yoksa uygulama
      **açılmıyor**; `10.0.0.5` verilince açılıyor (canlı)
      Kanıt: `KnownProxies`/`KnownIPNetworks` varsayılanları temizleniyor —
      yalnız verilen vekillere güveniliyor
      Kanıt: ara katman EN BAŞTA; hız sınırı ve olay günlüğü gerçek IP'yi görüyor

- [x] **A-23** Npgsql havuz tavanı ve bölüm sınırlarının saat dilimi ·
      bitti: 2026-08-26
      Kanıt: havuz tavanı 20'ye sabitlendi, ortam değişkeni verilirse
      dokunulmuyor
      Kanıt: bölüm sınırı artık AÇIK saat dilimiyle yazılıyor — `Europe/Istanbul`
      ve `UTC` oturumlarında **aynı ana** işaret ediyor (canlı `pg_get_expr`
      karşılaştırması)
      ⚠️ Görevin öncülü "prod'da `SHOW TimeZone` karşılaştır" diyordu; bunun
      yerine bağımlılık tamamen kaldırıldı — doğrulanacak bir şey kalmadı


- [x] **A-25** Koltuk sayacının sefer başına taraması · bitti: 2026-08-26
      Kanıt: 40.000 sentetik satırla ölçüldü —
      **`Bitmap Heap Scan` (11 buffer) → `Index Only Scan` (1 buffer)**,
      çalışma süresi 0,031 ms, heap'e hiç gidilmiyor
      ⚠️ **Görevin öncülü kısmen eskimişti.** `A-22`'de eklenen
      `IX_Reservations_Canli` ölü satır birikmesini zaten çözmüştü; kalan sorun
      farklıydı: o indeks `Id` üzerinde olduğu için tarama TABLODAKİ TÜM canlı
      satırları kapsıyordu, tek seferi değil. Yani maliyet ölü satırlarla değil
      **eşzamanlı canlı sefer sayısıyla** büyüyordu — sezon ortasında yüzlerce
      sefer canlıyken her koltuk güncellemesi hepsini tarardı
      Kanıt: yeni indeks `VoyageId` üzerinde, toplanan kolonları içeriyor
      Kanıt: 161 test geçiyor


- [x] **A-27** Müşteri iptalinde kademeli iade hesabı · bitti: 2026-08-26
      `S-12` + `S-16` cevapları uygulandı; üç ayrıntıyı ben seçtim →
      [[api-benim-kararlarim]]
      Kanıt: canlı iptal → `oran: 100, tutar: 1500.00` ve açıklayıcı metin
      Kanıt: yedi kademe testi, **sınır anları dahil** (tam 48:00 ve tam
      24:00 müşteri lehine)
      Kanıt: kuponlu rezervasyonda iade ÖDENEN tutar üzerinden (900, 1000 değil)
      Kanıt: oran ve tutar rezervasyona donduruluyor
      Kanıt: 161 test geçiyor
      ⚠️ Para hareketi yok — `A-29` + `A-18` bekliyor


- [x] **A-32** Rezervasyonda çift gönderme koruması · bitti: 2026-08-26
      Web oturumu bildirdi, kodda doğrulandı → [[api-benim-kararlarim]]
      Kanıt: aynı anahtarla eşzamanlı iki canlı istek **aynı kodu** döndürdü
      (`XGEZ4GBE`), veritabanında **tek satır**
      Kanıt: anahtarsız istek **400**
      Kanıt: farklı anahtar iki ayrı rezervasyon açıyor (koruma her şeyi
      tekile indirmiyor)
      Kanıt: 153 test geçiyor
      ⚠️ Web tarafı her ödeme denemesinde YENİ UUID üretmeli


- [x] **A-30** Bildirim sağlayıcıları: Postmark + Netgsm + Mailpit · bitti: 2026-08-25
      `G-04` cevaplandı → [[genel-gorevler]]. `INotificationSender` arkasına
      `IEmailSender` / `ISmsSender` ayrıldı; sağlayıcı seçimi yapılandırmadan
      Kanıt: Mailpit gerçek postayı yakaladı —
      `musteri@ornek.com | Rezervasyonunuz alındı — Y4YABQ7N`
      Kanıt: **rezervasyon onayı ilk kez gerçekten gönderiliyor.** Domain
      kuralı ("hem e-posta hem SMS gider, telefon zorunlu alan") yazılıydı ama
      `SendSmsAsync` kod tabanında HİÇBİR YERDEN çağrılmıyordu
      Kanıt: telefon normalizasyonu 14 vakayla teste bağlı
      Kanıt: 143 test geçiyor

- [x] **A-30b** A-30 denetiminin altı bulgusu · bitti: 2026-08-25
      → [[api-kararlar]]
      Kanıt: **bombalama açığı kapandı** — aynı numaraya 8 rezervasyon,
      hepsi 201 (rezervasyon engellenmiyor) ama yalnız **5 bildirim** gitti,
      3'ü durduruldu (her istekte e-posta farklı, telefon aynıydı)
      Kanıt: alıcı adresi artık uygulama günlüğüne yazılmıyor
      Kanıt: üretim koruması genişledi — `::1`, `UseTls=false`, Netgsm
      kimlik bilgisi eksikliği de açılışta patlatıyor
      Kanıt: `CompositeNotificationSender` Scoped'a çekildi (Singleton'ken
      transient HTTP istemcilerini hapsediyordu — geliştirmede GÖRÜNMÜYORDU)
      Kanıt: `LoggingNotificationSender` ölü kod olarak silindi


- [x] **A-21a** Kimlik olaylarının bağlanması + jeton zinciri · bitti: 2026-08-25
      34 olay türünden 9'u bağlı değildi; **ucu olduğu hâlde loglanmayan üçü**
      bağlandı: `auth.token.refreshed`, `auth.logout`,
      `account.email_change.requested`
      Ayrıca kodun iddia ettiği ama var olmayan iki şey kod haline getirildi →
      [[api-kararlar]]
      Kanıt: `ReplacedById` artık doluyor — canlı yenileme sonrası eski jeton
      `iptal=t, zincirli=t`, yenisi `f/f`
      Kanıt: aynı jetonu ikinci kez sunma **401** ve müşteriye giden mesaj
      "hiç olmayan jeton" ile AYNI; ayrım yalnız günlükte (`auth.token.reused`)
      Kanıt: yarış deterministik olarak teste bağlandı — koşullu UPDATE'in
      koşulu kaldırılınca `Expected 0, Actual 1` ile kırmızıya dönüyor
      Kanıt: sahte jetonla çıkış **204** dönüyor ama olay kaydı ÜRETMİYOR
      Kanıt: 129 test geçiyor
      ⚠️ `A-21` KAPANMADI: arama, tekne görüntüleme, yorum, destek talebi,
      teklif ve platform erişimi olayları ilgili uçlar yazılmadığı için bekliyor


- [x] **A-05** QR biniş doğrulama uç noktası · bitti: 2026-08-25
      İki uç: `POST /api/boarding/scan` (jetonla, kamera/klavye) ve
      `POST /api/boarding/manual` (`G-12` seçenek c, rezervasyon koduyla)
      Kanıt: **eksik yolcu bilgisi binişi ENGELLEMİYOR** — 3 kişilik
      rezervasyonda hiç yolcu kaydı yokken canlı istek **200**,
      `passengerListIncomplete: true` ama durum `Boarded`
      Kanıt: kural teste bağlı — "yolcular eksikse reddet" eklemesi **altı
      testi birden** kırıyor (denendi, geri alındı)
      Kanıt: kimliksiz `scan`/`manual` **401**, `boarding.scan` yetkisi olmayan
      kullanıcı **403**
      Kanıt: başka işletmenin jetonu **tanınmıyor** ve "yok" ile aynı cevabı
      veriyor; başkasının kaydına başarısız satır bile yazılmıyor
      Kanıt: iptal edilmiş rezervasyonu okutma **400**, `BoardingScans`'e
      `Succeeded=false / Cancelled` yazıldı
      Kanıt: `Manual` jeton ucundan geçmiyor (**400**) — elle işaretleme
      QR'dan daha zayıf bir kanıt, ayırt edilebilir kalmalı
      Kanıt: olay günlüğünde jeton benzeri dizgi **0 satır**

- [x] **A-05b** A-05 denetiminin beş bulgusu · bitti: 2026-08-25
      Üç ecc denetimi; eşzamanlı okutma yarışını C# ve veritabanı denetimleri
      BAĞIMSIZ olarak kritik işaretledi → [[api-kararlar]]
      Kanıt: canlı paralel iki okutma → **2 okutma satırı, 1 durum geçişi**,
      `boardedAt` ikisinde de aynı
      Kanıt: yarış testi artık gerçekten ölçüyor — koşullu UPDATE'in koşulu
      kaldırılınca `Expected 0, Actual 1` ile kırmızıya dönüyor
      ⚠️ İlk yazdığım paralel test **yanlış sebeple geçiyordu**; koşul
      kaldırıldığında yeşil kalıyordu. Çakışmanın anı elle kuruldu
      Kanıt: `Note` kolonu ayrıldı — elle binişte `Succeeded=true` satırda
      `Note` dolu, `FailureReason` boş (canlı sorgu)
      Kanıt: 122 test geçiyor
      ⚠️ **Web tarafına devredildi:** `DeviceInfo` ve `Note` istemciden gelen
      serbest metin; panelde gösterilirken kaçış uygulanmazsa depolanan XSS
      potansiyeli var → `03-Web`


- [x] **A-03c** Devredilmiş yönetim: işletme rolleri ve çalışanları ·
      bitti: 2026-08-25
      İşletme sahibi kendi rollerini tanımlıyor, çalışanlarını ekliyor ve
      yetkilerini kısıyor. Dokuz uç, üç güvenlik duvarı → [[api-desenler]]
      Kanıt: **yükselme senaryosu canlı** — `staff.manage` + `role.manage`
      verilmiş ama `boat.write` verilmemiş çalışanın üç denemesi de reddedildi
      (kendine tam yetkili rol yazma, sahip rolünü kendine atama, sahibi çıkarma)
      Kanıt: başka işletmenin rol kimliği ve `platform.admin` rolü **404**
      (403 değil — 403 bir oracle olurdu)
      Kanıt: dört uç kimliksiz **401**
      Kanıt: katalog `commission.edit`, `platform.settings`, `partner.approve`,
      `user.manage`, `eventlog.read` içermiyor
      Kanıt: çıkarılan çalışan yeniden eklenince **aynı satır** güncellendi
      (`01a03997-…`), benzersiz indekse takılmadı
      Kanıt: üç ret denemesi de `EventLogs`'a `partner.staff.denied` olarak
      düştü, düşürülen anahtar yok
      Kanıt: 105 test geçiyor

- [x] **A-03d** A-03c denetiminin altı bulgusu · bitti: 2026-08-25
      Üç ecc denetimi (güvenlik, C#, veritabanı) → [[api-kararlar]]
      Kanıt: serbest metin sızıntısı kapandı — `permissions` dizisine yazılan
      `"0532 111 22 33 Ahmet Yilmaz"` çağırana döndü, `EventLogs`'a
      `{"reason": "UnknownOrForbiddenPermission"}` düştü
      Kanıt: e-posta oracle'ı kapandı — "kayıtlı değil" ile "başka işletmede"
      artık aynı cevap (testle sabitlendi)
      Kanıt: hız sınırı canlı çalışıyor — 18 denemeden sonra **429**, okuma
      uçları etkilenmedi (200)
      Kanıt: `IX_PartnerMembers_PartnerId` ve `IX_Roles_PartnerName` artık
      veritabanında (`\d` çıktısıyla doğrulandı); ilki EF'in indeks ezme
      tuzağı yüzünden hiç yaratılmamıştı
      Kanıt: `Roles.Name` `citext` — uygulama ile veritabanı aynı kuralı
      işletiyor, ikisi de teste bağlı
      Kanıt: üretim ortamında `AllowedHosts` boşken uygulama **açılmıyor**
      (`InvalidOperationException`), geçerli değerle açılıyor
      ⚠️ Bir bulgu bilerek düzeltilmedi: `ReplaceRolePermissions`'ta eşzamanlı
      güncellemede "son yazan kazanır". Projede hiçbir yerde eşzamanlılık
      jetonu yok; yalnız buraya koymak tutarsız olurdu


- [x] **A-26** Kupon–komisyon kuralı kaldırıldı, bedeli karşılayan taraf
      dondurulur · bitti: 2026-08-25
      Mert'in S-10 + S-14 cevabı → [[api-kararlar]]
      Kanıt: `%20` kupon `%15` komisyonlu işletmede **uygulandı** (canlı,
      `POST /api/pricing/quote` → indirim 360 TL / toplam 1440 TL); eskiden
      reddediliyordu
      Kanıt: aynı kupon `%15` ve `%25` komisyonlu iki işletmede **aynı** indirimi
      verdi — çağıranın ayırt edebildiği fark kalmadı
      Kanıt: `trg_coupon_within_commission` ve fonksiyonu veritabanından düştü
      (`pg_trigger` / `pg_proc` sayımı 0)
      Kanıt: `%30` işletme kuponuyla rezervasyon **201**, `CouponFundedBy=Partner`
      olarak donduruldu (`JUZR88GH`)
      Kanıt: kupon satırı sonradan `Platform`'a çevrildi, rezervasyon `Partner`
      kaldı — dondurma tutuyor
      Kanıt: `trg_reservation_coupon_funder` yanlış karşılayan yazılmasını
      reddetti (canlı `INSERT` denemesi hata verdi)
      Kanıt: `CK_Coupons_FundedByValue` küçük harfli `'platform'` yazımını
      reddetti; `CK_Coupons_FundedBy` `PartnerId` boşken `Partner` seçilmesini
      reddetti; `CK_Reservations_CouponFundedBy` iki yönde de reddetti
      Kanıt: migration geri alındı → tetikleyici geri geldi, tekrar uygulandı →
      tekrar düştü; `has-pending-model-changes` temiz
      Kanıt: 82 test geçiyor
      ⚠️ Devredilen: "hakediş negatif olamaz" üst sınırı KONULMADI — hangi sınır
      olacağı iş kararı, `S-15` olarak Mert'te. `A-18` bu cevap gelmeden yazılamaz

- [x] **A-26b** Kimliksiz fiyat yanıtından ticari alanların çıkarılması ·
      bitti: 2026-08-25
      Denetim bulgusu: `commissionRate` `POST /api/pricing/quote` yanıtında
      **kimliksiz** olarak düz sayı dönüyordu — yani `A-26`'nın kapatmaya
      çalıştığı çıkarım sızıntısı zaten gereksizdi → [[api-kararlar]]
      Kanıt: düzeltme öncesi canlı yanıtta `"commissionRate": 15.0` görüldü
      Kanıt: düzeltme sonrası kimliksiz yanıtta `commissionRate`, `contractId`,
      `partnerId`, `couponId`, `couponFundedBy` **yok**; `discountAmountTry` ve
      `grandTotalTry` duruyor
      Kanıt: üç test — yasak alan adları, serileştirilmiş gövdede arama,
      `QuoteResponse`'a yeni alan eklenirse patlayan liste

- [x] **A-13** `EventLogs.Payload` içeriğine sınır · bitti: 2026-08-25
      Kanıt: sekiz olay türü canlı üretildi (`pricing.quoted`, `coupon.applied`,
      `coupon.rejected`, `reservation.created`, `reservation.cancelled`,
      `reservation.cancel.failed`, `auth.login.failed`, `payment.abandoned`) —
      payload anahtarları birebir korundu, **düşürülen/kırpılan anahtar 0**.
      Yani liste gerçekten yazılanla eşleşiyor
      Kanıt-2: izinsiz anahtar (`contactEmail`) payload'a **girmedi** · 1012
      karakterlik metin 512'ye kırpıldı · iç içe nesne düştü · listesi olmayan
      olay türünün payload'ı düştü ama OLAY yazıldı
      Kanıt-3: kupon kutusuna `"0532 111 22 33 Ahmet Yilmaz"` yazıldı →
      `EventLogs`'a **`(kupon bicimi degil)`** düştü, içerik girmedi; gerçek
      kupon kodu normal yazıldı
      Kanıt-4: emoji sınırın ortasına denk geldiğinde surrogate çifti
      bölünmüyor — bölünseydi JSON yazıcısı U+FFFD koyar, veri sessizce bozulurdu
      Kanıt-5: **78 test, 78'i geçiyor**
      `EventTypes` ↔ `EventPayloadPolicy` eşleşmesi iki yönlü testle sabitlendi
      (eksik ve fazla); derleyici göremiyor
      Denetim bir bulgu verdi ve düzeltildi: serileştirme istisna fırlatırsa
      (döngüsel referans, çakışan `JsonPropertyName`) istisna dıştaki genel
      `catch`'e sıçrıyor ve yalnız payload değil **olayın tamamı** kayboluyordu
      Yan düzeltmeler: `payment.abandoned` anahtarları Türkçeden İngilizceye
      (tablo temizlenemediği için fark kalıcı olurdu) · `UserAgent` kesmesi de
      surrogate güvenli — orası `text` kolonu, bozuk metin Npgsql'de istisna
      fırlatıp olayı düşürebilirdi
      -> [[api-kararlar]] 2026-08-25

      ⚠️ `A-12`'ye devredilen iki nokta (kod değil, yazılı karar gerekiyor):
      rezervasyon kodu `EventLogs`'ta kalıcı ve `Reservations` silinse bile
      kişiye 1:1 bağlanabiliyor · `IpHash` deterministik, aynı kişinin anonim
      olayları zamanla birbirine bağlanabiliyor

- [x] **A-24** Rezervasyon iptal uç noktası · bitti: 2026-08-25
      Kanıt: `POST /api/reservations/{code}/cancel` canlı çağrıldı. Çarter iptali
      → `voyageReleased: true`, sefer `Cancelled`, **aynı tarihe yeni çarter 201**
      Kanıt-2: paylaşımlı seferde 2 rezervasyondan biri iptal →
      `voyageReleased: false`, sefer `Planned`, `SoldSeats` 5→3 — bir kişinin
      vazgeçmesi diğerlerinin turunu kapatmıyor
      Kanıt-3: yanlış e-posta ve OLMAYAN kod **aynı** mesajı verdi
      ("Rezervasyon bulunamadı.") · kod tek başına yetmiyor · tekrar iptalde
      "zaten iptal edilmiş" · `+90 500 111 22 33` kayıtlı `0500 111 22 33` ile
      eşleşti
      **Seferi bırakma mantığı ÜÇÜNCÜ KEZ KOPYALANMADI** — `VoyageRelease` tek
      yer, hem zamanlanmış iş hem iptal ucu onu çağırıyor. "Canlı satış" durum
      listesi `ReservationStatuses.Live`'a taşındı; SQL ile eşitliği
      `pg_get_functiondef` okuyan bir testle sabitlendi
      Denetim üç bulgu verdi, üçü de düzeltildi ve canlı doğrulandı:
      telefon kuyruk eşleşmesi (7 hane yetiyordu) → **tam eşleşme**;
      başarısız denemeler hiç loglanmıyordu → yazılıyor (kişisel veri yok);
      IP sınırı yetmiyordu → **koda göre saatte 5** (denendi: 5. sonrası 429,
      başka kod aynı IP'den hâlâ 400)
      `VoyageRelease`'in `Status` filtresi SUNUCUDA çalışıyor, doğrulandı:
      `r."Status" IN ('Pending','Paid','Boarded','Completed')`
      **72 test, 72'si geçiyor** · İade hesabı YOK -> `S-12`

- [x] **A-22** Rezervasyon oluşturma uç noktası · bitti: 2026-08-24
      Kanıt: `POST /api/reservations` canlı çağrıldı. **İstemci `grandTotalTry:1`
      ve `discountAmountTry:9999` gönderdi, sunucu 1800.00 ve 0 döndü** — istekte
      o alanlar YOK, tutar `QuoteAsync` ile sıfırdan hesaplandı
      Kanıt-2: dondurma eksiksiz — birim fiyat 900/500, komisyon 15, kur 1.0,
      yaş sınırları 2/12, sözleşme kimliği rezervasyona yazıldı; QR jetonu
      veritabanında 64 karakterlik SHA-256, düz metin yalnız cevapta
      Kanıt-3: **+1 gün kuralı** — 2 gece konaklamalı → 3 gün → 30.000 TL,
      sefer 10 Ekim → 13 Ekim tutuyor · **Mehmet/Cemil** — çarterin ortasına
      günlük tur satılamadı (409) · kapasite 12'de 5 dolu, 8 istendi → 409 ·
      aynı gün ikinci rezervasyon AYNI sefere bindi, `SoldSeats` 2→5
      Kanıt-4: kupon hakkı tetikleyicisi doğrudan denendi →
      `ERROR: Kupon kullanim hakki dolmus (1 / 1)`. Rezervasyonun süresi dolunca
      `UsedCount` **1 → 0**, kupon tekrar geçti
      Kanıt-5: migration geri alındı ve tekrar uygulandı (3→0→3 tetikleyici,
      indeks 1→0→1) · **60 test, 60'ı geçiyor** · hız sınırı 10. istekten sonra
      429 · uygulama günlüğünde 0 hata
      Denetim üç gerçek hata buldu, biri KRİTİK (terk edilen çarter takvimi
      kalıcı kilitliyordu, canlı üretildi ve kapatıldı) -> [[api-kararlar]] ·
      [[api-terk-edilen-sefer-kilidi]]
      İki denetim bulgusu YANLIŞ çıktı, ölçüldü: negatif sayı 400 dönüyor,
      `Location` başlığı üretiliyor
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
