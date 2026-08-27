---
rol: note
kapsam: api
guncelleme: 2026-08-24
durum: guncel
---

# Rezervasyonun süresi dolunca SEFER de bırakılmalı

Koltuğu bırakmak yetmiyor. `ExpireReservationHoldsJob` rezervasyonu `Expired`'a
çekiyor, `trg_reservation_sync_seats` koltukları geri veriyor — ama seferin
kendisi `Planned` kalıyordu.

Neden ölümcül: takvimi koruyan kısıt `Reservation`'a değil **`Voyage`'a** bakıyor.

```sql
EXCLUDE USING gist ("BoatId" WITH =, tstzrange("StartsAt","EndsAt",'[)') WITH &&)
  WHERE ("Status" <> 'Cancelled')      -- Voyage.Status, Reservation.Status DEĞİL
```

Yani rezervasyon ölse de sefer takvimi işgal etmeye devam ediyordu.

## Sonuç: kimliksiz, bedava takvim kilidi

Özel (çarter) turda her rezervasyon **kendi seferini açıyor**. Saldırgan:

1. Kimliksiz `POST /api/reservations` atar — ödeme adımı yok, 201 döner.
2. Ödemeyi hiç yapmaz.
3. 15 dakika sonra rezervasyon `Expired` olur, **sefer `Planned` kalır**.
4. O tekne o tarih aralığında **turun bitişine kadar** satılamaz.

Hız sınırı bunu yavaşlatmıyor: 15 dakikada 10 istek, 10 ayrı tarih demek. Bir
teknenin üç aylık takvimi birkaç saatte, tek IP'den, tek kuruş ödenmeden
kapatılabiliyordu.

**Canlı üretildi (2026-08-24):** 10–13 Ekim çarteri terk edildi, rezervasyon
`Expired` / sefer `Planned` kaldı, aynı tarihe yeni istek **409** aldı.

## Düzeltme

Süre dolunca, seferde **canlı rezervasyon kalmadıysa** sefer de `Cancelled`
oluyor. Kilit noktalar:

- **`SoldSeats`'e bakılmaz.** Bebek koltuk tüketmediği için yalnız bebekli bir
  rezervasyonda sayaç 0'dır ama rezervasyon canlıdır. Rezervasyon
  DURUMLARINA bakılıyor.
- **Paylaşımlı seferde bir kişinin vazgeçmesi seferi iptal etmez.** Düzeltmenin
  fazla geniş yazılması tam bunu bozardı ve hiçbir kısıt yakalamazdı — ayrı bir
  test bunu sabitliyor.
- Filtre `trg_reservation_sync_seats` ve `count_live_coupon_redemptions` ile
  **aynı** liste: `Pending, Paid, Boarded, Completed`. Üçü de "satış hâlâ ayakta
  mı" diye soruyor; biri kayarsa diğerleriyle sessizce çelişir.

## Asıl ders

Bu hata sınıfı **daha önce çözülmüştü**: `ExpireOffersJob` tam olarak aynı şeyi
teklifler için yapıyor ve dosyanın başındaki yorum sorunu tarif ediyor.
A-22 yazılırken o desen fark edilmedi ve hata tekrarlandı.

> Takvimi işgal eden bir satır yaratan her kod yolu, onu **bırakan** yolu da
> yazmak zorunda. `Voyage` yaratan bir yer varsa, `Voyage`'ı `Cancelled`'a
> çeken bir yer de olmalı.

Bugün `Voyage` yaratan iki yer var: `ExpireOffersJob`'un beslediği teklif akışı
ve `ReservationRepository`. İptal ucu (`A-24`) yazılırken aynı sorunun üçüncü
kez doğmaması için bırakma mantığı ortak bir yere alınmalı.

İlgili: [[api-notlar]] · [[api-sema]] · [[api-kararlar]] · [[api-olay-gunlugu-iptal-jetonu]]
