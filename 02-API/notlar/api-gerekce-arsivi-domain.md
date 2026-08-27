---
rol: not
kapsam: api
guncelleme: 2026-08-27
durum: guncel
---

# Gerekçe arşivi — Domain katmanı

Varlıklar, enum'lar ve şema değişmezleri.

Kod içindeki ⚠️ işaretli gerekçe yorumları 2026-08-27'de silindi; kod artık
yalnız *ne yaptığını* anlatan XML doc taşıyor → [[api-kararlar]]. Silinmeden
önce **23 blok birebir** buraya taşındı: hiçbiri yeniden yazılmadı,
kısaltılmadı, özetlenmedi. Satır numaraları silme anındaki hâle aittir;
dosya adı kalıcı, satır numarası değil.

**Bu bir arşivdir, talimat değil.** Bir madde koda aykırı çıkarsa kod
doğrudur → [[api-desenler]]

Diğer katmanlar: [[api-gerekce-arsivi-application]]

---


## `src/DailyCruising.Domain/Billing/Coupon.cs`

**satır 22**

> <summary>
> İndirimin bedelini KUPONU OLUŞTURAN taraf karşılar (Mert, 2026-08-25 / S-14).
> Bu karar iki eski kuralı birden iptal ediyor:
>
>   1. "İndirimi tamamen platform karşılar" — artık geçerli değil. İşletme
>      kendi kampanyasını yapabiliyor ve bedelini kendi üstleniyor.
>   2. "Kupon oranı komisyon oranını aşamaz" — kural KALDIRILDI (S-10).
>      Kural bir sızıntı üretiyordu: aynı kuponun bir teknede geçip diğerinde
>      geçmemesi, kimliksiz bir çağırana o iki işletmenin komisyon oranını
>      sıralatıyordu. `trg_coupon_within_commission` tetikleyicisi de
>      `A-26` ile kaldırıldı → [[api-kararlar]]
>
> ⚠️ <see cref="FundedBy"/> ile <see cref="PartnerId"/> AYRI şeylerdir ve
> birbirinden türetilemez. `PartnerId` kuponun nerede GEÇERLİ olduğunu söyler
> (kapsam); platform yönetimi tek bir işletmeye özel kampanya yapabilir ve o
> kuponun bedelini yine platform karşılar. Bedeli kimin ödediği ancak açıkça
> yazılırsa bilinir.
> </summary>


## `src/DailyCruising.Domain/Billing/Enums.cs`

**satır 34**

> <summary>
> İŞLETME KAYNAKLI İPTAL (`A-57`, Mert soru 18).
>
> ⚠️ Eskiden bu durumlar <see cref="PlatformDecision"/>'a düşüyordu ve
> raporda **platform hatası gibi görünüyordu**. Hangi işletmenin kaç tur
> iptal ettiği ölçülemiyordu — oysa bu, işletme kalitesinin en doğrudan
> göstergelerinden biri.
> </summary>


## `src/DailyCruising.Domain/Catalog/BoatSlug.cs`

**satır 3**

> <summary>
> TEKNE ADRESLERİ — geçmişi ve dilleri (`A-46`, Mert soru 4).
>
> İki karar aynı tabloyu istiyordu ve ayrı ayrı yapılsaydı tablo iki kez
> tasarlanırdı:
>
> 1. **Ad değişince slug değişsin, eskisi yönlendirsin** (soru 4). Eski
>    satır `IsCanonical = false` olarak duruyor; o adrese gelen istek
>    `301` ile yenisine gidiyor. Silinseydi paylaşılmış her bağlantı
>    kırılır ve SEO değeri sıfırlanırdı.
> 2. **Dile göre ayrı slug** ([[domain-gereksinimler]] 2026-08-24,
>    Mert: *"kesinlikle yapacağız"*). `LanguageCode` bugün hep `tr`, ama
>    şema buna kapatılmıyor.
>
> ⚠️ `Boats.Slug` KALDI ve yürürlükteki adresin kopyasını taşıyor. İki
> yerde tutmak ayrışma riski demek; bu yüzden ad güncellemesi ikisini de
> TEK İŞLEMDE yazıyor. Kaldırmak, `Slug`'ı okuyan her sorguyu değiştirmek
> olurdu ve bu görevin kapsamı değil.
> </summary>

