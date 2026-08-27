---
rol: not
kapsam: api
guncelleme: 2026-08-27
durum: guncel
---

# Gerekçe arşivi — Api katmanı

Controller'lar, yetkilendirme, boru hattı, Program.cs.

Kod içindeki ⚠️ işaretli gerekçe yorumları 2026-08-27'de silindi; kod artık
yalnız *ne yaptığını* anlatan XML doc taşıyor → [[api-kararlar]]. Silinmeden
önce **90 blok birebir** buraya taşındı: hiçbiri yeniden yazılmadı,
kısaltılmadı, özetlenmedi. Satır numaraları silme anındaki hâle aittir;
dosya adı kalıcı, satır numarası değil.

**Bu bir arşivdir, talimat değil.** Bir madde koda aykırı çıkarsa kod
doğrudur → [[api-desenler]]

Diğer katmanlar: [[api-gerekce-arsivi-domain]]

---


## `src/DailyCruising.Api/Authorization/PermissionAuthorization.cs`

**satır 21**

> <summary>
> İşletmenin aktif olup olmadığı — `OnTokenValidated` içinde okunup
> buraya konuyor (`A-44`).
>
> ⚠️ Sorgu BURADAN taşındı ve sebebi ölçülebilir: `A-43`'te bu işleyici
> kendi sorgusunu atıyordu, `A-44` ikinci bir sorgu daha ekleyecekti.
> İkisi tek okumada birleştirildi.
> </summary>

**satır 42**

> ⚠️ İŞLETME AKTİF DEĞİLSE PANEL KAPALI (`A-42`).
>
> Domain akışı: hesap BAŞVURUDA açılıyor ama panele erişim SÖZLEŞME
> ONAYLANANA kadar kapalı. `Partner` kaydında yazılıydı, hiçbir yer
> uygulamıyordu; başvuru ucu yazılınca canlı bir açığa dönüştü.
> Askıya alma da (`A-38`) yalnız durumu değiştiriyor, jetonu iptal
> etmiyordu.
>
> ⚠️ `403` — `401` DEĞİL: kim olduğunu biliyoruz, izni yok. Damga
> uyuşmazlığı (`A-44`) ise `401` veriyor, çünkü orada jetonun
> KENDİSİ geçersiz.


## `src/DailyCruising.Api/Contracts/QuoteResponse.cs`

**satır 6**

> <summary>
> Fiyat sorgusunun MÜŞTERİYE dönen hâli.
>
> ⚠️ NEDEN AYRI BİR TİP VAR. <see cref="Quote"/> iki işi birden yapıyordu:
> hem hesabın sonucu hem de HTTP yanıtı. Bu ikili kullanım gerçek bir sızıntı
> üretti — denetim (2026-08-25) `commissionRate` alanının KİMLİKSİZ yanıtta
> düz metin olarak döndüğünü buldu ve canlı doğrulandı:
>
>     curl -X POST /api/pricing/quote  →  "commissionRate": 15.0
>
> Yani `A-26` ile kapatılmaya çalışılan sızıntı (kuponun davranışından
> komisyon oranını ÇIKARSAMAK) zaten gereksizdi: oran doğrudan yazıyordu.
> Tek bir anonim istek, herkese açık bir `boatRentalTypeId` ile her işletmenin
> komisyon oranını verebiliyordu.
>
> Bundan sonra kural: <see cref="Quote"/> içine eklenen bir alan buraya
> KENDİLİĞİNDEN gelmez. Yeni alan müşteriye gösterilecekse buraya elle
> yazılır — "unutulursa sızar" yerine "unutulursa görünmez".
>
> Dışarıda bırakılanlar ve sebepleri:
>   `CommissionRate` · `ContractId` — platform ile işletme arasındaki ticari şart
>   `PartnerId`                     — müşterinin işi değil, tekne zaten belli
>   `CouponId`                      — iç kimlik; müşteriye kod yeter
>   `CouponFundedBy`                — indirimi kimin karşıladığı işletmenin
>                                     pazarlama kararı; müşteri için işlevsiz
> </summary>


## `src/DailyCruising.Api/Controllers/AccountController.cs`

**satır 141**

> <summary>
> KVKK "hesabımı sil" (`A-12`).
>
> ⚠️ SİLME DEĞİL ANONİMLEŞTİRME ve cevap bunu açıkça söylüyor.
> Rezervasyon bir muhasebe kaydı, mesaj bir anlaşmazlık kaydı; ikisi de
> `Restrict` zinciriyle tutuluyor. Kişiyi işaret eden alanlar temizleniyor,
> kayıtların kendisi duruyor.
>
> ⚠️ GERİ ALINAMAZ. Bu yüzden mevcut parola isteniyor: çalıntı bir erişim
> jetonuyla hesap kalıcı olarak kapatılabilirdi.
> </summary>


## `src/DailyCruising.Api/Controllers/AuthController.cs`

**satır 12**

> <summary>
> ⚠️ Hız sınırı SINIF ÜZERİNDE DEĞİL, eylem üzerinde.
>
> 2026-08-24 güvenlik denetimi bu denetleyicide hız sınırının HİÇ olmadığını
> buldu ve canlı doğrulandı: 40 ardışık başarısız giriş, 40 kez 401, tek bir
> 429 yok. `/api/auth/login` kaba kuvvete tamamen açıktı — üstelik aynı gün
> asgari parola uzunluğunu 8'e indirme kararının GEREKÇESİ bu sınırdı.
>
> Sınıfa toptan uygulanmadı: `refresh` ve `logout` yüksek frekanslı, tek IP
> arkasındaki bir ofiste 15 dakikada 10 jeton tazelemesi normaldir ve meşru
> kullanıcıları kilitlerdi. Kaba kuvvet yüzeyi `login` ve `register`; jeton
> tazeleme değil — tazeleme jetonu 256 bit ve karşılaştırma karma üzerinden
> yapılıyor, denenerek bulunamaz.
> </summary>


## `src/DailyCruising.Api/Controllers/BoardingController.cs`

**satır 55**

> <summary>
> Reddedilen okutmayı olay günlüğüne yazar ve 400'e çevirir.
>
> ⚠️ BU KAYIT VAZGEÇİLMEZ. `BoardingScans` tablosuna yazmak
> `ReservationId` gerektiriyor; "hiç tanınmayan jeton" denemesinde
> elimizde rezervasyon YOK. Yani jeton deneme saldırısının TEK izi bu
> olay kaydıdır → `BoardingService.ScanAsync`
>
> Payload'a jeton KONMUYOR: `EventLogs` temizlenemiyor ve oraya düşen bir
> jeton, kaydı okuyabilen herkes için kullanılabilir bir anahtar olurdu.
> Aynı sebeple `LogReason` sabit; okutan kişiye giden ayrıntılı metin
> yalnız HTTP yanıtında kalıyor → [[api-desenler]]
> </summary>


