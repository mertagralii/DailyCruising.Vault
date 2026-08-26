---
rol: status
kapsam: genel
guncelleme: 2026-08-24
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

**Tasarım bitti, şema bitti, uç noktalar başlamadı.** Frontend'de 19 ekranın
tamamı uygulanıp ölçüldü ve `origin/main`'e alındı. Backend'de veritabanı şemasının
sekiz bölümü de çıkarıldı ve Mert'in onayından geçti.

Şema `main`'e birleştirildi (`8bbb04f`, `c5b4b87`), dal silindi.

**Kritik yol:** rezervasyon oluşturma ucu (`A-22`) → zamanlanmış iş katmanı
(`A-15`, 5 numaralı blocker) → kimlik doğrulamanın kalanı (`A-03`) → frontend'in
gerçek veriye bağlanması (`W-04`).

`A-04` bitti ama **`PricingService`'i çağıran bir uç henüz yok** — fiyat
hesaplaması yazıldı, kullanılmıyor. `A-22` bu yüzden sırada.

⚠️ **Mert'in cevabını bekleyen sekiz soru var** (`S-1`…`S-8`) → [[api-durum]].
Son ikisi varsayımla ilerlendi: kuponun matrahı (tur + ek hizmet varsayıldı) ve
fiyat ucunda hız sınırı (dakikada 60 kondu, onaylanmadı).

Alan ayrıntıları kendi dosyalarında: [[api-durum]] · [[web-durum]]

## 🔴 Blocker'lar

Üçü de iki alanı birden kesiyor; bu yüzden alan dosyalarında değil burada.

| # | Konu | Neden blocker | Kimde |
|---|---|---|---|
| 1 | **Kimlik doğrulama yok** | `/admin`, `/owner-panel`, `/support-panel`, `/account` **herkese açık**. Gerçek veriye bağlanmadan önce mutlaka kapatılmalı — bu bir güvenlik açığı | Beraber |
| 2 | **İş uç noktası yok** | **Şema bitti** (2026-08-24, 75 tablo, `feat/veritabani-semasi` dalında `8bbb04f`) ama iş uç noktası hâlâ yok — yalnız `/api/health` ve `/openapi/v1.json`. Arayüz `src/lib/data/*.ts` mock verisiyle çalışıyor. **Blocker duruyor, sebebi değişti** → [[api-durum]] | Beraber |
| ~~3~~ | ~~**Fiyat sunucuda doğrulanmıyor**~~ | **2026-08-24'te kapatıldı** (`A-04`). `POST /api/pricing/quote` ayakta. Kanıt: istemci `grandTotalTry:1` ve `discountAmountTry:9999` gönderdi, sunucu **1000.00 ve 0** döndü — `QuoteRequest`'te tutar alanı **yok**, yani alanlar reddedilmedi, **hiç okunmadı**. 42 test geçiyor | — |
| ~~4~~ | ~~**Vault'un yedeği yok**~~ | **2026-08-24'te kapatıldı.** `mertagralii/DailyCruising.Vault` (private) oluşturuldu, 117 dosya push edildi. Artık vault'ta yapılan yanlış bir yazma geri alınabilir | — |
| 5 | **Zamanlanmış iş katmanı yok** | Sekiz karar buna dayanıyor ve hiçbirinde adı geçmiyor. Kodda `IHostedService`/`BackgroundService`/`Hangfire`/`Quartz` **sıfır sonuç**. Çöküş sessiz değil **satışı durdurucu**: süresi dolmayan hold `CHECK (SoldSeats <= Capacity)` yüzünden koltukları kalıcı kilitler, süresi dolmayan teklif seferi `EXCLUDE` kısıtı yüzünden tarihi sonsuza kadar kapatır. **Şemanın en güçlü iki garantisi, iş katmanı yokken sistemi kilitleyen mekanizmalara dönüşüyor** → [[genel-tasiyici-gerekce-taramasi]] | Claude |
| 6 | **`Boats.AverageRating` güncellenmiyor** | Şema iki bölümde **zıt** söylüyor: "önden hesaplı" ↔ "canlı hesaplanır". Güncelleyen yok. Alan `0` kalır, puan filtresi her teknede aynı değeri görür; `IX_Boats_Search` sayesinde **hızlı çalışır ve hata vermez** — sessiz yanlış sonuç → [[genel-tasiyici-gerekce-taramasi]] | Claude |
| 7 | **KVKK gerekçesi doğrulanmadı** | Kimlik verisi toplamanın tek hukuki dayanağı "yolcu listesi ister" anahtarı; şemada yalnız rezervasyona dondurulan **kopyası** var, kaynak kolon `Boats`/`BoatRentalTypes` listelerinde yok. Yoksa ya hiç istenmez ya herkesten istenir — ikisi de gerekçeyi çökertir → [[genel-tasiyici-gerekce-taramasi]] | Claude |
| ~~8~~ | ~~Yönetim ve işletme detay ekranları erişilemez~~ | **2026-08-23'te koptu, aynı gün kapatıldı.** 23 yönetim + 3 işletme ekranı geri bağlandı ve tarayıcıda doğrulandı. Sonrasında işletmeye 4 ekran daha eklendi (tekne detayı — tasarımda vardı hiç uygulanmamıştı, fiyatlandırma, menü, yeni tekne başvurusu); işletme tarafı **3 değil 7**, yetim ekran kalmadı → [[web-durum]] | — |

