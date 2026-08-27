---
rol: status
kapsam: api
guncelleme: 2026-08-26
durum: guncel
---

# API Durumu

> **Bu dosyanın sahibi `DailyCruising.Back-End/` içinde çalışan oturumdur.**
> API tarafının güncel durumu buraya yazılır; `01-Genel/durum.md`'ye **yazılmaz**.
> Genel dosya bu dosyayı özetler → [[durum]]

## Nerede duruyoruz

**2026-08-27 — `A-62` BİTTİ.** Dosya beyanı içerik imzasıyla doğrulanıyor,
evraklar yetkili uçlardan indiriliyor, `FileKey` dışarı hiç verilmiyor.
**441 test geçiyor, 69 yol.**

🔴 **Backend'de Mert'in kararına bağlı olmayan iş KALMADI.** Açık üç işten
ikisi İyzico pazaryeri görüşmesine (`A-41`, `A-58`), biri frontend alanına
(`A-07`) bağlı.


🔔 **MERT'E HATIRLATMA — İYZİCO GÖRÜŞMESİ BEKLİYOR (`A-41`).**
İyzico'dan hesaba **pazaryeri (marketplace) özelliğinin açılması** istenecek;
sandbox ve üretim için ayrı ayrı. O açılana kadar tahsilat platform
hesabında, hakediş transferi ELLE. Uygulama her açılışta uyarıyor ve
kayıt açıldığında uyarı kendiliğinden susuyor.

**2026-08-26 — `A-60` (dosya depolama) BİTTİ.** S3 uyumlu depolama + WebP'ye
çevirme + üç boyut. Gerçek bir MinIO konteynerine karşı doğrulandı.
⚠️ Görsel kütüphanesi **SkiaSharp** seçildi çünkü ImageSharp ticari kullanımda
ücretli — Mert'in bilmesi gereken bir lisans kararı → [[api-kararlar]]


**2026-08-26 — MERT'İN 23 KARARINDAN DOĞAN 12 İŞİN HEPSİ BİTTİ.**
`A-44`…`A-59` arası kapandı. **414 test geçiyor.**

🔴 **`A-48`'de bilinen bir koruma boşluğu var ve bilerek bırakıldı:** beş
tabloda (`Voyages`, `Boats`, `Coupons`, `LedgerEntries`, `EventLogs`) iyimser
eşzamanlılık jetonu YOK — tetikleyiciler satırı arkadan güncelliyor ve jeton
kendi işlemimizi çarpıyordu. Boşluk bir testle sabitlendi → [[api-kararlar]]

**Panoda kalan dört iş de dış bir şeye bağlı:** `A-41` ve `A-58` İyzico
pazaryeri özelliğine, `A-60` dosya depolama kararına, `A-07` frontend alanına.


**2026-08-26 — `A-55` (ret ucu + yeniden başvuru) BİTTİ.** Platform artık
başvuru reddedebiliyor; reddedilen işletme aynı vergi numarasıyla yeniden
başvurabiliyor ama yalnız **e-posta + parola** teyidiyle → [[api-kararlar]]


**2026-08-26 — `A-44` (güvenlik damgası) BİTTİ.** Yetkisi değişen
kullanıcının jetonu artık ANINDA geçersiz; devir, rol değişimi ve üye
pasifleştirmesinde 15 dakikalık pencere kapandı.

⚠️ **Dağıtımda tüm açık oturumlar bir kez düşecek** — eski jetonlarda damga
talebi yok. Bilerek → [[api-kararlar]]


