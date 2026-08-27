---
rol: not
kapsam: api
guncelleme: 2026-08-26
durum: guncel
---

# "Eşzamanlı iki istek" testi çoğu zaman yarışmıyor

Yarış koşulunu koruyan bir kısıt yazdıktan sonra refleks olarak şöyle bir test
yazılıyor:

```csharp
var gorevler = new[]
{
    Servis(db1).IadeAsync(kod, ...),
    Servis(db2).IadeAsync(kod, ...)
};
// biri başarılı, biri hata bekleniyor
```

**Bu test kısıtı ölçmüyor.** İki görev pratikte sırayla koşuyor: ikincisi
başladığında birincisi çoktan bitmiş oluyor ve ikinci istek veritabanı kısıtına
DEĞİL, servisteki durum kontrolüne takılıyor. Sonuç yine "biri başarılı, biri
hata" — test yeşil, ama kanıtladığı şey kısıt değil.

## Nasıl ölçüldü

`A-29b`'de `UX_Refunds_ReservationId_Aktif` kısmi benzersiz indeksi
migration'dan tamamen çıkarıldı:

| Test | İndeks var | İndeks yok |
|---|---|---|
| `Escaman_iki_iade_veritabaninda_kesiliyor` | yeşil | **yeşil** |
| `Ayni_rezervasyona_ikinci_aktif_iade_satiri_veritabaninda_kesiliyor` | yeşil | **kırmızı** |

Yani sekiz testlik paketin tamamı, kapıyı söktükten sonra da yeşil kalıyordu.

## Kural

**Bir veritabanı kısıtını, o kısıtı doğrudan ihlal eden bir yazmayla test et.**
Aynı satırı iki ayrı `DbContext`'ten ekle ve `23505` + kısıt adını bekle —
`PostgresHatalari.BekleKisit`. Servis üzerinden geçen eşzamanlılık testi
faydalı olabilir ama **kısıtın kanıtı değildir**; onu ancak servis kontrolünün
kaldırıldığı bir mutasyon kanıtlar.

Bu, `api-desenler`'deki "mutasyonu doğru yere koy" kuralının ikinci yüzü:
mutasyon doğru yerdeydi (migration kaynağı, canlı veritabanı değil) ama
**testin kendisi yanlış şeyi ölçüyordu**.

İlgili: [[api-hasindex-yutulmasi]] · [[api-aralikla-silme-tuzagi]] · [[api-desenler]] · [[api-kararlar]]
