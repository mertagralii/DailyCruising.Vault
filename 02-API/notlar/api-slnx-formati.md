---
rol: not
kapsam: api
guncelleme: 2026-08-21
durum: guncel
---

# .slnx solution formatı

`dotnet new sln` .NET 10'da klasik `.sln` değil, **`DailyCruising.slnx`** üretti —
XML tabanlı yeni format.

## Neden önemli

- Eski araçlar ve bazı CI şablonları hâlâ `*.sln` arıyor. `find . -name "*.sln"`
  yazan bir script bu projede **hiçbir şey bulamaz**.
- Visual Studio / Rider sürümüne göre destek değişebilir. Mert bir IDE'de açamazsa
  ilk şüpheli budur.
- `dotnet build` ve `dotnet sln add` sorunsuz çalışıyor — CLI tarafında sorun yok,
  bu doğrulandı.

## Kaçış yolu

Gerekirse klasik formata dönüştürülebilir; ancak `.slnx` bilinçli bir tercih değil,
şablonun varsayılanıydı. Bir sorun çıkmadıkça dokunmaya gerek yok.

İlgili: [[api-notlar]] · [[api-mimari]] · [[api-webapi-sablon-tuzaklari]]
