---
rol: status
kapsam: genel
guncelleme: 2026-09-05
durum: guncel
---

# Durum — Genel Resim, Blocker'lar, Çelişkiler

> **"Nerede kaldık" sorusunun tek otoritesi bu dosyadır.** `04-Oturumlar/` arşivdir;
> çeliştiklerinde bu dosya doğrudur. Yapılacak işler burada değil panolardadır:
> [[genel-gorevler]] · [[api-gorevler]] · [[web-gorevler]]

## ✍️ Bu dosyaya kim yazar

Aynı anda birden fazla Claude oturumu açık olabiliyor. Üçü de bu dosyaya yazarsa
biri diğerinin yazdığını **sessizce siler** — vault git reposu olmadığı için geri
de alınamaz. Bu yüzden yazma hakkı bölünmüştür:

Ölçüt **cwd değil, o oturumun üzerinde çalıştığı alandır** — 2026-08-24 testinde
frontend işi yapan oturumun `pwd`'si vault çıktı, yani klasör güvenilir bir işaret değil.

| Oturumun üzerinde çalıştığı alan | Yazabileceği | Alan durumu |
|---|---|---|
| Backend kodu | `02-API/*` | [[api-durum]] |
| Frontend kodu | `03-Web/*` | [[web-durum]] |
| Vault / genel | `00-Index.md` · `04-Oturumlar/` · **bu dosya** | — |

**Alan oturumları bu dosyaya yazmaz.** Kendi `*-durum.md` dosyasına yazar; genel
resmi vault oturumu buradan derler. Ama `domain-gereksinimler.md` ve
`genel-gorevler.md` **ortaktır** — domain cevabını konuşan oturum, görev kanıtını
kapatan oturum yazar. Genel dosyaya girmesi gereken bir şey varsa
vault oturumuna `SendMessage` ile haber verilir.

⚠️ **Başka bir oturum çalışıyorken okunan durum anında bayatlar.** 2026-08-24'te
Front-End'i "2 dosya commit'lenmemiş" diye okudum; ölçtüğüm anda doğruydu, ama
peer oturum saniyeler sonra commit attı ve kayıt yalan oldu. Başka oturum
açıkken **git durumu, dosya sayısı ve "şu an ne yapılıyor" bilgisi vault'a
yazılmaz** — yazılacaksa önce o oturuma sorulur → [[genel-esszamanli-oturumlar]]

## ➡️ Şu an nerede duruyoruz

**2026-08-28: aktif blocker sayısı 1'e indi — kalan tek engel Mert'te.**

Panolar (28 Ağustos, alan oturumlarının kendi ölçümü):

| Alan | Yapılacak | Tamamlandı |
|---|---|---|
| API | 3 | 93 |
| Web | 4 | 64 |
| Genel | 6 | 11 |

⚠️ **Bu sayılar panodan okunamıyordu, sayılarak bulundu.** Üç panoda birden
**bitmiş görevler Yapılacak bölümünde duruyordu**; web "5 kaldı" derken pano 9
gösteriyordu, aradaki 4 taşınmamış satırdı. `dogrula.py` **kontrol 17** artık
bunu ölçüyor (ilk çalıştırmada 7 kayma buldu) → [[genel-desenler]]

Web'in 11 → 17 → 5 seyri **iş miktarının değişmesi değil**: 21 bağlanmamış yol
28 Ağustos'ta görünür oldu, 30–31 Ağustos'ta on üçü kapandı.

Backend'de Mert'in kararına bağlı olmayan iş kalmadı; kalan üçün ikisi `A-41`'e
bağlı, üçüncüsü (`A-07`) frontend alanı.

| Alan | Ölçü |
|---|---|
| API | **28 controller · 93 yol · 42 migration · 484 test** (31 Ağu ölçümü) → [[api-mimari]] |
| Web | 25 rota · rota koruması (`proxy.ts`) çalışıyor · gerçek API'ye bağlandı (`W-04`) → [[web-mimari]] |

Ödeme uçtan uca çalışıyor: **gerçek İyzico sandbox'ına karşı** rezervasyon →
ödeme → geri dönüş → `Paid`, ve iade → `Refunded`, defter 0.00 kapanıyor (`A-29`).

**Kritik yol artık tek düğümde:** `A-41` (alt üye iş yeri ve hakediş transferi).
Bugün tahsilat **platform hesabına** yapılıyor, hakediş defterde duruyor ama
işletmeye para geçmiyor. `A-58` de buna bağlı.

## 2026-09-05 — 29 sorunun tamamı cevaplandı, öncelik demo testine döndü

**Mert 4 Eylül'de bekleyen 29 sorunun hepsini cevapladı.** Tam liste
[[domain-gereksinimler]]; API'yi bağlayanların gerekçeleri
`02-API/api-kararlar.md` 2026-09-04 altında (10 karar).

