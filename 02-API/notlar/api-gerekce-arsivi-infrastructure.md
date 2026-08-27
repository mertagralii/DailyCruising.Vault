---
rol: not
kapsam: api
guncelleme: 2026-08-27
durum: guncel
---

# Gerekçe arşivi — Infrastructure katmanı

EF yapılandırmaları, depolar, işler, dış servisler.

Kod içindeki ⚠️ işaretli gerekçe yorumları 2026-08-27'de silindi; kod artık
yalnız *ne yaptığını* anlatan XML doc taşıyor → [[api-kararlar]]. Silinmeden
önce **152 blok birebir** buraya taşındı: hiçbiri yeniden yazılmadı,
kısaltılmadı, özetlenmedi. Satır numaraları silme anındaki hâle aittir;
dosya adı kalıcı, satır numarası değil.

**Bu bir arşivdir, talimat değil.** Bir madde koda aykırı çıkarsa kod
doğrudur → [[api-desenler]]

Diğer katmanlar: [[api-gerekce-arsivi-api]]

---


## `src/DailyCruising.Infrastructure/Analytics/EventLogger.cs`

**satır 100**

> <summary>
> ⚠️ Surrogate GÜVENLİ. `value[..max]` bir emojinin ortasında kesebilir;
> geriye yarım surrogate kalır. Payload'da bu yalnız U+FFFD'ye dönüşüyordu,
> ama BURASI jsonb değil `text` kolonu: Npgsql'in UTF8 kodlaması geçersiz
> metinde istisna fırlatabilir ve o istisna olayın TAMAMINI düşürürdü.
> </summary>

**satır 133**

> <summary>
> Payload'ı `EventPayloadPolicy`'ye göre süzer.
>
> ⚠️ Bu süzgeç ÇAĞIRANIN dikkatine güvenmemek için var. Nokta çözümler
> zaten vardı (e-posta biçim kontrolü, kupon kodu kesme, rezervasyon kodu
> kontrolü) ama her biri ayrı bir yerde ve yeni olay yazan birinin
> hiçbirini bilmesi gerekmiyordu. `EventLogs` temizlenemediği için tek bir
> unutma kalıcı.
>
> Üç kural, hepsi FAIL-CLOSED:
>   1. Olay türünün listesi yoksa payload düşer.
>   2. Listede olmayan anahtar düşer.
>   3. İç içe değer (nesne/dizi) düşer — kesme derinlemesine yapılamıyor,
>      bugünkü payload'ların hepsi düz ve düz kalmalı.
>
> Düşen her şey uygulama günlüğüne yazılıyor: sessiz kayıp, hiç kayıt
> olmamasından daha kötü olurdu.
> </summary>

**satır 180**

> ⚠️ BU CATCH ŞART. Serileştirme istisna fırlatabiliyor: döngüsel
> referans ("object cycle detected") ya da aynı JSON adına düşen iki
> property. Yakalanmasaydı istisna dıştaki genel `catch`'e sıçrar ve
> yalnız payload değil OLAYIN TAMAMI kaybolurdu — aktör, zaman, IP
> özeti dahil. "Payload düşer, olay kalır" garantisi o yolda
> tutmuyordu; denetim bunu 2026-08-25'te yakaladı.
>
> Bugün çağıranların hepsi düz anonim tip, yani tetiklenmiyor. Ama
> payload'a bir domain nesnesi geçiren biri olduğunda olay sessizce
> kaybolurdu ve hiçbir test bunu görmezdi.


## `src/DailyCruising.Infrastructure/Authentication/PasswordHasherAdapter.cs`

**satır 7**

> <summary>
> ASP.NET Core'un `PasswordHasher` uygulaması: PBKDF2-HMAC-SHA512, 100.000
> tur, rastgele tuz, sürüm damgalı biçim.
>
> Neden bu: .NET ile birlikte geliyor, denenmiş, ve sürüm damgası sayesinde
> algoritma güçlendirildiğinde eski hash'ler tanınıp yeniden üretilebiliyor.
> Kendi hash şemamızı yazmak bu üçünü de kaybettirirdi.
>
> ⚠️ Bu YALNIZ parola içindir. Jetonlarda kullanılamaz — bcrypt/PBKDF2 her
> çağrıda farklı çıktı verir, `WHERE TokenSha256 = @hash` hiç eşleşmez.
> Jeton için <see cref="JwtTokenService"/> içindeki SHA-256 kullanılıyor.
> </summary>


## `src/DailyCruising.Infrastructure/Boarding/BoardingRepository.cs`

**satır 33**

> <summary>
> ⚠️ `AsNoTracking` YOK, bilerek: dönen rezervasyonun durumu değişecek.
> `Voyage` de yükleniyor çünkü sonuçta sefer saatleri dönüyor ve ikinci
> bir sorgu, okutma başına fazladan gidiş-dönüş demek olurdu.
> </summary>

**satır 109**

> <summary>
> ⚠️ Konuşma (müşteri × TEKNE) bazında; rezervasyona bağlı değil. Bu
> yüzden zincir: rezervasyon → `UserId` + `Voyage.BoatId` → konuşma.
>
> Koşulda `Status = Open`: zaten kapalı bir konuşmanın `ClosedAt`'ini
> yeniden yazmak, "ne zaman kapandı" sorusunun cevabını bozar — tekrar
> okutma normal ve her seferinde tarihi ileri kaydırırdı.
> </summary>


## `src/DailyCruising.Infrastructure/Catalog/BoatCatalogRepository.cs`

**satır 12**

> <summary>
> ⚠️ HER PANEL SORGUSU `partnerId` ALIR. Parametresiz bir "hepsini getir"
> metodu bilerek yok — kapsamı unutan yeni bir çağrı yolu başka işletmenin
> teknesini sessizce döndürürdü.
> </summary>

**satır 158**

> <summary>
> ⚠️ `Status == Published` ŞART. Taslak ve pasif tekneler müşteriye
> görünmez; filtre unutulsaydı işletmenin henüz yayına almadığı teknesi
> doğrudan bağlantıyla okunabilirdi.
> </summary>

**satır 194**

> ⚠️ `partnerId` FİLTRESİ ŞART. Yalnız `boatId` ile sorgulansaydı bir
> işletme başka bir işletmenin doluluk bilgisini öğrenebilirdi —
> rakip istihbaratı. Kapsam filtresi bu projede her depoda var.

**satır 206**

> ⚠️ Yalnız ÖDENMİŞ ve BİNMİŞ rezervasyonlar. `Pending`
> olanlar tutma süresi dolunca kendiliğinden düşüyor;
> onları saymak işletmeyi olmayan bir yükümlülükle
> korkuturdu.

**satır 245**

> ⚠️ Yürürlükteki adres bulunamazsa `null` dönüyoruz: yönlendirecek
> hedefi olmayan bir eski adres, sonsuz döngüye ya da boş bir
> `Location` başlığına yol açardı.

**satır 257**

> ⚠️ ÖNCE ESKİSİ GEÇMİŞE, SONRA YENİSİ. Ters sırada
> `UX_BoatSlugs_Yururlukte` iki yürürlükteki adresi reddederdi —
> `A-03e`'deki sahiplik devrinde öğrenilen sıra kuralının aynısı.


## `src/DailyCruising.Infrastructure/Catalog/PricingCatalogRepository.cs`

**satır 10**

> <summary>
> ⚠️ HER SORGU KAPSAM ZİNCİRİNİN TAMAMINI TAŞIR: fiyat → kiralama tipi →
> tekne → işletme. Kısayol (yalnız `priceId` ile bulma) bilerek yok.
> </summary>

**satır 48**

> ⚠️ Tek sorguda: ayrı bir "temel fiyatı var mı" çağrısı N+1
> üretirdi ve panelde tip sayısı kadar gidiş-dönüş olurdu.

**satır 128**

> <summary>
> ⚠️ `ToDictionary` PROJEKSİYONUN İÇİNDE ÇAĞRILAMAZ — EF onu SQL'e
> çeviremiyor ve istek çalışma anında `InvalidOperationException` ile
> düşüyor (`The LINQ expression 't => t.LanguageCode' could not be
> translated`). Derleyici bunu görmez; canlı istek atınca **500** çıktı.
>
> Çözüm sorguyu ikiye bölmek DEĞİL: çeviriler düz bir liste olarak
> çekiliyor (hâlâ tek sorgu, N+1 yok) ve sözlüğe bellekte dönüşüyor.
> </summary>

**satır 222**

> <summary>
> ⚠️ `EX_Prices_NoOverlappingSeasons` bir EXCLUDE kısıtı, benzersiz indeks
> DEĞİL — SqlState `23P01` (ExclusionViolation) döner, `23505` değil.
> `UniqueViolation` beklenseydi çakışan sezon çıplak 500 verirdi.
> </summary>

**satır 240**

> ⚠️ CHECK KISITLARI (23514). Uygulama katmanı bunların çoğunu zaten
> kontrol ediyor ama tam örtüşme GARANTİ DEĞİL: biri değişip diğeri
> unutulursa hata buraya düşer. Yakalanmasaydı çıplak 500 dönerdi.
> Denetim bulgusu (2026-08-26); altı kısıt canlı sayıldı.

**satır 259**

> ⚠️ `RESTRICT` ihlali **23001**, 23503 DEĞİL.
>
> Denetim bunun ölü kod olduğunu, EF'in `Restrict`'inin `NO ACTION`
> ürettiğini ve 23503 fırlatacağını söyledi. Canlı denendi: FK'ler
> gerçekten `RESTRICT` (`confdeltype = 'r'`) ve silme denemesi
> `23001: violates RESTRICT setting` verdi. Kol YAŞIYOR (2026-08-26).

**satır 268**

> ⚠️ `ForeignKeyViolation` İKİ ANLAMA GELİR ve ayrımı kısıt adının
> ÖNEKİ yapar, içinde geçmesi DEĞİL: `FK_BoatRentalTypes_Boats_BoatId`
> (gelen) ile `FK_Reservations_BoatRentalTypes_...` (giden) İKİSİ DE
> "BoatRentalType" içeriyor. `Contains` ile ayırmaya çalışmıştım ve
> gelen-kayıt-geçersiz durumu "kullanımda, silinemiyor" mesajı
> alıyordu. Denetim bulgusu (2026-08-26).


## `src/DailyCruising.Infrastructure/Jobs/DispatchNotificationsJob.cs`

**satır 11**

> <summary>
> Giden kutusundaki bildirimleri gönderir (`A-28`).
>
> ⚠️ BAŞARILI GÖNDERİMDE SATIR SİLİNİYOR. Satır alıcı adresi, telefon ve
> gövdede ad taşıyor; kalsaydı kişisel verinin kalıcı ikinci bir kopyası
> oluşurdu ve `A-12` anonimleştirmesi onu da temizlemek zorunda kalırdı.
> Kalıcı iz `EventLogs`'ta ve orada kişisel veri yok.
> </summary>

**satır 84**

> ⚠️ Sağlayıcı mesajı kesiliyor: kimlik bilgisi ya da müşteri
> verisi içerebilir ve bu kolon `Failed` satırlarda kalıcı.