## 🟡 Karara bağlanmamış — genel

Alan-özgü olanlar kendi dosyalarında: [[api-durum]] · [[web-durum]]

| Konu | Durum | Not |
|---|---|---|
| ~~Kimlik doğrulama yöntemi~~ | **Karara bağlandı 2026-08-22** | "6 rol" ifadesi eskidir. Roller **veritabanı kaydı**, kodda sabit değil. İki boyut: **ne yapabilir** × **kimin verisinde**. Uygulama görevi `A-03` → [[domain-gereksinimler]] |
| ~~i18n yöntemi~~ | **Karara bağlandı 2026-08-23** | Ayrı **çeviri tabloları** (alan çifti değil). Diller TR/EN/DE/RU; özellik ertelendi ama **şema baştan kurulacak** → [[domain-gereksinimler]] |
| **Dile göre ayrı slug** | Gelecek sürüm | SEO gerekçesi. Mert: *"kesinlikle yapacağız"*. i18n çeviri tabloları kararının uzantısı; şema buna kapatılmayacak → [[domain-gereksinimler]] |
| **"Kararı platform değil tekne sahibi verir"** | Tasarım ilkesi | Ayarlanabilir olan **işletme tarzıdır**; komisyon, iptal politikası ve kupon platformda kalır. Yeni bir ayar eklenirken bu ayrım sorulur → [[domain-gereksinimler]] |
| Deploy | Karar yok | CI/CD, hosting, ortam yönetimi konuşulmadı |
| **Sezonluk AI analiz raporları** | Gelecek sürüm | ⚠️ **Analiz ertelenir, VERİ TOPLAMA ertelenemez** — olay günlüğü şemaya bugün girmeli, geçmişe dönük üretilemez → [[domain-gereksinimler]] |
| **AI otomasyonları** | Gelecek sürüm | E-postaya kişiye göre otomatik cevap, haftalık otomatik blog yazısı → [[domain-gereksinimler]] |
| **Sefer devri (charter için yer açma)** | Gelecek sürüm | Paylaşımlı rezervasyon sahibine tam iade + kupon + öncelik teklif edip seferi charter'a açma. Mert: *"bunu kesinlikle ekleyeceğiz"*. İlk sürümde yok ama şema buna kapatılmayacak → [[domain-gereksinimler]] |
| **ECC Memory katmanı yerini hak ediyor mu** | Kuruldu, kullanılmıyor | Tek faydası harness'lar arası devir (Codex/Cursor). Sadece Claude Code kullanılıyorsa atıl bir global npm bağımlılığı + klasör. Başka harness planı yoksa kaldırılmalı → [[genel-kararlar]] |