**2026-08-26 — `A-56` (otomatik iade) BİTTİ.** İptal edilen rezervasyonların
iadesi artık 15 dakikada bir kendiliğinden gidiyor; canlıda doğrulandı
(`6PY3ETG4`: iş buldu, gönderdi, defter 0.00'da denk).


**2026-08-26 — MERT'İN 23 SORUSUNUN HEPSİ CEVAPLANDI.** 12 numaradan
başlanıp sırayla geçildi. **6 karar onaylandı** (kod değişmiyor),
**17 tanesi iş çıkardı** — `A-44`…`A-60` panoda → [[api-benim-kararlarim]]

En pahalı soru (12 — teklifin paylaşımlı teknede tüm kapasiteyi kapatması)
**onaylandı**: `EX_Voyages_NoOverlapPerBoat` değişmiyor.

⚠️ İki karar **kendi başına başlayamaz**: `A-58` (satışa kapatma) İyzico
pazaryeri özelliğine, `A-60` (belge yükleme) dosya depolama kararına bağlı.

⚠️ Bir kararda **kendi tavsiyemin tersi** seçildi ve gerekçem zayıfladı:
otomatik iade (`A-56`). "Yanlış tutar geri istenemez" demiştim, ama tutar
iptal anında donuyor ve formülü test edilmiş — otomatikleşen şey hesap değil,
gönderme adımı.


**2026-08-26 — `A-20` (Testcontainers) BİTTİ.** Testler artık tek kullanımlık
`postgres:18.6-alpine` konteynerinde koşuyor; yerel PostgreSQL ve
`DC_TEST_PASSWORD` gerekmiyor. Kanıt: yerel `dailycruising_test` veritabanı
silindi, 367 test yine geçti. **CI'ın önündeki teknik engel kalktı** —
kurulumun kendisi `G-07`.


**2026-08-26 — `A-43` (test HTTP katmanı) BİTTİ.** `WebApplicationFactory`
kuruldu; yetkilendirme, durum kodları ve hız sınırı artık testten geçiyor.
`A-42`'de kapatılan güvenlik kapısının kanıtı elle `curl` olmaktan çıktı —
kapı sökülünce iki test kırmızıya dönüyor.

Yolda iki yapılandırma anahtarı açıldı (`ScheduledJobs:Enabled`,
`RateLimiting:Enabled`); ikisi de varsayılan açık ve **üretimde kapatılamıyor**
→ [[api-kararlar]]


**2026-08-26 — `A-42` (işletme başvuru ucu) BİTTİ.** `POST /api/partners/apply`
canlıda çalışıyor; IBAN zorunlu ve mod-97 sağlamasıyla doğrulanıyor.

🔴 **Yolda bir güvenlik açığı bulundu ve kapatıldı:** işletme paneli, işletme
`Active` olmadan da açıktı. Domain ve `Partner` kaydı "kapalı olmalı" diyordu,
hiçbir yer uygulamıyordu. Askıya alınan işletme de panelde çalışmaya devam
ediyordu. Artık `PermissionAuthorizationHandler` her istekte veritabanından
doğruluyor → [[api-kararlar]]

⚠️ **O kapının otomatik testi yok** — test projesi HTTP barındırmıyor.
`A-43` açıldı.


**2026-08-26 — `A-41`'in BİZİM tarafımız bitti.** Şema (`Partners.Iban`,
`BusinessType`, `PartnerPayeeAccounts`) ve bölüştürme kuruldu; sağlayıcıya
söylenen hakediş defterdekiyle aynı kaynaktan geliyor (`EarningCalculator`).

🔴 **İyzico tarafı hesap seviyesinde engelli:** `POST /onboarding/submerchant`
→ `2000 — Bu servis sadece pazaryeri müşterilerine açıktır`. Mert'in İyzico'dan
sandbox hesabına **pazaryeri özelliğini açtırması** gerekiyor. Alıcı kaydını
açan kod YAZILMADI — doğrulanamazdı.

🔴 **`A-42` açıldı: işletme başvuru ucu HİÇ YOK.** Domain akışının 3. adımı
yazılmamış; bugün sisteme hiçbir yoldan işletme giremiyor. IBAN'ı toplayacak
yer de burası → [[api-benim-kararlarim]]


**2026-08-26 — `A-29b` (iade ucu) BİTTİ.** `POST /api/payments/refund` canlıda
uçtan uca çalışıyor; defter 0.00'da denk. `A-29`'un kalan tek parçası
`IyzicoPaymentProvider` gövdesi → [[api-gorevler]]

**2026-08-26 — `A-29` (İyzico) da BİTTİ.** Mert anahtarları user-secrets'a
koydu; `IyzicoPaymentProvider` Checkout Form akışıyla yazıldı ve **gerçek
sandbox'a karşı uçtan uca doğrulandı**: tarayıcıda test kartıyla ödendi,
rezervasyon `Paid`, ardından gerçek iade yapıldı ve defter 0.00'da denk.

🔴 **AMA PARA İŞLETMEYE HÂLÂ GİTMİYOR.** Alt üye iş yeri (submerchant)
yazılmadı — tahsilat tamamen platform hesabına yapılıyor. `A-41` olarak açıldı
ve **yüksek öncelikli**; işletmelerden belge toplama adımı Mert'in cevabına
bağlı → [[api-benim-kararlarim]]

**Gerçek ölçü (2026-08-26):** 104 tablo · 20 controller · 64 yol / 79 işlem ·
**32 migration** · **13 zamanlanmış iş** · 385 test.


**Şema BİTTİ — `A-01` tamamlandı (2026-08-24).** Sekiz bölümün tamamı Mert onaylı
→ [[api-sema]]. Gerekçeler [[api-kararlar]] içinde, altı tarihli giriş.

**`A-02` de BİTTİ.** PostgreSQL 18.6 kurulu ve çalışıyor; `dailycruising_dev`
veritabanında **1. bölümün 13 tablosu** duruyor. Dört eklenti açık: `citext`,
`btree_gist`, `unaccent`, `pg_trgm`.

