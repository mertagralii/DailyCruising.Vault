---
rol: status
kapsam: genel
guncelleme: 2026-08-28
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
| API | 3 | 74 |
| Web | 11 | 33 |
| Genel | 6 | 9 |

Backend'de Mert'in kararına bağlı olmayan iş kalmadı; kalan üçün ikisi `A-41`'e
bağlı, üçüncüsü (`A-07`) frontend alanı.

| Alan | Ölçü |
|---|---|
| API | 21 controller · 69 yol · 85 işlem · 106 tablo · 39 migration → [[api-mimari]] |
| Web | 25 rota · rota koruması (`proxy.ts`) çalışıyor · gerçek API'ye bağlandı (`W-04`) → [[web-mimari]] |

Ödeme uçtan uca çalışıyor: **gerçek İyzico sandbox'ına karşı** rezervasyon →
ödeme → geri dönüş → `Paid`, ve iade → `Refunded`, defter 0.00 kapanıyor (`A-29`).

**Kritik yol artık tek düğümde:** `A-41` (alt üye iş yeri ve hakediş transferi).
Bugün tahsilat **platform hesabına** yapılıyor, hakediş defterde duruyor ama
işletmeye para geçmiyor. `A-58` de buna bağlı.

Frontend `W-04` **bitti** — web artık gerçek API'ye bağlı; `W-10`, `W-03` (tekne
görselleri) ve `W-55`'in büyük kısmı da 24–28 Ağustos arasında kapandı.

⚠️ **Bu dosya dört gün geride kaldı** (`guncelleme` 24 Ağustos, bugün 28'i) ve bu
sürede 1 numaralı blocker'ı yanlış yere yazılı tuttu. İki hata aynı kökten:
blocker metnini kopyaladım, kaynağa bakmadım — 27 Ağustos'ta katalog uçları için,
28'inde `middleware.ts` için. **Ölçüt kopyalanmaz, yeniden ölçülür.** İkisini de
alan oturumları yakaladı → [[genel-desenler]]

⚠️ **Mert'te bekleyen kararlar:** `A-41` (İyzico pazaryeri) · `S-18` (kupon
kırpma çelişkisi, `S-10` ile `S-15` birbirini bozuyor) · `S-12` (müşteri
kaynaklı iptalde iade oranı — iptal e-postasını da kilitliyor).

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
