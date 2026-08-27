---
rol: not
kapsam: api
guncelleme: 2026-08-27
durum: guncel
---

# Gerekçe arşivi — Application katmanı

İş kuralları, servisler, sözleşmeler ve doğrulamalar.

Kod içindeki ⚠️ işaretli gerekçe yorumları 2026-08-27'de silindi; kod artık
yalnız *ne yaptığını* anlatan XML doc taşıyor → [[api-kararlar]]. Silinmeden
önce **249 blok birebir** buraya taşındı: hiçbiri yeniden yazılmadı,
kısaltılmadı, özetlenmedi. Satır numaraları silme anındaki hâle aittir;
dosya adı kalıcı, satır numarası değil.

**Bu bir arşivdir, talimat değil.** Bir madde koda aykırı çıkarsa kod
doğrudur → [[api-desenler]]

Diğer katmanlar: [[api-gerekce-arsivi-infrastructure]]

---


## `src/DailyCruising.Application/Abstractions/EventPayloadPolicy.cs`

**satır 3**

> <summary>
> `EventLogs.Payload` içine NE girebileceğinin tek tanımı.
>
> ⚠️ NEDEN GEREKLİ: bu tablo değişmez ve temizlenemez — `UPDATE`/`DELETE`
> tetikleyiciyle reddediliyor, `TRUNCATE` yetkisi uygulama rolünde yok. Bir
> kez giren asla silinemez. jsonb serbest olduğu sürece, payload'a yanlışlıkla
> bir isim, telefon ya da arama kutusuna yazılmış bir metin koyan TEK bir
> satır kalıcı bir KVKK sorunu üretiyordu.
>
> Nokta çözümler zaten vardı (`NormalizeEmailForLog`, `Kisalt`, `KodBicimi`)
> ama kural yoktu: yeni bir olay yazan biri hiçbirini bilmek zorunda değildi.
> Artık kural burada ve uygulaması `EventLogger`'da — çağıranın bir şey
> hatırlamasına gerek yok.
>
> FAIL-CLOSED: listesi olmayan olay türü payload YAZAMAZ. Açık bırakılsaydı
> yeni bir olay türü eklemek sessizce sınırların dışına çıkmak olurdu.
> `EventTypes` içindeki her sabitin burada karşılığı olduğu testle sabitleniyor
> (`OlayGunluguTests.Her_olay_turunun_payload_listesi_var`); derleyici bunu
> göremez.
> </summary>

**satır 37**

> <summary>
> Olay türü -> izin verilen anahtarlar. Boş dizi "payload yok" demek.
>
> ⚠️ Buraya bir anahtar eklemek, o alanın SİLİNEMEZ bir tabloya
> gireceğini kabul etmektir. Kişisel veri ancak açık bir kararla girer
> (bkz. `auth.login.failed` -> `email`, Mert 2026-08-24) ve girdiği her
> alan `A-12` kapsamında ayrıca ele alınır.
> </summary>

**satır 56**

> ⚠️ JETONUN KENDİSİ YOK ve olmayacak. `EventLogs` temizlenemiyor;
> oraya düşen bir yenileme jetonu, kaydı okuyabilen herkes için
> kullanılabilir bir anahtar olurdu. Kimlik (`SubjectId`) yeterli.

**satır 73**

> ⚠️ Yalnız iş yeri türü ve şehir. IBAN, vergi numarası, telefon ve
> e-posta BİLEREK yok — bu kayıt silinemiyor.

**satır 81**

> ⚠️ Tutar ve oran VAR, müşteri kimliği YOK. "Kim ne kadar iade
> aldı" sorusu `Refunds` tablosundan cevaplanıyor; `EventLogs`
> temizlenemediği için oraya kişi bağlanmıyor.

**satır 90**

> ⚠️ Liste ESKİDEN BOŞTU — yani her arama payloadsız yazılıyordu
> ve "ne arandı" sorusu cevapsızdı. Mert'in istediği "ayrıntılı"
> veri buydu. Kimlik alanları (bölge, tekne tipi) ve SAYILAR var;
> serbest metin YOK — `EventLogs` temizlenemiyor.

**satır 102**

> ⚠️ Tekne ADI listede YOK. Kimlik `SubjectId`'de duruyor; ad
> değişebilir bir alan ve `EventLogs` temizlenemiyor — bugün
> zararsız görünen bir metin yarın silinemez hale gelir.

**satır 110**

> ⚠️ YORUM METNİ listede YOK. `EventLogs` temizlenemiyor ve yorum
> metni müşterinin serbest yazısı — hakaret, kişisel veri, her şey
> olabilir. Metin `Reviews` tablosunda duruyor ve ORASI
> düzeltilebilir; günlüğe düşen düzeltilemez.

**satır 118**

> ⚠️ MESAJ METNİ listede YOK — ne orijinali ne maskelenmişi.
> Maskelenmiş hal bile serbest metin; `EventLogs` temizlenemiyor.
> Metin `Messages` tablosunda duruyor ve ORASI KVKK kapsamında
> temizlenebiliyor (`A-12`).

**satır 126**

> ⚠️ SAYILAR VAR, METİN YOK. Maskelenen içeriğin kendisi
> (telefon, e-posta, IBAN) `EventLogs`'a asla girmiyor — o tablo
> temizlenemiyor ve oraya düşen bir numara kalıcı olurdu.

**satır 132**

> ⚠️ TUTAR VAR — mesaj ve yorumdan FARKLI olarak. Teklif tutarı
> serbest metin değil, satıcının koyduğu bir SAYI; kişisel veri
> taşımıyor ve "hangi fiyattan teklif verildi, hangisi kabul
> edildi" sorusu pazarlık davranışının tek ölçüsü. Not metni
> (`Note`) yine YOK — o serbest yazı.

**satır 142**

> ⚠️ TUTAR listede YOK. Fiyat bilgisi `Prices` tablosunda yaşıyor
> ve rezervasyona kopyalanıyor; `EventLogs` temizlenemediği için
> buraya yazılan bir tutar sonsuza kadar kalır. `action` neyin
> yapıldığını (`add`/`update`/`remove`), `kind` fiyatın temel mi
> sezon mu olduğunu söylüyor — soruyu cevaplamaya bu yetiyor.

**satır 179**

> --- biniş ---
> ⚠️ JETON YOK ve olmayacak. `EventLogs` temizlenemiyor; oraya
> düşen bir biniş jetonu, kaydı okuyabilen herkes için
> kullanılabilir bir anahtar olurdu. Rezervasyon kodu yeterli.

**satır 191**

> --- yan sistemler ---
> ⚠️ Liste ESKİDEN BOŞTU: her talep payloadsız yazılıyordu ve
> "hangi konuda talep geliyor" sorusu cevapsızdı. `category`
> SERBEST METİN DEĞİL, izinli listeden (`SupportService.Kategoriler`)
> — serbest olsaydı `EventLogs`'a temizlenemeyen kullanıcı metni
> girerdi. Konu ve gövde YOK, ikisi de serbest yazı.

**satır 208**