**`A-09` da BİTTİ.** Sekiz bölümün tamamı koda döküldü: **75 tablo**, 3 EXCLUDE
kısıtı, 5 tetikleyici. `EXCLUDE USING gist` beklendiği gibi EF tarafından
üretilemedi, elle SQL yazıldı ve **canlı test edildi** — Mehmet/Cemil çakışması
reddedildi, aynı günün ikinci turu geçti.

**`main`'e birleştirildi ve push'landı** (2026-08-24): commit `8bbb04f`, 91 dosya.
Birleştirme sonrası `main` üzerinde `--no-incremental` derleme 0 uyarı 0 hata,
`GET /api/health` 200. Özellik dalı hem yerelde hem uzakta silindi.

**`A-11` de BİTTİ** (2026-08-24): `EventLogs` bölümlenmiş, 26 parça, toplam 101 tablo.

**`A-03` birinci dilim, `A-15` ve `A-14` de BİTTİ** (2026-08-24):
kimlik doğrulama + JWT + yetki kontrolü çalışıyor; zamanlanmış iş katmanı kuruldu
ve kilitlenme senaryosu canlı çözüldü.

**Sırada:** `A-17` TCMB kur işi (**dövizli satış buna bağlı**) · `A-03` kalanı
(parola sıfırlama, e-posta doğrulama, çalışan yönetimi) · `A-16` puan ortalaması ·
`A-10` ayrı veritabanı rolü · `A-06` test projesi.

| # | Bölüm | Durum |
|---|---|---|
| 1 | Kimlik ve yetki | ✅ onaylandı 2026-08-24 |
| 2 | Katalog | ✅ onaylandı 2026-08-24 |
| 3 | Kiralama tipleri ve fiyat | ✅ onaylandı 2026-08-24 |
| 4 | Takvim ve sefer | ✅ onaylandı 2026-08-24 |
| 5 | Rezervasyon | ✅ onaylandı 2026-08-24 |
| 6 | Para | ✅ onaylandı 2026-08-24 |
| 7 | Teklif ve mesajlaşma | ✅ onaylandı 2026-08-24 |
| 8 | Yan sistemler + olay günlüğü | ✅ onaylandı 2026-08-24 |

Domain katmanı **dolu**: 11 klasör, 54 dosya, 74 entity. Infrastructure'da
`DailyCruisingDbContext` + 12 yapılandırma dosyası + 7 migration.
Veritabanında **75 tablo (+26 EventLogs parçası) · 3 EXCLUDE kısıtı · 54 CHECK**.
**Application katmanı hâlâ boş** — iş mantığı ve uç nokta yazılmadı.
Çalışan tek uç: `GET /api/health` → `{"status":"healthy"}`.

Bağlantı dizesi **user-secrets'ta**, `appsettings.json`'da değil — parola repoya
girmiyor.

## 🟢 Cevap bekleyenler — şemayı bloke eden YOK

**Şemayı bloke eden soru YOK.** 35b/38/39/40/41 kapalı — beşi de 22–23 Ağustos'ta
cevaplanmıştı, [[domain-gereksinimler]] "Cevap bekleyenler" tablosu güncellenmediği
için açık görünüyordu; 2026-08-24'te düzeltildi.

| # | Konu | Kimde |
|---|---|---|
| 41 | Ödeme sağlayıcı (sanal POS) seçimi — şemayı bloke etmiyor | Mert |
| G-13 | Fatura modelinin mali müşavirle teyidi | Mert |

**Çıkarımla şema kurulmaz** — kurulursa altı ay sonra "Mert böyle demişti" diye
anılır → [[api-desenler]].

## 🟡 Karara bağlanmamış — API

| Konu | Durum | Not |
|---|---|---|
| Ödeme sağlayıcı | Karar yok | Eski sistem Paratika (marketplace, alt üye iş yeri). Aynısı mı, alternatif mi? |
| SMS sağlayıcı | Karar yok | Eski sistem Verimor; canlıda IP whitelist hatası veriyor |
| Veri göçü | Karar yok | 35 tekne, 104 kullanıcı, 120 rezervasyon, 46 blog taşınacak mı? |
| Test projesi | Yok | xUnit projesi kurulmadı. Domain modeli gelmeden test yazılacak bir şey de yok |
| API-önce mi | Karar yok | Mobil uygulamalar var → "önce API katmanı" mantıklı. Ayrı API + Next.js istemci kurgumuza zaten uygun |

## Şema kurulurken unutulmayacaklar

