---
rol: status
kapsam: api
guncelleme: 2026-08-24
durum: guncel
---

# API Durumu

> **Bu dosyanın sahibi `DailyCruising.Back-End/` içinde çalışan oturumdur.**
> API tarafının güncel durumu buraya yazılır; `01-Genel/durum.md`'ye **yazılmaz**.
> Genel dosya bu dosyayı özetler → [[durum]]

## Nerede duruyoruz

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

## ❓ Mert'e sorulacaklar

Gözetimsiz çalışırken karara bağlanamayan noktalar. Hiçbiri tahminle
kapatılmadı; belgelenmiş bir varsayımla ilerlendi ve buraya yazıldı.

| # | Konu | Şimdilik ne yapıldı |
|---|---|---|
| S-1 | **TCMB hangi kuru?** Dört değer yayınlanıyor: döviz alış/satış, efektif alış/satış. Seçim müşterinin ödeyeceği tutarı değiştiriyor — bugün EUR alış 55,99 satış 56,09, yani €500'lük turda ~50 TL fark | **`ForexSelling`** (döviz satış). Gerekçe: yabancı para borcunu TL'ye çevirmenin standardı ve platform lehine ihtiyatlı |
| S-2 | **Parola kuralı ne olsun?** Şu an hiçbir kural yoktu; `"1"` bile kabul ediliyordu ve bu, PBKDF2'nin 100.000 turunu anlamsızlaştırıyordu | **En az 10 karakter**, karmaşıklık zorunluluğu YOK. Gerekçe: uzunluk tek başına en etkili ölçüt; "büyük harf + rakam + sembol" şartı kullanıcıyı `Parola1!` gibi tahmin edilebilir kalıplara itiyor |
| S-3 | **Hız sınırı ne olsun?** Kullanıcı bazlı saatte 3 jeton vardı ama saldırgan farklı adreslerle sınırsız istek atabiliyordu | **IP başına 15 dakikada 10 istek** (hesap uçlarında). Gerekçe: gerçek kullanıcı bu sayıya normalde ulaşmıyor, bombalama ulaşıyor |
| S-4 | **E-posta değiştirmede mevcut parola isteniyor.** UX'i biraz zorlaştırıyor ama denetimin gösterdiği hesap ele geçirme zincirini kırıyor | Zorunlu yapıldı. İstemezsen kaldırılır ama zincir yeniden açılır |
| S-5 | **Başarısız girişte e-posta adresi olay günlüğüne yazılmıyor.** Suistimal analizi için "hangi adres denendi" değerli olurdu, ama tablo değişmez ve süresiz saklanıyor — giren kişisel veri asla silinemez | Yalnız sebep yazılıyor (`unknown_user` / `bad_password`). İstersen adres de eklenir ama **geri alınamaz** |
| S-6 | **Olay günlüğü hangi ayrıntıya kadar tutulsun?** Şu an kimlik olayları ve terk edilen ödeme var. Arama sorguları, tekne görüntülemeler ve oturum takibi büyük hacim ve daha fazla kişisel veri demek | Şimdilik dar tutuldu. AI raporları için hangi verinin gerçekten gerektiğini sen bilirsin → `A-21` |
| S-7 | **Kuponun matrahı ne?** İndirim yalnız tur bedeline mi, yoksa tur + ek hizmet toplamına mı uygulansın? 1000 TL tur + 500 TL menüde %10 kupon: birincisinde 100 TL, ikincisinde 150 TL indirim | **Tur + ek hizmet.** Gerekçe: komisyon matrahı da tur + menü + ek hizmet. İki oran ayrı tabana uygulansaydı "kupon komisyonu aşamaz" kuralı karşılaştırdığı şeyler farklı olduğu için anlamını yitirirdi |
| S-8 | **Fiyat sorgulama ucunda hız sınırı kaç olsun?** Uç kimliksiz kalmalı — müşteri fiyatı üye olmadan görmeli. Ama sınırsızken kupon kodu denemek bedavaydı | **IP başına dakikada 60 istek** kondu (denendi: 61. istek 429). Hesap uçlarının 15 dk / 10 sınırı buraya çok dardı; 60 bol tutuldu, daraltmak istersen tek satır |

## 🟢 Doğrulanmış

- `dotnet build` — 0 uyarı, 0 hata
- `GET /api/health` yanıt veriyor
- `POST /api/pricing/quote` — istemci `grandTotalTry:1` ve `discountAmountTry:9999` gönderdi, sunucu **1000.00** ve **0** döndü (2026-08-24)
- Denetimde canlı üretilen dört açık kapatıldı ve **yeniden denendi**: taşan
  kişi sayısı, `int.MaxValue` gece, takvim sonu tarih, 200.000 satırlık ek
  hizmet — dördü de artık HTTP 400 (2026-08-24)
- Production kipinde beklenmeyen hata `{"error":"Beklenmeyen bir hata oluştu."}`
  dönüyor, yığın izi sızmıyor
- **42 test, 42'si geçiyor**
- Repo `mertagralii/DailyCruising.API` (private), push edildi

İlgili: [[durum]] · [[api-sema]] · [[api-gorevler]] · [[api-kararlar]] · [[api-desenler]] · [[api-araclar]] · [[api-notlar]] · [[domain-gereksinimler]]
