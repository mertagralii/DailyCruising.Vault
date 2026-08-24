---
rol: not
kapsam: genel
guncelleme: 2026-08-24
durum: guncel
---

# Taşıyıcı gerekçe taraması — 2026-08-24

`**Dayanak:**` biçimi konduktan sonra **zaten dağılmış** kopyaları bulmak için
yapılan tek seferlik tarama. Vault'un tamamı okundu (`domain-gereksinimler` 1.482
satır, `api-sema` 983 satır dahil). 10 bulgu çıktı.

**Taşıyıcı gerekçe:** "X ertelenebilir / ucuz / gerekmiyor, **çünkü Y var**" — Y
kalkarsa X sessizce çöker → [[genel-desenler]]

## 🔴 Bulgu 1 — Zamanlanmış iş katmanı yok, sekiz karar ona dayanıyor

**Doğrulandı:** kodda `IHostedService`, `BackgroundService`, `Hangfire`, `Quartz`
araması **sıfır sonuç** verdi.

Ona dayanan kararlar, hiçbirinde adı geçmeden:

| Karar | Nerede |
|---|---|
| Hold 15 dakika sonra koltukları iade eder | `domain-gereksinimler` |
| Teklif süresi dolunca tarih serbest kalır | `domain-gereksinimler` |
| Konuşma tur tarihi geçince kapanır | `domain-gereksinimler` |
| Kalkıştan 24 saat önce hatırlatma gider | `domain-gereksinimler` |
| Kurlar TCMB'den günlük çekilir | `domain-gereksinimler` + `api-sema` |
| Sözleşme süresi dolunca uyarı gider | `api-sema` |
| Süre dolunca sefer İptal'e çekilir | `api-sema` |
| Hakediş iki haftada bir | `api-kararlar` |

**Çöküş biçimi sessiz değil, satışı durdurucu:**

- Süresi dolmayan hold, `CHECK (SoldSeats <= Capacity)` yüzünden koltukları
  **kalıcı kilitler** — o sefer bir daha satılamaz
- Süresi dolmayan `VoyageType=Teklif` seferi, `EXCLUDE` kısıtı yüzünden o tarihi
  **sonsuza kadar kapatır**
- `ExchangeRates` boş kalırsa dövizli tekne satılamaz

⚠️ **Şemanın en güçlü iki garantisi, iş katmanı yokken sistemin kendisini
kilitleyen mekanizmalara dönüşüyor.** `A-14` yalnız bölüm oluşturmayı kapsıyor,
bunları değil.

**Terim farkı:** "süre dolar" · "otomatik kapanır" · "günlük çekilip saklanır" ·
"temizlik işi" · "zamanlanmış iş yok" — beş terim, hiçbiri `grep` ile diğerini
bulmuyor.

## 🔴 Bulgu 2 — "Terk edilen ödeme tetikleyicisi zaten şemada var" — yok

`domain-gereksinimler` özelliği "ucuz" sayıyor, *"AI bile gerekmez"* diyor.
Dayandığı `Beklemede → SüresiDoldu` tetikleyicisi **mevcut değil**; sayılan beş
tetikleyicinin hiçbiri durum geçişi üretmiyor. Zaten veritabanı tetikleyicisi
**zamanla kendiliğinden ateşlenmez** — Bulgu 1'e bağlı.

## 🔴 Bulgu 3 — `Boats.AverageRating` "önden hesaplı" ama kimse hesaplamıyor

Aynı dosyanın iki bölümü **zıt** söylüyor: bölüm 2 *"önden hesaplı"*, bölüm 8
*"canlı hesaplanır, önden tutulmaz"*. Güncelleyen tetikleyici veya servis yok.

**Sessiz yanlış sonuç:** alan `0` kalır, puana göre sıralama ve "puan" filtresi
**her teknede aynı değeri** görür. `IX_Boats_Search` eklendiği için sorgu **hızlı
çalışır ve hata vermez** — en geç fark edilecek tür.

## 🟡 Bulgu 4 — KVKK gerekçesi olan "yolcu listesi ister" anahtarı şemada yok

Kimlik verisi (TCKN/pasaport) toplamanın tek hukuki gerekçesi bu anahtar. Şemada
yalnız **rezervasyona dondurulan kopya** (`RequiresPassengerList`) var; `Boats` ve
`BoatRentalTypes` kolon listelerinde kaynak kolon **yok**. Kopyanın kaynağı belirsiz.