- **Olay günlüğü bugün girmeli.** Sezonluk AI raporları ertelendi ama **veri toplama
  ertelenemez** — geçmişe dönük üretilemez → [[domain-gereksinimler]]
- **Çeviri tabloları baştan kurulacak.** i18n özelliği ertelendi, şema ertelenmedi
  (TR/EN/DE/RU) → [[domain-gereksinimler]]
- **Sefer devri şemaya kapatılmayacak.** İlk sürümde yok ama Mert "kesinlikle
  ekleyeceğiz" dedi
- **Fiyat sunucuda doğrulanacak.** Gerekçe PRD değil güvenlik → [[api-kararlar]] 2026-08-22
- **Roller veritabanı kaydı**, kodda sabit değil. İki boyut: ne yapabilir × kimin
  verisinde → `A-03`

## ✅ Mert'in cevapladıkları (2026-08-24)

Sekiz soru da cevaplandı, cevapsız soru **kalmadı**. Gerekçeler ve iptal edilen
kararlar → [[api-kararlar]] 2026-08-24.

| # | Konu | Mert'in cevabı | Sonuç |
|---|---|---|---|
| S-1 | TCMB hangi kuru | *"Sana bırakıyorum bu kısmı"* | **`ForexSelling`** korundu — döviz satış, TL'ye çevirmenin ticari standardı |
| S-2 | Parola kuralı | *"Çok karmaşık olmasın ki kullanıcılar hızlı kayıt olabilsinler"* | Asgari **10 → 8**, karmaşıklık şartı yok. 8, NIST SP 800-63B tabanı |
| S-3 | Hesap uçlarında hız sınırı | *"IP başına 10 istek iyi 15 dk'da"* | Değişmedi |
| S-4 | E-posta değişiminde mevcut parola | *"Sorulsun"* | Değişmedi |
| S-5 | Başarısız girişte denenen adres | *"Loglansın"* | **Yazılıyor** — trim + küçük harf, 254 karakterde kesiliyor |
| S-6 | Olay günlüğü ayrıntısı | *"Ayrıntılı olursa daha iyi olur, AI'a vereceğimiz veri daha iyi olur"* | Fiyat ucu olay günlüğüne bağlandı; kalanı `A-21` |
| S-7 | Kuponun matrahı | *"Şu anda olduğu gibi kalsın"* | Tur + ek hizmet, değişmedi |
| S-8 | Fiyat ucunda hız sınırı | *"IP başına dakikada 60"* | Değişmedi |
| S-9 | Kupon reddinde sebep | *"Kupon reddedilince müşteri sebebini görsün"* | **Sebep ayrıştırıldı** — sabahki tek-metin kararını iptal eder |

⚠️ **S-5'in bedeli geri alınamaz.** `EventLogs` append-only ve TRUNCATE yetkisi
uygulama rolünde yok; oraya giren e-posta adresi **silinemez**. Hesabı olmayan
birinin adresi de düşüyor — biri e-postasını yanlış yazınca üçüncü bir kişinin
adresi kalıcı olarak kaydedilir. `A-12` bu satırı ayrıca ele almak zorunda.

## ✅ ÇÖZÜLDÜ — S-10 / S-15 çelişkisi (2026-08-26)

**ÇÖZÜLDÜ.** Mert 2026-08-26'da karar almayı bana bıraktı; **A seçeneğinin
daraltılmış hâlini** uyguladım → [[api-benim-kararlarim]]

Özet: kısıt yaratma anına alındı (müşteriye görünmüyor → sızmıyor), yalnız
**işletme** kuponlarına uygulanıyor, aşan kısmı platform üstleniyor ve
rezervasyona donduruluyor.

Kırpmayı yazdım, mevcut bir test kırmızıya döndü ve haklıydı:

`Komisyonu_asan_kupon_artik_uygulaniyor` — *"aynı kupon, komisyonu farklı iki
işletmede AYNI indirimi vermeli"*. Bu test `S-10`'un tam karşılığı.

**Neden çelişiyor:** kırpma tavanı **karşılayanın payı**, o da komisyon
oranından türüyor. Yani:

| Kupon | %15 komisyonlu işletme | %25 komisyonlu işletme |
|---|---|---|
| Platform kuponu %20, 1.000 TL tur | tavan 150 → indirim **150** | tavan 250 → indirim **200** |

Çağıran iki teknede farklı indirim görüyor ve **komisyon oranını okuyor**.
`S-10`'da kaldırdığımız sızıntının aynısı — üstelik daha kötüsü: eski kural
ikili bir eşik veriyordu (*"geçti / geçmedi"*), kırpma ise oranı **neredeyse
tam olarak** söylüyor (`indirim = min(kupon%, komisyon%)`).

### Ölçtüğüm seçenekler