**satır 32**

> <summary>⚠️ GLOBAL benzersiz: iki tekne aynı adresi paylaşamaz.</summary>


## `src/DailyCruising.Domain/Community/Reviews.cs`

**satır 122**

> <summary>
> HATIRLATMA GÖNDERİLDİ Mİ (`A-50`, Mert soru 8).
>
> ⚠️ Bu alan olmadan hatırlatma yazılamazdı: iş saatlik çalışıyor ve
> "7 gün geçmiş, yorum yazılmamış" koşulu her saat DOĞRU kalırdı —
> müşteri aynı hatırlatmayı saatte bir alırdı.
>
> Sayaç değil TARİH: hatırlatma yalnız BİR KEZ gönderiliyor (Mert),
> dolayısıyla "gönderildi mi" sorusunun cevabı tek bir damga.
> </summary>


## `src/DailyCruising.Domain/Identity/ConsentDocument.cs`

**satır 3**

> <summary>
> ONAY METNİ VE SÜRÜMÜ (`A-59`, Mert soru 22).
>
> ⚠️ Bu tablo olmadan `ConsentRecord.DocumentVersion` sunucudaki bir
> SABİTTEN geliyordu. Metin değişip sabit güncellenmezse, yeni metni
> onaylayan kullanıcı **eski sürümle** kaydedilir ve bunu hiçbir şey
> söylemezdi — KVKK ispatı sessizce değersizleşirdi.
>
> `ContractTemplates` deseninin aynısı: metin ve sürüm veritabanında,
> onay kaydı gerçek bir sürüme bağlanıyor.
>
> ⚠️ **METİN GÜNCELLENMEZ, YENİ SÜRÜM EKLENİR.** Yürürlükteki metnin
> gövdesi değiştirilebilseydi, geçmişte onay veren kullanıcıların neyi
> onayladığı geriye dönük olarak DEĞİŞİRDİ — anlaşmazlıkta elde tutulacak
> tek kanıt buydu. Aynı ilke sözleşme anlık görüntüsünde de var.
> </summary>


## `src/DailyCruising.Domain/Identity/User.cs`

**satır 35**

> <summary>
> GÜVENLİK DAMGASI (`A-44`) — yetkisi değişen kullanıcının erişim
> jetonunu ANINDA geçersiz kılar.
>
> ⚠️ Neden gerekli: yetkiler erişim jetonuna GÖMÜLÜ ve jeton 15 dakika
> yaşıyor. Sahiplik devredildiğinde, rol değiştirildiğinde ya da üyelik
> pasife alındığında veritabanı doğru oluyor ama ELDEKİ JETON donmuş
> kalıyordu: eski sahip 15 dakika boyunca personel yönetmeye devam
> edebiliyordu. Canlı doğrulamada ölçüldü (2026-08-26).
>
> Damga değişince jetondaki kopya tutmaz ve istek `401` alır — istemci
> yenileme akışına girer, yeni jeton doğru yetkilerle üretilir.
> </summary>


## `src/DailyCruising.Domain/Notifications/NotificationOutbox.cs`

**satır 3**

> ⚠️ `NotificationChannel` BU DOSYADA TANIMLI DEĞİL — `Notifications.cs`
> içinde zaten vardı (`Email` / `Sms` / `InApp`). İkinci bir tanım yazmıştım,
> derleyici yakaladı. Aynı kavramın iki enum'u olsaydı biri `InApp`'i bilir
> diğeri bilmezdi ve fark ancak çalışma anında görünürdü.

**satır 17**

