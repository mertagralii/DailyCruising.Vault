---
rol: not
kapsam: api
guncelleme: 2026-08-30
durum: guncel
---

# Uç envanteri — web panosundaki 12 iş için ölçüm (2026-08-30)

Arayüz oturumu Mert'ten "panodaki tüm işleri bitir, ama başlamadan önce
backend'e sor" hedefini aldı ve 12 kalem için uç sordu. Cevaplar
**openapi.json (91 yol) ve canlı ölçümle** verildi, kod okunarak değil.

## Ucu OLMAYANLAR — gerçek eksikler

| İhtiyaç | Durum |
|---|---|
| İşletmenin **kendi rezervasyonları** | uç **yok**. `GET /api/reservations` müşteri bazlı (`Where(r => r.UserId == userId)`) |
| İşletme **profil/ayar yazma** | uç **yok**; `PUT /api/partner/...` diye bir şey yok |
| Genel bakış sayıları (tur, doluluk) | yalnız `finance/summary` var |
| Favoriler | uç yok, **tablo da yok** |
| Bildirim tercihleri | uç yok, **tablo da yok** |
| Kuponlar | **tablo VAR** (`Coupons`, `CouponRedemptions`), uç yok |
| Yorum yanıtını düzenleme/silme | yalnız `POST .../reply` — **tek atış** |
| Yönetim panelinin 9 modülü | müşteriler, personel, kuponlar, bölgeler, reklam, e-posta, SMS, log, aktivite |

Favoriler ve bildirim tercihleri **şema işi** — tablo eklemek Mert'in
haberi olması gereken bir karar.

## Ölçülen davranışlar

- **Ortalama puan moderasyondan sonra ANINDA güncelleniyor**, iş beklemiyor:
  `trg_review_sync_boat_rating` tetikleyicisi
  `AFTER INSERT OR DELETE OR UPDATE OF "Status", "Rating", "BoatId"`.
  Arayüz "birazdan güncellenecek" DEMEMELİ.
- **Reddedilen yorum işletmeye görünmüyor**: `ListForPartnerAsync`
  `Status != Rejected` süzüyor. Müşteriye açık liste ise yalnız `Approved`.
- **Tekne güncelleme kısıtsız**: bölge + kapasite + kaptan değişimi `204`;
  geçersiz bölge `400 UnknownLookup`.

## İki uçta da TAM DEĞİŞTİRME var

`PUT /api/partner/boats/{id}` ve kiralama tipi kaydetme, gönderilen gövdeyi
kaydın TAMAMI kabul ediyor. Önce `GET` edip üstüne yazılmazsa gönderilmeyen
alanlar sıfırlanır. Kiralama tipinde bu bir veri kaybına yol açıyordu →
`A-71`, [[api-yazilmis-ama-uygulanmamis-kontrol]]

## Görüş: finans ekranı bugün açılabilir

`W-35` için uçlar gerçek veri döndürüyor; defter ve komisyon doğru. Yalan
olan tek şey **paranın işletmeye gitmiş olması** — tahsilat platform
hesabında, transfer elle. "Hakediş: ₺X" doğru, "Ödendi" yanlış. Durum
rozeti + tek satır açıklamayla ekran açılabilir; `A-41` gelince rozet
değişir, ekran değişmez. Bölümü tümden kapatmak işletmeye kendi parasını
göstermemek demek.

→ [[api-notlar]] · [[api-durum]] · [[api-gorevler]]
