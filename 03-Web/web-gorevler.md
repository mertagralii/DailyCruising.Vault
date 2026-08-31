---
rol: gorev
kapsam: web
guncelleme: 2026-08-31
durum: guncel
---

# Web Görevleri

`DailyCruising.Front-End/` işleri. Kimlik öneki **`W-`**, numara geri kullanılmaz.

**Kurallar:** Yapılıyor'da en fazla 3 görev · Tamamlandı'ya taşımak `Kanıt:` satırı
ister. Biçim ve gerekçe -> [[genel-desenler]]

## 🔵 Yapılacak

> **2026-08-27 — Mert kapsamı değiştirdi.** Önceki çerçevede tasarım otoriteydi;
> "tasarımda yok" bir işi durdurmaya yeterdi. Artık **backend otorite**:
>
> *"Tasarımımız eksik olabilir, bir temel olması adına yaptık. Sen çoğunlukla
> back-end tarafına odaklanarak ona göre tasarım kısmını geliştir."*
>
> Sonuç: **uç varsa ekran yazılır.** Tasarımda karşılığı olmaması artık gerekçe
> değil, **görev** → [[web-kararlar]]
>
> Gruplar bu ayrıma göre: uç + veri + ekran varsa **bağla** · uç var ekran yoksa
> **ekran yaz** · uç var veri yoksa **backend'e söyle** · uç yoksa **backend'e söyle**

### 🟩 A — Bağlama: uç, veri ve ekran hazır

> **2026-08-28 ölçümü.** `openapi.json`'daki **74 yol** ile front-end'in
> gerçekten çağırdığı yollar karşılaştırıldı: **21 yolun çağrısı yok.**
> Ölçüt "uç adı geçiyor mu" değil, **`api()`/`dcFetch()` çağrısında yolun
> kendisi var mı** — gevşek arama önce "hepsi bağlı" demişti, yanlıştı.
> Aşağıdaki altı görev o 21 yolun tamamını kapsıyor. **Beşinin ekranı zaten
> var**, yalnız mock veriyle çalışıyor.







- [ ] **W-66** Biniş QR'ı hiçbir uçtan gelmiyor · 🔴 **para hareketi sonrası**
      `qrImageUrl` **hiçbir yanıtta yok**; `QrCode` bileşeni yer tutucu
      çiziyor. Yani ödeme yapan müşterinin elinde okutulacak bir QR **yok**,
      yalnız kod var. Biniş ucu (`boarding/scan`) QR bekliyor
      Bugün elle kod okutma (`boarding/manual`) çalışıyor, yani biniş
      tamamen kilitli değil — ama tasarımın ve müşteriye verilen sözün
      merkezinde QR var
      Backend'e bildirilecek: rezervasyon yanıtına ya da ayrı bir uca
      imzalı QR görseli



- [ ] **W-38** Blog — uç yok, statik mi API mi karar verilmedi
- [ ] **W-39** Favoriler, kuponlarım, bildirim tercihleri — **uç yok**
      Ekranlar uydurma veri basmıyor artık (`W-39a`); kalan iş uçlar
      yazılınca. Favori ve bildirim tercihi için tablo da yok, kupon
      tablosu var ama okuyan uç yok
- [ ] **W-40** Yolcu listesi — ölçüldü, **bir uç hatası çıktı**
      Uyarı kutusu tekne detay sayfasında **zaten var ve çalışıyor**
      (`requiresPassengerList` bayrağı `true` yapılıp ölçüldü). Eksik olan
      **rezervasyon akışı**: müşteri karar verip ödediği ekranda görmüyor.
      Akışa koyacaktım, koymadım — ölçünce `pricing/quote` bu bayrağı
      **her zaman `false`** döndürüyor (aynı tekne, aynı an: tekne detayı
      `true`, işletme detayı `true`, quote `false`). Akış zaten quote
      çağırdığı için uyarıyı oradan kurmak en doğal seçimdi; kursaydım
      **hiç görünmeyen bir uyarı** yayına girecekti ve tekne sayfasında
      çalıştığı için "çalışıyor" diyecektim.
      Ayrıca `passengerListReminderHours` müşteri ucunda hiç dönmüyor
      (işletme ucunda `24` var) — "kalkıştan X saat önce" yazılamıyor.
      İkisi de backend'e bildirildi. Veri toplama kısmı KVKK'da (Mert)
      `requiresPassengerList` **tekne detayında geliyor**, form ucu yok
- [ ] **W-06** `brand.ts` kurumsal verileri · **Mert'te** (G-10)

### 🟦 E — Altyapı

## 🟡 Yapılıyor

## 🟢 Tamamlandı

- [x] **W-61** Destek talebi detayı ve yanıt · bitti: 2026-08-30
      Talep satırına **"Aç"** düğmesi; detay modalı mesaj dizisini ve
      durumu basıyor, yanıt kutusundan mesaj gönderiliyor
      Kanıt: (canlı, tarayıcıda, dört adım)
      · Gerçek talepler listelendi — `ZH8NAAND · Açık`, `PCMZRHAV ·
        Yanıtlandı`, yeni açtığım `H3YBSUJZ`
      · Detay açıldı: `other · Normal öncelik · 30 Ağustos 2026 04:58`,
        mesaj `Sen · 30 Ağu 04:58`
      · Yanıt gönderildi → mesaj listeye eklendi (`Destek · Platform ·
        30 Ağu 05:00`) ve **durum `Açık` → `Yanıtlandı`** oldu
      · Talep `Resolved`'a çekildi → **yanıt kutusu ve Gönder düğmesi
        kayboldu**, yerine "Bu talep kapandı" metni geldi
      Boş metinle Gönder **kapalı**. 390px'te taşma 0, konsol temiz
      **Dördüncü adım ayrıca ölçüldü:** kutuyu hiç basmayan bozuk bir ekran
      da ilk üç adımdan geçerdi
      ⚠️ `isInternal` gönderilmiyor — iç not yönetim panelinin ayrı işi
      🔴 **İşletme panelindeki "Destek taleplerim" hâlâ MOCK** (`#DT-1842`,
      "Deniz Yıldızı"). Uç kullanıcı bazlı çalışıyor ve işletme kendi
      taleplerini görebilir; yalnız yönetim paneli bağlandı → `W-67`

