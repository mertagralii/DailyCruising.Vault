---
rol: map
kapsam: api
guncelleme: 2026-08-24
durum: guncel
---

# API Araçları

`DailyCruising.Back-End/` altında çalışırken **hangi durumda hangi aracı** kullanacağım.

Gerekçesiz araç satırı eklenmez.

| Tetikleyici | Araç | Neden |
|---|---|---|
| C# kodu yazdım veya değiştirdim | `ecc:csharp-reviewer` ajanı | async doğruluğu, nullable referans tipleri, .NET konvansiyonları |
| Şema, migration veya sorgu yazılacak | `ecc:database-reviewer` ajanı | İndeks, kısıt ve performans hataları en pahalı düzeltilen hatalar |
| PostgreSQL'e özgü bir şey yapılacak | `ecc:postgres-patterns` skill'i | PascalCase tırnak davranışı gibi Postgres'e özgü tuzaklar var -> [[api-desenler]] |
| Kimlik doğrulama, yetki veya ödeme kodu yazıldı | `ecc:security-reviewer` ajanı | Satır bazlı yetki ve fiyat doğrulaması bu projenin iki bilinen güvenlik riski -> [[durum]] |
| Build hatası aldım | `ecc:build-error-resolver` ajanı | Dar kapsamlı, mimariye dokunmayan düzeltme |
| EF Core / .NET 10 API'si soruldu | `context7` MCP | .NET 10 ve `.slnx` yeni; eğitim verim bayat olabilir -> [[api-slnx-formati]] |
| Test yazılacak | `ecc:csharp-testing` skill'i | xUnit projesi henüz yok; kurulunca biçim buradan |
| Domain modeli tasarlanacak | `superpowers:brainstorming` | A-01 çıkarımla değil konuşularak tasarlanacak -> [[api-gorevler]] |

## Dikkat

- **Rider MCP kurulu.** IDE üzerinden çalışma gerekirse mevcut; ama derleme ve test
  için `dotnet` CLI yeterli, önce o denenir
- Domain soruları cevaplanmadan şema kuran araç yok — eksik olan bilgi, araç değil

İlgili: [[api-notlar]] · [[api-desenler]] · [[api-mimari]] · [[api-gorevler]] · [[genel-araclar]]