## `src/DailyCruising.Infrastructure/Jobs/ExpireOffersJob.cs`

**satır 11**

> <summary>
> Süresi dolan özel teklifleri kapatır ve tuttukları tarihi serbest bırakır.
>
> ⚠️ Bu iş çalışmazsa tarih SONSUZA KADAR kapalı kalır: teklif, takvimde
> `VoyageType = Offer` bir sefer açarak tarihi tutuyor ve `EXCLUDE` kısıtı o
> aralıkta başka sefer açılmasını engelliyor. Teklif kapanmazsa o tekne o
> tarihte hiç satılamaz — üstelik sebebi takvimde görünmez, çünkü kayıt bir
> "satış" gibi durur.
>
> Seferi silmiyoruz, `Cancelled`'a çekiyoruz: `EXCLUDE` kısıtı iptal edilmiş
> seferleri zaten dışlıyor, ve teklifin tarihi tuttuğu kaydı silmek geçmişi
> yok etmek olurdu.
> </summary>


## `src/DailyCruising.Infrastructure/Jobs/ExpireReservationHoldsJob.cs`

**satır 12**

> <summary>
> Süresi dolan 15 dakikalık rezervasyon tutmalarını serbest bırakır.
>
> ⚠️ Bu iş çalışmazsa sistem KENDİNİ KİLİTLER: ödeme ekranında terk edilen her
> rezervasyon koltukları tutmaya devam eder ve `CHECK (SoldSeats &lt;= Capacity)`
> kısıtı sefer dolduğunda yeni satışı reddeder. Sefer bir daha satılamaz.
>
> Koltukları burada elle azaltmıyoruz: durumu `Expired`'a çekmek yeterli,
> `trg_reservation_sync_seats` sayacı kendisi yeniden hesaplıyor. Sayaç tek
> bir yerden yönetildiği için buradaki bir hata onu bozamaz.
>
> ⚠️ AMA KOLTUK YETMİYOR — SEFER DE BIRAKILMALI. 2026-08-24 güvenlik
> denetiminde bulundu ve CANLI üretildi: `Expired` rezervasyonun açtığı
> `Voyage` satırı `Planned` kalıyordu ve `EX_Voyages_NoOverlapPerBoat`
> kısıtı `Voyage.Status`'a baktığı için o tekne o tarih aralığında
> **turun bitişine kadar** satılamıyordu.
>
> Sonuç, kimliksiz ve bedava bir takvim kilidiydi: bir çarter için istek
> atıp ödemeyi hiç yapmayan biri, tekneyi 3 günlüğüne kapatıyordu. Aynı
> hata sınıfı `Offer` akışında daha önce görülüp `ExpireOffersJob` ile
> çözülmüştü; A-22'de tekrarlanmıştı.
>
> Sefer YALNIZ canlı rezervasyonu kalmadığında iptal ediliyor: paylaşımlı
> seferde bir müşteri vazgeçse de diğerlerinin seferi sürmeli.
> </summary>

**satır 111**

> ⚠️ Anahtarlar Türkçeydi (`tutar`, `yetiskin`…), diğer
> bütün olaylar İngilizce. `EventLogs` üzerinde analitik
> sorgu yazan biri iki ayrı ad kümesiyle uğraşırdı ve
> tablo temizlenemediği için bu fark kalıcı olurdu.
> Üretim verisi yokken düzeltildi (2026-08-25).


## `src/DailyCruising.Infrastructure/Jobs/FetchExchangeRatesJob.cs`

**satır 9**

> <summary>
> Günlük kurları çeker ve saklar.
>
> ⚠️ Bu iş çalışmazsa **dövizli tekne satılamaz**: rezervasyon kuru dondurmak
> zorunda ve kur yoksa TL karşılığı hesaplanamaz. Sessiz bir bozulma değil,
> doğrudan satış kaybı.
>
> Kurlar saklanıyor çünkü "o gün kur neydi" sorusu üç ay sonra da sorulacak —
> hakediş ve anlaşmazlık bunun üzerinden yürüyecek.
> </summary>


## `src/DailyCruising.Infrastructure/Jobs/GeneratePayoutsJob.cs`

**satır 11**

> <summary>
> PERİYODİK HAKEDİŞ ÜRETİMİ (`A-18`).
>
> Sözleşmedeki `PayoutPeriodDays` (varsayılan 14) dolduğunda o işletmenin
> HENÜZ ÖDENMEMİŞ defter kayıtlarını bir `Payout` altında topluyor.
>
> ⚠️ PARA HAREKETİ YOK. Bu iş yalnız hakedişi HAZIRLIYOR (`Prepared`);
> gerçek transfer talimatı ödeme sağlayıcısına `A-29` ile gidecek.
> Ayrım bilinçli: hesabın doğruluğu transferden bağımsız denetlenebilmeli.
>
> ⚠️ NEGATİF HAKEDİŞ ÖDENMİYOR. Toplam sıfır ya da altındaysa `Payout`
> üretilmiyor ve kayıtlar bir sonraki döneme kalıyor — iade, kazançtan
> büyükse işletme borçlanmış olur ve platformun onu tahsil etme mekanizması
> YOK. Bir sonraki dönemin kazancı borcu kapatıyor.
> </summary>

**satır 91**

> ⚠️ NEGATİF ya da SIFIR hakediş ödenmiyor ve kayıtlar bir
> sonraki döneme KALIYOR. İade kazançtan büyükse işletme
> borçlanmış olur; platformun tahsil mekanizması yok, sonraki
> dönemin kazancı borcu kapatıyor.

**satır 114**

> ⚠️ `PayoutId` damgası UPDATE — ama `trg_ledger_entries_immutable`
> tetikleyicisi UPDATE'i reddediyor. Bu kolon o kuralın İSTİSNASI
> olmak zorunda: kaydın TUTARI değişmiyor, yalnız hangi ödemeye
> dahil olduğu işaretleniyor.


## `src/DailyCruising.Infrastructure/Jobs/ProcessRefundsJob.cs`

**satır 13**

> <summary>
> İADEYİ OTOMATİK GÖNDERİR (`A-56`, Mert 2026-08-26).
>
> İlk tasarımda iade ELLE tetikleniyordu; gerekçem *"yanlış tutar
> müşteriden geri istenemez"* idi. Mert otomatiği seçti ve gerekçem
> zayıftı: **tutar iptal ANINDA donuyor** (`Reservations.RefundDueTry`) ve
> formülü test edilmiş. Otomatikleşen şey bir hesap değil, yalnız gönderme
> adımı.
>
> ⚠️ SORGU, SERVİSİN ÖN KOŞULLARINI AYNEN YANSITIYOR — ve bu bir üslup
> tercihi değil, sonsuz döngü koruması. `RefundService` ön koşulu
> tutmayan bir rezervasyonda İSTİSNA atıyor ve `Refunds` satırı
> YAZILMADAN dönüyor; yani deneme sayacı artmıyor. Sorgu o kayıtları
> dışarıda bırakmasaydı iş onları her çalışmada tekrar dener, her
> çalışmada patlar ve sayaç hiç ilerlemezdi.
>
> ⚠️ DENEME SAYACI AYRI BİR KOLON DEĞİL. Başarısız her deneme geriye bir
> `Failed` satırı bırakıyor (kısmi benzersiz indeks yalnız `Failed`
> olmayanı tekilleştiriyor), yani satır sayısı DENEME SAYISININ KENDİSİ.
> Ayrı bir sayaç ikinci bir gerçek kaynağı olurdu.
> </summary>

**satır 112**

> ⚠️ HER REZERVASYON KENDİ BAŞINA. Biri patlarsa turun geri
> kalanı devam etmeli; tek bir sorunlu kayıt bütün iade
> kuyruğunu durdurmamalı.

**satır 117**

> ⚠️ SEBEP REZERVASYONDAN (`A-54`). Sabit
> `CustomerCancellation` yazılıydı ve askıya alma yüzünden
> iptal edilen bir tur da "müşteri vazgeçti" diye
> raporlanırdı — `A-57`'nin eklediği ayrım tam da bunu
> önlemek içindi.

**satır 150**

> <summary>
> ⚠️ TÜKENEN DENEME SESSİZ KALMAMALI.
>
> Bu kontrol olmasaydı iş, beşinci denemeden sonra rezervasyonu
> sorgudan düşürür ve bir daha hiç bakmazdı: müşteri parasını bekler,
> sistem "iptal edildi" der ve hiçbir yerde "bu iade yapılamadı"
> yazmazdı. Sessiz bırakma, başarısızlığın kendisinden pahalı.
> </summary>


## `src/DailyCruising.Infrastructure/Jobs/SendReviewInvitationsJob.cs`

**satır 12**

> <summary>
> YORUM DAVETİNİ ÜRETİR VE E-POSTAYA KOYAR (`A-40`).
>
> `A-35` daveti TÜKETEN uçları yazdı; üreten yoktu ve `ReviewInvitations`
> satırı elle kuruluyordu. Bu iş o boşluğu kapatıyor.
>
> ⚠️ DAVET YALNIZ BİNİŞ YAPMIŞ REZERVASYONA GİDİYOR. Yorum hakkı rezervasyon
> yapmakla değil FİİLEN TEKNEYE BİNMEKLE doğuyor ([[domain-gereksinimler]]
> 2026-08-22). Servis katmanı bunu zaten reddediyor (`NotBoarded`) — ama
> daveti göndermek, karşılığı olmayan bir e-posta atmak olurdu: müşteri
> tıklar, "katılmadınız" der ve platformdan şüphelenir.
>
> ⚠️ DÜZ METİN JETON YALNIZ E-POSTAYA GİRİYOR. Veritabanına SHA-256 özeti
> yazılıyor; salt-okunur bir yedek sızarsa düz metin jeton listesi doğrudan
> kullanılabilir olurdu.
> </summary>

**satır 46**

> <summary>
> Tur BİTTİKTEN sonra ne kadar beklenecek.
>
> ⚠️ Sıfır olsaydı davet, müşteri daha iskeleye varmadan giderdi.
> Üç saat, günlük bir turun toparlanma süresi — ama bu bir TAHMİN
> -> [[api-benim-kararlarim]]
> </summary>

**satır 75**

> ⚠️ ÜÇ KOŞUL BİRDEN, ve üçü de gerekli:
>   `BoardedAt != null` → yorum hakkı binişle doğuyor
>   `EndsAt < esik`     → tur bitmiş olmalı
>   davet YOK           → aynı rezervasyona ikinci davet gitmemeli
>
> Üçüncüsü olmasaydı her tur bu işi tekrar tetikler ve müşteri her
> saat bir "değerlendirin" e-postası alırdı.

**satır 104**

> ⚠️ ERKEN DÖNÜŞ YOK — hatırlatma ondan SONRA çalışıyor.
>
> İlk yazdığımda burada `if (adaylar.Count == 0) return 0;` vardı ve
> hatırlatma HİÇ çalışmıyordu: yeni davet üretilecek rezervasyon
> kalmadığı anda iş dönüyordu. Tam da hatırlatmanın gerektiği durum
> buydu — davetler çoktan gönderilmiş, kimse yorum yazmamış.
> Test yakaladı.

