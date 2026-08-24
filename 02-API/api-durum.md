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

**Şema çıkarma sürüyor.** `A-01` sekiz bölüme ayrıldı; her bölüm Mert'in onayından
geçiyor, onaysız kod yazılmıyor → [[api-sema]]

| # | Bölüm | Durum |
|---|---|---|
| 1 | Kimlik ve yetki | ✅ onaylandı 2026-08-24 |
| 2 | Katalog | ✅ onaylandı 2026-08-24 |
| 3 | Kiralama tipleri ve fiyat | ✅ onaylandı 2026-08-24 |
| 4 | Takvim ve sefer | ✅ onaylandı 2026-08-24 |
| 5 | Rezervasyon | ✅ onaylandı 2026-08-24 |
| 6 | Para | 🟡 tasarlandı, toplu onay bekliyor |
| 7 | Teklif ve mesajlaşma | 🟡 tasarlandı, toplu onay bekliyor |
| 8 | Yan sistemler + olay günlüğü | 🟡 tasarlandı, toplu onay bekliyor |

Kod tarafında iskelet kurulu, **iş kodu henüz yok**. Dört katman oluşturuldu ama
üçü bilinçli boş — şema onaylanmadan doldurulmayacak → [[api-kararlar]] 2026-08-21.
Çalışan tek uç: `GET /api/health` → `{"status":"healthy"}`.

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

## 🟢 Doğrulanmış

- `dotnet build` — 0 uyarı, 0 hata
- `GET /api/health` yanıt veriyor
- Repo `mertagralii/DailyCruising.API` (private), push edildi

İlgili: [[durum]] · [[api-sema]] · [[api-gorevler]] · [[api-kararlar]] · [[api-desenler]] · [[api-araclar]] · [[api-notlar]] · [[domain-gereksinimler]]