## `src/DailyCruising.Api/Controllers/BoatsController.cs`

**satır 10**

> <summary>
> MÜŞTERİYE AÇIK tekne sayfası (`A-33`).
>
> `[AllowAnonymous]`: müşteri kayıt olmadan tekneleri geziyor
> ([[domain-gereksinimler]] akış 1. adım). Bu yüzden hız sınırı kullanıcıya
> değil IP'ye bağlı — `fiyat` politikası da aynı sebeple kimliksiz.
>
> ⚠️ Rota `slug` ile, `id` ile DEĞİL: paylaşılan bağlantı okunabilir olmalı ve
> kimlikle gezinmek rakip işletmelerin tekne sayısını saydırırdı.
> </summary>

**satır 28**

> <summary>
> ⚠️ `boat.viewed` BULUNAMAYAN tekne için de yazılıyor mu? HAYIR.
> Var olmayan bir slug'a yapılan istek görüntüleme değil, çoğunlukla bot
> taraması; talep eğrisine karıştırılırsa "hangi tekneye bakıldı" verisi
> bozulur. Bulunamayan istek `BoatCatalogDenied` olarak ayrı yazılıyor.
> </summary>

**satır 37**

> ⚠️ ESKİ ADRES `301` İLE YENİSİNE (`A-46`, Mert soru 4).
>
> `302` DEĞİL: geçici yönlendirme SEO değerini taşımaz ve arama
> motoru eski adresi indekste tutmaya devam eder. Adres değişimi
> kalıcı bir karar, cevabı da kalıcı olmalı.
>
> Kontrol tekne detayından ÖNCE: eski adresle gelen isteğe önce
> içerik verip sonra yönlendirmek, aynı içeriğin iki adreste
> yayınlanması (yinelenen içerik) demekti.

**satır 61**

> ⚠️ `slug` payload'a KONMUYOR: çağıranın yazdığı ham metin
> temizlenemeyen `EventLogs`'a düşerdi. İzin listesinde de yok,
> yani konsa bile `EventLogger` süzerdi — ikisi birbirini yedekliyor.


## `src/DailyCruising.Api/Controllers/ConversationsController.cs`

**satır 10**

> <summary>
> SİSTEM İÇİ MESAJLAŞMA (`A-36`).
>
> ⚠️ TEK CONTROLLER, İKİ TARAF. Müşteri ve işletme aynı uçları kullanıyor;
> kim olduklarını `ICurrentUser.PartnerId` belirliyor. Ayrı controller'lar
> olsaydı kapsam mantığı iki yerde durur ve biri kayınca diğeri doğru
> kalarak hatayı gizlerdi.
>
> `[HasPermission]` YOK: mesajlaşma bir işletme yetkisi değil, konuşmanın
> TARAFI olma durumu. Çalışanın mesaj yazabilmesi için `PartnerId` yeter.
> </summary>

**satır 23**

> ⚠️ `[Authorize]` ŞART. Olmadan kimliksiz istek servise kadar geliyordu ve
> "Giriş gerekli." diye **400** alıyordu — oysa doğrusu **401**. Canlı
> denemede çıktı (2026-08-26); yetkilendirme kararı boru hattında verilmeli,
> iş kuralında değil.

**satır 66**

> ⚠️ EŞİK AŞILDIYSA PLATFORMA GÖRÜNÜR OLUYOR (`A-52`).
>
> Kullanıcıya hiçbir şey söylenmiyor ve bu bilerek: uyarı
> caydırıcı olduğu kadar nasıl kaçılacağını da öğretirdi.
> Kayıt `EventLogs`'ta ve `eventlog.read` yetkisiyle
> görülebiliyor — platformun denetim yüzeyi orası.

**satır 89**

> <summary>
> ⚠️ Payload'da METİN YOK — uzunluğu ve kaç şeyin maskelendiği var.
> Maskelenmiş metin bile serbest yazı ve `EventLogs` temizlenemiyor;
> metin `Messages` tablosunda duruyor, orası KVKK kapsamında
> temizlenebiliyor.
> </summary>


## `src/DailyCruising.Api/Controllers/OffersController.cs`

**satır 10**

> <summary>
> ÖZEL TEKLİF uçları (`A-36b`).
>
> Rota KONUŞMADAN başlıyor: teklif konuşmanın içinde yaşıyor ve kapsam
> zinciri de öyle — teklif → konuşma → (müşteri | tekne → işletme).
>
> ⚠️ Kabul ve ret MÜŞTERİNİN, gönderme ve geri çekme SATICININ. Ayrım
> servis katmanında `PartnerId`'ye bakılarak yapılıyor; tek bir uçta
> birleştirilseydi "kim neyi yapabilir" sorusu rotadan okunamazdı.
> </summary>

**satır 45**

> ⚠️ TUTAR payload'da — mesaj ve yorumdan farklı olarak. Satıcının
> koyduğu bir SAYI, kişisel veri değil; "hangi fiyattan teklif
> verildi, hangisi kabul edildi" pazarlığın tek ölçüsü. Not metni
> yazılmıyor, o serbest yazı.


## `src/DailyCruising.Api/Controllers/PartnerBoatsController.cs`

**satır 30**

> <summary>
> ⚠️ Liste ve detay olay günlüğüne YAZILMIYOR. İşletmenin kendi verisini
> kendi okuması olağan bir panel hareketi; her ekran açılışını temizlenemeyen
> bir tabloya yazmak günlüğü kullanılamaz hale getirirdi. Platform
> personelinin aynı veriyi okuması AYRI bir uç (`A-38`) ve ORADA yazılıyor —
> muafiyetin bedeli orada ödeniyor.
> </summary>

**satır 78**

> <summary>
> Durum değişikliği AYRI uç — yayından kaldırmak bir düzenleme değil.
> Olay `from`/`to` taşıyor: "tekne ne zaman satıştan çekildi" sorusu
> yalnız böyle cevaplanabiliyor, `Boats` tablosunda son hal duruyor.
> </summary>
> <summary>
> YAYINDAN KALDIRMADAN ÖNCE gösterilecek uyarının verisi (`A-45`).
>
> ⚠️ Ayrı bir OKUMA ucu, durum ucunun cevabına eklenmiş bir alan
> değil: uyarı işlemden ÖNCE gösterilmeli. Cevaba konsaydı işletme
> "40 yolcunuz vardı" yazısını tekne çoktan yayından kalktıktan sonra
> okurdu.
> </summary>

