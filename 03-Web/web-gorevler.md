---
rol: gorev
kapsam: web
guncelleme: 2026-09-05
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







- [ ] **W-40** Yolcu listesi — **uyarı tamam**, veri toplama Mert'te
      Uyarı rezervasyon akışında, ödeme formundan önce; kaynağı **teklif**
      olduğu için hiçbir koşulda kaybolmuyor, süre ("kalkıştan en geç 24
      saat önce") varsa ekleniyor (`8daecfc`).
      Kalan iş yolcu **verisini toplamak**: form ucu yok ve KVKK dayanağı
      Mert'te. ⚠️ Backend'in açtığı ek karar: düzeltme **geriye dönük
      değil** — bayrak rezervasyona donduruluyor, geliştirmede 10
      rezervasyon hâlâ yanlış damgalı. Mevcut satırlar düzeltilsin mi,
      Mert'in kararı
- [ ] **W-06** `brand.ts` kurumsal verileri · **Mert'te** (G-10)

### 🟦 E — Altyapı

## 🟡 Yapılıyor

## 🟢 Tamamlandı

- [x] **W-88** Sözleşme onay ekranı iki sütuna alındı · 2026-09-05
      🔴 **Mert testte gördü:** *"etrafta çok fazla boşluk var, burası
      çok boş gözüküyor."* Ölçüm (1440px, `demo-gokova`): sayfa
      **2114px**, metin kutusu **1038×420px** ve içinde **tek cümle**;
      altında ~390px çukur. Dört kart alt alta yığılıydı ve ekranın
      başlık şeridi hiç basılmıyordu.
      Solda metin, sağda özet + onay + ret. İçerik alanı 1780px'ten
      **970px**'e indi, başlık şeridi eklendi.
      ⚠️ **Kutu küçültülmedi, esnetildi.** Çukurun sebebi kutunun büyük
      olması değil, yüksekliğinin içeriğe bakmamasıydı; küçültmek demoyu
      düzeltir **üretimi bozardı** — gerçek sözleşme uzun. Şimdi uzun
      metin sayfayı uzatmak yerine kutunun içinde kayıyor.
      🔴 **İlk denemede boşluğu taşıdım, kapatmadım:** iki sütuna
      geçince sol kart sağdan kısa kaldı ve **altında 287px** yeni çukur
      açıldı. Ölçüm yakaladı; satır esnetildi.
      Kanıt: canlı, iki hesap — 1440 · 1280 · 390px'te yatay taşma **0**;
      iki sütunun yükseklik farkı **üç durumda da 0** (ilk kez gören ·
      reddetmiş, geçmiş + gerekçe basılı · ret formu açık). Mobilde tek
      sütun, yapışkanlık kapalı. `build`, `lint`, `tsc` temiz. `22a749e`

- [x] **W-86** Ret gerekçesi platform panelinde · 2026-09-05
      `W-87` reddi **görünür** yapmıştı, bu görev **okunur** yaptı.
      Backend `GET /api/platform/partners/{id}/contracts` yanıtına
      `rejectedAt` ve `rejectionReason` ekledi (alanlar veritabanında
      duruyordu, platform izdüşümü seçmiyordu). Sözleşme listesi ikisini
      de basıyor: ret tarihi satır başlığında, gerekçe altında ayrı kutuda.
      Ret rozeti **griden çıkarıldı** — "süresi doldu" ve "yenisiyle
      değişti" kendiliğinden olan şeyler, ret ise işletmenin cevabı ve
      platformdan eylem bekliyor. Rozetin rengi burada durum değil,
      **sıradaki iş**.
      ⚠️ Sebep tekrar edecek cinsten: iki uç **ayrı izdüşüm** kullanıyor
      (`PartnerContractItem` ↔ `ContractListItem`). Bir uca alan eklemek
      diğerini etkilemiyor ve **tek uca bakan ölçüm eksiği göstermiyor.**
      Üretilen tipler tazelendi: 119 yol · 149 işlem. Belge artık 148
      işlemde **yanıt şeması** taşıyor — daha önce hiçbirinde yoktu, yani
      elle yazılan yanıt tipleri sessizce yalan söyleyebiliyordu.
      Kanıt: canlı, gerçek veri, iki yönlü. **Olumlu** — Mert'in başvurusu
      (`my_mert07@hotmail.com`) satırda "Sözleşme reddedildi", modalda
      `Ret: 5 Eyl 05:13` ve gerekçe kutusu. **Olumsuz** — Kekova Mavi Tur'da
      iki sözleşme var (%15 gönderildi, %25 reddedildi) ve gerekçe kutusu
      **yalnız 1 kez** basılıyor; satır durumu "Sözleşme gönderildi",
      çünkü ret **cevaplanmış**. Sayfa taşması 0; `tsc`, `lint`, `build`
      temiz. `5189ce6`

- [x] **W-87** Yönetim tablosu sığdırıldı, sözleşme reddi görünür oldu · 2026-09-05
      🔴 **Mert testte iki şey birden buldu.** Birincisi yerleşim: yat
      işletmeleri tablosu kabından **510px taşıyordu** ve kaydırma çubuğu
      tablonun altında olduğu için 31 satırlık listede yana kaydırmak
      ancak sayfanın en dibine inerek mümkündü. *"Tam sığmıyor ekrana,
      kaydırmak için taa en aşağıya inip kaydırmam gerekiyor."*
      İkincisi daha ağır: başvuru yaptı, sözleşme gönderdi, işletme
      hesabından reddetti, platforma döndü — **reddin hiçbir izi yoktu**.
      Sütunlar oransal yapıldı (`w` pay, `min` taban) ve yönetim paneli
      1440px kaba alındı; sapma yalnız bu panelde, misafir sayfaları
      1140px kaldı. İşlem düğmeleri iki sütunlu ızgaraya alındı.
      Durum rozeti artık `contractStatus`'ü de okuyor — uç bu alanı
      **zaten döndürüyordu**, ekran hiç okumamıştı.
      ⚠️ Ret **gerekçesi** hâlâ görünmüyor, platform ucu döndürmüyor →
      `W-86`. Yani bu görev reddi *görünür* yaptı, *okunur* yapmadı.
      Kanıt: canlı, gerçek veri, Playwright ölçümü — 1440'ta ve 1280'de
      yatay taşma **0**, 1180'de tablo kendi içinde 77px kaydırıyor ve
      sayfa taşmıyor, 390'da sayfa taşması 0; destek ve yorum tabloları
      da 0'a düştü. Beş düğmenin hepsi **99px**, iki hizalı sütun, aynı
      satırdakiler eşit yükseklikte. Mert'in başvurusu
      (`my_mert07@hotmail.com`) **"Sözleşme reddedildi"** basıyor ve
      "Sözleşme gönder" düğmesi açık; 31 satırın dağılımı Aktif 19 ·
      Sözleşme gönderildi 9 · Başvuru alındı 2 · Sözleşme reddedildi 1.
      `npm run build`, `lint` ve `tsc` temiz. `982ee73`

- [x] **W-85** Sözleşme okuma ve onay · 2026-09-05
      🔴 **Mert testte buldu ve katılım akışının kopuk halkasıydı:**
      *"ben sözleşmeyi gönderdim de gönderdiğim kişi nasıl okuyup
      onaylayacak?"*
      Ölçtüm: platform sözleşme gönderiyor, işletme giriş yapıyor ve
      panelin **her bölümü "okunamadı"** yazıyor — bir sayfada **7 kez**.
      Sözleşme kelimesi **0 kez**. `partner/contracts` **`404`**,
      `partner/profile` **`403`**. Yani **hiçbir yeni işletme sisteme
      giremiyordu** ve ekran bunu "sistem bozuk" diye gösteriyordu.
      🔴 **Bu, Mert'in daha önce bildirdiği 403'ü de açıkladı.** O zaman
      üretemeyip *"olmayan bir kusur arıyor olabilirim"* demiştim —
      **ön koşulu yanlış kurmuşum**: demo işletmesiyle test etmiştim, o
      `Active`. Mert `ContractSent` bir hesapla test etmiş.
      Backend iki ucu yazdı (`10097c0`), ekran bağlandı:
      · Aktif olmayan işletmeye **panel hiç basılmıyor**, yerine sözleşme
        ekranı geliyor; sözleşme henüz gönderilmemişse **sebebi yazıyla**
      · Metin `sandbox=""` `<iframe srcDoc>` içinde —
        `dangerouslySetInnerHTML` yok, gövde temizlenmiyor (`W-64` yolu)
      · **Komisyon oranı ve periyot metnin dışında da** basılıyor:
        imzalanan sayı bunlar, metni okumadan onaylayan bile görmeli
      · Onay kutusu ekranda ama **isteğe alan olarak gitmiyor** —
        sunucunun doğrulayamayacağı boole güvence değil süs olur
      Kanıt: canlı, uçtan uca — `ContractSent` hesapla panel yerine
      sözleşme ekranı geldi (`Test 1788568945 Ltd`, `%15`, `14 gün`,
      metin iframe'de); **yanlış parola reddedildi**, doğru parolayla
      onaylandı ve **panel açıldı** (`TOPLAM HAKEDİŞ` göründü).
      Taşma 0, `npm run build` temiz. `4b475f0`
      **2026-09-05 devamı — reddetme eklendi** (Mert istedi, `S-36`).
      **Reddedilen sözleşmedir, işletme değil**: başvuru kapanmıyor,
      platform gerekçeyi okuyup düzeltilmiş sözleşme gönderebiliyor.
      ⚠️ **Ret parola İSTEMİYOR, kabul istiyor.** Asimetri bilinçli:
      kabul işletmeyi komisyon oranına bağlıyor ve geri alınamıyor; ret
      bağlamıyor ve geri alınabiliyor. Geri alınabilir bir eylemin önüne
      geri alınamaz olanın sürtünmesini koymak koruma değil engel olurdu.
      Önceki sözleşmeler **gizlenmiyor** — `Rejected` ile `Cancelled`
      ayrı anlatılıyor: reddi işletme yapar, iptali platform.
      🔴 **Ölçerken kendi eksiğimi buldum:** reddettikten sonra geçmiş
      ekrandan **kayboluyordu** ve işletme az önce ne yaptığını göremiyordu
      — reddin gidip gitmediğini bilemezdi. Düzeltildi.
      Kanıt: pazarlık döngüsü canlı ölçüldü — `%25` sözleşme geldi, boş
      gerekçede düğme **kapalı**, gerekçeyle reddedildi ve uçta
      `Rejected %25 · "Komisyon oranı yüksek geldi, %15 olabilir mi?"`
      göründü; platform `%15`'lik yeni sözleşme gönderdi ve ekranda
      **ikisi birlikte** basıldı: üstte `%15` onay bekliyor, altta
      *"Sen reddettin · Gerekçen: …"*. `7334f3b`

- [x] **W-84** Şehir alanı il listesine çevrildi · 2026-09-05
      Mert testte istedi: *"`/add-boat` kısmında şehir yerine il ilçe
      olmalı."* İlçe **isteğe bağlı** olacak (Mert, 2026-09-05).
      **İl açılır liste oldu** (81 il, plaka sırasında). Serbest metinde
      aynı il için `Muğla`, `MUĞLA`, `Mugla`, `muğla` birikiyor ve şehre
      göre süzme hiç çalışmıyor.
      🔴 **Sessiz bir veri kaybı önlendi.** Ayarlar ekranında kayıtlı
      değer listede yoksa **listeye eklenip seçili kalıyor**. Demo
      işletmesinin şehri `Bodrum` yazıyor — o bir **ilçe**, il değil.
      Yedek olmasaydı açılır liste hiçbirini seçili gösteremez,
      kullanıcı başka bir alanı düzeltip kaydettiğinde şehrini farkında
      olmadan değiştirmiş olurdu.
      ⚠️ **İLÇE KUTUSU BİLEREK KONMADI.** Uçta `district` alanı yok:
      ölçtüm, gövdeye eklenince uç **`201` dönüyor ve değeri sessizce
      yutuyor**. Kutuyu koymak kullanıcıdan bilgi alıp çöpe atmak
      olurdu. Backend'den alan istendi; gelince bağlanacak.
      ⚠️ **İlçe listesi de gömülmedi.** ~970 ilçelik doğrulanmamış bir
      liste serbest metinden **daha kötü** olur: kullanıcı kendi
      ilçesini bulamayınca yakın olanı seçer ve yanlış veri "seçilmiş"
      göründüğü için kimse şüphelenmez.
      Kanıt: canlı — `/add-boat`'ta alan `İl`, **82 seçenek**
      (`Seçiniz` + 81), varsayılan boş, `district` kutusu **yok**;
      ayarlar ekranında kayıtlı `Mugla` **83. seçenek olarak eklenip
      seçili** kaldı. Liste sayıldı: 81 il, tekrar 0, plaka sırası doğru
      (34 İstanbul · 48 Muğla · 81 Düzce). Taşma 0, derleme temiz.
      **2026-09-05 devamı — ilçe eklendi.** Backend `district` alanını
      yazdı (isteğe bağlı, 120 karakter); başvuru formunda ve işletme
      ayarlarında serbest metin olarak duruyor.
      ⚠️ Boş bırakılan isteğe bağlı alan **`null` gidiyor, `""` değil**:
      boş dize "ilçesi yok" ile "yazmadı" arasındaki farkı kaybettirirdi
      ve veritabanında boş dize ile `NULL` ayrı şeyler.
      Kanıt: `/add-boat`'ta `İlçe` alanı `required=false`, ipucu "İsteğe
      bağlı"; ayarlarda `Yalıkavak` yazılıp kaydedildi ve **uçtan geri
      okundu**; ilçesiz başvuru uçta `200`. Ölçüm sonrası demo verisi
      eski hâline döndürüldü. `ff70bb0` · `5680ab0`

- [x] **W-83** Kullanıcı menüsü role göre süzülüyor · 2026-09-05
      🔴 **Mert testte buldu:** müşteri hesabında (Ayşe) `Yönetim Paneli`,
      `İşletme Panelim` ve `Destek Paneli` bağlantılarının **üçü birden**
      görünüyordu. Menü listesi düz bir dizi olarak basılıyordu, rol
      süzgeci hiç yoktu.
      **Kapı doğru çalışıyordu** — tıklayan `403` alıyordu. Yani bu bir
      yetki açığı değil, **yanlış vaat**: kullanıcıya giremeyeceği bir
      yere bağlantı gösteriliyordu.
      Süzgecin kaynağı `GUARDED` listesi; **ikinci bir rol tablosu
      yazılmadı**. İki liste ayrı tutulsaydı biri değiştiğinde diğeri
      sessizce ayrışır ve menü yine girilemeyen bir panele bağlantı
      gösterirdi.
      Kanıt: canlı, **üç rolde de** menü açılarak ölçüldü —
      müşteri **hiçbiri**, işletme yalnız `/owner-panel`, platform
      `/admin` + `/support-panel`. Olumlu dal ayrıca ölçüldü: yalnız
      "müşteri görmüyor" ölçülseydi, **hepsini gizleyen** bozuk bir
      süzgeç de geçerdi.
      ⚠️ Ölçüm yolunda iki kez yanıldım: sunucu HTML'inde bağlantıları
      aradım, oysa menü paneli **yalnız açılınca** basılıyor — üç rol de
      "görmüyor" çıktı ve neredeyse "süzgeç çalışıyor" diyecektim.
      `15883b6`

- [x] **W-82** Elle yazılan yanıt tipleri şemaya karşı denetlendi · 2026-09-05
      Backend `A-07` ile yanıt şemalarını yazdı: gövde şeması taşıyan
      operasyon **0/146 → 145/146**, 181 bileşen şeması. Öncesinde her uç
      şemasız bir `200` bildiriyordu — belge **dolu görünüp hiçbir şey
      söylemiyordu**, elle yazılan tiplerin karşılaştırılacağı bir şey
      yoktu.
      **Sonuç: 15 tipin 15'i birebir eşleşti, uydurma alan 0.**
      Denetlenenler: blog satırı ve tek kaydı, blog kategorisi,
      moderasyon satırı, favori kartı, bildirim tercihi, kampanya,
      kuponlarım, işletme kuponu, arama satırı, tekne detayı, işletme
      rezervasyonu, işletme profili, biniş bileti.
      **Bu oturumda üç tip yanlış çıkmıştı** — blog liste satırı
      (`translations` yok, düz `title`), iade oranı (önizleme değil
      kayıt), favori kartı (`isAvailable` atlanabilirdi — atlanmadı.)
      Üçünü de **tarayıcı** yakaladı, `tsc` sustu; artık şema var.
      ⚠️ Denetim betiğinin kendisi iki kez yanlış alarm verdi: sayfalama
      zarfını satır sanıp `/api/blog` ve `/api/search` için "10 uydurma
      alan" bildirdi. Zarfın içine inince ikisi de temiz çıktı —
      **ölçüm aracının kendisi de ölçülmeli**.
      Kanıt: `npm run tip-uret` → 116 yol · 146 işlem · yanıt şeması
      145/146; karşılaştırma çıktısı `uydurma alan tasiyan tip: 0`.
      `tsc` 0 hata, `eslint` temiz. `89041b1`

- [x] **W-81** Donanım süzgeci ve tekne kuralları canlı · 2026-09-05
      **Yeni kod yazılmadı** — ikisi de `W-53`/`W-54`'te yazılmıştı ve
      panoda *"Tur özellikleri filtresi geri KONMADI"* diye açık uyarı
      duruyordu. Eksik olan **veriydi**: katalogda 9 donanım / 3 kural
      vardı ama yayındaki sekiz teknenin **hiçbirinde atama yoktu**.
      Backend `S-23`'ü kapatırken bunu buldu (kendi notu da bayatmış:
      "uç yok" diyordu, uç zaten vardı) ve demo verisine kalıcı atama
      koydu.
      Kanıt: canlı, **süzgeç gerçekten süzüyor** —
      `/boats` süzgeçsiz **8 kart** → `klima` **6** → `klima+şnorkel`
      **3**. Tekne detayında `Teknede neler var` ve `Kurallar` bölümleri
      gerçek adlarla basılıyor (`Klima`, `Şnorkel takımı`,
      `Evcil hayvan`, `Sigara`).
      ⚠️ **Üçüncü kez `revalidate: 60` tuzağına yaklaşıldı ve üçüncü kez
      tekrar ölçülerek geçildi.** İlk ölçümde iki bölüm de boştu; kod
      doğruydu, sayfa 60 sn önbellekliydi. Hata ilan edilmedi, pencere
      beklenip yeniden ölçüldü → [[web-olcum-yanlis-pozitifleri]]

- [x] **W-80** İşletme paneli — kampanyalarım · 2026-09-05
      Mert **(a)** dedi: işletme kendi kampanyasını kendisi açabilir.
      Backend uçları yazdı (`A-89`), ekran bağlandı.
      **Üç alan formda yok ve olmamalı**: `fundedBy`, `partnerId`,
      `isPubliclyListed`. Üçü de sunucuda sabit; forma konsaydı işletme
      kampanyasının bedelini **platforma yazabilir** ya da kuponunu
      sitenin genel vitrinine sokabilirdi. Sınır sunucuda, ekran onu
      tekrar hesaplamıyor — **anlatıyor**.
      **Bedelin nereden çıktığı yazıyla duruyor:** *"Bu indirimin bedeli
      senin hakedişinden düşülür."* Görmeden %30 kupon açan işletme
      parayı sonradan öğrenirdi.
      Kullanım sayısı **işletmeye** gösteriliyor, müşteriye
      gösterilmiyor: kendi kampanyasının kaç kez kullanıldığını bilmeli,
      ama müşteriye göstermek platformun iç sayacını dışarı vermek olurdu.
      🔴 **İki tarih tuzağı, ikisi de ölçümle bulundu:**
      · Uç **sadece-tarih** (`"2026-09-05"`) ve **UTC olmayan offset**
        (`+03:00`) gövdelerini **`500`** ile reddediyor — `400` değil.
        Yalnız `Z` kabul ediliyor. Gün sınırı bu yüzden Türkiye gününe
        göre kurulup UTC'ye çevriliyor; doğrudan `T00:00:00Z`
        gönderilseydi kampanya **başlangıç gününün ilk üç saatinde
        çalışmazdı**
      · Varsayılan tarih `toISOString().slice(0,10)` ile alınıyordu; o
        **UTC gününü** verir ve Türkiye'de gece yarısı–03:00 arasında
        "dün" yazardı. Yerel gün elle kuruluyor
      Kanıt: canlı, panelde — menüden `Kampanyalarım`, mevcut kupon
      `MAVI10 · Açık · %10 · 0 / 25 kullanım`; formdan `OLCUM40`
      oluşturuldu ve **listede belirdi** (`%40 · tüm teknelerin`);
      kod yazarken büyük harfe çevriliyor (`olcum40` → `OLCUM40`);
      kapatma `204`. Ölçüm kuponları sonradan kapatıldı.
      Taşma 0, `npm run build` temiz. `94633f5`

- [x] **W-39** Kuponlar — üç tür bağlandı · 2026-09-05
      Mert'in 2026-09-04 kararı: *"kullandığı kuponlar ve bana özel
      kuponlar ve genel kuponlar olsun."* Backend üç türü ayrıştırdı,
      ekran **ayrı bölümler** hâlinde basıyor.
      **Neden tek liste değil:** tek listede toplansaydı müşteri kampanya
      kuponunu "bana özel" sanıp paylaşmaktan çekinir, ya da tersine
      kişisel kuponunu paylaşır ve arkadaşında çalışmayınca ikisi de
      sebebini bilemezdi.
      ⚠️ "Sana özel" rozeti yalnız `isAssignedToMe` doğru olanlarda —
      liste iki kaynağı birleştiriyor ve geçmişte kullanılmış bir
      **kampanya** kuponu da orada görünüyor.
      🔴 **Sessiz bir kırılma önlendi:** fiyat sorgusu `dogrudan: true`
      ile vekili atlıyordu, yani **jeton eklenmiyordu**. Uç kimliği
      kullanmaya başladığı için giriş yapmış kullanıcının kendi kuponu
      sessizce reddedilecekti — müşteri "kuponum çalışmıyor" der, hiçbir
      hata görünmezdi.
      `dogrudan`ın gerekçesi hız sınırıydı: vekilden geçen istekte backend
      herkesi tek IP sayıyordu. **Vekil artık istemcinin gerçek IP'sini
      iletiyor** (`X-Forwarded-For`), o gerekçe kalktı. Backend başlığa
      yalnız `KnownProxies` listesindeki vekilden gelirse güveniyor;
      liste boşken başlık yok sayılıyor, yani yanlış yapılandırmada
      **açık üretmiyor**.
      Kanıt: canlı, **iki dal da** ölçüldü —
      · Ayşe hesabıyla `AYSEYE20` → `Tur ₺2.900 · İndirim −₺580 ·
        Toplam ₺2.320`, *"Kupon uygulandı"*
      · **Can hesabıyla aynı kupon** → indirim **yok**, toplam ₺2.900,
        *"Bu kupon size tanımlı değil…"* — yalnız olumlu dal ölçülseydi,
        her kuponu herkese uygulayan bozuk bir yol da geçerdi
      · Hesap sayfasında üç bölüm: `AYSEYE20` (Sana özel rozetiyle),
        "Henüz kupon kullanmadın", `YAZ2026` kampanyası
      · Taşma 0, `npm run build` temiz
      ⚠️ Vekil izin listesine `coupons` eklendi — **üçüncü kez** (`blog`,
      `favorites`). Yeni uç bağlarken ilk bakılacak yer orası
      → [[web-mimari]]
      `2f709c2`

- [x] **W-79** Blog kısa adı başlıktan üretiliyor · 2026-09-05
      Backend tekne slug'ındaki Türkçe `İ` kusurunu düzeltirken sordu:
      blog kısa adını sunucu mu çevirsin, reddetmeye devam mı etsin.
      **Karar: sunucu reddetmeye devam etsin, çeviriyi istemci görünür
      şekilde yapsın.** Sunucu sessizce değiştirseydi kaydedilen adres
      kullanıcının yazdığından farklı olur ve bunu ancak yayınlandıktan
      sonra fark ederdi.
      ⚠️ `toLowerCase()` tek başına yetmiyor: noktalı `İ` (U+0130)
      küçültmeden geçiyor ve `NFD` ayrıştırması onu **büyük `I`**'ya
      çeviriyor — backend'de `akdeniz-Incisi` tam bu yüzden doğmuştu.
      Türkçe harfler önce çevriliyor.
      **Üretim yalnız yeni yazıda ve kullanıcı alana dokunmadıkça**
      çalışıyor: kayıtlı bir yazının adresini başlık değişince
      değiştirmek yıkıcı olurdu, paylaşılmış adres sessizce `404`'e
      dönerdi.
      Kanıt: canlı, panelde üç davranış —
      · `"Gökova koylarında İZMİR çıkışlı üç gün"` →
        `gokova-koylarinda-izmir-cikisli-uc-gun`, ipucu *"başlıktan
        üretildi, değiştirebilirsin"*
      · Elle `"Şile & Ağva"` yazıldı → `sile-agva` (elle giriş de
        normalleştiriliyor, kullanıcı `400` görmüyor)
      · Sonra başlık değiştirildi → kısa ad **değişmedi**
      `80f2fa9`

- [x] **W-66** Biniş karekodu · 2026-09-05
      `S-25` cevaplandı — Mert **(b)** dedi: asıl jetona dokunulmuyor,
      belge açıldığında **ayrı ve kısa ömürlü** bir bilet üretiliyor.
      Backend ucu yazdı, ekran bağlandı.
      **Uç görsel değil METİN döndürüyor** (`token`) ve bu doğru ayrım:
      karekod okunamadığında (ıslak ekran, güneş, çizik baskı) kaptanın
      elle girebileceği tek şey metnin kendisi. Görsel dönseydi o metin
      kaybolurdu. Çizim istemcide (`qrcode`, yalnız bu ekranda yükleniyor).
      ⚠️ **Yeni bilet öncekini iptal ediyor** ve bunu ekranda **yazıyla**
      söylüyorum: *"Belgeyi en son açtığın cihazdaki karekod geçerlidir."*
      Söylenmeseydi belgeyi iki cihazda açan müşterinin kodu **iskelede**
      çalışmaz ve sebebi görünmezdi.
      🔴 **Bunu ölçüm sırasında istemeden kendim yaşadım:** karekodu
      karşılaştırmak için ikinci bir bilet istedim ve ekrandakini
      geçersiz kıldım. Uyarı metni bu yüzden var.
      Ömür kalkıştan **12 saat sonrası**, tur bitişi değil — bitişte ölen
      bilet geç kalkan turda kaptanın elinde ölürdü.
      Kanıt: canlı, uçtan uca —
      · Tuval **176×176**, **14.025 koyu piksel** (ne boş ne dolu, gerçek
        desen)
      · Aynı bilet `boarding/scan`'de **`200`** → `S732EGRV`,
        `Ayşe Yılmaz`, 2 yetişkin; **geçersiz jeton `400`**
      · Ödenmemiş rezervasyonda uç `400`; ekran bileti **hiç istemiyor**,
        *"ödeme tamamlandığında oluşur"* yazıyor
      · Hata dalında karekod yerine rezervasyon kodu basılıyor — elle
        okutma çalıştığı için müşteri belgesiz kalmıyor
      · Taşma 0, `npm run build` temiz
      ⚠️ **Kanıtlamadığım şey:** karekodun görüntüsünü çözüp içindeki
      metni okumadım (çözücü kütüphane eklemek istemedim). Kanıtlanan,
      biletin okutmada kabul edilmesi ve tuvalin gerçek desen taşıması.
      `d26a19f`

- [x] **W-78** İptal onayında iade tutarı, onaydan önce · 2026-09-05
      Onay penceresi *"iptal onaylandığında tutar sana bildirilir"*
      diyordu: müşteri **geri alınamaz** bir işlemi sonucunu görmeden
      onaylıyordu. `S-12` politikasıyla bunun somut bedeli var — kalkışa
      24 saatten az kala **iade sıfır**.
      🔴 **Kendi varsayımım yanlış çıktı ve ölçerek buldum:**
      `cancellationRefundRate` bir önizleme değil **kayıt**, yalnız iptal
      edilmiş rezervasyonda dolu. Backend ayrı alan açtı
      (`refundPreviewRate`/`refundPreviewTry`); aynı ada iki anlam
      yüklenmedi.
      Kanıt: canlı, iki dilim ekranda ölçüldü —
      %50 → *"ödemenin %50 kadarı, yani ₺1.850 iade edilecek"*;
      %0 → *"kalkışa kalan süre nedeniyle iade yapılmayacak"* (ayrı
      cümle). %100 dilimi ölçülemedi: o rezervasyonu biniş sınamasında
      kendim tükettim, backend'den düzeltmesi istendi.
      Oran okunamazsa sayı **uydurulmuyor**, genel cümleye düşülüyor.
      `dd3544e` · `d26a19f`

- [x] **W-76** Blog gövdesinde zengin metin (CKEditor) · 2026-09-04
      `S-31` cevaplandı; Mert *"b olabilir yada CKEditör de olabilir"*
      dedi, seçim teknik tarafa kaldı. **CKEditor seçildi** — yazarlar
      kaptan ve işletmeci, Markdown sözdizimi gerçek bir engel ve blogun
      amacı yazmaya teşvik etmek → [[domain-gereksinimler]] 2026-09-04
      🔒 **Sıra tersine çevrilemezdi ve çevrilmedi:** önce backend yazma
      yolunda izin listeli temizleyiciyi kurdu, sonra editör açıldı.
      Temizlemeyi **bağımsız ölçtüm**, raporu doğru kabul etmedim:
      `<script>`, `onclick`, `javascript:` bağlantısı, `<iframe>`,
      `<style>` ve `<h1>` **veritabanına yazılmadan** düşüyor; başlık ve
      özet düz metne iniyor.
      **Araç çubuğu sunucunun izin listesiyle birebir.** Sunucunun
      düşürdüğü bir düğme editörde bulunsaydı yazar onu kullanır,
      kaydeder ve biçimlendirmesinin **sessizce kaybolduğunu** görürdü.
      `h1` yok (sayfa başlığı zaten `h1`), renk/hizalama/yazı tipi yok
      (`style` ve `class` sunucuda düşüyor).
      🔴 **Onuncu "build temiz ≠ görünüm doğru" örneği:**
      `ckeditor5.css` import edilmeden editör **çalışıyor ama biçimsiz** —
      araç çubuğu saydam, kenarlık yok. `tsc`, `eslint` ve `npm run build`
      üçü de temiz geçti; yalnız tarayıcıda görüldü
      → [[web-desenler]]
      Kanıt: canlı, uçtan uca —
      · XSS yükü gönderildi, **saklanan hâl** okundu: `<h2>` ve
        `<strong>` kaldı, betik/olay/iframe/style düştü
      · Yazı sayfasında ölçülen stil: `h2` 35px/700, `blockquote` 24px +
        3px sol kenar, `ul` madde işaretli, bağlantı altı çizili,
        `script` **0 adet**
      · Panelde editör yüklendi, araç çubuğunda **12 düğme** ve hiçbiri
        izin listesi dışında değil; zengin gövde **birebir** açıldı
        (`h2`, `strong`, `li`, `blockquote`, `a`)
      · Kaydetme editör yolundan da çalıştı: yazı `Published` →
        `UnderReview`'a düştü ve **gövde birebir korundu** — editör hiçbir
        etiketi düşürmedi
      · Araç çubuğu arka planı `rgb(255,255,255)`, editör yüksekliği
        320px, taşma **0**, `npm run build` temiz
      ⚠️ `javascript:` bağlantısında sunucu `href`'i düşürüyor ama `<a>`
      kalıyor; href'siz bağlantı **düz metin gibi** basılıyor, altı
      çizili görünüp tıklanabilir sanılmasın diye. Ölçülmüş davranış.
      ⚠️ Editör yüklenemezse alan `textarea`'ya düşüyor — boş kutu
      bırakmak yazıyı kaydedilemez hâle getirirdi.
      `60dd064`

- [x] **W-77** `/design-system` rotaları yayında kapatıldı · 2026-09-04
      Bileşen vitrini derlemede statik rota olarak üretiliyordu, yani
      canlıda herkese açık olurdu; e-posta şablonları da orada.
      **Silinmedi, kapatıldı**: geliştirmede hâlâ gerekiyor ve silinen bir
      vitrin ilk gerekli olduğunda yeniden yazılırdı.
      Kanıt: geliştirmede `200`; `next start` ile **üretim derlemesi
      ayağa kaldırıldı** ve iki rota da **404** döndü, kontrol olarak
      `/blog` `200`. `e794690`

- [x] **W-75** Fiyat kutusunda KDV oranı · 2026-09-04
      `S-20` ile oran rezervasyona donduruldu ve `pricing/quote` yanıtına
      `vatRate` eklendi. Ekran oranı **uçtan** yazıyor, koda gömmüyor:
      oran değiştiği gün ekran kendiliğinden doğru olsun.
      ⚠️ **Vergi tutarı basılmıyor** — uç da bilerek döndürmüyor. Tutar
      toplamdan türetilebiliyor; ikisini birden taşımak yuvarlamada
      ayrışmaya açık kapı bırakır ve aynı ekranda birbirini tutmayan iki
      sayı görünürdü.
      Kanıt: canlı — `/booking` özetinde `Toplam ₺1.000` altında
      **"Tüm fiyatlara %20 KDV dahildir."**; uç ölçümünde `vatRate: 20`.
      Taşma 0, konsol temiz. `tsc` 0 hata, `eslint` temiz

- [x] **W-39b** Favoriler ve bildirim tercihleri · 2026-09-04
      Hesap sayfasının iki sekmesi "bağlı değil" yazıyordu; backend
      uçları yazdı (`A-77`, `A-78`), ikisi de gerçek veriye bağlandı.
      🔴 **Favori düğmesi hiçbir yerde yoktu** — ekran doldurulamıyordu,
      yani uç gelse bile özellik ölü kalırdı. Tekne detayına eklendi.
      ⚠️ **Vekilin izin listesinde `favorites` öneki yoktu** ve bunu
      yalnız tarayıcı yakaladı: düğme belirsizlikte kendini gizlediği
      için özellik **sessizce ölmüştü**, `tsc` ve `eslint` ikisi de temiz
      geçiyordu. Aynı tuzak `blog` önekinde de vardı — vekil izin listesi
      artık yeni uç bağlarken kontrol edilecek → [[web-desenler]]
      **Bildirim tercihi eskiden paneldeki en sinsi mock'tu**: anahtarlar
      açılıp kapanıyordu ama hiçbir yere kaydedilmiyordu, kapatılan
      bildirim yine geliyordu.
      Kanıt: canlı, müşteri hesabıyla —
      · Tekne detayında düğme `☆ Favorilere ekle` → tıklandı →
        `★ Favorilerimde`, `aria-pressed` `false`→`true`
      · Hesap → Favoriler: **2 tekne**, gerçek adlar ve marina, tip
        rozetleri gerçek (`GULET` / `A04-GULET`)
      · Bildirimlerde SMS kapatıldı → e-posta anahtarı **kilitlendi** ve
        sebebi yazdı: *"Bu son açık kanalın — kapatılamaz"*
      · Kaydedildi → **uçtan okundu**: `emailEnabled true, smsEnabled
        false, reviewInvitationsEnabled false`. Yani tercih yalnız
        ekranda değil, gerçekten yazıldı — eski mock'un yapamadığı tam
        olarak buydu
      · 390px'te iki sekmede de taşma **0**, konsol temiz
      Ölçüm sonrası tohum hesabı eski hâline döndürüldü (favoriler
      silindi, tercihler açıldı).
      ⚠️ Yayından kalkan tekne listeden **çıkarılmıyor**, işaretleniyor ve
      bağlantısı kapanıyor: sessizce çıkarılsaydı müşterinin listesi
      sebebi görünmeden kısalır ve o kendi sildiğini sanardı.
      ⚠️ Favori kartında **fiyat yok** — fiyat tarihe, kişi sayısına ve
      satış biçimine bağlı; favoride üçü de belli değil. Bağlayıcı
      olmayan bir başlangıç fiyatı, tıklayan müşteriye ilk ekranda başka
      bir tutar göstermek olurdu (backend'in kararı, katılıyorum).
      `6306da3`

- [x] **W-74** İşletme müşterinin iletişim bilgisini artık görmüyor · 2026-09-04
      `S-27` cevaplandı ve gerekçe bizim düşündüğümüz değildi: mesele
      KVKK değil **aracıdan kaçış** — işletme müşteriye doğrudan
      ulaşabilirse ikinci turu platform dışında satar.
      Backend `GET /api/partner/reservations` yanıtından `contactEmail`
      ve `contactPhone` alanlarını çıkardı; panel de kaldırdı.
      **Boş bırakılmadı, sebebi yazıldı**: alanlar kaybolsaydı işletmeci
      telefonu arar, bulamaz ve "sistem eksik" diye okurdu. Liste altında
      duruyor: gecikme ya da hava muhalefetinde **destek talebi aç,
      platform müşteriye senin adına ulaşır**.
      Kanıt: `contactEmail`/`contactPhone` tipten ve dönüşümden çıkarıldı,
      panelde iletişim satırı yok; `tsc` 0 hata, `eslint` temiz. `6306da3`

- [x] **W-38** Blog — üç ekran gerçek uca bağlandı · 2026-09-04
      Mert karar verdi (*"bloglar uç yazılsın, blog yazılabilecek çünkü
      siteden"*), backend uçları yazdı (`07730fb`), web üç parçayı kurdu:
      herkese açık liste + detay, işletme panelinde yazma, yönetim
      panelinde onay.
      **Yolda üç sahte etkileşim bulundu ve kaldırıldı** — üçü de hiçbir
      şeye bağlı değildi ve kullanıcı bunu öğrenemiyordu: bülten formu
      e-postayı alıp hiçbir yere göndermiyordu, yorum formu *"yorumun 24
      saat içinde yayınlanır"* diyordu, Paylaş/Kaydet düğme gibi görünen
      `span`'lardı. Sayfalama da `[1,2,3]` diye sabitti ve tıklanınca
      hiçbir şey olmuyordu. Detay sayfası **her slug için aynı yazıyı**
      gösteriyordu; `/blog/olmayan-bir-sey` dolu bir makale açıyordu.
      🔴 **Bir veri kaybı önlendi, tarayıcı yakaladı.** `GET /api/blog/posts`
      liste satırı çözülmüş düz bir `title` döndürüyor ve `translations`
      **taşımıyor**; tek kayıt uçları tam tersi. Satırı doğrudan forma
      verseydim form **boş açılır**, kullanıcı kaydedince gövde
      **silinir** ve uç `200` dönerdi. `tsc` sustu çünkü tipi ben yazdım
      → [[web-elle-yazilan-tip-yalan-soyler]]
      🔒 **Gövde düz metin basılıyor, `dangerouslySetInnerHTML` ile
      değil.** Backend gövdeyi temizlemiyor (`BlogService.Clean()` yalnız
      `Trim()`, kod tabanında sanitizer yok — arandı). HTML bassaydım
      `blog.write` yetkisi olan bir işletme çalışanı herkese açık sayfaya
      script gömerdi; yazıyı platform onaylıyor ama onaylayan kişi kaynak
      koda bakmıyor, yani onay bunu **yakalamaz**.
      Kanıt: (canlı, iki panelde, uçtan uca)
      · `/blog` gerçek yazı + gerçek kategori (`Rotalar · 1`), `/blog`
        detayı gerçek gövde ve MinIO'dan yüklenen kapak
      · `/blog/olmayan-bir-yazi` → **404**
      · Kategori süzgeci **iki dalda da** ölçüldü: gerçek kategoride yazı
        görünüyor, olmayan kategoride "yazı yok" — her şeye boş dönen
        bozuk bir süzgeç yalnız ikinciden geçerdi
      · İşletme panelinde yazı açıldı → **TR ve EN alanları dolu geldi**;
        Türkçe başlık değiştirilip kaydedildi → uçta `tr` güncellendi,
        **`en` yerinde kaldı** (`W-55` yinelemesi önlendi)
      · Yönetimde yazı okundu, dil seçici `tr`/`en` çalışıyor, **boş
        gerekçede Reddet kapalı**; gerekçeyle reddedildi → kuyruk boşaldı
        ve gerekçe **yazarın panelinde** göründü: *"Gövde çok kısa;
        koyların adlarını..."*
      · Yayına alınan yazı açıldığında uyarı **kaydetmeden önce**
        görünüyor: *"Kaydettiğin anda yazı siteden kalkar"*; `Onaya
        gönder` düğmesi yayındaki yazıda **yok**
      · 390px'te taşma **0** (dosya kutusu 1px taşırıyordu, düzeltildi),
        1280px'te 0, konsol temiz
      ⚠️ Vekilin izin listesinde `blog` öneki **yoktu**; eklenmeseydi
      panelin bütün çağrıları `404` dönerdi.
      `ca13561` · `17a89b1` · `75295ec`

- [x] **W-73** Kart rozetinde tekne tipinin adı · 2026-09-04
      Ana sayfadaki öne çıkan kartlar ve blog yazısının kenar sütunu tur
      tipi rozetinde **marina adı** basıyordu. Yanlış bilgi değildi ama
      sorulan bilgi de değildi — `GET /api/search` tip adını hiç
      döndürmüyordu, yalnız `boatTypeId` vardı.
      Backend ekledi (`52579a7`). **`lookups` ile eşleme yapılmadı**:
      çeviri mantığı iki yere bölünürse biri kaydığında arama sonucu ile
      süzgeç menüsü **sessizce ayrışır**.
      Kanıt: canlı uç ölçüldü, **iki dalın ikisi de** —
      çevrilmiş tip → `Gulet`, çevirisiz tohum satırı → ham anahtar
      `a04-gulet` (**boş dönmüyor**, yer tutucu gerekmiyor). Ana sayfada
      rozet 4 kartta doğru basılıyor, dört bağlantının dördü de **HTTP
      200**; blog yazısında da aynı. `tsc` 0 hata, `eslint` temiz.
      ⚠️ Ham anahtar `a04-gulet` artık **ana sayfada görünüyor** — istemci
      tarafında "anahtar gibi duruyorsa gizle" sezgisi konmadı, o ayrım
      uydurma olurdu. Kaynağı geliştirme veritabanındaki tohum çöpü,
      `S-22` ile backend'de. `a2f54c4`

- [x] **W-72** Blog yazısındaki 404 veren tekne kartları · 2026-08-31
      `W-71`'deki kusurun aynısı yazının içinde de vardı: "Bu koylara
      çıkan tekneler" listesi dört tekne basıyor ve **dördünün de
      bağlantısı 404** veriyordu. Yazıyı okuyup "bu tekneye bakayım"
      diyen ziyaretçi, tam ilgilendiği anda ölü sayfaya düşüyordu.
      Altındaki "Bodrum'daki 96 tekneyi gör" bağlantısı da uydurma sayı
      taşıyordu (10 tekne var).
      Gerçek katalogdan besleniyor; okuma başarısızsa bölüm hiç
      basılmıyor.
      **Tarama yapıldı:** veri dosyalarındaki tüm sabit slug'lar `/api/boats`
      ucuna karşı denendi — tekneye işaret eden başka 404 bağlantı yok.
      Kanıt: yazı canlı → dört uydurma ad ve "96 tekneyi" yok; kenar
      sütunundaki dört bağlantı gerçek tekneye gidiyor, **dördü de HTTP
      200**. Taşma 0. `80479f7`

- [x] **W-71** Ana sayfadaki uydurma iddialar ve **404 veren kartlar** · 2026-08-31
      ⚠️ Bu oturumun en ciddi bulgusu: ana sayfanın "öne çıkan tekneler"
      bölümü **üç uydurma tekne** basıyordu ve üçünün bağlantısı da
      **404** veriyordu (`gulet-isil`, `poyraz-kaptan`, `mavi-yelken-ii`).
      Sitenin en görünür kartları ziyaretçiyi ölü sayfaya götürüyordu.
      Artık `GET /api/search`'ten geliyor; okuma başarısızsa bölüm hiç
      basılmıyor — uydurma tekne de "tekne yok" iddiası da yanlış olurdu.
      Aynı sınıftan: üst şeritteki "340+ onaylı tekne" (ölçülen **10**;
      **her sayfada** duruyordu, sitedeki en çok okunan yanlış oydu),
      "4.812 doğrulanmış yorum · 4,8/5" (ölçülen **2** onaylı yorum),
      "4,8 ★ (2.140 değerlendirme)" (uygulama yayında değil), bölge
      kartlarındaki tekne sayıları (Bodrum 96 · Marmaris 74 · Fethiye 68,
      toplam 10 tekne varken) ve üç isimli misafir yorumu.
      **"Yakında" ayrımı gerçekti, korundu:** `boatCount: 0` yerine
      `soon` bayrağı kondu — sayı uydurmaydı ama ayrım değildi.
      `brand.ts`'te yalnız doğrulanamayan sayılar çıktı; telefon, adres,
      TÜRSAB numarası `W-06` ile Mert'te, dokunulmadı.
      Kanıt: ana sayfa canlı → uydurma dizelerin hiçbiri yok; öne çıkan
      dört kartın dördü de gerçek tekneye gidiyor ve **dördü de HTTP
      200**. Konsol temiz, taşma 0. `5c7abc3`

- [x] **W-70** Yolcu listesi uyarısı teklife bağlandı, sessiz delik kapandı · 2026-08-31
      `W-69`'da uyarı `boat=<slug>` sorgu parametresinden okunuyordu —
      `pricing/quote` bayrağı yanlış döndürdüğü için mecburen. Uç
      düzeltildi (bayrak tekneden okunuyor, tur süresinden türetilmiyor),
      kaynak teklife taşındı.
      **Kapatılan delik:** yer imine alınmış bağlantıda `boat` eksik
      kalırsa uyarı hiç çıkmıyordu. Teklif her durumda çağrılıyor.
      Süre teklif yanıtında yok, yalnız tekne detayında; bu yüzden ikisi
      ayrıldı — **kritik iddia her zaman görünür, ayrıntı zarifçe düşer.**
      Kanıt: üç durum canlı ölçüldü — `true` + `boat` var → tek uyarı,
      "kalkıştan en geç 24 saat önce"; `true` + `boat` **yok** → uyarı
      yine çıkıyor, yalnız süre düşüyor (**kapatılan delik tam olarak
      bu**); `false` → uyarı yok, form çalışıyor. Konsol temiz, taşma 0.
      Ölçüm sırasında bir kez "süre gelmiyor" görüldü — hata değil,
      tekne detayının 60 sn önbelleğiydi; hata ilan etmeden önce
      tekrar ölçüldü. `8daecfc`

- [x] **W-69** Yolcu listesi uyarısı karar anına taşındı · 2026-08-31
      Uyarı tekne detay sayfasında vardı ama **sayfanın altında**,
      Kurallar ile Değerlendirmeler arasında. Müşteri yukarıdaki panelden
      doğrudan ödemeye gidiyor ve bu turun kimlik bilgisi isteyeceğini
      **ödeme sonrasına kadar hiç görmüyordu.**
      ⚠️ **Neredeyse sessizce çalışmayan bir uyarı yayına alıyordum.**
      Bayrak `pricing/quote` yanıtında da var ve akış zaten quote
      çağırıyor — oradan kurmak en doğal seçimdi. Ölçünce quote bu
      bayrağı **aynı tekne için yanlış** döndürüyor:
      `boats/{slug}` → `true`, `partner/boats/{id}` → `true`,
      `pricing/quote` → **`false`**. Kursaydım uyarı hiç görünmeyecek ve
      tekne sayfasındaki uyarı çalıştığı için "çalışıyor" diyecektim.
      Bunun yerine bağlantıda **zaten geçen ama okunmayan** `boat`
      parametresinden tekne detayı çekiliyor.
      Sınır kodda ve panoda yazılı: `boat` yoksa uyarı basılamaz —
      yer imine alınmış bağlantıda eksik kalır. Sağlam çözüm quote'un
      düzelmesi; uç düzelince bu okuma yedeğe düşer.
      Kanıt: üç durum canlı ölçüldü — bayrak `true` teknede uyarı
      **formun üstünde**; `false` teknede basılmıyor, form çalışıyor;
      `boat` parametresiz hata yok, form çalışıyor. Konsol temiz,
      taşma 0. Pozitif durum için tohum teknesinin bayrağı `true`
      yapıldı (katalogda hiçbiri `true` değildi). `f0d4697`

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
