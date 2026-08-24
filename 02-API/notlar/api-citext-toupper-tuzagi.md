---
rol: not
kapsam: api
guncelleme: 2026-08-24
durum: guncel
---

# `citext` kolonda `ToUpper()` — indeksi öldüren refleks

MSSQL'de kolon zaten harf duyarsız harmanlamalıdır ve `WHERE Code = @code`
büyük/küçük fark etmeden çalışır. Postgres'te varsayılan **duyarlıdır**, o
yüzden bu depoda kupon ve e-posta kolonları `citext` tipinde.

Sorun şu: `citext` olduğunu bilmeyen (ya da o an unutan) biri refleksle
şunu yazıyor:

```csharp
.FirstOrDefaultAsync(c => c.Code.ToUpper() == code.ToUpper(), ct);
```

Bu **iki kere yanlış**. Harf duyarsızlığı zaten kolondan geliyor, yani
`ToUpper()` hiçbir şey eklemiyor. Üstelik EF bunu `upper("Code") = ...`
diye çeviriyor ve `IX_Coupons_Code` **kullanılamaz** hale geliyor: indeks
`"Code"` üzerinde, sorgu `upper("Code")` üzerinde.

## Ölçüm

```
explain select 1 from "Coupons" where upper("Code")=upper('A04GECERLI');
  Seq Scan on "Coupons"  (cost=0.00..17.20 rows=2 width=4)

explain select 1 from "Coupons" where "Code"='a04gecerli';
  Index Only Scan using "IX_Coupons_Code"  (cost=0.15..8.17 rows=1 width=4)
```

İkinci sorgu küçük harfle yazılmasına rağmen `A04GECERLI` kaydını buluyor —
`citext`in yaptığı iş tam olarak bu.

## Neden önemli

Bu sorgu kimliksiz, herkese açık fiyat sorgulama ucunda çalışıyor. Kupon
tablosu bugün iki satır; kampanya biriktikçe her fiyat sorgusu tabloyu baştan
sona tarar hale gelirdi ve **hiçbir test bunu yakalamazdı** — sonuç doğru,
yalnız yavaş.

## Kural

`citext` kolonda **asla** `ToUpper()`/`ToLower()` yazma. Düz eşitlik yeter.
Aynı tuzak `Users.Email` için de geçerli.

## Genel ders

Fonksiyonla sarmalanmış kolon indeksi kullanamaz — bu Postgres'e özgü değil,
MSSQL'de de aynı (orada "non-sargable" deniyor). Postgres'e özgü olan kısım,
`citext` sayesinde sarmalamaya **hiç gerek olmaması**.

İlgili: [[api-notlar]] · [[api-kararlar]] · [[api-desenler]] · [[api-sema]]