**satır 106**

> ⚠️ Önceki durumu SERVİS döndürüyor, burada ayrıca okunmuyor.
> Burada okunduğunda iki sorun vardı: aynı satır iki kez çekiliyordu
> ve durum ZATEN istenendiyse servis hiçbir şey yazmadan dönerken
> buradaki olay koşulsuz yazılıyordu — günlüğe `from == to` taşıyan
> sahte bir "değişti" satırı düşüyordu. Denetim bulgusu (2026-08-26).

**satır 125**

> <summary>
> Kural ihlallerini HTTP'ye çevirir ve reddi günlüğe yazar.
>
> ⚠️ Günlüğe giden `LogReason` SABİT bir etiket. Bir zamanlar personel
> ucunda `ex.Message` yazılıyordu ve çağıranın gönderdiği ham metin
> temizlenemeyen `EventLogs`'a düşüyordu (denetim 2026-08-25) — o hata
> burada tekrarlanmıyor.
> </summary>


## `src/DailyCruising.Api/Controllers/PartnerDocumentsController.cs`

**satır 13**

> <summary>
> İŞLETME EVRAKLARI (`A-60`, Mert soru 23: *"başvuruda yüklensin"*).
>
> ⚠️ `PartnerDocuments` tablosu şemada 2026-08-24'ten beri VARDI ve
> **ölü tabloydu**: yazan yok, okuyan yoktu. Bu uç onu canlandırıyor.
>
> ⚠️ `[Authorize]` — başvuru ucu kimliksiz ama BELGE YÜKLEME değil.
> Kimliksiz olsaydı herkes herhangi bir işletmeye dosya iliştirebilirdi.
> Başvuran zaten hesabını başvuruda açıyor; yükleme giriş yaptıktan sonra.
>
> ⚠️ İşletme `Active` OLMAK ZORUNDA DEĞİL. Evraklar tam da inceleme için
> yükleniyor; aktiflik kapısı burada uygulanırsa hiçbir başvuru belge
> yükleyemez ve platform hiçbir şeyi inceleyemez.
> </summary>

**satır 36**

> <summary>
> ⚠️ BOYUT SINIRI ZORUNLU ve `RequestSizeLimit` ile uygulanıyor.
> Depolama katmanı dosyayı belleğe alıyor; sınırsız bırakılsaydı tek
> bir istek sunucuyu düşürebilirdi.
> </summary>

**satır 55**

> ⚠️ Dosya ADI payload'a KONMUYOR — kullanıcının yazdığı ham
> metin ve `EventLogs` temizlenemiyor.

**satır 86**

> <summary>
> Evrağı indirir (`A-62`).
>
> ⚠️ `FileKey` hiçbir yerde dışarı verilmiyor; indirme buradan geçiyor.
> Anahtar verilseydi depolama adresine doğrudan erişim denemesine
> davetiye olurdu.
>
> ⚠️ `inline` DEĞİL `attachment`: tarayıcı dosyayı GÖSTERMEK yerine
> indiriyor. Yüklenen bir PDF ya da SVG'nin tarayıcıda çalıştırılması
> (betik gömülmüşse) böyle engelleniyor.
> </summary>


## `src/DailyCruising.Api/Controllers/PartnerPricingController.cs`

**satır 80**

> ---- Fiyatlar ----
>
> ⚠️ `price.read` / `price.write` — `boat.*` DEĞİL (`A-47`, Mert soru 5).
>
> İşletme, çalışanına tekne bilgisini düzenletip FİYATA DOKUNDURMAMAK
> isteyebilir. İki yetki ayrılmasaydı bu ayrım hiç kurulamazdı: kapasiteyi
> düzeltebilen herkes sezon fiyatını da değiştirebilirdi.
>
> Kiralama tipleri BİLEREK `boat.*` kalıyor: süre, kapasite ve kural
> tanımı teknenin yapılandırması, fiyatı değil.
>
> ⚠️ Yetkiler katalogda 2026-08-24'ten beri VARDI ve hiçbir uç
> kullanmıyordu — tanımlanmış ama bağlanmamış bir yetki, verilmiş
> gibi görünüp hiçbir şey yapmaz.

**satır 148**

> ---- Ek hizmetler ----
>
> ⚠️ Yazma `extra.write`, okuma `price.read` (`A-47`). Ek hizmet bir
> menü kalemi ve FİYATI var; tekne yapılandırmasından çok fiyatlandırma
> tarafına ait. Ayrı yetki olması, menüyü güncelleyen bir çalışana
> sezon fiyatlarını açmıyor.


## `src/DailyCruising.Api/Controllers/PartnerReviewsController.cs`

**satır 44**

> ⚠️ Payload BOŞ — cevap metni işletmenin serbest yazısı ve
> `EventLogs` temizlenemiyor. Metin `ReviewReplies`'ta duruyor.


## `src/DailyCruising.Api/Controllers/PartnerStaffController.cs`

**satır 35**

> <summary>
> ⚠️ Eylem adı `AssignablePermissions`, `Permissions` DEĞİL: ikincisi
> yetki sabitlerini tutan statik sınıfla çakışıyor ve `[HasPermission]`
> içindeki `Permissions.RoleManage` bu sınıfın metodunu göstermeye
> başlıyor.
> </summary>

**satır 118**

> <summary>
> ⚠️ Sınıf sınırının ÜSTÜNE ikinci bir sınır. Öznitelikler toplanıyor,
> yani ikisi de geçerli.
>
> Sebep: bu uç e-posta alıyor ve "eklenebilir mi" cevabı veriyor.
> Mesajlar birleştirildi (bkz. `PartnerStaffService.AddMemberAsync`) ama
> birleştirme tek başına yetmez — sınırsız deneme, mesaj tek tip olsa
> bile zamanlama farkından bilgi sızdırabilir ve her deneme
> temizlenemeyen `EventLogs`'a bir satır yazar.
> </summary>

**satır 138**

> ⚠️ Payload'a e-posta KONMUYOR. `EventLogs` temizlenemiyor ve
> eklenen kişinin adresi orada kalıcı olurdu; `memberId` zaten
> `PartnerMembers` üzerinden kişiye bağlanıyor → `A-12`

**satır 183**

> <summary>
> SAHİPLİK DEVRİ (`A-03`).
>
> ⚠️ `staff.manage` YETMEZ, yalnız mevcut sahip devredebilir. Yetseydi
> sahibin çalışanına verdiği personel yönetimi yetkisi işletmeyi
> devralmaya dönüşürdü — kontrol servis katmanında.
> </summary>