> <summary>
> GİDEN KUTUSU (`A-28`).
>
> Bildirimler önce buraya yazılıyor, sonra `DispatchNotificationsJob`
> gönderiyor. İki şeyi birden çözüyor:
>
> 1. **HTTP cevabı gönderimi beklemiyor.** Önce rezervasyon `POST`'u
>    Postmark ve Netgsm'in cevabını bekliyordu; iki sağlayıcı da yavaşsa
>    müşteri saniyelerce cevap alamıyordu.
> 2. **Yeniden deneme var.** Önce sağlayıcı o an erişilemezse bildirim
>    KAYBOLUYORDU — müşteri rezervasyon kodunu hiç almıyordu ve bunun tek
>    izi bir uygulama günlüğü satırıydı.
>
> ⚠️ SATIRLAR KİŞİSEL VERİ TAŞIYOR (alıcı adresi, telefon, gövdede ad).
> Bu yüzden başarılı gönderimde satır SİLİNİYOR — kalıcı ikinci bir kopya
> oluşmuyor. Kalıcı iz `EventLogs`'ta ve orada kişisel veri yok.
> </summary>


## `src/DailyCruising.Domain/Partners/Partner.cs`

**satır 18**

> <summary>
> HAKEDİŞ HESABI (`A-41`). Ödeme sağlayıcısına alıcı kaydı açmak için
> zorunlu; onsuz para işletmeye HİÇ gönderilemez.
>
> ⚠️ Nullable, çünkü bu alan eklenmeden ÖNCE kaydolmuş işletmeler var.
> Zorunlu yapılsaydı migration mevcut kayıtlarda patlardı; boş bırakılan
> işletme için alıcı kaydı açılmıyor ve bu görülebilir bir durum
> (`PartnerPayeeAccount` satırı yok), sessiz bir hata değil.
> </summary>

**satır 29**

> <summary>
> ⚠️ `TaxNumber`'ın ANLAMINI belirliyor: <see cref="PartnerBusinessType.Personal"/>
> ise TC kimlik numarası, diğerlerinde vergi numarası. Tür olmadan
> `TaxNumber` yorumlanamaz ve sağlayıcıya yanlış alanda gönderilir.
> </summary>

**satır 41**