**satır 139**

> ⚠️ `Reference` rezervasyon kimliği: gönderim başarısız olursa
> destek hangi tura ait olduğunu bulabilmeli.

**satır 148**

> ⚠️ DAVET VE E-POSTA AYNI KAYDETMEDE. Ayrı olsalardı araya giren bir
> hata ya "jetonu olan ama e-postası gitmeyen" ya da "e-postası giden
> ama jetonu olmayan" bir davet bırakırdı — ikincisinde müşteri
> geçersiz bir link tıklardı.

**satır 160**

> <summary>
> KULLANILMAMIŞ DAVETE BİR KEZ HATIRLATMA (`A-50`, Mert soru 8).
>
> ⚠️ `ReminderSentAt` OLMADAN YAZILAMAZDI. İş saatlik çalışıyor ve
> "7 gün geçmiş, yorum yazılmamış" koşulu her saat DOĞRU kalırdı —
> müşteri aynı hatırlatmayı saatte bir alırdı. Alan, "gönderildi mi"
> sorusunun tek cevabı.
>
> ⚠️ DÜZ METİN JETON YENİDEN ÜRETİLEMİYOR: veritabanında yalnız
> SHA-256 özeti var. Bu yüzden hatırlatma linki değil, davetin
> **süresi dolmadan** yeniden gönderilecek bir link taşıyamıyor —
> çözüm, hatırlatmada YENİ bir jeton üretip eskisinin yerine
> koymak. Eski jeton geçersizleşiyor ve bu doğru: ilk e-postadaki
> link artık çalışmıyorsa müşteri ikincisini kullanır.
> </summary>


## `src/DailyCruising.Infrastructure/Jobs/TcmbExchangeRateSource.cs`

**satır 8**

> <summary>
> TCMB günlük kur bülteni (`https://www.tcmb.gov.tr/kurlar/today.xml`).
>
> ⚠️ HANGİ KUR — Mert'in kararını bekliyor, şimdilik `ForexSelling`.
> TCMB dört değer yayınlıyor: döviz alış/satış ve efektif alış/satış. Seçim
> müşterinin ödeyeceği tutarı değiştiriyor: bugün EUR alış 55,99 satış 56,09,
> yani €500'lük bir turda müşteri arasındaki fark ~50 TL.
>
> `ForexSelling` seçildi çünkü platform, yabancı para cinsinden bir borcu TL'ye
> çeviriyor ve satış kuru bu yönün standardı. Ayrıca platform lehine ihtiyatlı:
> kur satış-alış aralığında dalgalanırsa platform zarar etmiyor.
> </summary>


## `src/DailyCruising.Infrastructure/Messaging/MessagingRepository.cs`

**satır 10**

> <summary>
> ⚠️ KAPSAM İKİ TARAFLI: müşteri `CustomerUserId`'siyle, işletme
> `Boat.PartnerId`'siyle erişiyor. Her sorgu İKİSİNİ BİRDEN `WHERE`'e koyuyor
> ve hangisinin geçtiği çağırana göre değişiyor — üçüncü bir kişi hiçbir
> koşulu sağlamıyor.
> </summary>

**satır 23**

> <summary>
> ⚠️ Yalnız AÇIK konuşma (`A-51`). Kapanmışları da döndürseydi yeni
> konuşma hiç açılamaz, müşteri bindiği tekneye bir daha yazamazdı.
> </summary>

**satır 61**

> ⚠️ `MaskedBody` seçiliyor, `Body` DEĞİL. Orijinal metin
> yalnız platform yönetiminde ve bu projeksiyon onu hiç
> okumuyor — "yanlışlıkla döndürmek" için önce bu satırı
> değiştirmek gerekir.

**satır 147**

> <summary>
> ⚠️ Tek `UPDATE` — mesajları çekip döngüde işaretlemek konuşma
> uzadıkça yavaşlar ve bu uç her ekran açılışında çağrılıyor.
> </summary>

**satır 167**

> <summary>
> ⚠️ Toplam VERİTABANINDA hesaplanıyor, mesajlar çekilip toplanmıyor:
> uzun bir konuşmanın tüm gövdelerini belleğe almak, hem gereksiz hem
> de orijinal (maskelenmemiş) metinleri dolaştırmak olurdu.
> </summary>


## `src/DailyCruising.Infrastructure/Messaging/OfferRepository.cs`

**satır 15**

> <summary>
> ⚠️ Zaman aralığı `BoatRentalTypes.StartTime/EndTime`'dan kuruluyor.
> Çok günlü tiplerde `DurationDays` de ekleniyor — `PricingService`'in
> yaptığının BASİTLEŞTİRİLMİŞİ değil, aynısı olmak zorunda; ayrışırsa
> teklif seferi rezervasyon seferinden farklı bir aralık tutar ve
> çakışma kısıtı yanlış cevap verir -> [[api-benim-kararlarim]]
> </summary>

**satır 126**

> ⚠️ ZORUNLU. `CK_Voyages_RentalTypeRequired`: `Block` dışındaki
> her seferde kiralama tipi dolu olmalı — sefer "hangi ürünün
> takvimi" sorusuna cevap veremezse kapasite ve süre kimden
> gelecek belli olmaz. İlk sürümde atlanmıştı ve kısıt yakaladı
> (canlı deneme, 2026-08-26).

**satır 133**

> ⚠️ `VoyageType.Offer` — `Sale` DEĞİL. Arama `KalanKoltuk` içinde
> `Offer` seferini `Sale` gibi sayıyor (tarih dolu görünüyor) ama
> `CompleteVoyagesJob` yalnız `Sale` seferlerini tamamlıyor:
> kabul edilmemiş bir teklif "yapılmış tur" sayılmamalı.

**satır 166**

> ⚠️ `23P01`, `23505` DEĞİL — EXCLUDE kısıtı benzersiz indeks
> değil. Çevrilmediğinde satıcı çıplak **500** görüyordu ve
> "tarih dolu" olduğunu anlamıyordu (canlı deneme, 2026-08-26).

**satır 193**

> <summary>
> ⚠️ `Include` ŞART: kabul akışı `Conversation.Boat.PartnerId` ve
> `Voyage.DepartureDate` okuyor. Yüklenmediğinde bunlar `null` geliyor ve
> kabul **500** ile düşüyordu (canlı deneme, 2026-08-26) — derleyici
> gezinti özelliğinin dolu olduğunu varsayıyor, çalışma anı varsaymıyor.
> </summary>

**satır 271**

> <summary>
> ⚠️ `Status = Sent` KOŞULU `WHERE`'DE. Müşteri kabul ederken satıcı
> iptal ederse, ikisi de kendi okumasına göre yazar ve son yazan
> kazanırdı — üstelik biri seferi bırakırken diğeri onu satışa çevirirdi.
> </summary>

**satır 286**

> ⚠️ Durum ve rezervasyon kimliği AYNI `UPDATE`'te.
> `CK_Offers_Accepted` ikisinin eşzamanlı olmasını istiyor:
> önce `Accepted` yazıp sonra kimliği eklemek, aradaki anda
> kısıtı ihlal ediyor ve **500** veriyordu (canlı deneme,
> 2026-08-26). Kısıt haklı — "kabul edildi ama rezervasyonu
> yok" bir teklif anlamsız.

**satır 296**

> <summary>
> ⚠️ Sefer SİLİNMİYOR, `Cancelled`'a çekiliyor. Çakışma kısıtı
> `WHERE "Status" <> 'Cancelled'` ile çalışıyor, yani iptal tarihi
> serbest bırakıyor — ama kayıt duruyor ve "bu tarih neden bir süre
> doluydu" sorusu cevaplanabiliyor -> [[api-desenler]].
> </summary>


## `src/DailyCruising.Infrastructure/Notifications/EmailSenders.cs`

**satır 59**

> ⚠️ ALICI ADRESİ LOGLANMIYOR. Bu satır önce `{To}` da yazıyordu ve
> hemen aşağıdaki `PostmarkEmailSender` tam tersini yapıp gerekçesini
> de yazıyordu — yani kendi kuralımı bir sınıf sonra çiğnemişim.
> Uygulama günlükleri `EventLogs` kadar korumalı değil ve e-posta
> adresi kişisel veri. Denetim bulgusu (2026-08-25).

**satır 70**

> <summary>
> Postmark ile gönderim (Mert, 2026-08-25). İşlemsel postada teslimat
> kalitesi için seçildi: rezervasyon onayı spam'e düşerse müşteri kodunu
> hiç görmez ve destek talebi olarak geri gelir.
>
> ⚠️ HTTP hataları YUTULMUYOR. `IEventLogger`'ın aksine bildirim gönderimi
> işin bir parçası: parola sıfırlama postası gitmediyse kullanıcı bunu
> bilmeli, sessizce "başarılı" dönmemeliyiz.
> </summary>

**satır 106**

> ⚠️ Alıcı adresi günlüğe YAZILMIYOR: uygulama günlükleri
> `EventLogs` kadar korumalı değil ve adres kişisel veri.
> Postmark'ın hata kodu sorunu teşhis etmeye yetiyor.


## `src/DailyCruising.Infrastructure/Notifications/ReservationNotificationThrottle.cs`

**satır 8**

> <summary>
> Sayaç olarak `Reservations` tablosunu kullanıyor: her rezervasyon tam olarak
> bir onay bildirimi üretiyor, yani "son bir saatte bu numaraya kaç rezervasyon
> açıldı" ile "kaç bildirim gitti" aynı sayı.
>
> ⚠️ NEDEN AYRI BİR SAYAÇ TABLOSU DEĞİL. Ayrı tablo, bildirim gönderilmeden
> önce yazılması gereken ikinci bir kayıt demek; hata durumunda ikisi ayrışır
> ve sayaç yalan söyler. Rezervasyon satırı zaten atılamaz bir gerçek.
>
> ⚠️ NEDEN BELLEK İÇİ SAYAÇ DEĞİL. Uygulama yeniden başlayınca sıfırlanır ve
> birden fazla sunucuda her biri kendi sayacını tutar — saldırgan için
> sınır fiilen sunucu sayısıyla çarpılır.
> </summary>

**satır 51**

> ⚠️ Sessiz değil. Meşru bir müşteri sınıra takılırsa bunun görülmesi
> gerekiyor — sınır yanlış ayarlanmışsa tek belirtisi bu satır olur.
> İletişim bilgisi YAZILMIYOR: kişisel veri ve zaten `Reservations`'ta.


## `src/DailyCruising.Infrastructure/Notifications/ReservationNotifier.cs`

**satır 7**