**satır 192**

> ⚠️ `panel`in dakikada 120 isteği bu uç için fazla: gövdedeki parola
> doğrulanıyor, yani bu bir parola tahmin ucu -> denetim 2026-08-26

**satır 207**

> <summary>
> Kural ihlallerini olay günlüğüne yazıp DOĞRU HTTP koduna çeviren
> sarmalayıcı. Yakalanmazsa hepsi 500 dönerdi.
>
> İki ayrı istisna, iki ayrı kod:
>   `PartnerStaffNotFoundException` → **404**. Kayıt yok ya da BAŞKA
>     işletmenin; ikisi ayırt edilmiyor. 403 dönseydi "bu kimlik var ama
>     senin değil" demiş olurduk ve çağıran rakip işletmelerin rol
>     kimliklerini deneyerek haritalayabilirdi.
>   `PartnerStaffException` → **400**. Kural ihlali; mesaj işletme
>     sahibine gidiyor ve açıklayıcı olabilir.
>
> REDDEDİLEN denemenin kaydı başarılıdan daha değerli: reddedilen işlem
> hiçbir satırı değiştirmiyor, yani `EventLogs` dışında hiçbir yerde izi
> kalmaz. Yükselme duvarına çarpan bir çağrı ya arayüz hatasıdır ya
> kasıtlı denemedir; ikisi de görünmeli.
>
> ⚠️ GÜNLÜĞE `ex.Message` DEĞİL `ex.LogReason` YAZILIYOR.
>
> Burada bir zamanlar `reason = ex.Message` vardı ve üstündeki yorum
> "metinlerin tamamı sabittir" diye iddia ediyordu. İDDİA YANLIŞTI:
> `YetkileriCozAsync`, tanınmayan yetki anahtarlarını mesaja OLDUĞU GİBİ
> koyuyordu ve o anahtarlar çağıranın `permissions` dizisine yazdığı ham
> metindi. `role.manage` yetkisi olan biri oraya ne yazarsa temizlenemeyen
> `EventLogs` tablosuna kalıcı olarak düşüyordu. Denetim (2026-08-25).
>
> `LogReason` sabit bir etiket; çağıranın gönderdiği hiçbir şey içermiyor.
> Ayrıntılı metin yalnız HTTP yanıtında, yani onu yazan kişiye dönüyor.
> </summary>


## `src/DailyCruising.Api/Controllers/PaymentsController.cs`

**satır 15**

> <summary>
> ⚠️ TUTAR YOK ve olmayacak. İade tutarı iptal anında hesaplanıp
> `Reservations.RefundDueTry` içinde DONDURULDU; buradan tutar alınsaydı
> yetkili bir personel oranı aşan bir iade yaptırabilirdi. Aynı ilke fiyat,
> rezervasyon ve ödeme uçlarında da geçerli.
> </summary>

**satır 59**

> <summary>
> Sağlayıcının geri dönüşü.
>
> ⚠️ SONUÇ İSTEMCİDEN ALINMIYOR. Bu uca "başarılı" yazan bir istek
> ödemeyi tamamlamış saymıyor; `PaymentService` sonucu sağlayıcıdan
> TEYİT ediyor. Buraya gelen tek bilgi işlem kimliği.
> </summary>

**satır 101**

> <summary>
> SAĞLAYICIYA İADE TALİMATI (`A-29`).
>
> ⚠️ Sınıfın `[AllowAnonymous]` ödeme uçlarından TAMAMEN AYRI bir kapı:
> giriş zorunlu, `refund.manage` yetkisi zorunlu, hız sınırı `panel`.
> Diğer iki uç müşteriye ait — bu uç kasadan para çıkarıyor.
>
> Başarısızlık 502 dönüyor, 400 değil: istek doğruydu, KARŞI TARAF
> reddetti. 400 dönseydi çağıran isteğini düzeltmeye çalışırdı, oysa
> düzeltilecek bir şey yok — tekrar denenmesi gereken bir iş var.
> </summary>


## `src/DailyCruising.Api/Controllers/PlatformController.cs`

**satır 15**

> <summary>
> PLATFORM YÖNETİMİ (`A-38`).
>
> ⚠️ **MUAFİYETİN BEDELİ BURADA ÖDENİYOR.** Platform personeli kapsam
> filtresinden muaf (Mert, 2026-08-24); karşılığında HER erişim
> `platform.data.accessed` olarak yazılıyor — okuma dahil.
>
> Diğer controller'larda liste ve detay okumaları GÜNLÜĞE YAZILMIYOR (kendi
> verisini okumak olağan). Burada yazılıyor ve fark tam olarak budur: başka
> birinin verisine bakmak olağan değildir.
> </summary>

**satır 46**

> ⚠️ OKUMA DA YAZILIYOR. Yalnız yazma işlemleri kaydedilseydi,
> "kim kimin verisine baktı" sorusu cevapsız kalırdı — ve
> muafiyetin asıl riski görme, değiştirme değil.

**satır 66**

> <summary>
> Sözleşme gönderir — komisyon oranı burada belirlenir.
>
> ⚠️ "Komisyon düzenleme" diye ayrı bir uç YOK: oranı değiştirmek yeni
> sözleşme (ve yeni onay) demektir.
> </summary>

**satır 85**

> <summary>
> Başvuruyu reddeder (`A-55`). `partner.approve` yetkisi — onaylamanın
> karşılığı; askıya alma (`partner.suspend`) AYRI bir yetki, çünkü
> aktif bir işletmeyi durdurmak başvuru reddetmekten farklı bir karar.
> </summary>
> <summary>
> İŞLETME EVRAĞINI İNDİRİR (`A-62`) — inceleme için.
>
> ⚠️ Kapsam filtresi YOK ve olmamalı: inceleme tam da başkasının
> evrakına bakmak demek. Muafiyetin bedeli burada ödeniyor —
> `platform.data.accessed` yazılıyor. `A-38`'de kurulan kural.
>
> `partner.read` yetkisi: başvuruyu inceleyen kişi evrağı da görmeli.
> </summary>

**satır 109**

> ⚠️ ERİŞİM ÖNCE YAZILIYOR, dosya sonra veriliyor. Ters sırada
> yazılsaydı, indirme yarıda kesilen bir erişim hiç
> kaydedilmezdi — oysa bakılmış olurdu.

**satır 133**

> ⚠️ Sebep METNİ payload'a KONMUYOR — serbest yazı ve `EventLogs`
> temizlenemiyor. Metin `Partners.RejectionReason`'da duruyor.