| # | Yaklaşım | Sızıntı | Bedel |
|---|---|---|---|
| A | **Kuponu YARATIRKEN sınırla**, uygularken değil | **Yok** — her teknede aynı indirim | Platform kuponu tüm işletmeler için geçerli olacaksa **en düşük** komisyona göre sınırlanır; büyük kampanya imkânsızlaşır |
| B | Kırpmayı uygula, sızıntıyı kabul et | Var, ve S-10'dakinden **daha kesin** | S-10 boşa gitmiş olur |
| C | Kırpma yok, indirim yalnız tur bedelini aşamasın | Yok | Hakediş **negatife düşebilir** — S-15'in çözmek istediği şey çözülmemiş kalır |
| D | Aşan kısmı platform karşılar | Yok | `S-14` kararına aykırı (*"kuponu kim oluşturduysa o"*) |

**Önerim A.** Kısıt kuponun yaratıldığı anda çalışır, müşteriye hiç görünmez,
ve `S-15`'in amacını (kimse borca girmesin) tam karşılar. Bedeli: platform
geneli kuponlar en düşük komisyon oranıyla sınırlı kalır.

⚠️ **Bunu ben seçmedim** — dört seçeneğin de iş tarafında farklı bedeli var.
`A-29` (İyzico) bu cevaba bağlı: hakediş hesabı yazılmadan ödeme akışı
tamamlanamaz.

## ✅ Mert cevapladı — S-15, S-16, S-17 (2026-08-26)

| # | Soru | **Mert'in cevabı** | Ne yapılacak |
|---|---|---|---|
| S-15 | İndirim, karşılayan tarafın payından büyük olursa | **"Sıfıra kadar, fazlası kırpılır"** — karşılayan taraf en fazla kendi payı kadar öder | `PricingService` indirimi kırpacak; kırpma olduğunda müşteriye AÇIKÇA söylenecek → `A-26b` |
| S-16 | Kademeli iade komisyona da uygulanıyor mu | **"Komisyon da yarılanır"** — iki taraf aynı oranda kaybeder | `A-27` artık yazılabilir |
| S-17 | Çalınmış jeton saptandığında | **"Yalnız o zinciri kapat + kullanıcıya e-posta gönder"** | `TokenReused` saptanınca zincir iptal edilecek, uyarı postası gidecek → `A-31` |

⚠️ **S-15 ESKİ BİR GEREKÇEYİ TERS ÇEVİRİYOR.** Şemadaki not şöyle diyordu:
*"Aşan kupon o teknede geçersiz sayılır, KIRPILMAZ — kırpılsaydı müşteri ilan
edilen oranla uygulanan oranın farkını şikayet ederdi."* Artık kırpılıyor, yani
o şikayet riski gerçek. Bu yüzden kırpma **sessiz olmayacak**: yanıt indirimin
kısmen uygulandığını ayrı bir alanla söyleyecek. Aksi halde müşteri "%90 kupon"
görüp %85 indirim alacak ve sebebini hiçbir yerde bulamayacaktı.

⚠️ **S-17'nin yanlış pozitif bedeli var.** Kötü bağlantıda istemcinin aynı
yenileme isteğini iki kez göndermesi "çalıntı jeton" sayılıyor. Zincir kapanması
o cihazın yeniden giriş yapması demek (diğer cihazlar açık kalıyor) ama uyarı
postası da gidiyor — yani meşru kullanıcı sebepsiz "şüpheli erişim" postası
alabilir. Sıklığı `EventLogs`'tan izlenmeli; çok çıkarsa eşik gerekir.

## ✅ Mert cevapladı — S-10 … S-14 (2026-08-25)

| # | Soru | **Mert'in cevabı** | Ne yapılacak |
|---|---|---|---|
| S-10 | Kuponun uygulanıp uygulanmaması işletmenin komisyon oranını ele veriyor | **"Kupon kuralını kaldır"** — kupon komisyondan büyük olabilsin | `trg_coupon_within_commission` tetikleyicisi kaldırılacak, `PricingService` kırpmayı bırakacak → `A-26` |
| S-11 | Rezervasyon ucu kimliksiz ve 15 dk koltuk tutuyor | **"Kimliksiz kalsın"** — IP başına 15 dk / 10 sınırıyla | Değişiklik yok. ⚠️ `A-19` (`UseForwardedHeaders`) hala şart: ters vekil arkasında bu sınır ya herkesi tek kovaya sokar ya IP değiştirerek aşılır |
| S-12 | Müşteri iptalinde iade oranı | **"Kademeli"** — kalkışa **48+ saat** kala %100, **24–48 saat** arası %50, **24 saatten az** kala iade yok | Politika kodlanacak; para hareketi `G-03` (sanal POS) ve `A-18` (defter ters kaydı) beklerken **hesaplanan iade tutarı** rezervasyona yazılacak → `A-27` |
| S-13 | İptalde e-postaya onay linki | **"Şu anki gibi kalsın"** — kod + e-posta/telefon tam eşleşme | Değişiklik yok. Mevcut sıkılaştırmalar korunuyor: telefon tam eşleşme, başarısız denemeler loglanıyor, koda göre saatte 5 deneme |
| S-14 | S-10'un doğurduğu soru: kupon komisyonu aşınca açığı kim karşılar | **"Kuponu kim oluşturduysa o"** — işletme kuponu → işletmeden, platform kuponu → platformdan | Defter dağılımı `Coupon.PartnerId` boş mu dolu mu diye ayrışacak → `A-26` |

