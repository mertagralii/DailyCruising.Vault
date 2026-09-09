---
rol: gorev
kapsam: api
guncelleme: 2026-09-09
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

### Mert'in 2026-08-26 kararlarından doğan işler

> 23 sorunun hepsi cevaplandı; 6'sı onaylandı (kod değişmiyor), **17'si iş
> çıkardı**. Gerekçeler → [[api-benim-kararlarim]]

- [ ] **A-58** Alıcı kaydı olmayan işletmeyi satışa kapat · 🔴 **`A-41`'e BAĞLI** (soru 21)
      ⚠️ Bugün açılamaz: hiçbir işletmenin alıcı kaydı yok, katılaştırma
      **tüm satışı durdururdu**. İyzico pazaryeri özelliği açılıp işletmeler
      onboard edildikten SONRA

- [ ] **A-41** Alt üye iş yeri ve hakediş transferi · 🔴 **MERT'TE** ·
      ⚠️ **2026-09-05: SAĞLAYICI DEĞİŞTİ — Mert "ödeme sistemi paratika olacak"
      dedi.** Aşağıdaki İyzico ölçümü artık geçmiş kaydıdır. Paratika'nın
      pazaryeri modeli belgeli ve satıcı kaydı bir API aksiyonu (`SELLERADD`);
      `RegisterPayeeAsync` gerçekten yazıldı. Kalan iş kod değil **hesap**:
      Paratika üye işyeri açılması, pazaryeri modelinin etkinleştirilmesi ve
      `Merchant` / `MerchantUser` / `MerchantPassword` bilgilerinin verilmesi.
      → [[api-kararlar]] 2026-09-05 (13)
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
      API yarısı BİTTİ. `A-07a`: `openapi.json` repoda, bayatlaması test edilir.
      `A-07b` (2026-09-05): 146 operasyonun 145'i artık gövde şeması taşıyor,
      durum kodları gerçeği söylüyor, 181 bileşen şeması üretiliyor.
      **KALAN, ve bu oturumun işi DEĞİL:** web tarafında `openapi-typescript`
      ile tip üretimi + `npm` betiği. `03-Web/` başka bir oturumun yazma
      alanında — backend oturumu oraya yazmıyor
      Kabul: web tarafı elle tip yazmaz

### Web oturumunun bildirdiği eksikler — sıra Mert'te

> Yönetim panelinin **25 modülünden 15'inin ucu yok**. Liste web tarafında
> `admin-durum.ts` tarafından ÜRETİLİYOR, elle yazılmıyor.

- [ ] **A-112** Yasal metin sürümleri ve onay sayıları · 🔴 **MERT'TE** ·
      ⚠️ **uyum konusu olabilir**
      Tasarımdaki "Sözleşme listesi" işletme sözleşmesi şablonları DEĞİL,
      sitenin yasal metinleri: kullanım koşulları, gizlilik politikası, her
      birinin sürümü ve kaç kullanıcının onayladığı.
      **Ölçüldü:** `ConsentDocuments` (2 satır, `BodyHtml` dahil) ve
      `ConsentRecords` (UserId, ConsentType, DocumentVersion, AcceptedAt, Ip,
      UserAgent) tabloları VAR. Veri modeli hazır, "kaç kullanıcı onayladı"
      sorusu bugün SQL'de cevaplanabiliyor. **Eksik olan yalnız uç** — hiçbir
      uç bu iki tabloyu okumuyor ya da yazmıyor.
      Onaylanırsa desen `A-109` ile aynı olmalı: metin değişince yeni SÜRÜM,
      eski sürüm okunmaya devam eder çünkü kullanıcı onu kabul etmiştir

- [ ] **A-113** Ucu olmayan 12 panel modülü (müşteri listesi `A-117`, rezervasyon listesi `A-128` ile kapandı) (genel bakış `A-115` ile kapandı) · 🔴 **SIRALAMA MERT'TE**
      platform personeli · müsaitlik (platform kapsamı) · iptal talebi kuyruğu ·
      rezervasyon ayarları · personel adına rezervasyon · bölge yazma ·
      reklam · platform finans · e-posta şablonları · SMS şablon + gönderim
      kayıtları · log okuma · **aktivite (denetim izi)**
      ⚠️ Web oturumu birini ayırıyor: **aktivite kaydı**. Panelde artık para
      ve müşteri verisi üzerinde işlem yapılıyor (kupon açma/kapatma,
      sözleşme gönderme, yorum denetleme) ve "kim yaptı" sorusu bugün yalnız
      veritabanına bakarak cevaplanabiliyor. Yazma uçları çoğaldıkça ağırlaşır

- [ ] **A-114** Blog moderasyon listesi kategori ADI döndürsün
      Bugün kategori kimliği dönüyor, cephe ikinci bir istekle çözüyor.
      Küçük iş; liste büyüdüğünde maliyeti artar

## 🟡 Yapılıyor

- [ ] **A-133** Biniş red sebepleri enum'a çevrilsin, belgeye girsin

      `NotPaid`, `Cancelled`, `TokenExpired`, `TokenNotFound`, `Refunded`,
      `Expired`, `AlreadyCompleted`, `NotBoardable` — hepsi
      `BoardingService.cs` içinde **düz dize sabiti**. C# enum'u olmadıkları
      için OpenAPI belgesine girmiyorlar.

      Sonucu: ön yüz bu anahtarları Türkçeye çeviren bir sözlük tutuyor ama
      `satisfies` kapısı onu koruyamıyor — sunucuya yeni bir sebep
      eklendiğinde sözlük sessizce eksik kalır ve ekranda **ham İngilizce**
      görünür. Ön yüz bunu bir kez yaşadı (`4a015e7`): `NotPaid` olduğu gibi
      basılıyordu, Mert'in "Paid yazıyor" dediği kusurun aynısı.

      Bugün ayrışmış değil; kusur, ayrışmayı **hiçbir şeyin yakalamayacak
      olması**. Enum'a çevrilirse `EnumSchemaTransformer` (`A-122`) onları
      belgeye sokar ve kapı çalışmaya başlar.

      🔴 **SIRALAMA MERT'TE**

- [ ] **A-134** Okutulmuş karekod tekrar okutulduğunda sunucu ne yapmalı?

      Mert: *"Okutulmuş QR tekrar okutulamamalı, ama okutulursa uyarı
      vermeli."* Bugün ikinci okutma **kabul ediliyor**: biniş tekrar
      işaretlenmiyor (`isFirstBoarding` false), `AlreadyBoarded: true`
      dönüyor, kaptan yolcu listesini görüyor.

      Harfiyen uygulanırsa sunucunun ikinci okutmayı **reddetmesi** gerekir —
      o zaman manifestoyu teyit etmek için okutan kaptan hata alır. Hem API
      hem web oturumu buna karşı; karar Mert'in.

      ⚠️ **Reddedilen bir ara yol:** ikinci okutmayı `Succeeded = false` +
      `FailureReason = "AlreadyBoarded"` yazmak. Üç sebeple hayır, ölçüldü →
      [[api-kararlar]]

      🔴 **MERT'TE**

## 🟢 Tamamlandı

- [x] **A-151** Platform rolleri panelden düzenlenip silinebiliyor · bitti: 2026-09-09

      Web oturumu istedi: *"mevcut rolleri düzenleyebilmek ve kişiye özel
      rol oluşturabilmek."* İkincisi mevcut uçlarla kuruluyor (rol yarat +
      ata); yazılan şey birincisi.

      `GET · PUT · DELETE /api/platform/staff/roles/{roleId}`

      ⚠️ **Yeni sınıf bir tehlike: bir rolü değiştirmek o rolü taşıyan
      HERKESİ değiştirir.** `A-150`'de bir kişi etkileniyordu. Web
      oturumunun uyarısı doğruydu ve kapı uçta.

      **Ayrıntı ucu ZORUNLUYDU, süs değil:** liste ucu yalnız
      `permissionCount` döndürüyor. Düzenleme formu hangi kutuları
      işaretleyeceğini hiçbir yerden okuyamazdı.

      **Sistem rolleri hiç düzenlenemiyor — adları bile.** Gerekçe
      ölçüldü → [[api-kararlar]] 2026-09-09.

      **`LastAdmin` kapısı bilerek YAZILMADI.** Çağıranın `staff.manage`
      yetkisi zaten var; rolden sonra da kalıyorsa sistemde yönetici var,
      kalmıyorsa `CannotModifySelf`'e takılıyor. Yani hiç
      ateşlenemezdi. `A-150`'de küresel değişmezi yalıtmayı öğrendikten
      sonraki adım bu: **ateşlenemeyen kapıyı hiç yazmamak.**
      → [[api-kararlar]] 2026-09-09

      Kanıt: `dotnet test` 725/725. **Altı mutasyon, altısı da doğru testi
      kırmızıya döndürdü:** sistem rolü kapısı · ad benzersizliğinde kendini
      hariç tutma · damganın yalnız ilk taşıyıcıda yenilenmesi · yetki
      kümesinin değiştirilmek yerine birleştirilmesi · `RoleInUse` ·
      `CannotModifySelf`'in her zaman reddetmesi.
      Canlıda (`:5163`) dört kapı da doğrulandı: `SystemRoleImmutable`
      (düzenleme ve silme), `RoleInUse`, ve gerçek bir düzenlemede
      `payout.read` rolden düştü, sonra geri verildi.

- [x] **A-150** Personel düzenleme, rol değiştirme ve durum uçları · bitti: 2026-09-09

      ⚠️ **İki kilitlenme kapısı, ikisi de UÇTA.** Web oturumu buldu ve
      "ekranda olursa curl ile atlanır" dedi — doğru.

      `CannotModifySelf`: çağıran kendi yönetim yetkisini kaldıramaz.
      Kaldırabilseydi **geri veremezdi** — yetki gidince rol değiştirme ucu
      da kapanır.

      `LastAdmin`: yönetim yetkisi taşıyan son AKTİF kişi korunuyor. Sayım
      **yetkiye** göre, rol adına göre değil (özel rol de `staff.manage`
      taşıyabilir); askıdaki kişi sayılmıyor.

      `Closed` kabul edilmiyor → [[api-kararlar]]. E-posta düzenlenemiyor:
      giriş kimliği o.

      ⚠️ **İlk testim HİÇBİR ŞEY ölçmüyordu** ve yeşildi: "son yönetici"
      küresel bir değişmez, paylaşılan veritabanındaki diğer yöneticiler
      sayıyı 1'in üstünde tutuyor ve kapı hiç ateşlenmiyordu.
      → [[api-kararlar]]

      Kanıt: `96264b8` · 720/720 · üç mutasyon, üçü kırmızı

- [x] **A-149** Zorunlu parola değişikliği gerçekten zorlanıyor · bitti: 2026-09-09

      Bayrak + jetonda `mcp` talebi + ara katman kapısı +
      `POST /api/account/change-password`.

      ⚠️ **Bayrak tek başına bir söz olurdu.** Kapı, bayrak açıkken dar bir
      izin listesi dışındaki her uca `403` veriyor. Liste, parolanın
      değiştirilebilmesi için ZORUNLU olanlarla sınırlı — mutasyonla
      ölçüldü: `change-password` listeden çıkarılınca kullanıcı kilitleniyor.

      Mevcut parola soruluyor; yeni parola eskisiyle aynı olamıyor (yoksa
      zorunluluk tek tuşla aşılırdı). Değişince damga yenileniyor, **eski
      jeton 401 alıyor** — ön yüzün vekil katmanını ilgilendiriyor.

      Kanıt: `37ce71c` + `cac35c5` · üç mutasyon kırmızı · kodlar:
      `InvalidCredentials` · `PasswordTooShort` · `PasswordUnchanged`

- [x] **A-148** Platform ve işletme kapsamları veritabanında ayrıldı · bitti: 2026-09-09

      Mert: *"İşletme çalışanı platform rolü veremez. Platform yöneticisi
      sadece kendi platform yönetimi için roller ve kişiler alabilir."*

      `A-146`'da ölçülen açık kapatıldı: iki tetikleyici de yalnız **rolün
      doğru tabloya** gitmesini zorluyordu. Artık iki yönlü ve ikisi de
      geri alınan işlemlerde ölçüldü.

      Kanıt: `37ce71c` · migration `A112` · `dailycruising` rolüyle uygulandı

- [x] **A-147** Personel rol seçenekleri ucu · bitti: 2026-09-09

      ⚠️ **Eksik BENDEYDİ:** `A-145` `roleIds` istiyordu ama kimliklerin
      okunacağı bir uç yoktu. Ön yüzün tek seçeneği GUID'leri koda gömmekti
      ve veritabanı sıfırlandığında form **sessizce** yanlış role atardı.
      Web oturumu bunu reddedip bildirdi — doğru karardı.

      Yalnız platform rolleri dönüyor (6 işletme rolü listede yok).
      `permissionCount` ile "Destek Personeli — 11 yetki" yazılabiliyor;
      Mert'in *"yetkileri de ayarlayalım"* isteğinin karşılanabilen kısmı.

      `PlatformStaffRole` artık `id` de taşıyor — ikinci eksik.

      ⚠️ Test **"liste doldu"** demiyor, "listeden alınan kimlik oluşturmada
      çalışıyor" diyor. Uç zaten `POST /api/platform/staff`'ı beslemek için
      var; kimlik orada kabul edilmezse liste dolu görünüp işe yaramaz.

      Kanıt: `f4966dc` · 715/715 · iki mutasyon, ikisi kırmızı · uçtan
      doğrulandı

- [x] **A-145** Panelden platform personeli hesabı açılabiliyor · bitti: 2026-09-09

      Mert: *"e-posta adresini, şifresini, rolünü … buradan ayarlayıp
      personeli oluşturacağız. Ardından artık personelimiz siteye giriş
      yapabilecek."*

      ⚠️ **Başarı ölçütü kayıt yazılması DEĞİL, girişin çalışması** —
      Mert'in cümlesi bunu söylüyor. Test de üretimin gerçek parola
      doğrulayıcısına soruyor, kendi iddiasını üretmiyor.

      Parola kuralı tekrar yazılmadı; aynı sayı `limits.passwordMinLength`
      ile ön yüze veriliyor. Karmaşıklık şartı yok ve bu bilinçli.

      🔴 **Karşılanamayan istek:** *"gerekliyse yetkilerini de ayarlayalım"*
      — `RolePermission` rol bazlı, kişiye özel yetki kavramı yok. Rol
      oluşturma ucu (`POST /api/platform/roles`) yazılmadı, Mert'te.

      🔴 **`mustChangePassword` YOK.** Yöneticinin belirlediği parolayı iki
      kişi biliyor; sistemde "ilk girişte değiştir" kavramı yok ve uç onu
      icat etmedi. → [[api-kararlar]]

      ⚠️ Test saati **2034**'e taşındı: üretim yolundan yazılan kullanıcılar
      servisin saatini taşıyor ve 2031'de `OverviewTests`'in YIL penceresine
      düşüyorlardı. İlk deneme (2026 → 2031) durumu kötüleştirdi (4 → 20);
      yıllar sayılarak boş olan seçildi.

      Kanıt: `a759914` · 714/714 · **üç mutasyon, üçü kırmızı** · uçtan:
      oluşturma 201 → **yeni personel girişi 200** · kısa parola 400 ·
      kayıtlı e-posta 400