**satır 140**

> <summary>
> İşletmeyi ödeme sağlayıcısında ALICI olarak kaydeder (`A-41`).
>
> ⚠️ Bugün yalnız sahte sağlayıcıyla çalışıyor — İyzico hesabında
> pazaryeri özelliği kapalı ve gerçek sağlayıcı bunu AÇIKÇA söylüyor.
> Uç yine de var: özellik açıldığında değişecek tek şey sağlayıcının
> gövdesi olacak.
>
> `payout.manage` yetkisi — para akışını kuran bir işlem.
> </summary>

**satır 159**

> ⚠️ Anahtarın KENDİSİ dönmüyor, yalnız açıldığı bilgisi:
> sağlayıcı anahtarı bir kimlik bilgisi ve panele düşmesi
> gereksiz.

**satır 175**

> ⚠️ Sebep METNİ payload'a KONMUYOR — serbest yazı ve `EventLogs`
> temizlenemiyor. Metin `Partners.RejectionReason`'da duruyor,
> orası düzeltilebilir.


## `src/DailyCruising.Api/Controllers/PricingController.cs`

**satır 11**

> <summary>
> Fiyat sorgulama. Anonim: müşteri rezervasyona başlamadan fiyatı görmeli,
> üye olmaya zorlanmamalı.
>
> Bu ucun DÖNDÜRDÜĞÜ tutar bağlayıcı DEĞİLDİR. Rezervasyon oluşturulurken
> hesap aynı servisle yeniden yapılmalıdır; buradaki cevabı saklayıp
> rezervasyonda kullanmak, istemcinin tutarı belirlemesiyle aynı kapıya
> çıkar — sadece kapı bir adım geriye taşınmış olur.
>
> ⚠️ Bu bir KURAL, bugün doğrulanmış bir davranış değil: rezervasyon
> oluşturma ucu henüz yazılmadı. Yazıldığında bu satırın gerçekten geçerli
> olduğu teste bağlanmalı.
> </summary>

**satır 177**

> <summary>
> Olay günlüğüne yazılacak kupon kodu.
>
> ⚠️ BİÇİM DOĞRULANIYOR, yalnız kesilmiyor. Denetim (2026-08-25) şunu
> gösterdi: kupon kutusu serbest metin ve `email` alanının aksine hiçbir
> biçim kontrolü yoktu — müşteri oraya adını, telefonunu ya da adresini
> yazarsa değer olduğu gibi `EventLogs`'a düşüyordu ve o tablo
> temizlenemiyor.
>
> Gerçek kupon kodları harf, rakam, tire ve alt çizgiden oluşuyor
> (`A04GECERLI`, `TEKHAK`, `KUPON1a2b3c4d`). Bu biçime uymayan girdi,
> girdinin KENDİSİ yerine sabit bir işaretle kaydediliyor: deneme sayısı
> ve IP korelasyonu korunuyor, içerik saklanmıyor.
> </summary>


## `src/DailyCruising.Api/Controllers/ReservationsController.cs`

**satır 12**

> <summary>
> Rezervasyon oluşturma.
>
> KİMLİKSİZ ÇAĞRILABİLİR: misafir rezervasyonu ikincil bir kolaylık değil,
> birinci sınıf senaryo — müşteri kayıt olmadan gezip satın alabilmeli
> (Mert, 2026-08-22). Jetonla çağrılırsa rezervasyon o kullanıcıya bağlanır.
>
> ⚠️ Bu uç TUTAR ALMAZ ve fiyat sorgusunun cevabını da almaz. Tutar
> `PricingService` ile SIFIRDAN yeniden hesaplanır. A-04'ün kabul ölçütü
> buydu ve gerçek uygulaması burada: fiyat sorgusunun cevabını istemciden
> geri alıp saklamak, istemcinin tutarı belirlemesiyle aynı kapıya çıkardı.
> </summary>

**satır 54**

> ⚠️ İletişim bilgisi YOK. Ad, e-posta ve telefon
> `Reservations` tablosunda zaten duruyor ve ORASI
> temizlenebilir; `EventLogs` temizlenemez. Aynı kişisel
> veriyi silinemez bir tabloya ikinci kez yazmak `A-12`'yi
> imkânsız hale getirirdi.

**satır 75**

> ONAY E-POSTASI VE SMS'İ — domain kuralı: "rezervasyon tamamlanınca
> müşteriye hem e-posta hem SMS gider". Bu kural yazılıydı ama
> 2026-08-25'e kadar HİÇ uygulanmamıştı; `SendSmsAsync` kod
> tabanında hiçbir yerden çağrılmıyordu.
>
> Olay kaydından SONRA: gönderim uzun sürebilir ve olay kaydı
> rezervasyonun gerçekleştiğinin kanıtı — o kayıt gönderimi
> beklememeli.
>
> ⚠️ Hata BURADA yakalanmıyor; `ReservationNotifier` kendi içinde
> yutuyor ve gürültülü biçimde günlüğe yazıyor. Rezervasyon zaten
> oluştu, sağlayıcı erişilemez diye geri almak müşteriyi hiçbir
> şey kazanmadan kaybetmek olurdu.

**satır 130**

> <summary>
> Rezervasyon iptali.
>
> İlk sürümde DEĞİŞİKLİK yok, yalnız iptal — müşteri kişi sayısını veya
> tarihi değiştiremez, iptal edip yeniden alır -> [[api-sema]] bölüm 5.
>
> ⚠️ İADE TUTARI DÖNMÜYOR. Müşteri iptalinde iade oranı karara bağlanmadı
> (yalnız HAVA iptali için %100 kuralı var) ve sanal POS seçilmedi, yani
> bugün iade fiziken yapılamıyor -> [[api-durum]] S-12. Bu uç koltuğu,
> seferi ve kuponu serbest bırakıyor; para hareketi yok.
> </summary>

**satır 143**

> ⚠️ KODA GÖRE ikinci bir sınır. IP sınırı bu saldırıyı durdurmuyor:
> saldırgan IP değiştirerek tek bir rezervasyonun telefonunu/e-postasını
> sınırsız deneyebilirdi ve her deneme aynı zamanda bir İPTAL denemesi —
> doğru tahmin geri alınamaz. Bu politika denemeyi rezervasyon başına
> bağlıyor, saldırganın kaç IP'si olduğundan bağımsız.


## `src/DailyCruising.Api/Controllers/ReviewsController.cs`

**satır 10**