⚠️ **S-12'nin bir ucu açık kalıyor:** kademeli oranın **komisyona da uygulanıp
uygulanmayacağı** sorulmadı. %50 iadede platform kendi payının yarısını da geri
veriyor mu, yoksa komisyonu tam mı alıyor? `A-27` bunu ayrıca sormak zorunda —
tahmin edilmeyecek.

⚠️ **S-10 geri alınamaz bir kapı açıyor.** Bugüne kadar veritabanı tetikleyicisi
"kupon komisyonu aşamaz" kuralını **garanti ediyordu**; kaldırılınca garanti
uygulama katmanına iner ve orada bir hata doğrudan **negatif hak ediş** üretir.
`A-26` bunun yerine "hak ediş negatif olamaz" kısıtını koymak zorunda.
## 🟢 Doğrulanmış

- `dotnet build` — 0 uyarı, 0 hata
- `GET /api/health` yanıt veriyor
- `POST /api/pricing/quote` — istemci `grandTotalTry:1` ve `discountAmountTry:9999` gönderdi, sunucu **1000.00** ve **0** döndü (2026-08-24)
- Denetimde canlı üretilen dört açık kapatıldı ve **yeniden denendi**: taşan
  kişi sayısı, `int.MaxValue` gece, takvim sonu tarih, 200.000 satırlık ek
  hizmet — dördü de artık HTTP 400 (2026-08-24)
- Production kipinde beklenmeyen hata `{"error":"Beklenmeyen bir hata oluştu."}`
  dönüyor, yığın izi sızmıyor
- **44 test, 44'ü geçiyor**
- Kupon ret sebebi ayrıştırıldı ve canlı doğrulandı: olmayan kod → *"Böyle bir
  kupon kodu yok."*, komisyonu aşan kupon → *"Bu kupon bu turda kullanılamıyor."*
  (komisyondan söz etmiyor)
- Başarısız girişte denenen adres yazılıyor: `"  YaNLIS@Ornek.COM  "` →
  `yanlis@ornek.com`. Serbest metin ve `<script>alert(1)</script>` →
  `(e-posta bicimi degil)`, içerik saklanmıyor
- Fiyat ucu olay günlüğüne bağlandı: `pricing.quoted`, `pricing.quote.failed`,
  `coupon.applied`, `coupon.rejected` satırları `EventLogs`'ta görüldü
- Parola: 7 karakter → 400, 8 karakter → 200
- **`/api/auth/login` hız sınırına bağlandı** — önce 40 istek 40 kez 401 (tek 429
  yok), şimdi 10 istek sonra **429**. `refresh` bilerek sınırsız, denendi
- **Olay kaydı artık kopan bağlantıda da yazılıyor**: eski davranışta 3 kopan
  istek → 0 kayıt, yeni davranışta → 3 kayıt
- **`POST /api/reservations` ayakta** (A-22). İstemci `grandTotalTry:1` gönderdi,
  sunucu **1800.00** döndü — istekte tutar alanı yok
- +1 gün kuralı: 2 gece → 3 gün → **30.000 TL** · Mehmet/Cemil: çarterin ortasına
  günlük tur **409** · kapasite aşımı **409** · aynı gün ikinci rezervasyon aynı
  sefere bindi
- Kupon hakkı tetikleyicisi: `ERROR: Kupon kullanim hakki dolmus (1 / 1)`.
  Rezervasyon süresi dolunca `UsedCount` **1 → 0**, kupon tekrar geçti
- **Terk edilen çarterin takvimi bırakılıyor** — sefer `Cancelled`, aynı tarihe
  yeni çarter **201**. Paylaşımlı seferde bir vazgeçme seferi iptal etmiyor
- **Sahiplik devri ayakta** (`A-03e`): jetonsuz **401**, yetkisiz çalışan
  **403**, yanlış parola **400**, kendine devir **400**, devir **204**.
  Devir sonrası veritabanında bayrak ve roller takas, işletmede tek sahip