> <summary>
> REZERVASYON ONAYI — e-posta ve SMS.
>
> Domain kuralı (Mert, şema kararı): *"Rezervasyon tamamlanınca müşteriye HEM
> e-posta HEM SMS gider; ikisinde de rezervasyon bilgileri ve bir rezervasyon
> kodu bulunur. Sonuç: telefon zorunlu alan."*
>
> ⚠️ Bu kural yazılıydı ama HİÇ UYGULANMAMIŞTI: `SendSmsAsync` kod tabanında
> hiçbir yerden çağrılmıyordu ve rezervasyon onayı yalnız HTTP cevabında
> dönüyordu. Müşteri sekmeyi kapatınca kodunu kaybediyordu (2026-08-25'te
> `G-04` cevaplanınca ölçüldü).
>
> ⚠️ SINIF `Infrastructure`'DA, `Application`'da DEĞİL. Günlükleme için
> `ILogger` gerekiyor ve `Application` katmanı bilerek HİÇBİR pakete bağlı
> değil — `AppUrlOptions`'ın `IOptions&lt;&gt;` yerine düz sınıf olmasının
> sebebi de bu. Bağımlılık yönü bir tek yerde bile delinirse kural biter.
>
> ⚠️ GÖNDERİM HATASI REZERVASYONU BOZMAZ. Rezervasyon zaten oluştu ve
> koltuklar tutuldu; sağlayıcı erişilemez diye onu geri almak, müşteriyi
> hiçbir şey kazanmadan kaybetmek olurdu. Hata gürültülü biçimde günlüğe
> yazılıyor ve kod HTTP cevabında zaten dönüyor.
> </summary>

**satır 40**

> ⚠️ HEDEF BAZLI SINIR. Bu uç kimliksiz ve iletişim bilgisinin
> SAHİPLİĞİNİ doğrulamıyor; gönderim bağlanmadan önce oraya üçüncü bir
> kişinin numarasını yazmanın etkisi yoktu, artık var. IP sınırı vekil
> havuzuyla aşılıyor, kurbanın numarası aşılamıyor.

**satır 52**

> ⚠️ ARTIK DOĞRUDAN GÖNDERİLMİYOR, KUYRUĞA YAZILIYOR (`A-28`).
>
> Önce HTTP cevabı Postmark ve Netgsm'in cevabını bekliyordu ve
> sağlayıcı o an erişilemezse bildirim KAYBOLUYORDU — müşteri
> rezervasyon kodunu hiç almıyordu.
>
> Kuyruğa yazmak aynı işlemin parçası: rezervasyon oluştuysa bildirim
> de sırada demektir, ikisi birlikte ya var ya yok.


## `src/DailyCruising.Infrastructure/Notifications/SmsSenders.cs`

**satır 19**

> <summary>
> Netgsm ile SMS (Mert, 2026-08-25).
>
> Türkiye'ye SMS'te iki yerel kısıt var ve yurt dışı sağlayıcıları eleyen
> şey bunlar:
>   1. Gönderici başlığı operatörden ÖNCEDEN onaylı olmalı
>   2. İYS — rezervasyon onayı "hizmeti bilgilendirme" sayılıyor ve izin
>      gerektirmiyor; pazarlama SMS'i gönderilirse İYS kaydı zorunlu
>
> ⚠️ Netgsm HTTP 200 döndürüp GÖVDEDE hata kodu verebiliyor. Yalnız durum
> koduna bakan bir kod, gönderilmemiş SMS'i başarılı sayar — bu yüzden gövde
> de ayrıştırılıyor.
> </summary>

**satır 58**

> ⚠️ YEREL DOĞRULAMA. Önce yalnız uzak API'nin hata koduna
> güveniliyordu: `"abc"` gibi bir girdi BOŞ `gsmno` ile gönderiliyor,
> Netgsm "70" (eksik parametre) dönüyordu. Yani her bozuk numara bir
> ağ turu ve bir hata günlüğü üretiyordu — hem gürültü hem gecikme.
>
> Şemada telefon serbest metin; `[Phone]` doğrulaması yok ve
> `ContactPhone` müşterinin yazdığı şey. Denetim bulgusu (2026-08-25).

**satır 94**

> ⚠️ ASIL KONTROL BURADA. Netgsm başarısız gönderimde de HTTP 200
> dönüyor; hata yalnız gövdede. Bunu atlayan bir kod "SMS gitti"
> sanır ve müşteri rezervasyon kodunu hiç almaz.


## `src/DailyCruising.Infrastructure/Partners/PartnerApplicationRepository.cs`

**satır 55**

> <summary>
> ⚠️ `IsPartnerAssignable` FİLTRESİ ŞART. Filtresiz alınsaydı sahip
> rolüne komisyon değiştirme, defter okuma ve yetki yönetimi gibi
> PLATFORM yetkileri de bağlanırdı — ve
> `trg_role_permission_assignable` tetikleyicisi başvuruyu reddeder,
> yani hiç kimse kaydolamazdı.
> </summary>

**satır 148**

> ⚠️ Kısıt adları veritabanından DOĞRULANDI (2026-08-26).
> Tanınmayan bir ihlal yutulmuyor: yutulsaydı bambaşka bir kısıt
> "bu e-posta kayıtlı" diye raporlanır ve gerçek sebep kaybolurdu.


## `src/DailyCruising.Infrastructure/Partners/PartnerStaffRepository.cs`

**satır 11**

> <summary>
> ⚠️ KAPSAM FİLTRESİ BURADA. Her sorgu `partnerId` alıyor ve `WHERE` cümlesine
> koyuyor. Servis katmanı "bu benim mi" diye kontrol etmiyor — etseydi, o
> kontrolü unutan yeni bir çağrı yolu başka işletmenin verisini sessizce
> döndürürdü ve hiçbir yerde hata görünmezdi.
> </summary>

**satır 30**

> <summary>
> ⚠️ `IsPartnerAssignable` FİLTRESİ BURADA DA VAR ve olmak zorunda.
> Sorgu yalnız anahtara baksaydı, çağıran `commission.edit` yazarak
> platforma özel bir yetkiyi role koyabilirdi — servis katmanındaki
> katalog kontrolü bu metodun sonucuna güveniyor.
> </summary>

**satır 71**

> <summary>
> ⚠️ `ToLower()` YOK, bilerek. `Roles.Name` kolonu `citext`; karşılaştırma
> zaten büyük/küçük harf duyarsız ve `IX_Roles_PartnerName` benzersiz
> indeksi de aynı semantikle çalışıyor.
>
> `ToLower()` kullanılsaydı iki sorun olurdu: indeks kullanılamaz hale
> gelirdi ve uygulama ile veritabanı FARKLI kurallara göre karar verirdi.
>
> Bu kontrol yine de "önce bak sonra yaz"; eşzamanlı iki istek arasına
> girilebilir. Kapıyı kapatan şey benzersiz indeks
> (`SaveWithRaceHandlingAsync` onu anlaşılır hataya çeviriyor); buradaki
> kontrol yalnız normal akışta güzel bir mesaj vermek için.
> </summary>

**satır 93**

> <summary>
> Rol başına AKTİF çalışan sayısı.
>
> ⚠️ `Status == Active` filtresi şart. Çıkarılmış çalışanın satırı
> duruyor; sayılsaydı kullanılmayan bir rol "kullanımda" görünüp
> silinemezdi.
> </summary>

**satır 111**

> <summary>
> ⚠️ `Status` FİLTRESİ YOK, bilerek. Çıkarılmış çalışanın satırı duruyor ve
> `RoleId`'si rolü işaret etmeye devam ediyor; veritabanındaki RESTRICT
> yabancı anahtarı silmeyi zaten reddeder. Buradaki kontrol o hatayı
> anlaşılır bir mesaja çeviriyor.
> </summary>

**satır 142**

> <summary>
> ⚠️ ÜÇ ADIM, TEK İŞLEM ve SIRA ÖNEMLİ.
>
> `IX_PartnerMembers_SingleOwner` (`UNIQUE (PartnerId) WHERE IsOwner`)
> işletme başına tek sahip garantisi veriyor. Önce yeni sahibi
> işaretlemek arada bir an İKİ sahip yaratır ve indeks devri reddeder.
> Bu yüzden ÖNCE eski sahibin bayrağı düşüyor.
>
> Roller de takas ediliyor: yeni sahip sahip rolünü, eski sahip yeninin
> önceki rolünü alıyor. Eski sahip sahip rolünde bırakılsaydı `IsOwner`
> olmadan tam yetkili bir üye kalırdı ve "sahip kim" sorusunun iki
> cevabı olurdu.
> </summary>

**satır 183**

> <summary>
> ⚠️ Çıkarılmış çalışan da DÖNÜYOR (`Status` filtresi yok). Panel
> "kimi çıkarmıştım" sorusunu cevaplayabilmeli ve aynı kişi yeniden
> eklenirken mevcut satırın güncelleneceği buradan görülüyor.
> </summary>

**satır 222**

> <summary>
> ⚠️ Yeni damga KODDA üretiliyor, veritabanı varsayılanı beklenmiyor:
> `ExecuteUpdate` varsayılanı tetiklemiyor, yalnız verilen değeri yazıyor.
> Varsayılana güvenilseydi damga hiç değişmez ve koruma sessizce
> çalışmazdı.
> </summary>

**satır 272**

> ⚠️ Burada bir de `db.RolePermissions.Local` taraması ve
> `Entry(...).State = Deleted` döngüsü vardı; KALDIRILDI. Ölü koddu:
> `RemoveRange(sorgu)` sonuçları kimlik haritasından çözüyor, yani
> zaten izlenen satırları AYNI nesne olarak bulup siliyor. İki
> mekanizma okuyanı "kapatılan bir açık var" sanmaya itiyordu.
> Denetim bulgusu (2026-08-25).

**satır 296**

> <summary>
> ⚠️ Yeniden deneme stratejisi (`EnableRetryOnFailure`) açık OLMAMALI —
> açıksa çıplak `BeginTransactionAsync` istisna fırlatır ve
> `IExecutionStrategy.ExecuteAsync` ile sarmalamak gerekir. Bugün açık
> değil (`Program.cs`), açılırsa burası da değişmeli.
> </summary>


## `src/DailyCruising.Infrastructure/Payments/FakePaymentProvider.cs`

**satır 9**

> <summary>
> GELİŞTİRME SAĞLAYICISI. Gerçek para hareketi yok; 3D Secure akışını
> taklit ediyor.
>
> Neden var: ödeme akışının tamamı (rezervasyon → ödeme → defter → `Paid`)
> sağlayıcı hesabı olmadan uçtan uca çalışabilsin ve arayüz tarafı
> beklemeden geliştirilebilsin diye.
>
> ⚠️ ÜRETİMDE KULLANILAMAZ. `Program.cs` üretimde bu sağlayıcıyla açılmayı
> reddediyor — yoksa uygulama sorunsuz açılır, müşteriler "ödedim" der ve
> hiçbir para tahsil edilmez.
> </summary>

**satır 60**

> <summary>
> ⚠️ HER ZAMAN BAŞARILI DÖNMÜYOR. İşlem kimliği `fail` içeriyorsa
> başarısız dönüyor — başarısızlık yolunun da test edilebilmesi için.
> Yalnız mutlu yolu taklit eden bir sahte, hata yollarını hiç
> çalıştırmadan "çalışıyor" hissi verirdi.
> </summary>

**satır 77**