- [x] **A-144** Müşteri ve personel ayrıntısı aynı dönem seçimini kabul ediyor · bitti: 2026-09-09

      İki uç asimetrikti: müşteri yalnız `period`, personel yalnız
      `from`/`to`. Mert ikisinde de ikisini istedi. Ortak çözücü
      (`PeriodSelection`) yazıldı; dönem sözlüğü `OverviewPeriod`'dan
      geliyor ve **çoğaltılmadı** — iki sözlük sessizce ayrışır.

      ⚠️ **`period` ile `from`/`to` birlikte gelirse `400 PeriodAndRange`.**
      Web oturumu "aralık kazansın" önerdi, reddedildi → [[api-kararlar]]

      Personeldeki `rangeStart`/`rangeEnd` → `periodStart`/`periodEnd`;
      müşteri ucu zaten bu adı kullanıyordu. Yanına dönem adı eklendi,
      serbest aralıkta `custom`.

      Varsayılanlar **bilerek farklı**: müşteride `all`, personelde `month`.

      Kanıt: `03d1ce4` · 712/712 · **iki mutasyon, ikisi kırmızı** · uçtan
      ikisinde de `all/day/week/month/year` + `custom` + `400`

- [x] **A-143** İşlem ayrıntısı · ömür boyu çözülen · destek sayaçlarında tarih süzgeci · bitti: 2026-09-09

      ⚠️ **`payload` kararı tersine çevrilmedi, KAPSAMI değişti.** 08 Eylül'de
      "ham JSON gönderme" denmişti; gerekçe ekrana yaramaması ve içeriğinin
      bilinmemesiydi. Mert *"ne değişti"* isteyince gövde **izin
      listesinden** geçirilerek Türkçe etiketli alanlara çevrildi.

      ⚠️ **İzin listesi, yasak listesi DEĞİL — ve gerekçesi ölçüldü:**
      `AuthService` başarısız girişte kullanıcının **tam e-postasını**
      gövdeye yazıyor (`NormalizeEmailForLog` yalnız biçim doğruluyor).
      Yasak listesi kurulsaydı o alanı tek tek hatırlamak gerekirdi ve
      gövdeye yarın eklenecek alan kendiliğinden ekrana düşerdi.

      🔴 **Karşılanamayan istek, uydurulmadı:** *"hangi izin eksikti"* gövdede
      YOK. Red olayları `action` ve `reason` taşıyor, izin anahtarı hiçbir
      yerde kaydedilmiyor. Olay yazan tarafı değiştirmek ayrı bir iş.

      ⚠️ **Red sebepleri kümesi KAPALI değil** ve bu sözleşmede yazılı: olay
      türlerinin aksine tek yerde tanımlı değiller, yansımayla sayılamıyorlar.
      18'i çevrildi, tanınmayan ham geçiyor. `EventTitles`'daki bütünlük
      testinin karşılığı burada **kurulamıyor**.

      Sayaç anlambilimi: `openTickets` ve `resolvedTotal` aralıktan
      **etkilenmiyor** — biri anlık durum, diğeri ömür boyu. → [[api-kararlar]]

      ⚠️ **Ekranda bir kusur çıktı ve düzeltildi (`8bb1257`):** alan
      etiketleri Türkçeydi ama DEĞERLER ham geçiyordu — *"İşlem:
      moderation.publish"*. `action`, `stage`, `resource` için de sözlük
      eklendi. Kusuru ne derleme ne test ne uçtan bakmak yakaladı;
      tarayıcıda göründü.

      Kanıt: `f429d7e` + `8bb1257` · 709/709 · **dört mutasyon, dördü
      kırmızı** · uçtan:
      "yalnız bugün" aralığında `resolvedInRange` 1→0 düşerken açık ve ömür
      boyu değişmedi · ters aralık `400 InvalidRange`

- [x] **A-142** İşlem geçmişi sınıfa göre süzülüyor · blog ve yorum etiketleri · bitti: 2026-09-08

      ⚠️ **Süzgeç UÇTA, istemcide değil — sebebi `totalCount`.** Web oturumu
      süzgeci basmayı bekledi ve doğru yaptı: istemcide süzseydi yalnız açık
      sayfa süzülür, sayaç 36'da kalır ve ekranda sekiz satır dururken
      "36 kayıt" yazardı.

      ⚠️ **`Write` süzgeci DIŞLAMAYLA kuruldu, kapsamayla değil.** `KindOf`
      tanınmayan türü `Write` sayıyor; kapsama listesi kurulsaydı sözlükte
      olmayan bir olay süzgeçten **düşerdi** — aynı satır ekranda
      "Değişiklik" rozetiyle görünürken süzgeçte kaybolurdu. Testte sözlükte
      olmayan bir tür yazılıp ölçüldü; mutasyon kapsamaya çevirince beklenen
      2 yerine 1 döndü.

      `subjectType`'ın **tam listesi ölçüldü: 20 tür.** Web oturumu 8 yazmıştı
      ve tahminle yazdığını söyledi — tam görünen ama sessizce eksik bir
      sözlük. Blog ve yorum etiketi eklendi (5 → 7 tür çözülüyor).

      Kanıt: `9496b8f` + `56f8bf7` · 706/706 · uçtan: 10+21+5 = 36 ve her
      süzgeçte `totalCount` satır sayısına eşit · **ekranda görüldü**, üç çip
      de doğru, Reddedilen deneme dalı ilk kez

- [x] **A-141** Personelin işlem geçmişi ucu · bitti: 2026-09-08

      Mert: *"personel detayına girdiğimde ekstra olarak neler yapmış onu da
      göreyim."* Kaynak zaten vardı (`EventLog`), ucu yoktu.

      ⚠️ **`ActorType` değeri `Platform`, `PlatformStaff` DEĞİL.** Web
      oturumu öyle sanıyordu; enum'da o değer yok. Ölçülmeseydi sorgu
      **herkes için boş** döner ve ekran "hiçbir şey yapmamış" derdi —
      hata da vermeden. Peer'ın verdiği bir değeri doğrulamanın karşılığı.

      ⚠️ **Okunur başlık sunucuda, koruma bir TESTTE.** `EventTypes` bir
      `const string` sınıfı, enum değil — derleyici bütünlüğü zorlayamıyor.
      Yansımayla 77 sabitin hepsi okunup başlığı olduğu doğrulanıyor, ters
      yön de (sözlükte fazlalık kalamaz). → [[api-kararlar]]

      ⚠️ **`kind` üç değerli**, web oturumunun istediği iki değil:
      `Read` · `Write` · `Denied`. Red/başarısızlık olayları ikisinden de
      değil; sıkıştırmak denetim ekranında yalan üretirdi.

      `payload` dönmüyor (içeriği bilinmiyor, kişisel veri riski).
      Yetki `eventlog.read`, `staff.manage` değil.

      Kanıt: `1a093f3` · `dotnet test` 705/705 · **üç mutasyon, üçü kırmızı**
      · uçtan doğrulandı, 36 satır, başlıksız 0

- [x] **A-139** Yetki ve rol adlarındaki Türkçe karakterler · bitti: 2026-09-08

      Ölçüm: **51 yetkinin 51'inde** Türkçe karakter yoktu, sıfır istisna.
      Roller de öyle. Kaynağı `A03_YetkiKatalogu` (24 Ağustos) tohum verisi.

      ⚠️ **Kusur iki hafta görünmedi çünkü bu isimleri hiçbir ekran
      basmıyordu.** `A-138`'in personel ayrıntısı onları ilk kez gösterdi.
      "Yazılan ama okunmayan veri" — bayatlığı hiçbir şeyin bağırmadığı bir
      alan, `DepartureDate`/`StartsAt` ile aynı sınıf.

      ⚠️ **Eski migration DEĞİŞTİRİLMEDİ, yenisi yazıldı.** Çalıştırılmış
      bir migration'ı düzenlemek onu zaten uygulamış veritabanlarında hiçbir
      şey yapmaz — *"geliştirmede düzeldi, üretimde bozuk kaldı"*nın klasik
      yolu budur. Uyarı web oturumundan geldi.

      `Category` de düzeltildi; ekranda gruplama başlığı ve yarısını
      düzeltmek aynı ekranda iki yazım demekti. `Key` değişmedi.

      İskeletin **boş** üretilmesi şemanın değişmediğinin kanıtı. `Down`
      bilerek boş: geri alma, doğru isimleri bozuğa döndürmek olurdu.

      Kanıt: `ff66132` · 51 addan 46'sında Türkçe karakter var, kalan 5'i
      ("Fatura kes", "Destek talebi ata"…) gerçekten diakritiksiz ·
      `dotnet test` 702/702 · **ekranda görüldü**: "Kullanıcıları
      görüntüle", başlıklarda "MESAJLAŞMA" · migration `dailycruising`
      rolüyle uygulandı

- [x] **A-140** Personel sayfası `totalCount` diyor · üç dalı sınayan demo personel · bitti: 2026-09-08

      Ön yüz zarf ayrışmasını ölçtü: sayfalı şemaların **12'si
      `totalCount`**, 2'si `total` — biri benim dünkü ucumdu. Çoğunluğa
      çekildi. Kalan istisna `BlogListResponse`, bilerek bırakıldı.

      Demo personel üç dalı açıyor: **Selin** (ortalama 60 dk) · **Kerem**
      (yalnız yanıtsız talep → ortalama `null`, ekran "—" basmalı) ·
      **Deniz** (iki rollü, `(UserId, RoleId)` bileşik anahtarının ilk
      canlı örneği).

      Kanıt: `c7da3b3` · 702/702 · uçtan doğrulandı, zarf `totalCount`,
      üç dal da görünür · personel 4 → 7

- [x] **A-138** Platform personeli listesi ve ayrıntısı · bitti: 2026-09-08

      Panelin Personel Listesi modülünün ucu yoktu. `/api/partner/members`
      İŞLETME personeli — başka kapsam. Karışma riski veritabanında da
      kapalı: `trg_user_role_is_platform` işletme rolünün `UserRoles`'a
      yazılmasını reddediyor.

      ⚠️ **`roleNames` ÇOĞUL ve bu ölçülerek seçildi.** `UserRoles`'un
      anahtarı `(UserId, RoleId)` bileşik; ikinci rolü engelleyen kısıt yok.
      Bugünkü veride herkesin **tam olarak bir** rolü var — yani tekil bir
      alan bugün doğru görünür ve ikinci rol verildiği gün o rol ekranda
      **hiç görünmezdi, hata da vermeden**. Günün ilk dersinin dördüncü
      tekrarı: tek çeşit veri kusuru gizler.

      ⚠️ **Destek ölçütleri ROLE değil YETKİye bağlı** (`support.read`).
      Role bakılsaydı `platform.admin` rolündeki biri gerçekten talep
      üstlendiği hâlde ölçütsüz görünürdü — o rol de bu yetkiyi taşıyor.
      Ön yüz "yalnız destek rolündekiler" demişti; daraltma kabul edildi.

      Gönderilmeyen iki alan, ikisi de sistemde YOK: **departman**
      (`Domain`'de kavram hiç geçmiyor) ve **memnuniyet puanı** (puanlama
      hiç toplanmıyor). İkisi de tasarımda ve örnek veride gerçekmiş gibi
      duruyordu — ön yüz ölçüp bildirdi, ikimiz de göndermedik.

      Kanıt: `af69017` · `dotnet test` 702/702 · **üç mutasyon, üçü kırmızı**
      (rolleri `Take(1)` ile tekile indirmek · yetki kapısını kaldırıp
      ölçütü herkese vermek · açık talebi toplam talep saymak) · uçtan
      doğrulandı

- [x] **A-137** Destek mesajı iç not olup olmadığını söylüyor · bitti: 2026-09-08

      `IsInternal` **süzgeçte hep vardı ama izdüşümde yoktu**: iç notlar
      personele dönüyor, panelde müşteriye gitmiş bir yanıtla **birebir aynı**
      görünüyordu. Personel iç notu okuyup müşteriye *"size yazmıştık"* der,
      ya da gerçek yanıtı iç not sanıp aynı şeyi ikinci kez yazar.

      ⚠️ `fromStaff`'ın yerine geçmiyor, onunla BİRLİKTE anlam kazanıyor —
      iki ayrı eksen. Müşteri tarafında hep `false`; gizleme değil süzgecin
      sonucu, iç notlar ona zaten hiç dönmüyor.

      ⚠️ **Test tek bayrağı değil, iki eksenin AYRI olduğunu ölçüyor.** Aynı
      talepte müşteriye giden bir personel yanıtı da var ve `false` olması
      aranıyor; yoksa her personel mesajına `true` yazan kod da geçerdi.
      Mutasyon (`IsInternal = m.FromStaff`) kırmızı verdi.

      Kanıt: `abc87a8` · `dotnet test` 696/696

- [x] **A-136** Ayşe'ye ödeme dökümünün her parçasını taşıyan rezervasyon · bitti: 2026-09-08

      Konuşulan her şey üç ayrı kayda dağılmıştı ve biri (`TWMWER6R`)
      **misafir** Ayşe'nindi — kayıtlı müşterinin detay sekmesinde hiç
      görünmüyor, iki Ayşe farklı kişiler.

      ⚠️ **Ödenmiş `6UGJC9S4`'e kalem EKLENMEDİ.** En az iş gibi görünüyordu
      ama ödeme kaydı ₺2.900 diyor; kalem eklenince rezervasyon başka bir
      tutar söyler ve **defterle çelişirdi**.

      ⚠️ **Tekne ölçülerek seçildi.** Ayşe'nin her zamanki teknesinin ek
      hizmet fiyatları (150/450/1200) 1,2'ye TAM bölünüyor — orada hangi
      kalem seçilirse seçilsin kuruş yuvarlaması **sınanmadan geçerdi**.
      Deniz Kızı'nda 280×1 → 233,33 ve 320×2 → 533,33 ama toplamın neti
      766,67: bir kuruş artık. "Ek hizmetli bir kayıt" istemek yetmiyordu,
      **artık üreten** bir kayıt gerekiyordu.

      Kanıt: `008cc29` · `ZJYWDJBW` · ekranda görüldü: Meze tabağı **233,34**
      (artık üstlenilmiş), satır toplamı = genel toplam, karekod ve okutma
      kaydı dolu