**Mert'in bugünkü önceliği kendi makinesinde uçtan uca test.** Kendi cümlesi:
*"ilk istediğim şey benim makinemde ben tam olarak bir test edeyim kullanayım."*
Yayın adımları **bilinçli olarak ertelendi**: *"İlk önce projeyi bitirelim tam
anlamıyla demo test ortamında çalışabilen bir hale getirelim, yayına alacağımız
vakit dediğin entegrasyonları yaparız."*

⚠️ **Bu, "karar bekliyor" ile "hesap bekliyor" ayrımını doğurdu.** İki yayın
engelleyicisi **karar olarak kapandı, eylem olarak açık**:

| Konu | Karar | Bugün eksik olan |
|---|---|---|
| `S-19` ağ topolojisi | API ve Next aynı makinede, `127.0.0.1` yeterli | — kapandı |
| E-posta / SMS | **Postmark + Netgsm** | hesaplar |

Bunlar blocker listesine **girmiyor**, çünkü kimseyi bugün durdurmuyorlar —
yayın günü durduracaklar. Karıştırılırsa pano yanlış aciliyet gösterir.

Bu hükmü güvenli kılan şey ikisinin de **açılış kapısı** olması: hesap yoksa
uygulama açılmıyor, yani yayın günü fark edilmemeleri mümkün değil. **Aynı şey
`S-24` için geçerli değil** — kova izni eksikse uygulama açılır, sessizce kırılır.
Bu yüzden yukarıdaki tabloda ayrıca işaretlendi.

API tarafında 4–5 Eylül'de biten dokuz iş: `A-76` blog uçları · `A-77` favoriler ·
`A-78` bildirim tercihleri · `A-79` (`S-27`) · `A-80` (`S-20`, KDV rezervasyona
donduruldu) · `A-81`/`A-82` veri düzeltmeleri · `A-83` HTML temizleyici ·
`A-84` biniş bileti (`S-25`) · `A-85` iade önizlemesi + `demo-veri.sh`.
**571 test yeşil**, `openapi.json` güncel (backend ölçümü).

**2026-09-04: `S-30` kapandı — blog uç yazılacak.** Mert karar verdi: blog
statik kalmıyor, siteden yazılabilecek. `W-38` artık **karar değil uç bekliyor**
(`Bağımlı: backend ucu`), yani web'in beklediği şey Mert'ten backend'e geçti.
Gerekçe ve elenen alternatif → [[domain-gereksinimler]] 2026-09-04