> <summary>
> ⚠️ ALICI KAYDI SAHTE AMA GERÇEKÇİ (`A-41`). Gerçek bir anahtar
> üretiyor ki bölüştürme akışı uçtan uca çalışsın: İyzico hesabında
> pazaryeri özelliği açılana kadar geliştirme ve test durmasın.
>
> Para hareketi YOK — sahte sağlayıcı üretimde zaten açılmıyor.
> </summary>

**satır 142**

> <summary>
> İyzico kimlik bilgileri ve adresi.
>
> ⚠️ `ApiKey` ve `SecretKey` BURAYA VARSAYILAN DEĞER ALMAZ ve
> `appsettings.json`'a YAZILMAZ — geliştirmede `dotnet user-secrets`,
> üretimde ortam değişkeni. Boş bırakılırsa üretimde uygulama AÇILMAZ
> (`Program.cs`); yoksa her ödeme çağrısı sağlayıcıda reddedilir ve bunu
> ancak ilk müşteri ödeyemediğinde görürdük.
>
> `BaseUrl` sır değil, bu yüzden `appsettings.json`'da: sandbox ile üretim
> AYNI kimlik bilgisini kabul etmez, ayrım adresle yapılır.
> </summary>


## `src/DailyCruising.Infrastructure/Payments/IyzicoPaymentProvider.cs`

**satır 13**

> <summary>
> İYZİCO (`A-29`). Doğrulandı: 2026-08-26, sandbox, Mert'in kendi hesabı.
>
> ⚠️ KART BİLGİSİ BU SUNUCUYA HİÇ GELMİYOR. **Checkout Form** kullanılıyor:
> müşteri kart bilgisini İyzico'nun barındırdığı sayfaya giriyor, biz yalnız
> bir adrese yönlendiriyoruz. Alternatif olan doğrudan `/payment/auth` ucu
> kart numarasını bizim sunucumuzdan geçirirdi ve PCI kapsamına girerdik —
> `PaymentStartRequest` içinde kart alanı OLMAMASI zaten bu tercihi
> söylüyordu.
>
> Akış:
>   1. `StartAsync`  → `/payment/iyzipos/checkoutform/initialize/auth/ecom`
>                       dönen `token` bizim işlem kimliğimiz, `paymentPageUrl`
>                       müşterinin gideceği adres
>   2. `CompleteAsync` → `/payment/iyzipos/checkoutform/auth/ecom/detail`
>                       İyzico geri dönüşünde `token` POST ediyor
>   3. `RefundAsync`  → önce detay (işlem kırılımını bulmak için),
>                       sonra `/payment/refund`
> </summary>

**satır 42**

> <summary>
> ⚠️ TCKN TOPLAMIYORUZ ama İyzico ZORUNLU tutuyor (ölçüldü: alan
> çıkarıldığında `errorCode 8 — identityNumber gönderilmesi zorunludur`).
>
> Bu değer BİLEREK GEÇERSİZ bir TCKN: 11 hanenin son basamağı doğrulama
> kuralını tutmuyor, yani hiçbir gerçek kişiye ait olamaz. Rastgele
> geçerli bir numara üretmek, var olan birinin kimlik numarasını
> gerçek bir ödemeye bağlamak olurdu.
>
> **Mert'in kararı gerekiyor** — ödeme adımında TCKN sorulacak mı →
> [[api-benim-kararlarim]]
> </summary>

**satır 100**

> ⚠️ BÖLÜŞTÜRME (`A-41`). İyzico'nun pazaryeri modelinde alıcı ve ona
> gidecek tutar SEPET KALEMİNE yazılıyor, isteğin köküne değil —
> çünkü çok kalemli bir sepette her kalem farklı satıcıya ait
> olabilir. Bizde tek kalem var ama alanın yeri bu.
>
> İkisi birlikte gitmek zorunda: yalnız anahtar gönderilirse İyzico
> tutarı bilemez, yalnız tutar gönderilirse kime gideceğini.

**satır 170**

> ⚠️ TUTAR TEYİDİ. Buraya kadar gelmiş bir ödeme "başarılı" ama NE
> KADAR tahsil edildiğini hâlâ sağlayıcıdan doğrulamadık. `paidPrice`
> DEĞİL `price` karşılaştırılıyor: taksitli ödemede `paidPrice` faizle
> birlikte DAHA YÜKSEK oluyor, `price` bizim istediğimiz tutar olarak
> kalıyor. `paidPrice` karşılaştırılsaydı her taksitli ödeme
> reddedilirdi.

**satır 221**

> ⚠️ `ip` alanı GÖNDERİLMİYOR. İyzico zorunlu tutmuyor (ölçüldü:
> alansız iade `success` döndü) ve elimizde iadeyi yapan personelin
> değil müşterinin IP'si olmalıydı — uydurma bir IP göndermek
> sahtekârlık kaydını kirletirdi.

**satır 247**

