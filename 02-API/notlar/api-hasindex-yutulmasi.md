---
rol: not
kapsam: api
guncelleme: 2026-08-24
durum: guncel
---

# Aynı kolona ikinci `HasIndex` birincisini yutuyor

`api-desenler`'deki "kısmi indeks" deseni bu tuzağı doğuruyor: bir kolona hem
düz indeks hem kısmi benzersiz indeks istendiğinde, EF ikisini **tek indeks**
sayıyor ve düz olan hiç yaratılmıyor.

## Yutan kod

```csharp
b.HasIndex(x => x.BoatRentalTypeId);          // ← sessizce kayboluyor

b.HasIndex(x => x.BoatRentalTypeId)
    .IsUnique()
    .HasFilter("\"ValidFrom\" IS NULL")
    .HasDatabaseName("IX_Prices_SingleBasePrice");
```

Sonuç: veritabanında yalnız `IX_Prices_SingleBasePrice` var. Aynı hata
`Contracts.PartnerId` için de yapılmıştı — hem de yanına **"bu sorgu kısmi
indeksi kullanamaz"** yorumu yazılarak. Yorum ihtiyacı doğru anlatıyordu,
indeks yoktu.

## `HasDatabaseName` eklemek YETMİYOR

İlk denemem buydu:

```csharp
b.HasIndex(x => x.BoatRentalTypeId)
    .HasDatabaseName("IX_Prices_BoatRentalTypeId");   // hâlâ yutuluyor
```

`dotnet ef migrations add` **boş migration** üretti. İkinci çağrının
`HasDatabaseName`'i birincininkini eziyor; çağrılar hâlâ aynı indeksi
yapılandırıyor sayılıyor.

## Çalışan biçim

Ad, **ikinci parametre** olarak verilmeli — indeksi baştan ayrı kimlikle
tanımlayan aşırı yükleme bu:

```csharp
b.HasIndex(x => x.BoatRentalTypeId, "IX_Prices_BoatRentalTypeId");
```

Bundan sonra migration üçünü de üretti ve `pg_indexes` üçünü de gösterdi.

## Nasıl yakalanır

Derleme temiz, testler geçer, sorgular doğru sonuç verir — **yalnız yavaş**.
Tek güvenilir kontrol veritabanına bakmak:

```sql
select indexname, indexdef from pg_indexes where tablename='Prices';
```

Yapılandırmada sayılan indeks sayısı ile buradaki sayı tutmuyorsa fark budur.

İlgili: [[api-notlar]] · [[api-desenler]] · [[api-citext-toupper-tuzagi]] · [[api-sema]]