> ⚠️ Liste ESKİDEN BOŞTU — yani muafiyetin bedeli ödeniyor GİBİ
> görünüyordu ama kayıtta NE ERİŞİLDİĞİ yoktu. "Platform birine
> baktı" bilgisi tek başına denetime yaramaz.
>
> `resource` ve `action` sabit metinler (controller'da yazılı),
> `subjectId` zaten `EventLogEntry`'de. Serbest metin YOK.


## `src/DailyCruising.Application/Abstractions/FileSignature.cs`

**satır 3**

> <summary>
> DOSYA İÇERİĞİNİN GERÇEKTEN NE OLDUĞUNU DOĞRULAR (`A-62`).
>
> ⚠️ `Content-Type` başlığı İSTEMCİNİN YAZDIĞI BİR METİN. `.pdf` diye
> gönderilen bir dosya aslında bir betik, bir HTML sayfası ya da bir
> çalıştırılabilir olabilir. `A-60`'ta yalnız izin listesi vardı ve bu
> eksikti: liste "hangi türü kabul ediyoruz"u söylüyordu, "gelen şey
> gerçekten o mu"yu değil.
>
> Burada dosyanın İLK BAYTLARINA bakılıyor — her biçimin standartla
> sabitlenmiş bir imzası var ve istemci onu uyduramaz (uydurursa da
> dosya gerçekten o biçimde olur).
>
> ⚠️ Bu bir virüs taraması DEĞİL. Amaç, beyan ile içeriğin uyuşmasını
> zorlamak; kötü niyetli ama geçerli bir PDF yine geçer. Depolamanın
> çalıştırılabilir olmaması ve kovanın genel okumaya kapalı olması ayrı
> katmanlar.
> </summary>

**satır 23**

> <summary>
> İmza tanınıyor ve beyan edilen türle uyuşuyor mu.
>
> ⚠️ Akışın konumu ÇAĞIRANDA bırakılmıyor: okuma sonrası başa
> sarılıyor. Sarılmasaydı yükleme, imza için okunan baytları
> kaybetmiş bir akışla devam eder ve dosya bozuk yazılırdı.
> </summary>

**satır 71**

> ⚠️ TANINMAYAN TÜR REDDEDİLİYOR. `true` dönseydi, izin
> listesine yeni bir tür eklendiği an imza doğrulaması o tür
> için sessizce devre dışı kalırdı.


## `src/DailyCruising.Application/Abstractions/IAuthRepository.cs`

**satır 31**

> <summary>
> Jetonu iptal eder ve zincire bağlar — YALNIZ hâlâ iptal edilmemişse.
> Etkilenen satır sayısını döner: 1 ise döndürmeyi biz yaptık, 0 ise
> başkası bizden önce davrandı.
>
> ⚠️ NEDEN KOŞULLU UPDATE. Aynı yenileme jetonuyla iki istek aynı anda
> gelirse (biri gerçek kullanıcı, biri jetonu çalan) ikisi de satırı
> `RevokedAt = NULL` okuyabilir ve ikisi de döndürmeyi tamamlayabilirdi:
> yeniden kullanım tespiti YARIŞ İLE ATLATILIRDI ve saldırgan kendi
> zincirini sessizce kurardı. Koşulu veritabanı değerlendiriyor, yani
> kimin ilk olduğuna uygulama değil veritabanı karar veriyor.
> Denetim bulgusu (2026-08-25) → [[api-desenler]]
> </summary>

**satır 50**

> <summary>
> Verilen jetondan TÜREYEN bütün zinciri iptal eder ve kaç satır
> etkilendiğini döner (Mert, 2026-08-26 / S-17).
>
> Çalınmış jeton saptandığında yalnız o zincir kapanıyor; kullanıcının
> diğer cihazları (telefon, tablet) açık kalıyor. Sebep: kazananın
> saldırgan mı meşru kullanıcı mı olduğu bilinmiyor ama **yanlış pozitif
> gerçek** — kötü bağlantıda istemcinin aynı isteği iki kez göndermesi de
> bu dala düşüyor. Tüm oturumları kapatmak (OWASP önerisi) o durumda
> kullanıcıyı sebepsiz her yerden atardı.
>
> ⚠️ Dönen sayı ÖNEMLİ: uyarı postası yalnız gerçekten bir şey iptal
> edildiğinde gidiyor. Aksi halde saldırgan aynı ölü jetonu tekrar tekrar
> sunup kurbana posta yağdırabilirdi — zincir bir kez kapandıktan sonra
> tekrarlar 0 döndürüyor ve sessiz kalıyor.
> </summary>


## `src/DailyCruising.Application/Abstractions/IBoardingRepository.cs`

**satır 5**

> <summary>
> Biniş okutma.
>
> ⚠️ İKİ SORGU DA `partnerId` ALIYOR. Kapsam filtresi burada, servis katmanında
> değil — aynı gerekçe `IPartnerStaffRepository`'de yazılı: kontrolü unutan yeni
> bir çağrı yolu, başka işletmenin rezervasyonunu sessizce okuturdu.
>
> Rezervasyonun işletmesi `Reservations` üzerinde DOĞRUDAN durmuyor;
> `BoatRentalTypes -> Boats -> PartnerId` üzerinden geliyor. Bu yolculuk tek
> bir yerde yazılı olmalı, her çağıranda tekrar kurulmamalı.
> </summary>

**satır 18**

> <summary>
> Jetonun ÖZETİNE göre rezervasyon. Yalnız çağıranın işletmesine ait
> olanı döner; başkasınınki null.
>
> ⚠️ "Jeton yok" ile "başka işletmenin" AYIRT EDİLMİYOR ve edilmemeli:
> ayırt edilseydi, geçerli bir jetonu ele geçiren biri hangi işletmeye ait
> olduğunu deneme yanılmayla bulabilirdi.
> </summary>

**satır 38**

> <summary>
> Rezervasyonu `Boarded`'a çeker — YALNIZ hâlâ `Paid` ise. Etkilenen satır
> sayısını döner: 1 ise BU çağrı ilk binişi yaptı, 0 ise başkası önce
> davrandı (ya da durum bu arada değişti).
>
> ⚠️ NEDEN KOŞULLU UPDATE, NEDEN `entity.Status = ...` DEĞİL.
> Aynı jeton iki cihazda aynı anda okutulabiliyor: iki istek de satırı
> `Paid` görüp ikisi de durum geçişi kaydı yazardı ve son yazan
> `BoardedAt`'i belirlerdi. Oysa "ilk biniş anı" gerçek biniş anıdır —
> yorum hakkının doğması ve mesajlaşmanın kapanması ona bağlı.
>
> `WHERE "Status" = 'Paid'` koşulunu VERİTABANI değerlendiriyor, yani
> kimin ilk olduğuna uygulama değil veritabanı karar veriyor. Kilit ya da
> eşzamanlılık jetonu gerekmiyor. Denetim bulgusu (2026-08-25).
> </summary>

**satır 55**

> <summary>
> İLK BİNİŞTE KONUŞMAYI KAPATIR (`A-36`).
>
> Konuşma QR okutulup biniş resmileştiği anda kapanıyor
> ([[domain-gereksinimler]] 2026-08-23). Kapatma BURADA, biniş işleminin
> İÇİNDE: ayrı bir iş olsaydı biniş ile kapanma arasında müşteri mesaj
> yazmaya devam edebilirdi.
>
> ⚠️ Misafir rezervasyonunda (`UserId` boş) konuşma yoktur; 0 döner ve
> bu HATA DEĞİL.
>
> Etkilenen satır sayısı döner.
> </summary>


## `src/DailyCruising.Application/Abstractions/IBoatCatalogRepository.cs`

**satır 6**

> <summary>
> Tekne kataloğu deposu.
>
> ⚠️ KAPSAM FİLTRESİ BURADA. Panel metotlarının her biri `partnerId` alıyor ve
> `WHERE`'e koyuyor; parametresiz bir "hepsini getir" metodu BİLEREK yok.
> Servis katmanında "bu benim mi" diye kontrol edilseydi, kontrolü unutan yeni
> bir çağrı yolu başka işletmenin teknesini SESSİZCE döndürürdü
> → [[api-desenler]] "Kapsam filtresi depo katmanında durur".
> </summary>

**satır 61**

> <summary>
> Verilen adresin hangi tekneye ait olduğunu ve YÜRÜRLÜKTEKİ adresini
> döndürür (`A-46`). Bulunamazsa `null`.
>
> ⚠️ Eski bir adres de bulunuyor — amaç tam olarak bu: `301` ile
> yenisine yönlendirilebilsin.
> </summary>

**satır 70**

> <summary>
> Tekneye yeni bir yürürlükteki adres verir, eskisini geçmişe atar.
> ⚠️ TEK İŞLEMDE: arada kalırsa iki yürürlükteki adres ya da hiç adres
> olmayan bir tekne kalırdı.
> </summary>


## `src/DailyCruising.Application/Abstractions/IEventLogger.cs`

**satır 5**

> <summary>
> Olay günlüğüne yazar.
>
> UYARI: ASLA İSTİSNA FIRLATMAZ. Olay günlüğü analiz içindir, işin doğruluğu
> için değil: bir olayı kaybetmek kabul edilebilir, müşterinin girişini
> bozmak değil. Yazma başarısız olursa uygulama günlüğüne düşer ve iş akışı
> devam eder.
>
> ⚠️ <b>CancellationToken ALMIYOR ve alamaz.</b> Önce alıyordu ve her çağıran
> isteğin kendi jetonunu geçiyordu — yani <c>HttpContext.RequestAborted</c>'ı.
> Sonuç, denetimin 2026-08-24'te bulduğu açıktı: cevabı beklemeden bağlantıyı
> koparan bir saldırgan (kaba kuvvet ve kupon deneme betikleri tam olarak
> böyle davranır) yazmayı iptal ettiriyor, <c>SaveChangesAsync</c>
> <c>OperationCanceledException</c> fırlatıyor, buradaki genel <c>catch</c>
> onu yutuyor ve <b>kayıt hiç yazılmıyordu</b>. Saldırının tek görünür izini
> saldırganın kendisi siliyordu.
>
> Parametre "None geçin" diye belgelenmedi, <b>kaldırıldı</b>: bu projede
> tekrarlanan ilke — yanlış geçilebilen bir alan er ya da geç yanlış geçilir,
> var olmayan alan geçilemez (bkz. <c>QuoteRequest</c>'te tutar alanının
> olmaması).
>
> Yazma İŞ İŞLEMİNDEN AYRI bir kapsamda yapılıyor. Aynı işlemde olsaydı iki
> yönde de yanlış olurdu: olay yazımındaki bir hata rezervasyonu geri alırdı,
> ya da rezervasyon geri alındığında olay da kaybolurdu — oysa "denendi ve
> başarısız oldu" tam olarak kaydetmek istediğimiz şey.
> </summary>

**satır 50**

> <summary>
> Olaya özgü alanlar.
>
> ⚠️ Buraya bir kez giren ASLA SİLİNEMEZ: tablo değişmez, `UPDATE`/`DELETE`
> tetikleyiciyle reddediliyor, `TRUNCATE` yetkisi uygulama rolünde yok.
>
> Eskiden burada "kişisel veri KONMAZ" yazıyordu; 2026-08-24'te Mert
> başarısız girişte denenen e-posta adresinin yazılmasını istedi, yani o
> cümle artık DOĞRU DEĞİL. Kural şuna dönüştü:
>
> <list type="bullet">
>   <item>Kişisel veri ancak <b>açık bir kararla</b> girer, kolaylık olsun
>     diye değil. Giren her alan `A-12` (KVKK) kapsamında ayrıca ele alınır.</item>
>   <item>Serbest metin <b>hiç girmez</b>. Girecekse önce biçimi doğrulanır
>     ve kesilir — bkz. <c>AuthService.NormalizeEmailForLog</c>,
>     <c>PricingController.Kisalt</c>. Kalıcı çözüm `A-13` (payload şeması).</item>
> </list>
> </summary>

**satır 98**

> <summary>
> ⚠️ ZATEN KULLANILMIŞ bir yenileme jetonu tekrar sunuldu.
>
> Bu, oturum süresi dolmasından FARKLI bir olaydır ve çok daha ciddidir:
> döndürme (rotation) yüzünden her jeton yalnız bir kez kullanılabiliyor,
> dolayısıyla ikinci kullanım ya jetonun ÇALINDIĞINI ya da meşru
> istemcinin aynı jetonu iki kez gönderdiğini (ağ tekrarı) gösterir.
>
> Ayrı olay türü olmasının sebebi: müşteriye dönen cevap ikisinde de aynı
> ("oturum süresi dolmuş") ve öyle kalmalı — ayrım YALNIZ günlükte.
> </summary>

**satır 111**

> <summary>
> KVKK "hesabımı sil" talebi yerine getirildi. ⚠️ Bu kaydın KALICI olması
> İSTENEN şey: talebin yerine getirildiğinin kanıtı bu. Payload'da
> kişisel veri yok — yalnız sayılar.
> </summary>

**satır 118**

> <summary>
> İşletme başvurusu alındı (`A-42`). ⚠️ IBAN, vergi numarası ve telefon
> payload'a YAZILMIYOR — `EventLogs` temizlenemiyor.
> </summary>

**satır 124**

> <summary>
> İşletme evrakı yüklendi (`A-60`). ⚠️ Dosya ADI payload'a girmiyor —
> kullanıcının yazdığı ham metin ve `EventLogs` temizlenemiyor.
> </summary>

**satır 140**

> <summary>
> ⚠️ İade talimatı sağlayıcı tarafından REDDEDİLDİ. Bu kayıt olmadan
> başarısız iade sessizce kaybolurdu: müşteri parasını beklerken sistem
> "iptal edildi" diyor olurdu.
> </summary>

**satır 147**

> <summary>
> ⚠️ İADE DENEMELERİ TÜKENDİ, ARTIK DENENMİYOR (`A-56`).
>
> Bu kayıt olmadan otomatik iade işi bir rezervasyonu sessizce
> bırakırdı: müşteri parasını bekler, sistem "iptal edildi" der ve
> hiçbir yerde "bu iade yapılamadı" yazmaz.
> </summary>

**satır 190**

> <summary>
> Mesaj gönderildi. ⚠️ `maskedItemCount` payload'da: ısrarla numara ya da
> IBAN paylaşmaya çalışmak platform dışına kaçış girişimidir ve bu
> sinyal `Messages` tablosunda satır satır durur ama TOPLU olarak
> yalnız günlükten okunur.
> </summary>

**satır 204**

> <summary>
> ⚠️ MASKELEME EŞİĞİ AŞILDI (`A-52`, Mert soru 10) — bir konuşmada
> ısrarla iletişim bilgisi paylaşılmaya çalışılıyor.
>
> Maskeleme bir sürtünme katmanı, güvenlik duvarı değil: kararlı bir
> kullanıcı numarayı yazıyla geçirebiliyor. Bu kayıt, denemeyi
> ÖLÇÜLEBİLİR yapan şey — yaptırım kararı veriye dayanabilsin diye.
>
> ⚠️ Otomatik yaptırım YOK (Mert): insan bakıyor. "Kullanıcıya uyarı
> göster" seçeneği elendi, çünkü caydırıcı olduğu kadar NASIL
> KAÇILACAĞINI da öğretirdi.
> </summary>

**satır 221**

> <summary>
> Kiralama tipi ve fiyat değişiklikleri.
>
> ⚠️ FİYAT DEĞİŞİKLİĞİ ÖZELLİKLE ÖNEMLİ: rezervasyon o günkü fiyatı
> donduruyor ([[domain-gereksinimler]] 2026-08-22), yani "bu rezervasyon
> neden bu tutardan satıldı" sorusunun cevabı `Prices` tablosunda YOK —
> orada yalnız son hal var. Tutarın kendisi payload'a KONMUYOR (aşağıda),
> ama değişikliğin ZAMANI ve kimin yaptığı buradan okunuyor.
> </summary>

**satır 268**

> <summary>
> Destek talebi cevaplandı / durumu değişti.
>
> ⚠️ `SupportTickets` yalnız SON durumu tutuyor; "kaç kez ileri geri
> gitti", "kim ne zaman devraldı" sorusu yalnız günlükten cevaplanıyor.
> </summary>


## `src/DailyCruising.Application/Abstractions/IFileStorage.cs`

**satır 3**

> <summary>
> DOSYA DEPOLAMA (`A-60`, Mert 2026-08-26: *"S3'te olması gerekiyor"*).
>
> ⚠️ Arayüz S3'e göre DEĞİL, bizim kavramlarımıza göre yazıldı: "anahtar",
> "içerik türü", "genel okunabilir mi". S3'ün `PutObjectRequest` şekli
> buraya sızmıyor — sağlayıcı değişirse (R2, Spaces, MinIO) yalnız
> uygulama değişecek. Bu, `IPaymentProvider`'da alınan kararın aynısı.
>
> ⚠️ Dosya İÇERİĞİ veritabanına ASLA girmiyor; veritabanında yalnız
> ANAHTAR duruyor (`BoatMedia.FileKey`, `PartnerDocument.FileKey`).
> Binary'yi tabloya koymak yedek boyutunu ve geri yükleme süresini
> çöpe atardı.
> </summary>

**satır 18**

> <summary>
> Dosyayı yazar ve ANAHTARINI döndürür.
>
> ⚠️ Anahtar İÇERİK ÖZETİNDEN türüyor. Sebebi performans:
> içerik değişmediği sürece adres değişmiyor, adres değiştiğinde de
> içerik kesinlikle değişmiş oluyor. Böylece CDN'e **sonsuz önbellek**
> (`immutable`) verilebiliyor — resmin geç yüklenmesi sorununun en
> büyük parçası bu.
> </summary>


## `src/DailyCruising.Application/Abstractions/IImageProcessor.cs`

**satır 3**

> <summary>
> Yüklenen görseli SUNUMA HAZIR hale getiriyor (`A-60`).
>
> ⚠️ Arayüz "WebP" demiyor, "işlenmiş görsel" diyor: yarın AVIF eklenirse
> çağıran taraf değişmeyecek.
> </summary>


## `src/DailyCruising.Application/Abstractions/IMessagingRepository.cs`

**satır 14**

> <summary>
> ⚠️ İKİ TARAFLI ERİŞİM TEK METOTTA. Müşteri kendi konuşmasını, işletme
> kendi teknesinin konuşmasını görüyor. İkisi ayrı metotlar olsaydı biri
> kapsam kontrolünü unuttuğunda diğeri doğru kalır ve hata fark edilmezdi.
> </summary>


## `src/DailyCruising.Application/Abstractions/INotificationSender.cs`

**satır 38**

> <summary>
> Bildirim sağlayıcılarının yapılandırması.
>
> ⚠️ Sağlayıcı seçimi ORTAM DEĞİŞKENİNDEN geliyor, koddan değil. Sebep: aynı
> ikili (`Postmark` + `Netgsm`) yarın `Brevo` olabilir ve o gün yalnız
> yapılandırma değişmeli. Ödeme sağlayıcısında da aynı ilke → `G-03`.
> </summary>

**satır 87**

> <summary>
> Sunucu jetonu. ⚠️ Postmark'ın TEST jetonu
> (`POSTMARK_API_TEST`) gönderim yapmadan başarılı cevap döner; canlıya
> çıkarken gerçek jetonla değiştirilmeli.
> </summary>

**satır 113**

> <summary>
> ⚠️ Netgsm'de IP kısıtı KAPALI bırakılmalı ya da sunucu IP'si eklenmeli.
> Eski sistemde SMS sağlayıcısı (Verimor) tam bu yüzden canlıda
> patlamıştı — kod doğruydu, IP listede değildi → [[genel-kararlar]]
> </summary>

**satır 121**

> <summary>
> Uygulamanın dışarıya görünen adresi.
>
> `IOptions&lt;&gt;` yerine düz sınıf: Application katmanı hiçbir pakete bağlı
> değil ve öyle kalmalı. Değeri `Program.cs` yapılandırmadan okuyup tekil
> örnek olarak kaydediyor.
>
> ⚠️ Parola sıfırlama ve e-posta doğrulama linkleri BU adresten kurulur,
> `Request.Host`'tan DEĞİL. `AllowedHosts` gevşek olduğunda saldırgan sahte
> bir Host başlığı gönderip kendi sunucusuna işaret eden bir sıfırlama linki
> ürettirebilir — kullanıcı tıkladığında jeton saldırgana gider.
> </summary>


## `src/DailyCruising.Application/Abstractions/INotificationThrottle.cs`

**satır 3**

> <summary>
> HEDEF BAZLI GÖNDERİM SINIRI.
>
> ⚠️ Bu sınıf bir denetim bulgusundan doğdu (2026-08-25) ve kapattığı açığı
> **rezervasyon onayını bağlayan değişikliğin kendisi açmıştı**:
>
> `POST /api/reservations` KİMLİKSİZ ve `contactPhone` / `contactEmail`
> alanlarının sahipliğini DOĞRULAMIYOR. Onay gönderimi bağlanmadan önce
> oraya üçüncü bir kişinin numarasını yazmanın hiçbir etkisi yoktu. Bağlandığı
> an aynı alan şuna dönüştü: **istediğin numaraya, bizim paramızla, ücretli
> SMS gönderten bir uç.**
>
> Mevcut hız sınırı IP başına (15 dakikada 10) ve vekil havuzuyla aşılıyor.
> Aşılamayan tek şey KURBANIN NUMARASI — sınır oraya konuyor.
>
> Sınır rezervasyonu ENGELLEMİYOR, yalnız gönderimi durduruyor: meşru bir
> müşteri arka arkaya üç tur alabilmeli ve kodu HTTP cevabında zaten dönüyor.
> </summary>


## `src/DailyCruising.Application/Abstractions/IOfferRepository.cs`

**satır 55**

> <summary>
> Teklifi KOŞULLU olarak sonlandırır — yalnız `Sent` durumundayken.
>
> ⚠️ Oku-değiştir-yaz DEĞİL: müşteri kabul ederken satıcı iptal ederse
> ikisi de kendi okumasına göre yazar ve son yazan kazanırdı.
> Etkilenen satır sayısı döner.
> </summary>

**satır 74**

> <summary>
> Kabul edilen teklifin rezervasyonunu ekler.
>
> ⚠️ `ReservationRepository` KULLANILMIYOR: o, fiyat listesinden gelen
> bir `Quote` bekliyor ve sefer arayıp açıyor. Teklifte tutar zaten
> belli ve sefer zaten TUTULMUŞ — o yolu zorlamak, ikinci bir sefer
> açma denemesine ve kendi tuttuğu tarihle çakışmaya yol açardı.
> </summary>


## `src/DailyCruising.Application/Abstractions/IPartnerApplicationRepository.cs`

**satır 11**

> <summary>
> YENİDEN BAŞVURU ADAYI (`A-55`) — yalnız şu üçü birden tutarsa dolu döner:
> vergi numarası kayıtlı, kayıt `Rejected` durumunda, VE başvuru
> e-postası o işletmenin SAHİBİNİN e-postasıyla aynı.
>
> ⚠️ E-posta eşleşmesi şart. Vergi numarası yarı-kamusal bir bilgi;
> yalnız ona bakılsaydı numarayı bilen herkes reddedilmiş bir kaydı
> kendi hesabına açtırabilirdi.
> </summary>

**satır 23**

> <summary>
> Parola teyidi. ⚠️ Servis katmanında yapılamıyor: `IPasswordHasher`
> orada var ama parola ÖZETİ `Users` tablosunda ve bu depo onu okuyor.
> </summary>


## `src/DailyCruising.Application/Abstractions/IPartnerDocumentRepository.cs`

**satır 10**

> <summary>
> ⚠️ `FileKey` DÖNMÜYOR. Anahtar depolama adresinin bir parçası; panele
> düşmesi gereksiz ve sızarsa doğrudan erişim denemesine davetiye olur.
> İndirme ayrı ve yetkili bir uçtan yapılmalı → `A-62`
> </summary>

**satır 17**

> <summary>⚠️ KAPSAM FİLTRELİ — başka işletmenin evrakı `null` döner.</summary>

**satır 20**

> <summary>
> ⚠️ KAPSAM FİLTRESİ YOK — yalnız platform personeli için. Çağıran
> yetkiyi doğrulamak ve erişimi günlüğe yazmak ZORUNDA.
> </summary>


## `src/DailyCruising.Application/Abstractions/IPartnerStaffRepository.cs`

**satır 6**

> <summary>
> İşletmenin kendi rolleri ve çalışanları.
>
> ⚠️ HER SORGU `partnerId` ALIR. Kapsam filtresi burada, servis katmanında
> değil: servis "bu benim mi" diye kontrol etseydi, kontrolü unutan yeni bir
> çağrı yolu sessizce başka işletmenin verisini döndürürdü. Parametresiz bir
> "hepsini getir" metodu bilerek YOK.
> </summary>

**satır 44**

> <summary>
> Parola teyidi. ⚠️ Servis katmanında yapılamıyor: `IPasswordHasher`
> orada var ama parola ÖZETİ `Users` tablosunda ve bu depo onu okuyor.
> </summary>

**satır 50**

> <summary>
> Sahipliği devreder — TEK İŞLEMDE.
>
> ⚠️ `IX_PartnerMembers_SingleOwner` işletme başına tek sahip garantisi
> veriyor. İki satır ayrı ayrı güncellenseydi arada bir an İKİ sahip
> olurdu ve benzersiz indeks devri reddederdi.
> </summary>

**satır 60**

> <summary>
> Rol HERHANGİ bir üyelik satırında kullanılıyor mu — `Status` FARK ETMEZ.
>
> ⚠️ Bu, <see cref="CountMembersPerRoleAsync"/>'den farklı bir sorudur ve
> ikisini karıştırmak gerçek bir hataydı: çıkarılmış çalışanın satırı
> duruyor ve `RoleId`'si hâlâ o rolü gösteriyor. Yalnız aktifleri sayıp
> "rol boşta" demek, `PartnerMembers.RoleId` üzerindeki RESTRICT yabancı
> anahtarına çarpan bir silme denemesi üretiyordu.
>
>   `CountMembersPerRoleAsync` → panelde gösterilecek KAÇ KİŞİ (aktif)
>   `RoleInUseAsync`           → SİLİNEBİLİR Mİ (hepsi)
> </summary>

**satır 78**

> <summary>
> GÜVENLİK DAMGASINI YÜKSELTİR (`A-44`) — bu kullanıcıların elindeki
> erişim jetonları ANINDA geçersizleşir.
>
> ⚠️ Yetkiyi değiştiren HER yolda çağrılmak zorunda. Bir yol atlanırsa
> koruma o yolda sessizce kalkar: veritabanı doğru olur, jeton donmuş
> kalır ve kimse fark etmez.
>
> Rol yetkileri değiştiğinde o role bağlı TÜM kullanıcılar etkileniyor;
> bu yüzden kullanıcı listesi alıyor, tek kullanıcı değil.
> </summary>

**satır 98**

> <summary>
> Kullanıcının üyeliği — HANGİ işletmede olursa olsun.
>
> Kapsam kuralının istisnası ve tek meşru sebebi var: `PartnerMembers.UserId`
> benzersiz, yani bir kullanıcı en fazla bir işletmede çalışır. Başka
> işletmede üye olan birini eklemeye çalışmak veritabanı hatası verirdi;
> önce bakıp anlaşılır bir mesaj döndürebilmek için bu metot var.
> ⚠️ Dönen nesnenin `PartnerId`'si ÇAĞIRANA GÖSTERİLMEZ.
> </summary>


## `src/DailyCruising.Application/Abstractions/IPlatformRepository.cs`

**satır 9**

> <summary>
> ⚠️ KAPSAM FİLTRESİ YOK ve bu KASITLI: platform personeli muaf
> (Mert, 2026-08-24). Muafiyetin bedeli olay günlüğünde ödeniyor —
> `PlatformService` her erişimde `platform.data.accessed` yazıyor.
> </summary>

**satır 40**

> <summary>
> İşletmenin GELECEK, ÖDENMİŞ rezervasyonlarını iptal eder (`A-54`).
> İptal edilen rezervasyon sayısını döndürüyor.
>
> ⚠️ %100 iade ve `PartnerCancellation` sebebi ile: kademeli iade
> müşterinin kendi vazgeçmesi için tasarlandı, burada müşterinin
> hiçbir kusuru yok.
> </summary>


## `src/DailyCruising.Application/Abstractions/IPricingCatalogRepository.cs`

**satır 6**

> <summary>
> Kiralama tipi ve fiyat deposu.
>
> ⚠️ KAPSAM ZİNCİRİ: fiyat → kiralama tipi → tekne → işletme. Her metot
> zincirin TAMAMINI `WHERE`'e koyuyor; yalnız `priceId` ile çalışan bir metot
> bilerek yok. Zincirin bir halkası atlanırsa başka işletmenin fiyatı, kimliği
> tahmin edilerek düzenlenebilirdi.
> </summary>


## `src/DailyCruising.Application/Abstractions/IReviewRepository.cs`

**satır 8**

> <summary>
> Daveti ÖZETİYLE bulur.
>
> ⚠️ Karşılaştırma **SHA-256** ile; bcrypt kullanılırsa `WHERE` hiç
> eşleşmez (`A-03` uyarısı). Düz metin jeton veritabanında hiç durmuyor:
> salt-okunur bir yedek ya da raporlama replikası sızarsa düz metin liste
> doğrudan kullanılabilir olurdu.
> </summary>

**satır 26**

> <summary>
> Daveti TÜKETİR — kullanılmamışsa. Etkilenen satır sayısı döner;
> 0 ise başka bir istek arada tüketmiştir.
>
> ⚠️ Oku-değiştir-yaz DEĞİL, koşullu `UPDATE`. "Önce oku, kullanılmamışsa
> yaz" iki eşzamanlı isteğin ikisini de geçirirdi ve aynı tur iki kez
> puanlanırdı → [[api-desenler]].
> </summary>


## `src/DailyCruising.Application/Abstractions/ISupportRepository.cs`

**satır 17**

> <summary>
> ⚠️ İKİ TARAFLI: müşteri kendi talebini, platform personeli HEPSİNİ
> görüyor. Muafiyetin bedeli olay günlüğünde ödeniyor
> ([[api-desenler]] — platform erişimi yazılır).
> </summary>


## `src/DailyCruising.Application/Authentication/AccountService.cs`

**satır 232**

> ⚠️ TALEP DE KAYDA GEÇİYOR, yalnız tamamlanması değil.
>
> `EmailChangeCompleted` baştan beri yazılıyordu ama `...Requested`
> yazılmıyordu. Fark önemli: hesap devralma zincirinde saldırgan
> TALEBİ yapar, kurban uyarı e-postasını görüp parolasını değiştirir
> ve değişiklik hiç tamamlanmaz. O senaryoda saldırının TEK izi bu
> kayıt olurdu — tamamlanmamış bir devralma denemesi başka hiçbir
> tabloda görünmez (`PendingEmail` sonradan temizlenir).
>
> Hedef adres payload'a KONMUYOR: `EventLogs` temizlenemiyor ve o
> adres üçüncü bir kişiye ait olabilir (yanlış yazım) → `A-12`


## `src/DailyCruising.Application/Authentication/AuthService.cs`

**satır 79**

> Başarısız giriş KAYDEDİLİYOR. Kaba kuvvet ve doldurma
> saldırılarının tek görünür izi bu; hiçbir tablo "denendi ve
> olmadı"yı tutmuyor.
>
> ⚠️ DENENEN ADRES de yazılıyor (Mert, 2026-08-24). Aynı gün
> "adresi yazma, tablo değişmez ve süresiz saklanıyor" diye
> bırakılmıştı; Mert suistimal analizini tercih etti.
>
> BEDELİ GERİ ALINAMAZ: `EventLogs` append-only ve `UPDATE`/`DELETE`
> tetikleyiciyle reddediliyor, yani buraya giren adres silinemez.
> Hesabı olmayan birinin adresi de düşüyor — biri e-postasını
> yanlış yazınca ÜÇÜNCÜ bir kişinin adresi kalıcı olarak kaydedilir.
> KVKK akışında bu satır ayrıca ele alınacak -> `A-12`.
>
> Adres normalize ediliyor: aynı hesabı hedefleyen denemeler
> "Ali@X" / "ali@x" diye ikiye ayrılmasın, sayım bozulmasın.

**satır 144**

> ⚠️ ZATEN KULLANILMIŞ JETON, "yok" ya da "süresi dolmuş"tan FARKLI
> bir olaydır ve çok daha ciddidir.
>
> Döndürme (rotation) yüzünden her yenileme jetonu tam olarak BİR KEZ
> kullanılabiliyor. İkinci kullanım iki şeyden biri: jeton çalınmış
> (hem saldırgan hem meşru kullanıcı aynı jetonu deniyor) ya da meşru
> istemci ağ tekrarı yüzünden aynı isteği iki kez göndermiş.
>
> Önceden bu dal `stored is null` ile AYNI koda düşüyordu: hiçbir iz
> kalmıyordu. Üstelik hemen aşağıdaki yorum "zincir ReplacedById
> üzerinden izlenebiliyor" diyordu — oysa `ReplacedById` HİÇBİR YERDE
> atanmıyordu, yani zincir hiç kurulmuyordu (2026-08-25'te bulundu).
>
> Müşteriye dönen cevap DEĞİŞMİYOR: "oturum süresi dolmuş". Ayrım
> yalnız günlükte — aksi halde saldırgana jetonun gerçek olduğunu
> söylemiş olurduk.
> ⚠️ ZATEN KULLANILMIŞ JETON, "yok" ya da "süresi dolmuş"tan FARKLI
> bir olaydır ve çok daha ciddidir.
>
> Döndürme (rotation) yüzünden her yenileme jetonu tam olarak BİR KEZ
> kullanılabiliyor. İkinci kullanım iki şeyden biri: jeton çalınmış
> (hem saldırgan hem meşru kullanıcı aynı jetonu deniyor) ya da meşru
> istemci ağ tekrarı yüzünden aynı isteği iki kez göndermiş.
>
> Müşteriye dönen cevap DEĞİŞMİYOR: "oturum süresi dolmuş". Ayrım
> yalnız günlükte — aksi halde saldırgana jetonun gerçek olduğunu
> söylemiş olurduk.

**satır 189**

> DÖNDÜRME (rotation). Önce yeni jeton yazılıyor, SONRA eskisi koşullu
> olarak iptal edilip zincire bağlanıyor.
>
> ⚠️ SIRA ÖNEMLİ ve ters çevrilemez: `ReplacedById` yabancı anahtar,
> yani var olmayan bir satıra işaret edemez. Yeni jeton önce yazılmalı.
>
> ⚠️ Bu ara pencerede süreç ölürse geriye "hiç kimseye verilmemiş"
> bir jeton kalır. Zararsız: düz metni yalnız bu isteğin cevabında
> dönecekti ve cevap hiç dönmedi — kimse o jetonu bilmiyor.

**satır 206**

> YARIŞI KAYBETTİK: aynı jetonla başka bir istek bizden önce
> döndürmeyi tamamladı. Bu, tam olarak yukarıdaki yeniden kullanım
> durumudur — yalnız iki istek AYNI ANDA geldiği için ilk kontrol
> ikisini de temiz görmüştü.
>
> ⚠️ Bu dal ÖNCE yalnız günlüğe yazıyordu, zinciri kapatmıyor ve
> uyarı postası göndermiyordu. Yani yeniden kullanımın NASIL
> saptandığına göre farklı davranıyorduk. İki dal da aynı yardımcıyı
> çağırıyor: sonuç, tespitin yoluna değil olayın kendisine bağlı.
>
> Testi yazınca çıktı: aynı `DbContext` içinde `ExecuteUpdateAsync`
> değişiklik takipçisini atladığı için ilk kontrol bayat veriyle
> "temiz" diyor ve akış hep BU dala düşüyordu.

**satır 249**

> ⚠️ Olay YALNIZ gerçekten bir oturum kapandığında yazılıyor.
> Her çağrıda yazılsaydı, uydurma jetonla yapılan çağrılar da
> "çıkış yapıldı" gibi görünür ve "bu hesap ne zaman kapandı"
> sorusunun cevabı kirlenirdi.

**satır 284**

> ⚠️ Tuple alanı `Auth`, `Result` DEĞİL. `(await X).Result` yazımı,
> engelleyici `Task.Result` deseniyle GÖRSEL OLARAK aynı; burada
> `await` zaten önce çalıştığı için kilitlenme riski yok ama kodu
> tarayan biri (ya da bir çözümleyici) yanlış teşhis edip "düzeltmeye"
> kalkabilirdi. Denetim bunu işaret etti.

**satır 293**

> <summary>
> Jetonları üretir ve kaydedilen varlığı da döndürür.
>
> ⚠️ `Id` KODDA üretiliyor (`Guid.CreateVersion7()`), veritabanı
> varsayılanı beklenmiyor. Sebep: yenileme yolunda eski jetonun
> `ReplacedById`'si bu kimliğe bağlanacak ve bağlama KOŞULLU bir UPDATE
> ile yapılıyor — kimliğin önceden bilinmesi gerekiyor.
>
> `uuidv7()` varsayılanı tabloda duruyor ve elle atılan `INSERT`'lerde
> hâlâ çalışıyor; burada yalnız uygulama kendi değerini veriyor.
> </summary>

**satır 374**

> ⚠️ UYARI POSTASI YALNIZ GERÇEKTEN BİR ŞEY KAPANDIYSA.
>
> Her tespitte gönderilseydi saldırgan aynı ölü jetonu tekrar tekrar
> sunup kurbana posta yağdırabilirdi — rezervasyon ucunda kapatılan
> bombalama açığının aynısı. Zincir bir kez kapandıktan sonra iptal
> edilecek bir şey kalmıyor ve tekrarlar sessiz kalıyor.

**satır 386**

> <summary>
> Çalınmış jeton uyarısı (Mert, 2026-08-26 / S-17).
>
> ⚠️ Gönderim hatası KİMLİK AKIŞINI BOZMAZ. Zincir zaten kapatıldı; posta
> gitmedi diye çağırana farklı bir cevap dönmek, hem saldırgana bilgi
> verir hem de zaten yapılmış olan korumayı geri almaz.
>
> ⚠️ Postada IP ya da cihaz bilgisi YOK. Kullanıcıya "şu IP'den girildi"
> demek, yanlış pozitifte kendi IP'sini gösterip paniğe yol açıyor; gerçek
> saldırıda ise kurbanın yapabileceği bir şey değil. Yapılması gereken tek
> şey söyleniyor: parolanı değiştir.
> </summary>

**satır 439**

> <summary>
> Olay günlüğüne yazılacak e-posta adresi. Küçük harfe indiriliyor ki aynı
> hedefe yapılan denemeler `Ali@X` / `ali@x` diye ikiye bölünmesin.
>
> ⚠️ BİÇİM DOĞRULANIYOR, yalnız kesilmiyor. Denetim (2026-08-24) şunu
> gösterdi: alan serbest metindi ve giriş kutusuna yazılan HER ŞEY —
> yanlışlıkla yapıştırılmış bir parola, rastgele bir not, üçüncü birinin
> verisi — 254 karaktere kadar `EventLogs`'a düşüyordu. O tablo
> temizlenemiyor, yani yanlış giden şey kalıcı.
>
> E-postaya benzemeyen girdi, girdinin KENDİSİ yerine sabit bir işaretle
> kaydediliyor: deneme sayısı ve IP korelasyonu korunuyor, içerik
> saklanmıyor. Kontrol kasıtlı olarak gevşek — RFC 5322'yi tam doğrulamak
> amaç değil, serbest metni dışarıda tutmak amaç.
> </summary>


## `src/DailyCruising.Application/Authorization/Permissions.cs`

**satır 45**

> <summary>
> İade talimatını SAĞLAYICIYA gönderme yetkisi (`A-29`).
>
> ⚠️ `reservation.cancel`'dan AYRI ve bilerek. İptal, iade tutarını
> hesaplayıp donduruyor ama parayı OYNATMIYOR; asıl para hareketi bu
> yetkiyle oluyor. İkisi tek yetkide toplansaydı, müşteri iptali
> yapabilen destek personeli aynı anda platform kasasından para
> çıkarabilirdi. `IsPartnerAssignable = false`: tekne sahibi kendi
> çalışanına iade yetkisi veremez.
> </summary>


## `src/DailyCruising.Application/Billing/EarningCalculator.cs`

**satır 6**

> <summary>
> HAKEDİŞ HESABI — TEK YER (`A-41`).
>
> ⚠️ Bu sınıf, aynı formülün iki yerde yaşamasını engellemek için var.
> `LedgerService` defteri yazarken, ödeme akışı sağlayıcıya "bu paranın şu
> kadarı işletmenin" derken AYNI sayıyı kullanmak zorunda. İki ayrı hesap
> bugün aynı sonucu verir, komisyon ya da kupon kuralı değiştiği gün
> ayrışır — ve ayrıştığında belirti "defter tutmuyor" değil, **işletmeye
> yanlış tutar ödenmesi** olur.
> </summary>


## `src/DailyCruising.Application/Billing/LedgerService.cs`

**satır 7**

> <summary>
> PARA DEFTERİ (`A-18`).
>
> Her rezervasyonun para hareketi ÇİFT TARAFLI kaydediliyor: bir tarafın
> alacağı diğerinin borcu. Bir dönemin bütün kayıtlarının toplamı SIFIR
> olmalı — tutmuyorsa hesap yanlıştır ve bu tek kontrolle görülür.
>
> ⚠️ DÜZELTME GÜNCELLEME DEĞİL TERS KAYIT. `trg_ledger_entries_immutable`
> UPDATE ve DELETE'i reddediyor; iade, ödemenin kaydını değiştirmiyor,
> karşısına ters işaretli yeni kayıt yazıyor. Böylece "ne oldu" sorusunun
> cevabı geçmişe dönük değişmiyor.
> </summary>

**satır 21**

> <summary>
> Ödeme alındığında dört kayıt yazılır ve toplamları sıfırdır:
>
>   Müşteri  −GrandTotal      (parayı verdi)
>   Platform +GrandTotal      (tahsil etti)
>   Platform −PartnerEarning  (işletmeye borçlandı)
>   İşletme  +PartnerEarning  (alacaklı)
>
> `PartnerEarning = TotalTry + ExtrasTotalTry − komisyon − işletmenin
> karşıladığı indirim`. Platformun üstlendiği artık (`PlatformAbsorbedTry`)
> işletmeden DÜŞÜLMÜYOR — `S-15`: kimse borca girmiyor.
>
> ⚠️ MÜKERRER YAZIMA KARŞI KORUMALI. Ödeme sağlayıcısı aynı bildirimi iki
> kez gönderebilir; ikinci çağrı hiçbir şey yazmıyor.
> </summary>

**satır 51**

> ⚠️ Formül BURADA DEĞİL. Ödeme akışı da sağlayıcıya aynı sayıyı
> söylüyor; iki kopya bir gün ayrışırdı → `EarningCalculator`.

**satır 68**

> <summary>
> İptal iadesinde TERS KAYIT.
>
> `S-16` (Mert): komisyon da AYNI ORANDA iade ediliyor. %50 iadede
> platform kendi payının da yarısını geri veriyor, yani iki taraf da aynı
> oranda kaybediyor.
>
> ⚠️ Ödeme kaydı yoksa hiçbir şey yazılmıyor: ödenmemiş bir rezervasyonun
> iadesi yok. Bugün ödeme akışı henüz yazılmadığı (`A-29`) için normal yol
> budur ve sessizce geçmesi doğrudur.
> </summary>


## `src/DailyCruising.Application/Boarding/BoardingContracts.cs`

**satır 19**

> <summary>
> ⚠️ `Manual` BURADAN GELEMEZ. Elle işaretleme jeton gerektirmiyor ve
> ayrı bir ucu var; bu alandan kabul edilseydi, jetonu olan biri işlemi
> "elle işaretleme" gibi kaydedip denetim izini bulandırabilirdi.
> </summary>

**satır 30**

> <summary>
> ELLE BİNİŞ (`G-12`, Mert 2026-08-24 seçenek c): iskelede internet yokken QR
> okutulamıyor, tekne sahibi internet gelince panelden işaretliyor.
>
> Jeton DEĞİL rezervasyon kodu alıyor: elle işaretlemenin sebebi zaten
> jetonun okutulamamış olması.
>
> ⚠️ Bu, QR'dan DAHA ZAYIF bir kanıttır — müşterinin o an orada olduğunu
> göstermiyor, tekne sahibinin beyanına dayanıyor. Bu yüzden ayrı uç, ayrı
> olay kaydı ve `BoardingScans.Method = Manual` ile ayırt edilebilir kalıyor.
> </summary>


## `src/DailyCruising.Application/Boarding/BoardingService.cs`

**satır 7**

> <summary>
> QR BİNİŞ DOĞRULAMA.
>
> Bu servisin en önemli özelliği neyi ENGELLEMEDİĞİ:
>
> ⚠️ <b>Eksik yolcu bilgisi binişi ENGELLEMEZ</b> (Mert, 2026-08-22).
> "Ödemiş müşteriyi form yüzünden tekneye almamak iade talebi ve kötü yorum
> üretir." Yolcu listesi kontrolü bu dosyada bilerek YOKTUR; sonuçta yalnız
> bir UYARI bayrağı dönüyor ki tekne sahibi panelden tamamlayabilsin.
> Buraya bir "yolcular eksikse reddet" dalı eklenmesi, yazılı bir kararı
> bozmak olur.
>
> Reddedilen her deneme de KAYDEDİLİYOR: `BoardingScans.Succeeded = false`.
> Suistimal sinyali başka hiçbir yerde görünmüyor — reddedilen okutma hiçbir
> satırı değiştirmiyor.
> </summary>

**satır 45**

> <summary>
> Çağıranın işletmesi VE kimliği.
>
> ⚠️ `UserId` de kontrol ediliyor. Bugün jeton üretimi `sub` olmadan
> `partner_id` koymuyor, yani ikisi birlikte gelir — ama bu tek bir
> uygulamanın örtük garantisi. `UserId!.Value` yazmak, ileride servis
> hesabı ya da API anahtarı gibi bir yol eklendiğinde sessizce
> `NullReferenceException` üretirdi. Projenin geri kalanı da `UserId`'yi
> nullable olarak ele alıyor. Denetim bulgusu (2026-08-25).
> </summary>

**satır 94**

> ⚠️ BURAYA `BoardingScans` SATIRI YAZILAMIYOR: o tablo
> `ReservationId` istiyor ve elimizde bir rezervasyon yok. Yani
> "hiç tanınmayan jeton" denemesinin TEK izi olay günlüğüdür —
> controller yazıyor. Bu kayıt kaldırılırsa jeton deneme
> saldırısı hiçbir yerde görünmez olur.
>
> "Jeton yok" ile "başka işletmenin jetonu" ayırt EDİLMİYOR:
> ayırt edilseydi ele geçirilen bir jetonun hangi işletmeye ait
> olduğu deneme yanılmayla bulunabilirdi.

**satır 177**

> ⚠️ YOLCU LİSTESİ YAZMADAN ÖNCE OKUNUYOR.
>
> Önce yazılıp sonra okunuyordu ve bu, başarılı bir binişi başarısız
> gösterebiliyordu: durum `Boarded`'a çekildikten SONRA yolcu adları
> sorgusu düşerse istisna `BoardingException` olmadığı için 500'e
> dönüşüyordu — müşteri iskelede "biniş başarısız" duyuyor, oysa
> veritabanında binmiş görünüyordu. Bu sorgu yazılan hiçbir şeye
> bağlı değil (`Passengers` bu akışta değişmiyor), yani sıra bedelsiz
> değiştirilebiliyor. Denetim bulgusu (2026-08-25).

**satır 227**

> ⚠️ KONUŞMA AYNI İŞLEMDE KAPANIYOR. Ayrı bir iş olsaydı
> biniş ile kapanma arasında müşteri mesaj yazmaya devam
> edebilirdi — ve o pencere dakikalarca sürebilirdi.
>
> Misafir rezervasyonunda konuşma yok; 0 döner, hata değil.

**satır 260**

> ⚠️ Bebek yolcu listesine girer ama koltuk tüketmez; "eksik mi"
> sorusu TOPLAM kişi sayısına göre soruluyor.

**satır 309**

> ⚠️ BU CATCH ŞART ve üstteki yorumun iddiasını KOD HALİNE getiriyor.
>
> Yakalanmasaydı kayıt hatası, hemen ardından fırlatılacak
> `BoardingException`'ın YERİNE geçerdi: okutan kişi "iptal edilmiş
> rezervasyon" yerine anlamsız bir 500 görürdü ve reddin sebebi
> olay günlüğüne de yazılmazdı — yani denetim izini korumak için
> konan kayıt, denetim izini yok etmiş olurdu.
> Denetim (2026-08-25) yorumun yalan söylediğini yakaladı.
>
> Kayıt kaybı burada kabul ediliyor: red zaten `EventLogs`'a
> controller tarafından ayrıca yazılıyor.


## `src/DailyCruising.Application/Catalog/BoatCatalogContracts.cs`

**satır 65**

> <summary>
> Tekne yaratma/güncelleme gövdesi.
>
> ⚠️ `Status` BURADA YOK. Durum ayrı bir uçtan değişiyor: yayından kaldırmak
> bir güncelleme değil, satışı durduran bir KARAR. Aynı gövdede olsaydı
> "kapasiteyi düzeltirken yanlışlıkla yayından kaldırma" mümkün olurdu ve
> olay günlüğünde ikisi ayırt edilemezdi.
>
> ⚠️ `Slug` de yok: URL adı yaratılışta addan türetiliyor ve DEĞİŞMİYOR.
> Değişseydi paylaşılmış her bağlantı sessizce kırılırdı.
> </summary>

**satır 111**

> <summary>
> YAYINDAN KALDIRMANIN BEDELİ (`A-45`, Mert soru 3).
>
> ⚠️ Yayından kaldırmak satılmış turları İPTAL ETMİYOR — tersi olsaydı tek
> tık binlerce lirayı iade sürecine sokardı. Ama işletme bunu bilmeden
> tekneyi çektiğini sanabilir ve önümüzdeki hafta 40 kişiyi ağırlamak
> zorunda olduğunu fark etmeyebilir.
>
> Bu kayıt uyarının verisini taşıyor: karar işletmede kalıyor, ama
> bilgisiz kalmıyor.
> </summary>

**satır 166**

> <summary>⚠️ Yalnız sabit metin — çağıranın gönderdiği hiçbir şey değil.</summary>


## `src/DailyCruising.Application/Catalog/BoatCatalogService.cs`

**satır 21**

> <summary>
> ⚠️ Platform personeli bu servisi KULLANAMAZ. `PartnerId` boş olduğu için
> burada patlar — ve bu doğru: platformun tekne düzenlemesi ayrı bir uç
> (`A-38`) ve her erişimi olay günlüğüne yazılmak zorunda. Sessizce
> "kapsamsız" çalıştırılsaydı o borç ödenmeden muafiyet kullanılırdı.
> </summary>

**satır 74**

> ⚠️ DOĞRUDAN YAYINDA. Platform onayı beklenmiyor
> ([[domain-gereksinimler]] 2026-08-22) — bunun dayanağı yukarıdaki
> onaylı sözleşme kontrolü. O kontrol kaldırılırsa bu satır da
> yeniden düşünülmeli.

**satır 136**

> ⚠️ AD DEĞİŞİRSE SLUG DA DEĞİŞİYOR (`A-46`, Mert soru 4).
>
> Eskiden `Slug` bilerek dokunulmuyordu ve gerekçe *"paylaşılmış
> bağlantıları kırar"* idi. Gerekçe artık geçerli değil: eski adres
> `BoatSlugs`'ta duruyor ve `301` ile yenisine yönlendiriyor. Adını
> tamamen değiştiren bir işletme eski URL'yle yaşamak zorunda
> kalmıyor.
>
> `Status` hâlâ dokunulmuyor — ayrı bir uçtan değişiyor.

**satır 176**

> ⚠️ SLUG SAVE'DEN SONRA ve yalnız AD GERÇEKTEN DEĞİŞTİYSE.
> Her güncellemede yeni slug üretilseydi, kapasiteyi düzelten bir
> işletme farkında olmadan adresini değiştirir ve eski bağlantılar
> gereksiz yere yönlendirmeye düşerdi.

**satır 197**

> <summary>
> Durum değişikliği AYRI uçtan — yayından kaldırmak bir düzenleme değil,
> satışı durduran bir karar. Olay günlüğünde de ayrı görünmesi gerekiyor.
>
> ⚠️ Yayından kaldırmak MEVCUT REZERVASYONLARI İPTAL ETMEZ. Tekne satıştan
> çekilir, satılmış turlar yapılır. Tersi olsaydı bir tık binlerce lirayı
> iade sürecine sokardı → Mert'e sorulacak: kaldırma anında gelecekteki
> seferler için uyarı gösterilmeli mi?
> </summary>
> <returns>
> Önceki durum, ya da durum ZATEN istenendiyse <c>null</c>.
>
> ⚠️ Dönüş tipi `Task` iken controller olayı KOŞULSUZ yazıyordu ve durum
> hiç değişmediğinde günlüğe `from == to` taşıyan sahte bir "değişti"
> satırı düşüyordu — yani günlüğün tek amacı olan "tekne ne zaman satıştan
> çekildi" sorusu güvenilmez hale geliyordu. Denetim bulgusu (2026-08-26).
>
> Önceki durumu BURADAN döndürmek ayrıca çift okumayı da kapatıyor:
> controller önce `GetAsync` ile okuyup sonra buranın tekrar okumasına
> sebep oluyordu ve iki okuma arasında durum değişirse günlüğe yanlış
> `from` yazılabilirdi.
> </returns>
> <summary>
> Yayından kaldırmanın bedeli (`A-45`). İşlemi ENGELLEMİYOR — yalnız
> panelin uyarı gösterebilmesi için veri veriyor.
>
> ⚠️ Engelleme seçeneği bilerek elendi (Mert, soru 3): tekne
> arızalandığında işletmenin yapacak bir şeyi kalmazdı.
> </summary>

**satır 333**

> ⚠️ Ticari kapasite SATILAN koltuk, yasal kapasite belgedeki üst sınır.
> Ticari > yasal olsaydı tekne yasal sınırının üstünde dolabilirdi ve
> bunu fark eden tek yer liman kontrolü olurdu.

**satır 381**

> <summary>
> URL adı üretir ve çakışırsa sonuna numara ekler.
>
> ⚠️ Bu bir OKU-SONRA-YAZ: iki eşzamanlı istek aynı numarayı bulabilir.
> Son sözü `IX_Boats_Slug` benzersiz indeksi söylüyor ve depo katmanı onu
> anlaşılır mesaja çeviriyor — buradaki döngü yarışı çözmüyor, YAYGIN
> durumda kullanıcıya numara sormaktan kurtarıyor.
> </summary>

**satır 416**

> <summary>
> "Mavi Yolculuk Gulet'i" → "mavi-yolculuk-guleti".
>
> ⚠️ TAŞIYICI OLAN TEK HARF "ı". `FormD` ayrıştırması "ş"→"s", "ğ"→"g",
> "ü"→"u", "ö"→"o", "ç"→"c" çevirisini ZATEN yapıyor (aksan işareti
> ayrılıp düşüyor); ama "ı" (noktasız i) ayrışmıyor, ASCII harf de
> olmadığı için AŞAĞIDAKİ DÖNGÜDE TAMAMEN DÜŞÜYOR: "Ilıca" → "ilca".
>
> Diğerleri yine de açıkça yazılı: kullanıcıya görünen bir URL'nin
> Unicode ayrıştırma tablosunun ayrıntısına bağlı kalması istenmedi.
> Mutasyon testiyle ölçüldü (2026-08-26) — "ş" satırı kaldırılınca test
> yeşil kalıyor, "ı" satırı kaldırılınca kırmızıya dönüyor.
> </summary>


## `src/DailyCruising.Application/Catalog/PricingCatalogContracts.cs`

**satır 83**

> <summary>
> ⚠️ İkisi de boş = TEMEL fiyat. Biri dolu diğeri boş olamaz: açık uçlu
> bir sezon, `EXCLUDE USING gist` kısıtının çakışma tespitini anlamsız
> kılardı ve "hangi tarihte hangi fiyat" sorusu cevapsız kalırdı.
> </summary>

**satır 120**

> <summary>
> Dil kodu → çeviri. **`tr` ZORUNLU.**
>
> ⚠️ Sebep somut: `PricingRepository.GetExtrasAsync` istenen dili bulamazsa
> `tr`'ye düşüyor, o da yoksa **boş metin** döndürüyor. `tr` olmadan
> eklenen bir ek hizmet, satın alındığında rezervasyona ADI BOŞ yazılırdı
> ve hiçbir yerde hata görünmezdi.
> </summary>


## `src/DailyCruising.Application/Catalog/PricingCatalogService.cs`

**satır 25**

> <summary>
> Tekne bu işletmenin mi.
>
> ⚠️ Alt kaynakların sorguları zincirin tamamını zaten taşıyor; bu kontrol
> onların YERİNE değil, "tekne yok" ile "tipi yok" ayrımını yapabilmek
> için. Olmasaydı başkasının teknesine tip eklemek "kiralama tipi
> geçersiz" gibi yanıltıcı bir hata verirdi.
> </summary>

**satır 97**

> ⚠️ `RentalTypeId` DEĞİŞTİRİLEMİYOR. Değiştirilebilseydi, "kişi başı"
> bir tipin fiyatları girilip tip "tekne başı"na çevrilebilirdi ve
> fiyat satırları sessizce ANLAMSIZ hale gelirdi — `AdultPrice` dolu,
> `BoatPrice` boş, satılan şey tekne. Kaldırıp yeniden eklemek gerekir.

**satır 128**

> <summary>
> ⚠️ REZERVASYONU OLAN TİP SİLİNMEZ, pasife alınır.
>
> Silinebilseydi satılmış turların hangi koşullarla (hangi saatte, hangi
> yaş sınırlarıyla) satıldığı yok olurdu. Veritabanı yabancı anahtarı da
> engellerdi ama mesajı kullanıcıya bir şey anlatmazdı.
> </summary>

**satır 216**

> ⚠️ TEMEL FİYAT SEZONA ÇEVRİLEMEZ, tersi de olmaz. Çevrilebilseydi
> temel fiyatı olmayan bir tip oluşurdu ve o tip HİÇBİR tarihte fiyat
> veremezdi — belirti "tekne sessizce satılamaz hale geldi" olurdu.

**satır 241**

> <summary>
> ⚠️ TEMEL FİYAT SİLİNMEZ. Silinebilseydi tip hiçbir tarihte fiyat
> veremez hale gelirdi ve tekne SESSİZCE satılamaz olurdu — işletme bunu
> ancak rezervasyon gelmediğini fark ederek anlardı.
> </summary>

**satır 336**

> ⚠️ ÇEVİRİLER YERİNDE GÜNCELLENİYOR, topluca silinip yeniden
> yazılmıyor. Silme-ekleme yapılsaydı `ExtraTranslations` satırlarının
> kimlikleri her kaydetmede değişirdi; bugün kimseyi kırmaz ama
> otomatik çeviri işi (`Source`, `SourceHash`) bu kimliklere bakacak.

**satır 378**

> <summary>
> ⚠️ SATILMIŞ EK HİZMET SİLİNMEZ, pasife alınır.
>
> `ReservationExtras.ExtraId` bu satırı gösteriyor; silinseydi "müşteri ne
> satın aldı" sorusunun cevabı kaybolurdu. Veritabanı da engellerdi ama
> mesajı kullanıcıya ne yapması gerektiğini söylemezdi.
> </summary>

**satır 406**

> <summary>
> ⚠️ `tr` ÇEVİRİSİ ZORUNLU ve sebebi somut:
> `PricingRepository.GetExtrasAsync` istenen dili bulamazsa `tr`'ye
> düşüyor, o da yoksa **boş metin** döndürüyor. `tr` olmadan eklenen bir
> ek hizmet satın alındığında rezervasyona ADI BOŞ yazılır ve hiçbir yerde
> hata görünmez — müşteri "  " satın almış olur.
> </summary>


## `src/DailyCruising.Application/Messaging/ContactMasker.cs`

**satır 5**

> <summary>
> TELEFON, E-POSTA VE IBAN MASKELEME ([[domain-gereksinimler]] 2026-08-23).
>
> Mesajlaşmanın amacı platform dışına kaçışı ÖNLEMEK. Uyarı bir kuraldır,
> mesajlaşma bir mekanizmadır — ama "beni şu numaradan ara" yazılabildiği
> sürece mekanizma da delinir.
>
> ⚠️ BU BİR GÜVENLİK DUVARI DEĞİL, BİR SÜRTÜNME KATMANI. Kararlı bir
> kullanıcı numarayı yazıyla ("sıfır beş üç iki...") ya da araya karakter
> koyarak geçirebilir. Amaç bunu imkânsız kılmak değil, KOLAY olmaktan
> çıkarmak ve denemeyi ÖLÇÜLEBİLİR yapmak — `MaskedItemCount` ısrarla
> numara paylaşmaya çalışanı gösteriyor.
> </summary>

**satır 28**

> <summary>
> Telefon: en az 10 rakam, aralarında boşluk/nokta/tire/parantez olabilir.
>
> ⚠️ `{9,}` DEĞİL `{10,}`: Türkiye numarası alan koduyla 10 hane
> (5321234567). Daha düşük tutulsaydı "12 kişilik tekne 2026 yılında"
> gibi masum metinler maskelenirdi.
>
> ⚠️ Zaman aşımı VERİLİYOR. Kullanıcı metni üzerinde çalışan bir regex,
> geri izlemeyle CPU'yu kilitleyebilir (ReDoS) — mesaj kutusu herkese açık.
> </summary>

**satır 61**

> <summary>
> Maskelenmiş metin ve kaç şeyin gizlendiği.
>
> ⚠️ ORİJİNAL METİN DEĞİŞTİRİLMİYOR — çağıran onu `Message.Body`'ye
> yazıyor. Anlaşmazlıkta platformun elinde kayıt kalmalı.
> </summary>

**satır 76**

> ⚠️ SIRA ÖNEMLİ: e-posta ÖNCE. Telefon deseni
> "iletisim2026@ornek.com" gibi bir adresin rakamlarını yakalamaz ama
> "05321234567@ornek.com" gibi bir adresi ikiye bölerdi ve geriye
> "[gizlendi]@ornek.com" kalırdı — yani alan adı sızardı.

**satır 105**

> ⚠️ Zaman aşımında METNİN TAMAMI maskeleniyor, olduğu gibi
> GEÇİRİLMİYOR. Fail-open olsaydı, saldırgan regex'i yorarak
> maskelemeyi atlatabilirdi — kasıtlı olarak yavaş bir metin
> kurmak zor değil.


## `src/DailyCruising.Application/Messaging/MessagingContracts.cs`

**satır 27**

> <summary>
> ⚠️ MASKELENMİŞ hal. Orijinal metin (`Message.Body`) yalnız platform
> yönetiminde; bu tip orijinali TAŞIMIYOR — alan hiç var olmazsa
> yanlışlıkla doldurulamaz.
> </summary>

**satır 72**

> <summary>
> Mesaj gönderiminin sonucu (`A-52`).
>
> ⚠️ `MaskingThresholdCrossed` yalnız eşiğin AŞILDIĞI mesajda `true`.
> Sonraki mesajlarda tekrar `true` olsaydı platform aynı konuşma için
> düzinelerce uyarı alır ve bildirim gürültüye dönüşürdü.
> </summary>


## `src/DailyCruising.Application/Messaging/MessagingService.cs`

**satır 6**

> <summary>
> SİSTEM İÇİ MESAJLAŞMA (`A-36`).
>
> Mert (2026-08-23): *"bütün bu konuşmalar bizim sistemimizin içerisinde olsun
> ki hem takip edebilelim, hem kullanıcıyı hem tekne sahibini koruyabilelim."*
>
> ⚠️ KONUŞMA (MÜŞTERİ × TEKNE) BAZINDA, rezervasyon bazında DEĞİL. Rezervasyon
> olmadan da açılıyor ("fiyat sorunuz" akışı) ve rezervasyondan sonra da
> sürüyor — müşteri buluşma yerini, saati, ne getireceğini soruyor.
> </summary>

**satır 39**

> ⚠️ İŞLETME KENDİ TEKNESİYLE KONUŞMA AÇAMAZ. Açabilseydi, konuşmanın
> iki tarafı da aynı işletme olur ve `SenderRole` anlamsızlaşırdı.

**satır 68**

> ⚠️ KAPALI KONUŞMA ARTIK ENGEL DEĞİL (`A-51`, Mert soru 9).
>
> Eskiden burada `ConversationClosed` fırlatılıyordu ve müşteri
> bindiği tekneye BİR DAHA HİÇ mesaj atamıyordu — gelecek sezon
> aynı tekneyi kiralamak istese bile. Depo artık yalnız AÇIK
> konuşmayı arıyor; kapalı olan bulunmuyor ve yenisi açılıyor.
>
> Her kiralama kendi konuşmasını alıyor, geçmişler ayrı ayrı
> duruyor. "Konuşmayı yeniden aç" seçeneği elendi: kapanmanın
> anlamını yitirir ve QR ile kapanma kuralını (`A-36a`) zayıflatırdı.

**satır 98**

> ⚠️ KAPALI KONUŞMAYA MESAJ GİTMİYOR. Konuşma QR okutulup biniş
> resmileştiği anda kapanıyor; kapandıktan sonra yazılabilseydi
> "kapanma" bir görüntüden ibaret olurdu.

**satır 113**

> ⚠️ Eşik ÖNCE ve SONRA karşılaştırılıyor, yalnız sonraki toplama
> bakılmıyor. Yalnız "toplam >= eşik" denseydi eşiği aştıktan sonraki
> HER mesaj yeni bir bildirim üretir ve platform aynı konuşma için
> düzinelerce uyarı alırdı — bildirim gürültüye dönüşünce kimse
> bakmaz.

**satır 163**

> ⚠️ MASKELEME BURADA, controller'da DEĞİL. Yeni bir mesaj yazma yolu
> (teklif notu, otomatik mesaj) eklendiğinde maskelemeyi unutmak
> mümkün olmasın diye tek geçit.

**satır 170**

> ⚠️ `ConversationId` DEĞİL, GEZİNTİ ÖZELLİĞİ atanıyor.
>
> Yeni konuşmanın `Id`'si veritabanı varsayılanından (`uuidv7()`)
> geliyor ve `SaveChanges`'e kadar `Guid.Empty`. Kimliği kopyalamak
> ilk mesajı `FK_Messages_Conversations_ConversationId` ihlaliyle
> düşürüyordu — canlı denemede **500** çıktı. Gezinti özelliği
> atandığında EF sırayı kendisi kuruyor.
>
> Aynı tuzağa `RefreshToken` zincirinde de düşülmüştü (2026-08-25).

**satır 195**

> <summary>
> ⚠️ EŞİK BİR TAHMİN (`A-52`). Kaç maskelemenin "ısrar" sayılacağını
> söyleyen bir veri henüz yok; beş, tek bir yanlışlıkla yazılmış
> telefondan ayrışacak kadar yüksek, ısrarı kaçırmayacak kadar düşük
> seçildi. Gerçek rakamlar biriktiğinde gözden geçirilmeli
> → [[api-benim-kararlarim]]
> </summary>


## `src/DailyCruising.Application/Messaging/MessagingTexts.cs`

**satır 3**

> <summary>
> Mesajlaşma ekranında gösterilen sabit metinler.
>
> ⚠️ SUNUCUDA duruyor, arayüzde değil. Web ve mobil ayrı ayrı yazsaydı biri
> güncellenip diğeri unutulurdu — ve bu metin bir HUKUKİ uyarı: platform
> dışında ödeme yapan müşteri neyi kaybettiğini burada okuyor.
> </summary>


## `src/DailyCruising.Application/Messaging/OfferContracts.cs`

**satır 7**

> <summary>
> ÖZEL TEKLİF gönderme (`A-36b`).
>
> ⚠️ **BURADA TUTAR VAR ve bu, "Para istemciden gelmez" kuralına AYKIRI
> DEĞİL.** O kural MÜŞTERİNİN tutar göndermesini yasaklıyor: müşteri kendi
> ödeyeceği tutarı belirleyemez. Burada tutarı SATICI koyuyor ve teklifin
> tamamı zaten "fiyat listesi yok, pazarlık var" akışının kendisi
> ([[domain-gereksinimler]] 2026-08-23).
>
> ⚠️ EK HİZMET FİYATLARI YİNE İSTEKTEN GELMİYOR: yalnız kimlik ve adet
> gönderiliyor, birim fiyat `Extras` tablosundan okunuyor. Satıcı ek hizmet
> fiyatını değiştirmek istiyorsa kataloğu düzenler — teklifte tek seferlik
> bir fiyat yazamaz, yoksa katalog ile satılan arasında kalıcı bir ayrışma
> olurdu.
> </summary>

**satır 62**

> <summary>
> 48 saat. ⚠️ Bu süre boyunca TARİH TUTULUYOR — teklif bir vaat değil,
> takvimde yer kaplayan bir rezerv.
> </summary>


## `src/DailyCruising.Application/Messaging/OfferReservationFactory.cs`

**satır 9**

> <summary>
> KABUL EDİLEN TEKLİFTEN REZERVASYON.
>
> ⚠️ `ReservationFactory.FromQuote` KULLANILMIYOR ve sebebi şu: o, `Quote`'un
> TAMAMINI dondurulacak alanların kaynağı sayıyor ("hesap ile saklanan
> arasında ikinci bir dönüşüm yok"). Teklifte fiyat hesabı YOK — tutarı
> satıcı koydu. Sahte bir `Quote` uydurup oradan geçmek, o kuralı korumak
> değil TAKLİT etmek olurdu; alanların nereden geldiği görünmez hale gelirdi.
>
> Bunun yerine her alanın kaynağı BURADA, tek tek yazılı:
>   tutar → teklif · komisyon, sözleşme, yaş sınırları → sistem ·
>   kur → kabul anı · birim fiyatlar → YOK (teklifte kırılım yok)
> </summary>

**satır 49**

> ⚠️ `Pending` VE HOLD SÜRESİ VAR — standart 15 dakika.
>
> İlk sürümde `HoldExpiresAt = null` yazmıştım, gerekçem şuydu:
> "tarih zaten teklifle tutuldu, ikinci bir sayaç kabul eden
> müşteriyi düşürür." **Veritabanı bunu reddetti**
> (`CK_Reservations_HoldExpiry`, canlı deneme 2026-08-26) ve
> haklıydı: süresi olmayan bir `Pending`, ödenmeden SONSUZA KADAR
> tekneyi tutar ve `ExpireReservationHoldsJob` onu hiç görmez.
>
> Sistemde "bekleyen rezervasyon N dakikada düşer" TEK bir kural
> var; teklife özel ikinci bir süre uydurmak, o kuralı iki yerden
> okunur hale getirirdi -> [[api-benim-kararlarim]]

**satır 68**

> ⚠️ BİRİM FİYAT YOK. Teklifte kişi başı kırılım yok — toplam var.
> Uydurma bir birim fiyat yazmak (`toplam / kişi`) muhasebeyi
> yanıltırdı: o sayı hiçbir zaman kimseye teklif edilmedi.

**satır 89**

> ⚠️ KOMİSYON SİSTEMDEN, teklifle DEĞİŞTİRİLEMEZ
> ([[domain-gereksinimler]]: "komisyon normal oranla aynı").


## `src/DailyCruising.Application/Messaging/OfferService.cs`

**satır 10**

> <summary>
> ÖZEL TEKLİF (`A-36b`).
>
> Tekne sahibi fiyat girmeden kiralama tipi tanımlayabiliyor; müşteri "fiyat
> için iletişime geçin" görüyor, sistem içinden mesajlaşıyorlar ve satıcı
> panelden özel teklif gönderiyor ([[domain-gereksinimler]] 2026-08-23).
>
> ⚠️ TEKLİF BİR VAAT DEĞİL, TAKVİMDE YER KAPLAYAN BİR REZERV. 48 saat boyunca
> tarih tutuluyor; süre dolunca serbest kalıyor. Bu, rezervasyondaki 15
> dakikalık `Pending` mekanizmasının uzun sürelisi — aynı yapı, farklı süre.
> </summary>

**satır 54**

> ⚠️ KAPALI KONUŞMADA TEKLİF YOK. Konuşma biniş sonrası kapanıyor;
> kapalıyken teklif gönderilebilseydi, tur bitmiş bir müşteriye
> takvimde yer tutan bir teklif yollanabilirdi.

**satır 79**

> ⚠️ EK HİZMET BİRİM FİYATLARI TABLODAN, istekten DEĞİL.

**satır 175**

> <summary>
> MÜŞTERİ KABUL EDİYOR → rezervasyon oluşuyor.
>
> ⚠️ Tutar TEKLİFTEN geliyor, fiyat listesinden DEĞİL — teklifin varlık
> sebebi listede fiyat olmaması. Ama kur, komisyon ve sözleşme yine
> sistemden okunuyor: satıcı komisyonunu teklifle değiştiremez
> ([[domain-gereksinimler]]: *"komisyon normal oranla aynı"*).
>
> ⚠️ Tutulan sefer SATIŞ seferine çevriliyor, yenisi açılmıyor: yeni
> sefer açmak `EX_Voyages_NoOverlapPerBoat`'a kendi tuttuğu tarih
> yüzünden takılırdı.
> </summary>

**satır 227**

> ⚠️ KUR SİSTEMDEN. Teklif dövizliyse TL karşılığı KABUL ANINDA
> hesaplanıyor — teklif anındaki kurla değil. Rezervasyon "satın alma
> anının fotoğrafı" ve satın alma anı budur.

**satır 237**

> ⚠️ SIRA: ÖNCE REZERVASYON, SONRA TEKLİFİN KAPANIŞI.
>
> `CK_Offers_Accepted` bir teklifin `Accepted` olabilmesi için
> `ReservationId`'sinin dolu olmasını istiyor. Önce teklifi
> kapatmak, aradaki anda o kısıtı ihlal ediyor ve **500**
> veriyordu (canlı deneme, 2026-08-26).
>
> Yarış koruması bu sırada da bozulmuyor: kapanış YİNE koşullu
> (`Status = Sent`) ve 0 dönerse fırlatıyoruz — istisna tüm
> işlemi geri alıyor, yani rezervasyon da yazılmamış oluyor.


## `src/DailyCruising.Application/Partners/IbanNormalizer.cs`

**satır 17**

> <summary>
> Boşlukları atıp büyük harfe çeviriyor.
>
> ⚠️ Normalleştirme UYGULAMANIN işi, veritabanının değil: kısıt
> boşluklu yazımı reddediyor ki aynı hesap iki farklı değer olarak
> durmasın.
> </summary>

**satır 45**

> <summary>
> ISO 13616 sağlaması: ilk dört karakter sona alınıyor, harfler
> sayıya çevriliyor (A=10 … Z=35), sonuç mod 97 = 1 olmalı.
>
> ⚠️ Sayı 26 haneyi aşıyor, `long`'a sığmıyor — bu yüzden basamak
> basamak kalan alınıyor. Tek seferde çevirmeye çalışmak taşma
> yüzünden SESSİZCE yanlış sonuç verirdi.
> </summary>


## `src/DailyCruising.Application/Partners/PartnerApplicationContracts.cs`

**satır 5**

> <summary>
> İŞLETME BAŞVURUSU (`A-42`) — domain akışının 3. adımı.
>
> ⚠️ `IBAN ZORUNLU` (Mert, 2026-08-26). Başvuru sürtünmesini artırıyor ama
> alternatifi daha kötü: IBAN'sız kabul edilen işletme, ödeme sağlayıcısında
> alıcı kaydı açılamayan bir kayıt olarak birikir ve bunu ancak ilk hakediş
> ödenmediğinde fark ederdik → [[api-benim-kararlarim]]
> </summary>

**satır 18**

> <summary>
> ⚠️ Anlamı <see cref="BusinessType"/>'a bağlı: şahısta TC kimlik
> numarası, diğerlerinde vergi numarası.
> </summary>


## `src/DailyCruising.Application/Partners/PartnerApplicationService.cs`

**satır 9**

> <summary>
> İŞLETME BAŞVURUSU (`A-42`).
>
> ⚠️ BU UÇ 2026-08-26'YA KADAR HİÇ YOKTU. Domain akışının 3. adımı
> (*"Başvuru kaydedilir"*) yazılmamıştı; `Partners` satırları yalnız
> testlerde açılıyordu ve üretimde sisteme işletme girmenin yolu yoktu.
> `A-35`'teki "daveti tüketen uç var, üreteni yok" durumunun aynısı.
>
> Tek istekte beş kayıt açılıyor ve HEPSİ TEK İŞLEMDE:
> kullanıcı → işletme → sahip rolü → rol yetkileri → sahip üyeliği.
> </summary>

**satır 27**

> <summary>
> YÜRÜRLÜKTEKİ onay metinlerinin sürümleri (`A-59`).
>
> ⚠️ Eskiden bu bir SABİTTİ. Metin değişip sabit güncellenmezse yeni
> metni onaylayan kullanıcı ESKİ sürümle kaydedilirdi ve bunu hiçbir
> şey söylemezdi — KVKK ispatı sessizce değersizleşirdi.
>
> ⚠️ Yine de İSTEMCİDEN alınmıyor: istemci belirleseydi kullanıcının
> hangi metni onayladığını istemci söylerdi ve ispat yine değersiz
> olurdu. Kaynak veritabanı.
>
> Metin bulunamazsa başvuru REDDEDİLİYOR: sürümsüz bir onay kaydı,
> anlaşmazlıkta hiçbir şey kanıtlamaz.
> </summary>

**satır 81**

> ⚠️ IBAN ZORUNLU (Mert, 2026-08-26). Boş bırakılabilseydi, alıcı
> kaydı açılamayan işletmeler sessizce birikir ve bunu ancak ilk
> hakediş ödenmediğinde fark ederdik → `A-41`

**satır 106**

> ⚠️ YENİDEN BAŞVURU ÖNCE KONTROL EDİLİYOR (`A-55`, Mert 2026-08-26).
>
> Reddedilmiş bir işletme aynı vergi numarasıyla tekrar başvurabiliyor
> ve kayıt `ApplicationReceived`'a dönüyor. Bu yol e-posta ve vergi
> numarası kontrollerinden ÖNCE gelmek zorunda: ikisi de zaten
> kayıtlı, sıradan akış onu "çakışma" sayıp reddederdi.

**satır 116**

> ⚠️ PAROLA TEYİDİ ŞART. E-posta eşleşmesi tek başına yetmez:
> vergi numarası yarı-kamusal, e-posta da tahmin edilebilir.
> Parola olmadan, ikisini bilen biri reddedilmiş bir kaydı
> yeniden açtırıp platformun onay kuyruğuna sokabilirdi.

**satır 123**

> ⚠️ AYNI MESAJ. "Parola yanlış" denseydi bu uç, hangi vergi
> numarasının reddedilmiş bir kayda ait olduğunu ele veren
> bir sorgulama aracına dönerdi.

**satır 208**

> ⚠️ SAHİP ROLÜ İŞLETMEYE ÖZEL OLMAK ZORUNDA.
> `trg_partner_member_role_scope` üyeliğin rolünün aynı işletmeye
> ait olmasını şart koşuyor; `PartnerId` boş genel bir
> `partner.owner` rolü hiçbir üyeliğe bağlanamaz.

**satır 273**

> ⚠️ IBAN, vergi numarası ve telefon PAYLOAD'A YAZILMIYOR.
> `EventLogs` temizlenemiyor; oraya düşen bir IBAN kaydı okuyabilen
> herkes için kalıcı olurdu.

**satır 295**

> <summary>
> REDDEDİLMİŞ KAYDI YENİDEN AÇAR (`A-55`).
>
> Yeni kullanıcı, yeni işletme, yeni rol AÇILMIYOR — hepsi zaten var.
> Kayıt güncelleniyor ve `ApplicationReceived`'a dönüyor.
>
> ⚠️ `RejectionReason` TEMİZLENİYOR. Kalsaydı, incelemeyi bekleyen bir
> başvuruda panelde eski red sebebi görünmeye devam ederdi — askı
> sebebinin `ReinstateAsync`'te temizlenmesiyle aynı gerekçe.
>
> ⚠️ RED SEBEBİ YİNE DE KAYBOLMUYOR: `platform.data.accessed` olayı
> reddi kaydetti ve `EventLogs` append-only, silinemiyor. Yani "bu
> işletme daha önce neden reddedilmişti" sorusunun cevabı duruyor,
> yalnız işletmenin göreceği yerde durmuyor.
> </summary>

**satır 334**

> ⚠️ ONAY KAYITLARI YENİDEN YAZILIYOR. Yeni bir başvuru, yeni bir
> onay demek: eski kayıtlar önceki başvuruya ait ve o başvuru
> reddedildi. Eskisine yaslanmak, kullanıcının bugün onayladığını
> ispatlamazdı.


## `src/DailyCruising.Application/Partners/PartnerDocumentService.cs`

**satır 6**

> <summary>
> İŞLETME EVRAKI YÜKLEME (`A-60`).
>
> ⚠️ Dosya İÇERİĞİ veritabanına girmiyor; `FileKey` giriyor. Binary'yi
> tabloya koymak yedek boyutunu ve geri yükleme süresini çöpe atardı.
> </summary>

**satır 21**

> <summary>
> ⚠️ İZİN LİSTESİ, yasak listesi DEĞİL. Yasak listesi her zaman eksik
> kalır; izin listesi tanımadığını reddeder. `.svg` bilerek YOK —
> içine betik gömülebiliyor ve tarayıcıda çalışabiliyor.
> </summary>

**satır 59**

> ⚠️ İÇERİK BELLEĞE ALINIYOR — imza doğrulaması için başa sarılabilir
> bir akış gerekiyor ve `IFormFile` akışı her zaman sarılabilir
> değil. Boyut sınırı YUKARIDA uygulandığı için bu güvenli; sınır
> olmasaydı tek bir istek sunucuyu düşürebilirdi.

**satır 67**

> ⚠️ İZİN LİSTESİ TEK BAŞINA YETMİYOR (`A-62`). Liste "hangi türü
> kabul ediyoruz"u söylüyor, "gelen şey gerçekten o mu"yu değil.
> `Content-Type` istemcinin yazdığı bir metin: `.pdf` diye
> gönderilen bir dosya bir betik ya da HTML olabilir.

**satır 90**

> <summary>
> EVRAĞI İNDİRİR (`A-62`).
>
> ⚠️ `FileKey` DIŞARIYA HİÇ VERİLMİYOR; indirme bu uçtan geçiyor.
> Anahtar verilseydi depolama adresine doğrudan erişim denemesine
> davetiye olurdu ve kova ayarı yanlışsa evraklar herkese açılırdı.
> İki katman: anahtar gizli VE kova genel okumaya kapalı.
>
> ⚠️ Kapsam filtresi ŞART: `documentId` tahmin edilebilir olmasa da
> yalnız kimliğe güvenmek, sızan tek bir kimliğin başka bir işletmenin
> evrakını açması demekti.
> </summary>

**satır 114**

> <summary>
> PLATFORM PERSONELİ için — kapsam filtresi YOK, çünkü inceleme tam da
> başkasının evrakına bakmak demek.
>
> ⚠️ Muafiyetin bedeli çağıranda ödeniyor: `PlatformController`
> `platform.data.accessed` yazıyor. `A-38`'de kurulan kural — başka
> birinin verisine bakmak olağan değildir ve iz bırakmalı.
> </summary>

**satır 143**

> ⚠️ Tür UZANTIDAN türüyor: `PartnerDocuments`'ta içerik türü
> kolonu yok ve anahtar yüklerken izin listesinden gelen uzantıyla
> kuruluyor — yani uzantı güvenilir, kullanıcının yazdığı bir şey
> değil.

**satır 165**

> <summary>
> İndirilen evrak. ⚠️ `FileKey` YOK — depolama adresi dışarı çıkmıyor.
> </summary>


## `src/DailyCruising.Application/Partners/PartnerStaffContracts.cs`

**satır 68**

> <summary>
> İşletme yönetimi kuralının ihlali.
>
> ⚠️ İKİ AYRI METİN TAŞIR ve karıştırılmamalıdır:
>
>   <see cref="Exception.Message"/> — ÇAĞIRANA gider. İşletme sahibinin kendi
>     gönderdiği veriyi içerebilir; ona kendi yazdığını geri söylemek sızıntı
>     değil, kullanılabilirliktir.
>
>   <see cref="LogReason"/> — `EventLogs`'a gider ve SABİTTİR. O tablo
>     append-only ve TEMİZLENEMEZ; oraya giren serbest metin kalıcıdır.
>
> Ayrım bir denetim bulgusundan doğdu (2026-08-25): `Message` doğrudan olay
> günlüğüne yazılıyordu ve içinde çağıranın yazdığı ham yetki anahtarları
> vardı. `role.manage` yetkisi olan biri `permissions` dizisine ne yazarsa
> `EventLogs`'a kalıcı olarak düşüyordu. Kodun kendi yorumu bunun imkânsız
> olduğunu iddia ediyordu → [[api-kararlar]]
> </summary>


## `src/DailyCruising.Application/Partners/PartnerStaffService.cs`

**satır 112**

> Anahtar İŞLETME KİMLİĞİNİ İÇERİYOR: iki işletme aynı adı verse de
> `Roles.Key` çakışmıyor. Kullanıcıya gösterilen ad `Name`.
>
> ⚠️ BURADA `[..64]` KESMESİ VARDI, KALDIRILDI. Tam uzunluk 73
> karakter ve kolon `HasMaxLength(100)` — kesmeye hiç gerek yoktu.
> Bedeli görünmezdi: `Guid.CreateVersion7()` ZAMAN SIRALI, ilk 12
> onaltılık karakteri milisaniye damgası. 64'e kesmek kuyruktaki
> rastgele 32 karakterin 9'unu atıyordu ve geriye kalan gerçek
> rastgelelik ~38 bite iniyordu — aynı milisaniyede aynı işletme
> için iki rol yaratıldığında çakışma ihtimali "128 bit, imkânsız"
> sezgisinden çok daha erken geliyordu. Denetim (2026-08-25).

**satır 179**

> ⚠️ ROLÜN YETKİLERİ DEĞİŞTİ → o role bağlı HERKESİN jetonu
> geçersizleşmeli (`A-44`). Tek kullanıcı değil: bir rolden yetki
> kısıldığında o rolü taşıyan bütün çalışanlar etkileniyor ve
> yalnız birinin jetonu tazelenirse diğerleri 15 dakika daha eski
> yetkilerle çalışırdı.

**satır 201**

> ⚠️ AKTİF sayısına DEĞİL, herhangi bir üyelik satırına bakılıyor.
>
> Çıkarılmış çalışanın satırı duruyor ve `RoleId`'si hâlâ bu rolü
> gösteriyor; `PartnerMembers.RoleId` üzerindeki RESTRICT yabancı
> anahtarı silmeyi zaten reddeder. Burası önce yalnız aktifleri
> sayıyordu ve "çalışanı çıkar, sonra rolü sil" akışı veritabanı
> hatasıyla patlıyordu — testi yazınca çıktı.

**satır 265**

> ⚠️ İKİ AYRI RET, TEK MESAJ — bilerek.
>
> "Böyle bir kullanıcı yok" ile "başka bir işletmede çalışıyor"
> ayrı ayrı söylenseydi, `staff.manage` verilmiş HERHANGİ bir çalışan
> rastgele e-posta deneyerek platformdaki kimin kayıtlı olduğunu ve
> kimin bir işletmede çalıştığını öğrenirdi. Yetki işletme sahibinin
> güvendiği kişiye verilmiş olabilir ama platformun tamamına değil.
> Denetim bulgusu (2026-08-25).
>
> Mesaj yine EYLEME DÖNÜK: iki şartı da söylüyor, hangisinin
> tutmadığını söylemiyor.

**satır 287**

> ⚠️ `PartnerMembers.UserId` BENZERSİZ ve benzersizlik `Status`'tan
> BAĞIMSIZ: çıkarılmış çalışanın satırı duruyor. Yeni satır eklemek
> veritabanı hatası verirdi; mevcut satır güncelleniyor.

**satır 381**

> ⚠️ ERİŞİM ARTIK ANINDA KESİLİYOR (`A-44`, 2026-08-26).
>
> Buradaki yorum eskiden şunu söylüyordu: *"anında kesmek her istekte
> veritabanına gitmeyi gerektirir; bu ölçekte ödenmeyecek bir bedel"*
> ve çıkarılan çalışan 15 dakika daha çalışabiliyordu.
>
> O denge `A-43`'te DEĞİŞTİ: işletme aktiflik kapısı eklenirken
> istek başına okuma zaten başlamıştı. Damga o okumaya bir kolon
> ekliyor, yeni bir gidiş-dönüş getirmiyor — yani gerekçe artık
> geçerli değil.

**satır 394**

> <summary>
> SAHİPLİĞİ DEVREDER (`A-03`).
>
> ⚠️ YALNIZ MEVCUT SAHİP devredebilir — `staff.manage` yetkisi YETMEZ.
> Yetmeseydi, sahibin çalışanına verdiği personel yönetimi yetkisi
> işletmeyi devralmaya dönüşürdü.
>
> ⚠️ GERİ ALINAMAZ: devirden sonra eski sahip artık sahip değil ve geri
> alması yalnız YENİ sahibin rızasıyla mümkün. Bu yüzden parola teyidi
> isteniyor — çalıntı bir erişim jetonuyla işletme devralınabilirdi.
> </summary>

**satır 445**

> ⚠️ İKİ KULLANICI BİRDEN (`A-44`). Devir iki tarafın da yetkisini
> değiştiriyor: eski sahip sahip rolünü bırakıyor, yenisi alıyor.
> Yalnız birinin damgası yükseltilseydi, eski sahip 15 dakika
> boyunca personel yönetmeye devam ederdi — bu görevi doğuran
> ölçüm tam olarak buydu (soru 1).

**satır 516**

> ⚠️ `eksik` ÇAĞIRANIN GÖNDERDİĞİ ham metni içeriyor. Mesaj çağırana
> gidiyor — kendi yazdığını geri görmesi sızıntı değil. Ama olay
> günlüğüne SABİT sebep gidiyor: `EventLogs` temizlenemiyor ve
> oraya yazılan serbest metin kalıcı olurdu.


## `src/DailyCruising.Application/Payments/IPaymentProvider.cs`

**satır 5**

> <summary>
> Sanal POS sağlayıcısı (`G-03`: İyzico, Mert 2026-08-25 — *"sonrasında
> değiştirebilirim; Paratika, Param, PayTR"*).
>
> ⚠️ ARAYÜZ SAĞLAYICININ API ŞEKLİNE GÖRE DEĞİL, BİZİM DOMAIN
> KAVRAMLARIMIZA GÖRE yazıldı. İyzico'nun "alt üye iş yeri" modeliyle
> PayTR ve Paratika'nın pazaryeri semantiği AYNI DEĞİL; arayüz birinin
> şekline göre yazılsaydı ikincisinde kırılırdı.
>
> Burada geçen tek para kavramı: müşterinin ödeyeceği tutar ve
> rezervasyon. Bölüştürme, komisyon ve hakediş bizim defterimizin işi
> (`LedgerService`), sağlayıcının değil.
> </summary>

**satır 29**

> <summary>
> Sağlayıcının geri dönüşünü doğrular. ⚠️ Sonucu İSTEMCİDEN DEĞİL
> sağlayıcıdan teyit etmek zorunda: istemci "ödendi" diyebilir.
>
> ⚠️ `expectedAmountTry` TUTAR TEYİDİ İÇİN. "Ödendi mi" sorusunun
> cevabı tek başına yetmiyor: NE KADAR ödendiği de sağlayıcıdan
> doğrulanmalı. Beklenenden düşük bir tahsilat `Succeeded` sayılsaydı,
> rezervasyon `Paid` olur ve defter tahsil edilmemiş parayı gerçek
> gösterirdi — `A-18`'in tam olarak engellemeye çalıştığı şey.
> </summary>

**satır 45**

> <summary>
> İŞLETMEYİ SAĞLAYICIDA ALICI OLARAK KAYDEDER (`A-41`).
>
> ⚠️ Adlandırma yine sağlayıcıdan BAĞIMSIZ: İyzico buna "alt üye iş
> yeri" (submerchant) diyor, PayTR başka bir şey. Bizim domain
> kavramımız "paranın bir kısmının gideceği alıcı".
>
> Dönen anahtar `PartnerPayeeAccounts.ExternalKey`'e yazılıyor ve
> ödeme başlatırken `PaymentStartRequest.PayeeKey` olarak geri
> gönderiliyor.
> </summary>

**satır 60**

> <summary>
> Alıcı kaydı için sağlayıcıya verilecek bilgiler (`A-41`).
>
> ⚠️ `TaxNumber`'ın ANLAMI `BusinessType`'a bağlı: şahısta TC kimlik,
> diğerlerinde vergi numarası. Sağlayıcılar bunları AYRI alanlarda
> istiyor; ayrımı burada taşımak, her sağlayıcının kendi eşlemesini
> yapabilmesi demek.
> </summary>

**satır 93**

> <summary>
> Paranın bir kısmının gideceği ALICI — sağlayıcı tarafındaki kimliği
> (`A-41`). İyzico'da `subMerchantKey`, başka sağlayıcıda başka bir şey.
>
> ⚠️ Alan adı BİLEREK sağlayıcıdan bağımsız. `SubMerchantKey` denseydi
> arayüz İyzico'nun şekline göre yazılmış olurdu ve PayTR'ye geçişte
> kırılırdı — bu arayüzün ilk satırındaki uyarının tam olarak sebebi.
>
> `null` ise bölüştürme YOK: tahsilat tamamen platform hesabına yapılır
> ve hakediş yalnız defterde durur.
> </summary>

**satır 106**

> <summary>
> Alıcıya gidecek tutar. `AmountTry` eksi bu = platformda kalan.
>
> ⚠️ Bu sayı defterdeki hakedişle AYNI kaynaktan geliyor
> (`EarningCalculator`). İkisi ayrı hesaplansaydı, sağlayıcıya söylenen
> tutar ile defterin yazdığı tutar bir gün ayrışır ve mutabakat
> tutmazdı.
> </summary>

**satır 127**

> <summary>
> `Payments.Provider` kolonuna bakıp DOĞRU sağlayıcıyı seçer.
>
> ⚠️ TEK GLOBAL ÖRNEK YETMEZ. Sağlayıcı değiştirildiğinde eski ödemeler eski
> sağlayıcıda kalır: PayTR'ye geçtikten altı ay sonra bir İyzico ödemesinin
> iadesi İYZİCO'DAN geçmek zorunda. Tek örnekle o iade sessizce yanlış
> sağlayıcıya gider ve başarısız olur → [[api-benim-kararlarim]]
> </summary>


## `src/DailyCruising.Application/Payments/PaymentService.cs`

**satır 8**

> <summary>
> ÖDEME AKIŞI (`A-29`).
>
> İki adım: `StartAsync` 3D Secure'a yönlendiriyor, `CompleteAsync`
> sağlayıcının dönüşünü DOĞRULUYOR.
>
> ⚠️ SONUÇ İSTEMCİDEN ALINMIYOR. Geri dönüş adresine "başarılı" yazan bir
> istemci ödemeyi tamamlamış saymıyor; sonuç sağlayıcıdan teyit ediliyor.
> Aksi halde herkes ödemeden rezervasyon onaylatırdı.
> </summary>

**satır 45**

> BÖLÜŞTÜRME (`A-41`). İşletmenin bu sağlayıcıdaki alıcı kaydı varsa
> paranın hakediş kısmı doğrudan ona yönlendiriliyor.
>
> ⚠️ Alıcı kaydı SAĞLAYICI ADIYLA aranıyor. İyzico'da açılmış bir
> alıcı kaydı PayTR'de hiçbir şey ifade etmiyor; sağlayıcıya
> bakılmadan bulunan bir anahtar, parayı var olmayan bir hesaba
> göndermeye çalışırdı.

**satır 55**

> ⚠️ Alıcı kaydı YOKSA bölüştürme yapılmıyor ve ödeme yine de
> alınıyor. Reddetmek, alıcı kaydı henüz açılmamış her işletmenin
> satışını durdururdu. Bedeli: para platformda kalıyor, hakediş
> yalnız defterde duruyor ve işletmeye transfer ELLE yapılmak
> zorunda. Bu boşluk `Payments.RawResponse` içinde görülebiliyor —
> `payeeKey` boşsa bölüştürme olmamış demektir.

**satır 66**

> ⚠️ TUTAR REZERVASYONDAN. İstemciden tutar alan hiçbir yol yok —
> aynı ilke fiyat ve rezervasyon uçlarında da geçerli.

**satır 91**

> <summary>
> Sağlayıcının dönüşü. Başarılıysa rezervasyon `Paid` oluyor ve DEFTER
> KAYITLARI yazılıyor.
>
> ⚠️ MÜKERRER ÇAĞRIYA KARŞI KORUMALI. Sağlayıcı aynı bildirimi iki kez
> gönderebilir; ikinci çağrı defteri iki katına çıkarmıyor
> (`LedgerService.PostPaymentAsync` de ayrıca koruyor — iki katman).
> </summary>

**satır 109**

> ⚠️ Sağlayıcı, ödemenin KENDİ kaydındaki isimle çözülüyor — global
> yapılandırmayla değil. Sağlayıcı değiştirildikten sonra eski bir
> ödemenin teyidi hâlâ eski sağlayıcıdan geçiyor.


## `src/DailyCruising.Application/Payments/RefundService.cs`

**satır 8**

> <summary>
> SAĞLAYICIYA İADE TALİMATI (`A-29`).
>
> İptal ile iade AYRI iki iş ve bu bilerek. `ReservationService.CancelAsync`
> iade oranını hesaplayıp DONDURUYOR ama parayı oynatmıyor; para hareketi
> buradan geçiyor.
>
> ⚠️ İPTALİN İÇİNE GÖMÜLMEDİ. Gömülseydi sağlayıcıya giden HTTP çağrısı
> müşterinin iptal isteğini bekletirdi: çağrı zaman aşımına uğradığında
> müşteri "iptal başarısız" görürdü, oysa rezervasyon iptal edilmiş olurdu —
> aynı tuzağın bildirim tarafındaki hâli `A-28` olarak panoda duruyor.
> Ayrılınca iade tekrar denenebilir bir iş oluyor.
> </summary>

**satır 82**

> ⚠️ NİYET, ETKİDEN ÖNCE YAZILIYOR. Önce sağlayıcı çağrılıp sonra
> kayıt atılsaydı, arada düşen bir süreç PARASI GİTMİŞ ama kaydı
> olmayan bir iade bırakırdı. Tersi güvenli: kaydı olup gönderilmemiş
> iade görülebilir ve tekrar denenebilir.
>
> Aynı satır ikinci kez eklenemiyor: `UX_Refunds_ReservationId_Aktif`
> kısmi benzersiz indeksi eşzamanlı iki talebi veritabanında kesiyor.
> Servis seviyesindeki durum kontrolü yarışta yetmez — iki istek de
> `Cancelled` görür ve İKİ KEZ para gönderilirdi.

**satır 99**

> ⚠️ `Sent` AYRI BİR ADIM ve ayrı commit. Süreç tam bu noktada
> düşerse kayıt `Sent`'te kalır: "gönderilmiş olabilir, sağlayıcıdan
> teyit et" demektir. `Requested`'ta kalsaydı KESİNLİKLE
> gönderilmemiş olurdu. İkisini ayırmayan bir tasarım, operatörü
> parayı ikinci kez göndermek ile müşteriyi bekletmek arasında
> kanıtsız seçim yapmaya zorlardı.


## `src/DailyCruising.Application/Platform/PlatformContracts.cs`

**satır 21**

> <summary>
> İşletmeye sözleşme gönderme.
>
> ⚠️ KOMİSYON ORANI BURADA BELİRLENİYOR ve sonradan değiştirilemiyor:
> *"Oranı değiştirmek yeni sözleşme (ve yeni onay) demektir"*
> ([[domain-gereksinimler]] 2026-08-22). Bu yüzden "komisyon düzenleme" diye
> ayrı bir uç YOK — yeni sözleşme göndermek O İŞİN KENDİSİ.
> </summary>

**satır 36**

> <summary>
> İŞLETME BAŞVURUSUNU REDDETME (`A-55`).
>
> ⚠️ Sebep ZORUNLU ve bu bir tercih değil: `CK_Partners_RejectionReason`
> `Rejected` durumundaki bir kaydın sebepsiz olmasını veritabanı
> seviyesinde reddediyor. Uygulama katmanı bunu önce ve anlaşılır bir
> mesajla yakalıyor.
> </summary>

**satır 54**

> <summary>
> GELECEK TURLARI DA İPTAL ET (`A-54`, Mert soru 15).
>
> ⚠️ VARSAYILAN `false` ve bu bilerek. Askıya alma çoğu zaman geri
> alınabilir bir tedbir (eksik belge gibi); tek tık ödemiş
> müşterilerin turunu iptal etmemeli. Dolandırıcılık şüphesi gibi
> ciddi durumlarda platform bunu AÇIKÇA seçiyor.
>
> ⚠️ İptal edilen turlar **%100 iade** alıyor — kademeli iade
> müşterinin kendi vazgeçmesi için; burada müşterinin hiçbir kusuru
> yok.
> </summary>


## `src/DailyCruising.Application/Platform/PlatformService.cs`

**satır 8**

> <summary>
> PLATFORM YÖNETİMİ (`A-38`).
>
> ⚠️ **KAPSAM FİLTRESİNDEN MUAF TEK SERVİS.** Platform personeli tüm
> işletmelerin verisini görüyor (Mert, 2026-08-24) — karşılığında HER erişim
> olay günlüğüne yazılıyor. Muafiyet bedava değil; bedeli burada ödeniyor ve
> ödenmediği an muafiyet meşruiyetini kaybeder.
>
> ⚠️ `IsPlatformStaff` kontrolü HER metotta. `[HasPermission]` tek başına
> yetmez: bir yetki yanlışlıkla işletme rolüne verilirse
> (`IsPartnerAssignable` bunu engelliyor ama katalog değişebilir) ikinci
> duvar tutar.
> </summary>

**satır 62**

> <summary>
> SÖZLEŞME GÖNDERİR — komisyon oranı burada belirleniyor.
>
> ⚠️ "Komisyon düzenleme" diye AYRI BİR UÇ YOK ve olmamalı:
> *"Oranı değiştirmek yeni sözleşme (ve yeni onay) demektir"*
> ([[domain-gereksinimler]] 2026-08-22). Oranı doğrudan güncelleyen bir
> uç, işletmenin onaylamadığı bir orana tabi olmasına yol açardı.
> </summary>

**satır 117**

> ⚠️ GÖVDE KOPYALANIYOR, referans verilmiyor. Şablon
> sonradan değişse işletmenin fiilen neyi onayladığı
> kaybolmamalı ([[domain-gereksinimler]] 2026-08-22).

**satır 150**

> <summary>
> İşletmeyi ASKIYA ALIR.
>
> ⚠️ MEVCUT REZERVASYONLAR İPTAL EDİLMİYOR. Askıya almak satışı durdurur;
> satılmış turlar yapılır. Tersi olsaydı bir tık, ödemiş müşterilerin
> turlarını iptal ederdi — ve askıya alma çoğu zaman geri alınabilir bir
> tedbirdir -> [[api-benim-kararlarim]]
> </summary>

**satır 178**

> Sebep `Partners`'a yazılıyor, yalnız günlüğe değil: işletme
> panelinde "neden askıdayım" sorusunun cevabı görünmeli.
>
> ⚠️ `SuspensionReason`, `RejectionReason` DEĞİL. İlkinde yazıyordum;
> kolon adı içeriğiyle uyuşmuyordu ve `CK_Partners_RejectionReason`
> o kolonu `Rejected` durumuna bağlıyor.

**satır 189**

> ⚠️ TURLARI İPTAL ETMEK AYRI VE AÇIK BİR SEÇİM (`A-54`, Mert soru 15).
>
> Varsayılan iptal ETMEMEK: askıya alma çoğu zaman geri alınabilir bir
> tedbir (eksik belge gibi) ve tek tık ödemiş müşterilerin turunu
> iptal etmemeli. Dolandırıcılık şüphesinde platform bunu açıkça
> seçiyor.
>
> ⚠️ İADE OTOMATİK GİDİYOR: iptal edilen rezervasyonlar
> `RefundDueTry > 0` ile kalıyor ve `ProcessRefundsJob` (`A-56`)
> onları topluyor. Bu bağ olmasaydı müşterinin turu iptal olur,
> parası iade edilmezdi — `A-54` bu bağ kurulmadan kapanamazdı.

**satır 206**

> <summary>
> BAŞVURUYU REDDEDER (`A-55`).
>
> ⚠️ Bu uç 2026-08-26'ya kadar YOKTU. `PartnerStatus.Rejected` enum'da
> vardı, `CK_Partners_RejectionReason` onu zorluyordu — ama platform
> bir başvuruyu inceleyebiliyor, sözleşme gönderebiliyor, askıya
> alabiliyor, **reddedemiyordu**. `A-42` başvuru ucunu yazınca eksiklik
> canlıya döndü: gelen başvuruların gidecek bir "hayır" yolu yoktu.
>
> ⚠️ RET GERİ ALINAMAZ DEĞİL. Mert (2026-08-26): reddedilen işletme
> aynı vergi numarasıyla YENİDEN başvurabiliyor ve kayıt
> `ApplicationReceived`'a dönüyor → `PartnerApplicationService`.
>
> ⚠️ `Active` bir işletme REDDEDİLEMEZ. Aktif bir işletmeyi durdurmanın
> yolu askıya almaktır (`SuspendAsync`) — ret, başvuru aşamasına ait
> bir karar. Ayrılmasaydı "reddedilmiş" bir işletmenin satılmış turları
> olurdu ve `RejectionReason` başvuruyla ilgisiz bir metin taşırdı.
> </summary>

**satır 261**

> <summary>
> İŞLETMEYİ ÖDEME SAĞLAYICISINDA ALICI OLARAK KAYDEDER (`A-41`).
>
> ⚠️ Bu uç bugün YALNIZ sahte sağlayıcıyla çalışıyor: İyzico hesabında
> pazaryeri özelliği kapalı ve gerçek sağlayıcı açıkça hata veriyor.
> Uç yine de var, çünkü akışın geri kalanı (bölüştürme, hakediş) bu
> kaydı bekliyor ve özellik açıldığında değişecek TEK şey
> `IyzicoPaymentProvider.RegisterPayeeAsync` gövdesi olacak.
>
> ⚠️ IBAN ve iş yeri türü ZORUNLU: ikisi de `A-42` başvurusunda
> toplanıyor ama bu alandan önce kaydolmuş işletmelerde boş olabilir.
> Boşken sağlayıcıya gitmek, eksik veriyle kayıt açtırmak olurdu.
> </summary>

**satır 332**

> <summary>
> YORUM MODERASYONU — `A-35`'in eksik yarısı.
>
> ⚠️ `ModeratedByUserId` YAZILMAK ZORUNDA: `CK_Reviews_Moderated`
> onaylanan bir yorumun KİMİN onayladığını da istiyor. Sözleşme
> onayındaki desenin aynısı — karar bir kişiye bağlanabilmeli.
> </summary>

**satır 360**

> ⚠️ `trg_review_sync_boat_rating` bu kaydetmede çalışıyor ve
> `Boats.AverageRating` ile `ReviewCount`'u yeniden hesaplıyor.
> Ortalama uygulama tarafında HESAPLANMIYOR — tetikleyici tek kaynak.

**satır 368**

> <summary>
> ⚠️ İZİNLİ ÖNCEKİ DURUMLAR AÇIKÇA VERİLİYOR. "Ne olursa olsun yeni
> duruma geç" deseydi, reddedilmiş bir işletme incelemeye geri alınabilir
> ya da askıdaki bir işletme sessizce aktifleşebilirdi.
> </summary>


## `src/DailyCruising.Application/Pricing/PricingContracts.cs`

**satır 11**

> <summary>
> Fiyat sorgusu. ⚠️ İçinde TUTAR ALANI YOK ve olmayacak.
>
> İstemciden tutar almak, sonra onu "doğrulamak" güvenlik değil: doğrulama
> atlanabilir, unutulabilir, yanlış yazılabilir. Alan hiç olmazsa atlanacak
> bir şey de olmaz.
> </summary>

**satır 37**

> <summary>
> Sunucunun hesapladığı fiyat. Kayıt, rezervasyona dondurulacak alanların
> tamamını taşıyacak şekilde tasarlandı: amaç, hesap ile saklanan arasında
> ikinci bir dönüşüm bulunmaması.
>
> ⚠️ Bu bir NİYET, henüz bir güvence değil. Rezervasyon oluşturma ucu
> yazıldığında alanları tek tek kopyalarsa ikisi yine ayrışabilir. Güvence,
> ancak dönüşümü tek bir yere kilitleyen bir üretici metotla kurulur —
> o uç yazılırken yapılacak.
> </summary>

**satır 110**

> <summary>
> İndirimin, karşılayan tarafın payını aşan ve platformun üstlendiği
> kısmı. Normalde sıfır — gerekçe → `Reservation.PlatformAbsorbedTry`.
>
> ⚠️ MÜŞTERİYE DÖNEN YANITTA YOK. `QuoteResponse` bunu taşımıyor:
> değeri komisyon oranından türüyor ve dışarı verilirse `S-10`'da
> kapatılan sızıntı geri gelir.
> </summary>

**satır 161**

> ⚠️ `ExceedsCommission` 2026-08-25'te KALDIRILDI (Mert / S-10): kupon
> artık komisyon oranını aşabiliyor. Değer geçmiş `EventLogs` satırlarında
> metin olarak DURUYOR; o kayıtları okuyan biri karşılığını burada
> bulamazsa şaşırmasın diye yazılı bırakıldı → [[api-kararlar]]


## `src/DailyCruising.Application/Pricing/PricingService.cs`

**satır 46**

> <summary>
> Kupon ret sebebinin müşteriye söylenmesi. 2026-08-24 sabahı güvenlik
> denetimi üzerine tek metne indirilmişti; AYNI GÜN Mert geri istedi:
> *"kupon reddedilince müşteri sebebini görsün"*. Bu satırlar o kararı
> uygular ve sabahkini iptal eder.
>
> Bedeli biliniyor ve kabul edildi. Sızıntı mesajın METNİNDE değil,
> cevapların birbirinden AYIRT EDİLEBİLMESİNDE: kimliksiz bir çağıran
> "bu işletmede geçerli değil" cevabından kodun gerçek olduğunu anlar.
>
> ⚠️ Bu listede eskiden bir de `ExceedsCommission` dalı vardı ve ASIL
> SIZINTI oydu: oranı bilinen bir kuponla deneyerek işletmenin komisyon
> oranına eşik konabiliyordu. 2026-08-25'te Mert kuralın kendisini
> kaldırdı (S-10), dal da onunla birlikte gitti → [[api-kararlar]]
>
> Pratikteki sınır: kupon üretmek işletmeye ya da platforma ait. Saldırgan
> yalnız VAR OLAN kuponları deneyebilir, istediği oranda kupon üretip
> ikili arama yapamaz.
> </summary>

**satır 195**

> ⚠️ `MinPassengers` burada BİLEREK kontrol edilmiyor. O sınır SEFERE
> kopyalanıyor, rezervasyona değil: paylaşımlı seferde asgari 8 kişilik
> bir tura 2 kişilik rezervasyon meşrudur, sefer dolmazsa iptal edilir.
> Burada kontrol edilseydi geçerli bir satış reddedilirdi.

**satır 359**

> <summary>
> Kupon uygulanıyor ya da reddediliyor. Ret sebebi AYRIŞTIRILIYOR;
> gerekçesi ve bedeli <see cref="KuponRetMesaji"/> üstünde.
>
> ⚠️ "İndirim oranı komisyon oranını AŞAMAZ" kuralı 2026-08-25'te
> KALDIRILDI (Mert / S-10). Kural bir sızıntı üretiyordu: aynı kuponun bir
> teknede geçip diğerinde geçmemesi, kimliksiz çağırana iki işletmenin
> komisyon oranını sıralatıyordu. Kupon artık her teknede aynı davranıyor.
>
> Bedeli: platformun zarar etmesini engelleyen şey artık bir kural değil,
> indirimi KİMİN üstlendiği. Kuponu oluşturan taraf karşılıyor
> (S-14) ve bu <see cref="CouponFunder"/> olarak rezervasyona donuyor.
>
> MATRAH KARARI: indirim tur + ek hizmet toplamına uygulanıyor. Gerekçe:
> komisyon matrahı da tur + menü + ek hizmet — iki oran aynı tabana
> uygulanmalı ki hakediş hesabı tek bir matrah üzerinden yürüsün.
> Mert'e soruldu.
> </summary>


## `src/DailyCruising.Application/Privacy/AnonymizationService.cs`

**satır 7**

> <summary>
> KVKK "hesabımı sil" akışı (`A-12`).
>
> ⚠️ SİLME DEĞİL ANONİMLEŞTİRME. Hesabın tamamen silinmesi imkânsız:
> rezervasyonu ya da mesajı olan kullanıcıyı `Restrict` zinciri tutuyor ve
> tutmalı da — rezervasyon bir muhasebe kaydı, mesaj bir anlaşmazlık kaydı.
>
> ⚠️ İKİ TABLO TEMİZLENEMİYOR ve bu geri alınamaz:
>   `EventLogs.Payload` — append-only, TRUNCATE yetkisi uygulama rolünde yok
>   `LedgerEntries.Note` — değişmez, düzeltme güncelleme değil ters kayıt
> Oralara giren kişisel veri KALICI. Bugün oraya bilerek konan tek şey
> başarısız girişteki e-posta adresi (Mert, 2026-08-24 / S-5) ve rezervasyon
> kodu. İkisi de bu akışın erişemediği yerde duruyor.
> </summary>

**satır 48**

> ⚠️ YAKLAŞAN TUR VARKEN ANONİMLEŞTİRİLMİYOR.
>
> İsim silinirse iskelede mürettebat karşısındaki kişiyi listeyle
> eşleştiremez ve ÖDEMİŞ müşteri tekneye alınamaz. "Eksik yolcu bilgisi
> binişi engellemez" kuralıyla aynı aile.
>
> Engel değil ERTELEME: müşteri turdan sonra ya da rezervasyonu iptal
> ederek talebini yineleyebiliyor.

**satır 67**

> ⚠️ Bu kayıt TALEBİN YERİNE GETİRİLDİĞİNİN kanıtı ve `EventLogs`
> temizlenemediği için kalıcı — burada kalıcılık İSTENEN şey.
> Kişisel veri YOK: yalnız kullanıcı kimliği ve sayılar.


## `src/DailyCruising.Application/Privacy/IAnonymizationRepository.cs`

**satır 5**

> <summary>
> KVKK "hesabımı sil" akışı.
>
> ⚠️ HESABIN TAMAMEN SİLİNMESİ İMKÂNSIZ ve bu bilerek. Rezervasyonu ya da
> mesajı olan kullanıcıyı `Restrict` yabancı anahtar zinciri tutuyor — tutmalı
> da: rezervasyon bir muhasebe kaydı, mesaj bir anlaşmazlık kaydı. KVKK da
> "hukuki yükümlülük" gerekçesiyle saklanan veriyi silmeyi zorunlu kılmıyor.
>
> Yapılan şey **anonimleştirme**: kişiyi işaret eden alanlar temizleniyor,
> kaydın kendisi duruyor.
> </summary>

**satır 20**

> <summary>
> Kalkışı GELECEKTE olan canlı rezervasyon sayısı.
>
> ⚠️ Anonimleştirme bunlar varken YAPILMAMALI: iskelede mürettebat
> karşısındaki kişiyi listeyle eşleştiremez ve ödemiş müşteri tekneye
> alınamaz. Kural "eksik yolcu bilgisi binişi engellemez" ile aynı
> aileden — form yüzünden müşteriyi mağdur etmiyoruz.
> </summary>


## `src/DailyCruising.Application/Reservations/IReservationRepository.cs`

**satır 8**

> <summary>
> Çift gönderme koruması: bu anahtarla zaten bir rezervasyon var mı.
>
> ⚠️ Bu kontrol TEK BAŞINA yetmez — iki eşzamanlı istek arasında
> atlanabiliyor. Asıl garanti `IX_Reservations_IdempotencyKey` benzersiz
> indeksi; buradaki arama yalnız normal akışta gereksiz iş yapmamak için.
> </summary>

**satır 17**

> <summary>
> Rezervasyonu TEK İŞLEMDE yazar: seferi bulur ya da açar, satırı kilitler,
> rezervasyonu ve ek hizmetlerini ekler, kupon kullanımını işler.
>
> Neden servis değil de burası: adımların tamamı tek bir veritabanı
> işleminde ve doğru kilit sırasıyla olmak zorunda. Servise bölünseydi
> aralarına başka bir çağrı girebilir, işlem sınırı belirsizleşirdi.
>
> ⚠️ Kapasite, sefer çakışması ve kupon hakkı burada UYGULAMA KODUYLA
> kontrol edilmiyor; kısıtların reddi yakalanıp
> <see cref="ReservationConflictException"/>'a çevriliyor. Gerçek garanti
> veritabanında: `CK_Voyages_SoldSeats`, `EX_Voyages_NoOverlapPerBoat`,
> `trg_coupon_redemption_limit`.
> </summary>


## `src/DailyCruising.Application/Reservations/ReservationContracts.cs`

**satır 3**

> <summary>
> Rezervasyon isteği. ⚠️ İçinde TUTAR ALANI YOK ve olmayacak — fiyat sorgusunun
> cevabı da taşınmıyor.
>
> İstemcinin gördüğü tutarı gönderip sunucuda "doğrulamak" güvenlik değil.
> Fiyat sorgusunun cevabını (`Quote`) gönderip saklamak da değil: o cevap
> istemcinin elinden geçmiş demektir, kapıyı bir adım geriye taşımaktan ibaret
> olur. Bu yüzden istek, fiyat sorgusuyla AYNI girdileri taşıyor ve tutar
> burada SIFIRDAN yeniden hesaplanıyor.
>
> Yolcu bilgisi bilerek İSTENMİYOR. Mert'in tarif ettiği akışta ödeme
> ekranında yalnız ödeyen kişi kendi bilgisini girer; yolcu listesi ödemeden
> sonra e-postaya giden linkten doldurulur -> [[domain-gereksinimler]] 2026-08-22.
> </summary>

**satır 30**

> <summary>
> ÇİFT GÖNDERME KORUMASI — istemcinin ürettiği benzersiz anahtar (UUID
> yeterli). Aynı anahtarla ikinci istek YENİ rezervasyon açmıyor, ilkini
> geri döndürüyor.
>
> ⚠️ ZORUNLU. İsteğe bağlı olsaydı göndermeyi unutan istemci sessizce
> korumasız kalırdı ve bunu ancak bir müşteri iki kod aldığında fark
> ederdik. Zorunlu olması istemcinin unutmasını derleme/çalışma anında
> görünür kılıyor.
>
> Anahtar ÖDEME DENEMESİ başına üretilmeli, oturum ya da kullanıcı başına
> değil: aynı müşteri aynı tura iki ayrı rezervasyon yapabilmeli.
> </summary>

**satır 70**

> <summary>
> QR'ın taşıyacağı düz metin jeton. YALNIZ BURADA, yalnız bir kez dönüyor;
> veritabanında SHA-256 özeti duruyor. Kaybolursa yeniden üretilmez.
> </summary>
>
> ⚠️ ÇİFT GÖNDERİMDE null. Jetonun düz metni yalnız üretildiği anda
> biliniyor; veritabanında yalnız özeti var. Aynı istek anahtarıyla gelen
> ikinci istek ilk rezervasyonu döndürüyor ama onun jetonunu ÜRETEMİYOR —
> üretebilseydi jeton tek kullanımlık olmazdı.

**satır 111**

> <summary>
> Müşteriye dönecek tutar. ⚠️ PARA HAREKETİ YOK — sanal POS entegrasyonu
> (`A-29`) yazılmadı. Bu tutar hesaplanıp saklanıyor; ödeme akışı
> yazıldığında buradan yürüyecek.
> </summary>


## `src/DailyCruising.Application/Reservations/ReservationFactory.cs`

**satır 8**

> <summary>
> `Quote` -> `Reservation` dönüşümünün TEK YERİ.
>
> A-04'te şu yazılmıştı: *"Hesabın çıktısı aynı zamanda rezervasyona
> dondurulacak alanların tamamıdır"* — ama o bir NİYETTİ, güvence değil.
> Alanlar iki ayrı uçta tek tek kopyalansaydı biri unutulduğunda hiçbir şey
> uyarmazdı: `dotnet build` temiz geçer, testler geçer, yalnız
> `GrandTotalTry` ile bileşenleri sessizce ayrışırdı — ve o ayrışma yıllar
> sonra hakedişte ortaya çıkardı.
>
> Bu sınıf o niyeti güvenceye çeviriyor: dönüşüm burada olmazsa hiç olmaz.
> Yeni bir dondurulan alan eklendiğinde eklenecek tek yer burası.
>
> ⚠️ Veritabanı da ayrıca denetliyor: `CK_Reservations_GrandTotal` toplamın
> bileşenlere EŞİT olmasını istiyor, `trg_reservation_commission` dondurulan
> komisyonun sözleşmedekiyle aynı olduğunu doğruluyor. Yani buradaki bir hata
> veritabanına giremez — ama girmeye çalıştığında 500 döner, o yüzden hata
> yine de burada yapılmamalı.
> </summary>


## `src/DailyCruising.Application/Reservations/ReservationService.cs`

**satır 98**

> ⚠️ `voyageId: Guid.Empty` GEÇİCİ. Sefer henüz yok: "bul ya da aç"
> adımı işlem ve satır kilidi gerektirdiği için depoda yapılıyor ve
> `VoyageId`'yi rezervasyon eklenmeden ÖNCE orası dolduruyor.

**satır 112**

> <summary>
> Rezervasyondan sonuç nesnesi.
>
> ⚠️ `boardingToken` TEKRAR GÖNDERİMDE null. Jetonun düz metni yalnız
> üretildiği anda biliniyor; veritabanında yalnız özeti var. Çift gönderme
> korumasına takılan ikinci istek ilk rezervasyonu görüyor ama onun
> jetonunu ÜRETEMİYOR — üretebilseydi jeton tek kullanımlık olmazdı.
>
> Bu bir kayıp değil: ilk isteğin cevabı jetonu zaten taşıdı. İstemci onu
> kaybettiyse QR yeniden üretilmeli (ayrı bir uç, `A-05` kapsamında yok).
>
> ⚠️ `kuponRedSebebi` de tekrar gönderimde null — sebep hesaptan geliyor,
> rezervasyon satırında saklanmıyor. İlk cevap onu taşıdı.
>
> ⚠️ Bu parametre BAŞTA SABİT `null` YAZILMIŞTI ve normal akışta da ret
> sebebini düşürüyordu: kuponu reddedilen müşteri sebebini göremiyordu.
> Test yakaladı (`Suresi_dolan_rezervasyonun_kuponu_serbest_kaliyor`).
> Yardımcıya çıkarılan kod, çıkarılırken alan kaybedebiliyor.
> </summary>

**satır 150**

> <summary>
> Rezervasyonu iptal eder.
>
> KİMLİK: kod TEK BAŞINA yetmez. Kod 8 karakter ve misafir rezervasyonunda
> müşterinin elindeki tek anahtar; yalnız kodla iptale izin vermek, kod
> deneyen birinin başkasının turunu iptal etmesi demekti. Jetonla çağıran
> sahibi için e-posta/telefon gerekmiyor.
>
> ⚠️ "Kod yok" ile "kod var ama kimlik tutmuyor" AYNI cevabı veriyor.
> Ayrışsalardı kimliksiz bir çağıran, geçerli kodları deneyerek ayıklayan
> bir araç elde ederdi — kupon ret sebebinde bilerek kabul ettiğimiz
> sızıntının aksine burada kabul edilecek bir tarafı yok: bu bilgi
> müşteriye hiçbir şey kazandırmıyor.
> </summary>

**satır 212**

> <summary>
> KADEMELİ İADE (Mert, 2026-08-25 / S-12):
>
>   kalkışa 48+ saat   → %100
>   kalkışa 24-48 saat → %50
>   kalkışa &lt;24 saat   → iade yok
>
> Gerekçe: iptalin işletmeye maliyeti zamanla artıyor — koltuk 48 saat
> kala yeniden satılabilir, 6 saat kala satılamaz. Tek oran ya işletmeyi
> son dakika boşluğuna açık bırakır ya müşteriyi erken iptalde
> cezalandırırdı.
>
> ⚠️ KOMİSYON DA AYNI ORANDA iade ediliyor (S-16): %50 iadede platform
> kendi payının da yarısını geri veriyor. Ayrı alan tutulmuyor —
> `CommissionRate` ve `CancellationRefundRate` zaten donmuş, komisyon payı
> ikisinden türetilebiliyor ve üçüncü bir kopya ayrışabilirdi.
>
> ⚠️ SINIR ANLARI: tam 48:00 kala %100, tam 24:00 kala %50. Sınırda
> müşteri lehine karar veriliyor; "48 saat kala iptal ettim ama %50 aldım"
> şikayeti, tersinden çok daha pahalı.
>
> Matrah `GrandTotalTry` — müşterinin FİİLEN ödediği tutar. İndirim
> düşülmüş hâli üzerinden iade ediliyor, ilan edilen liste fiyatı
> üzerinden değil.
> </summary>

**satır 288**

> <summary>
> Telefon karşılaştırması: iki numara da aynı biçime indirilip TAM
> eşleştiriliyor.
>
> ⚠️ Önce KUYRUK eşleşmesiydi (`a.EndsWith(b)`) ve 7 rakam yetiyordu.
> 2026-08-25 güvenlik denetimi bunu iki ayrı yönden kırdı:
>
>   · İkinci faktörün arama uzayı 10 haneden 7 haneye, yani 10 milyona
>     düşüyordu. Kodu ele geçiren biri (kod e-postayla gidiyor ve
>     iletilebilir) numaranın yalnız son 7 hanesini tahmin ederek
>     rezervasyonu iptal edebilirdi.
>   · Tahmin olmadan da kırılıyordu: son 7 hanesi tesadüfen çakışan iki
>     gerçek müşteri (santral, VoIP, aile hattı) birbirinin rezervasyonunu
>     iptal edebilirdi.
>
> Normalleştirme müşteriyi zorlamamak için: `+90 500 111 22 33`,
> `0500 111 22 33` ve `5001112233` aynı numaradır ve üçü de aynı değere
> iniyor. Yabancı numaralarda iki taraf da aynı kurallardan geçtiği için
> tam eşleşme yine çalışıyor.
> </summary>


## `src/DailyCruising.Application/Reviews/ReviewService.cs`

**satır 8**

> <summary>
> YORUMLAR (`A-35`).
>
> ⚠️ YORUM HAKKI REZERVASYONA BAĞLI, KULLANICIYA DEĞİL. Üyelik gerekmiyor;
> misafir de yorum yazıyor ([[domain-gereksinimler]] 2026-08-22). Hakkı
> taşıyan şey, tur sonrası e-postayla giden tek kullanımlık jeton.
>
> ⚠️ YORUM HAKKI FİİLEN TEKNEYE BİNMEKLE DOĞAR — rezervasyon yapmakla değil.
> QR okutulmamış bir rezervasyon yorum yazamıyor.
> </summary>

**satır 73**

> ⚠️ QR KONTROLÜ. Yorum hakkı rezervasyon yapmakla değil FİİLEN
> TEKNEYE BİNMEKLE doğuyor. Kontrol olmasaydı, tura hiç gitmemiş —
> hatta parasını iade almış — biri tekneyi puanlayabilirdi.

**satır 83**

> ⚠️ Davet TÜKETİLİYOR ve tüketim KOŞULLU: iki eşzamanlı istek burada
> ayrışıyor, ikincisi 0 satır etkiler.

**satır 101**

> ⚠️ `Pending` — yorumlar yayına girmeden platform onayından geçiyor.
> Doğrudan `Approved` yazılsaydı hakaret içeren bir yorum tekne
> sayfasında anında görünürdü ve `AverageRating` tetikleyicisi onu
> ortalamaya katardı.

**satır 139**

> <summary>
> İşletmenin kendi yorumları — TÜM durumlar.
>
> ⚠️ Müşteri listesinden farklı olarak `Pending` ve `Rejected` de dönüyor:
> tekne sahibi hakkında yazılanı, onaylanmasını beklemeden görmeli.
> Görmeseydi kötü bir yorum ona ancak yayına girdikten sonra ulaşırdı.
> </summary>

**satır 152**

> <summary>
> Tekne sahibi yoruma CEVAP yazıyor ([[domain-gereksinimler]] 2026-08-22).
>
> ⚠️ Yorum başına EN FAZLA BİR cevap. Sınırsız olsaydı işletme, olumsuz
> bir yorumun altını kendi mesajlarıyla doldurup okunmaz hale getirebilirdi.
>
> ⚠️ Yalnız ONAYLI yoruma cevap yazılıyor. `Pending` bir yoruma cevap
> yazılsa ve yorum sonradan REDDEDİLSE, cevap sahipsiz kalırdı — ve
> cevabın içeriği reddedilen yorumdan alıntı taşıyabilirdi.
> </summary>

**satır 204**

> <summary>
> ⚠️ Jeton ÖZETİYLE aranıyor — **SHA-256**. `A-03` uyarısı: bcrypt
> kullanılsaydı `WHERE` hiç eşleşmez ve her davet "geçersiz" görünürdü.
>
> Bulunamayan jeton ile süresi dolmuş jeton AYNI hatayı almıyor: ikincisi
> müşteriye ne yapacağını söylüyor. Ama "bu jeton yok" ile "bu jeton
> başkasının" ayırt EDİLMİYOR — ayırt edilseydi rastgele deneyerek geçerli
> jeton aranabilirdi.
> </summary>


## `src/DailyCruising.Application/Search/SearchContracts.cs`

**satır 5**

> <summary>
> Müşteri araması (`A-34`). Kimliksiz.
>
> ⚠️ Tutar alanı YOK — `MinPrice`/`MaxPrice` bir FİLTRE, ödenecek tutar değil.
> Sonuçtaki fiyat bağlayıcı da değil: rezervasyon oluşturulurken
> `PricingService` yeniden hesaplıyor → [[api-desenler]] "Para istemciden gelmez".
> </summary>

**satır 28**

> <summary>
> Kişi başı liste fiyatı üzerinden — yetişkin fiyatı baz alınır.
>
> ⚠️ FİYATSIZ kiralama tipleri bu filtreye TAKILMAZ ama filtre
> verildiğinde LİSTEDEN DÜŞER: "500–800 TL arası" arayan müşteriye
> fiyatı bilinmeyen tekneyi göstermek, filtrenin anlamını bozar.
> Filtre verilmediğinde görünürler ([[domain-gereksinimler]] 2026-08-23).
> </summary>

**satır 68**

> <summary>
> Aranan tarihte geçerli EN DÜŞÜK yetişkin fiyatı ve hangi kiralama
> tipinden geldiği. Tarih verilmemişse temel fiyatlar üzerinden.
>
> ⚠️ **`null` OLABİLİR ve bu bir eksiklik DEĞİL.** Tekne sahibi kiralama
> tipini fiyat girmeden tanımlayabiliyor; o zaman müşteri "fiyat için
> iletişime geçin" görüyor ve özel teklif akışı başlıyor
> ([[domain-gereksinimler]] 2026-08-23). Arayüz bu alanın boş olmasını
> bir hata olarak DEĞİL, bir satış yolu olarak göstermeli.
> </summary>


## `src/DailyCruising.Application/Search/SearchService.cs`

**satır 11**

> <summary>
> ⚠️ SAYFA BOYUTU TAVANI. Sınırsız bırakılsaydı `pageSize=100000` ile
> tek istekte tüm katalog çekilebilirdi — hem sunucuyu yorar hem rakip
> bir siteye fiyat listesi kopyalamayı bedava kılardı. Uç kimliksiz,
> yani bunu yapan kişinin hesabı bile yok.
> </summary>

**satır 48**

> ⚠️ GEÇMİŞ TARİH REDDEDİLİYOR. Kabul edilseydi sorgu her zaman boş
> döner ve müşteri "hiç tekne yok" sanırdı — sebebi görünmezdi.


## `src/DailyCruising.Application/Support/SupportContracts.cs`

**satır 5**

> <summary>
> Destek talebi açma.
>
> ⚠️ `Priority` ve `Status` BURADA YOK. Öncelik platformun kararı; müşteri
> kendi talebini "Acil" işaretleyebilseydi tüm talepler acil olurdu ve
> sıralama anlamını yitirirdi.
>
> ⚠️ ÜYELİK GEREKMİYOR: turdan önce hesabı olmayan biri de sorun yaşayabilir.
> Kimlik varsa `UserId` bağlanıyor, yoksa yalnız iletişim bilgisi kalıyor.
> </summary>

**satır 34**

> <summary>
> Destek personelinin YALNIZ İLK İSMİ (`A-53`, Mert soru 14).
>
> ⚠️ Soyadı BİLEREK yok. Müşteri süreklilik hissediyor ("Ayşe ile
> konuşmuştum") ama kişiselleşen bir anlaşmazlık çalışanı hedef
> alamıyor.
>
> Müşterinin kendi mesajlarında `null` — kendi adını kendine
> göstermenin anlamı yok ve alan "karşı taraf kim" sorusuna ait.
> </summary>

**satır 81**

> <summary>
> ⚠️ İÇ NOT — müşteriye GÖRÜNMEZ. Yalnız platform personeli
> gönderebiliyor; müşteri gönderseydi kendi talebine kendisinin
> göremeyeceği bir not eklerdi ki bu anlamsız.
> </summary>


## `src/DailyCruising.Application/Support/SupportService.cs`

**satır 7**

> <summary>
> DESTEK TALEPLERİ (`A-37`) — müşteri ↔ PLATFORM.
>
> ⚠️ Mesajlaşmadan (müşteri ↔ tekne sahibi) BİLİNÇLİ OLARAK AYRI. Mert'in
> açık tercihi: *"net sınır, birleşik kod değil"* ([[domain-gereksinimler]]
> 2026-08-23). Ortak bir "konuşma" altyapısına birleştirilmiyor — çünkü
> kurallar farklı: destekte iç not var, öncelik var, atama var, maskeleme
> YOK (müşteri destek personeline telefonunu verebilmeli).
> </summary>

**satır 51**

> ⚠️ REZERVASYON BAĞLANIRKEN SAHİPLİK KONTROL EDİLİYOR. Edilmeseydi,
> kimlik bilen biri başkasının rezervasyon kodunu talebe iliştirip
> destek personelinden o rezervasyonun bilgilerini öğrenebilirdi.

**satır 79**

> ⚠️ Öncelik PLATFORMUN kararı, istekten gelmiyor.

**satır 130**

> ⚠️ İÇ NOTU YALNIZ PERSONEL yazabiliyor. Müşteri yazabilseydi kendi
> talebine kendisinin göremeyeceği bir not eklerdi — ve o not
> personele "müşteri böyle dedi" gibi görünürdü.

**satır 160**

> ⚠️ `FirstResponseAt` YALNIZ İLK PERSONEL CEVABINDA, ve İÇ NOT
> SAYILMIYOR. İç not sayılsaydı "ilk cevap süresi" raporu, müşterinin
> hiç görmediği bir nota göre hesaplanır ve gerçekte cevapsız kalan
> talepler hızlı görünürdü.

**satır 225**

> ⚠️ `ResolvedAt` YALNIZ İLK ÇÖZÜMDE yazılıyor. Talep yeniden
> açılıp tekrar çözülürse tarih GÜNCELLENMİYOR: "çözüm süresi"
> raporu ilk çözümü ölçmeli, son çözümü değil — yoksa uzun süre
> gidip gelen bir talep, son dokunuşuyla "hızlı çözüldü" görünür.