> <summary>
> ⚠️ YAZILMADI VE SEBEBİ HESAP SEVİYESİNDE (`A-41`).
>
> `POST /onboarding/submerchant` bu hesapta **`2000 — Bu servis sadece
> pazaryeri müşterilerine açıktır`** dönüyor. Üç farklı gövdeyle
> denendi (şahıs, limited, IBAN'sız), üçünde de AYNI hata — yani
> istek şekli hiç doğrulanmıyor, kapı hesapta.
>
> `/onboarding/submerchant/detail` ise `2001 — Alt üye işyeri
> bulunamadı` diyor: **okuma açık, yaratma kapalı.** Ölçüldü
> 2026-08-26.
>
> Gövde yazılmadı çünkü DOĞRULANAMAZDI — `A-29`'daki kararın aynısı.
> Doğrulanmamış para kodu "bitti" görünen ama ilk gerçek kullanımda
> patlayan bir şey bırakır.
>
> **Mert'ten gereken:** İyzico'dan sandbox (ve sonra üretim) hesabına
> **pazaryeri (marketplace) özelliğinin açılması.**
> </summary>

**satır 291**

> ⚠️ İMZA GÖVDENİN TAM METNİ ÜZERİNDEN hesaplanıyor. Gövde bir kez
> metne çevrilip HEM imzada HEM istekte aynı metin kullanılmalı;
> iki ayrı serileştirme (boşluk, alan sırası) imzayı bozar ve
> İyzico `1000 — Geçersiz imza` döner.

**satır 382**

> <summary>
> ⚠️ `InvariantCulture` ZORUNLU. Sunucu Türkçe kültürdeyse `1500.00`
> yerine `1500,00` üretilir ve İyzico tutarı ya reddeder ya YANLIŞ
> okur. Para biçimlendirmesinin kültüre bırakılması, kültür ayarı
> değiştiği gün sessizce yanlış tutar tahsil ettirir.
> </summary>


## `src/DailyCruising.Infrastructure/Payments/RefundRepository.cs`

**satır 17**

> <summary>
> ⚠️ Yalnız `Succeeded` ödeme. Başarısız ya da yarım kalmış bir ödemenin
> iadesi yoktur: o parayı hiç almadık.
> </summary>


## `src/DailyCruising.Infrastructure/Persistence/Configurations/BillingConfigurations.cs`

**satır 92**

> ⚠️ ÇİFT İADE KAPISI (`A-29`). Bir rezervasyonun aynı anda birden
> fazla AKTİF iadesi olamaz; `Failed` olanlar filtrenin dışında,
> çünkü başarısız bir iade tekrar denenebilmeli.
>
> Servis seviyesindeki durum kontrolü tek başına YETMEZ: eşzamanlı
> iki istek de rezervasyonu `Cancelled` görür, ikisi de sağlayıcıya
> talimat gönderir ve para İKİ KEZ çıkar. Kapı veritabanında.

**satır 178**

> ⚠️ PROJE KONVANSİYONUNDAN SAPMA, bilerek. Enum'lar metin
> saklanıyor ve hiçbirinin geçerli değer kısıtı yok; elle yazılan
> bir `UPDATE ... SET "FundedBy"='platform'` (küçük harf) sorunsuz
> yazılır, sonraki EF okuması `Enum.Parse` ile patlar ve o kupon
> tamamen kullanılamaz hale gelir — hatanın kaynağı da görünmez.
>
> Bu kolon PARA akışını belirlediği için istisna yapıldı: yanlış
> değer yalnız bir kaydı değil, bir tarafın hakedişini bozuyor.
> Denetim bulgusu (2026-08-25).


## `src/DailyCruising.Infrastructure/Persistence/Configurations/BoatSlugConfiguration.cs`

**satır 19**

> ⚠️ GLOBAL benzersiz. Dil ya da tekne kırılımında benzersiz olsaydı
> iki farklı tekne aynı adresi taşıyabilir ve `/tekne/mavi-yolculuk`
> hangisini açacağını bilemezdi.


## `src/DailyCruising.Infrastructure/Persistence/Configurations/ConsentDocumentConfiguration.cs`

**satır 17**

> ⚠️ Aynı tür + aynı sürüm İKİ KEZ olamaz: `ConsentRecord` yalnız
> sürüm etiketini saklıyor, çift kayıt "hangi metni onayladı"
> sorusunu belirsizleştirirdi.

**satır 22**

> ⚠️ TÜR BAŞINA TEK YÜRÜRLÜKTEKİ METİN — kısmi benzersiz indeks.
> İki yürürlükteki metin olsaydı başvuru ucu hangisini yazacağını
> bilemez ve onay kaydı rastgele birine bağlanırdı.


## `src/DailyCruising.Infrastructure/Persistence/Configurations/MessagingConfigurations.cs`

**satır 87**

> Konuşma (müşteri × tekne) bazlı — ikinci bir konuşma açılmaz.
> ⚠️ KISMİ BENZERSİZ (`A-51`, Mert soru 9): bir müşteri × tekne
> çifti için aynı anda YALNIZ BİR AÇIK konuşma olabilir, ama
> KAPANMIŞ konuşmalar birikebilir.
>
> Eskiden koşulsuz benzersizdi ve müşteri bindiği tekneye BİR DAHA
> HİÇ mesaj atamıyordu — gelecek sezon aynı tekneyi kiralamak istese
> bile. Filtre `A-29b`'deki iade indeksiyle aynı deseni izliyor.
>
> İki açık konuşma yasak kalıyor: hangisine yazılacağı belirsiz olur
> ve işletme aynı müşteriyi iki ayrı yerde cevaplardı.


## `src/DailyCruising.Infrastructure/Persistence/Configurations/PartnerConfigurations.cs`

**satır 36**

> ⚠️ IBAN BİÇİMİ VERİTABANINDA DOĞRULANIYOR (`A-41`).
>
> Türkiye IBAN'ı: `TR` + 24 rakam = 26 karakter. Yanlış biçimli bir
> IBAN uygulama katmanında sessizce geçseydi, hatayı ancak ödeme
> sağlayıcısı alıcı kaydını reddettiğinde — yani işletme parasını
> beklerken — görürdük.
>
> Boşluklu yazımı (`TR18 0006 ...`) kısıt REDDEDİYOR: normalleştirme
> uygulama katmanının işi ve veritabanı iki farklı biçimi eşit
> saymamalı, yoksa aynı hesap iki ayrı değer olarak durur.

**satır 91**

> "İşletmenin tüm çalışanları" panelin en sık sorgusu. Aşağıdaki kısmi
> indeks bu sorguda KULLANILAMAZ (filtresini içermiyor), düz indeks şart.
>
> ⚠️ BU SATIR ESKİDEN HİÇBİR ŞEY YAPMIYORDU.
>
> EF Core indeksleri PROPERTY KÜMESİNE göre anahtarlıyor: aşağıdaki
> `SingleOwner` indeksi (aynı kolon, `IsUnique` + filtre) bunu SESSİZCE
> eziyordu. Üretilen migration'da düz indeks hiç yoktu; `WHERE
> "PartnerId" = ...` sorguları seq scan yapıyordu ve yorum satırı
> olmayan bir indeksi anlatıyordu. Denetim (2026-08-25) yakaladı.
>
> `HasDatabaseName` YETMİYOR — o yalnız birleşmiş indeksin adını
> değiştirir. İkinci bir indeks için ADI HasIndex'e parametre olarak
> vermek gerekiyor; aynı kalıp `IX_Reservations_Canli`'de de kullanıldı.

**satır 193**

> "İşletmenin tüm sözleşmeleri" sorgusu kısmi indeksi kullanamaz.
>
> ⚠️ Adın İKİNCİ PARAMETRE olarak verilmesi şart — bkz.
> `PricingConfigurations`'daki aynı tuzak. Adsız bırakıldığında bu
> satır aşağıdaki kısmi benzersiz indeksin içinde kayboluyor ve
> indeks hiç yaratılmıyordu; yorum "gerekli" diyor ama veritabanında
> yoktu (2026-08-24'te doğrulandı).


## `src/DailyCruising.Infrastructure/Persistence/Configurations/PricingConfigurations.cs`

**satır 55**

> ⚠️ AYNI KİRALAMA TİPİ BİR TEKNEYE İKİ KEZ EKLENEMEZ.
>
> Eklenebilseydi "bu teknenin günlük tur fiyatı ne" sorusunun iki cevabı
> olurdu ve hangisinin geçerli olduğu, fiyat sorgusunun hangi satırı
> önce okuduğuna kalırdı. Denetim değil, uçları yazarken çıktı
> (2026-08-26): depo katmanında bu adı taşıyan bir kısıt VAR SANMIŞTIM,
> veritabanına bakınca yoktu.

**satır 111**

> ⚠️ İKİ PARAMETRELİ `HasIndex` ŞART. EF, aynı kolon listesine yapılan
> ikinci `HasIndex` çağrısını AYNI indeksin yapılandırması sayıyor:
> aşağıdaki kısmi benzersiz indeks bu satırı yutuyor ve düz indeks
> HİÇ YARATILMIYOR. Canlı veritabanında doğrulandı (2026-08-24):
> `Prices` üzerinde yalnız PK, GiST ve kısmi benzersiz indeks vardı.
>
> `.HasDatabaseName(...)` eklemek YETMİYOR — o da ikinci çağrının adı
> tarafından eziliyor; denendi, migration boş çıktı. Ayrı indeks ancak
> adı ikinci PARAMETRE olarak verilince tanımlanıyor.
>
> Bu indeks "kiralama tipinin bütün fiyatları" sorgusu için —
> kısmi indeksler yalnız kendi filtrelerine uyan satırları taşıyor.


## `src/DailyCruising.Infrastructure/Persistence/Configurations/ReservationConfigurations.cs`

**satır 80**

> CANLI rezervasyonlar. Üç ayrı yer "satış hâlâ ayakta mı" diye soruyor:
> `trg_reservation_sync_seats`, `count_live_coupon_redemptions` ve
> terk edilen seferi bırakan iş.
>
> Bunlardan `count_live_coupon_redemptions` kupon satırı FOR UPDATE ile
> KİLİTLİYKEN çalışıyor — orada yavaşlamak yalnız o sorguyu değil,
> aynı kuponu kullanan bütün eşzamanlı rezervasyonları bekletir.
>
> Kısmi olması önemli: `Expired`/`Cancelled` satırlar indekse hiç
> girmiyor, yani indeks tablo büyüdükçe değil YALNIZ canlı satış
> sayısınca büyüyor. Ölçüldü (2026-08-24, 100.000 satırlık sentetik
> yük): indeks olmadan `PK_Reservations` üzerinden heap'e gidiliyor,
> indeksle `Index Only Scan`.
> SAYAÇ İNDEKSİ. `trg_reservation_sync_seats` her yazmada o seferin
> canlı rezervasyonlarını yeniden topluyor.
>
> ⚠️ `IX_Reservations_Canli` bu sorguda KULLANILIYOR ama yetmiyor:
> o indeks `Id` üzerinde, yani planlayıcı TABLODAKİ TÜM canlı satırları
> tarayıp `VoyageId`'yi heap'te filtreliyor. Tarama maliyeti tek bir
> seferin değil, sistemdeki TÜM canlı rezervasyonların sayısıyla
> büyüyor — sezon ortasında yüzlerce sefer canlıyken her koltuk
> güncellemesi hepsini tarar.
>
> Bu indeks `VoyageId` üzerinde ve toplanan kolonları İÇERİYOR:
> tarama o seferin canlı satırlarıyla sınırlı ve heap'e hiç gidilmiyor.
>
> Ölü satırlar (`Expired`/`Cancelled`) filtreye hiç girmiyor, yani
> terk edilen rezervasyonların birikmesi sayacı yavaşlatmıyor.


## `src/DailyCruising.Infrastructure/Persistence/Configurations/UserConfiguration.cs`

**satır 11**

> ⚠️ GÜVENLİK DAMGASI VARSAYILANI VERİTABANINDA (`A-44`).
> Elle atılan `INSERT`'lerde ve başvuru ucunda ayrıca set etmek
> gerekmesin diye. Boş bir damga jetondaki boş damgayla EŞLEŞİRDİ
> ve koruma sessizce kalkardı.


## `src/DailyCruising.Infrastructure/Persistence/DailyCruisingDbContext.cs`

**satır 450**

> ⚠️ `EventLogs` BÖLÜMLENMİŞ ve APPEND-ONLY. Jetonun burada değeri
> SIFIR — satır hiç güncellenmiyor, `forbid_mutation` tetikleyicisi
> `UPDATE`'i zaten reddediyor. Buna karşılık bölümlenmiş tabloya
> yapılan `INSERT`'te EF'in `xmin`'i geri okuması çalışmıyor ve
> dokuz olay günlüğü testi birden kırıldı.
>
> Yani burada jeton hiçbir şey kazandırmıyor, yalnız kaybettiriyor.

**satır 471**

> ⚠️ İYİMSER EŞZAMANLILIK — PROJE GENELİ (`A-48`, Mert soru 6).
>
> Öncesinde HİÇBİR entity'de eşzamanlılık jetonu yoktu: iki çalışan
> aynı anda sezon fiyatını düzenlerse biri diğerinin üzerine
> SESSİZCE yazıyordu ve kimse fark etmiyordu.
>
> ⚠️ TEK TEK DEĞİL DÖNGÜYLE. Yalnız fiyat ve komisyona eklemek
> "tutarsız bir davranış adası" yaratırdı (Mert bunu açıkça eledi):
> kullanıcı bir ekranda "başkası değiştirdi" hatası alır, diğerinde
> almazdı. Döngü ayrıca yeni entity eklendiğinde korumanın
> KENDİLİĞİNDEN geldiği anlamına geliyor — unutulacak bir adım yok.
>
> ⚠️ MIGRATION GEREKTİRMİYOR: `xmin` PostgreSQL'in her satırda zaten
> tuttuğu sistem kolonu. Yeni bir kolon eklenmiyor, var olan
> okunuyor.
>
> ⚠️ `ExecuteUpdate`/`ExecuteDelete` BU KORUMANIN DIŞINDA. Onlar
> değişiklik izleyicisinden geçmiyor ve `WHERE xmin = ...` üretmiyor.
> Projede bilinçli olarak yarış-güvenli yazılmış yerler (koşullu
> UPDATE + etkilenen satır kontrolü) zaten bu yolu kullanıyor;
> oradaki güvence kısıtlardan geliyor, jetondan değil.

**satır 502**

> ⚠️ TETİKLEYİCİLERİN YAZDIĞI TABLOLAR DIŞARIDA — ve bu teknik
> bir zorunluluk, tercih değil.
>
> Bu dört tablonun satırlarını veritabanı tetikleyicileri
> güncelliyor (`sync_voyage_sold_seats`, `sync_boat_rating`,
> `sync_coupon_used_count`, `release_ledger_on_failed_payout`).
> Tetikleyici çalıştığı anda satırın `xmin`'i değişiyor; ama
> bağlamda TAKİP EDİLEN kopya eski değeri taşımaya devam ediyor
> ve o kopyayla yapılan bir sonraki `SaveChanges`
> `DbUpdateConcurrencyException` ile düşüyor.
>
> ÖLÇÜLDÜ: jeton bu dördüne de uygulandığında 39 test kırıldı;
> hepsi iptal akışında, sefer bırakma yolunda. Sebep "yarış"
> değil, kendi tetikleyicimizin kendi işlemimizi çarpması.
>
> ⚠️ Bu bir KORUMA BOŞLUĞU ve gizlenmemeli: bu dört tabloda
> kayıp güncelleme hâlâ mümkün. Karşılığında üçü zaten
> tetikleyiciyle korunuyor (koltuk, puan, kupon sayacı
> veritabanında hesaplanıyor, uygulama yazmıyor) ve
> `LedgerEntries` append-only → [[api-benim-kararlarim]]

**satır 527**

> ⚠️ Genel (`object`) yapıcı üzerinden gidilemiyor: Npgsql'in
> `UseXminAsConcurrencyToken` uzantısı YALNIZ türü bilinen
> `EntityTypeBuilder<T>` üzerinde tanımlı. Gölge özelliği elle
> kuruyoruz — uzantının yaptığının aynısı.


## `src/DailyCruising.Infrastructure/Platform/PlatformRepository.cs`

**satır 14**

> <summary>
> ⚠️ BU DEPODA KAPSAM FİLTRESİ YOK — tek istisna. Platform personeli
> muafiyeti burada yaşıyor. Muafiyetin bedeli olay günlüğünde ödeniyor;
> diğer depolarda `partnerId` parametresiz metot bilerek yoktur, burada ise
> bilerek vardır ve fark bu yorumla kayıtlıdır.
> </summary>

**satır 39**

> ⚠️ ONAYLI sözleşmenin oranı. En son sözleşme alınsaydı,
> gönderilmiş ama onaylanmamış bir sözleşmenin oranı yürürlükte
> gibi görünürdü — komisyon onaylanan sözleşmedeki orandır.

**satır 79**

> <summary>
> ⚠️ Yalnız `Sent` olanlar iptal ediliyor, `Approved` olanlara
> DOKUNULMUYOR: yürürlükteki sözleşme, yenisi onaylanana kadar geçerli
> kalmalı. İptal edilseydi işletme, yeni sözleşmeyi onaylayana kadar
> sözleşmesiz kalır ve tekne ekleyemez, satış yapamazdı.
> </summary>

**satır 132**

> ⚠️ Yalnız GELECEK ve ÖDENMİŞ. Geçmiş tur zaten yapıldı; `Pending`
> olan tutma süresi dolunca kendiliğinden düşüyor ve onu iptal
> etmek, iade edilecek parası olmayan bir rezervasyona iade kaydı
> açmaya çalışırdı.

**satır 154**

> ⚠️ %100 — kademeli iade MÜŞTERİNİN KENDİ vazgeçmesi için.
> Burada turu iptal eden platform; müşteriye ceza kesmek,
> kusuru olmayan tarafı cezalandırmak olurdu.

**satır 181**

> ⚠️ `PlatformCancelled` diye bir değer YOK ve uydurmadım: enum'a değer
> eklemek `A-39` gereği migration ister. `OwnerCancelled` anlamca en
> yakını — turu iptal ettiren şey işletmenin durumu


## `src/DailyCruising.Infrastructure/Pricing/PricingRepository.cs`

**satır 18**

> <summary>
> Tekne, kiralama tipi, işletme ve AKTİF sözleşme TEK sorguda. Ayrı
> okunsaydı, iki sorgu arasında sözleşme değişirse komisyon oranı bir
> sözleşmeden, kimliği başkasından gelirdi — ve hakediş yanlış hesaplanırdı.
>
> ⚠️ Tek sorgu olması tek başına yetmiyor: sıralama kesin olmazsa aynı
> ifade içindeki alt sorgular farklı satır seçebilir. Kesinliği
> `ThenByDescending(Id)` sağlıyor, aşağıya bakınız.
> </summary>

**satır 179**

> <summary>
> Kullanım sayısı `Coupons.UsedCount` kolonundan DEĞİL, gerçek kayıtlardan
> sayılıyor. Sayaç kolonu ile kayıtlar ayrışabilir; ayrıştığında sayaç
> yalan söyler, kayıtlar söylemez.
> </summary>
> <summary>
> Kuponun CANLI kullanım sayısı.
>
> ⚠️ Filtre `trg_coupon_redemption_limit` tetikleyicisindekiyle AYNI
> olmak zorunda. Burası eskiden bütün kullanımları sayıyordu, tetikleyici
> yalnız canlı olanları: süresi dolan bir rezervasyondan sonra veritabanı
> kuponu kabul ederken uygulama "hakkı dolmuş" diyordu. İkisi de hata
> vermez, cevap sessizce yanlış olurdu.
>
> Canlı olmayan (SüresiDoldu / İptal / İade) rezervasyonun kuponu serbest
> kalır — aksi halde ödeme ekranını terk eden her müşteri sınırlı bir
> kampanya kuponunu kalıcı olarak yakardı.
> </summary>


## `src/DailyCruising.Infrastructure/Privacy/AnonymizationRepository.cs`

**satır 37**

> ---- Rezervasyonlardaki iletişim bilgisi ----
>
> ⚠️ Rezervasyon SİLİNMİYOR. Muhasebe kaydı ve `Restrict` zinciri zaten
> izin vermiyor. Yalnız kişiyi işaret eden üç alan temizleniyor.
>
> Misafir rezervasyonları (`UserId` null) e-postaya göre de eşleşiyor:
> aynı kişi üye olmadan önce rezervasyon yapmış olabilir ve o kayıtlar
> da onun kişisel verisi.

**satır 65**

> ---- Mesajlar ----
>
> ⚠️ YALNIZ BU KULLANICININ YAZDIKLARI. Karşı tarafın (işletmenin)
> mesajları duruyor: onlar işletmenin anlaşmazlık kaydı ve bu kişinin
> silme talebi başkasının kaydını silmeye yetmiyor.


## `src/DailyCruising.Infrastructure/Reservations/ReservationRepository.cs`

**satır 12**

> <summary>
> Rezervasyonun yazılması. Bütün adımlar TEK işlemde.
>
> ⚠️ Bu sınıfta kapasite kontrolü, çakışma kontrolü ve kupon hakkı kontrolü
> YOKTUR — bilerek. Üçü de veritabanı kısıtı:
>
>   `CK_Voyages_SoldSeats`          kapasite (sayacı tetikleyici türetiyor)
>   `EX_Voyages_NoOverlapPerBoat`   aynı teknede çakışan sefer
>   `IX_Voyages_SharedVoyagePerDay` aynı güne iki paylaşımlı sefer
>   `trg_coupon_redemption_limit`   kuponun kullanım hakkı
>
> Buraya bir `if` yazmak, o `if`i atlayan ikinci bir kod yolunun er geç
> yazılması demek olurdu. Kısıtın reddi yakalanıp anlamlı bir hataya
> çevriliyor; karar veren yer veritabanı.
> </summary>

**satır 41**

> <summary>
> ⚠️ `Voyage` YÜKLENİYOR ve şart. Kademeli iade oranı kalkışa kalan süreye
> bakıyor (`Voyage.StartsAt`); yüklenmezse `NullReferenceException` ya da
> daha kötüsü, tembel yükleme kapalı olduğu için sessizce yanlış sonuç.
> </summary>

**satır 155**

> ⚠️ `ReservationId = reservation.Id` YAZILAMAZ: kimlik
> veritabanında `uuidv7()` ile üretiliyor, bu satırda
> hâlâ `Guid.Empty`. Gezinme özelliği bağlanınca EF
> yabancı anahtarı INSERT sonrası kendisi dolduruyor.

**satır 206**

> ⚠️ BAŞARISIZ VARLIKLAR DA BIRAKILIYOR. İşlemi geri almak
> veritabanını temizler ama BAĞLAMI temizlemez: reddedilen
> `Voyage` ve `Reservation` `Added` durumunda takılı kalır ve
> aynı bağlamla yapılan BİR SONRAKİ `SaveChangesAsync` onları
> hayalet olarak yeniden yazmaya kalkar.
>
> Uygulamada `DbContext` istek başına atıldığı için bu canlıda
> görünmüyordu; testte görüldü (2026-08-24). Bağlamı çağırana
> kirli bırakmak yine de yanlış.

**satır 301**

> <summary>
> Yarış kaybedildiğinde bağlamı temizler.
>
> ⚠️ Bugün yarış istisnası YALNIZCA `FindOrCreateVoyageAsync` içindeki
> `SaveChangesAsync`'ten gelebiliyor ve o çağrı rezervasyon `Add`
> edilmeden ÖNCE yapılıyor — yani temizlenecek tek şey seferdir. Yine de
> rezervasyon grafiği de açıkça bırakılıyor: iki adımın sırası bir gün
> değişirse ikinci turda çift `Reservation` ya da çift `CouponRedemption`
> eklenmesi, hiçbir kısıtın yakalayamayacağı bir hata olurdu.
> </summary>


## `src/DailyCruising.Infrastructure/Reservations/VoyageRelease.cs`

**satır 8**

> <summary>
> Canlı rezervasyonu kalmayan seferi iptal eder — takvimi bırakır.
>
> ⚠️ NEDEN ORTAK BİR YER: takvimi koruyan kısıt `Reservation`'a değil
> `Voyage.Status`'a bakıyor (`EX_Voyages_NoOverlapPerBoat`). Rezervasyon ölse
> de sefer takvimi işgal etmeye devam eder. Bu hata **iki kez** yapıldı —
> önce teklif akışında, sonra A-22'de — ve ikincisinde kimliksiz, bedava bir
> takvim kilidine dönüştü.
>
> İptal ucu (`A-24`) bunu yapan ÜÇÜNCÜ yer olacaktı. Üçüncü kopya yerine tek
> bir yer: `Voyage` yaratan her yol bunu çağırmak zorunda
> -> [[api-terk-edilen-sefer-kilidi]]
> </summary>


## `src/DailyCruising.Infrastructure/Reviews/ReviewRepository.cs`

**satır 12**

> <summary>
> ⚠️ Rezervasyon tekneye `Voyage` ÜZERİNDEN bağlı — `Reservation.BoatId`
> diye bir alan YOK. Zincir burada, tek projeksiyonda kuruluyor.
> </summary>

**satır 76**

> <summary>
> ⚠️ `UsedAt IS NULL` KOŞULU `WHERE`'DE. Servis katmanında kontrol edilip
> burada koşulsuz yazılsaydı, iki eşzamanlı istek arasındaki pencerede
> ikisi de geçerdi ve aynı tur iki kez puanlanırdı — üstelik ikinci yorum
> `IX_Reviews_ReservationId` benzersizine takılıp çıplak 500 verirdi.
> </summary>

**satır 95**

> <summary>
> ⚠️ `Status == Approved` ŞART. Yorumlar yayına girmeden platform
> onayından geçiyor ([[domain-gereksinimler]] 2026-08-22); filtre
> unutulsaydı onaylanmamış — hakaret içerebilecek — bir yorum tekne
> sayfasında görünürdü.
> </summary>

**satır 136**

> ⚠️ Sözlüğe dönüşüm BELLEKTE: `ToDictionary` EF projeksiyonunun
> içinde çevrilemiyor ve çalışma anında 500 veriyor (`A-33e` dersi).

**satır 169**

> ⚠️ REDDEDİLEN YORUMLAR İŞLETMEYE GÖSTERİLMİYOR (`A-49`,
> Mert soru 7). Reddedilme sebebi hakaret ya da kişisel veri
> olabiliyor; platform onu temizlerken işletmenin metni okumuş
> olmasının önüne geçiliyor.
>
> ⚠️ Filtre SORGUDA, servis katmanında değil: yeni bir okuma yolu
> (dışa aktarma, rapor, bildirim) filtreyi unutabilirdi. Aynı
> gerekçe destek talebindeki `IsInternal` filtresinde de var.


## `src/DailyCruising.Infrastructure/Search/SearchRepository.cs`

**satır 12**

> <summary>
> CANLI ARAMA (`A-34`) — özet tablo yok.
>
> `AvailabilityDays` özet tablosu 2026-08-24'te bilerek ertelendi: her fiyat
> değişikliğinde ~365 satır yeniden yazmak gerekiyordu ve o güncellemeyi
> atlayan tek bir kod yolu müşteriye YANLIŞ FİYAT gösterirdi. Geri dönüş
> eşiği ölçülü: arama p95 &gt; 300 ms ya da tekne sayısı &gt; 300
> ([[domain-gereksinimler]]).
>
> ⚠️ MÜSAİTLİK TANIMI REZERVASYONUNKİYLE AYNI OLMAK ZORUNDA. Ayrışırsa
> arama "yer var" der, rezervasyon reddeder — ya da tersi, ki daha kötü:
> arama gizler, tekne boş gider. Tanım tek yerde: <see cref="MusaitMi"/>.
> </summary>

**satır 41**

> ⚠️ TİCARİ kapasite, yasal kapasite DEĞİL: satılan koltuk sayısı
> ticari kapasiteyle sınırlı ve arama satılabilirliği ölçüyor.

**satır 45**

> Adım 2 — aranan tarihte geçerli fiyat. Tarih verilmemişse temel fiyat.
>
> ⚠️ Sezon fiyatı temel fiyatı EZER. `OrderBy(ValidFrom == null)`
> sezonu öne alıyor; sıralama olmasaydı hangisinin döneceği sorgu
> planına kalırdı ve aynı arama iki farklı fiyat gösterebilirdi.

**satır 74**

> ⚠️ `Boat`'ta `Voyages` gezinti özelliği YOK — `DbSet` üzerinden
> ilişkilendirilmiş alt sorgu yazılıyor. EF bunu tek SQL'e
> (LATERAL) çeviriyor, N+1 değil.

**satır 92**

> ⚠️ FİYATI OLMAYAN KİRALAMA TİPİ ELENMİYOR.
>
> Burada bir zamanlar `.Where(x => x.Fiyat != null)` vardı ve bu
> [[domain-gereksinimler]] 2026-08-23'e AYKIRIYDI: tekne sahibi
> kiralama tipini fiyat girmeden tanımlayabiliyor ve müşteri "fiyat
> için iletişime geçin" görüp özel teklif akışını başlatıyor. Eleme,
> o satış yolunu tamamen görünmez kılıyordu — üstelik bunu doğrulayan
> bir test bile yazmıştım (2026-08-26 düzeltmesi).

**satır 103**

> Fiyat filtresi VERİLDİĞİNDE fiyatsızlar düşüyor: "500–800 TL
> arası" arayan müşteriye fiyatı bilinmeyen tekneyi göstermek
> filtrenin anlamını bozardı. Filtre verilmediğinde görünüyorlar.
>
> ⚠️ `x.Fiyat != null` kontrolü AÇIKÇA yazılı ama TAŞIYICI DEĞİL:
> C#'ın yükseltilmiş karşılaştırma operatörü `null >= 500m` için
> zaten `false` döndürüyor. Mutasyon testiyle ölçüldü (2026-08-26) —
> kontrol kaldırılınca test yeşil kalıyor. Açık bırakılmasının
> sebebi okunabilirlik: `null`un hangi tarafa düştüğü bu satırdan
> okunuyor, dil kuralını hatırlamayı gerektirmiyor.

**satır 133**

> Tekne başına EN UCUZ kiralama tipi — aynı tekne listede bir kez.
> ⚠️ Fiyatsız tipler SONA: teknenin hem fiyatlı hem fiyatsız tipi
> varsa listede fiyatlı olan görünmeli, yoksa müşteri "fiyat
> sorunuz" görüp fiyatlı seçeneği hiç fark etmezdi.

**satır 197**

> <summary>
> O GÜN KAÇ KOLTUK KALDI — rezervasyon yolunun kurallarının aynısı.
>
> Üç durum ve üçü de `ReservationRepository.FindOrCreateVoyageAsync` ile
> aynı mantığı taşıyor:
>
> 1. **Blok** (`VoyageType.Block`) → tekne o gün hiç satılamaz, 0.
> 2. **Özel sefer var** (`IsExclusive`) → tekne o gün kapatılmış, 0.
>    `EX_Voyages_NoOverlapPerBoat` zaten ikinciyi engelliyor; arama bunu
>    göstermezse müşteri rezervasyona kadar gelip reddedilirdi.
> 3. **Paylaşımlı sefer var** → `Capacity - SoldSeats`.
>    Sefer YOKSA henüz kimse almamış demektir: tam kapasite.
>
> ⚠️ **`Offer` seferi TARİHİ TAMAMEN KAPATIYOR — `Sale` gibi DEĞİL.**
>
> İlk sürümde `Sale` ile aynı muamele görüyordu ve o yanlıştı: teklif
> verilmiş bir tarihte tekne aramada `12 koltuk boş` görünüyordu.
> [[domain-gereksinimler]] 2026-08-23 açık — *"Bu süre boyunca ilgili
> tarih rezerve edilir; başkası satın alamaz."*
>
> Veritabanı da böyle diyor: `EX_Voyages_NoOverlapPerBoat` tekne başına
> çakışan HİÇBİR sefere izin vermiyor (paylaşımlı/özel ayrımı yok). Yani
> teklif seferi varken o tarihe satış seferi zaten AÇILAMAZ; arama bunu
> göstermeseydi müşteri rezervasyona kadar gelip **500** alırdı
> (canlı denemede tam olarak bu oldu, 2026-08-26).
> </summary>


## `src/DailyCruising.Infrastructure/Storage/ImageProcessor.cs`

**satır 6**

> <summary>
> RESİM İŞLEME (`A-60`) — Mert'in "geç yükleme istemiyorum" sorusuna cevap.
>
> Format tek başına yetmiyor; üç şey birden gerekiyor ve ikisi burada:
>
> 1. **WebP'ye çevirme.** Aynı görsel kalitede JPEG'den ~%25-35 küçük.
>    Kabul edilen format kullanıcıya bırakılıyor (JPG, PNG, HEIC — telefon
>    ne verirse), SAKLANAN ve SUNULAN format tek: WebP. Kabul ile sunumu
>    ayırmak, işletmeyi format bilgisine mahkûm etmemek demek.
>
> 2. **Birden çok genişlik.** 4000 piksellik bir fotoğrafı 400 piksellik
>    kutuda göstermek, kullanıcıya gereksiz megabaytlar indirtiyor —
>    "geç yükleme" şikayetinin en büyük tek sebebi bu, format değil.
>
> 3. (Frontend'de) `srcset` + `loading="lazy"`.
>
> ⚠️ **SkiaSharp seçildi, ImageShar) DEĞİL.** ImageSharp'ın lisansı
> "Six Labors Split License": belirli gelir eşiğinin üzerindeki ticari
> kullanım ÜCRETLİ. DailyCruising ticari bir platform; sessizce ücretli
> bir lisansa bağlanmak, fark edildiğinde geri alması pahalı bir borç
> olurdu. SkiaSharp MIT ve WebP kodlamayı destekliyor.
> </summary>

**satır 37**

> <summary>
> ⚠️ 82: gözle ayırt edilmesi zor, dosya belirgin küçük. 100 dosyayı
> kayıpsıza yaklaştırıp WebP'nin bütün kazancını götürür.
> </summary>

**satır 58**

> ⚠️ ORİJİNALDEN BÜYÜĞE ÇIKILMIYOR. Büyütmek kalite
> kazandırmıyor, yalnız dosya boyutu ekliyor.


## `src/DailyCruising.Infrastructure/Storage/S3FileStorage.cs`

**satır 8**

> <summary>
> S3 UYUMLU DEPOLAMA (`A-60`).
>
> ⚠️ AWS'ye DEĞİL, S3 API'sine bağlı. `ServiceUrl` verilerek MinIO,
> Cloudflare R2 ya da DigitalOcean Spaces da kullanılabiliyor — ve
> geliştirmede tam olarak bu yapıldı: bu sınıf yerel bir MinIO
> konteynerine karşı DOĞRULANDI (2026-08-26). Gerçek bir S3 hesabı
> beklemeden çalıştığını ölçebilmenin tek yolu buydu.
> </summary>

**satır 23**

> ⚠️ İÇERİK ÖZETİ ÖNCE HESAPLANIYOR, yükleme sonra. Akış bir kez
> okunabildiği için belleğe alınıyor — bu yüzden boyut sınırı
> uçlarda ZORUNLU, yoksa büyük bir yükleme sunucuyu düşürürdü.

**satır 33**

> ⚠️ ANAHTAR İÇERİKTEN TÜRÜYOR: aynı dosya iki kez yüklenirse aynı
> anahtarı alıyor, ikinci kopya yer kaplamıyor. Ve adres içerik
> değişmedikçe DEĞİŞMİYOR — CDN'e sonsuz önbellek verilebilmesinin
> şartı bu.

**satır 39**

> ⚠️ BOYUT YÜKLEMEDEN ÖNCE OKUNUYOR. `PutObjectAsync` akışı KAPATIYOR;
> sonrasında `Length` okumak `ObjectDisposedException` veriyor.
> Testi yazmasaydım bu hata ancak ilk gerçek yüklemede görünürdü.

**satır 54**

> ⚠️ Önbellek başlığı BURADA yazılıyor, CDN'e bırakılmıyor:
> anahtar içerik özeti olduğu için bu adresin içeriği ASLA
> değişmiyor. `immutable`, tarayıcının doğrulama isteği bile
> atmamasını sağlıyor.

**satır 69**

> <summary>
> ⚠️ Adres YAPILANDIRMADAN kuruluyor, S3 istemcisinden değil: üretimde
> dosyalar CDN üzerinden sunulacak ve o adres kovanın adresiyle aynı
> olmayacak.
> </summary>

**satır 109**

> <summary>⚠️ Sır. `Storage:AccessKey` — user-secrets ya da ortam değişkeni.</summary>

**satır 112**

> <summary>⚠️ Sır. `Storage:SecretKey`.</summary>

**satır 118**

> <summary>
> ⚠️ Bazı S3 uyumlu sağlayıcılar (örn. Cloudflare R2) chunked
> imzalamayı desteklemediği için gerekebiliyor.
>
> ⚠️ YALNIZ HTTPS ÜZERİNDE ÇALIŞIYOR. AWS SDK açıkça reddediyor:
> *"When DisablePayloadSigning is true, the request must be sent over
> HTTPS"*. HTTP bir uç noktada açık bırakılırsa **her yükleme düşer** —
> ölçüldü (2026-08-26, MinIO).
> </summary>


## `src/DailyCruising.Infrastructure/Support/SupportRepository.cs`

**satır 58**

> ⚠️ `IsInternal` mesajlar MÜŞTERİYE FİLTRELENİYOR — burada,
> sorguda. Servis katmanında elenseydi yeni bir okuma yolu
> (dışa aktarma, rapor) filtreyi unutabilirdi.

**satır 68**

> ⚠️ Gönderen KİMLİĞİ dönmüyor, TARAFI dönüyor.

**satır 71**

> ⚠️ Tam ad ARA TİPTE kalıyor, DTO'ya hiç girmiyor
> (`A-53`). `SupportMessage`'ta gezinme özelliği yok,
> bu yüzden alt sorgu. Doğrudan `TicketMessageItem`
> içine yazılsaydı tam ad bir an için dışarıya
> dönebilecek bir nesnede dururdu.

**satır 116**

> <summary>
> Tam addan YALNIZ İLK İSMİ çıkarıyor (`A-53`, Mert soru 14).
>
> ⚠️ Soyadı bilerek düşüyor: müşteri süreklilik hissetsin ("Ayşe ile
> konuşmuştum") ama kişiselleşen bir anlaşmazlık çalışanı hedef
> alamasın.
>
> Tek kelimelik ad olduğu gibi dönüyor; boş ad `null` oluyor —
> arayüzde "  ile konuşuyorsunuz" gibi bir metin çıkmasın.
> </summary>

**satır 164**

> ⚠️ Personel listesinde ÖNCELİK önce, sonra tarih: destek kuyruğu
> "en acil önce" çalışıyor. Müşteri listesinde önceliğin bir
> anlamı yok, orada da aynı sıra zararsız.