- ⚠️ **Devirden sonra eski sahibin jetonu ≤15 dk eski yetkileri taşıyor** —
  eski sahip tekrar devir denediğinde `HasPermission` süzgecinden geçti,
  akışı durduran şey sahiplik kontrolü oldu. Yeniden girişte jetonda hiçbir
  yetki kalmıyor, yani veritabanı doğru; donmuş olan yalnız eski jeton
  -> [[api-benim-kararlarim]]
- **`A-03` kapandı** — kalan üç maddesinden ikisi `A-33`…`A-38`'e devroldu
- **Tekne katalog uçları ayakta** (`A-33a`): 401 jetonsuz · 400 sözleşme
  onaylı değilken · 201 + doğrudan `Published` · Türkçe ad
  `mavi-yolculuk-guleti-sahin` · aynı ad ikinci teknede `-2` · 400 kapasite
  yasal sınırı aşınca · 404 başka işletmenin teknesi
- Müşteri sayfası (`GET /api/boats/{slug}`, kimliksiz) **200**; gövdede
  `flagRegistryNo`, `captainName`, `engineInfo`, `legalCapacity`, `status` YOK.
  Tekne pasife alınınca aynı adres **404**
- Olay günlüğünde `boat.created`, `boat.status.changed`
  (`from: Published → to: Inactive`), `boat.viewed`, `boat.catalog.denied`
- `openapi.json` repoda, 32 uç. `./araclar/openapi-uret.sh` üretiyor,
  `OpenApiBelgesiTests` bayatlamayı yakalıyor — **A-33a'da kendiliğinden ateşledi**
- **Kiralama tipi ve fiyat uçları ayakta** (`A-33c`): 201 tip · 400 aynı tip
  tekrar · 201 temel fiyat · 400 ikinci temel fiyat · 201 sezon · 400 çakışan
  sezon · 201 bitişik sezon · 400 kişi başı tipe tekne fiyatı · 400 yarım açık
  sezon · 400 temel fiyat silme · 204 sezon silme · 404 başka işletmenin teknesi
- Sezon sınırı **kapsayıcı** doğrulandı: 2027-10-31'de başlayan **400**,
  2027-11-01'de başlayan **201**
- **Yeni kısıt `IX_BoatRentalTypes_BoatRental`** — migration
  `CONCURRENTLY` + `suppressTransaction`; ileri/geri denendi
- ⚠️ Migration'lar **`dailycruising` sahip rolüyle** koşuyor;
  `dailycruising_app` ile `permission denied for schema public` (A-10 çalışıyor)
- **Ek hizmet uçları ayakta** (`A-33e`): 400 `tr` çevirisi yokken · 201
  `tr`+`en` ile · 400 boş ad · 400 negatif fiyat · 200 liste (`names` sözlüğü) ·
  204 güncelleme · 200 liste (`en` çevirisi silinmiş) · 404 başka işletme
- ⚠️ **Liste ucu ilk sürümde 500 veriyordu** — `ToDictionary` EF
  projeksiyonunda çevrilemiyor; derleme ve 215 test temizdi, yalnız canlı
  istek gösterdi. O ucun testi yoktu -> [[api-desenler]]
- **`A-33` tamamen bitti** (tekne + kiralama tipi + fiyat + ek hizmet)
- **Arama ucu ayakta** (`A-34`, kimliksiz): müsaitlik canlı doğrulandı —
  12 boş → **12** · 10 satılınca → **2** · 3 kişi → **YOK** · 12/12 → **YOK** ·
  sefer `Cancelled` → yine **12** · bakım günü → **YOK**, ertesi gün → **12**
- Sezon fiyatı doğru uygulanıyor: 2027-09-15 → **650**, 2027-06-15 → **500**
- ⚠️ **`Boats.DefaultCalendarMode` kolonunda `'Open'` yazıyordu** — enum'da
  böyle bir değer yok, arama o satıra dokununca **500**. Geçmiş bir seed
  SQL'i yazmış. **68 enum kolonunun hiçbirinde CHECK kısıtı yok** → `A-39`
- **Enum kısıtları kuruldu** (`A-39`): 69 kolon, 49 tablo. Elle geçersiz enum
  yazma denemesi artık **reddediliyor**. Migration bozuk veride **durdu** ve
  arkasında hiçbir kısıt bırakmadı