- [x] **A-135** Ödeme dökümü kalem kalem KDV'siz karşılığıyla dönüyor · bitti: 2026-09-08

      Mert: panelde *"tur bedeli · ek hizmetler · KDV · genel toplam"* alt
      alta görünsün.

      ⚠️ **İsteği önce YANLIŞ anladım.** "Tur bedeli + ek hizmet + KDV =
      toplam" tarifini "KDV üste eklenecek" diye okudum ve fiyat kodunu
      değiştirmeye başladım — `PricingService`, DB kısıtı, migration
      planlandı. Mert durdurdu: *"yok ilan fiyatında yine kdvli tutarı
      görsün müşteri sadece bu sana bahsettiğim sayfada böyle gözüksün."*
      Geri alındı; **fiyatlandırma dokunulmadı.**

      Ders: "toplam şu artı bu" cümlesi, tahsilat modelini mi yoksa
      GÖSTERİMİ mi tarif ediyor — ikisi aynı cümleyle söyleniyor ve
      birbirinden ancak sorunca ayrılıyor. Yanlış olanı seçmek burada
      migration + fiyat değişikliği demekti.

      Ayrıştırmanın kuralı: ekranda alt alta yazılan her sayı üstündeki
      toplamı tutmak zorunda. Bu yüzden değerler tek tek "doğru"
      hesaplanmıyor, **toplamları koruyacak** şekilde üretiliyor — KDV
      artakalan olarak bulunuyor, son kalem yuvarlama artığını üstleniyor.

      ⚠️ **Testimin İKİ hâli de ölçmüyordu, ikisini de mutasyon gösterdi:**
      (1) "net + KDV = toplam" bir totolojiydi — net zaten çıkarmayla
      üretiliyor, KDV ne olursa olsun tutuyordu. (2) Seçtiğim 640+900
      tutarları yuvarlama artığı BIRAKMIYOR; artığı düzelten satırı sildim,
      test yine yeşil kaldı. Artık bırakan çifti hesaplayarak buldum
      (100+100 → satır başına 83,33 ama toplamın neti 166,67).

      Kanıt: `ce82522` · `dotnet test` 695/695 · uçtan (restart sonrası)
      `4P3WVK4Z`: satırların toplamı = genel toplam ✓, kalemlerin neti =
      ek hizmet toplamı ✓

- [x] **A-132** Karekodu saklanmış binilmiş bir demo rezervasyonu · bitti: 2026-09-08

      Mert binilmiş bir rezervasyonda karekodu göremiyordu. Ölçüldü:
      `2A2UA3HS`'te **jeton değil, biletin kendisi yok** — `BoardingTickets`
      satırı hiç oluşmamış, biniş bilet olmadan işaretlenmiş. Silme kodu
      arandı, yok: bu kayıt jeton saklama gelmeden önce öyle kurulmuş.

      ⚠️ **O kayda geçmişe dönük jeton YAZILMADI.** Düz metin jeton hiçbir
      yerde saklanmamış, geri getirilemez; yeni bir jeton basmak
      **okutulmamış bir jetonu okutulmuş gibi göstermek** olurdu — okutma
      kaydı `BoardingScans`'te ayrı duruyor ve panel ikisini yan yana
      gösteriyor. Denetim kaydı uydurulmaz.

      Bunun yerine `22-binilmis-karekod.py` akışın tamamını gerçek uçlardan
      geçiriyor: rezervasyon → ödeme → belge → okutma. Veritabanındaki
      şifreli jeton, gerçekten okutulmuş olanın ta kendisi.

      Kanıt: `2ddb93c` · `6UGJC9S4` · **uçtan** okundu
      (`GET /api/platform/reservations/6UGJC9S4`): `token` dolu,
      `isUsable` true, okutan "Mavi Yolculuk Kaptan" · ödemeden SONRA
      sayılan bilet 1 — kendiliğinden üretim canlı yolda da kanıtlandı,
      yalnız testte değil

      🔴 **MERT'TE:** biniş penceresi kapanmış, binilmiş bir rezervasyonda
      ekran ne göstermeli? Öneri: karekod değil, "biniş yapıldı · tarih ·
      kim okuttu". Kullanılmış karekodun tekrar gösterilecek işlevi yok.

- [x] **A-131** Sefer kaydırılırken kalkış tarihi de kayıyor · bitti: 2026-09-07

      `demo-veri.sh`'nin `dilim_yerlestir`'i iade dilimlerini kurmak için
      seferi `now()`'a göre kaydırıyor ama yalnız `StartsAt`/`EndsAt`'i
      güncelliyordu. **68 seferin 4'ünde** iki alan farklı GÜN söylüyordu —
      panel 5 Kasım, sistem 1 Eylül.

      Kusurun sessiz kalma sebebi, iki alanın **farklı yerlerde okunması**:
      ekranlar `DepartureDate` gösteriyor, biniş penceresi ve iade dilimleri
      `StartsAt`'ten hesaplanıyor. İkisi de kendi içinde tutarlı göründüğü
      için hiçbir ekran şikâyet etmedi; ancak bilet üretilmeye çalışıldığında
      "bu turun biniş penceresi kapandı" diye ortaya çıktı.

      Onarım yönü **ölçülerek** seçildi: kaydırmayı yapan alan `StartsAt`,
      `DepartureDate` dokunulmadan kalan taraftı — bu yüzden 4 satır
      `StartsAt`'e göre düzeltildi, tersi değil.

      Kanıt: `b65bfb1` · tutarsız sefer 4 → 0 · `dotnet test` 694/694

- [x] **A-130** Sorgu parametreleri belgede küçük harfle başlıyor · bitti: 2026-09-07

      Belge `?Page=2` yazıyordu, sunucu `?page=2`'yi de kabul ediyordu —
      ASP.NET sorgu bağlaması büyük/küçük harfe duyarsız (ölçüldü). Yani
      belge yanlış olanı söylüyor ama hiçbir istemci patlamıyordu; sözleşme
      sessizce yalan söylüyordu.

      Dönüştürücü yalnız `in: query` olanlara dokunuyor. **Yol parametreleri
      bilerek dışarıda:** `{id}` şablonuyla birebir eşleşmek zorundalar,
      orada küçültme belgeyi bozardı.

      Kanıt: `b77fa54` · büyük harfle başlayan sorgu parametresi 25 → 0 ·
      16 yol parametresinin tamamı hâlâ şablonuyla eşleşiyor

- [x] **A-129** Ödeme tamamlanınca biniş karekodu kendiliğinden üretiliyor · bitti: 2026-09-07

      Mert: *"müşteri rezervasyonunu yapıp ödemeyi yaptığında otomatik
      olarak QR'da oluşacak."* Önce karekod ayrı bir çağrı istiyordu;
      ödenmiş rezervasyonun yanında gösterilecek bir şey yoktu.

      `PostPaymentAsync` sonrasına bağlandı. Sefer başlangıcı ve
      kullanılabilir bilet var mı — `FindTicketContextAsync` ikisini **tek
      sorguda** okuyor.

      ⚠️ **Üretim bloğu bilerek yutuluyor.** Karekod üretilemedi diye ödeme
      düşmemeli: para çekilmiş, kayıt tutulmuş durumda. Karekod sonradan
      elle de üretilebilir, ödeme üretilemez. → [[api-kararlar]]

      ⚠️ **Mutasyon, korumamın sandığım şey OLMADIĞINI gösterdi.**
      `HasUsableTicket`'i bozdum, tekrarlı geri bildirim testi yine yeşil
      kaldı — çünkü `CompleteAsync` zaten `Succeeded`'da erken dönüyor.
      Test bunu kapsıyormuş gibi değil, olduğu gibi yazıyor.

      Kanıt: `b5986bc` · ödenmiş 31 rezervasyonun **31'inde** bilet ve
      şifreli jeton var (ikinci yoldan, psql ile okundu) · `dotnet test`
      694/694