> <summary>
> MÜŞTERİ YORUMLARI (`A-35`). Kimliksiz.
>
> ⚠️ ÜYELİK GEREKMİYOR ve bu kasıtlı: yorum hakkı REZERVASYONA bağlı,
> kullanıcıya değil ([[domain-gereksinimler]] 2026-08-22). Misafir de yorum
> yazıyor; hakkı taşıyan şey e-postayla giden tek kullanımlık jeton.
>
> Hız sınırı `hesap` politikası (15 dk / 10 istek, IP bazlı): bu uç
> **jeton doğruluyor**, yani kaba kuvvete açık bir yüzey. `fiyat`ın dakikada
> 60 isteği burada çok gevşek olurdu.
> </summary>

**satır 29**

> <summary>
> ⚠️ Jeton `[FromQuery]`, rota parçası DEĞİL. Rota parçaları sunucu
> erişim günlüklerine ham olarak düşer; sorgu dizesi de düşer ama
> tek kullanımlık jetonun ömrü zaten bu isteğe kadar. Asıl korunan yer
> GÖNDERME ucu: orada jeton GÖVDEDE.
> </summary>

**satır 58**

> ⚠️ Payload'da METİN YOK — `rating`, `hasBody`, `scoreCount`.
> Yorum metni müşterinin serbest yazısı; `EventLogs` temizlenemiyor
> ve oraya düşen bir hakaret ya da kişisel veri silinemez. Metin
> `Reviews` tablosunda duruyor, orası düzeltilebilir.


## `src/DailyCruising.Api/Controllers/SearchController.cs`

**satır 26**

> <summary>
> ⚠️ `GET`, `POST` DEĞİL. Arama sonucu paylaşılabilir ve yer imine
> eklenebilir olmalı; gövdeye taşınsaydı adres çubuğunda filtre kalmazdı.
> </summary>

**satır 37**

> ⚠️ SONUÇ SAYISI DA YAZILIYOR. Sıfır sonuçlu arama kaçırılan
> satışın doğrudan ölçüsü — hangi bölgeye, hangi tarihe tekne
> yetmediğini yalnız o söylüyor. Yalnız başarılı aramalar
> yazılsaydı veri sistematik olarak yanıltırdı.


## `src/DailyCruising.Api/Controllers/SupportController.cs`

**satır 13**

> <summary>
> DESTEK TALEPLERİ (`A-37`) — müşteri ↔ platform.
>
> ⚠️ TALEP AÇMAK KİMLİKSİZ: turdan önce hesabı olmayan biri de sorun
> yaşayabilir. Ama LİSTELEME ve OKUMA oturum istiyor — talep kimliğini bilen
> herkes içeriği okuyabilseydi, kimlik tahmin ederek başkalarının destek
> yazışmaları okunurdu.
>
> Personel uçları `support.*` yetkisiyle ve `IsPlatformStaff` ile korunuyor.
> </summary>

**satır 25**

> ⚠️ Sınıf düzeyinde `panel`: oturum açmış kullanıcının kendi taleplerini
> OKUMASI ve cevaplaması olağan bir kullanım. Başta tüm sınıfa `hesap`
> (15 dk / 10 istek) yazmıştım ve canlı denemede birkaç okumadan sonra
> **429** aldım — giriş korumasının bütçesi destek okumaya harcanıyordu.
> Kimliksiz TALEP AÇMA ucu ayrıca daraltılıyor (aşağıda).

**satır 39**

> ⚠️ BU uç kimliksiz ve kalıcı satır yazıyor: `hesap` politikası
> (15 dk / 10 istek, IP bazlı) burada kalıyor. Aksi halde bir bot
> `SupportTickets` tablosunu doldurabilirdi.

**satır 49**

> ⚠️ Payload'da KONU ve GÖVDE yok — ikisi de müşterinin serbest
> yazısı ve `EventLogs` temizlenemiyor. `category` izinli
> listeden geliyor, yani serbest metin değil.

**satır 99**

> <summary>
> Öncelik, durum, atama — YALNIZ platform personeli.
>
> ⚠️ `[HasPermission]` VE servis içinde `IsPlatformStaff` kontrolü, ikisi
> birden. Yetki bir işletme rolüne yanlışlıkla verilirse
> (`IsPartnerAssignable` bunu engelliyor ama katalog değişebilir)
> ikinci duvar tutar.
> </summary>


## `src/DailyCruising.Api/OpenApi/BearerSecurityTransformer.cs`

**satır 2**

> ⚠️ `Microsoft.OpenApi.Models` DEĞİL. v2.7.5'te tipler kök ad alanına
> taşındı; eski ad alanı hâlâ her yerdeki örneklerde geçtiği için kolayca
> yanlış yazılıyor. Assembly'den doğrulandı (2026-08-27).

**satır 9**

> <summary>
> OPENAPI BELGESİNE JWT ŞEMASINI EKLER (`A-63`).
>
> ⚠️ .NET'in yerleşik `AddOpenApi()`'si güvenlik şemasını KENDİLİĞİNDEN
> eklemiyor. Bu dönüştürücü olmadan Scalar'ın jeton alanı hiç çıkmaz ve
> arayüz işe yaramaz: uçların çoğu yetki istiyor, her istek 401 döner ve
> sebebi görünmez. Sessizce boş bir arayüz, hiç arayüz olmamasından kötü.
>
> ⚠️ Şema BELGEYE ekleniyor, uçlara ZORUNLU olarak işaretlenmiyor.
> Kimliksiz uçlar (arama, tekne detayı, rezervasyon, ödeme) gerçekten
> kimliksiz; hepsine "jeton gerekli" damgası vurmak belgeyi yalancı
> yapardı ve frontend gereksiz yere jeton beklerdi.
> </summary>


## `src/DailyCruising.Api/Program.cs`

**satır 123**

> ⚠️ GÜVENLİK DAMGASI DOĞRULAMASI (`A-44`).
>
> İmza ve süre geçerli olsa bile, kullanıcının yetkisi değiştiyse
> jeton ARTIK GEÇERLİ DEĞİL. Yetkiler jetona gömülü olduğu için
> veritabanı doğru olsa bile eldeki jeton 15 dakika donmuş kalıyordu:
> devredilen sahip personel yönetmeye devam edebiliyordu.
>
> ⚠️ BURADA, `[HasPermission]` işleyicisinde DEĞİL. İşleyici yalnız
> yetki isteyen uçlarda çalışıyor; düz `[Authorize]` olan uçlar
> (konuşmalar, destek, hesap) kapsam dışında kalırdı.
>
> ⚠️ Başarısızlık `401` — `403` değil. "Kim olduğunu biliyorum ama
> iznin yok" değil, "bu jeton artık geçerli değil" diyoruz; istemci
> yenileme akışına girmeli.