- ⚠️ Ürettiğim kolon listesi `BoatRentalTypes.WeekStartDay`'i kaçırmıştı
  (BCL enum'u `DayOfWeek`); EF modelini okuyan test yakaladı
- **Yorum uçları ayakta** (`A-35`): uydurma jeton **404** · geçerli davet
  **200** · QR okutulmamışken **400** `NotBoarded` · QR sonrası **201** ·
  aynı jetonla tekrar **400** `InvitationUsed` · `Pending` yorum tekne
  sayfasında görünmüyor, puan boş · onaydan sonra görünüyor, puan **5.00 / 1**
- ⚠️ **Yorum davetini ÜRETEN iş yok** — `A-35` yalnız tüketen uçları yazdı.
  Davet satırını elle kurdum → `A-40`
- ⚠️ Yarış korumasını hiçbir test ölçmüyordu; koşul kaldırıldığında testler
  yeşil kalıyordu. `Davet_ikinci_kez_tuketilemiyor` eklendi
- **Mesajlaşma ayakta** (`A-36a`): kimliksiz **401** · konuşma **201** ·
  numara ve e-posta `[gizlendi]`, veritabanında orijinal duruyor · işletmenin
  IBAN'ı maskelendi · üçüncü kişi **404** · QR okutuldu → konuşma
  **`Closed / Boarded`** · kapalıya mesaj **400**, okuma yine **200**
- ⚠️ İki hata yalnız CANLI denemede çıktı: yeni konuşmanın `Id`'si boşken ilk
  mesaj FK ihlaliyle **500**; `[Authorize]` yokken kimliksiz istek **400**
  alıyordu (401 olmalıydı)
- **Özel teklif ayakta** (`A-36b`): satıcı **201** · **tarih tutuldu**
  (arama o günü göstermiyor, ertesi günü gösteriyor) · ikinci teklif **400**
  `DateAlreadyHeld` · ret **204** → tarih serbest · kabul **200** +
  rezervasyon · çift gönderim aynı kimlik · sefer `Offer → Sale`
- ⚠️ **Dört hata yalnız CANLI denemede çıktı**: `CK_Voyages_RentalTypeRequired`,
  çevrilmemiş `23P01` (çıplak 500), eksik `Include` (NullReference),
  `CK_Reservations_HoldExpiry` (süresiz `Pending` tasarımım yanlıştı)
- ⚠️ `ExpireOffersJob` ve `CloseConversationsJob` **daha önceki oturumlardan
  zaten vardı**; pano söylemiyordu. `ExpireOffersJob`'un üzerine yazdım,
  git'ten geri aldım
- **Destek talepleri ayakta** (`A-37`): kimliksiz açma **201** · geçersiz
  kategori **400** · kimliksiz okuma **401** · müşteri iç not **400** ·
  müşteri durum değişikliği **403** · personel iç notu müşteri görüşünde
  **görünmüyor**, `FirstResponseAt` **boş** kalıyor · gerçek cevap
  `Answered` + `FirstResponseAt` **dolu**
- ⚠️ Hız sınırı hatası canlı çıktı: tüm sınıfa `hesap` yazmıştım, kendi
  talebini okuyan müşteri **429** alıyordu. Sınıf `panel`e alındı
- **Platform yönetimi ayakta** (`A-38`): kimliksiz **401** · işletme
  kullanıcısı **403** · platform personeli **200** · **okuma olay sayısını
  artırdı** — muafiyetin bedeli gerçekten ödeniyor · %18 sonra %12 sözleşme →
  eskisi `Cancelled`, yenisi `Sent` · %150 komisyon **400** · askı akışı tam
- ⚠️ **`SuspensionReason` kolonu eklendi**: askı sebebini `RejectionReason`'a
  yazıyordum, kolon adı içeriğiyle uyuşmuyordu ve kısıt onu `Rejected`
  durumuna bağlıyor. Migration eski kayıtları taşıyor
- **Yorum daveti işi ayakta** (`A-40`): `A-35` akışı canlıda hiç
  çalışmıyordu — daveti tüketen uçlar vardı, üreten yoktu
- ✅ **`A-20` (Testcontainers) BİTTİ** (aynı gün, öğleden sonra). Sabah
  `docker pull` hiçbir imajı indiremediği için geri alınmıştı; yeniden
  ölçüldüğünde engel kalkmıştı. Testler artık tek kullanımlık
  `postgres:18.6-alpine` konteynerinde; yerel PostgreSQL gerekmiyor.
  **Ders: "engel" diye kaydedilen şey ölçümdü, kalıcı bir gerçek değil —
  yeniden ölçmeden görev kapatılmış sayılmaz**
- ⚠️ `A-20`'nin `G-05` referansı yanlıştı (o i18n); CI görevi **`G-07`**
- **367 test, 367'si geçiyor** · `openapi.json` 63 yol
- Repo `mertagralii/DailyCruising.API` (private), push edildi

İlgili: [[durum]] · [[api-sema]] · [[api-gorevler]] · [[api-kararlar]] · [[api-desenler]] · [[api-araclar]] · [[api-notlar]] · [[domain-gereksinimler]]
