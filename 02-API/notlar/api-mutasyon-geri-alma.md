---
rol: not
kapsam: api
guncelleme: 2026-09-11
durum: guncel
---

# Mutasyon geri alınmadı, koruma kapalı kaldı

## Ne oldu

İki korumayı aynı anda mutasyona uğrattım:

- `RefundService` — sağlayıcıya gitmeden duran erken tavan kontrolü
- `LedgerService` — `if (refund.AmountTry > kalan)` son güvence

İkisini **tek bash çağrısında** `if (false)` yaptım. Sonra `RefundService`'i
`git checkout src/.../RefundService.cs` ile geri aldım — ve bu komut
mutasyonla birlikte **o dosyadaki gerçek değişikliklerimi de** sildi. Onları
elle yeniden yazdım.

`LedgerService`'in mutasyonu geri alınmadı. Fark etmedim çünkü:

- `dotnet test --filter "FullyQualifiedName~RefundTests"` **yeşildi** — o
  dosyada mutasyona değen test yok,
- kusuru gösteren test başka sınıfta (`LedgerTests`).

Tam test koşusu yakaladı: `Başarısız: 1, Başarılı: 762`.

## Neden yazılıyor

⚠️ **Tehlikeli olan mutasyonun kendisi değil, geri almanın ölçülmemesi.**
Mutasyon testi bir korumayı bilerek kırıyor; geri alma adımı unutulursa geriye
**kapalı bir koruma ve yeşil bir test süiti** kalıyor. Commit atılsaydı
kimsenin göreceği bir iz olmayacaktı.

Üç somut ders:

1. **Aynı anda tek mutasyon.** İki koruma birlikte kırılırsa hangi testin
   hangisini ölçtüğü de anlaşılmıyor — nitekim ilk koşuda yalnız bir test
   kırmızıya döndü ve ikinci korumanın ölçülüp ölçülmediği belirsiz kaldı.
   Ayrı ayrı kırınca ikisinin de kendi testi olduğu görüldü.
2. **`git checkout <dosya>` mutasyon geri alma aracı DEĞİL.** Commit'lenmemiş
   gerçek işi de götürüyor. Yedek al (`cp` → `/tmp`), yedekten dön.
3. **Mutasyondan sonra dar filtreyle değil TAM süitle koş.** Dar koşu
   "mutasyon geri alındı" sorusunu değil "bu dosyanın testleri geçiyor mu"
   sorusunu cevaplıyor. → [[api-yazilmis-ama-uygulanmamis-kontrol]]

## Ölçüm

    grep -n "if (false)" src/DailyCruising.Application/Billing/LedgerService.cs

Mutasyon çalışması bittiğinde bu komut **hiçbir şey döndürmemeli**.

İlgili: [[api-notlar]] · [[api-kararlar]]