## 🟢 Tamamlananlar

- Backend iskeleti kuruldu, `dotnet build` 0 uyarı/0 hata
- `GET /api/health` doğrulandı → `{"status":"healthy"}`
- Frontend iskeleti kuruldu, 19 ekran uygulandı ve `origin/main`'e alındı
- İki private repo oluşturuldu ve push edildi
- Bu vault + hafıza sistemi kuruldu (hook'lar, panolar, doğrulayıcı, 3 projeye özel skill)

## ⚠️ Vault ↔ kod çelişkileri

**2026-08-26 — `dogrula.py` şu an 2 bulgu veriyor, bu beklenen durumdur.**

Kontrol 15 (mimari bayatlığı) bugün eklendi ve iki gerçek bulgu üretti:

| Dosya | Beyan | Koddaki gerçek |
|---|---|---|
| `02-API/api-mimari.md` | `guncelleme: 2026-08-24`, "iş uç noktası hâlâ yok", 8 migration, 74 entity | 8 controller, 19 migration, 75 entity, 194 dosya eklendi/silindi |
| `03-Web/web-mimari.md` | `guncelleme: 2026-08-21` | 87 dosya eklendi/silindi |

**Bu dosyalar alan oturumlarına aittir** — vault oturumu içeriklerini düzeltmez, yalnız
bildirir. İkisine de `SendMessage` gönderildi. Düzeltilene kadar `dogrula.py` kırmızı
kalır; **kırmızı doğrudur, susturulmaz.**

Sebep bir disiplin hatası değil, kuralda boşluktu → [[genel-desenler]] "Tetikleyicisi
olmayan dosya çürür". Boşluk `CLAUDE.md`'de kapatıldı (okuma + yazma tetikleyicisi).


Bir not koda aykırı çıkarsa buraya yazılır; sessizce düzeltilmez.

| Tarih | Not | Çelişki | Çözüm |
|---|---|---|---|
| 2026-08-24 | [[domain-gereksinimler]] — "Cevap bekleyenler" tablosu | Tablo 35b/38/39/40/41'i **açık** gösteriyordu; beşi de 22–23 Ağustos'ta cevaplanmış, cevaplar **aynı dosyanın gövdesinde** duruyordu. Dosya kendi kendisiyle çelişiyordu; iki oturum bunları blocker sandı | Tablo 2026-08-24'te kapanış yerleriyle yeniden yazıldı. `dogrula.py` bunu **yakalayamaz** (semantik çelişki); korunma yolu `domain-karari` skill'i — cevap geldiğinde tabloyu aynı turda düşürür |
| 2026-08-22 | [[proje]] — "davranışı tersine mühendislikle çıkarılmış bir şartnameyle belgelendi" | Belge diskte **yok**; `~/Desktop`, `~/Documents`, `~/Downloads` ve proje klasörü tarandı. Bu dosyaya yapılan "PRD 14. kural" türü atıflar dayanaksız | Backend sıfırdan tasarlanacak → [[api-kararlar]] 2026-08-22. İş tanımı geçerli, davranış atıfları doğrulanmamış sayılır |

## Delete-zone — bilerek silinenler

Bunları **geri getirme**; sebebi burada.

| Ne silindi | Neden | Yerine |
|---|---|---|
| `WeatherForecast.cs`, `WeatherForecastController.cs` | .NET şablonunun örnek kodu | `HealthController.cs` |
| `Class1.cs` (3 katmanda) | Şablon dolgusu | — (katmanlar bilinçli boş) |
| `CLAUDE.md`, `AGENTS.md` (frontend repo) | Mert repoda AI aracı dosyası istemiyor | Kökteki `CLAUDE.md` (repo dışı) |
| Kökteki geçici git reposu | İki bağımsız repo kararı | Alt klasörlerdeki iki repo |

İlgili: [[proje]] · [[genel-kararlar]] · [[genel-gorevler]] · [[api-durum]] · [[web-durum]] · [[00-Index]]