**Web panosunda kalan dördü hâlâ Mert'te:** `W-39` favori/kupon/bildirim tercihi
(tablo bile yok), `W-40` yolcu listesi (KVKK — blocker 7'ye bağlı), `W-66` biniş
QR'ı (`S-25`), `W-06` `brand.ts` (`G-10`).

30–31 Ağustos'ta kapananlar: `W-37` yönetim paneli, `W-36a`/`W-36b` işletme paneli
gerçek veriye bağlandı ve yazılabilir oldu, `W-39a` hesap sayfası, `W-41` tarih
biçimi, `W-55` tekne detay ucu, `W-61` destek talebi detayı, `W-63` yorum denetimi,
`W-67` destek talepleri, `W-68` kurumsal sayfalardaki uydurma sayılar.

**Yeni yön ilk gününde iki gerçek boşluk buldu** (Mert'in "backend gerçeği
tasarımı yönlendirir" talimatı → [[genel-kararlar]]). İkisinin de bedeli somut:

- **İşletme kendi fiyatını giremiyor.** Tarife bugün yalnız veritabanına elle
  yazılarak oluşuyor; 12 işlemin ekran karşılığı yok (`W-58`).
- **Platform personeli başvuru onaylayamıyor.** Tekne eklemek sözleşmeye bağlı
  olduğu için bu, yeni bir işletmenin sisteme girişini **baştan sona kesiyor**
  (`W-59`).

Kalan dördü: personel yazma tarafı (`W-60`), destek talebi detayı (`W-61`), belge
görüntüleme (`W-62`), yoruma yanıt (`W-63`) → [[web-gorevler]]

Frontend `W-04` **bitti** — web artık gerçek API'ye bağlı; `W-10`, `W-03` (tekne
görselleri) ve `W-55`'in büyük kısmı da 24–28 Ağustos arasında kapandı.

⚠️ **Bu dosya dört gün geride kaldı** (`guncelleme` 24 Ağustos, bugün 28'i) ve bu
sürede 1 numaralı blocker'ı yanlış yere yazılı tuttu. İki hata aynı kökten:
blocker metnini kopyaladım, kaynağa bakmadım — 27 Ağustos'ta katalog uçları için,
28'inde `middleware.ts` için. **Ölçüt kopyalanmaz, yeniden ölçülür.** İkisini de
alan oturumları yakaladı → [[genel-desenler]]

⚠️ **Mert'te bekleyenler — 2026-09-05.** Hiçbiri artık *karar* değil; hepsi
**hesap, metin veya dış teyit**:

| Ne | Neden bekliyor |
|---|---|
| Postmark + Netgsm hesapları | üretimde uygulama bunlarsız **açılmıyor** |
| **Paratika** hesabı (`A-41`) | İyzico'dan Paratika'ya geçildi; para bugün işletmeye gitmiyor |
| S3 / DO Spaces kovası (`S-24`) | ⚠️ **sessiz başarısızlık riski** — açık okuma **iki** öneke verilmezse (`boat-media/*` **ve** `blog-media/*`) blog kapakları kırılır ve uygulama **hiçbir hata üretmez**; hata yalnız tarayıcıda ve nesne deposunda görünür |
| `W-40` aydınlatma metni + saklama süresi | *"onu ben yazıcam en son"* |
| `G-13` mali müşavir teyidi | henüz sorulmadı |
| Veri göçü | ertelendi — önce site ayağa kalksın |

`S-18` ve `S-12` **cevaplandı**, ayrıntı aşağıda.

**2026-09-05'te iki soru daha açıldı:** `S-32` — KDV oranının kaynağı bugün
yapılandırma; Mert **tarihli tabloya taşınsın** dedi, henüz yazılmadı (backend
sırasında). `S-23` — tekne detayında donanım/kural ataması yok, aramada süzgeci
de yok; **ürün sorusu değil, eksik uç.**

**2026-09-04'te dört soru açıldı** (60–63 → [[domain-gereksinimler]]). Biri
diğerlerinden farklı, çünkü ürün sorusu:

- **61 — `Coupons.UserId`.** "Kuponlarım" ekranı **bugünkü şemada ifade edilemiyor**;
  kupon kişiye ait değil. Bu bir uç eksiği değil, kuponun ne olduğuna dair bir
  karar — cevaplanmadan `W-39` yazılamaz.
- **60** — front-end'deki 7 statik blog yazısı veritabanına girecek mi. 4 Eylül
  blog kararının **kapsamadığı** parça; çıkarım yapılmadı, sorulacak.
- **62** blocker 7'nin kendisi · **63** `brand.ts` kurumsal verisi (`W-06`/`G-10`).

**2026-08-31'de iki yeni soru açıldı, ikisi de sayfada duran uydurma sayı**
(ayrıntı → [[web-durum]]):

- `S-26` — `/add-boat` sayfasındaki **"%12 komisyon" ve "3 gün ödeme"** vaatleri.
  İkisi de sözleşme başına tanımlı ve canlı veride **herkes %15'te**. Aynı sayfadaki
  üç "kaptan görüşü" de ad ve şehirle **uydurulmuştu**.
- `S-29` — `brand.ts`'teki **"340+ onaylı tekne"**. Backend geliştirme veritabanını
  ölçtü: **10 yayında tekne, 7 aktif işletme, 2 onaylı yorum** — otuz kat fark. Bu
  ibare **her sayfanın üst şeridinde** duruyor. `W-06`/`G-10` ile zaten Mert'te,
  ama artık kararı verecek sayı ölçülmüş durumda.

Bu ikisi tasarım hatası değil: tasarım yer tutucu koymuştu, **kod onu vaat olarak
yayına taşıdı**. `S-28` cevaplandı — backend ucu yazdı, ekran bağlandı.

⚠️ **2026-08-26'da Mert karar almayı backend oturumuna bıraktı.** O gün alınan
teknik kararlar `02-API/api-benim-kararlarim.md` içinde güven damgasıyla duruyor
ve **topluca onay bekliyor** — onaylanmadan kalıcı sayılmazlar.

Alan ayrıntıları kendi dosyalarında: [[api-durum]] · [[web-durum]]

## 🔴 Blocker'lar

Üçü de iki alanı birden kesiyor; bu yüzden alan dosyalarında değil burada.

| # | Konu | Neden blocker | Kimde |
|---|---|---|---|
| ~~1~~ | ~~**Panel rotaları korumasız — yalnız FRONTEND**~~ | **2026-08-28'de kapatıldı; blocker metni yanlıştı, sonucu değil ölçütü.** "`middleware.ts` yok" cümlesi doğru ama **Next 16'da `middleware.ts` kaldırıldı, adı `proxy.ts` oldu** — dosya var (`src/proxy.ts`), korunan önekler `src/lib/auth/config.ts` içindeki `GUARDED` listesinde (`/admin`+`/support-panel` → `staff`, `/owner-panel` → `owner`, `/account` → giriş yapmış herkes). Jetonlar `httpOnly` çerezde (`dc_at`/`dc_rt`/`dc_role`), süresi dolan jeton proxy'de yenileniyor. Kanıt: web oturumu 28 Ağustos'ta canlı doğruladı — girişsiz `/owner-panel` açılmıyor, girişle açılıyor; ben de dosyaları ve `GUARDED` listesini okudum. ⚠️ `proxy.ts` **yetki sınırı değil**, imza doğrulamıyor, yalnız yönlendiriyor — asıl kapı API'de (`A-42`+`A-44`) ve orada kapalı → [[web-durum]] | — |
| ~~2~~ | ~~**Katalog ve arama uçları yok**~~ | **2026-08-27'de kapatıldı** (`A-33` katalog, `A-34` arama). Kanıt: `SearchController`, `BoatsController`, `PartnerBoatsController`, `PartnerPricingController` ayakta; `/api/search`, `/api/boats`, `/api/partner/boats`, `/api/partner/documents`, `/api/partner/reviews` yolları var. **21 controller · 69 yol · 85 işlem.** "Sisteme tekne girilemiyor, müşteri arayamaz" cümlesi artık doğru değil | — |
| ~~3~~ | ~~**Fiyat sunucuda doğrulanmıyor**~~ | **2026-08-24'te kapatıldı** (`A-04`). `POST /api/pricing/quote` ayakta. Kanıt: istemci `grandTotalTry:1` ve `discountAmountTry:9999` gönderdi, sunucu **1000.00 ve 0** döndü — `QuoteRequest`'te tutar alanı **yok**, yani alanlar reddedilmedi, **hiç okunmadı**. 42 test geçiyor | — |
| ~~4~~ | ~~**Vault'un yedeği yok**~~ | **2026-08-24'te kapatıldı.** `mertagralii/DailyCruising.Vault` (private) oluşturuldu, 117 dosya push edildi. Artık vault'ta yapılan yanlış bir yazma geri alınabilir | — |
| ~~5~~ | ~~**Zamanlanmış iş katmanı yok**~~ | **2026-08-26'da kapatıldı** (`A-15`). `Application/Jobs/IScheduledJob` + `Infrastructure/Jobs/ScheduledJobRunner`, **altı iş** çalışıyor: hold temizliği, teklif süresi, konuşma kapatma, sefer tamamlama, olay günlüğü bölümü, TCMB kuru. `JobHealthController` durumu dışarı veriyor. Sekiz kararın dayandığı katman artık var → [[api-mimari]] | — |
| ~~6~~ | ~~**`Boats.AverageRating` güncellenmiyor**~~ | **2026-08-27'de kapatıldı** (`A-16`). `sync_boat_rating` tetikleyicisi veritabanında kurulu (`20260824134807_A16_TekneOrtalamaPuani`) ve çalışıyor — `AverageRating > 0` olan tekne var. Şemanın "önden hesaplı ↔ canlı hesaplanır" çelişkisi tetikleyiciyle çözüldü | — |
| 7 | **KVKK gerekçesi doğrulanmadı** | **2026-08-27: hâlâ açık, kapsamı daraldı.** Mert 19/20 numaralı sorularda TCKN ve adres için "yer tutucu kalsın" dedi — ödeme adımı kapsam dışı. Ama **yolcu listesi tarafı doğrulanmadı**: kimlik verisi toplamanın tek dayanağı "yolcu listesi ister" anahtarı, şemada yalnız rezervasyona dondurulan kopyası var, kaynak kolon `Boats`/`BoatRentalTypes` listelerinde yok → [[genel-tasiyici-gerekce-taramasi]] | Mert |
| ~~9~~ | ~~**Çift rezervasyon açığı**~~ | **2026-08-26'da açıldı ve aynı gün kapatıldı** (`baf71a7`). `Reservations.IdempotencyKey` **zorunlu**, benzersiz indeksli — `Payments` deseninin aynısı. Kanıt: aynı gövdeyle eşzamanlı iki `curl` → **201/201, aynı kod `XGEZ4GBE`, veritabanında tek satır**; anahtarsız istek **400**; farklı anahtar iki ayrı rezervasyon açıyor. 153 test geçiyor. **Zorunlu seçildi çünkü** isteğe bağlı olsaydı göndermeyi unutan istemci sessizce korumasız kalır, bunu ancak bir müşteri iki kod aldığında fark ederdik → [[api-kararlar]] | — |
| ~~8~~ | ~~Yönetim ve işletme detay ekranları erişilemez~~ | **2026-08-23'te koptu, aynı gün kapatıldı.** 23 yönetim + 3 işletme ekranı geri bağlandı ve tarayıcıda doğrulandı. Sonrasında işletmeye 4 ekran daha eklendi (tekne detayı — tasarımda vardı hiç uygulanmamıştı, fiyatlandırma, menü, yeni tekne başvurusu); işletme tarafı **3 değil 7**, yetim ekran kalmadı → [[web-durum]] | — |

## 🟡 Karara bağlanmamış — genel

Alan-özgü olanlar kendi dosyalarında: [[api-durum]] · [[web-durum]]

⚠️ **2026-08-26'da Mert karar almayı backend oturumuna bıraktı.** O gün alınan teknik
kararlar güven damgasıyla `02-API/api-benim-kararlarim.md` içinde toplanıyor ve
**topluca onay bekliyor** — onaylanmadan kalıcı sayılmazlar.

| Konu | Durum | Not |
|---|---|---|
| ~~Kimlik doğrulama yöntemi~~ | **Karara bağlandı 2026-08-22** | "6 rol" ifadesi eskidir. Roller **veritabanı kaydı**, kodda sabit değil. İki boyut: **ne yapabilir** × **kimin verisinde**. Uygulama görevi `A-03` → [[domain-gereksinimler]] |
| ~~i18n yöntemi~~ | **Karara bağlandı 2026-08-23** | Ayrı **çeviri tabloları** (alan çifti değil). Diller TR/EN/DE/RU; özellik ertelendi ama **şema baştan kurulacak** → [[domain-gereksinimler]] |
| **Dile göre ayrı slug** | Gelecek sürüm | SEO gerekçesi. Mert: *"kesinlikle yapacağız"*. i18n çeviri tabloları kararının uzantısı; şema buna kapatılmayacak → [[domain-gereksinimler]] |
| **"Kararı platform değil tekne sahibi verir"** | Tasarım ilkesi | Ayarlanabilir olan **işletme tarzıdır**; komisyon, iptal politikası ve kupon platformda kalır. Yeni bir ayar eklenirken bu ayrım sorulur → [[domain-gereksinimler]] |
| **`S-12` artık iki alanı birden kesiyor** | Mert'te | Müşteri kaynaklı iptalde iade oranı kararlaşmadı. Bugüne kadar API sorusuydu; iptal e-posta şablonunda `RefundFormatted` ve `RefundDays` yer tutucuları olduğu için **web tarafında da bağımlılık doğdu**. ⚠️ Cevap gelmeden iptal e-postası **gönderilmemeli** — yanlış tutar yazan e-posta geri alınamaz → [[api-durum]] · [[web-durum]] |
| **Testlerde iki bilinçli ad değişikliği** | Mert'te | Yorum dönüşümü sırasında `IyzicoTests`'te **kod** değişti, yorum değil: `Hidden` → `TestSecretKey`, `title` → `header`. İkincisi gerçek çeviri hatasıydı — değişken `Authorization` **başlığını** tutuyor. Backend geri almayı teklif etti, karar Mert'te → [[api-durum]] |
| **`PricingTests`'te tek Türkçe test adı** | Küçük kalem | `Kuponun_bedelini_kim_karsiliyor_teklife_taşiniyor` — diğer bütün test adları İngilizce, bu `ş`/`ı` içeriyor. Kod değişikliği sayıldığı için dokunulmadı |
| **Hata gövdesinde makine-okur `code` alanı** | Web'in cevabı bekleniyor, gelmezse Mert'e | Ölçüldü: **40 yanıt `{ error }`**, **8 yanıt `{ error, code }`** — desen zaten var (`PartnerApplications`, `PartnerDocuments`, `Boarding`), tutarlı değil. `LogReason` etiketleri **19 dosyada** hazır ama controller'lar gövdeye koymuyor, yalnız günlüğe yazıyor. Frontend'in ayrım yapması için Türkçe metne `Contains` atması gerekiyor — o metinler bugün yorum dönüşümünde elden geçti, **kırılgan**. Öneri: `code` eklensin, `error` değişmesin. **Yeni tasarım değil, var olanı tamamlamak** → [[api-durum]] |
| ⚠️ **Arayüzde "işletmeye ödendi" gösterilmemeli** | `A-41` açılana kadar | Para bugün işletmeye **gitmiyor**, transfer elle. Tahsilat platform hesabında, hakediş defterde. `A-41` altında yazılı ama **frontend'i ilgilendiren yüzü orada görünmüyordu** — o cümle bugün yalan → [[web-durum]] |
| Deploy | Karar yok | CI/CD, hosting, ortam yönetimi konuşulmadı |
| **Sezonluk AI analiz raporları** | Gelecek sürüm | ⚠️ **Analiz ertelenir, VERİ TOPLAMA ertelenemez** — olay günlüğü şemaya bugün girmeli, geçmişe dönük üretilemez → [[domain-gereksinimler]] |
| **AI otomasyonları** | Gelecek sürüm | E-postaya kişiye göre otomatik cevap, haftalık otomatik blog yazısı → [[domain-gereksinimler]] |
| **Sefer devri (charter için yer açma)** | Gelecek sürüm | Paylaşımlı rezervasyon sahibine tam iade + kupon + öncelik teklif edip seferi charter'a açma. Mert: *"bunu kesinlikle ekleyeceğiz"*. İlk sürümde yok ama şema buna kapatılmayacak → [[domain-gereksinimler]] |
| **ECC Memory katmanı yerini hak ediyor mu** | Kuruldu, kullanılmıyor | Tek faydası harness'lar arası devir (Codex/Cursor). Sadece Claude Code kullanılıyorsa atıl bir global npm bağımlılığı + klasör. Başka harness planı yoksa kaldırılmalı → [[genel-kararlar]] |

## 🟢 Tamamlananlar

- **2026-08-27: Yorum → `#region` + XML doc dönüşümü bitti.** `src/` 231 + `tests/` 46 = **277 dosya**. Kanıt: `dotnet test` → **441/441 yeşil, 0 hata**; `Migrations/` hariç serbest `//` yorum taraması **0** (403 eşleşmenin tamamı EF'in ürettiği `Designer.cs` ve elle yazılan migration SQL yorumları — dönüştürülmemesi doğru). Backend `007e4e1`'e kadar push edildi, 94 commit

- Backend iskeleti kuruldu, `dotnet build` 0 uyarı/0 hata
- `GET /api/health` doğrulandı → `{"status":"healthy"}`
- Frontend iskeleti kuruldu, 19 ekran uygulandı ve `origin/main`'e alındı
- İki private repo oluşturuldu ve push edildi
- Bu vault + hafıza sistemi kuruldu (hook'lar, panolar, doğrulayıcı, 3 projeye özel skill)

## ⚠️ Vault ↔ kod çelişkileri

**2026-09-05 — para kuralı tek dilim üzerinden sorulunca sınırda bozuluyordu.**
`S-12`'ye *"komisyon tam alınsın"* cevabı geldi; backend sayıyla baktığında **%100
iade diliminde işletmeyi komisyon kadar eksiye** düşürdüğü ve `CK_Payouts_Amount >= 0`
kısıtı yüzünden **sonraki turun hakedişini de kilitlediği** çıktı. Uygulanmadı,
geri soruldu, cevap **(c) orantılı** olarak değişti ve kod olduğu gibi kaldı.
Ders: bir para kuralı **tek dilim üzerinden** sorulursa cevap o dilimde doğru,
**sınırlarda yanlış** olabilir — sormadan önce uç değerlerle sayılaştır
→ [[genel-desenler]]

**2026-09-05 — kendi notunun tarihi, notun hâlâ doğru olduğunu göstermez.**
`api-benim-kararlarim.md`'de 26 Ağustos tarihli *"reddetme ucu YOK"* notu
duruyordu; ölçüldüğünde **uç ve yedi testi vardı** — arada başka bir oturum
yazmış. Eşzamanlı oturumlarda **kendi notun da başkasının notu kadar bayatlar**;
tarih tazelik değil, yalnız yazılma anıdır.

**2026-08-31 — ham katalog anahtarı ana sayfada görünüyor.** `a04-gulet` gibi
tohum çöpü artık müşteriye açık ekranda; istemciye "anahtar gibiyse gizle" sezgisi
**kasten konmadı** — gizlemek sorunu görünmez yapardı, veriyi düzeltmez. `S-22`
olarak Mert'te → [[web-durum]]

**2026-08-31 — `durum.md`'nin ölçü tablosu `acilis.md` ile çelişiyordu.** Tablo
*21 controller · 69 yol* diyordu, açılış *28 · 93 · 42*. Aynı dosyada iki ölçüm
tutulunca biri mutlaka bayatlıyor; tablo ölçülenle değiştirildi. Blocker 2'nin
arşiv satırındaki "21 controller" **kasten bırakıldı** — o, 27 Ağustos'ta doğru
olan tarihli bir kanıttır, güncel iddia değil.

**2026-08-31 — `genel-gorevler.md`'de yinelenen boş başlık bulundu.** İki adet
`## 🔵 Yapılacak` vardı; ikincisine yazılan bir görev panodan sessizce düşerdi.
Artığı **kendi taşıma betiğim** bırakmış. Kontrol 17 görmedi çünkü yalnız
maddelere bakıyor, bölüm yapısına bakmıyordu — `dogrula.py` **kontrol 18** eklendi,
iki yönde de sınandı → [[genel-desenler]]

**2026-08-31 — `a1d6689` commit gövdesinde yanlış sayı duruyor.** Backend
"485 test" yazdı, ölçüm **484**'tü; sayı çalıştırılmadan önce yazılmış. Commit
amend edilmedi — paylaşılan dalda geçmiş yeniden yazmak bir sayı için orantısız
bulundu, kapı da durdurdu. **Doğrusu 484 ve test sayısı artmadı**, mevcut bir test
düzeltildi. Bu satır o commit'in düzeltmesidir; `a1d6689`'u okuyan buraya baksın.

**2026-08-31 — "susan denetim" beşinci kez çıktı, üç ayrı katmanda.** Kontrol 15
(muafiyetle susuyordu), `Coupon_below_the_share_can_be_created` (iddiası örtüktü:
"patlamadıysa geçmiştir" — satırın yazılmasıyla yazma çağrısının sessizce hiçbir
şey yapmamasını ayırt edemiyordu; düzeltildi, `a1d6689`), `publiclyReadable`, hız
sınırı bölümlemesi, üretim kapıları. Beşi de tek bir soruyla bulundu: **"bu kontrol
çalışmasaydı ne farklı görünürdü?"** → [[genel-desenler]] "Bir kontrolün varlığı,
çalıştığının kanıtı değil"

**2026-08-31 — `api-mimari.md` ikinci kez çürümüştü, denetim susmuştu.**
Dosya *21 controller · 69 yol · 39 migration* diyordu; gerçek **28 · 93 · 42**.
Daha kötüsü, içindeki *"HÂLÂ YOK ve ürün bunlarsız çalışmıyor"* listesi katalog,
arama, yorumlar, mesajlaşma, teklifler, destek talepleri, hakediş ve platform
yönetim panelini sayıyordu — **sekizi de yazılmıştı.** Bu, `CLAUDE.md`'de
kayıtlı 26 Ağustos olayının **aynı dosyada birebir tekrarı**.

Asıl bulgu şu: **kontrol 15 bunu ölçmek için vardı ve sustu.** İçindeki
"dosya kirliyse taze say" muafiyeti, alan oturumlarının vault'a yazıp commit
atmaması yüzünden kalıcı hâle gelmişti. Muafiyet kaldırıldı — kirli dosyada
ölçüt artık `mtime`. Düzeltilir düzeltilmez ikinci gerçek bulguyu verdi:
`web-mimari.md` 28 Ağustos'tan beri yazılmamış, front-end'de **67 kaynak dosya**
eklenmiş/silinmiş. Backend `api-mimari.md`'yi düzeltti; `web-mimari.md` web
oturumunda → [[genel-desenler]] "Muafiyet kalıcı olduğu yerde kör nokta olur"

Yan bulgu, uç eksiği değil **şema sorusu**: "kuponlarım" ekranı yazılamıyor
çünkü `Coupons` tablosunda `UserId` kolonu yok — kupon kişiye ait değil. `W-39`
bu yüzden açık.

**2026-08-31 — mock veri, kodun kendi hatasını gizliyordu.** Web'in kısa tarih
biçimi **yılı atlıyordu**; tasarımdan gelen sahte kayıtların hepsi aynı yıl olduğu
için hata hiç görünmedi. Gerçek uca bağlanır bağlanmaz `2027-06-17` kalkışlı bir
tur listede "17 Haz" görünüp **geçmiş sanıldı**. Aynı gün backend yapısal olarak
aynı şeyi yaşadı: olay günlüğü `200` dönüyordu ama yük boş kalıyordu. Ortak ders
[[genel-desenler]]'e yazıldı → [[web-mock-hatayi-gizler]]

**2026-08-31 — pano tarihleri ile takvim ayrıştı.** `03-Web/web-gorevler.md` ve
`web-durum.md` frontmatter'ında `guncelleme: 2026-08-28` yazıyor, oysa içindeki
görev satırları `2026-08-30`/`2026-08-31`. Uzun süren bir oturumun "bugün"ü
başladığı gün donuyor. **Tarih yazan her satır takvimden okunmalı**, oturumun
belleğinden değil. Düzeltme web oturumunda (kendi alanı).

**2026-08-28 — panel ucu ile müşteri ucu ayrışmış.**
`GET /api/partner/boats/{id}/rental-types` yanıtında `rentalTypeKey` var ama
**`name` yok**; müşteri tarafındaki `GET /api/boats/{slug}` çevrilmiş `name`
döndürüyor. Fiyat ekranı bugün yazılsa işletmeye `gunluk-tekne` diye ham anahtar
gösterirdi. Aynı yanıtta bilinen iki eksik duruyor: `extras[].name` boş, `program`
null. `W-58`'in ek hizmet yarısı **ad gelmeden kurulamaz**. Web bunu doğrudan
backend oturumuna bildirdi.

**2026-08-28 — "web tarafında yapılabilir iş kalmadı" cümlesi yanlıştı.**
`03-Web/web-durum.md`'de duruyordu; web oturumu düzeltti. Cümle yanlış değil
**ölçülmemişti** — pano boş olduğu için "iş yok" sanılmıştı, oysa 21 yolun
karşılığı hiç panoya girmemişti. Panonun boş olması işin bittiğini göstermez,
yalnızca **panoya yazılmadığını** gösterir.

**2026-08-27 — iki ölçüm tuzağı, ikisi de kayda değer.**

**1. "Serbest yorum 0" kapsam bağımlıydı.** Backend "0" dedi, bağımsız taramam **403**
buldu. Çelişki değil, kapsam farkıydı: 403'ün tamamı `Migrations/` altında. İleride
aynı sayı yeniden ölçülürse **kapsamı da yazmak zorunlu** — çıplak bir sayı iki
oturumu boşuna karşı karşıya getiriyor.

**2. `EventLogTests`'in kod-only doğrulaması zayıf.** Dosyadaki ham SQL dizesi
tokenizer'ı şaşırtıyor, bazı `///` satırları fark gibi görünüyor. Backend satır
bazlı ikinci süzgeçle doğruladı (kod birebir aynı) ama **o süzgeç aynı satır
içindeki değişikliği yakalayamaz.** Yani bu dosyada "kod değişmedi" güvencesi
diğerlerinden zayıf — betik iyileştirilmeli.

⚠️ **GateGuard `truncate`/`TRUNCATE` kelimesini yıkıcı sayıyor.** İki test dosyası
(`EventLogTests`, `PartnerStaffTests`) heredoc ile yazılamadı, `Write` aracı ve yer
tutucu ile yazılmak zorunda kaldı. Aracın kendisi değil **kelimesi** tetikliyor →
[[genel-gateguard-davranisi]]


**2026-08-26 — `dogrula.py` TEMİZ.** Kontrol 15 (mimari bayatlığı) bugün eklendi, iki
gerçek bulgu üretti, ikisi de aynı gün kapandı:

| Dosya | Bulgu | Sonuç |
|---|---|---|
| `02-API/api-mimari.md` | 194 dosya eklendi/silindi; "iş uç noktası hâlâ yok" derken 8 controller vardı | backend düzeltti — 75 entity, 19 migration, 27 uç nokta, zamanlanmış işler ve dış servisler eklendi |
| `03-Web/web-mimari.md` | 87 dosya; rota envanteri "sadece `/`" diyordu | web oturumu düzeltti — dosya listesi yerine **katman** yazıldı |

Sebep disiplin hatası değil, kuralda boşluktu: `*-mimari.md` ne okuma ne yazma
tablosundaydı → [[genel-desenler]] "Tetikleyicisi olmayan dosya çürür". Boşluk
`CLAUDE.md` + `acilis.md`'de kapatıldı, denetimi kontrol 15 yapıyor.

**Kontrol ilk gününde üçüncü bir şey buldu:** düzeltme için dosya açılınca ölü bir uç
nokta çıktı — `GET /api/auth/yetki-denemesi`, *"geçici, A-03 bitince kaldırılacak"*
yorumuyla yazılmış, koşul gerçekleştiği hâlde ayakta kalmıştı. Kaldırıldı, 146 test
geçiyor. Kuralın değeri bakmayı zorlamasından geliyor →
[[genel-desenler]] "Koşullu geçici şeyin koşulu panoya yazılır"

**Dokuzuncu "build temiz ≠ görünüm doğru" örneği:** `rounded-circle` beş yerde ölü
sınıftı — `--r-circle` `:root`'ta vardı ama `@theme inline`'a bağlanmamıştı,
`border-radius: 0` üretiyordu. **Build, lint ve tip denetimi üçü de temiz geçti** →
[[web-baglanmamis-token-tuzagi]]

## Delete-zone — bilerek silinenler

Bunları **geri getirme**; sebebi burada.

| Ne silindi | Neden | Yerine |
|---|---|---|
| `WeatherForecast.cs`, `WeatherForecastController.cs` | .NET şablonunun örnek kodu | `HealthController.cs` |
| `Class1.cs` (3 katmanda) | Şablon dolgusu | — (katmanlar bilinçli boş) |
| `CLAUDE.md`, `AGENTS.md` (frontend repo) | Mert repoda AI aracı dosyası istemiyor | Kökteki `CLAUDE.md` (repo dışı) |
| Kökteki geçici git reposu | İki bağımsız repo kararı | Alt klasörlerdeki iki repo |

İlgili: [[proje]] · [[genel-kararlar]] · [[genel-gorevler]] · [[api-durum]] · [[web-durum]] · [[00-Index]]