- [x] **A-128** Platform geneli rezervasyon listesi + iki listede tur türü · bitti: 2026-09-07

      Mert `BJT8F9NB` kodlu rezervasyonu panelde arayıp **bulamadı**. Sebep
      ölçüldü: ayrıntıya tek giriş noktası müşteri kartıydı ve o rezervasyon
      **misafir** rezervasyonu — müşteri kaydı yok, hiçbir yoldan
      ulaşılamıyordu. Kodu bilmek de yetmiyordu.

      `GET /api/platform/reservations?q&status&from&to&partnerId&boatId&sort&page&pageSize`

      ⚠️ **Varsayılan sıralama düz tarih sıralaması DEĞİL:** önce gelecek
      turlar en yakından uzağa, sonra geçmiş turlar en yeniden eskiye.
      Personelin sorduğu şey *"bugün ne kalkıyor"*; artan tarih sıralaması
      listenin başına yıllar önceki turları koyardı. "Son gelenler" ayrı bir
      soru ve ayrı bir seçenek (`sort=created`).

      "Bugün" Türkiye saatine göre — sunucunun saat dilimine göre
      hesaplansaydı, sunucu taşındığı gün liste sessizce kayardı.

      `rentalTypeName` iki listeye de eklendi (Mert'in isteği); ayrıntıdaki
      alanla AYNI kaynaktan.

      Kanıt: **692 test yeşil** · 4 yeni test · **iki mutasyon iki doğru
      kırmızı** (düz tarih sıralaması · misafirleri süz) · canlı: 51
      rezervasyon, sıralama 26 Eylül'den başlıyor, `q=BJT8F9NB` misafir
      rezervasyonunu buluyor (`userId: null`), durum/tarih süzgeçleri,
      tanınmayan sıralama 400, kimliksiz 401
      ⚠️ Testlerimden biri tek başına yeşil, TAM TAKIMDA kırmızı verdi:
      süzgeçsiz sorulan liste paylaşılan veritabanında ilk sayfaya
      düşmüyordu — `A-115`'teki tuzağın aynısı, ikinci kez

- [x] **A-127** Biniş jetonu şifreli saklanıyor, panel mevcut karekodu gösteriyor · bitti: 2026-09-07

      ⚠️ **Bilinerek verilmiş bir güvenlik ödünü.** Mert üç seçenek arasından
      C'yi seçti (jetonu sakla), riski yazılı olarak önündeyken. Gerekçe ve
      sınırlar → [[api-kararlar]] 2026-09-07

      Maliyeti düşüren üç şey: AES-GCM ile şifreli saklama (anahtar
      veritabanının DIŞINDA) · uygulama anahtarsız açılmıyor · her
      görüntüleme olay günlüğüne yazılıyor.

      Kanıt: **688 test yeşil** · 7 şifreleme testi (gidiş-dönüş · her
      seferinde farklı çıktı · yanlış anahtar `null` · kurcalanmış metin
      reddediliyor · bozuk girdi) · canlı uçtan uca: müşteriye verilen jeton
      ile panelde görünen **AYNI**, veritabanında düz metin **YOK**,
      `boarding.ticket.viewed` günlüğe yazıldı, eski bilette `token: null`
      ⚠️ Üretim kapıları testi ilk koşuda kırmızı verdi: yeni anahtar kapısı
      diğer kapılardan ÖNCE ateşliyor ve test ölçmek istediklerine hiç
      ulaşamıyordu — kapı sırası da ölçülmesi gereken bir şeymiş

- [x] **A-126** Demo betikleri sabit damgadan kurtuldu, boş tablolar doldu · bitti: 2026-09-07

      Sekiz betik `DAMGA = "1788556570"` diye sabit bir zaman damgasına göre
      hesap arıyordu. Veritabanı sıfırlanınca damga yok oldu ve **sekizi
      birden hiçbir şey yapmadan bitti** — hata vermeden, "0 ekstra eklendi"
      deyip.

      **Ders:** boş sonuç dönen sorgu, hata veren sorgudan tehlikeli — biri
      durur, diğeri başarıyla yanlış üretir. Sonucu panelin yarısının boş
      görünmesiydi ve o boşluk bugün dört kez kusur gizledi.

      `ortak.py` yapısal çözücüler kazandı: `demo_hesaplar` (bir işletmenin
      üyesi olan demo kullanıcı) · `demo_platform` (platform rolü bağlı) ·
      `demo_musteriler` (ne üye ne personel). Sonuç dönmezse betik açıkça
      duruyor.

      Kanıt: gerçek sayımla — 32 ekstra · 26 rezervasyon-ekstra · 18
      işletme belgesi · 24 tekne belgesi · 8 konuşma · 24 mesaj · 8 teklif ·
      5 blog · 4 kupon · 6 favori · 2 alıcı hesabı · 1 biniş bileti · 2
      okutma · 51 rezervasyon · 68 sefer · 33 ödeme · 132 defter satırı

      ⚠️ **`pg_stat_user_tables` BAYAT olabiliyor:** kuponlar yazıldığı hâlde
      `n_live_tup` 0 gösterdi ve bir an "betik çalışmadı" sandım. Tablo
      doluluğu ölçerken gerçek `count(*)` kullanılmalı — istatistik tablosu
      tahmindir.
      Bugün üçüncü kez aynı aile: **ölçüm aracının ne ölçtüğünü sormadan
      sayıya güvenmek.**

      Hâlâ boş olanlar ve sebepleri: `Passengers` (yolcu listesi isteyen
      tekne yok) · `Notifications` (giden kutusu gönderim işiyle boşalıyor) ·
      `CouponAssignments` (kuponlar herkese açık) · `ReviewReplies` (işletme
      hiç cevap yazmadı) · `CalendarModeRules` (o ekran hiç kullanılmadı).
      Bunlar "veri yok" değil **"o akış hiç çalışmadı"** demek

- [x] **A-125** Rezervasyon ayrıntısı: tur türü, biniş belgesi, geçişi yapan · bitti: 2026-09-07

      Mert ekrana bakıp üç eksik bildirdi.

      `rentalTypeName` + `pricingStrategy` — şemada `rental` geçen tek bir
      alan yoktu, panel "tur türü" satırını basacak veri bulamıyordu.

      `history[].changedByName` — Mert: *"Durum geçmişinde QR'ı kimin
      okuttuğu yazılmıyor, o da yazmalı."* `ChangedByUserId` zaten
      yazılıyordu, yalnız izdüşümde yoktu. Boş bırakılabilir ve **boşluğu
      bir BİLGİ**: tutma süresi dolduğu için düşen geçişleri kimse
      yapmamıştır; "sistem" yazmak geçişi bir kişiye bağlıymış gibi
      gösterirdi.

      ⚠️ **`A-119` kapandı ama istenen cevapla DEĞİL.** Salt okunur biniş
      belgesi ucu **yazılamaz**: veritabanında jetonun yalnız SHA-256 özeti
      duruyor, düz metni hiçbir yerde saklanmıyor. "Mevcut belgeyi üretmeden
      okuyan uç" için okunacak bir düz metin yok. Bu eksiklik değil tasarım —
      özet saklamak, veritabanını ele geçiren birinin geçerli bilet
      üretememesi demek.
      Yerine belgenin DURUMU dönüyor (`issuedAt · expiresAt · revokedAt ·
      isUsable`) ve okutma denemeleri. **Başarısız denemeler asıl değerli
      olan:** başarılı okutma zaten durum geçmişinde var, iskelede
      çalışmayan bir karekodun sebebi yalnız orada yazılı.

      **Demo betiklerinde sessiz boş geçiş bulundu:** sekiz betik
      `DAMGA = "1788556570"` diye sabit bir damgaya göre hesap arıyordu.
      Veritabanı sıfırlanınca damga yok oldu ve sekizi birden **hiçbir şey
      yapmadan** bitti — hata vermeden, "0 ekstra eklendi" deyip. `ortak.py`
      yapısal çözücüler kazandı (`demo_hesaplar`, `demo_platform`,
      `demo_musteriler`).
      **Ders:** boş sonuç dönen sorgu, hata veren sorgudan tehlikeli — biri
      durur, diğeri başarıyla yanlış üretir.

      Kanıt: **681 test yeşil** · canlı uçtan uca: 32 ek hizmet → 13
      ekstralı rezervasyon → ödeme → biniş belgesi → **karekod gerçekten
      okutuldu** → ayrıntıda `Boarded · QR okutuldu · Akdeniz Mavi Tur
      Kaptan` ve iki satırlık ekstra dökümü · mutasyon (geçişi yapan boş
      dönsün) doğru testi kırdı

- [x] **A-124** Tam sayılar da telde göründüğü gibi bildiriliyor · bitti: 2026-09-07

      `A-123` altı alanı düzeltti, **242'sini bıraktı**. Web oturumu ölçtü:
      215 şema alanı + 27 sorgu parametresi hâlâ `integer|string` taşıyordu.

      ⚠️ **KUSUR TESTİMDEYDİ.** `A-123`'te yazdığım test yalnız `number` +
      `string` arıyordu ve yalnız `components.schemas` içine bakıyordu.
      Yeşil verdi, belge doğru göründü.

      **Koruma vardı, kapsamı yanlıştı** — bu oturumda başkalarında
      defalarca bulduğum kusurun, kendi testimdeki hâli. Ders:
      *bir testin yeşil olması, ölçmesi gerekeni ölçtüğünü göstermiyor.*

      Gerekçe tam sayıda daha güçlüymüş: kayan noktada metin seçeneğinin bir
      mazereti vardı (`NaN`, `Infinity`), tam sayıda o mazeret HİÇ YOK. Yani
      en zayıf gerekçeli olanlar en son düzeltildi.

      Test artık hem `number` hem `integer` arıyor, hem şema alanlarına hem
      PARAMETRELERE bakıyor, artık kalan `pattern` kalıplarını da yakalıyor.

      Kanıt: `integer|string` **215 → 0** · sorgu parametresi **27 → 0** ·
      artık kalıp **0** · **680 test yeşil** · mutasyon (tam sayılar kapsam
      dışı) 242 ihlali adıyla sayarak kırmızı verdi

- [x] **A-123** Belge sayıları telde göründüğü gibi bildiriyor · bitti: 2026-09-07

      `A-121`'in ikizi. Çerçeve `decimal` için `["number","string"]`,
      `double` için de aynısını üretiyordu. Metin biçimi bu uygulamada
      **hiçbir yönde** kullanılmıyor — üç yönden ölçüldü:
      çıkışta her tutar JSON sayısı · girişte metin `400` alıyor
      (`AllowReadingFromString` kapalı) · `NaN`/`Infinity` üretilemiyor
      (`AllowNamedFloatingPointLiterals` kapalı).

      Bedeli: belgeden tip üreten taraf her tutarı `number | string` görüyor
      ve o birleşim koda yayılıyor. **Web'in elle tip yazma gerekçelerinden
      üçüncüsü ve sonuncusu buydu; üçü de bugün düştü.**

      Boş bırakılabilirlik KORUNDU (`decimal?` hâlâ `null` alıyor) — onu da
      kaldırmak, gerçekten var olan bir hâli belgeden silmek olurdu.

      Kanıt: `number|string` taşıyan alan **6 → 0** · **680 test yeşil** ·
      yeni test BÜTÜN şemaları tarıyor (örnekleme yapan test yeni alanı
      kaçırırdı) · mutasyon altı alanı adıyla sayarak kırmızı verdi
      ⚠️ **İlk mutasyonum yanlıştı:** koşulu daraltacağım derken her şeyi
      kapsar hâle getirdim, test haklı olarak yeşil kaldı. Mutasyonun kendisi
      de ölçülmek zorunda — yanlış mutasyon, testin değil mutasyonun zayıf
      olduğunu gösterir

- [x] **A-122** Belgedeki enum değerleri kodla karşılaştırılıyor · bitti: 2026-09-07

      `A-121` belgeyi düzeltti ama bir boşluk bıraktı ve web oturumu tarif
      etti: *"kapı belge ile kod arasını tutuyor, enum ile belge arasını
      değil."*

      Mevcut testler yeni bir **uç** eklendiğinde belgenin bayatladığını
      söylüyor. Var olan bir numaralandırmaya yeni bir **değer** eklemek ise
      hiçbir uç eklemiyor — belge bayatlıyor, hiçbir test konuşmuyordu.

      Bedeli somut: cephe çeviri tablolarını belgeden üretilen birleşim
      tipine karşı sınıyor. Belge eskiyse yeni değer tabloya girmez, derleme
      kırılmaz ve o değer ekranda ham İngilizce basılır — bugün üç kez
      yaşandı (`Inactive`, `ExclusiveOpen`, `NotYours`).

      **Testin kendi kapsamı da ölçüldü:** ilk yazımda çerçevenin `DayOfWeek`
      numaralandırmasını "kodda yok" diye bildirdi — kodu değil kendi
      kapsamını yakaladı.

      Kanıt: **679 test yeşil** · mutasyon: `ReviewStatus`'e `Flagged`
      eklenip belge üretilmeyince test doğru mesajla kırmızı verdi

      **Zincirin bugünkü hâli** — üç halka, ikisi otomatik:
      enum → belge (benim testim) · belge → tip (cephenin `tip-uret`'i, elle)
      · tip → sözlük (cephenin `satisfies` kapısı, derlemede)

- [x] **A-121** Belge numaralandırmaları telde göründüğü gibi bildiriliyor · bitti: 2026-09-07

      **Belge YALAN söylüyordu.** Uygulama `JsonStringEnumConverter`
      kullanıyor, telde `"status":"Paid"` gidiyor; belge ise aynı alan için
      `{"type":"integer"}` yazıyordu. Dönüştürücü serileştirmeye uygulanıyor
      ama belgeye yansımıyordu.

      Kusuru **web oturumu buldu** ve benim yanlış bir önerimi ölçerek
      buldu: "enum'ları belgeden üret" demiştim, ölçtü, belgede `enum`
      dizisi taşıyan şema sayısının **sıfır** olduğunu gösterdi.

      İki somut bedeli vardı:
      1. Web belgeden tip üretince `ReservationStatus: number` çıkıyordu —
         telde HİÇBİR ZAMAN görülmeyen bir tip. Cephe elle yazdığı `string`
         tiplerle örtmek zorundaydı; **belge yanlış olduğu için elle yazma
         zorunluydu.**
      2. Değerlerin varlığı hiçbir yerde yazılı değildi. Cephe çeviri
         tablolarını elle yazıyor ve aynı gün İKİ KEZ aynı kusuru yaşadı —
         biri var olmayan anahtar (`Confirmed`), diğeri eksik anahtarlar
         (`Paid`, `Boarded`).

      `EnumSchemaTransformer` yazıldı; değerler `Enum.GetNames`'ten okunuyor,
      elle yazılmıyor — elle yazılan liste yeni değer eklendiği gün sessizce
      eksik kalırdı, yani düzeltilen kusurun aynısı.

      Kanıt: enum dizisi taşıyan şema **0 → 29** · `ReservationStatus` artık
      yedi değeriyle `"type":"string"` · **678 test yeşil** · yeni test hem
      TÜRÜ hem DEĞERLERİ ölçüyor (yalnız tür ölçülseydi boş dizi de geçerdi)
      · mutasyon (`integer`'a geri al) doğru testi kırdı
      -> [[api-kararlar]] 2026-09-07

- [x] **A-120** Yorum satırı tekne adresini, kapağını ve moderatörünü taşıyor · bitti: 2026-09-07

      Mert: *"Yorum onaylanma tarihi, Yorumu onaylayan Personel vs onlarda
      olsun."*

      `boatSlug` kimlik YERİNE değil yanında: herkese açık tekne sayfası
      `/boats/{slug}` ile açılıyor, kimlikle bağlantı kurulamıyor — alan
      olmadan ekran adı basıyor ama tıklanamıyordu. `moderatedByName` ad
      taşıyor, kimlik değil. `boatCoverUrl` genel bakıştaki desenin aynısı.

      **Cephenin şüphesi ölçüldü ve eşleşme DOĞRU çıktı:** destek listesi de
      müşteri alt ucu da `SupportTickets.UserId` okuyor. Sekmenin boş
      görünmesinin sebebi eşleşme değil veri yokluğuydu — `20-destek-talepleri.py`
      ile üç talep açıldı, durumları GERÇEK personel eylemleriyle ilerledi.

      Kanıt: **677 test yeşil** · canlı: destek sekmesi 3 talep
      (Open/Answered/Resolved · mesaj 1/4/2), `status=Resolved` → 1, yorum
      satırı slug + kapak + moderatör adı taşıyor
      ⚠️ Mesaj sayısı İÇ NOTLARI da sayıyor; personel listesi için doğru olan
      bu, müşterinin kendi ekranındaki sayıdan farklı olması normal

- [x] **A-118** Müşteri ayrıntısı: dönem sayaçları, üç alt liste, rezervasyon ayrıntısı · bitti: 2026-09-07

      Mert: *"bu sayede ben bir müşterimin durumunu da ön görebilirim. Diğer
      zamanlarda ne yapmış ne etmiş gibi gibi."*

      Beş uç: ayrıntı `?period=`, rezervasyon/yorum/destek alt listeleri
      (sayfalı + süzgeçli), `GET /api/platform/reservations/{code}`.

      ⚠️ **Rezervasyon listesi ayrıntı gövdesinden ÇIKARILDI.** Gömülü
      kaldığı sürece aynı veri iki yoldan gelirdi: gövdedeki sınırsız ve
      süzgeçsiz, uçtan gelen sayfalı ve süzgeçli. İkisi bir gün ayrışır ve
      hangisinin doğru olduğu sorulamazdı.

      ⚠️ **Dönem sayaçları künyedekilerden AYRI AD taşıyor:** `customer.*`
      hayat boyu, `stats.*` seçilen dönem. Aynı ada iki anlam yüklenseydi
      okuyanın hangi sayıya baktığı ekrandan ekrana değişirdi.

      **Canlı ölçümde kusur bulundu ve düzeltildi:** `period=all` için
      "önceki dönem" HAYAT BOYU toplamı döndürüyordu — depoda boş sınır
      "süzme yok" demek, "boş aralık" değil. Ekran "geçen döneme göre %0
      değişim" yazacaktı. Sorgu artık hiç çalıştırılmıyor.

      **Yeni yetki `platform.reservation.read`** (migration `A109`). Mevcut
      `reservation.read` katalogda **işletmeye verilebilir**; onunla
      korunsaydı bir işletme, başka işletmelerin rezervasyonlarını komisyon
      oranıyla birlikte okuyabilirdi. `boat.write` kusurunun aynısı.

      Rezervasyon ayrıntısı müşteriye dönen tipten ayrı; yolcu kimlik
      NUMARASI çekilmiyor — "liste doldurulmuş mu" sorusuna ad ve doğum
      tarihi yetiyor.

      Kanıt: **676 test yeşil** · 6 yeni test · **iki mutasyon iki doğru
      kırmızı** (alt liste müşteri kapısı kalksın · künye sayacı döneme
      bağlansın) · canlı: dört dönem doğru, `all`'da önceki 0 / oran `null`,
      üç alt liste sayfalı, rezervasyon ayrıntısı 200 · olmayan kod 404 ·
      kimliksiz 401

- [x] **A-117** Müşteri listesi ve müşteri ayrıntısı · bitti: 2026-09-06

      `GET /api/platform/customers?q&status&page&pageSize` + `/{userId}` ·
      yetki `user.read`.

      ⚠️ **"Müşteri" tanımını Mert İKİ AŞAMADA koydu; ikincisi yürürlükte.**

      İlk hâli: *"burada sadece bizim sitemizde kayıtlı olan müşteriler yer
      alacak. İşletmeci, destek ekibi, site sahibi vesayre barınmayacak."*

      O kural temizdi ama **gerçek para harcamış birini görünmez yapıyordu**:
      tur satın almış bir işletme sahibi hiçbir listede müşteri sayılmıyordu.
      Mert görünce genişletti:

      > (personel değil VE işletme üyesi değil) VEYA (en az bir rezervasyonu var)

      İkinci koşulla girenler `alsoRole` ile işaretli dönüyor
      (`PlatformStaff` / `PartnerMember` / boş). İkisi birden olan
      `PlatformStaff` sayılıyor.

      **Ders:** temiz bir kural, kapsamı dışında kalanı yok saydığı için
      yanlış olabiliyor. Süzgecin dışarıda bıraktığı şey, süzgece bakarak
      görülmüyor → [[api-kararlar]]

      **Canlı ölçümde ikinci bir kusur bulundu:** arama Türkçe harflere
      duyarlıydı — aynı listede `Yılmaz` dört sonuç, `Yilmaz` sıfır sonuç
      veriyordu. `unaccent` iki tarafa da uygulandı. Türkçe bir sitede arama
      kutusuna noktalı ı yazdırmak, arayana "adı doğru yaz" demektir.
      ⚠️ Bedeli biliniyor: `unaccent()` sabit sayılmadığı için süzgeç indeks
      kullanmıyor. Müşteri sayısı büyüyünce ifadeye dayalı indeks gerekir

      `birthDate` YOK — veritabanında böyle bir alan yok, tasarımda vardı.
      `lastLoginAt` VAR ve gerçek; konum bilgisi yok, uydurulmadı.

      Kanıt: **672 test yeşil** · 8 yeni test · **iki mutasyon iki doğru
      kırmızı** (işaret hep boş dönsün · rezervasyon koşulu kalksın) ·
      canlı: 33 müşteri, sayfa 1-2 çakışmıyor, `pageSize=100000` → 100'e
      kırpıldı, `status=Suspended` → 3, işaretli satır `PartnerMember`,
      personel kimliğiyle ayrıntı **404**, kimliksiz **401**,
      `Yilmaz`=`Yılmaz`=4 sonuç
      Kanıt-2: 30 müşteri daha yazıldı (`19-musteri-coklat.py`) — sayfalama
      ancak birden çok sayfa varken denenebiliyor

- [x] **A-116** Genel bakış kapak görseli + ekranın tabloları dolduruldu · bitti: 2026-09-06

      Mert: *"Adım adım gideceğiz bak mesela ben şuanda nereyi yapıyorum
      admin sayfasının Genel bakışını öyle değil mi? Ona göre buranın ilgili
      tablolarının yerlerini doldur."*

      `coverUrl` üç tekne listesine eklendi. Adres SQL'de üretilemiyor
      (`IFileStorage` bir SQL ifadesi değil): anahtar çekiliyor, adres
      bellekte üretiliyor — `PartnerBoatListItem` ile aynı desen.

      Yeni betik `18-genel-bakis.py`: rezervasyon, kullanıcı ve işletme
      kayıtlarını son on iki aya yayıyor, onaylı yorum yazıyor. Katalog
      betikleri her şeyi BUGÜNE yazıyordu; o hâlde ekran çalışıyor ama
      **çalıştığı görülemiyordu** — eğriler tek noktalı, "önceki dönem"
      sıfır, puan listesi tek satırlıktı.

      ⚠️ **Türetilmiş hiçbir sayı elle yazılmıyor:** tekne puanı ve yorum
      sayısı tetikleyiciden, ciro rezervasyon satırlarından. Elle yazılsaydı
      ekrandaki puan altındaki yorumların ortalamasını tutmayabilirdi ve bunu
      ancak elle bölen biri fark ederdi.

      Kanıt: canlı ölçüm, tutarlılık doğrulandı — ay → 47.350/3 = **15.783,33** =
      `averageBasketTry` ✓ · yıl → 455.300/32 = **14.228,12** ✓ ·
      68.295/455.300 = **%15,0** = sözleşme komisyon oranı ✓ · gün → veri
      yok, üç oran da `null` (boş hâl de canlıda görülebiliyor)
      Kanıt-2: 8 tekne · 6 işletme · 12 kullanıcı · 34 rezervasyon (32
      ödenmiş) · 22 onaylı yorum · 9 ayda veri · 664 test yeşil

      **Demo betiğinde sessiz veri kaybı bulundu ve düzeltildi:** betik
      `amenityIds` gönderiyordu, uç `amenities` bekliyor ve gövde artık
      `[{amenityId, inclusion}]` taşıyor (`A-101`). Sunucu 201 dönüyordu
      çünkü tanımadığı alanı sessizce atıyordu — **demo teknelerinin donanımı
      hiç yazılmamıştı.** `UnmappedMemberHandling` kilidi (`A-107`) olmasa
      bugün de fark edilmezdi
      ⚠️ Sözleşme şablonu adımı da psql'den `POST /api/platform/contract-templates`
      ucuna taşındı — demo verisi artık yeni ucu da sınıyor

- [x] **A-115** Yönetim panelinin genel bakış ucu · bitti: 2026-09-06

      Mert onayladı (web oturumu üzerinden), doluluk ölçütünü **kaldırdı** ve
      yerine geçen döneme göre değişim istedi.

      `GET /api/platform/overview?period=day|week|month|year` — sekiz ölçüt,
      altı liste, üç aylık eğri.

      **Yeni yetki `platform.overview.read`** (migration `A108`, yalnız
      `platform.admin`, işletmeye verilemez). Katalogdaki hiçbir anahtar doğru
      değildi: ekran para (ciro, komisyon) ve kişisel veriyi (müşteri adı,
      e-posta) BİR ARADA taşıyor. `ledger.read` ile korunsaydı defteri okuyan
      müşteri e-postalarını da görürdü; `user.read` ile korunsaydı kullanıcı
      yetkisi sessizce ciroyu açardı — yetkiyi VEREN ne verdiğini bilemezdi.

      ⚠️ **`publishedBoats` STOK, dönemden etkilenmez ve etkilenemez:**
      teknenin geçmişteki durumu saklanmıyor. `newUsers`/`newPartners` akış.
      İkisi aynı kartta yan yana; ekran ayrımı yazmazsa "bu ay 342 tekne
      yayınlandı" diye okunur.

      ⚠️ **Bölen sıfırken `null`, `0` değil** — `averageBasketTry`,
      `cancellationRate`, `reservationChangeRate`. Sıfır bir ölçüm iddiası:
      "ortalama sepet sıfır lira" ile "ortalamalanacak satış yok" farklı
      şeyler. Sıfırdan kurulan veritabanında **ilk açılışta görülecek hâl bu**.

      Dönem sınırları Türkiye saatine göre, yarı açık aralık; hafta pazartesi
      başlıyor. UTC'ye göre kesilseydi "bugün" yerel 03:00'te başlar, sabahın
      ilk satışları önceki güne yazılırdı.

      **Doluluk oranı bilerek yok:** tanımı belirsizdi (satılan koltuk/kapasite
      mi, dolu gün/açık gün mü). Web oturumu istemedi, Mert de kaldırdı.

      Kanıt: **664 test yeşil** · 7 yeni test · **üç mutasyon üç doğru
      kırmızı** (`null`→`0` · `null`→`%100` · sınırlar UTC'de) · canlı: dört
      dönem de doğru sınır, boş veritabanında üç oran `null`, listeler `[]`,
      seri 12 nokta, tanınmayan dönem 400, kimliksiz 401
      ⚠️ Testler tek başına yeşil, TAM TAKIMDA kırmızıydı: özet sorguları
      bütün veritabanını topluyor ve takım tek Postgres konteyneri paylaşıyor.
      Ölçüm penceresi kimsenin yazmadığı bir yıla (2031) taşındı
      ⚠️ EF tuzağı ikinci kez: `Select(...).OrderBy(kayıt alanı)` SQL'e
      çevrilemiyor — sıralama izdüşümden ÖNCE (bkz. `A-110`)
      -> [[api-kararlar]] 2026-09-06

- [x] **A-111** Destek kuyruğu temsilciyi, moderasyon listesi yazarı gösteriyor · bitti: 2026-09-06

      Web oturumu bildirdi, ikisi de aynı sınıftan: **alan var ama onu
      kullanacak ekran ona ulaşamıyor.**

      Destek talebi bir temsilciye ATANABİLİYORDU (`assignedToUserId`) ama
      atandığı hiçbir listede GÖRÜLEMİYORDU — yazılabilen ama okunamayan bir
      alan. `TicketListItem` artık `requestedByUserId/Name` ve
      `assignedToUserId/Name` taşıyor.

      ⚠️ **Dördü de `staff` kapısının ardında.** Aynı sorgu müşterinin kendi
      listesini de üretiyor; kapı olmasaydı hangi temsilcinin talebine
      baktığı müşteriye açılırdı. Koşul izdüşümün İÇİNDE — dışarıda olsaydı
      iki ayrı izdüşüm doğar, birine eklenen alan diğerinde eksik kalırdı.

      Yorum moderasyon listesi yazarı göstermiyordu. Ad, herkese açık
      listeyle AYNI yardımcıdan geçiyor (`AuthorName.ForPublicDisplay`):
      ayrı kaynaklardan okunsaydı moderatörün gördüğü ad ile sitede
      yayınlanan ad ayrışabilir, moderatör onayladığı şeyi görmemiş olurdu.

      Kanıt: **657 test yeşil** · 2 yeni test · mutasyon (personel kapısı
      kaldırıldı) doğru testi kırdı · testin iki yarısı da ölçülüyor —
      yalnız "personel görüyor" ölçülseydi sızıntı yeşil testin arkasında
      kalırdı

- [x] **A-110** Kupon atama listesi kimliği taşıyor, platform kuponu kapatabiliyor · bitti: 2026-09-06

      Web oturumu bildirdi: atama listesi yalnız e-posta döndürüyor, kaldırma
      ucu kimlik istiyor (`DELETE .../assignments/{userId}`), ikisini çeviren
      uç yok. **Atama yapılabiliyor ama kaldırılamıyordu.** Düğmeyi basmayıp
      haber vermeleri doğru karardı.

      Kimlik listeye kondu (`assignedTo: [{ userId, email }]`); ucun e-posta
      kabul etmesi SEÇİLMEDİ — e-posta değişebilir, kimlik değişmez. Silme
      yolu değişebilen bir anahtara bağlansaydı, adresini değiştiren
      kullanıcının ataması kaldırılamaz olurdu.

      İkinci eksik daha ağır çıktı: `POST /api/platform/coupons/{id}/deactivate`
      yoktu. Mevcut uç işletmenin KENDİ kuponuna bakıyor, platform kuponunun
      ise `PartnerId`'si boş — yanlış yüzdeyle açılan platform kuponunu
      kapatmanın hiçbir yolu yoktu.

      Düzenleme ve geri açma uçları bilerek yazılmadı → [[api-kararlar]]

      Kanıt: **655 test yeşil** · mutasyon (listeye boş kimlik) doğru testi
      kırdı · canlı: kupon 201 → atama 204 → listeden okunan kimlikle kaldırma
      **204** → pasife alma 204 → `isActive: false` · olmayan kupon 404 ·
      kimliksiz 401
      ⚠️ EF tuzağı: `Select(...).OrderBy(kayıt alanı)` SQL'e çevrilemiyor,
      sıralama izdüşümden ÖNCE yazılmalı — test çalışma anında yakaladı

- [x] **A-109** Sözleşme şablonu panelden yaratılıp düzenleniyor · bitti: 2026-09-06

      Mert: *"Sözleşme oluşturma şablonunu da yap o zaman hadi"* — sıfırdan
      test kurulumu için veritabanı silinecekti ve **şablon yaratan uç yoktu**;
      metin yalnız doğrudan SQL ile yazılabiliyordu. Temiz bir kurulumda
      platform hiçbir işletmeye sözleşme gönderemiyor, tekne eklemek onaylı
      sözleşmeye bağlı olduğu için sistem baştan tıkalı kalıyordu.

      `POST` + `PUT /api/platform/contract-templates` · yetki `contract.write`
      · liste `?includeInactive=true` ile katalogu da veriyor.

      ⚠️ **Yetki `contract.send` DEĞİL.** Hazır metinden sözleşme göndermek
      ile metnin kendisini yazmak aynı ağırlıkta iş değil. Test bunu
      katalogdaki bir role dayanmadan ölçüyor: yalnız `contract.send` taşıyan
      bir rol kurup şablon yazmayı deniyor, `403` alıyor.

      ⚠️ **Metin değişirse sürüm artar, ad/yürürlük değişirse artmaz.**
      Gönderilmiş her sözleşme `TemplateVersion` saklıyor; numara artmadan
      metin değişseydi aynı (şablon, sürüm) çiftinin altında iki farklı metin
      bulunur ve o kayıt hangi metnin onaylandığını söylemekten çıkardı.

      ⚠️ **Şablon silinmiyor, pasife alınıyor** — silmek gönderilmiş
      sözleşmelerin künyesindeki bağı koparırdı.

      **İlk yazımda güncelleme HİÇ KAYDEDİLMİYORDU:** mevcut bulucu
      `AsNoTracking` + `IsActive` süzgeci taşıyordu (gönderme yolunun doğru
      davranışı). Uç `200` dönüyor, gövde yeni değerleri gösteriyor,
      veritabanı eskide kalıyordu. Sürüm testi CEVABA baktığı için yeşildi;
      pasife alma testi GERİ OKUDUĞU için kırmızı verdi. Düzenleme için ayrı
      bir bulucu yazıldı, sürüm testi de geri okumaya çevrildi.

      Kanıt: **652 test yeşil** · 10 yeni test · **üç mutasyon üç doğru
      kırmızı** (yetki `contract.send`'e düşürüldü → yetki testi · sürüm hiç
      artmasın → sürüm testi · bulucu yine izlemesiz → iki test)
      -> [[api-kararlar]] 2026-09-06

- [x] **A-108** Rezervasyon formunda dalışçı sayısı · bitti: 2026-09-06

      Mert (2026-09-06): *"rezervasyon formunu da değiştir, dalışçı sayısı
      sorulsun"*

      `Reservations.DiverCount` · `Voyages.SoldDivers` + `DiverCapacity` ·
      migration `A107_RezervasyonDaliscSayisi`.

      ⚠️ **Dalışçı yolcuların ALT KÜMESİ, ek yolcu değil.** Ayrı sayılsaydı
      kapasite iki kez sayılır, tekne dolmadan dolu görünürdü. Kısıt:
      `DiverCount <= AdultCount + ChildCount` (bebek dalmaz, koltuk da tutmaz).

      ⚠️ **Kontenjan SEFERİN TAMAMI için denetleniyor, istek başına değil.**
      `dalis-turu` paylaşımlı (`PerPerson`): beş ayrı rezervasyon sekizer
      dalışçı yazsaydı her biri tek başına sınırın altında kalır, tekne kırk
      dalışçıyla kalkardı. Sayacı `sync_voyage_sold_seats()` tetikleyicisi
      tutuyor — `SoldSeats` ile AYNI işlevin içinde, çünkü iki sayaç iki ayrı
      yerden güncellenseydi birini unutan ilk kod yolu ikisini kalıcı olarak
      ayrıştırırdı. Sınırı `CK_Voyages_SoldDivers` koyuyor.

      Kanıt: **640 test yeşil** (`tam3.trx`) · 11 yeni test
      Kanıt-2: **üç mutasyon, üçü de doğru testi kırdı** — fabrika `0` yazınca
      4 kırmızı · sefer kısıtı zayıflatılınca YALNIZ sefer testi kırmızı ·
      sayacın durum süzgecine `'Cancelled'` eklenince YALNIZ iptal testi kırmızı
      Kanıt-3: **canlı** (`:5163`) — teklif `diverCount:3` → **200**,
      `diverCount/diverCapacity` gövdede · yolcudan fazla → **400** · kontenjan
      üstü → **400** "en fazla 6 dalışçı yeri var" · dalış olmayan tur → **400**
      · rezervasyon 4 dalışçı → **201** · aynı sefere 3 daha (toplam 7 > 6) →
      **409** "kontenjan doldu" · 2 daha (toplam 6 = sınır) → **201** ·
      `Voyages.SoldDivers` = 6 (tetikleyici saydı) · müşteri kendi
      rezervasyonunu okuyunca `diverCount: 4`
      Kanıt-4: veritabanında ölçüldü — üç kısıt `convalidated = t`,
      tetikleyicinin `UPDATE OF` listesinde `DiverCount` var

      **Sızıntı testi yine iş gördü:** `QuoteResponse`'a iki alan eklenince
      `A_new_field_cannot_silently_widen_the_response` kırmızı verdi ve soruyu
      sordurdu. İkisi de EVET: `diverCount` sunucunun neyi fiyatladığının
      yankısı, `diverCapacity` ise `Capacity` ile aynı sınıfta — formun kendi
      alanını neyle sınırlayacağı.

      ⚠️ **`supportsDivers` tekne detayına eklendi ve asıl mesele bu.** Cephe
      "dalışçı sorayım mı" sorusunu `diverCapacity != null` ile cevaplasaydı,
      **kontenjanı olmayan bir dalış turu dalış yapılmayan turdan ayırt
      edilemezdi** — sınırsız dalış turunda alan hiç görünmezdi

- [x] **A-107** Tanınmayan alan taşıyan gövde reddediliyor · bitti: 2026-09-05

      `UnmappedMemberHandling = Disallow`. Varsayılan davranış tanımadığı
      alanı SESSİZCE atıyordu ve bu gerçek bir veri kaybı üretti: panel
      `amenityIds` gönderiyordu, uç `amenities` bekliyordu, sunucu **200**
      döndü ve hiçbir şey yazılmadı.

      ⚠️ Sınırı bilinerek kabul edildi: kilit İSİM uyuşmazlığını yakalar,
      TİP uyuşmazlığını yakalamaz → `A-07`

      Kanıt: **619 test yeşil**. Canlı: geçerli giriş 200, `amenityIds`
      eklenmiş aynı giriş **400** ve yanıt alan adını söylüyor. Web tarafı
      tekne düzenlemeyi canlıda ölçtü, 400 yok. Kilit açılır açılmaz
      `15-tekne-zenginlestir.py` içinde de fazlalık alan buldu (`pricingStrategy`)

- [x] **A-106** Tekne sayfasında işletme künyesi · bitti: 2026-09-05

      `PublicBoatDetail.Partner`: TÜRSAB belge no, satışa başlama günü,
      yayındaki tekne sayısı, puan, yorum sayısı. Belge YALNIZ doğrulanmışsa
      dönüyor; doğrulama `POST /api/platform/partners/{id}/tursab-verification`
      ve `PartnerApprove` izniyle. Numara değişirse damga düşüyor.
      Gerekçeler → [[api-kararlar]] 2026-09-05

      Kanıt: **617 test yeşil**. Canlı zincir: damgasızken `null` → yetkisiz
      doğrulama **401** → platform **204** → numara görünüyor → numara
      değişti → damga düştü, müşteriye yine `null`

- [x] **A-105** Olanağın fiyata dahilliği · bitti: 2026-09-05

      `BoatAmenities.Inclusion` = `OnBoard` / `Included` / `Extra`. Katalogda
      değil TEKNE BAĞINDA: aynı olanak bir teknede dahil, diğerinde ücretli.
      `SaveBoatRequest.AmenityIds` → `Amenities` (atama listesi).

      Kanıt: **615 test yeşil**. Aynı olanak iki teknede iki farklı değer
      dönüyor. `EnumConstraintTests` kısıtı NOT VALID bırakmamı yakaladı,
      VALIDATE eklendi

- [x] **A-104** Sezon fiyat tablosu · bitti: 2026-09-05

      `rentalTypes[].seasons` — tarihler HAM, etiket değil: ekran "bugün
      hangi aralıktayız" kıyasını ancak tarihle yapabiliyor. Geçmiş sezon ve
      temel fiyat listeye girmiyor.

      ⚠️ Ölçüldü: `rentalTypes[].adultPrice` TEMEL fiyattır, bugünün sezon
      fiyatı değil — ve bu tutarlılık, çünkü arama da tarihsiz sorgulandığında
      temel fiyatı döndürüyor

      Kanıt: **614 test yeşil**. Canlı üç sezon dönüyor, biri bugünü kapsıyor

- [x] **A-103** Tekne detayı künye alanları · bitti: 2026-09-05

      `boatTypeName`, `regionName`, `widthMeters` eklendi; aramaya da
      `regionName`. Üçü de veritabanında vardı, izdüşümde yoktu.

      Kanıt: **612 test yeşil**. Canlı: `Gulet` · `Fethiye` · `6.4`

- [x] **A-102** Fiyat teklifi çarpanı döndürüyor · bitti: 2026-09-05

      `Quote.BilledDays` + `QuoteResponse.BilledDays`. `boatPrice` GÜNLÜK
      bedel; çarpan dönmediği için ekran "42.000 / 126.000" diye çelişik
      görünüyordu. Alan adı değiştirilmedi — yayınlanmış sözleşmede ve
      rezervasyon kaydında duruyor.

      ⚠️ İlk denemede alan yalnız İÇ nesneye eklendi, tel sözleşmesine
      geçmedi ve `openapi.json`'da hiç görünmedi. Web yakaladı

      Kanıt: **613 test yeşil**, mutasyon kırmızı. Canlı: `42000 × 3 = 126000`

- [x] **A-101** Platform sözleşme listesi ret gerekçesini döndürüyor · bitti: 2026-09-05

      Gerekçe işletme ucunda dönüyor, platform ucunda dönmüyordu — yani
      zorunlu tutulan bir metin hiç kimseye gösterilmiyordu.

      Kanıt: **611 test yeşil**, mutasyon kırmızı. Canlı platform ucu
      `Rejected | 2026-09-05T02:13:21 | canım istedi kardeşş` döndürdü,
      yetkisiz aynı istek **401**

- [x] **A-88** Kuponlar — üç tür · bitti: 2026-09-05
  Kanıt: `AYSEYE20` canlı → Ayşe `indirim 580`, Can `0 + "size tanımlı değil"`,
  kimliksiz `0 + aynı mesaj`. Herkese açık `/api/coupons` listesinde yalnız
  `YAZ2026`, `AYSEYE20` yok. İki mutasyon kırmızı verdi (tanım denetimi 1,
  son tanımda pasife alma 1). 581 test yeşil. → [[api-kararlar]] 2026-09-05 (4)
- [x] **A-89** İşletme kendi kuponunu açabiliyor · bitti: 2026-09-05
  Kanıt: `coupon.read`/`coupon.write` → `IsPartnerAssignable = t`, `coupon.write`
  tutan rol sayısı 20 (migration `A89_IsletmeKuponYetkisi`). `api/partner/coupons`
  canlı: `POST` → `201`, kendi listesinde `bedel=Partner listelenen=False`;
  `/api/coupons` herkese açık listesinde `MAVI10` yok. Üç mutasyon da kırmızı
  verdi (`FundedBy`→`Platform` 2, tekne sahipliği 1, pasife alma kapsamı 1).
  586 test yeşil. → [[api-kararlar]] 2026-09-05 (5)
- [x] **A-90** Gövdedeki tarihler UTC'ye çevriliyor, saat dilimsiz reddediliyor · bitti: 2026-09-05
  Kanıt: `+03:00` → `201` + DB'de `2026-09-06 21:00 UTC`; `"2026-09-07"` → `400`
  (eskiden `500`) + `$.validFrom` mesajı. Üç mutasyon da kırmızı verdi
  (`ToUniversalTime()` 1, saat dilimi şartı 1, kayıt kaldırma 2). 589 test yeşil.
  → [[api-kararlar]] 2026-09-05 (7)
- [x] **A-91** Tekne donanım/kural verisi ve müşteriye açık detay testi · bitti: 2026-09-05
  Kanıt: sekiz demo teknesine ayrışan donanım atandı; arama 8 → klima 6 →
  şnorkel 4 → mikrofon 1, `klima+şnorkel` 3. Detay 7 donanım + 3 kuralı
  çeviriyle döndürdü. İki mutasyon kırmızı (donanım listesi boşaltıldı,
  `IsAllowed` sabitlendi). `demo-veri.sh` artık atamayı da kuruyor.
  → [[api-kararlar]] 2026-09-05 (8)
- [x] **A-07b** Yanıt şemaları — 146 eylemin tamamı işaretlendi · bitti: 2026-09-05
  Kanıt: şema taşıyan operasyon 0 → 145/146, bileşen şeması 0 → 181, bildirilen
  kodlar `{200:146}` → `{200:88, 201:16, 204:42, 301:1, 400:120, 401:120,
  403:91, 404:85, 409:3}`. Yedi uçta şema alanları canlı gövdeyle birebir;
  kimliksiz yedi uçta yanlış `401` iddiası olmadığı ayrıca ölçüldü. Denetim
  testi yazıldığı anda beş gerçek boşluk buldu (dört ikili indirme + rezervasyon
  `201`). 591 test yeşil. → [[api-kararlar]] 2026-09-05 (9)
- [x] **A-95** Paratika ödeme sağlayıcısı yazıldı · bitti: 2026-09-05
  Kanıt: 7 test, beş mutasyon da kırmızı verdi (bölüştürme, doğrulanamayan
  cevap, tutar denetimi, vergi kimliği alanı, kültür). Açılış kapısı üretimde
  dört durumda ölçüldü: kimlik yok / API adresi deneme / ödeme sayfası deneme
  → üçü de reddetti, hepsi üretim → açıldı. 600 test yeşil.
  → [[api-kararlar]] 2026-09-05 (13)
- [x] **A-96** Depolama Amazon S3'e sabitlendi · bitti: 2026-09-05
  Kanıt: kod zaten gerçek AWS'ye bakıyordu; tek düzeltme `ForcePathStyle`
  yalnız `ServiceUrl` doluyken (AWS dışı) açık. 600 test yeşil, MinIO'ya
  koşan depolama testleri etkilenmedi. → [[api-kararlar]] 2026-09-05 (14)
- [x] **A-97** İşletmenin ilçesi ayrı alan · bitti: 2026-09-05
  Kanıt: migration `dailycruising` rolüyle uygulandı, uygulama rolünün yeni
  kolonda SELECT/UPDATE yetkisi kolon bazında doğrulandı. Canlı: başvuru
  `Muğla/Bodrum` yazdı, profil ucu döndürdü ve `PUT` ile değiştirildi.
  600 test yeşil. → [[api-kararlar]] 2026-09-05 (15)
- [x] **A-98** Paratika açılış kapıları testle bağlandı · bitti: 2026-09-05
  Kanıt: iki mutasyon kırmızı verdi (kimlik kapısı, ödeme sayfası adresi).
  Zincirin `Assert.Contains("")` yazan son adımı gerçek mesaja bağlandı.
  `ForcePathStyle` testi bilerek YAZILMADI — yazılanı ifadeyi kopyalıyordu.
  600 test yeşil. → [[api-kararlar]] 2026-09-05 (17)
- [x] **A-99** İşletme kendi sözleşmesini görüp kabul ediyor · bitti: 2026-09-05
  Kanıt: canlı akış — sözleşme listesi 200, panel 403, yanlış parola 400,
  başkasının sözleşmesi 404, doğru parola 204 → Active, dört delil alanı dolu,
  panel 200. Dört mutasyon da kırmızı verdi. 605 test yeşil.
  → [[api-kararlar]] 2026-09-05 (18)
- [x] **A-100** Sözleşme reddi · bitti: 2026-09-05
  Kanıt: pazarlık döngüsünün tamamı canlı ölçüldü — gerekçesiz ret 400,
  gerekçeli ret 204 (işletme ContractSent kaldı), reddedileni kabul 404,
  düzeltilmiş sözleşme 201, kabul 204 → Active, panel 200. Üç mutasyon da
  kırmızı verdi. Kural veritabanında da var (`CK_Contracts_RejectedEvidence`).
  609 test yeşil. → [[api-kararlar]] 2026-09-05 (19)
- [x] **A-92** Bütün tablolar gösterilebilir veriyle dolduruldu · bitti: 2026-09-05
  Kanıt: 82 tablonun 81'i dolu; tek boş kalan `NotificationOutbox` ve o bir
  kuyruk (gönderim işi boşaltıyor). Dört rolde canlı uç taraması yapıldı;
  sekiz teknenin sekizinde de puan var. Betikler `araclar/demo-doldur/`.
  → [[api-kararlar]] 2026-09-05 (10)
- [x] **A-93** Ekstralı teklif kabulü düzeltildi · bitti: 2026-09-05
  Kanıt: `An_offer_with_extras_can_be_accepted` üç tutarı ayrı ölçüyor;
  eski hesaba mutasyon kırmızı verdi. Canlı: 4 kabul, `OfferItems` 0 → 16.
  → [[api-kararlar]] 2026-09-05 (11)
- [x] **A-94** Konuşma rezervasyona bağlanıyor, kapatma işi çalışır oldu · bitti: 2026-09-05
  Kanıt: test bağın varlığını değil işin konuşmayı kapatmasını ölçüyor;
  çağrı kaldırılınca kırmızı. Canlı: `ConversationReservations` 0 → 4.
  593 test yeşil. → [[api-kararlar]] 2026-09-05 (12)

      `CouponAssignments` tablosu + `Coupons.IsPubliclyListed` / `Title`.
      Uçlar: `GET /api/coupons` (kimliksiz kampanyalar) ·
      `GET /api/coupons/mine` (tanımlı + kullanılan) ·
      `GET/POST /api/platform/coupons` · `POST/DELETE .../assignments`.
      Gerekçeler → [[api-kararlar]] 2026-09-05 (4)

      **Tanım fiyat hesabında UYGULANIYOR** — `CouponRejection.NotYours`.
      `QuoteAsync` artık çağıranın kimliğini alıyor (36 çağrı yeri).

      Kanıt: **581 test yeşil** (6'sı yeni). İki mutasyon, ikisi de yakalandı.
      Kanıt: canlı — `AYSEYE20` Ayşe'de `indirim 580`, Can'da `0 + "size
      tanımlı değil"`, kimliksizde aynı ret. Herkese açık listede yalnız
      `YAZ2026`.
      Kanıt: `coupon.read`/`coupon.write` ilk kez bir uç tarafından
      kullanılıyor — 12 gündür tanımlı ve boştular.

      ⚠️ **Açık:** işletme kendi kuponunu yönetemiyor (`coupon.write`
      işletmeye verilemiyor) ama `FundedBy = Partner` şemada var.

- [x] **A-87** Slug üretiminde noktalı `İ` kusuru · bitti: 2026-09-05

      `ToLowerInvariant()` `İ`'yi küçültmüyor; ayrıştırma onu BÜYÜK `I`'ye
      çeviriyordu. `akdeniz-incisi` **404**, `akdeniz-Incisi` 200 dönüyordu.
      Bulguyu web oturumu getirdi. Gerekçeler → [[api-kararlar]] 2026-09-05 (3)

      Kanıt: **575 test yeşil** (2'si yeni). Mutasyon **iki katman birlikte**
      kaldırılınca iki test de kırmızı — tek katman kaldırıldığında yeşil
      kalıyordu, çünkü diğer katman örtüyordu.
      Kanıt: canlı `akdeniz-incisi` `200`; eski adres `akdeniz-Incisi`
      **`301`** ile yenisine yönlendiriyor, izlenince `200` — paylaşılmış
      bağlantı kırılmadı.
      Kanıt: yeni tekne "İZMİR Ünlü Çağrı Deneme" → `izmir-unlu-cagri-deneme`.
      Kanıt: blog etkilenmiyor — kullanıcı kısa adı büyük harf içeriyorsa
      `400 InvalidSlug`, sessiz bozma yok.

      ⚠️ Yönlendirme migration'ı ilk yazımda **sessizce hiçbir şey yazmadı**:
      kaynak olarak `BoatSlugs` alınmıştı ve o tablo yalnız yeniden
      adlandırmada doluyor. Kaynak `Boats` yapıldı.

- [x] **A-86** `S-32` — KDV oranı tarihli tabloya taşındı · bitti: 2026-09-05

      `TaxRates` (`Rate`, `EffectiveFrom`, `Note`). Yürürlükteki oran
      `EffectiveFrom <= now` satırların en yenisi; `PricingContext` üzerinden
      komisyon oranıyla aynı sorgudan taşınıyor.
      `TaxOptions`, DI kaydı, `Billing:VatRate` ve 15. açılış kapısı
      **kaldırıldı**. Gerekçeler → [[api-kararlar]] 2026-09-05 (2)

      Kanıt: **573 test yeşil** (7'si KDV). Mutasyon: yürürlük tarihi şartı
      kaldırılınca kırmızı.
      Kanıt: canlı fiyat sorgusu `vatRate: 20.0`; tabloda tek satır,
      `2000-01-01`'den geçerli, notu "devralınan oran".
      Kanıt: tablo sahibi `dailycruising`, `EffectiveFrom` benzersiz.

      ⚠️ Testim paylaşılan veritabanında **başka testin satırını taşıdı**
      (`Where(Rate == 21)`). Kimliğe çevrildi. Bu hafta ikinci kez: aynı
      hatanın ilki `A-78`'de sabit e-postaydı.

- [x] **A-85** İade önizlemesi · bitti: 2026-09-05

      `refundPreviewRate` / `refundPreviewTry` sorgulama ve liste yanıtlarına
      eklendi; hesap `RefundPolicy` içine çıkarıldı ve iptal ucu da oradan
      çağırıyor. Gerekçeler → [[api-kararlar]] 2026-09-05

      Kanıt: **571 test yeşil** (9'u yeni). Mutasyon: önizleme yanıta
      bağlanmayınca kırmızı.
      Kanıt: sınır anları ayrı ölçüldü — tam 48:00 ve tam 24:00 müşteri
      lehine üst kademede.
      Kanıt: canlı — `refundPreviewRate: 100`, `refundPreviewTry: 1500.0`,
      `cancellationRefundRate: null`. Tahmin dolu, kayıt boş.

- [x] **A-84** `S-25` — biniş bileti ucu · bitti: 2026-09-04

      `BoardingTickets` tablosu + `POST /api/reservations/{code}/boarding-ticket`.
      Asıl biniş jetonuna dokunulmuyor; okutma iki jetonu da tanıyor.
      Gerekçeler → [[api-kararlar]] 2026-09-04 (14)

      Kanıt: **561 test yeşil** (9'u yeni). İki mutasyon, ikisi de yakalandı.
      Kanıt: canlı — yanlış e-posta `400`, doğru e-posta jeton + `expiresAt`,
      ikinci bilet sonrası veritabanında **2 bilet / 1 geçerli**.
      Kanıt: tablo sahibi `dailycruising`, uygulama rolü yetkili, kısmi
      benzersiz indeks `WHERE "RevokedAt" IS NULL` olarak kuruldu.

      ⚠️ **Süre testim önce doğru sonucu YANLIŞ SEBEPTEN veriyordu** —
      okutma anı biletin bitişinden sonraydı, o anda tur da bitmişti ve
      şart koddan çıkarılınca test yeşil kalıyordu. Mutasyon yakaladı,
      kurulum tersine çevrildi ve olumlu ikizi eklendi.

- [x] **A-83** `S-31` — blog gövdesi için sunucu tarafı HTML temizleyici
      · bitti: 2026-09-04

      `IHtmlContentSanitizer` (Application) + `BlogHtmlSanitizer`
      (Infrastructure, `HtmlSanitizer` 9.2.1039). Temizleme **yazma** yolunda;
      izin listesi, yasak listesi değil.
      Gerekçeler → [[api-kararlar]] 2026-09-04 (13)

      Kanıt: **552 test yeşil** (13'ü yeni). İki mutasyon, ikisi de yakalandı:
      servis temizleyiciyi atlayınca → 1 kırmızı; kütüphanenin varsayılan izin
      listesi boşaltılmayınca → 3 kırmızı.
      Kanıt: canlı uçtan uca — gönderilen gövdedeki `script`, `onclick`,
      `javascript:` bağlantısı, `iframe` ve `style` **veritabanı satırında da
      yok**; `<h2>`, `<strong>` ve geçerli `https` bağlantısı korundu.
      Başlık `<h1>Gökova</h1> rehberi` → `Gökova rehberi`.
      Kanıt: temizlemenin YAZMA yolunda olduğu, uç yanıtından değil
      **saklanan satırdan** doğrulandı.

      ⚠️ Kütüphane hakkında iki varsayımım ölçümle çürüdü: boş izin listesi
      metni de siliyor (`KeepChildNodes` gerekti) ve başlıktaki betik gövdesi
      düz metne dönüyor. İkincisi kabul edildi ve **teste yazıldı** — yazılmasa
      bir sonraki okuyan onu hata sanıp "düzeltir" ve başlıkları kaybeder.

- [x] **A-81 + A-82** `S-28` ve `S-22` veri düzeltmeleri · bitti: 2026-09-04

      İkisi de migration olarak yazıldı — elle SQL hiçbir yerde kayıtlı olmaz.
      Gerekçeler → [[api-kararlar]] 2026-09-04 (12)

      Kanıt: uygulama **öncesi** 15 ayrışık rezervasyon · 4 `a04-` referans
      satırı · a04 teknesinin 38 rezervasyonu.
      Kanıt: uygulama **sonrası** 0 · 0 · **38** — düzeltmeler yapıldı ve
      hiçbir rezervasyon kaybolmadı.
      Kanıt: canlı aramada tip adları yalnız `Gulet`; `lookups` gövdesinde
      `a04-` geçmiyor. Ana sayfa kart rozetinde ham anahtar kalmadı.
      Kanıt: 539 test yeşil.

      ⚠️ **Mert'e sorduğum sayı 10'du, gerçek 15.** Ters yönde 5 satır daha
      vardı; soruyu tek yönü ölçerek yazmıştım.
      ⚠️ **"Temizlik" küçük bir iş değildi:** `a04-` satırlarına 38
      rezervasyon bağlıydı, önce taşındılar.

- [x] **A-80** `S-20` — KDV oranı rezervasyona donduruldu · bitti: 2026-09-04

      `Reservations.VatRate` (`numeric(5,2)`, kısıt `0..100`), `Quote`
      üzerinden akıyor, `TaxOptions` yapılandırmadan geliyor.
      Vergi TUTARI saklanmıyor — toplamdan türetiliyor (fiyat KDV dahil).
      Gerekçeler → [[api-kararlar]] 2026-09-04 (11)

      **15. açılış kapısı eklendi:** `Billing:VatRate` üretimde tanımsızsa
      uygulama açılmıyor. Kapı bildirim kapısından ÖNCE.

      Kanıt: **539 test yeşil** (5'i yeni). Dondurma satırı kaldırılarak
      mutasyon denendi → 2 kırmızı.
      Kanıt: canlı fiyat sorgusunda `vatRate: 20`, komisyon oranı sızmıyor,
      türetilen vergi `1000 × 20/120 = 166.67`.
      Kanıt: canlı rezervasyon `AZ6QSV9B` satırında `VatRate = 20.00` dondu.
      Kanıt: veritabanında `column_default` **boş** (varsayılan aynı
      migration'da düşürüldü), kısıt `convalidated = t` (`NOT VALID` +
      `VALIDATE`), 80 eski satır `20` ile dolduruldu.
      Kanıt: `A_new_field_cannot_silently_widen_the_response` testi alanı
      eklerken DURDURDU; "müşteriye gitmeli mi" sorusu cevaplanıp listeye
      yazıldı — test amacına uygun çalıştı.
      Kanıt: `openapi.json` yeniden üretildi.

      ⚠️ Oranın KAYNAĞI hâlâ yapılandırma → `S-32` açıldı. Geçiş ucuz;
      rezervasyondaki kolon her iki hâlde de aynı.

- [x] **A-79** `S-27` uygulandı — müşteri iletişim bilgisi işletmeye kapatıldı
      · bitti: 2026-09-04

      `GET /api/partner/reservations` yanıtından `contactEmail` ve
      `contactPhone` kaldırıldı; `contactFullName` kaldı.
      Gerekçe → [[api-kararlar]] 2026-09-04 (9) — sebep KVKK değil **aracıdan
      kaçış**, ve bunu Mert söyledi, biz sormamıştık.

      Kanıt: **534 test yeşil.** Alanlar geri eklenerek mutasyon denendi,
      `A_row_does_not_carry_the_customer_email_or_phone` kırmızıya döndü.
      Kanıt: test alan üzerinden DEĞİL serileştirilmiş gövde üzerinden yazıldı
      — kaldırılmış bir özelliğe başvuran test derlenmez, yani yasağı koruyan
      hiçbir şey kalmazdı.
      Kanıt: canlı yanıtta 16 alan; `contactEmail` ve `contactPhone` yok,
      gövdenin tamamında tek `@` işareti bile geçmiyor, `contactFullName` var.
      Kanıt: `openapi.json` yeniden üretildi.

- [x] **A-78** Bildirim tercihleri · bitti: 2026-09-04

      `NotificationPreferences` tablosu ve iki uç:
      `GET/PUT /api/account/notification-preferences`. Üç alan:
      `emailEnabled`, `smsEnabled`, `reviewInvitationsEnabled`.
      Gerekçeler → [[api-kararlar]] 2026-09-04 (8)

      **Tercih SADECE kaydedilmiyor, UYGULANIYOR:** `ReservationNotifier`
      onay ve iptal bildirimlerinde kanal kapısı, `SendReviewInvitationsJob`
      davet ve hatırlatmada vazgeçme kapısı. Anonimleştirme tercih satırını
      siliyor.

      Kanıt: **533 test yeşil** (11'i yeni). İki mutasyon, ikisi de yakalandı:
      kanal kapısı etkisizleştirildi → 2 kırmızı; yorum daveti kapısı
      kaldırıldı → 1 kırmızı.
      Kanıt: canlı — jetonsuz `401` · kayıt yokken varsayılan `hepsi açık` ·
      SMS+davet kapatma `200` · **iki kanalı birden kapatma `400
      NoChannelLeft`** · tekrar okuyunca kalıcı · veritabanında tek satır.
      Kanıt: **kısıt uygulamadan bağımsız ölçüldü** — `psql` ile doğrudan
      `UPDATE "NotificationPreferences" SET "EmailEnabled"=false,
      "SmsEnabled"=false` denendi, veritabanı
      `CK_NotificationPreferences_AtLeastOneChannel` ile reddetti.
      Kanıt: `openapi.json` yeniden üretildi — 108 yol, 136 operasyon.

      ⚠️ **Kendi testim diğer testleri kırdı ve bunu yazıyorum:**
      `ReservationAsync` her test rezervasyonuna AYNI sabit e-postayı
      yazıyor. Vazgeçmiş bir kullanıcıyı o adrese bağlayınca aynı
      veritabanını paylaşan `The_reminder_is_sent_once_after_seven_days`
      kırmızıya döndü — sebebi kendi kodunda değil, benim testimin yan
      etkisiydi. Test kendi adresini kullanacak şekilde düzeltildi.

- [x] **A-77** Favori tekneler · bitti: 2026-09-04

      `FavoriteBoats` tablosu ve üç uç: `GET /api/favorites` ·
      `PUT /api/favorites/{boatId}` · `DELETE /api/favorites/{boatId}`.
      Ekleme ve çıkarma idempotent, kapsam jetondan.
      Gerekçeler → [[api-kararlar]] 2026-09-04 (7)

      **Anonimleştirme genişletildi:** favoriler hesap kapatmada siliniyor ve
      sayısı olay yüküne yazılıyor (`AnonymizationCounts.Favorites`,
      `EventPayloadPolicy` → `favorites`). Yabancı anahtar CASCADE bunu
      yapmıyor — anonimleştirme kullanıcı satırını silmiyor, üzerine yazıyor.

      Kanıt: **522 test yeşil** (11'i yeni). Üç mutasyon, üçü de yakalandı:
      anonimleştirmeden silme satırı çıkarıldı → 1 kırmızı; `isAvailable`
      daima `true` yapıldı → 1 kırmızı; liste sorgusundan kullanıcı kapsamı
      çıkarıldı → 4 kırmızı.
      Kanıt: canlı — jetonsuz `GET` ve `PUT` `401` · boş liste `[]` · ilk
      `PUT` `204`, ikinci `PUT` `204` ve tek satır · liste iki kart döndü ve
      `boatTypeName` iki dalı da gösterdi (`Gulet` çevirili, `a04-gulet` ham
      anahtar) · yayında olmayan tekne `404 BoatNotFound` · **pasifleşen tekne
      listede KALDI ve `isAvailable: false` döndü** · pasif tekne
      çıkarılabildi `204`.
      Kanıt: **kapsam canlı ölçüldü** — ikinci müşterinin listesi `[]`,
      birincinin favorisini silme denemesi `204` (idempotent) ama birincinin
      listesi **hâlâ 2 kayıt**. Yalnız status koduna bakan bir ölçüm burada
      yanılırdı.
      Kanıt: migration `dailycruising` rolü adına uygulandı; tablo sahibi
      `dailycruising`, uygulama rolünde `SELECT/INSERT/DELETE` var,
      **`TRUNCATE` yok** — `A-10`'un istediği hâl.
      Kanıt: `openapi.json` yeniden üretildi — 107 yol.

- [x] **A-76** Blog uçları — herkese açık okuma, yazarlık, moderasyon, kategori
      · bitti: 2026-09-04

      Dört tablo (`BlogPosts`, `BlogPostTranslations`, `BlogCategories`,
      `BlogCategoryTranslations`) şema kurulduğundan beri BOŞTU; `blog.write` ve
      `blog.approve` yetkileri kataloğa yazılmıştı ve **hiçbir uç onları
      kullanmıyordu** — verilebilen ama hiçbir şey açmayan iki yetki daha.
      Mert `S-30`'u cevapladı: *"bloglar bu arada uç yazılsın blog yazılabilecek
      çünkü siteden"*. Yani statik kalmıyor; 22 ve 24 Ağustos kararlarını
      (platform ve işletme yazabilir, işletme yazısı onaydan geçer) iptal etmiyor,
      **uyguluyor**.

      **17 operasyon, 12 yol, 4 controller:**
      herkese açık `GET /api/blog` · `GET /api/blog/{slug}` ·
      `GET /api/blog/categories` — yazarlık (`blog.write`)
      `GET/POST /api/blog/posts` · `GET/PUT/DELETE /api/blog/posts/{id}` ·
      `POST .../submit` · `POST .../cover` — moderasyon (`blog.approve`)
      `GET /api/blog/moderation` · `GET /api/blog/moderation/{id}` ·
      `POST .../publish` · `POST .../reject` — kategori (`blog.approve`)
      `POST /api/blog/categories` · `PUT/DELETE /api/blog/categories/{id}`

      Kararlar ve gerekçeleri → [[api-kararlar]] 2026-09-04 (altı giriş)

      Kanıt: **511 test yeşil** (23'ü yeni). Dört mutasyon denendi, üçü
      yakalandı: onaya geri düşme kuralı kaldırıldı → 1 kırmızı; `ReservedSlugs`
      boşaltıldı → 3 kırmızı; `Status == Published` süzgeci gevşetildi → 2
      kırmızı.
      Kanıt: **dördüncü mutasyon YAKALANMADI ve iddia benimdi.** Kapsam
      süzgecini "iki dal olmalı, yoksa `= NULL`'a çevrilir" diye yazmıştım;
      tek dala indirdim, 23 test yeşil kaldı. EF Core boş parametreyi
      `IS NULL`'a çeviriyor. Kod tek dala indirildi, yorum ölçümle değiştirildi.
      Kanıt: canlı uçtan uca — kategori `201`, işletme kategori denemesi `403`,
      taslak `201` (çeviri sözlüğü TAM döndü, tr+en), `posts` kısa adı `400
      ReservedSlug`, gönderim `UnderReview`, herkese açık detay `404`,
      moderasyon kuyruğunda göründü, işletmenin moderasyon denemesi `403`,
      yayın `200` (`approvedAt` + `publishedAt` doldu), anonim liste `total 1`,
      `?language=en` başlık/özet/kategori adı üçü birden İngilizce,
      görüntülenme sayacı `0 → 1`.
      Kanıt: yayındaki yazı güncellendi → `UnderReview`, `approvedAt` `null`,
      `publishedAt` korundu, herkese açık detay `404`. Reddedilen yazı doğrudan
      yayınlanamadı (`400 NotUnderReview`); yazar tekrar gönderdi → gerekçe
      temizlendi → yayınlandı.
      Kanıt: **kapsam canlı ölçüldü** — başka işletmenin jetonuyla `GET`, `PUT`
      ve `DELETE` üçü de `404`; aynı jetonla kendi listesi `200 []` (olumlu dal,
      "her şeye 404 diyen" bozuk bir yol elenmiş oldu); sahibi `200`.
      Kanıt: kapak yüklendi `200`, WebP'ye yeniden kodlandı; içeriği türüyle
      uyuşmayan dosya `400 ContentTypeMismatch`. Kova politikası genişletilmeden
      kapak adresi `403`tü, genişletildikten sonra `200 image/webp`, aynı
      ölçümde `boat-documents/*` ve `partner-documents/*` `403` kaldı → `S-24`.
      Kanıt: 13 olay günlüğü satırı yazıldı, yükleri dolu — ret GEREKÇESİ ve
      yazı BAŞLIĞI hiçbirinde yok (ikisi de serbest metin).
      Kanıt: `openapi.json` yeniden üretildi — 105 yol, 131 operasyon.

- [x] **A-75** Arama sonucuna tekne tipi adı eklendi · bitti: 2026-08-31
      Sonuçta `boatTypeId` vardı, adı yoktu; arayüz kart rozetinde tur
      tipini yazamıyordu. `lookups` ile istemci tarafı eşleme REDDEDİLDİ —
      çeviri mantığı iki yere bölünürse aramayla süzgeç menüsü sessizce
      ayrışır (aynı gerekçe kiralama tipi adında zaten yazılı).
      Kanıt: canlı — çevirisi olan tip `"Gulet"`, **çevirisi olmayan tip
      `"a04-gulet"`** (ham anahtara düşüyor, boş değil)
      Kanıt: test iki durumu birlikte ölçüyor — yalnız çevirili durum
      ölçülseydi geri düşüşü hiç çalışmayan kod da geçerdi ve çevirisiz tip
      kartta BOŞ görünürdü
      Kanıt: 488 test geçiyor
      Maliyet: sayfadaki FARKLI tip sayısı kadar satır okuyan tek ek sorgu
      (kart başına değil); kapak görselindeki desenin aynısı

- [x] **A-74** 🔴 Yolcu listesi bayrağı süreden türetiliyordu · bitti: 2026-08-31
      Fiyat bağlamı `RequiresPassengerList`'i `DurationKind == MultiDay`
      ifadesinden hesaplıyordu. `ReservationFactory` bayrağı TEKLİFTEN
      kopyalayıp rezervasyona **donduruyor** — yolcu listesi isteyen
      teknenin her rezervasyonu kalıcı `false` damgalanıyordu.
      Belgelenmiş kurala aykırı (2026-08-22): bayrak teknenin anahtarı ve
      KVKK gerekçesi tam olarak buna dayanıyor.
      Kanıt: canlı — tekne detayı `true`, quote `false`, **aynı tekne aynı an**
      Kanıt: canlı — rezervasyon açıldı, veritabanında tekne `t` iken
      rezervasyon `f` damgalanmıştı
      Kanıt: yeni testler eski kodla **BAŞARISIZ (2/3)**, düzeltmeyle geçiyor
      Kanıt: bayrak iki değeriyle sınanıyor — yalnız `true` ölçülseydi her
      zaman `true` dönen bir hata da geçerdi
      Kanıt: 487 test geçiyor
      ⚠️ Mevcut bir test **kusuru iddia ediyordu**
      (`Assert.True(offer.RequiresPassengerList)`); vault'taki karara
      bakılarak kaldırıldı
      ⚠️ `passengerListReminderHours` müşteri tekne detayına eklendi —
      işletme paneli alıyordu, müşteri hiç görmüyordu

- [x] **A-73** İşletme ayarları — yalnız değiştirilebilir alanlar · bitti: 2026-08-31
      `GET`/`PUT /api/partner/profile`. Mert: *"ayarlar ucunu da yaz, sadece
      işletmenin değiştirebileceği alanlar"*. Yazılabilen beş alan:
      `displayName, email, phone, address, city`.
      Kanıt: PUT gövdesine `legalName`/`taxNumber`/`iban`/`status`
      **eklenerek denendi — hiçbiri değişmedi**, veritabanından doğrulandı
      Kanıt: kimliksiz `401`, yetkisiz müşteri `403`, sahip `200`
      Kanıt: e-posta küçük harfe normalleştiriliyor; IBAN'ın yalnız son
      dört hanesi dönüyor
      Kanıt: değişiklik yokken ikinci `PUT` günlüğe satır YAZMIYOR
      Kanıt: migration 1 yetki + **11 mevcut sahip rolü** + 1 platform
      yöneticisi doldurdu
      Kanıt: 484 test geçiyor
      ⚠️ Yeni yetki `partner.settings`. Geri doldurma ZORUNLUYDU: sahip
      rolü atanabilir yetkileri BAŞVURU ANINDA topluca alıyor, sonradan
      eklenen yetki eski işletmelere hiç düşmezdi

- [x] **A-72** İşletmenin kendi rezervasyon listesi · bitti: 2026-08-30
      `GET /api/partner/reservations`. Panelin rezervasyon modülü bu uç
      olmadan HİÇ yazılamıyordu: müşteri listesi `UserId`'ye bağlı, işletme
      oradan tek satır göremiyordu. `reservation.read` yetkisi 2026-08-24'ten
      beri kataloğdaydı ve **hiçbir uç kullanmıyordu** — verilebilen ama
      hiçbir şey açmayan bir yetki.
      Kanıt: kimliksiz → `401`; `reservation.read` olmayan müşteri → `403`;
      işletme sahibi → `200` ve gerçek satırlar
      Kanıt: varsayılan `totalCount` 2, `includeCancelled=true` ile 3 —
      iptal gerçekten eleniyor ve sayı da süzgeçle hesaplanıyor
      Kanıt: `from/to` süzgeci 1 satır, `status=Boarded` 1 satır,
      `pageSize=5000` → 50 (tavan)
      Kanıt: kapsam testi karşı işletmenin kaydını KENDİ listesinde de
      görüyor — hiçbir şey döndürmeyen bozuk sorgu böyle eleniyor
      Kanıt: 478 test geçiyor
      ⚠️ Müşteri iletişim bilgisi DÖNÜYOR, yolcu kimlik bilgisi dönmüyor
      → `S-27`

- [x] **A-71** Kiralama tipi listesi çevirilerin ham hâlini döndürüyor · bitti: 2026-08-30
      **Okuma şekli geçerli bir yazma gövdesi üretemiyordu.** `GET` düz
      `name`/`program` (çözülmüş hâl) döndürüyor, `PUT` ise dil koduna göre
      sözlük bekliyor ve sözlüğü TAM kabul ediyor. Cevabı okuyup geri
      gönderen panel sözlüğü dolduramıyor, metinleri SİLİYOR ve `204`
      alıyor — hata yok, kayıp var.
      Kanıt: canlı uçta `program` yazma denendi → `204`, alan `null` geldi
      Kanıt: canlı, düzeltmeden sonra → `translations: {}` dönüyor ve düz
      `name` hâlâ katalog adına düşüyor; ikisinin ayrı sorular olduğu ölçüldü
      Kanıt: yeni test — okunan sözlük olduğu gibi geri yazılınca metinler
      korunuyor
      Kanıt: ikinci test — boş sözlükte metinler SİLİNİYOR; korumanın
      sözlüğü okumaktan geldiğini kanıtlıyor, yoksa eşitleme hiç silmiyor da
      olabilir ve ilk test bunu ayırt edemezdi
      Kanıt: 472 test geçiyor
      ⚠️ Silme davranışı DEĞİŞTİRİLMEDİ — kasıtlı ve belgeli. Ek hizmetlerin
      listesi `Translations`'ı zaten döndürüyordu; iki kardeş özellik
      ayrışmıştı

- [x] **A-70** On dört üretim açılış kapısı sınanıyor · bitti: 2026-08-30
      `A-69`'un açığa çıkardığı sınıf arandı: yazılmış ama uygulandığı hiç
      ölçülmemiş kontrol. `Program.cs`'te on dört üretim kapısı vardı,
      **hiçbirinin testi yoktu.** Kapılar sessizce bozulsa fark ettirecek
      bir şey yoktu.
      Kurgu: kapılar sırayla açılıyor — her adımda bir ayar düzeltilip
      hatanın BİR SONRAKİ kapıya ilerlediği ölçülüyor. Böylece hem her kapı
      ateşliyor hem de seçici olduğu kanıtlanıyor. Üretim sunucusu hiç TAM
      ayağa kalkmıyor (kalksa zamanlanmış işler dış servise istek atardı).
      Kanıt: 14 kapının 14'ü sırayla ateşliyor
      Kanıt: hız sınırı kapısı geçici devre dışı → test **BAŞARISIZ**
      (`Assert.Contains Failure`) → testin kapıyı gerçekten ölçtüğü
      doğrulandı, sonra geri getirildi
      Kanıt: 470 test geçiyor

- [x] **A-69** 🔴 Hız sınırı kimlik çözülmeden uygulanıyordu · bitti: 2026-08-28
      `UseRateLimiter` `UseAuthentication`'dan ÖNCEYDİ; `context.User` o
      noktada boş olduğu için kullanıcıya göre bölünmesi gereken BÜTÜN
      politikalar (`panel`, `rezervasyonSorgu`, `personelEkle`) sessizce
      IP'ye düşüyordu. Kod "kullanıcıya göre" diyor, davranış IP'ye göreydi.
      Kanıt: düzeltmeden ÖNCE — kimliksiz 130 istek sonrası **geçerli
      jetonlu** istek `429`
      Kanıt: düzeltmeden SONRA — aynı sel sonrası geçerli jetonlu istek `200`
      Kanıt: kimliksiz uçlar hâlâ sınırlı — `/api/partners/apply` 10 geçti,
      11 ve 12 → `429`
      Kanıt: yeni test ESKİ sırada BAŞARISIZ (`Expected: Not TooManyRequests,
      Actual: TooManyRequests`), yeni sırada geçiyor — testin kusuru
      gerçekten ölçtüğü doğrulandı
      Kanıt: 469 test geçiyor

- [x] **A-68** Rol özetine `canDelete` eklendi · bitti: 2026-08-28
      Panel bir rolü silinebilir sanıp uçtan ret alıyordu: `memberCount`
      yalnız AKTİF çalışanı sayıyor, silme kontrolü çıkarılmış çalışanın
      duran kaydını da sayıyor (kısıtlayıcı yabancı anahtar onu sayıyor).
      Sayının anlamı DEĞİŞTİRİLMEDİ; eksik olan soru ayrı alan oldu.
      Kanıt: rol + aktif çalışan → `memberCount=1 canDelete=false`
      Kanıt: çalışan pasife alındı → `memberCount=0 canDelete=false`
      (**ayrışma**) ve `DELETE` → `400 RoleInUse`; panel artık önceden biliyor
      Kanıt: kullanılmayan rol → `memberCount=0 canDelete=true`, `DELETE`
      → `204` — alan her zaman `false` dönseydi üstteki üç ölçüm de geçerdi
      Kanıt: sahip rolü → `canDelete=false`
      Kanıt: 468 test geçiyor; ayrışma ve olumlu durum ikisi de sınanıyor

- [x] **A-67** Ödeme geri çağrısı rezervasyon özeti döndürüyor · bitti: 2026-08-28
      `POST /api/payments/callback` artık `{succeeded, reservation}` dönüyor;
      `reservation`, üye listesi ve misafir sorgusuyla AYNI satır tipi
      (`MyReservationItem`). Frontend'in 2 numaralı önceliğiydi: dönüş sayfası
      gösterecek gerçek veri bulamadığı için aylarca sabit veriden okumuş.
      Kanıt: canlı `:5163`, sahte sağlayıcı — 200 ve gövdede gerçek kayıt
      (`code NBSSMUFM`, `status Paid`, `boatName A04 Teknesi`,
      `grandTotalTry 1000.0`, `paidAt` dolu)
      Kanıt: **gövdede iletişim bilgisi ve biniş jetonu YOK** — uç kimlik
      doğrulamıyor, elindeki tek şey sağlayıcının işlem kimliği
      Kanıt: aynı jetonla ikinci çağrı da 200 ve AYNI özeti döndürüyor —
      sayfayı yenileyen misafir dolu ekrandan boş ekrana düşmüyor
      Kanıt: tanınmayan jeton `400 "Ödeme kaydı bulunamadı."`, jetonsuz istek
      `400 "İşlem kimliği yok."`
      Kanıt: **başarısız ödemede de özet dönüyor** — canlı, işlem kimliği
      `fake-fail-*` yapılıp çağrıldı: `{"succeeded":false, code "VZNR9X85",
      status "Pending", grandTotalTry 500.0}`. İlk yazımda `null` dönüyordu;
      hata sayfası hangi rezervasyonun düştüğünü söyleyemiyordu
      Kanıt: **uçtan uca, tarayıcıda tıklanarak** — misafir rezervasyon açtı,
      ödemeyi onayladı, `/booking/success?code=MC5GU38F` gerçek kaydı gösterdi
      (Bodrum Marina · 21 Kasım 2026 09:00 · 2 yetişkin 1 çocuk · ₺2.300);
      sayfa yenilendi, özet durdu. Sunucu tarafından bağımsız doğrulandı:
      `Paid · 2300.00 · 2+1 · PaidAt dolu · 4 defter satırı · toplam 0.00`
      Kanıt: 468 test geçiyor (`Callback_returns_the_reservation_summary_every_time`)
      ⚠️ `qrImageUrl` **kasten yapılmadı** → `S-25`, [[api-kararlar]]

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

- [x] **A-63** API arayüzü — Scalar · bitti: 2026-08-27
      Mert (2026-08-27): *"Swagger gibi kullanabileceğimiz ne var"* → Scalar
      `Scalar.AspNetCore` 2.17.1 · **MIT** (paketin `nuspec`'inden
      doğrulandı, tahmin edilmedi — ImageSharp'ta bu adım atlansaydı
      ücretli bir lisansa bağlanacaktık)
      Adres: `/scalar/v1` — yalnız Development
      Kanıt: **tarayıcıda uçtan uca** — jeton yapıştırıldı,
      `GET /api/platform/partners` **200 OK, 53 ms**, gerçek veri döndü
      Kanıt: üretim kapısı ateşliyor — `ApiReference:Enabled=true` ile
      uygulama AÇILMIYOR; kapalıyken açılıyor (ölçüldü,
      `--no-launch-profile` ile)
      Kanıt: 441 test geçiyor
      ⚠️ **Swagger/Swashbuckle KULLANILMADI.** .NET 10'un yerleşik
      `Microsoft.AspNetCore.OpenApi`'si zaten belgeyi üretiyordu; Scalar
      yalnız görüntüleyici. Swashbuckle ailesinden paket geri gelmedi
      ⚠️ **JWT şeması için `BearerSecurityTransformer` yazmak ZORUNLU oldu.**
      .NET'in yerleşik `AddOpenApi()`'si güvenlik şemasını kendiliğinden
      EKLEMİYOR; onsuz Scalar'ın jeton alanı hiç çıkmaz, her istek 401 döner
      ve arayüz sessizce işe yaramaz olurdu
      ⚠️ Şema belgeye ekleniyor ama uçlara ZORUNLU işaretlenmiyor: kimliksiz
      uçlar gerçekten kimliksiz, hepsine "jeton gerekli" damgası vurmak
      belgeyi yalancı yapardı
      ⚠️ `Microsoft.OpenApi` v2.7.5'te tipler **kök ad alanına taşındı**
      (`Microsoft.OpenApi.Models` DEĞİL) — assembly'den doğrulandı
