---
rol: status
kapsam: web
guncelleme: 2026-08-24
durum: guncel
---

# Web Durumu

> **Bu dosyanın sahibi `DailyCruising.Front-End/` içinde çalışan oturumdur.**
> Web tarafının güncel durumu buraya yazılır; `01-Genel/durum.md`'ye **yazılmaz**.
> Genel dosya bu dosyayı özetler → [[durum]]

## ✅ Tasarım bitti (2026-08-24)

19 ekranın tamamı uygulandı, ölçüldü ve doğrulandı. `isBreak` hariç — kırılım
vitrini, gerçek sayfa değil; mobil şartnamesi oradan çıkarıldı.

| Alan | Masaüstü (1280) | Mobil (390) |
|---|---|---|
| 16 misafir/hesap sayfası | 12'si birebir, kalanı ≤4px | taşma yok |
| Yönetim paneli (24 modül) | 19'u birebir · 18px | taşma yok |
| Destek paneli (4 bölüm) | 12px | taşma yok |
| İşletme paneli (10 bölüm) | 4'ü birebir · 16px | taşma yok |

Kalan sapmaların ortak kaynağı koyu başlık bandındaki kicker satırı (+2px, üç
panelde de aynı). Metin farkı yalnızca iki bilinçli sapma: tasarımdaki bozuk `i̇`
karakteri ve gerçek `<input placeholder>` kullanımı → [[web-kararlar]]

## 🔜 Sıradaki iş

**API bekleniyor.** Mert backend'i geliştiriyor, bitince haber verecek. O gelince:

1. `src/lib/data/*.ts` mock verisi gerçek uçlarla değişir (`W-04`)
2. Kimlik doğrulama bağlanır — paneller şu an herkese açık
3. Rezervasyon toplamı sunucuda doğrulanır

API beklerken yapılabilecek iki iş var, ikisi de Mert'e bağlı: gerçek görseller
(`W-03`) ve `brand.ts` kurumsal verileri (`W-06`).

## 🟡 Karara bağlanmamış — web

| Konu | Durum | Not |
|---|---|---|
| Gövde satır yüksekliği | Tasarımdan farklı | `globals.css` gövdeye 26px sabit veriyor, tasarım `normal` kullanıyor. Açık `leading-` verilmeyen küçük metinler şişiyor. Tek tek düzeltiliyor; global değişiklik 19 sayfayı birden etkileyeceği için yapılmadı |
| Gerçek görseller | Yok | Her yerde gradyan yer tutucu (`Placeholder`). Tasarımda da öyleydi ama yayın için gerçek fotoğraf şart |
| `brand.ts` kurumsal verileri | Yer tutucu | Telefon, e-posta, adres, TÜRSAB no tasarımdan geldi. Yayın öncesi doğrulanmalı |
| `/design-system` rotası | Yayına çıkıyor | Bileşen vitrini; geliştirme sayfası olduğu hâlde derlemede statik rota olarak üretiliyor. Yayın öncesi kaldırılmalı veya korunmalı → [[web-mimari]] |
| Frontend↔API sözleşmesi | Yok | OpenAPI üretiliyor ama istemci tarafında tip üretimi yok → `A-07` (API panosunda, web değil) |

## ⚠️ Hata değil — bilinçli davranış

Bunlar rapor edilirse "bug" sanılmasın:

- **1180px üstünde geniş tablolar kartın dışına taşar.** Tasarım da böyle yapıyor;
  sütun genişlikleri tasarımla birebir aynı, dolayısıyla taşma miktarı da aynı.
  Kaydırma kabı yalnızca dar ekranda devrede (`wide:overflow-x-visible`)
  → [[web-kararlar]]
- **Hesabım sayfası tasarımdan 18px uzun.** "Daily Cruising puanı" istatistik
  kartında iki satıra sarıyor, tasarımdaki "Rıhtım puanı" tek satır. Marka adı
  uzunluğunun sonucu → [[web-olcum-yanlis-pozitifleri]]

## 🟢 Doğrulanmış

- `npm run build` başarılı, `npm run lint` temiz
- Mobil kırılım 19 rotada 390px'te tarandı, yatay taşma yok; 834px'te iki kart.
  Ölçüm **Playwright** ile yapıldı — `chrome-devtools` `resize_page` 390'a inemiyor
  → [[web-tasarimi-tarayicida-acmak]]
- Tüm çalışma `origin/main`'de — son commit `eb40c7e`

İlgili: [[durum]] · [[web-gorevler]] · [[web-kararlar]] · [[web-desenler]] · [[web-araclar]] · [[web-notlar]]