> <summary>
> ASKIYA ALMA sebebi — `RejectionReason` DEĞİL.
>
> ⚠️ İlk sürümde askı sebebi `RejectionReason`'a yazılıyordu. İki sorun:
> kolon adı içeriğiyle uyuşmuyordu ([[api-desenler]] "Kolon adı
> içeriğiyle uyuşmalı") ve `CK_Partners_RejectionReason` o kolonu
> `Rejected` durumuna bağlıyor — askıya alınan bir işletmenin
> "reddedilme sebebi" olması anlamsız. Düzeltildi 2026-08-26.
>
> Askı kalkınca temizleniyor: kalsaydı panelde "askıdasınız" metni aktif
> bir işletmede görünmeye devam ederdi.
> </summary>


## `src/DailyCruising.Domain/Partners/PartnerPayeeAccount.cs`

**satır 3**

> <summary>
> İşletmenin ÖDEME SAĞLAYICISI TARAFINDAKİ kimliği (`A-41`).
>
> ⚠️ SAĞLAYICI BAŞINA AYRI SATIR ve bu bilerek — `Payments.Provider`
> dersinin aynısı. İyzico'nun verdiği `subMerchantKey` yalnız İyzico'da
> geçerli; PayTR'ye geçildiğinde o anahtar hiçbir şey ifade etmez.
> Tek kolonda saklansaydı sağlayıcı değiştiği gün her ödeme, var olmayan
> bir alıcıya bölüştürülmeye çalışılır ve sessizce başarısız olurdu.
>
> Eski sağlayıcıdaki satır SİLİNMİYOR: geçmiş ödemelerin iadesi ve
> mutabakatı hâlâ oradan geçiyor.
> </summary>

**satır 46**

> <summary>
> İşletmenin hukuki türü. Ödeme sağlayıcısının alıcı kaydı için ZORUNLU:
> şahıs ile limited şirket farklı belge istiyor.
>
> ⚠️ Bu alan `TaxNumber`'ın ne anlama geldiğini de belirliyor —
> <see cref="Personal"/> için TC kimlik numarası, diğerlerinde vergi
> numarası. Tür bilinmeden `TaxNumber` tek başına yorumlanamaz.
> </summary>


## `src/DailyCruising.Domain/Reservations/BoardingScan.cs`

**satır 22**

> <summary>
> ⚠️ YALNIZ <see cref="Succeeded"/> false iken dolar. Sabit bir etiket
> (`Cancelled`, `TokenExpired`, `NotPaid`) taşır, serbest metin değil.
> </summary>

**satır 28**

> <summary>
> Okutan kişinin notu — bugün yalnız ELLE binişte (`Method = Manual`)
> doluyor: "iskelede internet yoktu" gibi.
>
> ⚠️ Ayrı kolon, bilerek. Bu not başta `FailureReason`'a yazılıyordu ve
> `Succeeded = true` olan satırlarda "başarısızlık sebebi" adlı bir alan
> dolu görünüyordu. `BoardingScans` tablosunu doğrudan sorgulayan biri
> (denetim, raporlama) kolonun adına bakıp yanlış sonuca varırdı.
> Denetim bulgusu (2026-08-25).
> </summary>


## `src/DailyCruising.Domain/Reservations/Reservation.cs`

**satır 22**

> <summary>
> ÇİFT GÖNDERME KORUMASI. İstemcinin ürettiği, o ödeme denemesine ait
> benzersiz anahtar.
>
> ⚠️ `Code` ve `BoardingTokenSha256` de benzersiz ama ikisi de SUNUCUDA
> üretiliyor — her istekte yenisi çıkıyor, dolayısıyla çift göndermeyi
> durdurmuyorlar. Koruma ancak istemcinin AYNI değeri tekrar göndermesiyle
> mümkün.
>
> Korunan senaryo: müşteri "Rezervasyonu tamamla" düğmesine iki kez
> basıyor ya da ağ tekrarı aynı isteği iki kez gönderiyor. Koruma
> olmadan iki rezervasyon oluşuyor ve İKİSİ DE koltuk düşüyor; müşteri
> iki kod alıyor ve birini iptal etmesi gerektiğini bilmiyor.
>
> `SoldSeats &lt;= Capacity` kısıtı bunu YAKALAMAZ: yalnız sefer zaten
> doluysa ikinciyi reddeder, boşsa ikisi de sessizce geçer.
> Koruma değil tesadüf olurdu.
>
> Aynı desen `Payments.IdempotencyKey`'de zaten vardı.
> </summary>

**satır 111**

> <summary>
> İndirimin bedelini kimin karşıladığı — rezervasyon anında DONDURULUYOR.
> Kupon yoksa null.
>
> ⚠️ `Coupons.FundedBy`'dan sonradan okunamaz: kupon satırı değişebilir
> (kampanya devredilir, kapsam düzeltilir) ve o an geçmiş rezervasyonların
> hakedişi sessizce başka bir tarafa kayardı. Rezervasyondaki her para
> alanı gibi bu da yazıldığı andaki gerçeği taşır → [[api-desenler]]
> </summary>

**satır 122**

> <summary>
> İndirimin, karşılayan tarafın payını AŞAN ve platformun üstlendiği
> kısmı. Normalde sıfır.
>
> Sıfırdan büyük olması şu dar durumu gösterir: kupon yaratıldığında
> oran uygundu ama sonradan sözleşme komisyonu düştü ve indirim artık
> karşılayanın payını aşıyor.
>
> ⚠️ NEDEN MÜŞTERİNİN İNDİRİMİ KIRPILMIYOR. Kırpmak, aynı kuponun farklı
> komisyonlu teknelerde farklı indirim vermesi demek — kimliksiz çağıran
> bunu okuyup komisyon oranını çıkarır. `S-10`'da tam olarak bu sızıntı
> kapatılmıştı → [[api-benim-kararlarim]] 2026-08-26.
>
> ⚠️ NEDEN İŞLETMEYE YÜKLENMİYOR. `S-15`'in amacı "kimse borca girmesin".
> Oranın değişmesi işletmenin kararı değil; farkı ona yüklemek onu
> haberi olmayan bir değişiklikten zarara sokardı.
>
> Rezervasyon anında DONDURULUYOR: sonradan hesaplansaydı kupon ve
> sözleşme satırları değişmiş olurdu.
> </summary>

**satır 167**

> <summary>
> İptalde müşteriye dönecek oran (0 / 50 / 100). İptal edilmemişse null.
>
> Mert (2026-08-25, S-12): kalkışa **48+ saat** kala %100, **24-48 saat**
> arası %50, **24 saatten az** kala iade yok.
>
> ⚠️ Oran İPTAL ANINDA dondurulur, sonradan hesaplanmaz. Sonradan
> hesaplansaydı "kalkışa kaç saat kalmıştı" sorusu bugünün saatine göre
> cevaplanır ve geçmiş iptaller zamanla yanlış orana kayardı.
> </summary>

**satır 179**

> <summary>
> Müşteriye dönecek TL tutarı. Para hareketi YOK — sanal POS (`G-03`)
> seçildi ama entegrasyon yazılmadı (`A-29`). Bu alan hesaplanan borcu
> taşıyor; `A-18` defter ters kaydını buradan üretecek.
>
> ⚠️ Komisyon da AYNI ORANDA iade ediliyor (Mert, 2026-08-26 / S-16):
> %50 iadede platform kendi payının da yarısını geri veriyor. Ayrı alan
> tutulmuyor çünkü `CommissionRate` ve `CancellationRefundRate` zaten
> donmuş — komisyon payı ikisinden türetilebiliyor ve üçüncü bir kopya
> ayrışabilirdi.
> </summary>

**satır 192**

> <summary>
> İPTALİN SEBEBİ (`A-54`) — otomatik iade işi bunu sağlayıcıya
> gönderdiği kayda yazıyor.
>
> ⚠️ Bu alan olmadan `A-56` iş, HER iptali `CustomerCancellation`
> sayıyordu. Askıya alma yüzünden iptal edilen bir tur da müşteri
> vazgeçmiş gibi raporlanırdı — `A-57` ile eklenen ayrım tam da bunu
> önlemek içindi ve kaydedilecek bir yer olmadan işe yaramazdı.
>
> `CancellationRefundRate` ile birlikte doluyor; ikisi de iptal anında
> donuyor.
> </summary>


## `src/DailyCruising.Domain/Reservations/ReservationStatuses.cs`

**satır 3**

> <summary>
> "Satış hâlâ ayakta mı" sorusunun TEK cevabı.
>
> Bu liste üç ayrı yerde kullanılıyor ve üçünün de AYNI olması zorunlu:
>
>   `trg_reservation_sync_seats`        koltuk sayacı (SQL)
>   `count_live_coupon_redemptions`     kupon kullanım hakkı (SQL)
>   `ExpireReservationHoldsJob`         seferin bırakılıp bırakılmayacağı (C#)
>   `PricingRepository`                 kupon sayımının uygulama tarafı (C#)
>
> ⚠️ Bir kez kaydı ve HİÇBİR YERDE HATA VERMEDİ: uygulama bütün kupon
> kullanımlarını sayarken tetikleyici yalnız canlı olanları sayıyordu. Süresi
> dolan bir rezervasyondan sonra veritabanı kuponu kabul ederken uygulama
> "hakkı dolmuş" diyordu — iki taraf da kendi içinde tutarlı, cevap yanlış.
>
> C# tarafı artık tek yerden okuyor. SQL tarafıyla eşleştiği
> `RezervasyonTests.Canli_durum_listesi_sql_ile_ayni` testiyle sabitleniyor;
> derleyici bunu göremez.
> </summary>