**satır 156**

> ⚠️ TEK SORGU. `A-43`'te eklenen işletme aktiflik kontrolü
> de burada okunuyor ve sonucu `HttpContext.Items`'a
> konuyor; iki ayrı sorgu istek başına iki gidiş-dönüş
> demekti.

**satır 190**

> ⚠️ Singleton DEĞİL: artık istek başına `DbContext` (scoped) okuyor.
> Singleton kalsaydı `IServiceScopeFactory` üzerinden kendi kapsamını
> açması şart olurdu — bunu zaten yapıyor, ama scoped kaydetmek niyeti
> açık bırakıyor ve ileride doğrudan enjeksiyona geçiş kolaylaşıyor.

**satır 226**

> ⚠️ `ForcePathStyle` — S3 uyumlu sağlayıcıların çoğu alt alan adı
> biçimini desteklemiyor (`bucket.host` yerine `host/bucket`).
> Gerçek AWS ikisini de kabul ediyor, bu yüzden her ikisinde de
> güvenli olan bu.

**satır 268**

> ⚠️ 15 sn'den 5 sn'ye indirildi. Rezervasyon POST'u gönderimi
> BEKLİYOR; iki sağlayıcı da 15 sn'de zaman aşımına uğrasaydı
> müşteri 30 sn cevap alamazdı ve ters vekil (nginx/Cloudflare)
> varsayılan 30 sn sınırında isteği düşürürdü — müşteri
> "başarısız" sanıp tekrar denerdi, oysa rezervasyon oluşmuştur.
> Asıl çözüm arka plan kuyruğu → `A-28`.

**satır 308**

> ⚠️ SCOPED, SINGLETON DEĞİL.
>
> Singleton'dı ve bu üretimde sessiz bir tuzaktı: `AddHttpClient` typed
> istemcileri TRANSIENT kaydediyor, yani singleton bir composite onları
> uygulamanın ömrü boyunca içine HAPSEDER (captive dependency). O zaman
> `IHttpClientFactory`'nin handler yenilemesi hiç çalışmaz ve Postmark/Netgsm
> tarafında bir DNS/IP değişimi uygulama yeniden başlatılana kadar fark
> edilmez.
>
> Geliştirmede GÖRÜNMÜYORDU: orada iki sağlayıcı da singleton (Mailpit + günlük),
> yani singleton-singleton'ı tüketiyordu ve hiçbir şey yanlış görünmüyordu.
> Denetim bulgusu (2026-08-25).

**satır 376**

> Platform yönetimi (`A-38`). ⚠️ Kapsam filtresinden muaf TEK servis;
> muafiyetin bedeli `platform.data.accessed` olayında ödeniyor.

**satır 416**

> İyzico'nun kendi `HttpClient`'ı: taban adres yapılandırmadan geliyor, yani
> sandbox ile üretim ayrımı TEK BİR AYARDA duruyor.
>
> ⚠️ Zaman aşımı 10 sn. Postmark'taki 5 sn'den uzun ve bilerek: ödeme başlatma
> müşterinin bekletildiği bir çağrı ama YARIDA KESİLMESİ bildirimden pahalı —
> İyzico tarafında oluşmuş bir ödemeyi bizim kaydetmememiz demek.

**satır 453**

> ⚠️ ZAMANLANMIŞ İŞLER KAPATILABİLİR — yalnız test sunucusu için.
>
> Test barındırıcısında çalışsalardı iki zarar verirlerdi: TCMB kur işi
> gerçek bir dış isteğe çıkardı, ve diğer işler BAŞKA TESTLERİN satırlarını
> değiştirirdi. İkincisi vault'ta iki kez kayıtlı bir tuzak — iş global
> çalışıyor, testin kendi kurduğu veriyle sınırlı değil.
>
> Varsayılan AÇIK: kapatmayı unutan bir ortam işleri kaybetmez, açmayı
> unutan bir ortam sessizce kaybederdi.

**satır 467**

> --- Hız sınırı ---
>
> Jeton üretimi kullanıcı bazında saatte üçle sınırlı ama bu tek başına
> yetmiyor: saldırgan FARKLI hedef adreslerle sınırsız istek atabilir. Her
> hedef kendi hakkını kullanır, toplam e-posta hacmi sınırsız kalır — e-posta
> bombalama ve gönderici itibarı hasarı.
>
> Bu yüzden ikinci katman IP bazlı.
> ⚠️ Ters vekil arkasında bu IP proxy'nin IP'si olur; `UseForwardedHeaders`
> yapılandırılmadan gerçek istemci görülmez -> görev A-19.

**satır 622**

> ⚠️ Bu dönüştürücü olmadan Scalar'ın jeton alanı HİÇ ÇIKMAZ ve arayüz
> işe yaramaz — uçların çoğu yetki istiyor.

**satır 640**

> GERÇEK İSTEMCİ IP'Sİ (A-19).
>
> Ters vekil arkasında `RemoteIpAddress` vekilin IP'sini döner. Sonuç: adli
> izler (`CreatedIp`, `EventLogs.IpHash`) bozuk ve IP bazlı hız sınırları
> işlevsiz — herkes tek kovaya düşer.
>
> ⚠️ AMA YANLIŞ YAPILANDIRMASI HİÇ YAPMAMAKTAN KÖTÜ. `KnownProxies` /
> `KnownNetworks` verilmezse ASP.NET herhangi bir `X-Forwarded-For` başlığına
> güvenir; saldırgan istediği IP'yi bildirir ve hız sınırını sınırsız
> atlatır, olay günlüğünü de kirletir.
>
> Bu yüzden: yapılandırma varsa açılıyor, üretimde YOKSA uygulama açılmıyor
> (aşağıdaki kontrol). Sessiz bir yanlış yerine gürültülü bir dağıtım hatası.

**satır 720**

> ⚠️ TLS KONTROLÜ. `UseTls` varsayılanı `false` (Mailpit TLS sunmuyor).
> Gerçek bir SMTP rölesine `UseTls` unutularak geçilirse SMTP AUTH
> kimlik bilgileri ve e-posta içeriği DÜZ METİN olarak ağa çıkar —
> ve hiçbir hata görünmez. Denetim bulgusu (2026-08-25).

**satır 754**

> ⚠️ Kimlik bilgisi kontrolü. Boş bırakılırsa uygulama sorunsuz açılır
> ve HER SMS Netgsm'in "30" koduyla reddedilir — tam da bu katmanın
> önlemeye çalıştığı SESSİZ KAYBIN yeni bir çeşidi.