Yoksa: ya yolcu listesi hiç istenmez ya herkesten istenir — ikisi de KVKK
gerekçesini çökertir. **Koda bakılıp teyit edilmeli.**

## 🟡 Bulgu 5 — Ölçüme bağlanan eşik, ölçüm altyapısı olmadan

`AvailabilityDays` ertelemesi *"p95 gecikme 300 ms'i aştığında geri dönülür,
tahminle değil ölçümle"* diyor. Ama APM/metrik/izleme kararı **yok**, deploy bile
karara bağlanmamış (`G-07`). Ölçen kimse yoksa eşik **hiç tetiklenmez**; erteleme
sessizce kalıcı olur. Bulgu 3 de aynı gerekçeye yaslanıyor — **zincirleme kullanım**.

## 🟡 Bulgu 6 — Slug ertelemesi 301 yönlendirmeye dayanıyor, mekanizma bilinçli kurulmadı

Dile göre slug *"şemayı bozmuyor, eskisi 301'e dönüşür"* diyor. Ama `web-kararlar`
İngilizce rota kararında **tam tersini** yazıyor: *"sonradan yapılsaydı yönlendirme
tablosu gerekirdi"* — yani bilerek yapılmadı. `Boats.Slug` tek ve benzersiz,
**geçmiş tutulmuyor**; `Redirects`/`SlugHistory` yok.

⚠️ Bu **dile göre slug'ı beklemeden** geçerli: bugün bir teknenin slug'ı değişirse
eski adres sessizce 404 olur.

## 🟡 Bulgu 7 — SaaS "karar ertelendi" değil, birinci yol sessizce seçilmiş

*"Bugün hiçbir şey gerektirmiyor"* ifadesi **abone başına ayrı veritabanı** yolunu
varsayıyor. Metnin kendisi ikinci yolun *"sonradan eklenirse çok pahalı"* olduğunu
kabul ediyor. Yani ikinci yola geçme ihtimali korunmuyor ama bu bir karar olarak
hiçbir yerde yazılı değil.

## 🟡 Bulgu 8 — Komisyon geri istenmemesi hakediş periyoduna dayanıyor

Periyot kolonu (`Contracts.PayoutPeriodDays`) şemanın kolon listesinde **yok**
(liste "kritik kolonlar" ile sınırlı olduğu için kesin değil, doğrulanmalı).
Periyodu fiilen işleten iş **Bulgu 1'e bağlı** — hakediş dönemini kapatan
zamanlanmış iş yok.

## 🟡 Bulgu 9 — Şema "olaylar kaydediliyor" diyor, hiçbir olay kaydedilmiyor

Sekiz bölümün her biri geniş zamanlı *"bu bölümde hangi olaylar kaydediliyor"*
başlığı taşıyor. `A-08` dürüstçe *"hiçbir olay henüz yazılmıyor"* diyor.

Bugün risk düşük (uç nokta yok, kaybedilen veri yok) — ama `A-08` ilk iş uç
noktasıyla **aynı anda** yapılmazsa ilk gerçek trafiğin olayları kalıcı kaybolur.

## 🟢 Bulgu 10 — SMS'e dayanan dört akış, sağlayıcı kararı açık

Telefonun zorunlu alan olmasının tek dayanağı çalışan bir SMS sağlayıcısı; `G-04`
açık ve eski sistemde IP whitelist hatası veriyordu. Şema sağlayıcıdan bağımsız
kurulmuş (`NotificationDeliveries`) — **bu iyi**, risk düşük.

## Ayrıca: iki bayat ifade

- `api-mimari.md` — Domain/Application/Infrastructure *"boş"* diyor. Gerçek: 74
  entity, 12 yapılandırma, 7 migration. **Yapılmışı yapılmamış gösteriyor**, ters
  yönde bayatlama
- `durum.md` — *"ana dala birleştirilmedi"* diyordu. Gerçek: `main`'e birleşti
  (`8bbb04f`, `c5b4b87`), dal silindi. **Aynı gün düzeltildi**

İlgili: [[genel-desenler]] · [[durum]] · [[api-durum]] · [[genel-notlar]]