- [x] **W-67** İşletme panelinde destek talepleri gerçek uca bağlandı
      · bitti: 2026-08-30
      Kanıt: canlı — panelde `1 talep · yalnızca kendi açtıkların`,
      satır `H3YBSUJZ · Ölçüm talebi · other · 30 Ağu 04:58 · Çözüldü`.
      Mock dizelerinin üçü de (`#DT-1842`, `#DT-1830`, "Deniz Yıldızı
      başvurusu") **0 kez**. "Aç" → aynı `SupportTicket` modalı, kapanmış
      talepte yanıt kutusu yok. 390px'te taşma 0, konsol temiz
      **Bakış açısı doğru çözülüyor:** aynı talepte işletme kendi mesajını
      "Sen", platformunkini "Destek · Platform" olarak görüyor — `fromStaff`
      alanından, oturumdan değil
      ⚠️ Talepler **mock'a düşmüyor**: `undefined` halinde bile boş liste
      basılıyor. Uydurma talep, işletmeye açmadığı bir talebi varmış gibi
      okutur → [[web-kararlar]] 2026-08-28

- [x] **W-63** Yoruma cevap ve yorum denetimi · bitti: 2026-08-30
      İşletme onaylı yoruma cevap yazıyor; platform bekleyen yorumu
      yayınlıyor ya da reddediyor
      Kanıt: (canlı, iki panelde)
      · Yönetimde `Yayında` yorumda **tire**, `Onay bekliyor` yorumda
        **Denetle** — karar verilmiş satırda düğme yok
      · Yorum yayınlandı → **puan `null/0` → `5/1`, ANINDA** (tetikleyici
        `Status` değişiminde çalışıyor, iş beklemiyor). Toast bu yüzden
        "güncellendi" diyor, "güncellenecek" değil
      · İşletme panelinde `Cevap yaz` → cevap yayınlandı, satır
        `Yayında` → `Yanıtlandı` oldu ve **cevap satırın altında** göründü
      · Boş metinde düğme kapalı · **2001 karakterde de kapalı**, sayaç
        `2001 / 2000 karakter` kırmızı
      390px'te taşma 0, konsol temiz
      ⚠️ **Cevap tek atış** — uçta `PUT`/`DELETE` yok, ikinci `POST`
      `ReplyExists` alıyor. Cevap yazılınca düğme **kayboluyor**, düzenleme
      yolu hiç açılmıyor
      ⚠️ Cevap yalnız **onaylı** yorumda (`ReviewNotApproved`); denetimde
      bekleyen yorumda düğme yok
      ⚠️ Reddedilen yorum işletmeye **hiç görünmüyor** — onay metni bunu
      söylüyor, personel kararının sonucunu bilerek versin

- [x] **W-55** Tekne detay ucu · bitti: 2026-08-30
      Son eksik `program` (tur akışı) kapandı: backend liste yanıtına
      `translations` sözlüğünü ekledi (`2927af7`), form ona bağlandı
      🔴 **Bir veri kaybı önlendi.** Uç `name`/`program`'ı **gösterim**
      olarak döndürüyor (çözülmüş, katalog adına düşebilen) ama `PUT`
      `translations` sözlüğünü **tam** kabul ediyor. Form gösterim
      alanlarına bağlı kalsaydı her kaydetme İngilizce çeviriyi
      **sessizce silerdi** — uç `204` döner, hata görünmezdi
      Kanıt: panelden Türkçe ad değiştirildi → `tr` güncellendi ve
      **`en` yerinde kaldı** (`Bay tour (full day)`). Düzeltme öncesi bu
      kayıt silinecekti
      Ad boşsa Türkçe kaydı çıkarılıyor (silme kastı) ve backend katalog
      adına düşüyor; ipucu metni o durumda hangi adın kullanıldığını
      **yazıyla** söylüyor — `name` doluyken `translations` boş olabiliyor
      ve bu ayrım ekranda görünmezdi



- [x] **W-68** Kurumsal ve pazarlama sayfalarındaki uydurma sayılar · 2026-08-31
      Herkese açık üç sayfa, karşılığı olmayan rakam basıyordu.
      `/add-boat`: "%12 komisyon" ve "3 gün ödeme" — ikisi de **sözleşme
      başına** tanımlı (`Contract.CommissionRate`, `PayoutPeriodDays`,
      varsayılan 14) ve canlı veride herkes %15'te; para zaten elle
      aktarılıyor. Üç "kaptan görüşü" ad, şehir ve tekne sayısıyla
      uydurulmuştu; bölüm boşken başlığıyla birlikte hiç basılmıyor.
      `/about`: "340+ tekne · 96.000 misafir yeri · 4,8/5 üzerinden 4.812
      yorum". Ölçülen gerçek **10 tekne, 2 onaylı yorum, 11 bölge** —
      tekne otuz kat, yorum iki bin kat şişikti.
      Ana sayfa: altı tur kategorisi toplam **250 tekne** iddia ediyordu.
      `/blog`: "Tümü · 48" yazıyordu, 7 yazı var; sayaç artık listeden
      hesaplanıyor, yani güncellenmesi gereken ikinci bir yer kalmadı —
      bayat sayının kaynağı hep bu ikilikti.
      **Dokunulmayanlar bilinçli:** ana sayfadaki "₺750'den" başlangıç
      fiyatları canlı sitenin gerçek değerleri olabilir, ölçmeden silmek
      yanlış olurdu → `S-29`. `brand.ts`'teki "340+" `W-06` ile Mert'te.
      Kanıt: `/add-boat`, `/about`, `/blog` canlı ölçüldü → %12, 3 gün,
      120 bin, 340+, 96.000, 4.812, "· 48" ve üç yazar adı **hiçbiri
      sayfada yok**; yatay taşma 0, konsol temiz.
      `718df36` · `e4ebb10` · `548d19a`

- [x] **W-36b** İşletme ayarları yazılabilir · 2026-08-31
      Mert onayladı ("ayarlar ucunu da yaz, sadece işletmenin
      değiştirebileceği alanlar"), backend `GET/PUT /api/partner/profile`
      yazdı. Ekran beş alanı yazıyor: işletme adı, e-posta, telefon,
      adres, şehir.
      Önceki hâli **paneldeki en tehlikeli mock'tu**: "Ödeme bilgileri"
      başlığı altında bir IBAN ve vergi numarası gösteriyor, yanında
      "hakediş ödemeleri bu hesaba yapılır" yazıyordu. İşletmeci kayıtlı
      hesabını doğrulamış sanabilirdi.
      **Kilitli alan için devre dışı input basılmıyor, salt okunur satır
      basılıyor** — devre dışı kutu "izin verilirse değişir" diye okunur.
      IBAN'ın yalnız son dört hanesi geliyor; neden değiştirilemediği
      yazıyla söyleniyor. Komisyon ve periyot bu ekranda hiç yok.
      Kanıt (kendi ölçümüm): gövdeye `legalName`, `taxNumber`, `iban`,
      `status` eklenip gönderildi → **dördü de değişmedi**, yalnız telefon
      yazıldı. Kimliksiz 401. Panelden `ISLETME-...@ORNEK.COM` kaydedildi
      → küçük harfli hâli ekranda göründü, uçtan okunduğunda kalıcıydı.
      `49469c5`

- [x] **W-39a** Hesap sayfasındaki uydurma müşteri verisi kaldırıldı · 2026-08-31
      Giriş yapmış müşteri kendi hesabını gördüğünü sanıyordu. En zararlısı
      kupon: "%10 indirim · DC10" ve "YAZSONU250" görünüyordu, müşteri
      bunları **ödeme adımında kullanmayı deneyip başarısız olurdu.**
      Favorilerde hiç kaydetmediği dört tekne, geçmişinde hiç katılmadığı
      dört tur, profilinde "Deniz Yılmaz" adı vardı.
      Bildirim tercihleri daha sinsiydi: anahtarlar açılıp kapanıyor ama
      hiçbir yere kaydedilmiyordu — kapatılan bildirim yine gelirdi.
      "Profilini tamamla · %70 · ✓ E-posta doğrulandı" kutusu **aynı
      sayfayla çelişiyordu**: profil sekmesi e-postayı "doğrulanmadı"
      gösterirken bu kutu doğrulanmış sayıyordu.
      Gerçeğe bağlananlar: profil (oturum), yaklaşan/geçmiş sayaçları ve
      geçmiş tur listesi (gerçek rezervasyonlar), sekme sayacı.
      Ucu olmayan dört bölüm sebebini yazıyor **ve bugün ne yapılabileceğini
      söylüyor** (kupon kodunu ödemede gir, parolayı Şifremi unuttum ile
      değiştir) — `W-39`'un kalanı hâlâ uç bekliyor.
      Kanıt: müşteri hesabıyla altı sekme gezildi → 0 uydurma dize; profil
      "Tohum Müşteri · doğrulanmadı", sayaçlar 1 yaklaşan / 3 geçmiş,
      rezervasyon RPAJWZCH gerçek. Taşma 0, konsol temiz. `3c18b17`

- [x] **W-36a** İşletme paneli gerçek veriye bağlandı · 2026-08-31
      Panel işletmecinin kendi işini gösterdiğini iddia ediyor ama tasarım
      verisi basıyordu: "₺186.400 bu ay net hakediş", "48 tur", "%78
      doluluk", "Gulet Işıl · Mavi Rüzgar · Deniz Yıldızı" ve son
      rezervasyonlarda **başka birinin müşteri adları** ("Elif Demir",
      "Zeynep Aksu"). Yönetim panelindekinden ağırdı: orada uydurma olan
      platform istatistiğiydi, burada işletmecinin **kendi parası**
      sandığı rakam.
      Bağlananlar: genel bakış kartları (`partner/finance/summary` +
      `partner/boats` + `partner/reviews`), yaklaşan turlar ve rezervasyon
      listesi (`partner/reservations` — backend bu oturumda yazdı),
      müsaitlik takvimi (`partner/boats/{id}/calendar`; uç zaten vardı,
      **menüden ulaşılamadığı için** modül mock basmaya devam ediyordu),
      panel başlığı (oturumdaki kullanıcı), değerlendirme özeti.
      Menü rozetleri kaldırıldı — "Değerlendirmeler 4,8", "Personel 6",
      "Tekne listesi 3" sabit yazılıydı; gerçekte 1 yorum, 2 tekne.
      Ayarlar ekranındaki **uydurma IBAN ve vergi numarası** kaldırıldı:
      "hakediş ödemeleri bu hesaba yapılır" diyordu ve işletmeci kayıtlı
      hesabını doğrulamış sanabilirdi.
      İki sınır ekranda **yazıyla** duruyor: iptaller uçta eleniyor,
      en fazla 50 kayıt geliyor. Sessiz kesme listeyi "hepsi bu" okutur.
      Kanıt: işletme hesabıyla ölçüldü → ₺4.250 hakediş / 3 kayıt,
      2 tekne / 2 yayında, 5,0 puan / 1 değerlendirme, 2 yaklaşan tur
      gerçek tekne adıyla; yatay taşma 0, konsol temiz.
      Uç ölçümü (kendi ölçümüm, rapora değil): varsayılan 7 kayıt,
      `includeCancelled=true` 9, `status=Cancelled` 2, tarih süzgeci 2.
      `f973baa` · `4e3e42c`

- [x] **W-41** Kısa tarih biçimine yıl eklendi · 2026-08-31
      `2027-06-17` kalkışlı bir tur listede **"17 Haz"** görünüyor ve
      bugünden önceymiş gibi okunuyordu. Rezervasyonlar birden çok yıla
      yayıldığı için yılsız kısa biçim burada yanlış.
      Bu kusur **mock veriyle görünmezdi**: uydurma kayıtların hepsi aynı
      yıldaydı. Gerçek uca bağlanınca ilk ölçümde çıktı.
      Kanıt: `tarihSaat(iso, "kisaYil")` eklendi, yalnız rezervasyon
      kalkışında kullanılıyor; müşteri tarafı zaten yıllı uzun biçimde.
      `f973baa`

- [x] **W-37** Yönetim paneli — uydurma veri kaldırıldı · 2026-08-30
      25 modülün 21'inin arkasında uç yok ama hepsi dolu ekran basıyordu
      (₺38,4 M ciro, 24.806 kullanıcı, "Serkan Öz · Öz Yatçılık"). Tasarım
      verisiydi; platform adına karar veren personel için uydurma rakam boş
      ekrandan kötü.
      Kaynağı olmayan modül artık **neden** bağlı olmadığını yazıyor ve
      varsa gerçek verinin yerini gösteriyor (tekneler → işletme satırındaki
      Belgeler, `platform/partners/{id}/boats` orada zaten kullanılıyor).
      Boş tablo da basılmıyor: "kayıt yok" bir olgu iddiasıdır.
      Ulaşılamaz 20 mock detay ekranı silindi — `detailScreens` bağlıydı ama
      gerçek listelerin işlem hücresi nesne olduğu için `setDetail(true)` hiç
      çalışamıyordu. Tasarım kaynağı `Rihtim.dc.html`'de duruyor.
      Kanıt: 25 modül tek tek gezildi → 4 bağlı (12 işletme · 3 talep ·
      3 yorum · 10 zamanlanmış iş, hepsi gerçek), 21 yazı, **0 uydurma dize**.
      "Uydurma yok" tek başına sayılmadı; bağlı 4 modülün veri bastığı ayrıca
      ölçüldü — sayfa boş olsaydı ilk ölçüm de temiz görünürdü. `9ba951d`

- [x] **W-35** Finans ve hakediş · bitti: 2026-08-30
      Bölüm **geri açıldı** — 2026-08-28'de tümden kapatılmıştı, çünkü
      "Ödendi / Aktarıldı / 3 iş günü içinde IBAN'ınıza" metinlerinin hiçbiri
      bir şeye dayanmıyordu. Uçlar geldi ve defter gerçek
      Kanıt: canlı — `TOPLAM HAKEDİŞ ₺4.250 · HESABINA GEÇEN ₺0 · YOLDA ₺0 ·
      BEKLEYEN ₺4.250`, defterde 3 kayıt rezervasyon koduyla
      (`Hakediş · MC5GU38F · ₺1.955`). **"Ödendi", "Aktarıldı", "3 iş günü"
      dizelerinin üçü de sayfada YOK.** 390px'te taşma 0, konsol temiz
      ⚠️ **Rakamlar doğru, para henüz gitmiyor.** Tahsilat platform
      hesabında, transfer elle (`A-41`). Ekran bunu **rozetle değil
      cümleyle** söylüyor: "hesaplanmış hakedişin… transferler elle
      yapılıyor". `A-41` açılınca metin değişir, ekran değişmez
      ⚠️ Dört tutar ayrı: `totalEarned = settled + inTransit + pending`.
      **Başarısız ödeme "yolda" değil "bekleyen"** — parası platformda

- [x] **W-57** İşletme paneli — tekne kaydının kalan alanları
      · bitti: 2026-08-30
      Künye bölümü açıldı: ad, marina, iki kapasite, kabin/yatak/banyo,
      mürettebat, boy/en, yapım ve bakım yılı, kaptan, motor, sicil no
      Kanıt: kabin `3 → 4` ve kaptan adı yazıldı → sunucuda göründü;
      **aynı istekte kapasite, açıklama, donanım (2) ve kurallar (2)
      bozulmadı**. Sonra geri alındı
      ⚠️ **`PUT` tam değiştirme**: gövde kaydın tamamı oluyor. Ekran
      `GET` edip üzerine yazıyor; göndermediğin alan sıfırlanır
      ⚠️ **Boş dize `null` oluyor, `0` değil.** "Girmedim" ile "sıfır"
      ayrı şeyler — kapasiteyi sıfıra düşürmek tekneyi satıştan düşürürdü
      ⚠️ **Tekne tipi ve bölge burada YOK.** İkisi katalog seçimi
      (`UnknownLookup`) ve ikisi de fiyatlandırmayı + aramada görünmeyi
      etkiliyor. Ekranda sebebi yazıyor

- [x] **W-60** İşletme paneli — personel yönetimi yazma tarafı
      · bitti: 2026-08-28
      `PUT members/{id}/role` · `POST members/{id}/deactivate` ·
      `PUT roles/{id}` · `DELETE roles/{id}` — dördü de bağlandı
      Kanıt: canlı, tarayıcıda — rol oluşturuldu (`2 yetki`), **düzenlendi**
      (`3 yetki`, form dolu açıldı), **silindi**. Personel eklendi, **rolü
      değiştirilebiliyor**, **pasife alındı** ve satır `Pasif` oldu.
      Kullanımdaki rolü silme denendi → **"Bu rolde personel var. Önce
      onları başka bir role al."** 390px'te taşma 0, konsol temiz
      Sahip rolünde Düzenle/Sil düğmesi **hiç yok** (`OwnerRoleImmutable`);
      rol değiştirme listesinde sahip rolü **görünmüyor**
      (`OwnerRoleNotAssignable`); pasif personelde rol değiştirme kapalı
      (`TargetInactive`)
      🔴 **Yolda bir hata bulundu:** oturum jetonu ekran açıkken dolunca
      (`401`) panel **"Henüz personel yok"** diyordu — altı kişilik ekibi
      olan işletmeye personeli olmadığını söylüyordu. Boş durum bir **olgu
      iddiasıdır**; okuma başarısızken edilemez. Artık "Liste okunamadı +
      sebep + Yeniden dene" basılıyor
      ⚠️ **`memberCount` silinebilirliği belirlemiyor** — yalnız AKTİF
      personeli sayıyor, silme ise **pasif** olanı da sayıyor. Backend
      ayrı bir `canDelete` alanı ekledi (`35d9434`); Sil düğmesi ona bağlı,
      sayıya değil. Sayı 0 ama silinemiyorsa satırda sebebi yazıyor:
      *"çıkarılmış bir çalışanın kaydında duruyor, silinemez"*
      Kanıt (üç durumun üçü de tarayıcıda): kullanılmayan rol →
      `canDelete: true`, Sil **var**, silme **başarılı** · pasif çalışanın
      taşıdığı rol → `memberCount: 0`, `canDelete: false`, Sil **yok**,
      sebep satırda · sahip rolü → düğme yok
      **Olumlu durum ayrıca ölçüldü:** `canDelete` her zaman `false` olsaydı
      bütün olumsuz sınamalar yine geçerdi

- [x] **W-65** Saatlerin Türkiye saati olduğu yazılıyor · bitti: 2026-08-28
      `TimezoneNote` — "Saatler Türkiye saatiyle (UTC+3) gösterilir."
      Basıldığı yerler: tekne detayında kiralama tipleri (**yalnız saat
      aralığı gösteren tip varsa**), rezervasyon detayı, misafir sorgulama
      sonucu
      Kanıt: canlı — saatli tipte 1 kez basılıyor, sorgulama sayfasında
      sonuç yokken **0 kez**. 390px'te taşma 0
      ⚠️ **Her zaman damgasının yanına konmadı**: saat başına bir ibare
      gürültü olur, gürültü okunmaz. Not, saatin **karar değiştirdiği**
      yerlerde bir kez basılıyor
      Metin backend'in onay e-postasındakiyle **bilerek aynı**

- [x] **W-62** Belge içeriğini görüntüleme · bitti: 2026-08-28
      İki panelde de tam: işletme kendi tekne belgelerini yönetiyor
      (liste · yükle · indir · sil), platform personeli işletme evrakını ve
      **her teknenin** evrakını görüyor
      Kanıt: canlı zincir — yönetim panelinde işletme satırı → Belgeler →
      `Tohum Fiyatlı 1787869006 · Yayında → Ruhsat · TR-2026-4471 ·
      15 Ocak 2026 – 15 Ocak 2027 · İnceleniyor`, indirme
      **200 · application/pdf · 82 bayt · `%PDF-` imzası**.
      Pasif tekne de listeleniyor (`Kisit Testi · Pasif`) — personel
      başvuruyu incelerken tekne yayında olmuyor, süzülseydi liste tam
      ihtiyaç anında boş dönerdi. 390px ve 1280px'te taşma 0, konsol temiz
      Liste bileşeni **iki panelde ortak** (`document-list.tsx`)
      ⚠️ Onaylı belgede silme düğmesi **hiç yok** (`VerifiedDocumentLocked`)
      ⚠️ **Geçerlilik sonu günün BAŞI olarak saklanıyor** — süre dolumu
      uyarısı yazılırsa belge o günün **sonuna** kadar geçerli sayılmalı
      ⚠️ İndirmede `400` ayrı mesaj veriyor: "kayıt var, dosya yok" gerçek
      bir hal ve "yetkin yok" demek yanıltıcı olurdu

- [x] **W-56** Alt puanlar · bitti: 2026-08-28
      Tekne detayında kırılım (temizlik · ekip · yemek · fiyat/performans),
      yorum formunda puanlama
      Kanıt: `a04-teknesi` → **Temizlik 5,0 · Ekip 5,0 · Yemek 4,0 ·
      Fiyat/performans 4,0**, her satırda kaç kişinin puanladığı parantezde.
      Puanı olmayan teknede bölüm **hiç basılmıyor** (ölçüldü: 0 kez).
      390px'te taşma 0
      🔴 **Yolda iki gerçek hata bulundu, ikisi de bendeydi:**
      davet yanıtı tipinde dört alan uydurulmuştu — "bu bağlantı kullanılmış"
      ekranı **hiç görünmüyordu** ve ekranda `Rezervasyon undefined`
      yazıyordu · yorum formundaki alt puan anahtarları koda gömülüydü, uç
      **kriter kimliği** bekliyor → [[web-elle-yazilan-tip-yalan-soyler]]
      Kriterler artık davet yanıtından geliyor, koda gömülü değil

- [x] **W-34** Müsaitlik takvimi — **işletme yarısı bitti** · 2026-08-28
      Ay ızgarası, aralık seçimi, sebeple satışa kapatma, tek tek açma.
      Dört durum: `Satıldı` · `Kapalı` · `Açık teklif` · boş — **renk tek
      başına taşımıyor**, her hücrenin `title` ve ekran okuyucu metni var
      Kanıt: canlı zincir — panelden **20–22 Eylül 2026** "Motor bakımı"
      sebebiyle kapatıldı → müşteri ucunda üçü de `isAvailable=false`,
      `remainingSeats=0` → panelden üçü de açıldı → üçü `müsait/12`e döndü.
      Sebep boşken düğme kapalı. 390px'te hücre 42×42, ızgara taşması **0**
      Bu ekran gelene kadar **işletme bir günü kapatamıyordu**: bakımdaki
      tekne için rezervasyon gelebiliyordu ve önlemenin yolu yoktu
      ⚠️ Silme düğmesi yalnız `isBlocked` günde — `blockId` alanında satış
      seferinin kimliği de gelebiliyor; backend süzüyor ama yanlış istek
      hiç gönderilmiyor
      ⚠️ `toISOString()` **kullanılmadı**: ay sınırı yerel tarihten
      kuruluyor, yoksa `Europe/Istanbul`'da ayın ilk günü bir önceki aya
      kayardı

- [x] **W-64** Gönderilen sözleşmenin metnini panelde okuma
      · bitti: 2026-08-28 · **Mert istedi**
      İşletme satırındaki "Sözleşmeler" düğmesi listeyi açıyor; her satırda
      şablon adı+sürümü, komisyon, hakediş periyodu, tarih ve durum var.
      "Metni oku" `bodyHtmlSnapshot`'ı gösteriyor
      Kanıt: canlı — "FE Test" işletmesinde `Tohum Sözleşmesi 1787875833 ·
      v1 · Komisyon %15 · hakediş 14 gün · Gönderildi`, metin açıldı
      🔒 **Metin `sandbox=""` `<iframe srcDoc>` içinde**, tarayıcıda
      doğrulandı: `contentWindow.document` erişimi **`SecurityError`** ile
      reddediliyor, yani yalıtım gerçek. `dangerouslySetInnerHTML`
      kullanılmadı → [[web-kararlar]] 2026-08-28
      "Sözleşmeler" düğmesi **her durumda** açık — reddedilmiş ya da askıdaki
      işletmenin geçmişte neyi imzaladığı tam da uyuşmazlıkta sorulur
      390px ve 1280px'te taşma **0**, konsol temiz

- [x] **W-58** İşletme paneli — fiyatlandırma ve ek hizmetler
      · bitti: 2026-08-28 · **12 işlem**
      Kiralama tipi · fiyat · ek hizmet: üç katman da okuma+yazma+silme
      Kanıt: canlı, tarayıcıda ölçüldü — panelden **1 Temmuz – 31 Ağustos
      2027 sezon fiyatı** eklendi (yetişkin 1400, çocuk 800, bebek 0) ve
      `Prices` tablosunda `2027-07-01 | 2027-08-31 | 1400.00 | 800.00 | 0.00`
      olarak göründü; sonra panelden silindi ve tablo eski hâline döndü.
      Ek hizmet formu "Öğle yemeği menüsü · 350" ile doldu. Kiralama tipi
      düzenlemede **katalog seçicisi kilitli** (backend
      `RentalTypeImmutable`). Taban fiyat satırında **Sil düğmesi hiç yok**
      (`BasePriceUndeletable`). 390px ve 1280px'te taşma **0**, konsol temiz
      **Bu ekran gelene kadar işletme kendi fiyatını giremiyordu** — tarife
      yalnız veritabanına elle yazılarak oluşuyordu
      ⚠️ Ek hizmet **açıklaması gösterilmiyor**: `GET` `names` (düz dize)
      döndürüyor, `PUT` `translations` (`{name, description}`) istiyor.
      Açıklama okunamadığı için forma konsaydı kaydedince **silinirdi**
      ⚠️ Yaş sınırları ve saat/gün alanları biçime göre değişiyor; ikisi
      karşılıklı reddediliyor (`TimesRequired` / `DurationRequired`)

- [x] **W-59** Yönetim paneli — iş ortağı onay akışı · bitti: 2026-08-28
      **6/6.** `review` · `contracts` · `reject` · `suspend` · `reinstate` ·
      `payee` — hepsi bağlı ve canlı doğrulandı
      Kanıt: "FE Test" işletmesi uçtan uca yürüdü —
      **İncelemeye al** → sunucuda `UnderReview`; **Sözleşme gönder**
      (şablon listesi 9 kayıt, komisyon %15, periyot 14 gün) → sunucuda
      `Partners.Status = ContractSent` ve `Contracts` satırı
      `15.00 · 14 · Sent`. Eylem kümesi her adımda kendiliğinden daralıyor
      Sınır kapıları istemcide de tutuluyor: komisyon 150 → düğme kapalı,
      periyot 120 → kapalı, 15/14 → açık. Sebep boş ya da yalnız boşlukken
      red/askı düğmesi kapalı. 390px ve 1280px'te taşma **0**, konsol temiz
      ⚠️ **Komisyon oranı ve hakediş periyodu ön doldurulmuyor.** Şablon bu
      iki değeri taşımıyor; varsayılan **uydurmak** yanlış oranla bağlanmış
      bir sözleşme demek olurdu. Her sözleşmede bilerek giriliyor → Mert
      şablona varsayılan eklemek isterse şema kararı (`S-?`)
      ⚠️ Sözleşme metni panelde okunamıyor → **`W-64`** (Mert istedi)

- [x] **W-03** Tekne görselleri · bitti: 2026-08-28 · **backend + web**
      Kanıt: canlı, tarayıcıda ölçüldü —
      · **Arama kartı** — `GET /api/search` `coverUrl` veriyor, dokuz teknenin
        ikisinde gerçek görsel, yedisinde gradyan yer tutucu. `/_next/image`
        **200**, `image/jpeg` 3139 bayt
      · **Tekne detayı** — `media[]` galeriye bağlandı, iki görselli teknede
        1 ana + 2 küçük resim. Açılışta **kapak** gösteriliyor: ölçümde kapak
        `sortOrder: 1`'deydi, listenin ilk elemanı değil
      · **İşletme paneli** — kart kapağı gerçek görsel, rozet `2 görsel` /
        `1 görsel`. Yükle · sırala · kapak seç · sil dördü de çalışıyor;
        her işlemden sonra kart rozeti `router.refresh()` ile tazeleniyor
      · **Sıralama kapağı bozmuyor**: kapağı 2. sıraya taşıdım, sunucuda
        `sortOrder 1 · isCover true` kaldı. Kapak değiştirince arama
        yanıtındaki `coverUrl` de değişti
      · **390px taşma taraması** — `/boats`, tekne detayı, panel + modal:
        dördünde de **0px**. Konsolda hata yok
      🔴 **Yolda gerçek bir hata bulundu ve düzeltildi:** vekil çok parçalı
      gövdeyi bozuyordu → [[web-vekil-multipart-boundary]]. Bu yalnız gerçek
      dosya yüklenince çıktı; `build`, `lint` ve `tsc` üçü de temiz geçiyordu

- [x] **W-53** · **W-54** Referans adları ve donanım/kural listeleri
      · bitti: 2026-08-28 · **backend + Mert'in onayı**
      Kanıt: `/boats` filtre menüsünde gerçek Türkçe adlar — **Bodrum, Gökova,
      Marmaris, Datça, Göcek** · **Günlük tekne turu, Dalış turu, Gün batımı
      turu, Konaklamalı tur, Haftalık kiralama**. Donanım **9**, kural **3**
      ⚠️ **"Tur özellikleri" filtresi geri KONMADI.** Donanım listesi doldu ama
      `GET /api/search`'te donanım parametresi **yok** — liste gösterilip süzme
      yapılamazdı. Backend'e bildirildi, `W-55` ile birlikte gelecek
      ⚠️ Tekne detayındaki "Teknede neler var" / "Kurallar" da **kurulamadı**:
      `lookups` katalogu veriyor, `GET /api/boats/{slug}` teknenin **atamasını**
      döndürmüyor. Bu hâlâ `W-55`
      ⚠️ Geliştirme veritabanında `a04-*` çöpü çevirisiz duruyor ve listede
      görünüyor — **süzülmedi**, backend'in isteği (temiz veritabanında yok)
      Not: uç değişikliği ekrana **5 dakika gecikmeyle** yansıdı; `lookups`
      yanıtı o kadar önbelleklenmiş durumda. Referans verisi için makul

- [x] **W-32** Misafir rezervasyon sorgulama · bitti: 2026-08-28
      Kanıt: `5GDRAYDE` + doğru e-posta → **200**, `Paid`, "A04 Teknesi".
      **Yanıtta iletişim alanı YOK** — backend bunu testle sabitlemiş
      Kanıt: yanlış e-posta ile olmayan kod **aynı gövdeyi** dönüyor
      (`"Rezervasyon bulunamadı."`) — geçerli kod ayıklanamıyor
      ⚠️ **Okuma ama `POST`**: kimlik bilgisi gövdede. Sorguda gitseydi
      e-posta ve telefon sunucu günlüklerine, vekil kayıtlarına ve tarayıcı
      geçmişine **düz metin** yazılırdı
      ⚠️ **Kod büyük harfe çevriliyor** — uç tam eşleşme istiyor (`5gdrayde`
      → `400`, ölçüldü). Backend bunu bilerek gevşetmedi: yalnız burada
      gevşetilseydi küçük harfli kod rezervasyonu **gösterir ama iptal
      ettirmezdi**
      ⚠️ Hız sınırı **saatte 20 ve koda göre**; sonuç tutuluyor, her
      render'da yeniden sorgulanmıyor

- [x] **W-20 doğrulaması tamamlandı** · 2026-08-28
      Kanıt: tarayıcıda tohum hesabıyla — konuşma listesi "Tohum Fiyatsız",
      gerçek mesaj, **maskelenmiş mesaj `[gizlendi]` ekranda**, teklif
      **₺25.000** geçerlilik süresiyle, "Teklifi kabul et" düğmesi, sunucudan
      gelen dış ödeme uyarısı, maskeleme bildirimi. Yatay taşma yok
      Önceki kayıttaki "tarayıcı doğrulaması yapılamadı" uyarısı **kalktı**

- [x] **W-20** Mesajlaşma ve özel teklif · bitti: 2026-08-28
      Kanıt: veri yolu canlı doğrulandı — konuşma "Tohum Fiyatsız", durum
      `Open`, gerçek mesaj; teklif **25.000 TRY · Sent · 6 yetişkin ·
      2027-07-05**, geçerlilik damgasıyla
      Kanıt: **maskeleme doğrulandı.** Gönderilen *"Beni 05321234567
      numarasından arayın, mail: test@ornek.com"* → saklanan *"Beni
      [gizlendi] numarasından arayın, mail: [gizlendi]"*. Arayüzdeki uyarı
      metni bu yüzden doğru
      ⚠️ Tasarımda **hiç yoktu**: tasarım 21 Ağustos'ta çizildi, domain kararı
      23 Ağustos'ta alındı (*"iletişim telefonla değil sistem içi
      mesajlaşmayla"*)
      Aynı bileşen **iki tarafı** da sunuyor; fark yalnız kimin mesajı sağda
      ve teklifi kimin gönderip kimin kabul ettiği
      ⚠️ **Gerçek zamanlı altyapı yok** → yoklama, 5 sn (sınır dk/120).
      **Kapalı konuşmada yoklama duruyor** — değişmeyecek şeyi sormak boşuna
      Dış ödeme uyarısı **sunucudan** geliyor, metni uydurulmuyor
      ✅ Tarayıcı doğrulaması **sonradan tamamlandı** — aşağıdaki kayda bak

- [x] **W-12** OpenAPI'den tip üretimi · bitti: 2026-08-28
      Kanıt: `npm run tip-uret` → `src/lib/api/types/uretilen.ts` (3.368 satır),
      **70 yol · 87 işlem**
      Betik her çalıştığında sözleşme boşluklarını **yüzeye çıkarıyor**:
      `yanıt şeması olan işlem: 0/87` · `14 enum belgede 'integer'`.
      Sessizce üretmek "tipler var demek ki güvenli" yanılgısını beslerdi
      İstek gövdeleri üretilen tipten okunuyor (`booking.ts`): backend bir alan
      adı değiştirirse **derleme kırılır**, çalışma zamanında değil
      ⚠️ Yanıt tipleri elle yazılmaya devam ediyor — belgede yanıt şeması yok

- [x] **W-49** İşletme başvuru formu · bitti: 2026-08-28
      Kanıt: **canlı başvuru açıldı** — `{"partnerId":"01a0459b-…",
      "status":"ApplicationReceived"}`. Eksik alanla gönderim `400
      ValidationFailed` ve **sekiz alanın adı** tek tek dönüyor
      ⚠️ Tasarımdaki form **gönderilmiyordu** ve alanların yarısı eksikti:
      vergi dairesi, vergi no, IBAN, işletme türü, adres, şehir. Uç on altı
      alanın hepsini zorunlu tutuyor
      ⚠️ Uç bir iş kuralı ortaya çıkardı: **şahıs başvurusunda 11 haneli TC
      kimlik**, şirkette 10 haneli vergi no. İpucu işletme türüne göre
      değişiyor — yazılmasaydı kullanıcı bunu `TaxNumberInvalid` hatasını
      gördükten sonra öğrenirdi
      Başarı metni **uçtan geliyor** (`note`), kendi metnimiz değil: süreç
      değişirse metin de sunucuda değişir
      Belge yükleme başvuruya konmadı — panel açıldıktan sonra yapılıyor

- [x] **W-45** Rol yönetimi ve sahiplik devri · bitti: 2026-08-28
      Kanıt: işletme panelinde gerçek veri — personel "Tohum Kaptan", rol
      "İşletme Sahibi · **1 kişi · 25 yetki**". Rol oluşturma modalında
      **25 izin kutucuğu**, 8 gerçek kategoride (Fiyat, İçerik, İş ortağı,
      Mesajlaşma, Para, Rezervasyon, Takvim, Tekne)
      ⚠️ Tasarımda **personel listesi vardı, rol editörü yoktu.** Domain:
      *"roller sabit değil, iş ortağı kendi çalışanlarını tanımlar ve
      yetkilerini kısar"* — rol düzenlenemiyorsa o karar karşılıksız kalıyordu
      ⚠️ `GET /api/partner/permissions` çağıranın **verebileceği** izinleri
      döndürüyor; kimse kendinden fazla yetki veremiyor ve kısıt **sunucuda**
      ⚠️ Sahiplik devri parola istiyor — tek tıkla yapılamayacak kadar ağır

- [x] **W-21** · **W-47** Yorum daveti ve tekne durum etkisi · bitti: 2026-08-28
      Kanıt: (`W-21`) `/review` jetonsuz → "Değerlendirme bağlantısı gerekiyor",
      uydurma jetonla → uç `404 "Değerlendirme linki geçersiz."` → ekranda
      "Bağlantı geçersiz". Kullanılmış davet ayrı ele alınıyor (`usedAt`)
      Domain gereği yorum **yalnız davet jetonuyla** yazılıyor: tur bitip QR
      okutulmadan yazılamıyor. Alt puanlar **isteğe bağlı** — zorunlu olsaydı
      yorum sayısı düşerdi
      Kanıt: (`W-47`) işletme panelinde "Yayından kaldır" → onay diyaloğunda
      **"Bu teknenin 2 satılmış seferi ve 3 yolcusu var."** Gerçek veri,
      yıkıcı eylemden **önce**
      ⚠️ Tasarımda durum değiştirme vardı, **etki önizlemesi yoktu** — tekne
      sahibi 3 yolcusu olan tekneyi bilmeden yayından kaldırabiliyordu
      Etki okunamazsa işlem **engellenmiyor**, yalnız uyarı gösterilemiyor

- [x] **W-43** Biniş ekranı (QR okutma) · bitti: 2026-08-28
      Kanıt: **canlı, uçtan uca.** Geçersiz kod → listeye "Geçmedi · Kod
      tanınmadı" olarak düştü. Ödenmemiş rezervasyon → `400 NotPaid`.
      Ödeme yapılıp tekrar denendi → **"Biniş onaylandı · BXJ4Z2MK"**, yolcu
      adı, kişi sayısı ve **29 Ağustos 09:00** (ham damga `06:00+00:00` —
      saat çevrimi çalışıyor), ayrıca "daha önce okutulmuştu" ve "yolcu
      listesi eksik" uyarıları
      ⚠️ **İlk yazdığım tip yanlıştı.** `{succeeded, failureReason, boatName,
      passengerCount}` varsaymıştım; uç **hiçbirini** döndürmüyor. Başarı ayrı
      alanla değil **HTTP 200** ile bildiriliyor. Canlı ölçüm olmasa ekran
      boş alanlarla çalışırdı
      ⚠️ **Başarısız okutmalar da listeleniyor** — backend'in isteği. Geçersiz
      kod `200 + succeeded:false` değil **`400` + `{error,code}`** geliyor;
      sadece hata bandı gösterilseydi listeye hiç düşmezdi, oysa iskelede en
      çok bakılan şey o liste
      ⚠️ **`alreadyBoarded` uç tarafından reddedilmiyor**, bilgi olarak
      dönüyor. Gösterilmezse aynı kişi iki kez binmiş sayılır ve kimse fark etmez
      Elle giriş gizli bir seçenek değil, birinci sınıf yol: iskelede internet
      çekmeyebilir (domain kararı)

- [x] **W-50** · **W-14** · **W-44** · **W-46** · **W-48** Kimlik ve hesap ekranları
      · bitti: 2026-08-28
      Kanıt: beş ekran yazıldı, hepsi tasarımda **yoktu**:
      · **Kayıt** (`/register`) — form gönderilmiyordu. **Canlı denendi**,
        gerçek hesap açıldı: `{"role":"customer","home":"/account"}`.
        ⚠️ Tasarımda telefon alanı yoktu, uç **zorunlu** tutuyor
      · **Parola sıfırlama** (`/forgot-password`, `/reset-password`) —
        girişteki bağlantı boştu, artık bağlı. Jetonsuz gelinirse
        "Bağlantı geçersiz" + yeni bağlantı isteme yolu
        ⚠️ Uç **her durumda `204`** dönüyor (hesap sayımını önlemek için);
        başarı metni "kayıtlıysa gönderdik" diyor, "gönderildi" demiyor
      · **E-posta doğrulama** (`/verify-email`) — ilk doğrulama ve e-posta
        değişikliği onayı, `?degisiklik=1` ile ayrılıyor
      · **Hesap kapatma** (`/account/close`) — tasarımda kart vardı, akış yoktu.
        Anonimleştirilen kayıt **sayıları gösteriliyor**: kullanıcının kendi
        verisi ve tek doğrulama fırsatı
      · **İş sağlığı** (yönetim panelinde yeni modül) — **canlı doğrulandı**:
        10 gerçek iş, hepsi başarılı, Türkiye saatiyle
      Kanıt: eksik telefonla kayıt → `400 ValidationFailed
      "Phone: The Phone field is required."` — doğrulama hataları geçirgen

- [x] **W-22** · **W-23** · **W-25** · **W-26** · **W-27** Panel listelerinin bağlanması
      · bitti: 2026-08-28
      Kanıt: **işletme paneli** gerçek tohum hesabıyla — "2 tekne · 2 yayında",
      `Tohum Fiyatlı` ve `Tohum Fiyatsız` gerçek adlarıyla listeleniyor.
      **Yönetim paneli** platform personeliyle — "**10 işletme**", gerçek
      e-postalarla (`isletme-17878…@ornek.com`)
      Bağlanan uçlar: `/partner/boats` · `/partner/documents` ·
      `/partner/reviews` · `/platform/partners` · `/platform/reviews` ·
      `/support/tickets`
      Gerçek veri **tasarımın kendi şekline** çevriliyor; işaretleme hiç
      değişmedi, piksel sapması riski sıfır
      ⚠️ **Kısmi.** Uçları olmayan bölümler **mock kaldı**: işletme panelinde
      genel bakış, rezervasyon listesi, müsaitlik takvimi, finans; yönetim
      panelinde 24 modülün 16'sı. Hangisinin gerçek olduğu prop'un varlığından
      okunuyor → `W-35`, `W-36`, `W-37`
      ⚠️ Tekne kartından **"Sil" düğmesi kaldırıldı** — `DELETE
      /api/partner/boats/{id}` **yok**. Çalışmayan düğme koyulmuyor
      ⚠️ **Bu uçların hiçbirinde sayfalama yok**, çıplak dizi dönüyorlar.
      Kayıt sayısı büyüdüğünde uçlara eklenmeli

- [x] **W-28** İzin bazlı menü gizleme · bitti: 2026-08-28
      Kanıt: rol kapısı **gerçek tohum hesaplarıyla** doğrulandı — işletme
      `/owner-panel` 200 / `/admin` 307 / `/support-panel` 307; platform
      personeli `/admin` 200 / `/support-panel` 200 / `/owner-panel` 307
      İzinler gerçek: işletme **25**, platform personeli **47** izin
      Süzme mantığı ayrıca sınandı: tüm izinlerle 5 modül · yalnız
      `partner.read` ile 2 · izinsiz yalnız `genel-bakis` · **haritada olmayan
      modül gizlenmiyor** (eksik eşleme fark edilsin diye)
      ⚠️ **Ekranda farkı görünmüyor**: tohum hesapları eşlenen izinlerin
      tamamına sahip. Süzme çalışıyor ama gerçek bir "izni olmayan kullanıcı"
      ile denenmedi — dar yetkili bir rol tohumlanırsa denenmeli
      ⚠️ Menü gizlemek **yetki sınırı değil**; asıl kapı API'de. Buranın işi
      kullanıcıya çalışmayacak bir kapı göstermemek

- [x] **W-19** Rezervasyon iptali + detay sayfasının bağlanması · bitti: 2026-08-28
      Kanıt: `/account/reservations/{kod}` gerçek veriyle — `6S39V2GB`
      "Tekneye binildi", `9PZTPTXU` "İptal edildi", ikisinde de **"artık iptal
      edilemiyor"** (sunucunun `canCancel: false` kararı). Olmayan kod **404**
      İptal ucu ayrıca doğrulandı: `THP6TNAQ` → **%100 iade, 1.000,00 TL**,
      hazır Türkçe `refundNote` doğrudan basılıyor
      ⚠️ Uç **kod tek başına kabul etmiyor** — `contactEmail` veya
      `contactPhone` şart (iki faktör). Üyede hesabın e-postası kullanılıyor;
      misafirken farklı e-postayla yapılan rezervasyonda uç reddeder
      ⚠️ **`canCancel` istemcide hesaplanmıyor.** Düğmeyi gösterip uca
      reddettirmek, kullanıcıya çalışmayan bir şey sunmaktır
      ⚠️ Olumlu iptal yolu **arayüzde denenmedi** — tohum müşterisinin üç
      rezervasyonunun üçü de iptal edilemez durumda. Uç doğrudan doğrulandı
      **Yol boyunca iki ciddi hata bulundu ve düzeltildi**
      → [[web-render-sirasinda-cerez]]

- [x] **W-18** Rezervasyon akışı · bitti: 2026-08-28
      Kanıt: **tarayıcıda uçtan uca, iki kez** (vekilli ve doğrudan çağrılı).
      Teklif canlı hesaplanıyor: 2 yetişkin **₺1.800** → 4 yetişkin **₺3.600**.
      Geçersiz kupon **hata değil uyarı** — "Bu kupon kodu bulunamadı.", toplam
      değişmiyor, kullanıcı ekrandan geri gönderilmiyor (uç `200` + red kodu
      döndürüyor). Form gönderimi → rezervasyon `5GDRAYDE` → ödeme →
      `/booking/success`
      ⚠️ **Sıra dışı yanıt yarışı kapatıldı:** tarih hızlı değiştirilirse eski
      teklif sonra dönüp **yanlış fiyatı ekranda bırakabiliyordu**. Her istek
      iptal ediliyor ve yalnız kendi anahtarını yazıyor
      ⚠️ Tasarımdaki **üç adımlı sihirbaz tek ekrana indirildi** — uçlar üç
      adım gerektirmiyor, sihirbaz iki gereksiz tıklama ekliyordu
      ⚠️ Arama tekne başına **tek kiralama tipi** döndürdüğü için kullanıcı
      bugün yalnız birini seçebiliyor (domain "bir tekne birden çok tip satar"
      diyor) → `W-55`

- [x] **W-29** Tekne detay sayfası · bitti: 2026-08-28
      Kanıt: üç gerçek tekne — fiyatlı **₺900**, fiyatsız **"Fiyat için
      iletişime geçin"**, yorumlu tekne **"1 değerlendirme"**. Olmayan slug
      **404** dönüyor
      Yorumlar gerçek uçtan (`/api/boats/{slug}/reviews`, **camelCase**
      sayfalama — aramadakinden farklı), işletme yanıtı da basılıyor
      `requiresPassengerList` açıksa uyarı kutusu çıkıyor
      ⚠️ **Kaynağı olmayan on bölüm yer tutucuyla doldurulmadı.** Uydurma
      içerik göstermek, eksik bölümden kötüdür → `W-55`
      ⚠️ Tarifesi olmayan teknede iletişim **telefon**; domain sistem içi
      mesajlaşma istiyor, o ekran yazılınca değişecek (`W-20`)

- [x] **W-17** · **W-33** Arama, filtreler ve sayfalama · bitti: 2026-08-28
      Kanıt: `/boats` **7 gerçek tekne** listeliyor, mock `gulet-isil` gitti.
      Filtreler ölçüldü: bölge 7→6 · `MinPrice=600` → 3 · `MaxPrice=600` → 2 ·
      `Sort=PriceAsc` gerçekten sıralıyor (₺500, ₺500, ₺750, ₺900) ·
      uydurma sıralama değeri **süzülüyor**, uca gitmiyor (giderse 400 + RFC 7807)
      `fromPrice === null` → "Fiyat için iletişime geçin" basılıyor
      **Sunucu tarafı arama:** filtre değişimi bir gezinme, her tuşta istek yok.
      Hız sınırı (dk/60) bu yüzden tüketilmiyor
      ⚠️ **Tasarımdan üç filtre kaldırıldı** — uçta karşılığı yok: gidiş tarihi
      (aralık yok) · tur özellikleri (`amenities` boş) · rozetler (backend:
      yayındaki her tekne zaten sözleşmeli, indirim filtresi yok).
      Sessizce çalışmayan filtre, olmayandan kötüdür
      ⚠️ **İki filtre eklendi** — uçta vardı tasarımda yoktu: kişi sayısı ve
      minimum puan
      ⚠️ Filtre adları hâlâ anahtar (`bodrum`, `gunluk-tekne`) → `W-53`

- [x] **W-31** Rezervasyonlarım listesi · bitti: 2026-08-28
      Kanıt: tohum müşteri oturumuyla `/account` — **üç gerçek rezervasyon**
      (`9PZTPTXU` İptal edildi · `6S39V2GB` Tekneye binildi · `JXCQN6K4`
      Süresi doldu). Mock `RH-8xxxx` kodları sayfadan tamamen kalktı.
      Rozet renkleri doğru, detay bağlantıları `/account/reservations/{kod}`,
      1280×730'da yatay taşma yok
      Yedi durumun tamamı eşlendi — tasarımda dördü vardı, `Boarded`/`Expired`/
      `Cancelled` uçtan geliyor ve karşılıksız kalsa rozet renksiz çıkardı
      `canCancel` sunucudan okunuyor, tekrar hesaplanmıyor
      ⚠️ Başlık "tekne · marina" — uç **kiralama tipi adını döndürmüyor**,
      tasarımdaki "tekne · tur tipi" kurulamadı
      ⚠️ "Yorum yap" ve "Faturayı indir" eylemleri **konmadı**: ilki davet
      jetonu istiyor (`W-21`), ikincisinin ucu yok. Olmayan şeye düğme koyulmadı

- [x] **W-16** Sahte ödeme sayfası · bitti: 2026-08-28
      Kanıt: **ödeme akışı uçtan uca canlı API'ye karşı çalıştırıldı.**
      `quote` (1000 TL) → `reservations` (kod `THP6TNAQ`, `idempotencyKey` ile)
      → `payments/start` → backend gerçekten `/payment/mock?operation=…&code=…`
      döndürdü → tarayıcıda "Ödemeyi onayla" → düğme `aria-busy`, "Ödeme
      alınıyor…" → `/booking/success`'e yönlendi.
      Backend doğruladı: `callback` → `succeeded: true`; iptal ucu **%100 iade
      ve 1.000,00 TL** döndürdü, yani rezervasyon gerçekten **ödenmiş**
      1280×730 ve 390px'te taşma yok; uzun işlem kimliği `break-all` ile sarıyor
      ⚠️ **Yayına çıkmamalı** — `/design-system` ile aynı durumda → [[web-durum]]

- [x] **W-42** Kimlik katmanının arayüze bağlanması · bitti: 2026-08-28
      Kanıt: tohum hesabıyla tarayıcıda uçtan uca.
      · Misafirde başlık "Giriş yap/Kayıt ol"; **`GET /api/auth/me` çağrısı 0** —
        çerez yoksa istek hiç atılmıyor
      · Oturum açıkken kullanıcı çipi görünür (`TM` + "Tohum Müşteri"), giriş
        bağlantısı gizli, açılır menüde ad + e-posta
      · **"E-posta doğrulanmadı" uyarısı çıkıyor** — `emailVerified` gerçek
        alandan; "Onaylı hesap" mührü artık koşulsuz basılmıyor
      · Çıkış: "Çıkılıyor…" → başlıktan kullanıcı gitti, giriş düğmesi geri geldi
      · Hesap sayfasında mock `accountUser` yok, gerçek ad ve e-posta var
      · `document.cookie` **boş** — jetonlar JS'e kapalı
      Önceki hâli `authed`'ı **rotadan tahmin ediyordu**; çıkış yapmış kullanıcı
      `/account`'a gidince kendini giriş yapmış görürdü → [[web-kararlar]]

- [x] **W-51** Geliştirme tohum verisi · bitti: 2026-08-28 · **backend yaptı**
      Kanıt: `./araclar/tohum-veri.sh` — platform personeli, sözleşmesi onaylı
      işletme, fiyatlı **ve fiyatsız** tekne, üç durumda rezervasyon
      (`Pending`/`Paid`/`Cancelled`), açık teklifli konuşma, moderasyon
      bekleyen yorum. `Paid` olanın **binişi de yapılmış**, yani yorum karekod
      duvarını geçerek gerçek yoldan yazılmış — `W-43` o rezervasyonla denenebilir
      Kanıt: **fiyatsız tekne canlıda doğrulandı** — `fromPrice: null`, alan
      her zaman var. İki oturumun da gösteremediği tek durum buydu
      ⚠️ Betik `hesap` kovasından 6 istek harcıyor (sınır 15 dk/10) —
      **arka arkaya iki kez çalıştırılamaz**

- [x] **W-15** API istemci katmanı · bitti: 2026-08-27
      Kanıt: **canlı API'ye karşı**, hem sunucudan hem tarayıcıdan ölçüldü.
      · Vekil üzerinden arama `200`, zarf doğru, sıralama çalışıyor
      · İzinsiz yol `404` · yetkisiz uç `401 Unauthorized` (**gövdesiz yanıttan
        üretildi**) · doğrulama `400 ValidationFailed` + alan bazlı `errors`
      · **`document.cookie` boş** — vekil `httpOnly` korumasını zayıflatmadı
      · **UTC çevrimi kanıtlandı:** ham `06:00:00+00:00`–`14:00:00+00:00`,
        ekranda **09:00–17:00** — kiralama tipinin gerçek tanımı. "3 saat erken"
        hatası kesildi
      · Sadece-tarih alanı elle ayrıştırılıyor; `new Date("2027-07-15")` UTC
        gece yarısı üretiyor, gün kayması riski kapatıldı
      Dosyalar: `lib/api/{errors,format,client,browser}.ts` +
      `app/api/dc/[...path]/route.ts`

- [x] **W-04** ~~API bağlantısı, mock verinin ayıklanması~~ · **iptal: 2026-08-27**
      **Silinmedi, bölündü.** Tek satır olarak tutmak hangisinin yapılabilir
      hangisinin uç beklediğini gizliyordu. Backend görüşmesinden sonra
      **on üç işe** ayrıldı: `W-15`…`W-30` (yapılabilir) ve `W-31`…`W-40`
      (API bekliyor). Gerekçe → [[web-kararlar]] 2026-08-27
      Kanıt: bölünmeyi doğrulayan ölçüm canlı API'ye karşı yapıldı —
      69 yol / 85 işlem tarandı, her görev kaleminin arkasında ya çalışan bir
      uç ya da "uç yok" tespiti var. Yerine geçen görevler: W-14, W-15…W-30,
      W-31…W-40, W-42. Kimse `W-04`'ü arayıp boşluk bulmasın diye burada

- [x] **W-13** Çift gönderim kapısı · bitti: 2026-08-27 · `durum.md` engel 9
      Kanıt: tarayıcıda ölçüldü — **aynı karede 3 tıklama → 1 istek**.
      Kilit `useState`'te değil `ref`'te; `useState` olsaydı 3 istek giderdi
      (durum güncellemesi eşzamanlı değil) → [[web-kararlar]]
      `Button.loading`: genişlik 142px'te sabit, `aria-busy="true"`, gösterge
      var, ekran okuyucuya "İşleniyor" duyuruluyor, bitince devre dışılık kalkıyor.
      1280×730 ve 390px'te yatay taşma yok — yükleme sırasında da yok.
      Düzeltilen hata: `loadingLabel` verildiğinde etiket **iki kez** basılıyordu
      (görünür metin + canlı bölge), ekran okuyucu iki kez okurdu.
      ⚠️ **Sunucu idempotency'sinin yerini tutmaz** — ağ tekrarı ve sekme
      kopyalama bu kapıdan geçmez, engel 9 kapanmadı.

- [x] **W-11** Rota koruması — panel rotaları kimlik doğrulamayla kapatıldı
      · bitti: 2026-08-27 · `durum.md` blocker 1
      Kanıt: **canlı API'ye karşı** (localhost:5163) ölçüldü, mock değil.
      Oturumsuz 5 korunan rota → `/login?next=…` (307); 5 korumasız rota → 200.
      Rol matrisi 16/16 doğru (sahte çerezle): `customer` panellerden
      `/forbidden`'a, `owner` yalnız `/owner-panel`, `staff` üçüne de girer.
      Rol çerezi yok/uydurma → girişe döner.
      Gerçek kullanıcı kaydedilip giriş yapıldı: rol `customer` türetildi,
      3 çerez de `httpOnly` yazıldı, tarayıcıda `document.cookie` **boş**.
      Çıkış çerezleri sildi, kapı tekrar devreye girdi.
      Açık yönlendirme: `//evil.com`, `https://evil.com`, `javascript:` süzülüyor
      — hiçbir `href`/`src`/`action` içinde görünmüyor.
      `npm run build` + `npm run lint` temiz, `ƒ Proxy (Middleware)` kayıtlı.
      Not: **proxy yetki sınırı değil** — asıl kapı API'de → [[web-kararlar]]

- [x] **W-10** Geri bildirim katmanı: toast, modal, hata sayfaları, iskelet,
      boş durum, sayfalama, dosya yükleme, rezervasyon başarı ekranı, QR biniş
      belgesi, e-posta şablonları · bitti: 2026-08-26
      Kanıt: 25 rota derleniyor (öncesi 20), `npm run build` + `npm run lint`
      temiz. 1280×730'da modal 560px ortalı, perde `rgba(0,0,0,.5)`, kaydırma
      kilidi 15px telafiyle sıçramasız, ESC kapatıyor, odak çağırana dönüyor.
      Toast en fazla 3, hata `role="alert"` diğerleri `role="status"`.
      390px'te yedi yeni sayfada yatay taşma 0; modal alttan çıkan sayfaya
      dönüşüyor (üst köşe 16px, alt 0). 404 gerçekten HTTP 404 dönüyor.
      Baskı kuralları: 4 kural ayrıştı, seçiciler eşleşti, uygulandığında
      gezinme öğeleri gizlendi ve gölge kalktı.
      Bulunan ve düzeltilen hata: `rounded-circle` ölü sınıftı
      -> [[web-baglanmamis-token-tuzagi]]

- [x] **W-01** 19 sayfanın tasarıma göre piksel denetimi · bitti: 2026-08-24
      Kanıt: 16 misafir/hesap sayfasının 12'si birebir, kalanı ≤4px · yönetim
      24 modülün 19'u birebir, toplam 18px · destek 4 bölüm, toplam 12px ·
      işletme 10 bölümün 4'ü birebir, toplam 16px. Mobil 390px'te taşma yok.
      Kalan ortak +2px koyu banttaki kicker satırından, üç panelde de aynı.
- [x] **W-02** Kalan sayfaların tasarıma göre ölçülmesi · bitti: 2026-08-24
      Kanıt: W-01 ile aynı ölçüm; 1280×730'da tasarımla yan yana
- [x] **W-07** Front-end çalışmasının commit'lenmesi · bitti: 2026-08-23
      Kanıt: `76ac110` tasarımın 19 ekranı · `9009db3` kopan detaylar · `2b1dd35`
      işletme paneli hizalama · `d42b985` mobil kırılımlar · `2777132` İngilizce
      rotalar. Beşi de `origin/main`'de, AI atfı yok, yazar Mert.
- [x] **W-09** Rota klasörlerinin İngilizceye çevrilmesi · bitti: 2026-08-24
      Kanıt: 17 klasör `git mv` ile taşındı, 20 rota derleniyor; ana sayfada 26,
      hesap sayfasında 19 iç bağlantı 200 döndü, eski Türkçe yollar 404
      -> [[web-kararlar]]
- [x] **W-05** Mobil kırılımların doğrulanması · bitti: 2026-08-23
      Kanıt: 19 rota 390px'te tarandı, yatay taşma yok; 834px'te iki kart.
      Ölçüm Playwright ile — `chrome-devtools` 390'a inemiyor -> [[web-araclar]]
- [x] **W-08** Kopan detay ekranlarının geri bağlanması · bitti: 2026-08-23
      Kanıt: yönetimde 23, işletmede 3 ekran; 21 yönetim modülünde tek tek açılıp doğrulandı
- [x] **W-00** Next.js 16 iskeleti, Tailwind v4, tasarım sistemi katmanı · bitti: 2026-08-21
      Kanıt: `npm run build` başarılı

İlgili: [[web-desenler]] · [[web-kararlar]] · [[web-mimari]] · [[durum]] · [[web-notlar]]