**satır 776**

> ⚠️ SAHTE ÖDEME SAĞLAYICISI ÜRETİMDE AÇILMIYOR. Açılsaydı uygulama
> sorunsuz çalışır, müşteriler "ödedim" der ve HİÇBİR PARA TAHSİL
> EDİLMEZDİ — üstelik defter kayıtları da yazılırdı, yani hesap
> tahsil edilmemiş parayı gerçek gösterirdi.
> ⚠️ TEST ANAHTARLARI ÜRETİMDE KAPALI OLAMAZ (`A-43`).
>
> İkisi de test sunucusu için eklendi ve ikisi de yanlışlıkla `false`
> kalırsa SESSİZCE koruma kaybettirir: uygulama sorunsuz açılır, hiçbir
> hata vermez ve yalnız hiçbir şey OLMAZ. Zamanlanmış işler kapalıysa
> tutmalar süresiz kalır ve takvim kilitlenir; hız sınırı kapalıysa
> kimliksiz bir çağıran sınırsız hesap açabilir.

**satır 801**

> ⚠️ API ARAYÜZÜ ÜRETİMDE AÇILAMAZ (`A-63`).
>
> Yukarıdaki `IsDevelopment()` koşulu ortam değişkenine güveniyor;
> yanlış ayarlanmış bir sunucu kendini Development sanabilir. Bu kapı
> ikinci katman: ortam Production ise ve biri arayüzü açıkça açmaya
> çalışıyorsa uygulama HİÇ AÇILMIYOR.
>
> Sessiz bir bayrak yerine açılışta patlamak seçildi — sahte ödeme
> sağlayıcısı ve sandbox adresi yasaklarındaki desen.

**satır 817**

> ⚠️ DEPOLAMA KİMLİK BİLGİSİ ZORUNLU. Boş bırakılırsa uygulama sorunsuz
> açılır ve HER dosya yüklemesi başarısız olur — işletme belge
> yükleyemez, tekne fotoğrafı çıkmaz, ve sebebi ancak biri şikayet
> edince görülür.

**satır 829**

> ⚠️ Yerel MinIO adresi üretimde açılmıyor: sandbox adresi yasağının
> aynısı. Açık kalsaydı yüklenen her dosya geliştirme makinesine
> gitmeye çalışır ve sessizce kaybolurdu.

**satır 848**

> ⚠️ Kimlik bilgisi kontrolü — Netgsm'dekiyle aynı gerekçe. Boş
> bırakılırsa uygulama sorunsuz açılır ve HER ödeme sağlayıcıda
> reddedilir; bunu ancak ilk müşteri ödeyemediğinde görürdük.

**satır 859**

> ⚠️ SANDBOX ADRESİ ÜRETİMDE AÇILMIYOR. Sandbox gerçek kart çekmez ve
> gerçek para hareketi yaratmaz: uygulama sorunsuz çalışır, müşteri
> "ödedim" der, defter kaydı yazılır ve HİÇBİR PARA TAHSİL EDİLMEZ.
> Sahte sağlayıcı yasağının aynısı, farklı kılıkta.

**satır 881**

> ⚠️ AÇILIŞ HATIRLATMASI — `A-41` (2026-08-26).
>
> İyzico hesabında PAZARYERİ özelliği kapalı olduğu sürece hiçbir işletmenin
> alıcı kaydı açılamıyor; tahsilat tamamen platform hesabına yapılıyor ve
> hakediş transferi ELLE yapılmak zorunda.
>
> Bu bir kod eksiği DEĞİL, hesap ayarı — dolayısıyla test kırmızıya dönmez ve
> sessizce unutulabilir. Uygulama her açılışta yüksek sesle söylüyor.
>
> Uyarı KENDİLİĞİNDEN SUSUYOR: alıcı kaydı açılmış en az bir işletme
> olduğunda çıkmıyor. Elle kaldırılması gereken bir şey bırakmıyor.

**satır 912**

> ⚠️ EN BAŞTA. Sonraki her ara katman (hız sınırı, kimlik doğrulama, olay
> günlüğü) `RemoteIpAddress`'i okuyor; başlık daha sonra işlenirse hepsi
> vekilin IP'sini görür.

**satır 920**

> ⚠️ API BELGESİ VE ARAYÜZÜ YALNIZ GELİŞTİRMEDE (`A-63`).
>
> Üretime sızan bir API arayüzü, yetki isteyen 85 işlemin TAM HARİTASINI
> herkese verir: hangi uçlar var, hangi alanları alıyorlar, hangi yetkiyi
> istiyorlar. Saldırgana keşif işini yaptırmak yerine hazır sunmak olurdu.
>
> Bu koşul TEK BAŞINA yeterli değil — `ASPNETCORE_ENVIRONMENT` yanlış
> ayarlanmış bir sunucu "Development" sanır ve arayüz açılır. Bu yüzden
> aşağıda ayrıca bir üretim kapısı var.

**satır 941**

> ⚠️ JWT ALANI ŞART. Uçların çoğu yetki istiyor; jeton
> yapıştırılamayan bir arayüzde her istek 401 döner ve arayüz
> hiçbir işe yaramaz.

**satır 960**

> ⚠️ ÇAKIŞMA `409`, `500` DEĞİL (`A-48`).
>
> İyimser eşzamanlılık jetonu proje geneline açıldı; "başkası aynı anda
> değiştirdi" artık düzenli olarak oluşacak bir durum. `500` dönseydi
> istemci bunu sunucu hatası sanar, kullanıcıya "bir şeyler ters gitti"
> der ve DOĞRU eylem — yeniden okuyup tekrar denemek — hiç
> önerilmezdi. Üstelik günlükler gerçek hatalarla dolardı.

**satır 990**

> Sıra önemli: UseAuthentication kimliği çözer, UseAuthorization onun sonucuna
> bakar. Ters yazılırsa her istek kimliksiz görünür ve yetkili uçlar 401 döner.
> ⚠️ HIZ SINIRI KAPATILABİLİR — yalnız test sunucusu için.
>
> Kovalar `RemoteIpAddress`'e göre bölünüyor; test sunucusunda o adres BOŞ,
> yani BÜTÜN testler tek kovayı paylaşıyor (15 dk / 10). Açık bırakılsaydı
> HTTP testleri çoğaldıkça paket `429` ile kırılır ve bu, gerçek bir hata
> gibi görünürdü.
>
> Varsayılan AÇIK: kapatmayı unutan ortam korumasını kaybetmez.
> Sınırın kendisi `HizSiniriTests` içinde AÇIKKEN sınanıyor.

